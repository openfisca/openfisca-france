# -*- coding: utf-8 -*-

from __future__ import division

from numpy import abs as abs_, logical_or as or_

from openfisca_france.model.base import *  # noqa analysis:ignore


class inapte_travail(Variable):
    value_type = bool
    entity = Individu
    label = u"Reconnu inapte au travail"
    definition_period = MONTH

class taux_incapacite(Variable):
    value_type = float
    entity = Individu
    label = u"Taux d'incapacité"
    definition_period = MONTH


# Cette formule se base sur les revenus imposables annuels. Est-ce vraiment le cas pour l'ASI et l'ASPA ?
class revenus_fonciers_minima_sociaux(Variable):
    value_type = float
    entity = Individu
    label = u"Revenus fonciers pour la base ressource du rmi/rsa"
    definition_period = MONTH

    def formula(individu, period):
        period_declaration = period.this_year
        f4ba = individu.foyer_fiscal('f4ba', period_declaration)
        f4be = individu.foyer_fiscal('f4be', period_declaration)


        # On projette les revenus du foyer fiscal seulement sur le déclarant principal
        return (f4ba + f4be) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL) / 12


class asi_aspa_base_ressources_individu(Variable):
    value_type = float
    label = u"Base ressources individuelle du minimum vieillesse/ASPA"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        last_year = period.last_year
        three_previous_months = period.last_3_months
        law = parameters(period)
        leg_1er_janvier = parameters(period.start.offset('first-of', 'year'))

        ressources_incluses = [
            'allocation_securisation_professionnelle',
            'chomage_net',
            'dedommagement_victime_amiante',
            'div_ms',
            'gains_exceptionnels',
            'indemnites_chomage_partiel',
            'indemnites_journalieres',
            'indemnites_volontariat',
            'pensions_alimentaires_percues',
            'pensions_invalidite',
            'prestation_compensatoire',
            'prime_forfaitaire_mensuelle_reprise_activite',
            'retraite_brute',
            'revenus_stage_formation_pro',
            'rsa_base_ressources_patrimoine_individu',
            'salaire_de_base',
            ]

        # Revenus du foyer fiscal que l'on projette sur le premier invidividus
        revenus_capitaux_prelevement_bareme_foyer_fiscal = max_(0, individu.foyer_fiscal('revenus_capitaux_prelevement_bareme', three_previous_months, options = [ADD]))
        revenus_capitaux_prelevement_liberatoire_foyer_fiscal = max_(0, individu.foyer_fiscal('revenus_capitaux_prelevement_liberatoire', three_previous_months, options = [ADD]))
        rente_viagere_titre_onereux_foyer_fiscal = individu.foyer_fiscal('rente_viagere_titre_onereux', three_previous_months, options = [ADD])
        revenus_foyer_fiscal = revenus_capitaux_prelevement_bareme_foyer_fiscal + revenus_capitaux_prelevement_liberatoire_foyer_fiscal + rente_viagere_titre_onereux_foyer_fiscal
        revenus_foyer_fiscal_individu = revenus_foyer_fiscal * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)

        def revenus_tns():
            revenus_auto_entrepreneur = individu('tns_auto_entrepreneur_benefice', three_previous_months, options = [ADD])
            # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1

            tns_micro_entreprise_benefice = individu('tns_micro_entreprise_benefice', last_year) * (3 / 12)
            tns_benefice_exploitant_agricole = individu('tns_benefice_exploitant_agricole', last_year) * (3 / 12)
            tns_autres_revenus = individu('tns_autres_revenus', last_year) * (3 / 12)

            return (
                revenus_auto_entrepreneur + tns_micro_entreprise_benefice + tns_benefice_exploitant_agricole +
                tns_autres_revenus
                )

        pension_invalidite = (individu('pensions_invalidite', period) > 0)
        aspa_eligibilite = individu('aspa_eligibilite', period)
        asi_eligibilite = individu('asi_eligibilite', period)

        # Inclus l'AAH si conjoint non éligible ASPA, retraite et pension invalidité
        aah = individu('aah', three_previous_months, options = [ADD])
        aah = aah * not_(aspa_eligibilite) * not_(asi_eligibilite) * not_(pension_invalidite)

        pensions_alimentaires_versees = individu(
            'pensions_alimentaires_versees_individu', three_previous_months, options = [ADD]
            )

        def abattement_salaire():
            aspa_couple = individu.famille('aspa_couple', period)

            # Abattement sur les salaires (appliqué sur une base trimestrielle)
            abattement_forfaitaire_base = (
                leg_1er_janvier.cotsoc.gen.smic_h_b * law.cotsoc.gen.nb_heure_travail_mensuel
                )

            taux_abattement_forfaitaire = where(
                aspa_couple,
                law.prestations.minima_sociaux.aspa.abattement_forfaitaire_tx_couple,
                law.prestations.minima_sociaux.aspa.abattement_forfaitaire_tx_seul
                )

            abattement_forfaitaire = abattement_forfaitaire_base * taux_abattement_forfaitaire
            salaire_de_base = individu('salaire_de_base', three_previous_months, options = [ADD])

            return min_(salaire_de_base, abattement_forfaitaire)

        base_ressources_3_mois = sum(
            max_(0, individu(ressource_type, three_previous_months, options = [ADD]))
            for ressource_type in ressources_incluses
            ) + aah + revenus_foyer_fiscal_individu + revenus_tns() - abs_(pensions_alimentaires_versees) - abattement_salaire()

        return base_ressources_3_mois / 3


class asi_aspa_base_ressources(Variable):
    value_type = float
    label = u"Base ressource du minimum vieillesse et assimilés (ASPA)"
    entity = Famille
    definition_period = MONTH

    def formula(famille, period):
        base_ressources_i = famille.members('asi_aspa_base_ressources_individu', period)
        ass = famille('ass', period)

        return ass + famille.sum(base_ressources_i, role = Famille.PARENT)


class aspa_eligibilite(Variable):
    value_type = bool
    label = u"Indicatrice individuelle d'éligibilité à l'allocation de solidarité aux personnes agées"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        age = individu('age', period)
        inapte_travail = individu('inapte_travail', period)
        taux_incapacite = individu('taux_incapacite', period)
        P = parameters(period).prestations.minima_sociaux
        condition_invalidite = (taux_incapacite > P.aspa.taux_incapacite_aspa_anticipe) + inapte_travail
        condition_age_base = (age >= P.aspa.age_min)
        condition_age_anticipe = (age >= P.aah.age_legal_retraite) * condition_invalidite
        condition_age = condition_age_base + condition_age_anticipe
        condition_nationalite = individu('asi_aspa_condition_nationalite', period)

        return condition_age * condition_nationalite


class asi_eligibilite(Variable):
    value_type = bool
    label = u"Indicatrice individuelle d'éligibilité à l'allocation supplémentaire d'invalidité"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        last_month = period.start.period('month').offset(-1)

        non_eligible_aspa = not_(individu('aspa_eligibilite', period))
        touche_pension_invalidite = individu('pensions_invalidite', period) > 0
        handicap = individu('handicap', period)
        touche_retraite = individu('retraite_nette', last_month) > 0
        condition_nationalite = individu('asi_aspa_condition_nationalite', period)

        eligible = (
            non_eligible_aspa *
            condition_nationalite *
            (handicap * touche_retraite + touche_pension_invalidite)
            )

        return eligible


class asi_aspa_condition_nationalite(Variable):
    value_type = bool
    default_value = True
    label = u"Condition de nationnalité et de titre de séjour pour bénéficier de l'ASPA ou l'ASI"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        ressortissant_eee = individu('ressortissant_eee', period)
        duree_possession_titre_sejour = individu('duree_possession_titre_sejour', period)
        duree_min_titre_sejour = parameters(period).prestations.minima_sociaux.aspa.duree_min_titre_sejour

        return or_(ressortissant_eee, duree_possession_titre_sejour >= duree_min_titre_sejour)


class asi_aspa_nb_alloc(Variable):
    value_type = int
    label = u"Nombre d'allocataires ASI/ASPA"
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        aspa_elig_i = famille.members('aspa_eligibilite', period)
        asi_elig_i = famille.members('asi_eligibilite', period)

        nb_allocataire_asi = famille.sum(asi_elig_i, role = Famille.PARENT)
        nb_allocataire_aspa = famille.sum(aspa_elig_i, role = Famille.PARENT)

        return nb_allocataire_asi + nb_allocataire_aspa


class asi(Variable):
    calculate_output = calculate_output_add
    value_type = float
    label = u"Allocation supplémentaire d'invalidité"
    reference = u"http://vosdroits.service-public.fr/particuliers/F16940.xhtml"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2007(famille, period, parameters):
        maries = famille('maries', period)
        en_couple = famille('en_couple', period)
        asi_aspa_nb_alloc = famille('asi_aspa_nb_alloc', period)
        base_ressources = famille('asi_aspa_base_ressources', period)
        P = parameters(period).prestations.minima_sociaux

        demandeur_eligible_asi = famille.demandeur('asi_eligibilite', period)
        demandeur_eligible_aspa = famille.demandeur('aspa_eligibilite', period)
        conjoint_eligible_asi = famille.conjoint('asi_eligibilite', period)
        conjoint_eligible_aspa = famille.conjoint('aspa_eligibilite', period)

        # Un seul éligible
        elig1 = ((asi_aspa_nb_alloc == 1) & (demandeur_eligible_asi | conjoint_eligible_asi))
        # Couple d'éligibles mariés
        elig2 = demandeur_eligible_asi & conjoint_eligible_asi & maries
        # Couple d'éligibles non mariés
        elig3 = demandeur_eligible_asi & conjoint_eligible_asi & not_(maries)
        # Un seul éligible et époux éligible ASPA
        elig4 = ((demandeur_eligible_asi & conjoint_eligible_aspa) | (conjoint_eligible_asi & demandeur_eligible_aspa)) & maries
        # Un seul éligible et conjoint non marié éligible ASPA
        elig5 = ((demandeur_eligible_asi & conjoint_eligible_aspa) | (conjoint_eligible_asi & demandeur_eligible_aspa)) & not_(maries)

        elig = elig1 | elig2 | elig3 | elig4 | elig5

        montant_max = (elig1 * P.asi.montant_seul +
            elig2 * P.asi.montant_couple +
            elig3 * 2 * P.asi.montant_seul +
            elig4 * (P.asi.montant_couple / 2 + P.aspa.montant_annuel_couple / 2) +
            elig5 * (P.asi.montant_seul + P.aspa.montant_annuel_couple / 2)) / 12

        ressources = base_ressources + montant_max

        plafond_ressources = (elig1 * (P.asi.plafond_ressource_seul * not_(en_couple) + P.asi.plafond_ressource_couple * en_couple) +
            elig2 * P.asi.plafond_ressource_couple +
            elig3 * P.asi.plafond_ressource_couple +
            elig4 * P.aspa.plafond_ressources_couple +
            elig5 * P.aspa.plafond_ressources_couple) / 12

        depassement = max_(ressources - plafond_ressources, 0)

        diff = ((elig1 | elig2 | elig3) * (montant_max - depassement) +
            elig4 * (P.asi.montant_couple / 12 / 2 - depassement / 2) +
            elig5 * (P.asi.montant_seul / 12 - depassement / 2))

        # Montant mensuel servi (sous réserve d'éligibilité)
        montant_servi_asi = max_(diff, 0)

        # TODO: Faute de mieux, on verse l'asi à la famille plutôt qu'aux individus
        # asi[CHEF] = demandeur_eligible_asi*montant_servi_asi*(elig1*1 + elig2/2 + elig3/2)
        # asi[PART] = conjoint_eligible_asi*montant_servi_asi*(elig1*1 + elig2/2 + elig3/2)
        return elig * montant_servi_asi


class aspa_couple(Variable):
    value_type = bool
    label = u"Couple au sens de l'ASPA"
    entity = Famille
    definition_period = MONTH

    def formula_2002_01_01(famille, period):
        maries = famille('maries', period)

        return maries

    def formula_2007_01_01(famille, period):
        en_couple = famille('en_couple', period)

        return en_couple


class aspa(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = u"Allocation de solidarité aux personnes agées"
    reference = "http://vosdroits.service-public.fr/particuliers/F16871.xhtml"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        maries = famille('maries', period)
        en_couple = famille('en_couple', period)
        asi_aspa_nb_alloc = famille('asi_aspa_nb_alloc', period)
        base_ressources = famille('asi_aspa_base_ressources', period)
        P = parameters(period).prestations.minima_sociaux

        demandeur_eligible_asi = famille.demandeur('asi_eligibilite', period)
        demandeur_eligible_aspa = famille.demandeur('aspa_eligibilite', period)
        conjoint_eligible_asi = famille.conjoint('asi_eligibilite', period)
        conjoint_eligible_aspa = famille.conjoint('aspa_eligibilite', period)

        # Un seul éligible
        elig1 = ((asi_aspa_nb_alloc == 1) & (demandeur_eligible_aspa | conjoint_eligible_aspa))
        # Couple d'éligibles
        elig2 = (demandeur_eligible_aspa & conjoint_eligible_aspa)
        # Un seul éligible et époux éligible ASI
        elig3 = ((demandeur_eligible_asi & conjoint_eligible_aspa) | (conjoint_eligible_asi & demandeur_eligible_aspa)) & maries
        # Un seul éligible et conjoint non marié éligible ASI
        elig4 = ((demandeur_eligible_asi & conjoint_eligible_aspa) | (conjoint_eligible_asi & demandeur_eligible_aspa)) & not_(maries)

        elig = elig1 | elig2 | elig3 | elig4

        montant_max = (
            elig1 * P.aspa.montant_annuel_seul +
            elig2 * P.aspa.montant_annuel_couple +
            elig3 * (P.asi.montant_couple / 2 + P.aspa.montant_annuel_couple / 2) +
            elig4 * (P.asi.montant_seul + P.aspa.montant_annuel_couple / 2)
            ) / 12

        ressources = base_ressources + montant_max

        plafond_ressources = (elig1 * (P.aspa.plafond_ressources_seul * not_(en_couple) + P.aspa.plafond_ressources_couple * en_couple) +
            (elig2 | elig3 | elig4) * P.aspa.plafond_ressources_couple) / 12

        depassement = max_(ressources - plafond_ressources, 0)

        diff = ((elig1 | elig2) * (montant_max - depassement) +
            (elig3 | elig4) * (P.aspa.montant_annuel_couple / 12 / 2 - depassement / 2))

        # Montant mensuel servi (sous réserve d'éligibilité)
        montant_servi_aspa = max_(diff, 0)

        # TODO: Faute de mieux, on verse l'aspa à la famille plutôt qu'aux individus
        # aspa[CHEF] = demandeur_eligible_aspa*montant_servi_aspa*(elig1 + elig2/2)
        # aspa[PART] = conjoint_eligible_aspa*montant_servi_aspa*(elig1 + elig2/2)
        return elig * montant_servi_aspa
