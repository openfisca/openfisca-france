# -*- coding: utf-8 -*-

from __future__ import division

from ...base import *  # noqa analysis:ignore

from numpy import maximum as max_, round as round_, minimum as min_, logical_not as not_, where, select

class ppa_eligibilite(Variable):
    column = BoolCol
    entity_class = Familles
    label = u"Eligibilité à la PPA pour un mois"

    def function(self, simulation, period):
        period = period.this_month
        P = simulation.legislation_at(period.start)
        age_min = P.minim.ppa.age_min
        condition_age_individus = simulation.calculate('age', period) >= age_min
        condition_age = self.any_by_roles(condition_age_individus)
        elig = condition_age

        return period, elig

class ppa_eligibilite_etudiants(Variable):
    column = BoolCol
    entity_class = Familles
    label = u"Eligibilité à la PPA (condition sur tout le trimestre)"

    def function(self, simulation, period):
        P = simulation.legislation_at(period.start)
        period = period.this_month
        ppa_majoree_eligibilite = simulation.calculate('rsa_majore_eligibilite', period)

        # Pour un individu
        etudiant = simulation.calculate('etu', period) # individu
        plancher_ressource = 169 * P.cotsoc.gen.smic_h_b * P.fam.af.seuil_rev_taux
        def condition_ressource(period):
            revenu_activite = simulation.calculate('ppa_revenu_activite_i', period)
            return revenu_activite > plancher_ressource
        m_1 = period.offset(-1, 'month')
        m_2 = period.offset(-2, 'month')
        m_3 = period.offset(-3, 'month')
        condition_etudiant_i = condition_ressource(m_1) * condition_ressource(m_2) * condition_ressource(m_3)
        condition_non_etudiant_i = simulation.calculate_add('ppa_revenu_activite_i', period.last_3_months) > 0
        condition_i = where(etudiant, condition_etudiant_i, condition_non_etudiant_i)

        # Au moins une personne de la famille doit être non étudiant ou avoir des ressources > plancher
        condition_famille = self.any_by_roles(condition_i)
        return period, ppa_majoree_eligibilite + condition_famille

class ppa_montant_forfaitaire_familial(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Montant forfaitaire familial"

    def function(self, simulation, period):
        period = period.this_month
        nb_parents = simulation.calculate('nb_par', period)
        nb_enfants = simulation.calculate('nb_enfant_rsa', period)
        ppa_majoree_eligibilite = simulation.calculate('rsa_majore_eligibilite', period)
        rmi = simulation.legislation_at(period.start).minim.rmi
        nb_personnes = nb_parents + nb_enfants

        taux_non_majore = (
            1 +
            (nb_personnes >= 2) * rmi.txp2 +
            (nb_personnes >= 3) * rmi.txp3 +
            (nb_personnes >= 4) * where(nb_parents == 1, rmi.txps, rmi.txp3) + # Si nb_par == 1, pas de conjoint, la 4e personne est un enfant, donc le taux est de 40%.
            max_(nb_personnes - 4, 0) * rmi.txps
        )

        taux_majore = rmi.majo_rsa.pac0 + rmi.majo_rsa.pac_enf_sup * nb_enfants

        mff = rmi.rmi * where(ppa_majoree_eligibilite, taux_majore, taux_non_majore)

        return period, mff

class ppa_revenu_activite(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Revenu d'activité pris en compte pour la PPA"

    def function(self, simulation, period):
        period = period.this_month
        ppa_revenu_activite_individus = simulation.compute('ppa_revenu_activite_i', period)
        ppa_revenu_activite = self.sum_by_entity(ppa_revenu_activite_individus)

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

        ppa_revenu_activite_i = sum(
            simulation.calculate(ressource, period) for ressource in ressources)

        return period, ppa_revenu_activite_i

class ppa_ressources_hors_activite(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Revenu hors activité pris en compte pour la PPA"

    def function(self, simulation, period):
        pf = simulation.calculate('rsa_base_ressources_prestations_familiales', period)
        ressources_hors_activite_individus = simulation.compute('ppa_ressources_hors_activite_i', period)
        ressources_hors_activite = self.sum_by_entity(ressources_hors_activite_individus) + pf

        return period, ressources_hors_activite

class ppa_ressources_hors_activite_i(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu hors activité pris en compte pour la PPA (Individus) pour un mois"

    def function(self, simulation, period):
        period = period.this_month

        ressources = [
            'chonet',
            'rstnet',
            'retraite_combattant',
            'dedommagement_victime_amiante',
            'pensions_alimentaires_percues',
            'prestation_compensatoire',
            ]

        ressources_hors_activite_i = sum(
            simulation.calculate(ressource, period) for ressource in ressources)

        return period, ressources_hors_activite_i

class ppa_base_ressources(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Bases ressource prise en compte pour la PPA"

    def function(self, simulation, period):
        period = period.this_month
        ppa_revenu_activite = simulation.calculate('ppa_revenu_activite', period)
        ppa_ressources_hors_activite = simulation.calculate('ppa_ressources_hors_activite', period)
        return period, ppa_revenu_activite + ppa_ressources_hors_activite

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

class ppa_fictive(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Prime pour l'activité fictive pour un mois"

    def function(self, simulation, period):
        period = period.this_month

        elig = simulation.calculate('ppa_eligibilite', period)
        pente = simulation.legislation_at(period.start).minim.rmi.pente
        montant_forfaitaire_familialise = simulation.calculate('ppa_montant_forfaitaire_familial', period)
        ppa_base_ressources = simulation.calculate('ppa_base_ressources', period)
        ppa_revenu_activite = simulation.calculate('ppa_revenu_activite', period)
        bonification_individus = simulation.compute('ppa_bonification', period)
        bonification = self.sum_by_entity(bonification_individus)

        ppa_montant_base = (
            montant_forfaitaire_familialise +
            bonification +
            pente * ppa_revenu_activite - ppa_base_ressources
            )

        ppa_deduction = montant_forfaitaire_familialise - ppa_base_ressources
        ppa_fictive = ppa_montant_base - max_(ppa_deduction,0)
        ppa_fictive = max_(ppa_fictive, 0)
        return period, elig * ppa_fictive

class ppa(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Prime Pour l'Activité"

    def function(self, simulation, period):
        period = period.this_month
        seuil_non_versement = simulation.legislation_at(period.start).minim.ppa.seuil_non_versement
        # éligibilité étudiants

        rsa_forfait_logement = simulation.calculate('rsa_forfait_logement', period)
        ppa_eligibilite_etudiants = simulation.calculate('ppa_eligibilite_etudiants', period)
        ppa = simulation.calculate_add('ppa_fictive', period.last_3_months) / 3
        ppa = ppa - rsa_forfait_logement
        ppa = ppa * ppa_eligibilite_etudiants * (ppa >= seuil_non_versement)

        return period, ppa
