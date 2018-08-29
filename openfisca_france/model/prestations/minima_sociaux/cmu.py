# -*- coding: utf-8 -*-

from __future__ import division

from numpy import absolute as abs_, logical_or as or_

from openfisca_france.model.base import *  # noqa analysis:ignore

class cmu_acs_eligibilite(Variable):
    value_type = bool
    entity = Famille
    label = u"Pré-éligibilité à la CMU, avant prise en compte des ressources"
    definition_period = MONTH

    def formula(famille, period, parameters):
        previous_year = period.start.period('year').offset(-1)
        this_year = period.this_year
        age_min = parameters(period).cmu.age_limite_pac
        nb_enfants = famille('cmu_nb_pac', period)

        # Une personne de 25 ans ne doit pas être à charge fiscale, ni hébergée par ses parents, ni recevoir de pensions alimentaires pour pouvoir bénéficier de la CMU individuellement.
        a_charge_des_parents = famille.members('enfant_a_charge', this_year)
        habite_chez_parents = famille.members('habite_chez_parents', period)
        recoit_pension = famille.members('pensions_alimentaires_percues', previous_year, options = [ADD]) > 0
        condition_independance = not_(a_charge_des_parents + habite_chez_parents + recoit_pension)

        age = famille.members('age', period)
        condition_age = (age >= age_min)


        eligibilite_famille = (
            (nb_enfants > 0)
            + famille.any(condition_age)
            + famille.all(condition_independance)
            )

        return eligibilite_famille


class acs_montant_i(Variable):
    value_type = float
    entity = Individu
    label = u"Montant de l'ACS attribué pour une personne en cas d'éligibilité de la famille"
    definition_period = MONTH

    def formula_2009_08_01(individu, period, parameters):
        P = parameters(period).cmu
        age = individu('age', period)
        montant_si_pac = select(
            [(age <= 15) * (age >= 0), age <= 25],
            [P.acs_moins_16_ans, P.acs_16_49_ans]
            )
        montant_si_parent = select(
            [age <=15, age <= 49, age <= 59, age >= 60],
            [P.acs_moins_16_ans, P.acs_16_49_ans, P.acs_50_59_ans, P.acs_plus_60_ans],
            )
        return where(
            individu.has_role(Famille.PARENT),
            montant_si_parent,
            montant_si_pac
            )


class acs_montant(Variable):
    value_type = float
    entity = Famille
    label = u"Montant de l'ACS en cas d'éligibilité"
    definition_period = MONTH

    def formula_2009_08_01(famille, period, parameters):
        acs_montant_i = famille.members('acs_montant_i', period)
        return famille.sum(acs_montant_i)


class cmu_forfait_logement_base(Variable):
    value_type = float
    entity = Famille
    label = u"Forfait logement applicable en cas de propriété ou d'occupation à titre gratuit"
    definition_period = MONTH

    def formula(famille, period, parameters):
        cmu_nbp_foyer = famille('cmu_nbp_foyer', period)
        P = parameters(period).cmu.forfait_logement
        law_rsa = parameters(period).prestations.minima_sociaux.rmi

        return forfait_logement(cmu_nbp_foyer, P, law_rsa)


class cmu_forfait_logement_al(Variable):
    value_type = float
    entity = Famille
    label = u"Forfait logement applicable en cas d'aide au logement"
    definition_period = MONTH

    def formula(famille, period, parameters):
        nb_personnes_foyer = famille('cmu_nbp_foyer', period)
        aide_logement = famille('aide_logement', period)
        P = parameters(period).cmu.forfait_logement_al
        law_rsa = parameters(period).prestations.minima_sociaux.rmi

        return (aide_logement > 0) * min_(12 * aide_logement, forfait_logement(nb_personnes_foyer, P, law_rsa))


class cmu_nbp_foyer(Variable):
    value_type = int
    is_period_size_independent = True
    entity = Famille
    label = u"Nombre de personnes dans le foyer CMU"
    definition_period = MONTH

    def formula(famille, period, parameters):
        nb_parents = famille('nb_parents', period)
        cmu_nb_pac = famille('cmu_nb_pac', period)

        return nb_parents + cmu_nb_pac


class cmu_eligible_majoration_dom(Variable):
    value_type = bool
    entity = Famille
    definition_period = MONTH

    def formula(famille, period):
        menage = famille.demandeur.menage
        residence_guadeloupe = menage('residence_guadeloupe', period)
        residence_martinique = menage('residence_martinique', period)
        residence_guyane = menage('residence_guyane', period)
        residence_reunion = menage('residence_reunion', period)

        return residence_guadeloupe | residence_martinique | residence_guyane | residence_reunion


class cmu_c_plafond(Variable):
    value_type = float
    entity = Famille
    label = u"Plafond annuel de ressources pour l'éligibilité à la CMU-C"
    definition_period = MONTH
    reference = u"https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006753234"

    def formula(famille, period, parameters):
        """
        - Le plafond dépends du nombre de personnes dans le foyer.
        - À un plafond de base pour une personne, on applique pour chaque personne supplémentaire un certain coefficient supplémentaire
                - Un coefficient pour la 2eme personne,
                - Un coefficient pour les 3e et 4e personne,
                - Un coefficient pour toute personne supplémentaire
        - Si un enfant est en garde alternée, on ne prend en compte que la moitié de son coefficient.
        - Pour savoir quel coefficient est attribué à chaque enfant, il faut trier les enfants de chaque famille par age.
        """

        cmu = parameters(period).cmu
        age_i = famille.members('age_en_mois', period)
        is_couple = (famille('nb_parents', period) == 2)
        is_enfant = famille.members.has_role(Famille.ENFANT)
        cmu_eligible_majoration_dom = famille('cmu_eligible_majoration_dom', period)
        coeff_garde_alt_i = where(famille.members('garde_alternee', period), 0.5, 1)

        rang_dans_fratrie = famille.members.get_rank(famille, - age_i, condition = is_enfant)  # 0 pour l'aîné, 1 pour le cadet, etc.

        # Famille monoparentale

        coeff_enfant_i = select(
            [rang_dans_fratrie == 0, rang_dans_fratrie <= 2, rang_dans_fratrie >= 3],
            [cmu.coeff_p2, cmu.coeff_p3_p4, cmu.coeff_p5_plus]
            ) * coeff_garde_alt_i

        coeff_monoparental = 1 + famille.sum(coeff_enfant_i, role = famille.ENFANT)


        # Couple

        coeff_enfant_i = select(
            [rang_dans_fratrie <= 1, rang_dans_fratrie >= 2],
            [cmu.coeff_p3_p4, cmu.coeff_p5_plus]
            ) * coeff_garde_alt_i

        coeff_couple = 1 + cmu.coeff_p2 + famille.sum(coeff_enfant_i, role = famille.ENFANT)

        coefficient_famille = where(is_couple, coeff_couple, coeff_monoparental)
        coefficient_dom = 1 + cmu_eligible_majoration_dom * cmu.majoration_dom

        plafonds = (
            cmu.plafond_base
            *  coefficient_dom
            *  coefficient_famille
            )

        return round_(plafonds)


class acs_plafond(Variable):
    value_type = float
    entity = Famille
    label = u"Plafond annuel de ressources pour l'éligibilité à l'ACS"
    definition_period = MONTH

    def formula(famille, period, parameters):
        cmu_c_plafond = famille('cmu_c_plafond', period)
        P = parameters(period).cmu

        return cmu_c_plafond * (1 + P.majoration_plafond_acs)


class cmu_base_ressources_individu(Variable):
    value_type = float
    label = u"Base de ressources de l'individu prise en compte pour l'éligibilité à la CMU-C / ACS"
    reference = [
        u"Article R861-8 du code de la Sécurité Sociale",
        u"https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=DEA53FDC793298CE041862E42D999E84.tplgfr43s_1?idArticle=LEGIARTI000034424885&cidTexte=LEGITEXT000006073189&dateTexte=20180829&categorieLien=id&oldAction=",
        u"Article R861-10 du code de la Sécurité Sociale pour les ressources exclues",
        u"https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=DEA53FDC793298CE041862E42D999E84.tplgfr43s_1?idArticle=LEGIARTI000030055485&cidTexte=LEGITEXT000006073189&dateTexte=20180829&categorieLien=id&oldAction=&nbResultRech=",
        u"Circulaire N°DSS/2A/2002/110 du 22 février 2002 relative à la notion de ressources à prendre en compte pour l'appréciation du droit à la protection complémentaire en matière de santé",
        u"http://circulaire.legifrance.gouv.fr/pdf/2009/04/cir_6430.pdf"
    ]
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        # Rolling year
        previous_year = period.start.period('year').offset(-1)
        # N-1
        last_month = period.last_month

        P = parameters(period).cmu

        ressources_a_inclure = [
            'aah',
            'allocation_securisation_professionnelle',
            'bourse_enseignement_sup',
            'bourse_recherche',
            'caah',
            'chomage_net',
            'dedommagement_victime_amiante',
            'gains_exceptionnels',
            'indemnites_chomage_partiel',
            'indemnites_journalieres',
            'indemnites_stage',
            'indemnites_compensatrices_conges_payes',
            'pensions_alimentaires_percues',
            'pensions_invalidite',
            'prestation_compensatoire',
            'prime_forfaitaire_mensuelle_reprise_activite',
            'retraite_combattant',
            'retraite_nette',
            'revenus_stage_formation_pro',
            'rsa_base_ressources_patrimoine_individu',
            'salaire_net',
            'rente_accident_travail',
        ]

        ressources = sum([
            individu(ressource, previous_year, options = [ADD])
            for ressource in ressources_a_inclure
            ])

        pensions_alim_versees = abs_(individu(
            'pensions_alimentaires_versees_individu',
            previous_year, options = [ADD])
        )

        revenus_stage_formation_pro_last_month = individu('revenus_stage_formation_pro', last_month)

        # Abattement sur revenus d'activité si :
        # - IJ maladie
        # - chômage
        # - ass
        # - formation professionnelle
        def abbattement_chomage():
            indemnites_journalieres_maladie = individu('indemnites_journalieres_maladie', period)

            chomage = individu('activite', period) == TypesActivite.chomeur
            indemnites_chomage_partiel = individu('indemnites_chomage_partiel', period)
            chomage_net = individu('chomage_net', period)
            allocation_aide_retour_emploi = individu('allocation_aide_retour_emploi', period)

            ass = individu.famille('ass', period)

            revenus_stage_formation_pro = individu('revenus_stage_formation_pro', period)

            condition_ij_maladie = indemnites_journalieres_maladie > 0
            condition_chomage = chomage * ((indemnites_chomage_partiel + chomage_net + allocation_aide_retour_emploi) > 0)
            condition_ass = ass > 0
            condition_revenus_formation_pro = revenus_stage_formation_pro > 0

            eligibilite_abattement_chomage = or_(condition_ij_maladie, or_(condition_chomage, or_(condition_ass, condition_revenus_formation_pro)))

            salaire_net = individu('salaire_net', previous_year, options=[ADD])

            return eligibilite_abattement_chomage * salaire_net * P.abattement_chomage

        # Revenus de stage de formation professionnelle exclus si plus perçus depuis 1 mois
        def neutralisation_stage_formation_pro():
            revenus_stage_formation_pro_annee = individu('revenus_stage_formation_pro', previous_year, options = [ADD])
            return (revenus_stage_formation_pro_last_month == 0) * revenus_stage_formation_pro_annee

        def revenus_tns():
            last_year = period.last_year

            revenus_auto_entrepreneur = individu('tns_auto_entrepreneur_benefice', previous_year, options = [ADD])

            # Les revenus TNS hors AE sont estimés en se basant sur N-1
            tns_micro_entreprise_benefice = individu('tns_micro_entreprise_benefice', last_year)
            tns_benefice_exploitant_agricole = individu('tns_benefice_exploitant_agricole', last_year)
            tns_autres_revenus = individu('tns_autres_revenus', last_year)

            return revenus_auto_entrepreneur + tns_micro_entreprise_benefice + tns_benefice_exploitant_agricole + tns_autres_revenus

        return ressources + revenus_tns() - pensions_alim_versees - abbattement_chomage() - neutralisation_stage_formation_pro()

class cmu_base_ressources(Variable):
    value_type = float
    label = u"Base de ressources prise en compte pour l'éligibilité à la CMU-C / ACS"
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        previous_year = period.start.period('year').offset(-1)

        ressources_a_inclure = [
            'af',
            'asf',
            'asi',
            'aspa',
            'ass',
            'cf',
            'paje_clca',
            'paje_prepare',
        ]

        ressources_famille = sum(
            [famille(ressource, previous_year, options = [ADD]) for ressource in ressources_a_inclure]
            )

        statut_occupation_logement = famille.demandeur.menage('statut_occupation_logement', period)
        cmu_forfait_logement_base = famille('cmu_forfait_logement_base', period)
        cmu_forfait_logement_al = famille('cmu_forfait_logement_al', period)

        P = parameters(period).cmu

        proprietaire = (statut_occupation_logement == TypesStatutOccupationLogement.proprietaire)
        heberge_titre_gratuit = (statut_occupation_logement == TypesStatutOccupationLogement.loge_gratuitement)
        forfait_logement = ((proprietaire + heberge_titre_gratuit) * cmu_forfait_logement_base +
            cmu_forfait_logement_al)

        ressources_individuelles = famille.members('cmu_base_ressources_individu', period)
        ressources_parents = famille.sum(ressources_individuelles, role = Famille.PARENT)

        age = famille.members('age', period)
        condition_enfant_a_charge = (age >= 0) * (age <= P.age_limite_pac)
        ressources_enfants = famille.sum(ressources_individuelles * condition_enfant_a_charge, role = Famille.ENFANT)

        return forfait_logement + ressources_famille + ressources_parents + ressources_enfants


class cmu_nb_pac(Variable):
    value_type = int
    is_period_size_independent = True
    entity = Famille
    label = u"Nombre de personnes à charge au titre de la CMU"
    definition_period = MONTH

    def formula(famille, period, parameters):
        P = parameters(period).cmu
        age = famille.members('age', period)
        return famille.sum((age >= 0) * (age <= P.age_limite_pac), role = Famille.ENFANT)


class cmu_c(Variable):
    value_type = bool
    label = u"Éligibilité à la CMU-C"
    entity = Famille
    definition_period = MONTH

    def formula(famille, period):
        cmu_c_plafond = famille('cmu_c_plafond', period)
        cmu_base_ressources = famille('cmu_base_ressources', period)
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)
        cmu_acs_eligibilite = famille('cmu_acs_eligibilite', period)

        if period.start.date >= date(2016, 1, 1):
            eligibilite_rsa = famille('rsa', period) > 0
        else:
            # Avant 2016, seules les bénéficiaires du RSA socle avait le droit d'office à la CMU.
            rsa_socle = famille('rsa_socle', period)
            rsa_socle_majore = famille('rsa_socle_majore', period)
            rsa_forfait_logement = famille('rsa_forfait_logement', period)
            rsa_base_ressources = famille('rsa_base_ressources', period)
            socle = max_(rsa_socle, rsa_socle_majore)
            rsa = famille('rsa', period)
            eligibilite_rsa = (rsa > 0) * (rsa_base_ressources < socle - rsa_forfait_logement)

        eligibilite_basique = cmu_base_ressources <= cmu_c_plafond

        return cmu_acs_eligibilite * not_(residence_mayotte) * or_(eligibilite_basique, eligibilite_rsa)


class acs(Variable):
    value_type = float
    label = u"Montant (annuel) de l'ACS"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        cmu_c = famille('cmu_c', period)
        cmu_base_ressources = famille('cmu_base_ressources', period)
        acs_plafond = famille('acs_plafond', period)
        acs_montant = famille('acs_montant', period)
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)
        cmu_acs_eligibilite = famille('cmu_acs_eligibilite', period)

        return (
            cmu_acs_eligibilite *
            not_(residence_mayotte) * not_(cmu_c) *
            (cmu_base_ressources <= acs_plafond) *
            acs_montant)


############################################################################
# Helper functions
############################################################################


def forfait_logement(nbp_foyer, P, law_rsa):
    '''
    Calcule le forfait logement en fonction du nombre de personnes dans le "foyer CMU" et d'un jeu de taux
    '''
    montant_rsa_socle = law_rsa.rmi * (1 +
        law_rsa.txp2 * (nbp_foyer >= 2) +
        law_rsa.txp3 * (nbp_foyer >= 3)
        )

    return 12 * montant_rsa_socle * select(
            [nbp_foyer == 1, nbp_foyer == 2, nbp_foyer > 2],
            [P.taux_1p, P.taux_2p, P.taux_3p_plus]
            )

