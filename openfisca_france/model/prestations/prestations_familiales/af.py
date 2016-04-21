# -*- coding: utf-8 -*-

from __future__ import division

from numpy import round, maximum as max_, logical_not as not_, logical_or as or_, vectorize, where


from ...base import *  # noqa analysis:ignore
from .base_ressource import nb_enf


class af_nbenf(Variable):
    column = IntCol
    entity_class = Familles
    label = u"Nombre d'enfants dans la famille au sens des allocations familiales"

    def function(self, simulation, period):
        period_mois = period.this_month

        pfam_enfant_a_charge_holder = simulation.compute('prestations_familiales_enfant_a_charge', period_mois)
        af_nbenf = self.sum_by_entity(pfam_enfant_a_charge_holder)

        return period, af_nbenf

class af_coeff_garde_alternee(DatedVariable):
    column = FloatCol(default = 1)
    entity_class = Familles
    label = u"Coefficient à appliquer aux af pour tenir compte de la garde alternée"

    @dated_function(start = date(2007, 5, 1))
    def function_2007(self, simulation, period):
        period = period.this_month
        nb_enf = simulation.calculate('af_nbenf', period)
        garde_alternee = simulation.compute('garde_alternee', period)
        pfam_enfant_a_charge = simulation.compute('prestations_familiales_enfant_a_charge', period)

        # Le nombre d'enfants à charge en garde alternée, qui vérifient donc pfam_enfant_a_charge = true et garde_alternee = true
        nb_enf_garde_alternee = self.sum_by_entity(garde_alternee.array * pfam_enfant_a_charge.array)

        # Avoid division by zero. If nb_enf == 0, necessarily nb_enf_garde_alternee = 0 so coeff = 1
        coeff = 1 - (nb_enf_garde_alternee / (nb_enf + (nb_enf == 0))) * 0.5

        return period, coeff

class af_allocation_forfaitaire_nb_enfants(Variable):
    column = IntCol
    entity_class = Familles
    label = u"Nombre d'enfants ouvrant droit à l'allocation forfaitaire des AF"

    def function(self, simulation, period):
        period = period.this_month
        age_holder = simulation.compute('age', period)
        age = self.split_by_roles(age_holder, roles = ENFS)
        autonomie_financiere_holder = simulation.compute('autonomie_financiere', period)
        autonomie_financiere = self.split_by_roles(autonomie_financiere_holder, roles = ENFS)
        pfam = simulation.legislation_at(period.start).fam.af
        af_forfaitaire_nbenf = nb_enf(age, autonomie_financiere, pfam.age3, pfam.age3)

        return period, af_forfaitaire_nbenf


class af_eligibilite_base(Variable):
    column = BoolCol
    entity_class = Familles
    label = u"Allocations familiales - Éligibilité pour la France métropolitaine sous condition de ressources"

    def function(self, simulation, period):
        period = period.this_month

        residence_dom = simulation.calculate('residence_dom', period)
        af_nbenf = simulation.calculate('af_nbenf', period)

        return period, not_(residence_dom) * (af_nbenf >= 2)


class af_eligibilite_dom(Variable):
    column = BoolCol
    entity_class = Familles
    label = u"Allocations familiales - Éligibilité pour les DOM (hors Mayotte) sous condition de ressources"

    def function(self, simulation, period):
        period = period.this_month

        residence_dom = simulation.calculate('residence_dom', period)
        residence_mayotte = simulation.calculate('residence_mayotte', period)
        af_nbenf = simulation.calculate('af_nbenf', period)

        return period, residence_dom * not_(residence_mayotte) * (af_nbenf >= 1)


class af_base(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Allocations familiales - allocation de base"
    # prestations familiales (brutes de crds)

    def function(self, simulation, period):
        period = period.this_month

        eligibilite_base = simulation.calculate('af_eligibilite_base', period)
        eligibilite_dom = simulation.calculate('af_eligibilite_dom', period)
        af_nbenf = simulation.calculate('af_nbenf', period)

        pfam = simulation.legislation_at(period.start).fam.af

        eligibilite = or_(eligibilite_base, eligibilite_dom)

        un_seul_enfant = eligibilite_dom * (af_nbenf == 1) * pfam.taux.enf_seul
        plus_de_deux_enfants = (af_nbenf >= 2) * pfam.taux.enf2
        plus_de_trois_enfants = max_(af_nbenf - 2, 0) * pfam.taux.enf3
        taux_total = un_seul_enfant + plus_de_deux_enfants + plus_de_trois_enfants
        montant_base = eligibilite * round(pfam.bmaf * taux_total, 2)
        coeff_garde_alternee = simulation.calculate('af_coeff_garde_alternee', period)
        montant_base = montant_base * coeff_garde_alternee

        af_taux_modulation = simulation.calculate('af_taux_modulation', period)
        montant_base_module = montant_base * af_taux_modulation

        return period, montant_base_module


class af_taux_modulation(DatedVariable):
    column = FloatCol(default = 1)
    entity_class = Familles
    label = u"Taux de modulation à appliquer au montant des AF depuis 2015"

    @dated_function(start = date(2015, 7, 1))
    def function_2015(self, simulation, period):
        period = period.this_month
        af_nbenf = simulation.calculate('af_nbenf', period)
        pfam = simulation.legislation_at(period.start).fam.af
        base_ressources = simulation.calculate('prestations_familiales_base_ressources', period)
        modulation = pfam.modulation
        plafond1 = modulation.plafond1 + af_nbenf * modulation.enfant_supp
        plafond2 = modulation.plafond2 + af_nbenf * modulation.enfant_supp

        taux = (
            (base_ressources <= plafond1) * 1 +
            (base_ressources > plafond1) * (base_ressources <= plafond2) * modulation.taux1 +
            (base_ressources > plafond2) * modulation.taux2
        )

        return period, taux


class af_allocation_forfaitaire_taux_modulation(DatedVariable):
    column = FloatCol(default = 1)
    entity_class = Familles
    label = u"Taux de modulation à appliquer à l'allocation forfaitaire des AF depuis 2015"

    @dated_function(start = date(2015, 7, 1))
    def function_2015(self, simulation, period):
        period = period.this_month
        pfam = simulation.legislation_at(period.start).fam.af
        af_nbenf = simulation.calculate('af_nbenf', period)
        af_forfaitaire_nbenf = simulation.calculate('af_allocation_forfaitaire_nb_enfants', period)
        nb_enf_tot = af_nbenf + af_forfaitaire_nbenf
        base_ressources = simulation.calculate('prestations_familiales_base_ressources', period)
        modulation = pfam.modulation
        plafond1 = modulation.plafond1 + nb_enf_tot * modulation.enfant_supp
        plafond2 = modulation.plafond2 + nb_enf_tot * modulation.enfant_supp

        taux = (
            (base_ressources <= plafond1) * 1 +
            (base_ressources > plafond1) * (base_ressources <= plafond2) * modulation.taux1 +
            (base_ressources > plafond2) * modulation.taux2
        )

        return period, taux


class af_age_aine(Variable):
    column = IntCol
    entity_class = Familles
    label = u"Allocations familiales - Âge de l'aîné des enfants éligibles"

    def function(self, simulation, period):
        period = period.this_month

        age_holder = simulation.compute('age', period)
        age_enfants = self.split_by_roles(age_holder, roles = ENFS)

        pfam_enfant_a_charge_holder = simulation.compute('prestations_familiales_enfant_a_charge', period)
        af_enfants_a_charge = self.split_by_roles(pfam_enfant_a_charge_holder, roles = ENFS)

        pfam = simulation.legislation_at(period.start).fam

        # Calcul de l'âge de l'aîné
        age_aine = -9999
        for key, age in age_enfants.iteritems():
            a_charge = af_enfants_a_charge[key] * (age <= pfam.af.age2)
            aine_potentiel = a_charge * (age > age_aine)
            age_aine = aine_potentiel * age + not_(aine_potentiel) * age_aine

        return period, age_aine


class af_majoration_enfant(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Allocations familiales - Majoration pour âge applicable à l'enfant"

    def function(self, simulation, period):
        period = period.this_month

        pfam_enfant_a_charge = simulation.calculate('prestations_familiales_enfant_a_charge', period)
        age = simulation.calculate('age', period)
        garde_alternee = simulation.calculate('garde_alternee', period)
        age_aine_holder = simulation.compute('af_age_aine', period)
        age_aine = self.cast_from_entity_to_roles(age_aine_holder, roles = ENFS)
        af_nbenf_holder = simulation.compute('af_nbenf', period)
        af_nbenf = self.cast_from_entity_to_roles(af_nbenf_holder, roles = ENFS)
        af_base_holder = simulation.compute('af_base', period)
        af_base = self.cast_from_entity_to_roles(af_base_holder, roles = ENFS)

        pfam = simulation.legislation_at(period.start).fam

        montant_enfant_seul = pfam.af.bmaf * (
            (pfam.af.maj_age_un_enfant.age1 <= age) * (age < pfam.af.maj_age_un_enfant.age2) * pfam.af.maj_age_un_enfant.taux1 +
            (pfam.af.maj_age_un_enfant.age2 <= age) * pfam.af.maj_age_un_enfant.taux2
            )

        montant_plusieurs_enfants = pfam.af.bmaf * (
            (pfam.af.maj_age_deux_enfants.age1 <= age) * (age < pfam.af.maj_age_deux_enfants.age2) * pfam.af.maj_age_deux_enfants.taux1 +
            (pfam.af.maj_age_deux_enfants.age2 <= age) * pfam.af.maj_age_deux_enfants.taux2
            )

        montant = (af_nbenf == 1) * montant_enfant_seul + (af_nbenf > 1) * montant_plusieurs_enfants

        # Attention ! Ne fonctionne pas pour les enfants du même âge (typiquement les jumeaux...)
        pas_aine = or_(af_nbenf != 2, (af_nbenf == 2) * not_(age == age_aine))

        coeff_garde_alternee = where(garde_alternee, pfam.af.facteur_garde_alternee, 1)

        return period, pfam_enfant_a_charge * (af_base > 0) * pas_aine * montant * coeff_garde_alternee


class af_majoration(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Allocations familiales - majoration pour âge"

    def function(self, simulation, period):
        period = period.this_month
        af_majoration_enfant_holder = simulation.compute('af_majoration_enfant', period)
        af_majoration_enfants = self.sum_by_entity(af_majoration_enfant_holder, roles = ENFS)

        af_taux_modulation = simulation.calculate('af_taux_modulation', period)
        af_majoration_enfants_module = af_majoration_enfants * af_taux_modulation

        return period, af_majoration_enfants_module


class af_complement_degressif(DatedVariable):
    column = FloatCol
    entity_class = Familles
    label = u"AF - Complément dégressif en cas de dépassement du plafond"

    @dated_function(start = date(2015, 7, 1))
    def function_2015(self, simulation, period):
        period = period.this_month
        af_nbenf = simulation.calculate('af_nbenf', period)
        base_ressources = simulation.calculate('prestations_familiales_base_ressources', period)
        af_base = simulation.calculate('af_base', period)
        af_majoration = simulation.calculate('af_majoration', period)
        pfam = simulation.legislation_at(period.start).fam.af
        modulation = pfam.modulation
        plafond1 = modulation.plafond1 + af_nbenf * modulation.enfant_supp
        plafond2 = modulation.plafond2 + af_nbenf * modulation.enfant_supp

        depassement_plafond1 = max_(0, base_ressources - plafond1)
        depassement_plafond2 = max_(0, base_ressources - plafond2)

        depassement_mensuel = (
            (depassement_plafond2 == 0) * depassement_plafond1 +
            (depassement_plafond2 > 0) * depassement_plafond2
        ) / 12

        af = af_base + af_majoration
        return period, max_(0, af - depassement_mensuel) * (depassement_mensuel > 0)


class af_allocation_forfaitaire_complement_degressif(DatedVariable):
    column = FloatCol
    entity_class = Familles
    label = u"AF - Complément dégressif pour l'allocation forfaitaire en cas de dépassement du plafond"

    @dated_function(start = date(2015, 7, 1))
    def function_2015(self, simulation, period):
        period = period.this_month
        af_nbenf = simulation.calculate('af_nbenf', period)
        af_forfaitaire_nbenf = simulation.calculate('af_allocation_forfaitaire_nb_enfants', period)
        pfam = simulation.legislation_at(period.start).fam.af
        nb_enf_tot = af_nbenf + af_forfaitaire_nbenf
        base_ressources = simulation.calculate('prestations_familiales_base_ressources', period)
        af_allocation_forfaitaire = simulation.calculate('af_allocation_forfaitaire', period)
        modulation = pfam.modulation
        plafond1 = modulation.plafond1 + nb_enf_tot * modulation.enfant_supp
        plafond2 = modulation.plafond2 + nb_enf_tot * modulation.enfant_supp

        depassement_plafond1 = max_(0, base_ressources - plafond1)
        depassement_plafond2 = max_(0, base_ressources - plafond2)

        depassement_mensuel = (
            (depassement_plafond2 == 0) * depassement_plafond1 +
            (depassement_plafond2 > 0) * depassement_plafond2
        ) / 12

        return period, max_(0, af_allocation_forfaitaire - depassement_mensuel) * (depassement_mensuel > 0)


class af_allocation_forfaitaire(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Allocations familiales - forfait"

    def function(self, simulation, period):
        period = period.this_month
        af_nbenf = simulation.calculate('af_nbenf', period)
        af_forfaitaire_nbenf = simulation.calculate('af_allocation_forfaitaire_nb_enfants', period)
        P = simulation.legislation_at(period.start).fam.af

        bmaf = P.bmaf
        af_forfait = round(bmaf * P.taux.forfait, 2)
        af_allocation_forfaitaire = ((af_nbenf >= 2) * af_forfaitaire_nbenf) * af_forfait

        af_forfaitaire_taux_modulation = simulation.calculate('af_allocation_forfaitaire_taux_modulation', period)
        af_forfaitaire_module = af_allocation_forfaitaire * af_forfaitaire_taux_modulation

        return period, af_forfaitaire_module


class af(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Familles
    label = u"Allocations familiales - total des allocations"

    def function(self, simulation, period):
        period = period.this_month
        af_base = simulation.calculate('af_base', period)
        af_majoration = simulation.calculate('af_majoration', period)
        af_allocation_forfaitaire = simulation.calculate('af_allocation_forfaitaire', period)
        af_complement_degressif = simulation.calculate('af_complement_degressif', period)
        af_forfaitaire_complement_degressif = simulation.calculate('af_allocation_forfaitaire_complement_degressif', period)

        return period, af_base + af_majoration + af_allocation_forfaitaire + af_complement_degressif + af_forfaitaire_complement_degressif
