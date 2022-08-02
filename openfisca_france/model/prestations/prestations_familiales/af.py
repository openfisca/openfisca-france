from numpy import logical_or as or_

from openfisca_france.model.base import *
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf


class af_nbenf(Variable):
    value_type = int
    entity = Famille
    label = "Nombre d'enfants dans la famille au sens des allocations familiales"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period):
        prestations_familiales_enfant_a_charge_i = famille.members('prestations_familiales_enfant_a_charge', period)
        af_nbenf = famille.sum(prestations_familiales_enfant_a_charge_i)

        return af_nbenf


class af_coeff_garde_alternee(Variable):
    value_type = float
    default_value = 1
    entity = Famille
    label = 'Coefficient à appliquer aux af pour tenir compte de la garde alternée'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula_2007_05_01(famille, period):
        nb_enf = famille('af_nbenf', period)
        garde_alternee = famille.members('garde_alternee', period)
        pfam_enfant_a_charge = famille.members('prestations_familiales_enfant_a_charge', period)

        # Le nombre d'enfants à charge en garde alternée, qui vérifient donc pfam_enfant_a_charge = true et garde_alternee = true
        nb_enf_garde_alternee = famille.sum(garde_alternee * pfam_enfant_a_charge)

        # Avoid division by zero. If nb_enf == 0, necessarily nb_enf_garde_alternee = 0 so coeff = 1
        coeff = 1 - (nb_enf_garde_alternee / (nb_enf + (nb_enf == 0))) * 0.5

        return coeff


class af_allocation_forfaitaire_nb_enfants(Variable):
    value_type = int
    entity = Famille
    label = "Nombre d'enfants ouvrant droit à l'allocation forfaitaire des AF"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period, parameters):
        af = parameters(period).prestations_sociales.prestations_familiales.prestations_generales.af
        af_forfaitaire_nbenf = nb_enf(famille, period, af.af_cm.age3, af.af_cm.age3)

        return af_forfaitaire_nbenf


class af_eligibilite_base(Variable):
    value_type = bool
    entity = Famille
    label = 'Allocations familiales - Éligibilité pour la France métropolitaine sous condition de ressources'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period):
        residence_dom = famille.demandeur.menage('residence_dom', period)
        af_nbenf = famille('af_nbenf', period)

        return not_(residence_dom) * (af_nbenf >= 2)


class af_eligibilite_dom(Variable):
    value_type = bool
    entity = Famille
    label = 'Allocations familiales - Éligibilité pour les DOM (hors Mayotte) sous condition de ressources'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period):
        residence_dom = famille.demandeur.menage('residence_dom', period)
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)
        af_nbenf = famille('af_nbenf', period)

        return residence_dom * not_(residence_mayotte) * (af_nbenf >= 1)


class af_base(Variable):
    value_type = float
    entity = Famille
    label = 'Allocations familiales - allocation de base'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    # prestations familiales (brutes de crds)

    def formula(famille, period, parameters):
        eligibilite_base = famille('af_eligibilite_base', period)
        eligibilite_dom = famille('af_eligibilite_dom', period)
        af_nbenf = famille('af_nbenf', period)

        af = parameters(period).prestations_sociales.prestations_familiales.prestations_generales.af
        bmaf = parameters(period).prestations_sociales.prestations_familiales.bmaf.bmaf

        eligibilite = or_(eligibilite_base, eligibilite_dom)

        un_seul_enfant = (
            eligibilite_dom
            * (af_nbenf == 1)
            * af.af_maj_dom.allocations_familiales_un_enfant
            )

        deux_enfants = (af_nbenf >= 2) * af.af_cm.taux.enf2
        plus_de_trois_enfants = max_(af_nbenf - 2, 0) * af.af_cm.taux.enf3
        taux_total = un_seul_enfant + deux_enfants + plus_de_trois_enfants
        montant_base = eligibilite * round_(bmaf * taux_total, 2)
        coeff_garde_alternee = famille('af_coeff_garde_alternee', period)
        montant_base = montant_base * coeff_garde_alternee

        af_taux_modulation = famille('af_taux_modulation', period)
        montant_base_module = montant_base * af_taux_modulation

        return montant_base_module


class af_taux_modulation(Variable):
    value_type = float
    default_value = 1
    entity = Famille
    label = 'Taux de modulation à appliquer au montant des AF depuis 2015'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula_2015_07_01(famille, period, parameters):
        nb_enf_tot = famille('af_nbenf', period)

        return taux_helper(famille, period, parameters, nb_enf_tot)


class af_allocation_forfaitaire_taux_modulation(Variable):
    value_type = float
    default_value = 1
    entity = Famille
    label = "Taux de modulation à appliquer à l'allocation forfaitaire des AF depuis 2015"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula_2015_07_01(famille, period, parameters):
        af_nbenf = famille('af_nbenf', period)
        af_forfaitaire_nbenf = famille('af_allocation_forfaitaire_nb_enfants', period)
        nb_enf_tot = af_nbenf + af_forfaitaire_nbenf

        return taux_helper(famille, period, parameters, nb_enf_tot)


class af_age_aine(Variable):
    value_type = int
    default_value = -9999
    entity = Famille
    label = "Allocations familiales - Âge de l'aîné des enfants éligibles"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    is_period_size_independent = True

    def formula(famille, period, parameters):
        af = parameters(period).prestations_sociales.prestations_familiales.prestations_generales.af

        age = famille.members('age', period)
        pfam_enfant_a_charge = famille.members('prestations_familiales_enfant_a_charge', period)

        condition_eligibilite = pfam_enfant_a_charge * (age <= af.af_cm.age2)
        age_enfants_eligiles = age * condition_eligibilite

        return famille.max(age_enfants_eligiles, role = Famille.ENFANT)


class af_majoration_enfant(Variable):
    value_type = float
    entity = Individu
    label = "Allocations familiales - Majoration pour âge applicable à l'enfant"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        pfam_enfant_a_charge = individu('prestations_familiales_enfant_a_charge', period)
        age = individu('age', period)
        garde_alternee = individu('garde_alternee', period)

        af_nbenf = individu.famille('af_nbenf', period)
        af_base = individu.famille('af_base', period)
        age_aine = individu.famille('af_age_aine', period)

        af = parameters(period).prestations_sociales.prestations_familiales.prestations_generales.af
        bmaf = parameters(period).prestations_sociales.prestations_familiales.bmaf.bmaf

        montant_enfant_seul = bmaf * (
            (af.af_maj_dom.tranches_age.age_debut_premiere_tranche <= age)
            * (age < af.af_maj_dom.tranches_age.age_debut_deuxieme_tranche)
            * af.af_maj_dom.majoration_premier_enfant.taux_tranche_1
            + (af.af_maj_dom.tranches_age.age_debut_deuxieme_tranche <= age)
            * af.af_maj_dom.majoration_premier_enfant.taux_tranche_2
            )

        montant_plusieurs_enfants = bmaf * (
            (af.af_maj.maj_age_deux_enfants.age1 <= age)
            * (age < af.af_maj.maj_age_deux_enfants.age2)
            * af.af_maj.maj_age_deux_enfants.taux1
            + (af.af_maj.maj_age_deux_enfants.age2 <= age)
            * af.af_maj.maj_age_deux_enfants.taux2
            )

        montant = (af_nbenf == 1) * montant_enfant_seul + (af_nbenf > 1) * montant_plusieurs_enfants

        # Attention ! Ne fonctionne pas pour les enfants du même âge (typiquement les jumeaux...)
        pas_aine = or_(af_nbenf != 2, (af_nbenf == 2) * not_(age == age_aine))

        coeff_garde_alternee = where(garde_alternee, af.af_cm.facteur_garde_alternee, 1)

        return (
            pfam_enfant_a_charge
            * (af_base > 0)
            * pas_aine
            * montant
            * coeff_garde_alternee
            )


class af_majoration(Variable):
    value_type = float
    entity = Famille
    label = 'Allocations familiales - majoration pour âge'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        af_majoration_enfant = famille.members('af_majoration_enfant', period)
        af_majoration_enfants_famille = famille.sum(af_majoration_enfant, role = Famille.ENFANT)

        af_taux_modulation = famille('af_taux_modulation', period)
        af_majoration_enfants_module = af_majoration_enfants_famille * af_taux_modulation

        return af_majoration_enfants_module


class af_complement_degressif(Variable):
    value_type = float
    entity = Famille
    label = 'AF - Complément dégressif en cas de dépassement du plafond'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2015_07_01(famille, period, parameters):
        eligibilite_dom = famille('af_eligibilite_dom', period)
        af_base = famille('af_base', period)
        af_majoration = famille('af_majoration', period)
        af = af_base + af_majoration
        af_nbenf = famille('af_nbenf', period)
        depassement_mensuel = depassement_helper(famille, period, parameters, af_nbenf)

        return (
            not_(eligibilite_dom)
            * (depassement_mensuel > 0)
            * max_(0, af - depassement_mensuel)
            )


class af_allocation_forfaitaire_complement_degressif(Variable):
    value_type = float
    entity = Famille
    label = "AF - Complément dégressif pour l'allocation forfaitaire en cas de dépassement du plafond"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2015_07_01(famille, period, parameters):
        af_nbenf = famille('af_nbenf', period)
        af_forfaitaire_nbenf = famille('af_allocation_forfaitaire_nb_enfants', period)
        nb_enf_tot = af_nbenf + af_forfaitaire_nbenf  # noqa F841

        depassement_mensuel = depassement_helper(famille, period, parameters, af_nbenf)

        af_allocation_forfaitaire = famille('af_allocation_forfaitaire', period)
        return max_(0, af_allocation_forfaitaire - depassement_mensuel) * (depassement_mensuel > 0)


class af_allocation_forfaitaire(Variable):
    value_type = float
    entity = Famille
    label = 'Allocations familiales - forfait'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2003_07_01(famille, period, parameters):
        af_nbenf = famille('af_nbenf', period)
        af_forfaitaire_nbenf = famille('af_allocation_forfaitaire_nb_enfants', period)
        af = parameters(period).prestations_sociales.prestations_familiales.prestations_generales.af
        bmaf = parameters(period).prestations_sociales.prestations_familiales.bmaf.bmaf

        af_forfait = round_(bmaf * af.af_maj.majoration_enfants.allocation_forfaitaire.taux, 2)
        af_allocation_forfaitaire = ((af_nbenf >= 2) * af_forfaitaire_nbenf) * af_forfait

        af_forfaitaire_taux_modulation = famille('af_allocation_forfaitaire_taux_modulation', period)
        af_forfaitaire_module = af_allocation_forfaitaire * af_forfaitaire_taux_modulation

        return af_forfaitaire_module


class af(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = 'Allocations familiales - total des allocations'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2015_07_01(famille, period, parameters):
        af_base = famille('af_base', period)
        af_majoration = famille('af_majoration', period)
        af_allocation_forfaitaire = famille('af_allocation_forfaitaire', period)
        af_complement_degressif = famille('af_complement_degressif', period)
        af_forfaitaire_complement_degressif = famille('af_allocation_forfaitaire_complement_degressif', period)

        return (
            af_base
            + af_majoration
            + af_allocation_forfaitaire
            + af_complement_degressif
            + af_forfaitaire_complement_degressif
            )

    def formula(famille, period, parameters):
        af_base = famille('af_base', period)
        af_majoration = famille('af_majoration', period)
        af_allocation_forfaitaire = famille('af_allocation_forfaitaire', period)

        return af_base + af_majoration + af_allocation_forfaitaire


def plafonds_helper(famille, period, parameters, nb_enf_tot):
    af = parameters(period).prestations_sociales.prestations_familiales.prestations_generales.af
    modulation = af.af_cond_ress

    plafond1 = (
        modulation.plafond_tranche_1_base
        + max_(nb_enf_tot, 0) * modulation.majoration_plafond_par_enfant_supplementaire
        )

    plafond2 = (
        modulation.plafond_tranche_2_base
        + max_(nb_enf_tot, 0) * modulation.majoration_plafond_par_enfant_supplementaire
        )

    return (plafond1, plafond2)


def taux_helper(famille, period, parameters, nb_enf_tot):
    af = parameters(period).prestations_sociales.prestations_familiales.prestations_generales.af
    modulation = af.af_cm.modulation

    base_ressources = famille('prestations_familiales_base_ressources', period)

    plafond1, plafond2 = plafonds_helper(famille, period, parameters, nb_enf_tot)

    taux = (
        (base_ressources <= plafond1) * 1
        + (base_ressources > plafond1) * (base_ressources <= plafond2) * modulation.taux_tranche_2
        + (base_ressources > plafond2) * modulation.taux_tranche_3
        )

    return taux


def depassement_helper(famille, period, parameters, nb_enf_tot):
    base_ressources = famille('prestations_familiales_base_ressources', period)

    plafond1, plafond2 = plafonds_helper(famille, period, parameters, nb_enf_tot)

    depassement_plafond1 = max_(0, base_ressources - plafond1)
    depassement_plafond2 = max_(0, base_ressources - plafond2)

    depassement_mensuel = (
        (depassement_plafond2 == 0) * depassement_plafond1
        + (depassement_plafond2 > 0) * depassement_plafond2
        ) / 12

    return depassement_mensuel
