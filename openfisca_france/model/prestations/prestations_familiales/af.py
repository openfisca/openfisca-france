# -*- coding: utf-8 -*-

from __future__ import division

from numpy import round, logical_or as or_


from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf


class af_nbenf(Variable):
    column = IntCol
    entity = Famille
    label = u"Nombre d'enfants dans la famille au sens des allocations familiales"
    definition_period = MONTH

    def formula(famille, period):
        prestations_familiales_enfant_a_charge_i = famille.members('prestations_familiales_enfant_a_charge', period)
        af_nbenf = famille.sum(prestations_familiales_enfant_a_charge_i)

        return af_nbenf


class af_coeff_garde_alternee(Variable):
    column = FloatCol(default = 1)
    entity = Famille
    label = u"Coefficient à appliquer aux af pour tenir compte de la garde alternée"
    definition_period = MONTH

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
    column = IntCol
    entity = Famille
    label = u"Nombre d'enfants ouvrant droit à l'allocation forfaitaire des AF"
    definition_period = MONTH

    def formula(famille, period, legislation):
        pfam = legislation(period).prestations.prestations_familiales.af
        af_forfaitaire_nbenf = nb_enf(famille, period, pfam.age3, pfam.age3)

        return af_forfaitaire_nbenf


class af_eligibilite_base(Variable):
    column = BoolCol
    entity = Famille
    label = u"Allocations familiales - Éligibilité pour la France métropolitaine sous condition de ressources"
    definition_period = MONTH

    def formula(famille, period):
        residence_dom = famille.demandeur.menage('residence_dom', period)
        af_nbenf = famille('af_nbenf', period)

        return not_(residence_dom) * (af_nbenf >= 2)


class af_eligibilite_dom(Variable):
    column = BoolCol
    entity = Famille
    label = u"Allocations familiales - Éligibilité pour les DOM (hors Mayotte) sous condition de ressources"
    definition_period = MONTH

    def formula(famille, period):
        residence_dom = famille.demandeur.menage('residence_dom', period)
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)
        af_nbenf = famille('af_nbenf', period)

        return residence_dom * not_(residence_mayotte) * (af_nbenf >= 1)


class af_base(Variable):
    column = FloatCol
    entity = Famille
    label = u"Allocations familiales - allocation de base"
    definition_period = MONTH
    # prestations familiales (brutes de crds)

    def formula(famille, period, legislation):
        eligibilite_base = famille('af_eligibilite_base', period)
        eligibilite_dom = famille('af_eligibilite_dom', period)
        af_nbenf = famille('af_nbenf', period)

        pfam = legislation(period).prestations.prestations_familiales.af

        eligibilite = or_(eligibilite_base, eligibilite_dom)

        un_seul_enfant = eligibilite_dom * (af_nbenf == 1) * pfam.af_dom.taux_enfant_seul
        plus_de_deux_enfants = (af_nbenf >= 2) * pfam.taux.enf2
        plus_de_trois_enfants = max_(af_nbenf - 2, 0) * pfam.taux.enf3
        taux_total = un_seul_enfant + plus_de_deux_enfants + plus_de_trois_enfants
        montant_base = eligibilite * round(pfam.bmaf * taux_total, 2)
        coeff_garde_alternee = famille('af_coeff_garde_alternee', period)
        montant_base = montant_base * coeff_garde_alternee

        af_taux_modulation = famille('af_taux_modulation', period)
        montant_base_module = montant_base * af_taux_modulation

        return montant_base_module


class af_taux_modulation(Variable):
    column = FloatCol(default = 1)
    entity = Famille
    label = u"Taux de modulation à appliquer au montant des AF depuis 2015"
    definition_period = MONTH

    def formula_2015_07_01(famille, period, legislation):
        af_nbenf = famille('af_nbenf', period)
        pfam = legislation(period).prestations.prestations_familiales.af
        base_ressources = famille('prestations_familiales_base_ressources', period)
        modulation = pfam.modulation
        plafond1 = modulation.plafond_tranche_1 + max_(af_nbenf - 2, 0) * modulation.majoration_plafond_par_enfant_supplementaire
        plafond2 = modulation.plafond_tranche_2 + max_(af_nbenf - 2, 0) * modulation.majoration_plafond_par_enfant_supplementaire

        taux = (
            (base_ressources <= plafond1) * 1 +
            (base_ressources > plafond1) * (base_ressources <= plafond2) * modulation.taux_tranche_2 +
            (base_ressources > plafond2) * modulation.taux_tranche_3
        )

        return taux


class af_allocation_forfaitaire_taux_modulation(Variable):
    column = FloatCol(default = 1)
    entity = Famille
    label = u"Taux de modulation à appliquer à l'allocation forfaitaire des AF depuis 2015"
    definition_period = MONTH

    def formula_2015_07_01(famille, period, legislation):
        pfam = legislation(period).prestations.prestations_familiales.af
        af_nbenf = famille('af_nbenf', period)
        af_forfaitaire_nbenf = famille('af_allocation_forfaitaire_nb_enfants', period)
        nb_enf_tot = af_nbenf + af_forfaitaire_nbenf
        base_ressources = famille('prestations_familiales_base_ressources', period)
        modulation = pfam.modulation
        plafond1 = modulation.plafond_tranche_1 + max_(nb_enf_tot - 2, 0) * modulation.majoration_plafond_par_enfant_supplementaire
        plafond2 = modulation.plafond_tranche_2 + max_(nb_enf_tot - 2, 0) * modulation.majoration_plafond_par_enfant_supplementaire

        taux = (
            (base_ressources <= plafond1) * 1 +
            (base_ressources > plafond1) * (base_ressources <= plafond2) * modulation.taux_tranche_2 +
            (base_ressources > plafond2) * modulation.taux_tranche_3
            )

        return taux


class af_age_aine(Variable):
    column = AgeCol
    entity = Famille
    label = u"Allocations familiales - Âge de l'aîné des enfants éligibles"
    definition_period = MONTH

    def formula(famille, period, legislation):
        pfam = legislation(period).prestations.prestations_familiales

        age = famille.members('age', period)
        pfam_enfant_a_charge = famille.members('prestations_familiales_enfant_a_charge', period)

        condition_eligibilite = pfam_enfant_a_charge * (age <= pfam.af.age2)
        age_enfants_eligiles = age * condition_eligibilite

        return famille.max(age_enfants_eligiles, role = Famille.ENFANT)


class af_majoration_enfant(Variable):
    column = FloatCol
    entity = Individu
    label = u"Allocations familiales - Majoration pour âge applicable à l'enfant"
    definition_period = MONTH

    def formula(individu, period, legislation):
        pfam_enfant_a_charge = individu('prestations_familiales_enfant_a_charge', period)
        age = individu('age', period)
        garde_alternee = individu('garde_alternee', period)

        af_nbenf = individu.famille('af_nbenf', period)
        af_base = individu.famille('af_base', period)
        age_aine = individu.famille('af_age_aine', period)

        pfam = legislation(period).prestations.prestations_familiales

        montant_enfant_seul = pfam.af.bmaf * (
            (pfam.af.af_dom.age_1er_enf_tranche_1_dom <= age) * (age < pfam.af.af_dom.age_1er_enf_tranche_2_dom) * pfam.af.af_dom.taux_1er_enf_tranche_1_dom +
            (pfam.af.af_dom.age_1er_enf_tranche_2_dom <= age) * pfam.af.af_dom.taux_1er_enf_tranche_2_dom
            )

        montant_plusieurs_enfants = pfam.af.bmaf * (
            (pfam.af.maj_age_deux_enfants.age1 <= age) * (age < pfam.af.maj_age_deux_enfants.age2) * pfam.af.maj_age_deux_enfants.taux1 +
            (pfam.af.maj_age_deux_enfants.age2 <= age) * pfam.af.maj_age_deux_enfants.taux2
            )

        montant = (af_nbenf == 1) * montant_enfant_seul + (af_nbenf > 1) * montant_plusieurs_enfants

        # Attention ! Ne fonctionne pas pour les enfants du même âge (typiquement les jumeaux...)
        pas_aine = or_(af_nbenf != 2, (af_nbenf == 2) * not_(age == age_aine))

        coeff_garde_alternee = where(garde_alternee, pfam.af.facteur_garde_alternee, 1)

        return pfam_enfant_a_charge * (af_base > 0) * pas_aine * montant * coeff_garde_alternee


class af_majoration(Variable):
    column = FloatCol
    entity = Famille
    label = u"Allocations familiales - majoration pour âge"
    definition_period = MONTH

    def formula(famille, period):
        af_majoration_enfant = famille.members('af_majoration_enfant', period)
        af_majoration_enfants_famille = famille.sum(af_majoration_enfant, role = Famille.ENFANT)

        af_taux_modulation = famille('af_taux_modulation', period)
        af_majoration_enfants_module = af_majoration_enfants_famille * af_taux_modulation

        return af_majoration_enfants_module


class af_complement_degressif(Variable):
    column = FloatCol
    entity = Famille
    label = u"AF - Complément dégressif en cas de dépassement du plafond"
    definition_period = MONTH

    def formula_2015_07_01(famille, period, legislation):
        af_nbenf = famille('af_nbenf', period)
        base_ressources = famille('prestations_familiales_base_ressources', period)
        af_base = famille('af_base', period)
        af_majoration = famille('af_majoration', period)
        pfam = legislation(period).prestations.prestations_familiales.af
        modulation = pfam.modulation
        plafond1 = modulation.plafond_tranche_1 + max_(af_nbenf - 2, 0) * modulation.majoration_plafond_par_enfant_supplementaire
        plafond2 = modulation.plafond_tranche_2 + max_(af_nbenf - 2, 0) * modulation.majoration_plafond_par_enfant_supplementaire

        depassement_plafond1 = max_(0, base_ressources - plafond1)
        depassement_plafond2 = max_(0, base_ressources - plafond2)

        depassement_mensuel = (
            (depassement_plafond2 == 0) * depassement_plafond1 +
            (depassement_plafond2 > 0) * depassement_plafond2
        ) / 12

        af = af_base + af_majoration
        return max_(0, af - depassement_mensuel) * (depassement_mensuel > 0)


class af_allocation_forfaitaire_complement_degressif(Variable):
    column = FloatCol
    entity = Famille
    label = u"AF - Complément dégressif pour l'allocation forfaitaire en cas de dépassement du plafond"
    definition_period = MONTH

    def formula_2015_07_01(famille, period, legislation):
        af_nbenf = famille('af_nbenf', period)
        af_forfaitaire_nbenf = famille('af_allocation_forfaitaire_nb_enfants', period)
        pfam = legislation(period).prestations.prestations_familiales.af
        nb_enf_tot = af_nbenf + af_forfaitaire_nbenf
        base_ressources = famille('prestations_familiales_base_ressources', period)
        af_allocation_forfaitaire = famille('af_allocation_forfaitaire', period)
        modulation = pfam.modulation
        plafond1 = modulation.plafond_tranche_1 + max_(af_nbenf - 2, 0) * modulation.majoration_plafond_par_enfant_supplementaire
        plafond2 = modulation.plafond_tranche_2 + max_(af_nbenf - 2, 0) * modulation.majoration_plafond_par_enfant_supplementaire

        depassement_plafond1 = max_(0, base_ressources - plafond1)
        depassement_plafond2 = max_(0, base_ressources - plafond2)

        depassement_mensuel = (
            (depassement_plafond2 == 0) * depassement_plafond1 +
            (depassement_plafond2 > 0) * depassement_plafond2
        ) / 12

        return max_(0, af_allocation_forfaitaire - depassement_mensuel) * (depassement_mensuel > 0)


class af_allocation_forfaitaire(Variable):
    column = FloatCol
    entity = Famille
    label = u"Allocations familiales - forfait"
    definition_period = MONTH

    def formula_2003_07_01(famille, period, legislation):
        af_nbenf = famille('af_nbenf', period)
        af_forfaitaire_nbenf = famille('af_allocation_forfaitaire_nb_enfants', period)
        P = legislation(period).prestations.prestations_familiales.af
        bmaf = P.bmaf
        af_forfait = round(bmaf * P.majoration_enfants.taux_allocation_forfaitaire, 2)
        af_allocation_forfaitaire = ((af_nbenf >= 2) * af_forfaitaire_nbenf) * af_forfait

        af_forfaitaire_taux_modulation = famille('af_allocation_forfaitaire_taux_modulation', period)
        af_forfaitaire_module = af_allocation_forfaitaire * af_forfaitaire_taux_modulation

        return af_forfaitaire_module


class af(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Famille
    label = u"Allocations familiales - total des allocations"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2015_07_01(famille, period, legislation):
        af_base = famille('af_base', period)
        af_majoration = famille('af_majoration', period)
        af_allocation_forfaitaire = famille('af_allocation_forfaitaire', period)
        af_complement_degressif = famille('af_complement_degressif', period)
        af_forfaitaire_complement_degressif = famille('af_allocation_forfaitaire_complement_degressif', period)

        return (
            af_base + af_majoration + af_allocation_forfaitaire + af_complement_degressif +
            af_forfaitaire_complement_degressif
            )

    def formula(famille, period, legislation):
        af_base = famille('af_base', period)
        af_majoration = famille('af_majoration', period)
        af_allocation_forfaitaire = famille('af_allocation_forfaitaire', period)

        return af_base + af_majoration + af_allocation_forfaitaire
