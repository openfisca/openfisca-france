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

class ppa_montant_forfaitaire_familial_non_majore(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Montant forfaitaire familial (sans majoration)"

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

        return period, rmi.rmi * taux_non_majore

class ppa_montant_forfaitaire_familial_majore(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Montant forfaitaire familial (avec majoration)"

    def function(self, simulation, period):
        nb_enfants = simulation.calculate('nb_enfant_rsa', period)
        rmi = simulation.legislation_at(period.start).minim.rmi
        taux_majore = rmi.majo_rsa.pac0 + rmi.majo_rsa.pac_enf_sup * nb_enfants

        return period, rmi.rmi * taux_majore

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
            'indemnites_journalieres',
            'tns_auto_entrepreneur_benefice',
            ]

        revenus_mensualises = sum(
            simulation.calculate(ressource, period) for ressource in ressources)

        def get_last_known(variable_name):
            valeur_n = simulation.calculate(variable_name, period.this_year)
            valeur_n_1 = simulation.calculate(variable_name, period.last_year)
            valeur_n_2 = simulation.calculate(variable_name, period.n_2)
            return select(
                [valeur_n > 0, valeur_n_1 > 0, valeur_n_2 > 0],
                [valeur_n, valeur_n_1, valeur_n_2]
                ) / 12
        revenus_annualises = get_last_known('tns_benefice_exploitant_agricole') + get_last_known('tns_autres_revenus') + get_last_known('tns_micro_entreprise_benefice')

        return period, revenus_mensualises + revenus_annualises

class ppa_ressources_hors_activite(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Revenu hors activité pris en compte pour la PPA"

    def function(self, simulation, period, reference_period):
        pf = simulation.calculate('ppa_base_ressources_prestations_familiales', period, extra_params = [reference_period])
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
            'aah',
            'chomage_net',
            'retraite_nette',
            'retraite_combattant',
            'pensions_alimentaires_percues',
            'prestation_compensatoire',
            'revenus_locatifs',
            ]

        ressources_hors_activite_i = sum(
            simulation.calculate(ressource, period) for ressource in ressources)

        return period, ressources_hors_activite_i

class ppa_base_ressources_prestations_familiales(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Prestations familiales prises en compte dans le calcul de la PPA"

    def function(self, simulation, period, reference_period):
        period = period.this_month

        prestations_calculees = [
            'af_base',
            'rsa_forfait_asf',
            'paje_base',
           ]
        prestations_autres = [
            'paje_clca',
            'paje_prepare',
            'paje_colca',
            ]

        result = sum(simulation.calculate(prestation, reference_period) for prestation in prestations_calculees)
        result += sum(simulation.calculate(prestation, period) for prestation in prestations_autres)
        cf_non_majore_avant_cumul = simulation.calculate('cf_non_majore_avant_cumul', reference_period)
        cf = simulation.calculate('cf', reference_period)
        # Seul le montant non majoré est pris en compte dans la base de ressources du RSA
        cf_non_majore = (cf > 0) * cf_non_majore_avant_cumul
        result = result + cf_non_majore

        return period, result

class ppa_base_ressources(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Bases ressource prise en compte pour la PPA"

    def function(self, simulation, period, reference_period):
        period = period.this_month
        ppa_revenu_activite = simulation.calculate('ppa_revenu_activite', period)
        ppa_ressources_hors_activite = simulation.calculate('ppa_ressources_hors_activite', period, extra_params = [reference_period])
        return period, ppa_revenu_activite + ppa_ressources_hors_activite
