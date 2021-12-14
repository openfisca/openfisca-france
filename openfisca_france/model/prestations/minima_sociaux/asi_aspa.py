from numpy import abs as abs_, logical_or as or_

from openfisca_france.model.base import *


class inapte_travail(Variable):
    value_type = bool
    entity = Individu
    label = "Reconnu inapte au travail"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class asi_aspa_base_ressources_individu(Variable):
    value_type = float
    label = "Base ressources individuelle du minimum vieillesse/ASPA"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        last_year = period.last_year
        three_previous_months = period.last_3_months
        law = parameters(period)
        leg_1er_janvier = parameters(period.start.offset('first-of', 'year'))

        ressources_incluses = [
            'allocation_securisation_professionnelle',
            'chomage_net',
            'dedommagement_victime_amiante',
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
            'traitement_indiciaire_brut'
            ]

        # Revenus du foyer fiscal que l'on projette sur le premier invidividu
        rente_viagere_titre_onereux_foyer_fiscal = individu.foyer_fiscal('rente_viagere_titre_onereux', three_previous_months, options = [ADD])
        revenus_foyer_fiscal_individu = rente_viagere_titre_onereux_foyer_fiscal * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        plus_values = individu.foyer_fiscal('assiette_csg_plus_values', period.this_year) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL) * (3 / 12)

        def revenus_tns():
            revenus_auto_entrepreneur = individu('rpns_auto_entrepreneur_benefice', three_previous_months, options = [ADD])
            # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1

            rpns_micro_entreprise_benefice = individu('rpns_micro_entreprise_benefice', last_year) * (3 / 12)
            rpns_benefice_exploitant_agricole = individu('rpns_benefice_exploitant_agricole', last_year) * (3 / 12)
            rpns_micro_entreprise_beneficens_autres_revenus = individu('rpns_autres_revenus', last_year) * (3 / 12)

            return (
                revenus_auto_entrepreneur
                + rpns_micro_entreprise_benefice
                + rpns_benefice_exploitant_agricole
                + rpns_micro_entreprise_beneficens_autres_revenus
                )

        pension_invalidite = (individu('pensions_invalidite', period) > 0)
        aspa_eligibilite = individu('aspa_eligibilite', period)
        asi_eligibilite = individu('asi_eligibilite', period)

        # Exclut l'AAH si éligible ASPA, retraite ou pension invalidité
        # en application du II.B. de http://www.legislation.cnav.fr/Pages/texte.aspx?Nom=LE_MIN_19031982
        aah = individu('aah', three_previous_months, options = [ADD])
        aah = aah * not_(aspa_eligibilite) * not_(asi_eligibilite) * not_(pension_invalidite)

        pensions_alimentaires_versees = individu(
            'pensions_alimentaires_versees_individu', three_previous_months, options = [ADD]
            )

        def abattement_salaire():
            aspa_couple = individu.famille('aspa_couple', period)

            # Abattement sur les salaires (appliqué sur une base trimestrielle)
            abattement_forfaitaire_base = (
                leg_1er_janvier.marche_travail.salaire_minimum.smic_h_b * law.marche_travail.salaire_minimum.nb_heure_travail_mensuel
                )

            taux_abattement_forfaitaire = where(
                aspa_couple,
                law.prestations.minima_sociaux.aspa.abattement_forfaitaire_tx_couple,
                law.prestations.minima_sociaux.aspa.abattement_forfaitaire_tx_seul
                )

            abattement_forfaitaire = abattement_forfaitaire_base * taux_abattement_forfaitaire
            salaire_de_base = individu('salaire_de_base', three_previous_months, options = [ADD])
            traitement_indiciaire_brut = individu('traitement_indiciaire_brut', three_previous_months, options = [ADD])
            return min_(salaire_de_base + traitement_indiciaire_brut, abattement_forfaitaire)

        base_ressources_3_mois = sum(
            max_(0, individu(ressource_type, three_previous_months, options = [ADD]))
            for ressource_type in ressources_incluses
            ) + aah + revenus_foyer_fiscal_individu + revenus_tns() - abs_(pensions_alimentaires_versees) - abattement_salaire() + plus_values

        return base_ressources_3_mois / 3


class asi_aspa_base_ressources(Variable):
    value_type = float
    label = "Base ressource du minimum vieillesse et assimilés (ASPA)"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        base_ressources_i = famille.members('asi_aspa_base_ressources_individu', period)
        ass_i = famille.members('ass', period)
        return famille.sum(base_ressources_i + ass_i, role = Famille.PARENT)


class aspa_eligibilite(Variable):
    value_type = bool
    label = "Indicatrice individuelle d'éligibilité à l'allocation de solidarité aux personnes agées"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

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
    label = "Indicatrice individuelle d'éligibilité à l'allocation supplémentaire d'invalidité"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        last_month = period.start.period('month').offset(-1)

        non_eligible_aspa = not_(individu('aspa_eligibilite', period))
        touche_pension_invalidite = individu('pensions_invalidite', period) > 0
        handicap = individu('handicap', period)
        touche_retraite = individu('retraite_nette', last_month) > 0
        condition_nationalite = individu('asi_aspa_condition_nationalite', period)

        eligible = (
            non_eligible_aspa
            * condition_nationalite
            * (handicap * touche_retraite + touche_pension_invalidite)
            )

        return eligible


class asi_aspa_condition_nationalite(Variable):
    value_type = bool
    default_value = True
    label = "Condition de nationalité et de titre de séjour pour bénéficier de l'ASPA ou l'ASI"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period, parameters):
        ressortissant_eee = individu('ressortissant_eee', period)
        ressortissant_suisse = individu('nationalite', period) == b'CH'
        duree_possession_titre_sejour = individu('duree_possession_titre_sejour', period)
        duree_min_titre_sejour = parameters(period).prestations.minima_sociaux.aspa.duree_min_titre_sejour

        return or_(ressortissant_eee, ressortissant_suisse, duree_possession_titre_sejour >= duree_min_titre_sejour)


class asi_aspa_nb_alloc(Variable):
    value_type = int
    label = "Nombre d'allocataires ASI/ASPA"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period, parameters):
        aspa_elig_i = famille.members('aspa_eligibilite', period)
        asi_elig_i = famille.members('asi_eligibilite', period)

        nb_allocataire_asi = famille.sum(asi_elig_i, role = Famille.PARENT)
        nb_allocataire_aspa = famille.sum(aspa_elig_i, role = Famille.PARENT)

        return nb_allocataire_asi + nb_allocataire_aspa


class asi(Variable):
    value_type = float
    label = "Allocation supplémentaire d'invalidité (ASI)"
    entity = Individu
    definition_period = MONTH
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006156277/"
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula_2007(individu, period, parameters):
        maries = individu.famille('maries', period)
        en_couple = individu.famille('en_couple', period)
        asi_aspa_nb_alloc = individu.famille('asi_aspa_nb_alloc', period)
        base_ressources = individu.famille('asi_aspa_base_ressources', period)
        P = parameters(period).prestations.minima_sociaux

        demandeur_eligible_asi = individu.famille.demandeur('asi_eligibilite', period)
        demandeur_eligible_aspa = individu.famille.demandeur('aspa_eligibilite', period)
        conjoint_eligible_asi = individu.famille.conjoint('asi_eligibilite', period)
        conjoint_eligible_aspa = individu.famille.conjoint('aspa_eligibilite', period)

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

        montant_max = (
            elig1 * P.asi.montant_seul
            + elig2 * P.asi.montant_couple
            + elig3 * 2 * P.asi.montant_seul
            + elig4 * (P.asi.montant_couple / 2 + P.aspa.montant_annuel_couple / 2)
            + elig5 * (P.asi.montant_seul + P.aspa.montant_annuel_couple / 2)) / 12

        ressources = base_ressources + montant_max

        plafond_ressources = (
            elig1 * (P.asi.plafond_ressource_seul * not_(en_couple) + P.asi.plafond_ressource_couple * en_couple)
            + elig2 * P.asi.plafond_ressource_couple
            + elig3 * P.asi.plafond_ressource_couple
            + elig4 * P.aspa.plafond_ressources_couple
            + elig5 * P.aspa.plafond_ressources_couple) / 12

        depassement = max_(ressources - plafond_ressources, 0)

        diff = (
            (elig1 | elig2 | elig3) * (montant_max - depassement)
            + elig4 * (P.asi.montant_couple / 12 / 2 - depassement / 2)
            + elig5 * (P.asi.montant_seul / 12 - depassement / 2)
            )

        # Montant mensuel servi (sous réserve d'éligibilité)
        montant_servi_asi = max_(diff, 0)
        return montant_servi_asi * (
            individu.has_role(Famille.DEMANDEUR) * demandeur_eligible_asi * (elig1 + elig2 / 2 + elig3 / 2)
            + individu.has_role(Famille.CONJOINT) * conjoint_eligible_asi * (elig1 + elig2 / 2 + elig3 / 2)
            )


class aspa_couple(Variable):
    value_type = bool
    label = "Couple au sens de l'ASPA"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

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
    label = "Allocation de solidarité aux personnes agées"
    reference = "http://vosdroits.service-public.fr/particuliers/F16871.xhtml"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2006_01_01(famille, period, parameters):
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
            elig1 * P.aspa.montant_annuel_seul
            + elig2 * P.aspa.montant_annuel_couple
            + elig3 * (P.asi.montant_couple / 2 + P.aspa.montant_annuel_couple / 2)
            + elig4 * (P.asi.montant_seul + P.aspa.montant_annuel_couple / 2)
            ) / 12

        ressources = base_ressources + montant_max

        plafond_ressources = (
            elig1
            * (P.aspa.plafond_ressources_seul * not_(en_couple) + P.aspa.plafond_ressources_couple * en_couple)
            + (elig2 | elig3 | elig4)
            * P.aspa.plafond_ressources_couple
            ) / 12

        depassement = max_(ressources - plafond_ressources, 0)

        diff = (
            (elig1 | elig2) * (montant_max - depassement)
            + (elig3 | elig4) * (P.aspa.montant_annuel_couple / 12 / 2 - depassement / 2)
            )

        # Montant mensuel servi (sous réserve d'éligibilité)
        montant_servi_aspa = max_(diff, 0)

        # TODO: Faute de mieux, on verse l'aspa à la famille plutôt qu'aux individus
        # aspa[CHEF] = demandeur_eligible_aspa*montant_servi_aspa*(elig1 + elig2/2)
        # aspa[PART] = conjoint_eligible_aspa*montant_servi_aspa*(elig1 + elig2/2)
        return elig * montant_servi_aspa
