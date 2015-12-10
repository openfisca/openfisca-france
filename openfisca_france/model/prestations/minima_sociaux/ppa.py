# -*- coding: utf-8 -*-

from __future__ import division

from ...base import *  # noqa analysis:ignore

from numpy import maximum as max_, round as round_, minimum as min_

class ppa_eligibilite(Variable):
    column = BoolCol
    entity_class = Familles
    label = u"Eligibilité à la PPA"

    def function(self, simulation, period):
        period = period.this_month
        age_min = simulation.legislation_at(period.start).minim.ppa.age_min
        ppa_revenu_activite = simulation.calculate('ppa_revenu_activite', period.last_month)
        condition_age_individus = simulation.calculate('age', period) >= age_min
        condition_age = self.any_by_roles(condition_age_individus)
        elig = condition_age * ppa_revenu_activite
        return period, elig

class ppa_revenu_activite(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Revenu d'activité pris en compte pour la PPA"

    def function(self, simulation, period):
        period = period.this_month
        salaire_individus_3_months = simulation.compute_add('salaire_net', period.last_3_months)
        salaire = self.sum_by_entity(salaire_individus_3_months) / 3
        return period, salaire

class ppa_base_ressources(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Bases ressource prise en compte pour la PPA"

    def function(self, simulation, period):
        period = period.this_month
        pente = simulation.legislation_at(period.start).minim.rmi.pente
        ppa_revenu_activite = simulation.calculate('ppa_revenu_activite', period)
        return period, ppa_revenu_activite * (1 - pente)

class ppa_bonification(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Bonification de la PPA pour un individu"

    def function(self, simulation, period):
        period = period.this_month
        P = simulation.legislation_at(period.start)
        smic_horaire = P.cotsoc.gen.smic_h_b
        rsa_base = P.minim.rmi.rmi
        salaire = simulation.calculate('salaire_net', period)
        seuil_1 = P.minim.ppa.bonification.seuil_1 * smic_horaire
        seuil_2 = P.minim.ppa.bonification.seuil_2 * smic_horaire
        bonification_max = round_(P.minim.ppa.bonification.montant_max * rsa_base)

        bonification = bonification_max * (salaire - seuil_1) / (seuil_2 - seuil_1)
        bonification = max_(bonification, 0)
        bonification = min_(bonification, bonification_max)

        return period, bonification

class ppa(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Prime Pour l'Activité"

    def function(self, simulation, period):
        period = period.this_month
        elig = simulation.calculate('ppa_eligibilite', period)
        rsa_socle = simulation.calculate('rsa_socle', period)
        rsa_socle_majore = simulation.calculate('rsa_socle_majore', period)
        ppa_base_ressources = simulation.calculate('ppa_base_ressources', period)
        bonification_individus_last_3_months = simulation.compute_add('ppa_bonification', period.last_3_months)
        bonification = self.sum_by_entity(bonification_individus_last_3_months) / 3
        ppa = elig * (
            max_(rsa_socle, rsa_socle_majore) - ppa_base_ressources + bonification
            )

        return period, ppa
