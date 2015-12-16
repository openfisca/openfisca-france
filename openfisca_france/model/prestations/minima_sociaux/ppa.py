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
        ppa_revenu_activite_individus = simulation.compute_add('ppa_revenu_activite_i', period.last_3_months)
        ppa_revenu_activite = self.sum_by_entity(ppa_revenu_activite_individus) / 3

        return period, ppa_revenu_activite

class ppa_revenu_activite_i(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu d'activité pris en compte pour la PPA (Individus) pour un mois"

    def function(self, simulation, period):
        period = period.this_month
        ressources = [
            'salaire_net',
            'revenus_stage_formation_pro',
            'bourse_recherche',
            'indemnites_chomage_partiel',
            'indemnites_journalieres'
            ]

        ppa_revenu_activite_i = sum(simulation.calculate(ressource, period) for ressource in ressources)

        return period, ppa_revenu_activite_i

class ppa_base_ressources(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Bases ressource prise en compte pour la PPA"

    def function(self, simulation, period):
        period = period.this_month
        ppa_revenu_activite = simulation.calculate('ppa_revenu_activite', period)
        return period, ppa_revenu_activite

class ppa_bonification(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Bonification de la PPA pour un individu"

    def function(self, simulation, period):
        period = period.this_month
        P = simulation.legislation_at(period.start)
        smic_horaire = P.cotsoc.gen.smic_h_b
        rsa_base = P.minim.rmi.rmi
        revenu_activite = simulation.calculate('ppa_revenu_activite_i', period)
        seuil_1 = P.minim.ppa.bonification.seuil_1 * smic_horaire
        seuil_2 = P.minim.ppa.bonification.seuil_2 * smic_horaire
        bonification_max = round_(P.minim.ppa.bonification.montant_max * rsa_base)

        bonification = bonification_max * (revenu_activite - seuil_1) / (seuil_2 - seuil_1)
        bonification = max_(bonification, 0)
        bonification = min_(bonification, bonification_max)

        return period, bonification

class ppa(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Prime Pour l'Activité"

    def function(self, simulation, period):
        period = period.this_month
        seuil_non_versement = simulation.legislation_at(period.start).minim.ppa.seuil_non_versement
        pente = simulation.legislation_at(period.start).minim.rmi.pente

        elig = simulation.calculate('ppa_eligibilite', period)

        rsa_socle = simulation.calculate('rsa_socle', period)
        rsa_socle_majore = simulation.calculate('rsa_socle_majore', period)
        montant_forfaitaire_familialise = max_(rsa_socle, rsa_socle_majore)

        ppa_base_ressources = simulation.calculate('ppa_base_ressources', period)
        ppa_revenu_activite = simulation.calculate('ppa_revenu_activite', period)
        rsa_forfait_logement = simulation.calculate('rsa_forfait_logement', period)

        bonification_individus_last_3_months = simulation.compute_add('ppa_bonification', period.last_3_months)
        bonification = self.sum_by_entity(bonification_individus_last_3_months) / 3

        ppa_montant_base = (
            montant_forfaitaire_familialise +
            bonification +
            pente * ppa_revenu_activite - ppa_base_ressources - rsa_forfait_logement
            )
        ppa_deduction = montant_forfaitaire_familialise - ppa_base_ressources - rsa_forfait_logement
        ppa = ppa_montant_base - max_(ppa_deduction,0)

        ppa = ppa * elig * (ppa >= seuil_non_versement)

        return period, ppa
