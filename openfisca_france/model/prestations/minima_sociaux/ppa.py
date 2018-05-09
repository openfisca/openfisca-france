# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france.model.base import *  # noqa analysis:ignore

from numpy import round as round_, logical_or as or_


class ppa_eligibilite(Variable):
    value_type = bool
    entity = Famille
    label = u"Eligibilité à la PPA pour un mois"
    definition_period = MONTH

    def formula(famille, period, parameters, mois_demande):
        P = parameters(mois_demande).prestations
        age_min = P.minima_sociaux.ppa.age_min
        condition_age_i = famille.members('age', period) >= age_min
        condition_age = famille.any(condition_age_i)

        return condition_age


class ppa_eligibilite_etudiants(Variable):
    value_type = bool
    entity = Famille
    label = u"Eligibilité à la PPA (condition sur tout le trimestre)"
    definition_period = MONTH

    def formula(famille, period, parameters):
        P = parameters(period)
        ppa_majoree_eligibilite = famille('rsa_majore_eligibilite', period)

        # Pour un individu
        etudiant_i = famille.members('etudiant', period)  # individu
        plancher_ressource = 169 * P.cotsoc.gen.smic_h_b * P.prestations.prestations_familiales.af.seuil_rev_taux

        def condition_ressource(period2):
            revenu_activite = famille.members('ppa_revenu_activite_individu', period2, extra_params = [period])
            return revenu_activite > plancher_ressource

        m_1 = period.offset(-1, 'month')
        m_2 = period.offset(-2, 'month')
        m_3 = period.offset(-3, 'month')
        condition_etudiant_i = condition_ressource(m_1) * condition_ressource(m_2) * condition_ressource(m_3)

        # Au moins une personne de la famille doit être non étudiant ou avoir des ressources > plancher
        condition_famille = famille.any(
            not_(etudiant_i) + condition_etudiant_i,
            role = Famille.PARENT)

        return ppa_majoree_eligibilite + condition_famille


class ppa_montant_forfaitaire_familial_non_majore(Variable):
    value_type = float
    entity = Famille
    label = u"Montant forfaitaire familial (sans majoration)"
    definition_period = MONTH

    def formula(famille, period, parameters, mois_demande):
        nb_parents = famille('nb_parents', period)
        nb_enfants = famille('rsa_nb_enfants', period)
        ppa_majoree_eligibilite = famille('rsa_majore_eligibilite', period)
        ppa = parameters(mois_demande).prestations.minima_sociaux.ppa

        nb_personnes = nb_parents + nb_enfants

        taux_non_majore = (
            1 +
            (nb_personnes >= 2) * ppa.taux_deuxieme_personne +
            (nb_personnes >= 3) * ppa.taux_troisieme_personne +
            (nb_personnes >= 4) * where(nb_parents == 1, ppa.taux_personne_supp, ppa.taux_troisieme_personne) +
            # Si nb_parents == 1, pas de conjoint, la 4e personne est un enfant, donc le taux est de 40%.
            max_(nb_personnes - 4, 0) * ppa.taux_personne_supp
            )

        return ppa.montant_de_base * taux_non_majore


class ppa_montant_forfaitaire_familial_majore(Variable):
    value_type = float
    entity = Famille
    label = u"Montant forfaitaire familial (avec majoration)"
    definition_period = MONTH

    def formula(famille, period, parameters, mois_demande):
        nb_enfants = famille('rsa_nb_enfants', period)
        ppa = parameters(mois_demande).prestations.minima_sociaux.ppa

        taux_majore = ppa.majoration_isolement_femme_enceinte + ppa.majoration_isolement_enf_charge * nb_enfants

        return ppa.montant_de_base * taux_majore


class ppa_revenu_activite(Variable):
    value_type = float
    entity = Famille
    label = u"Revenu d'activité pris en compte pour la PPA"
    definition_period = MONTH

    def formula(famille, period, parameters, mois_demande):
        ppa_revenu_activite_i = famille.members(
            'ppa_revenu_activite_individu', period, extra_params = [mois_demande])
        ppa_revenu_activite = famille.sum(ppa_revenu_activite_i)

        return ppa_revenu_activite


class ppa_revenu_activite_individu(Variable):
    value_type = float
    entity = Individu
    label = u"Revenu d'activité pris en compte pour la PPA (Individu) pour un mois"
    definition_period = MONTH

    def formula(individu, period, parameters, mois_demande):
        P = parameters(mois_demande)
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
            individu(ressource, period) for ressource in ressources)

        revenus_tns_annualises = individu('ppa_rsa_derniers_revenus_tns_annuels_connus', mois_demande.this_year)

        revenus_activites = revenus_mensualises + revenus_tns_annualises

        # L'aah est pris en compte comme revenu d'activité si revenu d'activité hors aah > 29 * smic horaire brut
        seuil_aah_activite = P.prestations.minima_sociaux.ppa.seuil_aah_activite * smic_horaire
        aah_activite = (revenus_activites >= seuil_aah_activite) * individu('aah', period)

        return revenus_activites + aah_activite


class ppa_rsa_derniers_revenus_tns_annuels_connus(Variable):
    value_type = float
    entity = Individu
    label = u"Derniers revenus non salariés annualisés connus"
    definition_period = YEAR

    def formula(individu, period):

        def get_last_known(variable_name):
            valeur_n = individu(variable_name, period)
            valeur_n_1 = individu(variable_name, period.last_year)
            valeur_n_2 = individu(variable_name, period.n_2)
            return select(
                [valeur_n > 0, valeur_n_1 > 0, valeur_n_2 > 0],
                [valeur_n, valeur_n_1, valeur_n_2]
                ) / 12.

        return (
            get_last_known('tns_benefice_exploitant_agricole') +
            get_last_known('tns_autres_revenus') +
            get_last_known('tns_micro_entreprise_benefice')
            )


class ppa_ressources_hors_activite(Variable):
    value_type = float
    entity = Famille
    label = u"Revenu hors activité pris en compte pour la PPA"
    definition_period = MONTH

    def formula(famille, period, parameters, mois_demande):
        pf = famille(
            'ppa_base_ressources_prestations_familiales', period, extra_params = [mois_demande])
        ressources_hors_activite_i = famille.members(
            'ppa_ressources_hors_activite_individu', period, extra_params = [mois_demande])
        ressources = [
            'ass',
            'aspa'
            ]

        ressources_hors_activite = famille.sum(ressources_hors_activite_i) + pf + sum(
            famille(ressource, mois_demande) for ressource in ressources)

        return ressources_hors_activite


class ppa_ressources_hors_activite_individu(Variable):
    value_type = float
    entity = Individu
    label = u"Revenu hors activité pris en compte pour la PPA (Individu) pour un mois"
    definition_period = MONTH

    def formula(individu, period, parameters, mois_demande):
        P = parameters(mois_demande)
        smic_horaire = P.cotsoc.gen.smic_h_b

        ressources = [
            'asi',
            'chomage_net',
            'retraite_nette',
            'retraite_combattant',
            'revenus_locatifs',
            'pensions_invalidite',
            'pensions_alimentaires_percues',
            'prestation_compensatoire',
            'prime_forfaitaire_mensuelle_reprise_activite',
            'rsa_indemnites_journalieres_hors_activite',
            ]

        ressources_hors_activite_mensuel_i = sum(
            individu(ressource, period) for ressource in ressources)
        revenus_activites = individu(
            'ppa_revenu_activite_individu', period, extra_params = [mois_demande])

        # L'aah est pris en compte comme revenu d'activité si  revenu d'activité hors aah > 29 * smic horaire brut
        seuil_aah_activite = P.prestations.minima_sociaux.ppa.seuil_aah_activite * smic_horaire
        aah_hors_activite = (revenus_activites < seuil_aah_activite) * individu('aah', period)

        return ressources_hors_activite_mensuel_i + aah_hors_activite


class ppa_base_ressources_prestations_familiales(Variable):
    value_type = float
    entity = Famille
    label = u"Prestations familiales prises en compte dans le calcul de la PPA"
    definition_period = MONTH

    def formula(famille, period, parameters, mois_demande):
        prestations_calculees = [
            'rsa_forfait_asf',
            'paje_base',
            ]
        prestations_autres = [
            'paje_clca',
            'paje_prepare',
            'paje_colca',
            ]

        result = sum(famille(prestation, mois_demande) for prestation in prestations_calculees)
        result += sum(famille(prestation, period) for prestation in prestations_autres)
        cf_non_majore_avant_cumul = famille('cf_non_majore_avant_cumul', mois_demande)
        cf = famille('cf', mois_demande)
        # Seul le montant non majoré est pris en compte dans la base de ressources du RSA
        cf_non_majore = (cf > 0) * cf_non_majore_avant_cumul

        af_base = famille('af_base', mois_demande)
        af = famille('af', mois_demande)

        result = result + cf_non_majore + min_(af_base, af)

        return result


class ppa_base_ressources(Variable):
    value_type = float
    entity = Famille
    label = u"Bases ressource prise en compte pour la PPA"
    definition_period = MONTH

    def formula(famille, period, parameters, mois_demande):
        ppa_revenu_activite = famille(
            'ppa_revenu_activite', period, extra_params = [mois_demande])
        ppa_ressources_hors_activite = famille(
            'ppa_ressources_hors_activite', period, extra_params = [mois_demande])
        return ppa_revenu_activite + ppa_ressources_hors_activite


class ppa_bonification(Variable):
    value_type = float
    entity = Individu
    label = u"Bonification de la PPA pour un individu"
    definition_period = MONTH

    def formula(individu, period, parameters, mois_demande):
        P = parameters(mois_demande)
        smic_horaire = P.cotsoc.gen.smic_h_b
        ppa_base = P.prestations.minima_sociaux.ppa.montant_de_base
        revenu_activite = individu(
            'ppa_revenu_activite_individu', period, extra_params = [mois_demande])
        seuil_1 = P.prestations.minima_sociaux.ppa.bonification.seuil_bonification * smic_horaire
        seuil_2 = P.prestations.minima_sociaux.ppa.bonification.seuil_max_bonification * smic_horaire
        bonification_max = round_(P.prestations.minima_sociaux.ppa.bonification.taux_bonification_max * ppa_base, 2)
        bonification = bonification_max * (revenu_activite - seuil_1) / (seuil_2 - seuil_1)
        bonification = max_(bonification, 0)
        bonification = min_(bonification, bonification_max)

        return bonification


class ppa_forfait_logement(Variable):
    value_type = float
    entity = Famille
    label = u"Forfait logement intervenant dans le calcul de la prime d'activité"
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=9A3FFF4142B563EB5510DDE9F2870BF4.tplgfr41s_2?idArticle=LEGIARTI000031675988&cidTexte=LEGITEXT000006073189&dateTexte=20171222"
    definition_period = MONTH

    def formula(famille, period, parameters):
        np_pers = famille('nb_parents', period) + famille('rsa_nb_enfants', period)
        aide_logement = famille('aide_logement', period)
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        participation_frais = famille.demandeur.menage('participation_frais', period)
        loyer = famille.demandeur.menage('loyer', period)

        avantage_nature = or_(
            ((statut_occupation_logement == TypesStatutOccupationLogement.primo_accedant) + (statut_occupation_logement == TypesStatutOccupationLogement.proprietaire)) * not_(loyer),
            (statut_occupation_logement == TypesStatutOccupationLogement.loge_gratuitement) * not_(participation_frais)
        )
        avantage_al = aide_logement > 0

        params = parameters(period).prestations.minima_sociaux.rsa
        montant_base = famille('ppa_montant_forfaitaire_familial_non_majore', period, extra_params = [period])
        montant_forfait = montant_base * (
            (np_pers == 1) * params.forfait_logement.taux_1_personne +
            (np_pers == 2) * params.forfait_logement.taux_2_personnes +
            (np_pers >= 3) * params.forfait_logement.taux_3_personnes_ou_plus
            )

        montant_al = avantage_al * min_(aide_logement, montant_forfait)
        montant_nature = avantage_nature * montant_forfait

        return max_(montant_al, montant_nature)


class ppa_fictive(Variable):
    value_type = float
    entity = Famille
    label = u"Prime pour l'activité fictive pour un mois"
    definition_period = MONTH

    def formula(famille, period, parameters, mois_demande):
        forfait_logement = famille('ppa_forfait_logement', mois_demande)
        ppa_majoree_eligibilite = famille('rsa_majore_eligibilite', mois_demande)

        elig = famille('ppa_eligibilite', period, extra_params = [mois_demande])
        pente = parameters(mois_demande).prestations.minima_sociaux.ppa.pente
        mff_non_majore = famille(
            'ppa_montant_forfaitaire_familial_non_majore', period, extra_params = [mois_demande])
        mff_majore = famille(
            'ppa_montant_forfaitaire_familial_majore', period, extra_params = [mois_demande])
        montant_forfaitaire_familialise = where(ppa_majoree_eligibilite, mff_majore, mff_non_majore)
        ppa_base_ressources = famille('ppa_base_ressources', period, extra_params = [mois_demande])
        ppa_revenu_activite = famille('ppa_revenu_activite', period, extra_params = [mois_demande])
        bonification_i = famille.members('ppa_bonification', period, extra_params = [mois_demande])
        bonification = famille.sum(bonification_i)

        ppa_montant_base = (
            montant_forfaitaire_familialise +
            bonification +
            pente * ppa_revenu_activite - ppa_base_ressources - forfait_logement
            )

        ppa_deduction = (
            montant_forfaitaire_familialise - ppa_base_ressources - forfait_logement
            )

        ppa_fictive = ppa_montant_base - max_(ppa_deduction, 0)
        ppa_fictive = max_(ppa_fictive, 0)
        return elig * ppa_fictive


class ppa(Variable):
    value_type = float
    entity = Famille
    label = u"Prime Pour l'Activité"
    definition_period = MONTH
    calculate_output = calculate_output_add
    # Prime d'activité sur service-public.fr
    reference = u"https://www.service-public.fr/particuliers/vosdroits/F2882"

    def formula_2016_01_01(famille, period, parameters):
        seuil_non_versement = parameters(period).prestations.minima_sociaux.ppa.seuil_non_versement
        # éligibilité étudiants

        ppa_eligibilite_etudiants = famille('ppa_eligibilite_etudiants', period)
        ppa = famille('ppa_fictive', period.last_3_months, extra_params = [period], options = [ADD]) / 3
        ppa = ppa * ppa_eligibilite_etudiants * (ppa >= seuil_non_versement)

        return ppa
