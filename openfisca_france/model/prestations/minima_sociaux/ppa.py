# -*- coding: utf-8 -*-

from __future__ import division

from ...base import *  # noqa analysis:ignore

from numpy import maximum as max_

class ppa_eligibilite(Variable):
    column = BoolCol
    entity_class = Familles
    label = u"Eligibilité à la PPA"

    def function(self, simulation, period):
        ppa_revenu_activite = simulation.calculate('ppa_revenu_activite', period.last_month)
        condition_age_individus = simulation.calculate('age', period) >= 18
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
        ppa_revenu_activite = simulation.calculate('ppa_revenu_activite', period)
        pente = 0.38       
        return period, ppa_revenu_activite * pente

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
        return period, elig * max_(rsa_socle, rsa_socle_majore) - ppa_base_ressources
