# -*- coding: utf-8 -*-

from __future__ import division


from numpy import datetime64, floor, logical_and as and_, logical_or as or_

from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf


class rsa_base_ressources(Variable):
    value_type = float
    label = u"Base ressources du Rmi ou du Rsa"
    entity = Famille
    definition_period = MONTH

    def formula_2017_01_01(famille, mois_demande, parameters, mois_courant):
        rsa_base_ressources_prestations_familiales = famille('rsa_base_ressources_prestations_familiales', mois_demande, extra_params = [mois_courant])
        rsa_base_ressources_minima_sociaux = famille('rsa_base_ressources_minima_sociaux', mois_demande, extra_params = [mois_courant])

        enfant_i = famille.members('est_enfant_dans_famille', mois_courant)
        rsa_enfant_a_charge_i = famille.members('rsa_enfant_a_charge', mois_courant)

        # Les ressources hors PF sont moyennées, à partir de mois_demande.last_3_months

        ressources_individuelles_i = (
            famille.members('rsa_base_ressources_individu', mois_demande) +
            famille.members('rsa_revenu_activite_individu', mois_demande, extra_params = [mois_courant])
            )

        ressources_individuelles = famille.sum(
            (not_(enfant_i) + rsa_enfant_a_charge_i) * ressources_individuelles_i
            )


        return (
            rsa_base_ressources_prestations_familiales + rsa_base_ressources_minima_sociaux + ressources_individuelles
            )

    def formula_2009_06_01(famille, period):
        rsa_base_ressources_prestations_familiales = famille('rsa_base_ressources_prestations_familiales', period)
        rsa_base_ressources_minima_sociaux = famille('rsa_base_ressources_minima_sociaux', period)

        enfant_i = famille.members('est_enfant_dans_famille', period)
        rsa_enfant_a_charge_i = famille.members('rsa_enfant_a_charge', period)
        ressources_individuelles_i = (
            famille.members('rsa_base_ressources_individu', period) +
            famille.members('rsa_revenu_activite_individu', period)
            )

        ressources_individuelles = famille.sum(
            (not_(enfant_i) + rsa_enfant_a_charge_i) * ressources_individuelles_i
            )

        return (
            rsa_base_ressources_prestations_familiales + rsa_base_ressources_minima_sociaux + ressources_individuelles
            )

    def formula(famille, period):
        rsa_base_ressources_prestations_familiales = famille('rsa_base_ressources_prestations_familiales', period)
        rsa_base_ressources_minima_sociaux = famille('rsa_base_ressources_minima_sociaux', period)

        rsa_base_ressources_i = famille.members('rsa_base_ressources_individu', period)
        rsa_base_ressources_i_total = famille.sum(rsa_base_ressources_i)

        return (
            rsa_base_ressources_prestations_familiales +
            rsa_base_ressources_minima_sociaux +
            rsa_base_ressources_i_total
            )


class rsa_has_ressources_substitution(Variable):
    value_type = bool
    label = u"Présence de ressources de substitution au mois M, qui désactivent la neutralisation des revenus professionnels interrompus au moins M."
    entity = Individu
    definition_period = MONTH

    def formula(famille, period):
        return (
            famille('chomage_net', period) +
            famille('indemnites_journalieres', period) +
            famille('retraite_nette', period)
            ) > 0


class rsa_base_ressources_individu(Variable):
    value_type = float
    label = u"Base ressource individuelle du RSA/RMI (hors revenus d'actvité)"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        # Revenus professionels
        types_revenus_pros = [
            'chomage_net',
            'retraite_nette',
            ]

        has_ressources_substitution = individu('rsa_has_ressources_substitution', period)

        # Les revenus pros interrompus au mois M sont neutralisés s'il n'y a pas de revenus de substitution.
        revenus_pro = sum(
            individu(type_revenu, period.last_3_months, options = [ADD]) * not_(
                (individu(type_revenu, period) == 0) *
                (individu(type_revenu, period.last_month) > 0) *
                not_(has_ressources_substitution)
                )
            for type_revenu in types_revenus_pros
            )

        types_revenus_non_pros = [
            'allocation_aide_retour_emploi',
            'allocation_securisation_professionnelle',
            'dedommagement_victime_amiante',
            'div_ms',
            'gains_exceptionnels',
            'pensions_alimentaires_percues',
            'pensions_invalidite',
            'prestation_compensatoire',
            'prime_forfaitaire_mensuelle_reprise_activite',
            'rsa_base_ressources_patrimoine_individu',
            'rsa_indemnites_journalieres_hors_activite',
            ]

        # Les revenus non-pro interrompus au mois M sont neutralisés dans la limite d'un montant forfaitaire,
        # sans condition de revenu de substitution.
        neutral_max_forfaitaire = 3 * parameters(period).prestations.minima_sociaux.rmi.rmi
        revenus_non_pros = sum(
            max_(0, individu(type_revenu, period.last_3_months, options = [ADD]) - neutral_max_forfaitaire * (
                (individu(type_revenu, period) == 0) *
                (individu(type_revenu, period.last_month) > 0)
                ))
            for type_revenu in types_revenus_non_pros
            )

        # Revenus du foyer fiscal que l'on projette sur le premier invidividus
        rev_cap_bar = max_(0, individu.foyer_fiscal('rev_cap_bar', period.last_3_months, options = [ADD]))
        rev_cap_lib = max_(0, individu.foyer_fiscal('rev_cap_lib', period.last_3_months, options = [ADD]))
        retraite_titre_onereux = individu.foyer_fiscal('retraite_titre_onereux', period.last_3_months, options = [ADD])
        revenus_foyer_fiscal = rev_cap_bar + rev_cap_lib + retraite_titre_onereux
        revenus_foyer_fiscal_projetes = revenus_foyer_fiscal * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        return (revenus_pro + revenus_non_pros + revenus_foyer_fiscal_projetes) / 3


class rsa_base_ressources_minima_sociaux(Variable):
    value_type = float
    label = u"Minima sociaux inclus dans la base ressource RSA/RMI"
    entity = Famille
    definition_period = MONTH

    def formula_2017_01_01(famille, mois_demande, parameters, mois_courant):
        # Prestations calculées que l'on réinjecte dans la BR du RSA
        aspa = famille('aspa', mois_demande)
        asi = famille('asi', mois_demande)
        ass = famille('ass', mois_demande)

        aah_i = famille.members('aah', mois_courant)
        caah_i = famille.members('caah', mois_courant)

        return aspa + asi + ass + famille.sum(aah_i + caah_i)

    def formula(famille, period):
        three_previous_months = period.last_3_months
        aspa = famille('aspa', period)
        asi = famille('asi', period)
        ass = famille('ass', period)
        aah_i = famille.members('aah', three_previous_months, options = [ADD]) / 3
        caah_i = famille.members('caah', three_previous_months, options = [ADD]) / 3

        return aspa + asi + ass + famille.sum(aah_i + caah_i)


class rsa_base_ressources_prestations_familiales(Variable):
    value_type = float
    entity = Famille
    label = u"Prestations familiales inclues dans la base ressource RSA/RMI"
    definition_period = MONTH

    def formula_2002_01_01(famille, period):
        prestations = [
            'af_base',
            'cf',
            'asf',
            'apje',
            'ape',
            ]
        result = sum(famille(prestation, period) for prestation in prestations)

        return result

    def formula_2004_01_01(famille, period):
        prestations = [
            'af_base',
            'cf',
            'asf',
            'paje_base',
            'paje_clca',
            'paje_prepare',
            'paje_colca',
            ]

        result = sum(famille(prestation, period) for prestation in prestations)

        return result

    def formula_2014_04_01(famille, period):
        # TODO : Neutraliser les ressources de type prestations familiales quand elles sont interrompues
        prestations_calculees = [
            'rsa_forfait_asf',
            'paje_base',
           ]
        prestations_autres = [
            'paje_clca',
            'paje_prepare',
            'paje_colca',
            ]

        # On réinjecte le montant des prestations calculées
        result = sum(famille(prestation, period) for prestation in prestations_calculees)

        result += sum(
            famille(prestation, period.last_3_months, options = [ADD]) / 3 for prestation in prestations_autres)

        cf_non_majore_avant_cumul = famille('cf_non_majore_avant_cumul', period)
        cf = famille('cf', period)
        # Seul le montant non majoré est pris en compte dans la base de ressources du RSA
        cf_non_majore = (cf > 0) * cf_non_majore_avant_cumul

        af_base = famille('af_base', period)
        af = famille('af', period)

        result = result + cf_non_majore + min_(af_base, af)  # Si des AF on été injectées et sont plus faibles que le cf

        return result

    def formula_2017_01_01(famille, mois_demande, parameters, mois_courant):
        # TODO : Neutraliser les ressources de type prestations familiales quand elles sont interrompues
        prestations_calculees = [
            'rsa_forfait_asf',
            'paje_base',
           ]
        prestations_autres = [
            'paje_clca',
            'paje_prepare',
            'paje_colca',
            ]

        # On réinjecte le montant des prestations calculées
        result = sum(famille(prestation, mois_demande) for prestation in prestations_calculees)

        result += sum(famille(prestation, mois_courant) for prestation in prestations_autres)

        cf_non_majore_avant_cumul = famille('cf_non_majore_avant_cumul', mois_demande)
        cf = famille('cf', mois_demande)
        # Seul le montant non majoré est pris en compte dans la base de ressources du RSA
        cf_non_majore = (cf > 0) * cf_non_majore_avant_cumul

        af_base = famille('af_base', mois_demande)
        af = famille('af', mois_demande)

        result = result + cf_non_majore + min_(af_base, af)  # Si des AF on été injectées et sont plus faibles que le cf

        return result


class crds_mini(Variable):
    value_type = float
    entity = Famille
    label = u"CRDS versée sur les minimas sociaux"
    definition_period = MONTH

    def formula_2009_06_01(famille, period, parameters):
        rsa_activite = famille('rsa_activite', period)
        taux_crds = parameters(period).prelevements_sociaux.contributions.crds.taux

        return - taux_crds * rsa_activite


class div_ms(Variable):
    value_type = float
    entity = Individu
    label = u"Dividende entrant en compte dans le calcul des minimas sociaux"
    definition_period = MONTH

    def formula(individu, period):
        period_declaration = period.this_year
        f3vc = individu.foyer_fiscal('f3vc', period_declaration)
        f3ve = individu.foyer_fiscal('f3ve', period_declaration)
        f3vg = individu.foyer_fiscal('f3vg', period_declaration)
        f3vl = individu.foyer_fiscal('f3vl', period_declaration)
        f3vm = individu.foyer_fiscal('f3vm', period_declaration)
        f3vt = individu.foyer_fiscal('f3vt', period_declaration)

        # On projette les revenus du foyer fiscal seulement sur le déclarant principal
        return (f3vc + f3ve + f3vg + f3vl + f3vm + f3vt) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL) / 12


class enceinte_fam(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH

    def formula(famille, period):
        enceinte_i = famille.members('enceinte', period)
        parent_enceinte = famille.any(enceinte_i, role = Famille.PARENT)

        age_en_mois_i = famille.members('age_en_mois', period)
        age_en_mois_benjamin = famille.min(age_en_mois_i, role = Famille.ENFANT)

        enceinte_compat = and_(age_en_mois_benjamin < 0, age_en_mois_benjamin > -6)
        return parent_enceinte + enceinte_compat


class rsa_enfant_a_charge(Variable):
    value_type = bool
    entity = Individu
    label = u"Enfant pris en compte dans le calcul du RSA"
    definition_period = MONTH

    def formula(individu, period, parameters):
        P_rsa = parameters(period).prestations.minima_sociaux.rsa
        P_rmi = parameters(period).prestations.minima_sociaux.rmi

        enfant = individu('est_enfant_dans_famille', period)
        age = individu('age', period)
        autonomie_financiere = individu('autonomie_financiere', period)

        if period.start.date >= date(2017, 01, 01):
            m_1 = period.last_month
            m_2 = m_1.last_month
            m_3 = m_2.last_month
            ressources = (
                individu('rsa_base_ressources_individu', period) +
                individu('rsa_revenu_activite_individu', period, extra_params = [m_1]) / 3 +
                individu('rsa_revenu_activite_individu', period, extra_params = [m_2]) / 3 +
                individu('rsa_revenu_activite_individu', period, extra_params = [m_3]) / 3
                )
        else:
            ressources = (
                individu('rsa_base_ressources_individu', period) +
                (1 - P_rsa.pente) * individu('rsa_revenu_activite_individu', period)
                )

        # Les parametres ont changé de nom au moment où le RMI est devenu le RSA
        if period.start.date >= date(2009, 6, 01):
            age_pac = P_rsa.age_pac
            majo_rsa = P_rsa.majo_rsa
            montant_base_rsa = P_rsa.montant_de_base_du_rsa
            taux_personne_supp = P_rsa.majoration_rsa.taux_personne_supp
        else:
            age_pac = P_rmi.age_pac
            majo_rsa = P_rmi.majo_rsa
            montant_base_rsa = P_rmi.rmi
            taux_personne_supp = P_rmi.txps

        # Règle CAF: Si un enfant touche des ressources, et que son impact global
        # (augmentation du montant forfaitaire - ressources prises en compte) fait baisser le montant du RSA, alors
        # il doit être exclu du calcul du RSA.
        # Cette règle est complexe, on applique donc l'approximation suivante:
        #       - Cas général: enfant pris en compte si ressources <= augmentation du MF pour un enfant
        #                      supplémentaire (taux marginal).
        #       - Si la présence de l'enfant ouvre droit au RSA majoré, pris en compte si
        #                      ressources <= majoration du RSA pour isolement avec un enfant.
        def ouvre_droit_majoration():
            famille = individu.famille
            enceinte_fam = famille('enceinte_fam', period)
            isole = not_(famille('en_couple', period))
            isolement_recent = famille('rsa_isolement_recent', period)

            presence_autres_enfants = famille.sum(enfant * not_(autonomie_financiere) * (age <= age_pac)) > 1

            # individu.famille.sum retourne un résultat qui n'est pas implicitement projeté sur l'individu.
            return not_(enceinte_fam) * isole * isolement_recent * not_(famille.project(presence_autres_enfants))

        rsa_enf_charge = enfant * not_(autonomie_financiere) * (age <= age_pac) * where(
            ouvre_droit_majoration(),
            ressources < (majo_rsa.pac0 - 1 + majo_rsa.pac_enf_sup) * montant_base_rsa,
            ressources < taux_personne_supp * montant_base_rsa
            )

        return rsa_enf_charge


class rsa_nb_enfants(Variable):
    value_type = int
    entity = Famille
    label = u"Nombre d'enfants pris en compte pour le calcul du RSA"
    definition_period = MONTH

    def formula(famille, period):
        return famille.sum(famille.members('rsa_enfant_a_charge', period))


class participation_frais(Variable):
    value_type = bool
    entity = Menage
    label = u"Partipation aux frais de logement pour un hebergé à titre gratuit"
    definition_period = MONTH


class rsa_revenu_activite(Variable):
    value_type = float
    label = u"Revenus d'activité du RSA"
    entity = Famille
    definition_period = MONTH

    def formula_2009_06_01(famille, period):
        rsa_revenu_activite_i = famille.members('rsa_revenu_activite_individu', period)
        rsa_enfant_a_charge_i = famille.members('rsa_enfant_a_charge', period)
        enfant_i = famille.members('est_enfant_dans_famille', period)

        return famille.sum(
            or_(not_(enfant_i), rsa_enfant_a_charge_i) * rsa_revenu_activite_i
            )


class rsa_indemnites_journalieres_activite(Variable):
    value_type = float
    label = u"Indemnités journalières prises en compte comme revenu d'activité"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        m_3 = period.offset(-3, 'month')

        def ijss_activite_sous_condition(period):
            return sum(individu(ressource, period) for ressource in [
                # IJSS prises en compte comme un revenu d'activité seulement les 3 premiers mois qui suivent l'arrêt de travail
                'indemnites_journalieres_maladie',
                'indemnites_journalieres_accident_travail',
                'indemnites_journalieres_maladie_professionnelle',
            ])


        date_arret_de_travail = individu('date_arret_de_travail', period)
        three_months_ago = datetime64(m_3.start)
        condition_date_arret_travail = date_arret_de_travail > three_months_ago

        # Si la date d'arrêt de travail n'est pas définie (et vaut donc par défaut date.min), mais qu'il n'y a pas d'IJSS à M-3, on estime que l'arrêt est récent.
        is_date_arret_de_travail_undefined = (date_arret_de_travail == date.min)
        condition_arret_recent = is_date_arret_de_travail_undefined * (ijss_activite_sous_condition(m_3) == 0)

        condition_activite = individu('salaire_net', period) > 0

        ijss_activite = sum(individu(ressource, period) for ressource in [
            # IJSS toujours prises en compte comme un revenu d'activité
            'indemnites_journalieres_maternite',
            'indemnites_journalieres_paternite',
            'indemnites_journalieres_adoption',
        ]) + (condition_date_arret_travail + condition_activite + condition_arret_recent) * ijss_activite_sous_condition(period)

        return ijss_activite


class rsa_indemnites_journalieres_hors_activite(Variable):
    value_type = float
    label = u"Indemnités journalières prises en compte comme revenu de remplacement"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        return (
            + individu('indemnites_journalieres', period)
            - individu('rsa_indemnites_journalieres_activite', period)
            )


class primes_salaires_net(Variable):
    value_type = float
    entity = Individu
    label = u"Indemnités, primes et avantages en argent (net)"
    definition_period = MONTH



class salaire_net_hors_revenus_exceptionnels(Variable):
    value_type = float
    label = u"Salaire net hors prime, indemnites de licenciement, prime de précarité..."
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        return (
            individu('salaire_net', period) -
            individu('primes_salaires_net', period) -
            individu('indemnite_fin_contrat_net', period)
            )


class rsa_revenu_activite_individu(Variable):
    value_type = float
    label = u"Revenus d'activité du Rsa - Individuel"
    entity = Individu
    definition_period = MONTH

    def formula_2017_01_01(individu, mois_demande, parameters, mois_courant):
        last_3_months = mois_demande.last_3_months

        types_revenus_activite = [
            'salaire_net_hors_revenus_exceptionnels',
            'indemnites_chomage_partiel',
            'indemnites_volontariat',
            'revenus_stage_formation_pro',
            'bourse_recherche',
            'hsup',
            'etr',
            'tns_auto_entrepreneur_benefice',
            'rsa_indemnites_journalieres_activite',
            ]

        has_ressources_substitution = individu('rsa_has_ressources_substitution', mois_demande)

        # Les revenus pros interrompus au mois M sont neutralisés s'il n'y a pas de revenus de substitution.

        revenus_moyennes = sum(
            individu(type_revenu, last_3_months, options = [ADD]) * not_(
                (individu(type_revenu, mois_demande) == 0) *
                (individu(type_revenu, mois_demande.last_month) > 0) *
                not_(has_ressources_substitution)
                )
            for type_revenu in types_revenus_activite
            ) / 3

        revenus_tns_annualises = individu('ppa_rsa_derniers_revenus_tns_annuels_connus', mois_demande.this_year)

        revenus_non_moyennes = (
            individu('primes_salaires_net', mois_courant) +
            individu('indemnite_fin_contrat_net', mois_courant)
            )

        return revenus_moyennes + revenus_tns_annualises + revenus_non_moyennes

    def formula_2009_06(individu, period):
        last_3_months = period.last_3_months

        # Note Auto-entrepreneurs:
        # D'après les caisses, le revenu pris en compte pour les AE pour le RSA ne prend en compte que
        # l'abattement standard sur le CA, mais pas les cotisations pour charges sociales.

        types_revenus_activite = [
            'salaire_net',
            'indemnites_chomage_partiel',
            'indemnites_volontariat',
            'revenus_stage_formation_pro',
            'bourse_recherche',
            'hsup',
            'etr',
            'tns_auto_entrepreneur_benefice',
            'rsa_indemnites_journalieres_activite',
            ]

        has_ressources_substitution = individu('rsa_has_ressources_substitution', period)

        # Les revenus pros interrompus au mois M sont neutralisés s'il n'y a pas de revenus de substitution.
        return sum(
            individu(type_revenu, last_3_months, options = [ADD]) * not_(
                (individu(type_revenu, period.first_month) == 0) *
                (individu(type_revenu, period.last_month) > 0) *
                not_(has_ressources_substitution)
                )
            for type_revenu in types_revenus_activite
            ) / 3


class rsa_fictif(Variable):
    value_type = float
    entity = Famille
    label = "RSA fictif pour un mois"
    definition_period = MONTH

    def formula_2016_10(famille, mois_courant, parameters, mois_demande):
        rsa_socle_non_majore = famille('rsa_socle', mois_courant)
        rsa_socle_majore = famille('rsa_socle_majore', mois_courant)
        rsa_socle = max_(rsa_socle_non_majore, rsa_socle_majore)

        rsa_forfait_logement = famille('rsa_forfait_logement', mois_demande)
        rsa_base_ressources = famille('rsa_base_ressources', mois_demande, extra_params = [mois_courant])

        montant = rsa_socle - rsa_forfait_logement - rsa_base_ressources
        montant = max_(montant, 0)

        return montant


class rsa_montant(Variable):
    value_type = float
    label = u"Revenu de solidarité active, avant prise en compte de la non-calculabilité."
    entity = Famille
    definition_period = MONTH

    def formula_2017_01_01(famille, period, parameters):
        seuil_non_versement = parameters(period).prestations.minima_sociaux.rsa.rsa_nv

        rsa = famille('rsa_fictif', period.last_3_months, extra_params = [period], options = [ADD]) / 3
        rsa = rsa * (rsa >= seuil_non_versement)

        return rsa

    def formula_2009_06(famille, period, parameters):
        rsa_socle_non_majore = famille('rsa_socle', period)
        rsa_socle_majore = famille('rsa_socle_majore', period)
        rsa_socle = max_(rsa_socle_non_majore, rsa_socle_majore)

        rsa_revenu_activite = famille('rsa_revenu_activite', period)
        rsa_forfait_logement = famille('rsa_forfait_logement', period)
        rsa_base_ressources = famille('rsa_base_ressources', period)

        P = parameters(period).prestations.minima_sociaux.rsa
        seuil_non_versement = P.rsa_nv

        montant = rsa_socle - rsa_forfait_logement - rsa_base_ressources + P.pente * rsa_revenu_activite

        montant = max_(montant, 0)
        montant = montant * (montant >= seuil_non_versement)

        return montant


class rsa(Variable):
    calculate_output = calculate_output_add
    value_type = float
    label = u"Revenu de solidarité active"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2009_06(famille, period):
        montant = famille('rsa_montant', period)
        non_calculable = famille('rsa_non_calculable', period)

        return (non_calculable == TypesRSANonCalculable.calculable) * montant

class TypesRSANonCalculable(Enum):
    __order__ = 'calculable tns conjoint_tns'  # Needed to preserve the enum order in Python 2
    calculable = u"Calculable"
    tns = u"tns"
    conjoint_tns = u"conjoint_tns"


class rsa_base_ressources_patrimoine_individu(Variable):
    value_type = float
    label = u"Base de ressources des revenus du patrimoine du RSA"
    entity = Individu
    definition_period = MONTH

    def formula_2009_06_01(individu, period, parameters):
        interets_epargne_sur_livrets = individu('interets_epargne_sur_livrets', period)
        epargne_non_remuneree = individu('epargne_non_remuneree', period)
        revenus_capital = individu('revenus_capital', period)
        valeur_locative_immo_non_loue = individu('valeur_locative_immo_non_loue', period)
        valeur_locative_terrains_non_loue = individu('valeur_locative_terrains_non_loue', period)
        revenus_locatifs = individu('revenus_locatifs', period)
        rsa = parameters(period).prestations.minima_sociaux.rsa

        return (
            + epargne_non_remuneree * rsa.patrimoine.taux_interet_forfaitaire_epargne_non_remunere / 12
            + interets_epargne_sur_livrets / 12
            + revenus_capital
            + revenus_locatifs
            + valeur_locative_immo_non_loue * rsa.patrimoine.abattement_valeur_locative_immo_non_loue
            + valeur_locative_terrains_non_loue * rsa.patrimoine.abattement_valeur_locative_terrains_non_loue
            )


class rsa_condition_nationalite(Variable):
    value_type = bool
    default_value = True
    entity = Individu
    label = u"Conditions de nationnalité et de titre de séjour pour bénéficier du RSA"
    definition_period = MONTH

    def formula_2009_06_01(individu, period, parameters):
        ressortissant_eee = individu('ressortissant_eee', period)
        duree_possession_titre_sejour = individu('duree_possession_titre_sejour', period)
        duree_min_titre_sejour = parameters(period).prestations.minima_sociaux.rsa.duree_min_titre_sejour
        return or_(ressortissant_eee, duree_possession_titre_sejour >= duree_min_titre_sejour)

    # RMI
    def formula(individu, period, parameters):
        ressortissant_eee = individu('ressortissant_eee', period)
        duree_possession_titre_sejour = individu('duree_possession_titre_sejour', period)
        duree_min_titre_sejour = parameters(period).prestations.minima_sociaux.rmi.duree_min_titre_sejour
        return or_(ressortissant_eee, duree_possession_titre_sejour >= duree_min_titre_sejour)


class rsa_eligibilite(Variable):
    value_type = bool
    entity = Famille
    label = u"Eligibilité au RSA et au RMI"
    definition_period = MONTH

    def formula(famille, period, parameters):
        rsa_nb_enfants = famille('rsa_nb_enfants', period)
        rsa_eligibilite_tns = famille('rsa_eligibilite_tns', period)
        condition_nationalite_i = famille.members('rsa_condition_nationalite', period)
        condition_nationalite = famille.any(condition_nationalite_i, role = Famille.PARENT)

        rmi = parameters(period).prestations.minima_sociaux.rmi
        rsa = parameters(period).prestations.minima_sociaux.rsa

        age_i = famille.members('age', period)

        etudiant_i = famille.members('etudiant', period)

        # rsa_nb_enfants est à valeur pour une famille, il faut le projeter sur les individus avant de faire une opération avec age_i
        condition_age_i = famille.project(rsa_nb_enfants > 0) + (age_i > rsa.age_pac)

        return (
            famille.any(condition_age_i * not_(etudiant_i), role = Famille.PARENT)
            * condition_nationalite
            * rsa_eligibilite_tns
            )


class rsa_eligibilite_tns(Variable):
    value_type = bool
    default_value = True
    entity = Famille
    label = u"Condition de chiffres d'affaires pour qu'un travailleur non salarié soit éligible au RSA"
    end = '2016-12-31'
    definition_period = MONTH

    def formula(famille, period, parameters):
        last_year = period.last_year

        tns_benefice_agricole_i = famille.members('tns_benefice_exploitant_agricole', last_year)
        tns_benefice_agricole = famille.sum(tns_benefice_agricole_i)

        tns_employe_i = famille.members('tns_avec_employe', period)
        tns_avec_employe = famille.any(tns_employe_i)

        tns_autres_revenus_CA_i = famille.members(
            'tns_autres_revenus_chiffre_affaires', last_year, options = [ADD])
        tns_autres_revenus_type_activite_i = famille.members('tns_autres_revenus_type_activite', period)

        has_conjoint = famille('nb_parents', period) > 1
        rsa_nb_enfants = famille('rsa_nb_enfants', period)
        P = parameters(period)
        P_agr = P.tns.exploitant_agricole
        P_micro = P.impot_revenu.rpns.micro
        maj_2p = P_agr.maj_2p
        maj_1e_2ad = P_agr.maj_1e_2ad
        maj_e_sup = P_agr.maj_e_sup

        def eligibilite_agricole(has_conjoint, rsa_nb_enfants, tns_benefice_agricole, P_agr):
            plafond_benefice_agricole = P_agr.plafond_rsa * P.cotsoc.gen.smic_h_b
            taux_avec_conjoint = (
                1 + maj_2p + maj_1e_2ad * (rsa_nb_enfants > 0) + maj_e_sup * max_(rsa_nb_enfants - 1, 0)
                )
            taux_sans_conjoint = 1 + maj_2p * (rsa_nb_enfants > 0) + maj_e_sup * max_(rsa_nb_enfants - 1, 0)
            taux_majoration = has_conjoint * taux_avec_conjoint + (1 - has_conjoint) * taux_sans_conjoint
            plafond_benefice_agricole_majore = taux_majoration * plafond_benefice_agricole

            return tns_benefice_agricole < plafond_benefice_agricole_majore

        def eligibilite_chiffre_affaire(ca, type_activite, P_micro):
            plaf_vente = P_micro.specialbnc.marchandises.max
            plaf_service = P_micro.specialbnc.services.max

            achat_revente = (type_activite == TypesTnsTypeActivite.achat_revente)


            service = (
                (type_activite == TypesTnsTypeActivite.bic)
                + (type_activite == TypesTnsTypeActivite.bnc)
            )

            return (achat_revente * (ca <= plaf_vente)) + (service * (ca <= plaf_service))

        eligibilite_agricole = eligibilite_agricole(
            has_conjoint, rsa_nb_enfants, tns_benefice_agricole, P_agr
            )
        eligibilite_chiffre_affaire = famille.all(
            eligibilite_chiffre_affaire(tns_autres_revenus_CA_i, tns_autres_revenus_type_activite_i, P_micro),
            role = Famille.PARENT
            )


        return eligibilite_agricole * not_(tns_avec_employe) * eligibilite_chiffre_affaire


class rsa_forfait_asf(Variable):
    value_type = float
    entity = Famille
    label = u"Allocation de soutien familial forfaitisée pour le RSA"
    definition_period = MONTH

    def formula_2014_04_01(famille, period, parameters):
        # Si un ASF est versé, on ne prend pas en compte le montant réel mais un forfait.
        prestations_familiales = parameters(period).prestations.prestations_familiales
        minima_sociaux = parameters(period).prestations.minima_sociaux

        asf_verse = famille('asf', period)
        montant_verse_par_enfant = prestations_familiales.af.bmaf * prestations_familiales.asf.taux_1_parent
        montant_retenu_rsa_par_enfant = prestations_familiales.af.bmaf * minima_sociaux.rmi.forfait_asf.taux1

        asf_retenue = asf_verse * (montant_retenu_rsa_par_enfant / montant_verse_par_enfant)

        return asf_retenue


class rsa_forfait_logement(Variable):
    value_type = float
    entity = Famille
    label = u"Forfait logement intervenant dans le calcul du Rmi ou du Rsa"
    definition_period = MONTH

    def formula(famille, period, parameters):
        np_pers = famille('nb_parents', period) + famille('rsa_nb_enfants', period)
        aide_logement = famille('aide_logement', period)
        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        participation_frais = famille.demandeur.menage('participation_frais', period)
        loyer = famille.demandeur.menage('loyer', period)

        avantage_nature = or_(
            (statut_occupation_logement == TypesStatutOccupationLogement.proprietaire) * not_(loyer),
            (statut_occupation_logement == TypesStatutOccupationLogement.loge_gratuitement) * not_(participation_frais)
            )
        avantage_al = aide_logement > 0


        # Les parametres ont changé de nom au moment où le RMI est devenu le RSA
        # Pour le RSA, on utilise les taux des textes de lois, pour le RMI ils sont déjà aggrégés
        # Il faudrait uniformiser, mais les taux légaux pour le RMI commencent par "1", et ne passent pas en python
        if period.start.date >= date(2009, 6, 01):
            params = parameters(period).prestations.minima_sociaux.rsa
            montant_base = params.montant_de_base_du_rsa
            taux_2p = 1 + params.majoration_rsa.taux_deuxieme_personne
            taux_3p = taux_2p + params.majoration_rsa.taux_troisieme_personne
            forf_logement_taux_1p = params.forfait_logement.taux_1_personne
            forf_logement_taux_2p = params.forfait_logement.taux_2_personnes * taux_2p
            forf_logement_taux_3p = params.forfait_logement.taux_3_personnes_ou_plus * taux_3p
        else:
            params = parameters(period).prestations.minima_sociaux.rmi
            montant_base = params.rmi
            forf_logement_taux_1p = params.forfait_logement.taux1
            forf_logement_taux_2p = params.forfait_logement.taux2
            forf_logement_taux_3p = params.forfait_logement.taux3

        montant_forfait = montant_base * (
            (np_pers == 1) * forf_logement_taux_1p +
            (np_pers == 2) * forf_logement_taux_2p +
            (np_pers >= 3) * forf_logement_taux_3p
            )

        montant_al = avantage_al * min_(aide_logement, montant_forfait)
        montant_nature = avantage_nature * montant_forfait

        return max_(montant_al, montant_nature)


class rsa_isolement_recent(Variable):
    value_type = bool
    entity = Famille
    label = u"Situation d'isolement depuis moins de 18 mois"
    base_function = requested_period_last_or_next_value
    definition_period = MONTH


class rsa_majore_eligibilite(Variable):
    value_type = bool
    entity = Famille
    label = u"Eligibilité au RSA majoré pour parent isolé"
    definition_period = MONTH

    def formula(famille, period):
        isole = not_(famille('en_couple', period))
        isolement_recent = famille('rsa_isolement_recent', period)
        enfant_moins_3_ans = nb_enf(famille, period, 0, 2) > 0
        enceinte_fam = famille('enceinte_fam', period)
        nbenf = famille('rsa_nb_enfants', period)
        rsa_eligibilite_tns = famille('rsa_eligibilite_tns', period)
        eligib = (
            isole *
            (enceinte_fam | (nbenf > 0)) *
            (enfant_moins_3_ans | isolement_recent | enceinte_fam) *
            rsa_eligibilite_tns
            )

        return eligib


class rsa_non_calculable(Variable):
    value_type = Enum
    possible_values = TypesRSANonCalculable
    default_value = TypesRSANonCalculable.calculable
    entity = Famille
    label = u"RSA non calculable"
    end = '2016-12-31'
    definition_period = MONTH

    def formula(famille, period):
        # Si le montant du RSA est nul sans tenir compte des revenus
        # TNS pouvant provoquer une non calculabilité (parce que
        # les autres revenus sont trop importants), alors a fortiori
        # la famille ne sera pas éligible au RSA en tenant compte de
        # ces ressources. Il n'y a donc pas non calculabilité.
        eligible_rsa = famille('rsa_montant', period) > 0

        non_calculable_tns_parent1 = famille.demandeur('rsa_non_calculable_tns_individu', period)
        non_calculable_tns_parent2 = famille.conjoint('rsa_non_calculable_tns_individu', period)

        non_calculable = select(
            [non_calculable_tns_parent1, non_calculable_tns_parent2],
            [1, 2]
            )
        non_calculable = eligible_rsa * non_calculable

        return select(
            [non_calculable == 0, non_calculable == 1, non_calculable == 2],
            [TypesRSANonCalculable.calculable, TypesRSANonCalculable.tns, TypesRSANonCalculable.conjoint_tns]
        )


class rsa_non_calculable_tns_individu(Variable):
    value_type = bool
    entity = Individu
    label = u"RSA non calculable du fait de la situation de l'individu. Dans le cas des TNS, l'utilisateur est renvoyé vers son PCG"
    definition_period = MONTH

    # En fait l'évaluation par le PCD est plutôt l'exception que la règle. En général on retient plutôt le bénéfice déclaré au FISC (après abattement forfaitaire ou réel).

    def formula(individu, period):
        this_year_and_last_year = period.start.offset('first-of', 'year').period('year', 2).offset(-1)
        tns_benefice_exploitant_agricole = individu(
            'tns_benefice_exploitant_agricole', this_year_and_last_year, options = [ADD])
        tns_micro_entreprise_chiffre_affaires = individu(
            'tns_micro_entreprise_chiffre_affaires', this_year_and_last_year, options = [ADD])
        tns_autres_revenus = individu('tns_autres_revenus', this_year_and_last_year, options = [ADD])

        return (
            (tns_benefice_exploitant_agricole > 0) +
            (tns_micro_entreprise_chiffre_affaires > 0) +
            (tns_autres_revenus > 0)
            )


class rsa_socle(Variable):
    value_type = float
    entity = Famille
    label = "RSA socle"
    definition_period = MONTH

    def formula_2009_06_01(famille, period, parameters):
        nb_parents = famille('nb_parents', period)
        eligib = famille('rsa_eligibilite', period)
        rsa_nb_enfants = famille('rsa_nb_enfants', period)
        nb_personnes = nb_parents + rsa_nb_enfants

        rsa = parameters(period).prestations.minima_sociaux.rsa
        taux = (
            1 +
            (nb_personnes >= 2) * rsa.majoration_rsa.taux_deuxieme_personne +
            (nb_personnes >= 3) * rsa.majoration_rsa.taux_troisieme_personne +
            (nb_personnes >= 4) * where(
                nb_parents == 1,
                rsa.majoration_rsa.taux_personne_supp, rsa.majoration_rsa.taux_troisieme_personne
                ) +  # Si nb_parents == 1, pas de conjoint, la 4e personne est un enfant, donc le taux est de 40%.
            max_(nb_personnes - 4, 0) * rsa.majoration_rsa.taux_personne_supp
            )
        socle = rsa.montant_de_base_du_rsa

        return eligib * socle * taux

    # RMI
    def formula(famille, period, parameters):
        nb_parents = famille('nb_parents', period)
        eligib = famille('rsa_eligibilite', period)
        rsa_nb_enfants = famille('rsa_nb_enfants', period)
        nb_personnes = nb_parents + rsa_nb_enfants

        rmi = parameters(period).prestations.minima_sociaux.rmi
        taux = (
            1 +
            (nb_personnes >= 2) * rmi.txp2 +
            (nb_personnes >= 3) * rmi.txp3 +
            (nb_personnes >= 4) * where(nb_parents == 1, rmi.txps, rmi.txp3) +
            # Si nb_parents == 1, pas de conjoint, la 4e personne est un enfant, donc le taux est de 40%.
            max_(nb_personnes - 4, 0) * rmi.txps
            )
        socle = rmi.rmi

        return eligib * socle * taux


class rsa_socle_majore(Variable):
    value_type = float
    entity = Famille
    label = u"Montant majoré pour parent isolé du Revenu de solidarité active socle"
    definition_period = MONTH

    def formula_2009_06_01(famille, period, parameters):
        eligib = famille('rsa_majore_eligibilite', period)
        nbenf = famille('rsa_nb_enfants', period)

        rsa = parameters(period).prestations.minima_sociaux.rsa
        taux = rsa.majo_rsa.pac0 + rsa.majo_rsa.pac_enf_sup * nbenf
        socle = rsa.montant_de_base_du_rsa

        return eligib * socle * taux
