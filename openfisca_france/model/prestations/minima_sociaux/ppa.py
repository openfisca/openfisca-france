from openfisca_france.model.base import *

from numpy import round as round_, logical_or as or_, remainder as remainder_, datetime64


class ppa_eligibilite(Variable):
    value_type = bool
    entity = Famille
    label = "Eligibilité à la PPA pour un mois"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period, parameters):
        P = parameters(period).prestations
        age_min = P.minima_sociaux.ppa.age_min
        condition_age_i = famille.members('age', period) >= age_min
        condition_age = famille.any(condition_age_i)

        return condition_age


class ppa_plancher_revenu_activite_etudiant(Variable):
    value_type = float
    entity = Individu
    label = "Plancher des revenus d'activité pour être éligible à la PPA en tant qu'étudiant"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        P = parameters(period)

        return (
            169
            * P.marche_travail.salaire_minimum.smic_h_b
            * P.prestations.prestations_familiales.af.seuil_rev_taux
            )


class ppa_eligibilite_etudiants(Variable):
    value_type = bool
    entity = Famille
    label = "Eligibilité à la PPA (condition sur tout le trimestre)"
    reference = [
        "Article L842-1 du code de la sécurité sociale",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=46068A49B8592A593A05D64D8EDB045A.tplgfr26s_3?idArticle=LEGIARTI000031087527&cidTexte=LEGITEXT000006073189&dateTexte=20181226",
        "Article L842-2 du Code de la Sécurité Sociale",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=F2B88CEFCB83FCAFA4AA31671DAC89DD.tplgfr26s_3?idArticle=LEGIARTI000031087615&cidTexte=LEGITEXT000006073189&dateTexte=20181226"
        ]
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period, parameters):
        ppa_majoree_eligibilite = famille('rsa_majore_eligibilite', period)

        etudiant_i = famille.members('etudiant', period)
        plancher_etudiant = famille.members('ppa_plancher_revenu_activite_etudiant', period)

        def condition_ressource(period2, plancher):
            revenu_activite = famille.members('ppa_revenu_activite_individu', period2)
            return plancher < revenu_activite

        m_1 = period.offset(-1, 'month')
        m_2 = period.offset(-2, 'month')
        m_3 = period.offset(-3, 'month')

        condition_etudiant_i = (
            condition_ressource(m_1, plancher_etudiant)
            * condition_ressource(m_2, plancher_etudiant)
            * condition_ressource(m_3, plancher_etudiant)
            )

        condition_non_etudiant_i = (
            not_(etudiant_i) * (
                condition_ressource(m_1, 0)
                + condition_ressource(m_2, 0)
                + condition_ressource(m_3, 0)
                )
            )

        condition_famille = famille.any(condition_non_etudiant_i + condition_etudiant_i, role = Famille.PARENT)
        return ppa_majoree_eligibilite + condition_famille


class ppa_montant_forfaitaire_familial_non_majore(Variable):
    value_type = float
    entity = Famille
    label = "Montant forfaitaire familial (sans majoration)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        nb_parents = famille('nb_parents', period)
        nb_enfants = famille('rsa_nb_enfants', period)
        ppa_majoree_eligibilite = famille('rsa_majore_eligibilite', period)  # noqa F841
        ppa = parameters(period).prestations.minima_sociaux.ppa

        nb_personnes = nb_parents + nb_enfants

        # Dans la formule "ppa_forfait_logement", le montant forfaitaire se calcule pour trois personnes dans le cas où le foyer se compose de trois personnes ou plus.
        taux_non_majore = (
            1
            + (nb_personnes >= 2) * ppa.taux_deuxieme_personne
            + (nb_personnes >= 3) * ppa.taux_troisieme_personne
            + (nb_personnes >= 4) * where(nb_parents == 1, ppa.taux_personne_supp, ppa.taux_troisieme_personne)
            # Si nb_parents == 1, pas de conjoint, la 4e personne est un enfant, donc le taux est de 40%.
            + max_(nb_personnes - 4, 0) * ppa.taux_personne_supp
            )

        return ppa.montant_de_base * taux_non_majore


class ppa_montant_forfaitaire_familial_majore(Variable):
    value_type = float
    entity = Famille
    label = "Montant forfaitaire familial (avec majoration)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        nb_enfants = famille('rsa_nb_enfants', period)
        ppa = parameters(period).prestations.minima_sociaux.ppa

        taux_majore = (
            ppa.majoration_isolement_femme_enceinte
            + ppa.majoration_isolement_enf_charge
            * nb_enfants
            )

        return ppa.montant_de_base * taux_majore


class ppa_revenu_activite(Variable):
    value_type = float
    entity = Famille
    label = "Revenu d'activité pris en compte pour la PPA"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        ppa_revenu_activite_i = famille.members(
            'ppa_revenu_activite_individu', period)
        ppa_revenu_activite = famille.sum(ppa_revenu_activite_i)

        return ppa_revenu_activite


class ppa_revenu_activite_individu(Variable):
    value_type = float
    entity = Individu
    label = "Revenu d'activité pris en compte pour la PPA (Individu) pour un mois"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'Article L842-4 du code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=358C45A1DF4FA63CC63BEC9456F63F18.tplgfr21s_3?idArticle=LEGIARTI000033813782&cidTexte=LEGITEXT000006073189',
        'Article R844-1 du code de la sécurité sociale',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=358C45A1DF4FA63CC63BEC9456F63F18.tplgfr21s_3?idArticle=LEGIARTI000031675756&cidTexte=LEGITEXT000006073189'
        ]

    def formula(individu, period, parameters):
        P = parameters(period)
        smic_horaire = P.marche_travail.salaire_minimum.smic_h_b

        ressources = [
            'salaire_net',
            'revenus_stage_formation_pro',
            'remuneration_apprenti',
            'bourse_recherche',
            'indemnites_chomage_partiel',
            'rpns_auto_entrepreneur_benefice',
            'rsa_indemnites_journalieres_activite'
            ]

        revenus_mensualises = sum(individu(ressource, period) for ressource in ressources)

        revenus_tns_annualises = individu('ppa_rsa_derniers_revenus_tns_annuels_connus', period.this_year)

        revenus_activites = revenus_mensualises + revenus_tns_annualises

        # L'aah est pris en compte comme revenu d'activité si revenu d'activité hors aah > 29 * smic horaire brut
        seuil_aah_activite = P.prestations.minima_sociaux.ppa.seuil_aah_activite * smic_horaire
        aah_activite = (revenus_activites >= seuil_aah_activite) * individu('aah', period)

        return revenus_activites + aah_activite


class ppa_rsa_derniers_revenus_tns_annuels_connus(Variable):
    value_type = float
    entity = Individu
    label = "Derniers revenus non salariés annualisés connus"
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
            get_last_known('rpns_benefice_exploitant_agricole')
            + get_last_known('rpns_autres_revenus')
            + get_last_known('rpns_micro_entreprise_benefice')
            )


class ppa_ressources_hors_activite(Variable):
    value_type = float
    entity = Famille
    label = "Revenu hors activité pris en compte pour la PPA"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        aspa = famille('aspa', period)
        pf = famille('ppa_base_ressources_prestations_familiales', period)

        ass_i = famille.members('ass', period)
        ressources_hors_activite_i = famille.members('ppa_ressources_hors_activite_individu', period)

        return aspa + pf + famille.sum(ass_i + ressources_hors_activite_i)


class ppa_ressources_hors_activite_individu(Variable):
    value_type = float
    entity = Individu
    label = "Revenu hors activité pris en compte pour la PPA (Individu) pour un mois"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        # Article L842-4 du code de la sécurité sociale
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=B1D8827D50F7B3CC603BB7D398E71AA8.tplgfr28s_3?idArticle=LEGIARTI000033813782&cidTexte=LEGITEXT000006073189&dateTexte=20181226",
        # Article R843-1 du code de la sécurité sociale
        "https://www.legifrance.gouv.fr/affichCode.do;jsessionid=3D8AB2FEC931285820291B1F952160BA.tpdila22v_2?idSectionTA=LEGISCTA000031694323&cidTexte=LEGITEXT000006073189&dateTexte=20160215"
        ]

    def formula(individu, period, parameters):
        P = parameters(period)
        smic_horaire = P.marche_travail.salaire_minimum.smic_h_b

        def ressources_percues_au_cours_du_mois_considere():
            ressources = [
                'asi',
                'caah',
                'chomage_net',
                'retraite_nette',
                'retraite_combattant',
                'pensions_invalidite',
                'pensions_alimentaires_percues',
                'prestation_compensatoire',
                'prime_forfaitaire_mensuelle_reprise_activite',
                'rsa_indemnites_journalieres_hors_activite',
                ]

            return sum(individu(ressource, period) for ressource in ressources)

        def ressources_percues_il_y_a_deux_ans():
            ressources_individuelles_mensuelles = [
                'revenus_capital',
                'revenus_locatifs',
                ]

            revenus_annuels = sum(individu(ressource, period.offset(-2, 'year').this_year, options = [ADD]) for ressource in ressources_individuelles_mensuelles)
            plus_values_annuelles = (
                individu.foyer_fiscal('assiette_csg_plus_values', period.offset(-2, 'year').this_year)
                + individu.foyer_fiscal('rente_viagere_titre_onereux', period.offset(-2, 'year').this_year, options = [ADD])
                ) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

            return (revenus_annuels + plus_values_annuelles) / 12

        ressources_hors_activite_mensuel_i = (
            + ressources_percues_au_cours_du_mois_considere()
            + ressources_percues_il_y_a_deux_ans()
            )

        revenus_activites = individu('ppa_revenu_activite_individu', period)

        # L'AAH est prise en compte comme revenu d'activité si revenu d'activité hors aah > 29 * smic horaire brut
        seuil_aah_activite = P.prestations.minima_sociaux.ppa.seuil_aah_activite * smic_horaire
        aah_hors_activite = (revenus_activites < seuil_aah_activite) * individu('aah', period)

        return ressources_hors_activite_mensuel_i + aah_hors_activite


class ppa_base_ressources_prestations_familiales(Variable):
    value_type = float
    entity = Famille
    label = "Prestations familiales prises en compte dans le calcul de la PPA"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "Pour la prise en compte du complément familial, II. de l'article R844-4 du code de la sécurité sociale",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=210D97A377874C24466BA7DE746FFF78.tplgfr27s_3?idArticle=LEGIARTI000031676000&cidTexte=LEGITEXT000006073189",
        "Pour la prise en compte des allocations familiales, 3° de l'article R844-5 du code de la sécurité sociale",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=210D97A377874C24466BA7DE746FFF78.tplgfr27s_3?idArticle=LEGIARTI000031676016&cidTexte=LEGITEXT000006073189"
        ]

    def formula(famille, period, parameters):
        prestations = [
            'paje_base',
            'paje_clca',
            'paje_prepare',
            'paje_colca',
            'rsa_forfait_asf'
            ]

        result = sum(famille(prestation, period) for prestation in prestations)

        cf_non_majore_avant_cumul = famille('cf_non_majore_avant_cumul', period)
        cf = famille('cf', period)
        cf_pris_en_compte = (cf > 0) * cf_non_majore_avant_cumul

        af_base = famille('af_base', period)
        af = famille('af', period)
        af_prises_en_compte = min_(af_base, af)

        result = result + cf_pris_en_compte + af_prises_en_compte

        return result


class ppa_base_ressources(Variable):
    value_type = float
    entity = Famille
    label = "Bases ressource prise en compte pour la PPA"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        ppa_revenu_activite = famille('ppa_revenu_activite', period)
        ppa_ressources_hors_activite = famille('ppa_ressources_hors_activite', period)
        return ppa_revenu_activite + ppa_ressources_hors_activite


class ppa_bonification(Variable):
    value_type = float
    entity = Individu
    label = "Bonification de la PPA pour un individu"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        P = parameters(period)
        smic_horaire = P.marche_travail.salaire_minimum.smic_h_b
        ppa_base = P.prestations.minima_sociaux.ppa.montant_de_base
        revenu_activite = individu('ppa_revenu_activite_individu', period)
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
    label = "Forfait logement intervenant dans le calcul de la prime d'activité"
    reference = "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=9A3FFF4142B563EB5510DDE9F2870BF4.tplgfr41s_2?idArticle=LEGIARTI000031675988&cidTexte=LEGITEXT000006073189"
    definition_period = MONTH
    set_input = set_input_divide_by_period

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
        ppa = parameters(period).prestations.minima_sociaux.ppa

        # Le montant forfaitaire se calcule de la même manière que celle de la formule 'ppa_montant_forfaitaire_familial_non_majore',
        # sauf dans le cas où le foyer se compose de trois personnes ou plus, où le montant forfaitaire se calcule pour trois personnes seulement.
        taux_non_majore = (
            1
            + (np_pers >= 2) * ppa.taux_deuxieme_personne
            + (np_pers >= 3) * ppa.taux_troisieme_personne
            )

        montant_base = ppa.montant_de_base * taux_non_majore

        montant_forfait = montant_base * (
            (np_pers == 1) * params.forfait_logement.taux_1_personne
            + (np_pers == 2) * params.forfait_logement.taux_2_personnes
            + (np_pers >= 3) * params.forfait_logement.taux_3_personnes_ou_plus
            )

        montant_al = avantage_al * min_(aide_logement, montant_forfait)
        montant_nature = avantage_nature * montant_forfait

        return max_(montant_al, montant_nature)


class ppa_fictive_ressource_activite(Variable):
    value_type = float
    entity = Famille
    label = "Proportion de ressources provenant de l'activité prise en compte pour la primie d'activité fictive"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period, parameters):
        pente = parameters(period).prestations.minima_sociaux.ppa.pente
        ppa_revenu_activite = famille('ppa_revenu_activite', period)

        return pente * ppa_revenu_activite


class ppa_fictive_montant_forfaitaire(Variable):
    value_type = float
    entity = Famille
    label = "Montant forfaitaire de la prime d'activité fictive"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        ppa_majoree_eligibilite = famille('rsa_majore_eligibilite', period)
        mff_non_majore = famille('ppa_montant_forfaitaire_familial_non_majore', period)
        mff_majore = famille('ppa_montant_forfaitaire_familial_majore', period)

        return where(ppa_majoree_eligibilite, mff_majore, mff_non_majore)


class ppa_fictive(Variable):
    value_type = float
    entity = Famille
    label = "Prime pour l'activité fictive pour un mois"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        forfait_logement = famille('ppa_forfait_logement', period)
        elig = famille('ppa_eligibilite', period)
        montant_forfaitaire_familialise = famille('ppa_fictive_montant_forfaitaire', period)
        ppa_base_ressources = famille('ppa_base_ressources', period)
        ppa_fictive_ressource_activite = famille('ppa_fictive_ressource_activite', period)
        bonification_i = famille.members('ppa_bonification', period)
        bonification = famille.sum(bonification_i)

        ppa_montant_base = (
            montant_forfaitaire_familialise
            + bonification
            + ppa_fictive_ressource_activite
            - ppa_base_ressources
            - forfait_logement
            )

        ppa_deduction = (
            montant_forfaitaire_familialise
            - ppa_base_ressources
            - forfait_logement
            )

        ppa_fictive = ppa_montant_base - max_(ppa_deduction, 0)
        ppa_fictive = max_(ppa_fictive, 0)
        return elig * ppa_fictive


class ppa(Variable):
    value_type = float
    entity = Famille
    label = "Prime Pour l'Activité"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add
    # Prime d'activité sur service-public.fr
    reference = "https://www.service-public.fr/particuliers/vosdroits/F2882"

    def formula_2016_01_01(famille, period, parameters):
        seuil_non_versement = parameters(period).prestations.minima_sociaux.ppa.seuil_non_versement
        # éligibilité étudiants

        ppa_eligibilite_etudiants = famille('ppa_eligibilite_etudiants', period)
        ppa = famille('ppa_fictive', period.last_3_months, options = [ADD]) / 3
        ppa = ppa * ppa_eligibilite_etudiants * (ppa >= seuil_non_versement)

        return ppa


class ppa_mois_demande(Variable):
    value_type = date
    entity = Famille
    definition_period = ETERNITY
    label = "Date de la demande de la prime pour l'activité"


class ppa_indice_du_mois_trimestre_reference(Variable):
    value_type = int
    entity = Famille
    label = "Nombre de mois par rapport au mois de du précédent recalcul de la prime d'activité"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period, parameters):
        ppa_mois_demande = famille('ppa_mois_demande', period)
        nombre_mois = (datetime64(period.start).astype('datetime64[M]') - ppa_mois_demande.astype('datetime64[M]')).astype('int')
        return remainder_(nombre_mois, 3)


class ppa_versee(Variable):
    value_type = float
    entity = Famille
    label = "Prime pour l'activité versée en prenant en compte la date de la demande"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        remainder = famille('ppa_indice_du_mois_trimestre_reference', period)
        return (
            + famille('ppa', period) * (remainder == 0)
            + famille('ppa', period.last_month) * (remainder == 1)
            + famille('ppa', period.last_month.last_month) * (remainder == 2)
            )
