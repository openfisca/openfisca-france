# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france.model.base import *  # noqa analysis:ignore

from numpy import maximum as max_, round as round_, minimum as min_, logical_not as not_, where, select

class ppa_eligibilite(Variable):
    column = BoolCol
    entity_class = Familles
    label = u"Eligibilité à la PPA pour un mois"

    def function(self, simulation, period, reference_period):
        period = period.this_month
        P = simulation.legislation_at(reference_period.start)
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
        etudiant = simulation.calculate('etudiant', period) # individu
        plancher_ressource = 169 * P.cotsoc.gen.smic_h_b * P.fam.af.seuil_rev_taux
        def condition_ressource(period2):
            revenu_activite = simulation.calculate('ppa_revenu_activite_individu', period2, extra_params = [period])
            return revenu_activite > plancher_ressource
        m_1 = period.offset(-1, 'month')
        m_2 = period.offset(-2, 'month')
        m_3 = period.offset(-3, 'month')
        condition_etudiant_i = condition_ressource(m_1) * condition_ressource(m_2) * condition_ressource(m_3)

        # Au moins une personne de la famille doit être non étudiant ou avoir des ressources > plancher
        condition_famille = self.any_by_roles(not_(etudiant) + condition_etudiant_i, roles = [CHEF, CONJ])
        return period, ppa_majoree_eligibilite + condition_famille

class ppa_montant_forfaitaire_familial_non_majore(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Montant forfaitaire familial (sans majoration)"

    def function(self, simulation, period, reference_period):
        period = period.this_month
        nb_parents = simulation.calculate('nb_parents', period)
        nb_enfants = simulation.calculate('rsa_nb_enfants', period)
        ppa_majoree_eligibilite = simulation.calculate('rsa_majore_eligibilite', period)
        rmi = simulation.legislation_at(reference_period.start).minim.rmi
        nb_personnes = nb_parents + nb_enfants

        taux_non_majore = (
            1 +
            (nb_personnes >= 2) * rmi.txp2 +
            (nb_personnes >= 3) * rmi.txp3 +
            (nb_personnes >= 4) * where(nb_parents == 1, rmi.txps, rmi.txp3) + # Si nb_parents == 1, pas de conjoint, la 4e personne est un enfant, donc le taux est de 40%.
            max_(nb_personnes - 4, 0) * rmi.txps
            )

        return period, rmi.rmi * taux_non_majore

class ppa_montant_forfaitaire_familial_majore(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Montant forfaitaire familial (avec majoration)"

    def function(self, simulation, period, reference_period):
        nb_enfants = simulation.calculate('rsa_nb_enfants', period)
        rmi = simulation.legislation_at(reference_period.start).minim.rmi
        taux_majore = rmi.majo_rsa.pac0 + rmi.majo_rsa.pac_enf_sup * nb_enfants

        return period, rmi.rmi * taux_majore

class ppa_revenu_activite(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Revenu d'activité pris en compte pour la PPA"

    def function(self, simulation, period, reference_period):
        period = period.this_month
        ppa_revenu_activite_individus = simulation.compute('ppa_revenu_activite_individu', period, extra_params = [reference_period])
        ppa_revenu_activite = self.sum_by_entity(ppa_revenu_activite_individus)

        return period, ppa_revenu_activite

class ppa_revenu_activite_individu(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu d'activité pris en compte pour la PPA (Individus) pour un mois"

    def function(self, simulation, period, reference_period):
        period = period.this_month
        P = simulation.legislation_at(reference_period.start)
        smic_horaire = P.cotsoc.gen.smic_h_b

        ressources = [
            'salaire_net',
            'revenus_stage_formation_pro',
            'bourse_recherche',
            'indemnites_chomage_partiel',
            'tns_auto_entrepreneur_benefice',
            'rsa_indemnites_journalieres_activite'
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

        revenus_activites = revenus_mensualises + revenus_annualises

        # L'aah est pris en compte comme revenu d'activité si  revenu d'activité hors aah > 29 * smic horaire brut
        seuil_aah_activite = P.minim.ppa.seuil_aah_activite * smic_horaire
        aah_activite = (revenus_activites >= seuil_aah_activite) * simulation.calculate('aah', period)

        return period, revenus_activites + aah_activite

class ppa_ressources_hors_activite(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Revenu hors activité pris en compte pour la PPA"

    def function(self, simulation, period, reference_period):
        pf = simulation.calculate('ppa_base_ressources_prestations_familiales', period, extra_params = [reference_period])
        ressources_hors_activite_individus = simulation.compute('ppa_ressources_hors_activite_individu', period, extra_params = [reference_period])
        ressources = [
        'ass',
        'asi',
        'aspa'
        ]

        ressources_hors_activite = self.sum_by_entity(ressources_hors_activite_individus) + pf + sum(
            simulation.calculate(ressource, reference_period) for ressource in ressources)

        return period, ressources_hors_activite

class ppa_ressources_hors_activite_individu(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Revenu hors activité pris en compte pour la PPA (Individus) pour un mois"

    def function(self, simulation, period, reference_period):
        period = period.this_month
        P = simulation.legislation_at(reference_period.start)
        smic_horaire = P.cotsoc.gen.smic_h_b

        ressources = [
            'chomage_net',
            'retraite_nette',
            'retraite_combattant',
            'pensions_invalidite',
            'pensions_alimentaires_percues',
            'prestation_compensatoire',
            'revenus_locatifs',
            'prime_forfaitaire_mensuelle_reprise_activite',
            'rsa_indemnites_journalieres_hors_activite',
            ]

        ressources_hors_activite_i = sum(
            simulation.calculate(ressource, period) for ressource in ressources)
        revenus_activites = simulation.calculate('ppa_revenu_activite_individu', period, extra_params = [reference_period])

        # L'aah est pris en compte comme revenu d'activité si  revenu d'activité hors aah > 29 * smic horaire brut
        seuil_aah_activite = P.minim.ppa.seuil_aah_activite * smic_horaire
        aah_hors_activite = (revenus_activites < seuil_aah_activite) * simulation.calculate('aah', period)

        return period, ressources_hors_activite_i + aah_hors_activite

class ppa_base_ressources_prestations_familiales(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Prestations familiales prises en compte dans le calcul de la PPA"

    def function(self, simulation, period, reference_period):
        period = period.this_month

        prestations_calculees = [
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

        af_base = simulation.calculate('af_base', reference_period)
        af = simulation.calculate('af', reference_period)

        result = result + cf_non_majore + min_(af_base, af)

        return period, result

class ppa_base_ressources(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Bases ressource prise en compte pour la PPA"

    def function(self, simulation, period, reference_period):
        period = period.this_month
        ppa_revenu_activite = simulation.calculate('ppa_revenu_activite', period, extra_params = [reference_period])
        ppa_ressources_hors_activite = simulation.calculate('ppa_ressources_hors_activite', period, extra_params = [reference_period])
        return period, ppa_revenu_activite + ppa_ressources_hors_activite

class ppa_bonification(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Bonification de la PPA pour un individu"

    def function(self, simulation, period, reference_period):
        period = period.this_month
        P = simulation.legislation_at(reference_period.start)
        smic_horaire = P.cotsoc.gen.smic_h_b
        rsa_base = P.minim.rmi.rmi
        revenu_activite = simulation.calculate('ppa_revenu_activite_individu', period, extra_params = [reference_period])
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

    def function(self, simulation, period, reference_period):
        period = period.this_month
        forfait_logement = simulation.calculate('rsa_forfait_logement', reference_period)
        ppa_majoree_eligibilite = simulation.calculate('rsa_majore_eligibilite', reference_period)

        elig = simulation.calculate('ppa_eligibilite', period, extra_params = [reference_period])
        pente = simulation.legislation_at(reference_period.start).minim.ppa.pente
        mff_non_majore = simulation.calculate('ppa_montant_forfaitaire_familial_non_majore', period, extra_params = [reference_period])
        mff_majore = simulation.calculate('ppa_montant_forfaitaire_familial_majore', period, extra_params = [reference_period])
        montant_forfaitaire_familialise = where(ppa_majoree_eligibilite, mff_majore, mff_non_majore)
        ppa_base_ressources = simulation.calculate('ppa_base_ressources', period, extra_params = [reference_period])
        ppa_revenu_activite = simulation.calculate('ppa_revenu_activite', period, extra_params = [reference_period])
        bonification_individus = simulation.compute('ppa_bonification', period, extra_params = [reference_period])
        bonification = self.sum_by_entity(bonification_individus)

        ppa_montant_base = (
            montant_forfaitaire_familialise +
            bonification +
            pente * ppa_revenu_activite - ppa_base_ressources
            - forfait_logement
            )

        ppa_deduction = (
            montant_forfaitaire_familialise
            - ppa_base_ressources
            - forfait_logement
            )

        ppa_fictive = ppa_montant_base - max_(ppa_deduction,0)
        ppa_fictive = max_(ppa_fictive, 0)
        return period, elig * ppa_fictive

class ppa(DatedVariable):
    column = FloatCol
    entity_class = Familles
    label = u"Prime Pour l'Activité"

    @dated_function(start = date(2016, 1, 1))
    def function(self, simulation, period):
        period = period.this_month
        seuil_non_versement = simulation.legislation_at(period.start).minim.ppa.seuil_non_versement
        # éligibilité étudiants

        ppa_eligibilite_etudiants = simulation.calculate('ppa_eligibilite_etudiants', period)
        m_1 = period.last_month
        m_2 = m_1.last_month
        m_3 = m_2.last_month
        ppa = sum(simulation.calculate('ppa_fictive', period2, extra_params = [period])
            for period2 in [m_1, m_2, m_3]) / 3
        ppa = ppa * ppa_eligibilite_etudiants * (ppa >= seuil_non_versement)

        return period, ppa
