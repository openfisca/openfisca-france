from numpy import absolute as abs_, logical_and as and_

from openfisca_core.periods import Period

from openfisca_france.model.base import *

from numpy import datetime64

from openfisca_core.periods import Instant

class ass_precondition_remplie(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu a travaillé au moins 5 ans durant les 10 dernières années précédant la fin de contrat de travail"
    definition_period = MONTH
    reference = [
        'Article R5423-1 du Code du travail',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006072050&idArticle=LEGIARTI000018525084&dateTexte=20190618&categorieLien=cid#LEGIARTI000018525084'
        ]
    set_input = set_input_dispatch_by_period

    def formula(individu,period):
        nombre_annees_travaillees_les_10_dernieres_annees = individu('nombre_annees_travaillees_les_10_dernieres_annees', period)
        condition_eligibilite = nombre_annees_travaillees_les_10_dernieres_annees >= 5

        return condition_eligibilite


class nombre_annees_travaillees_les_10_dernieres_annees(Variable):
    value_type = float
    entity = Individu
    label = "Nombre d'années travaillées dans les 10 dernières années précédent la fin du contrat de travail"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        nombre_jours_travailles_10_dernieres_annees = individu.empty_array()
        for months in range(0, 552):
            contrat_de_travail_fin_potentiel = period.offset(-months)
            nombre_jours_travailles_10_dernieres_annees = where(
                individu('contrat_de_travail_fin', period) == datetime64(contrat_de_travail_fin_potentiel.start),
                individu(
                    'nombre_jours_calendaires',
                    contrat_de_travail_fin_potentiel.offset(-120).start.period('month', 120),
                    options = [ADD],
                    ),
                nombre_jours_travailles_10_dernieres_annees,
                )

        nombre_mois_travailles_10_dernieres_annees = nombre_jours_travailles_10_dernieres_annees / 30
        nombre_annees_travaillees_10_dernieres_annees = nombre_mois_travailles_10_dernieres_annees / 12

        return nombre_annees_travaillees_10_dernieres_annees

class ass(Variable):
    value_type = float
    label = "Montant de l'ASS pour un individu"
    reference = [
        'https://www.service-public.fr/particuliers/vosdroits/F12484',
        'https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006072050/LEGISCTA000018496266/'
        ]
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        ass_base_ressources = individu.famille('ass_base_ressources', period)
        en_couple = individu.famille('en_couple', period)
        residence_mayotte = individu.menage('residence_mayotte', period)
        ass_params = parameters(period).chomage.allocations_assurance_chomage.ass

        elig = individu('ass_eligibilite_individu', period)

        non_cumul_avec_aah = not_(individu('aah', period) > 0)

        montant_journalier = where(residence_mayotte, ass_params.montant_plein_mayotte, ass_params.montant_plein)
        montant_mensuel = 30 * montant_journalier
        plafond_mensuel = montant_journalier * (
            not_(en_couple) * ass_params.plaf_seul
            + en_couple * ass_params.plaf_coup
            )
        revenus = ass_base_ressources / 12

        ass = min_(montant_mensuel, plafond_mensuel - revenus)
        ass = max_(ass, 0)
        ass = ass * elig * non_cumul_avec_aah
        # pas d'ASS si montant mensuel < montant journalier de base
        ass = ass * not_(ass < ass_params.montant_plein)

        return ass


class ass_base_ressources(Variable):
    value_type = float
    label = "Base de ressources de l'ASS"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period):
        ass_base_ressources_demandeur = famille.demandeur('ass_base_ressources_individu', period)
        ass_base_ressources_conjoint = famille.conjoint('ass_base_ressources_conjoint', period)

        result = ass_base_ressources_demandeur + ass_base_ressources_conjoint
        return result


class ass_base_ressources_individu(Variable):
    value_type = float
    label = "Base de ressources individuelle de l'ASS"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        # Articles R5423-1 à 6 du code du travail
        'https://www.legifrance.gouv.fr/affichCode.do?idSectionTA=LEGISCTA000018525086&cidTexte=LEGITEXT000006072050&dateTexte=20181227'
        ]

    def formula(individu, period, parameters):
        # Rolling year
        previous_year = Period(('year', period.start, 1)).offset(-1)
        # N-1
        last_year = period.last_year

        salaire_imposable = calculateWithAbatement(individu, parameters, period, 'salaire_imposable')
        revenus_stage_formation_pro = calculateWithAbatement(individu, parameters, period, 'revenus_stage_formation_pro')
        aah = calculateWithAbatement(individu, parameters, period, 'aah')
        retraite_nette = calculateWithAbatement(individu, parameters, period, 'retraite_nette')
        pensions_alimentaires_percues = calculateWithAbatement(individu, parameters, period, 'pensions_alimentaires_percues')
        indemnites_stage = calculateWithAbatement(individu, parameters, period, 'indemnites_stage')

        pensions_invalidite = individu('pensions_invalidite', previous_year, options=[ADD])
        revenus_locatifs = individu('revenus_locatifs', previous_year, options=[ADD])
        revenus_capital = individu('revenus_capital', period)

        def revenus_tns():
            revenus_auto_entrepreneur = individu('rpns_auto_entrepreneur_benefice', previous_year, options=[ADD])

            # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1
            rpns_micro_entreprise_benefice = individu('rpns_micro_entreprise_benefice', last_year)
            rpns_benefice_exploitant_agricole = individu('rpns_benefice_exploitant_agricole', last_year)
            rpns_autres_revenus = individu('rpns_autres_revenus', last_year)

            return revenus_auto_entrepreneur + rpns_micro_entreprise_benefice + rpns_benefice_exploitant_agricole + rpns_autres_revenus

        pensions_alimentaires_versees_individu = individu('pensions_alimentaires_versees_individu', previous_year, options=[ADD])

        return (
            salaire_imposable
            + retraite_nette
            + pensions_invalidite
            + pensions_alimentaires_percues
            - abs_(pensions_alimentaires_versees_individu)
            + aah
            + indemnites_stage
            + revenus_stage_formation_pro
            + revenus_tns()
            + revenus_locatifs
            + revenus_capital
            )


class ass_base_ressources_conjoint(Variable):
    value_type = float
    label = "Base de ressources individuelle pour le conjoint du demandeur de l'ASS"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        # Rolling year
        previous_year = Period(('year', period.start, 1)).offset(-1)

        last_month = Period(('month', period.start, 1)).offset(-1)

        ass_base_ressources_individu = individu('ass_base_ressources_individu', period)
        chomage_net_interrompue = individu('chomage_net', last_month) == 0
        chomage_net = individu('chomage_net', previous_year, options=[ADD]) * (1 - chomage_net_interrompue)
        indemnites_journalieres = calculateWithAbatement(individu, parameters, period, 'indemnites_journalieres')

        return (
            ass_base_ressources_individu
            + chomage_net
            + indemnites_journalieres
            )


def calculateWithAbatement(individu, parameters, period, ressourceName):
    last_month = Period(('month', period.start, 1)).offset(-1)
    has_ressources_substitution = (
        individu('chomage_net', last_month)
        + individu('indemnites_journalieres', last_month)
        + individu('retraite_nette', last_month)
        ) > 0
    # Rolling year
    previous_year = Period(('year', period.start, 1)).offset(-1)

    ressource_year = individu(ressourceName, previous_year, options=[ADD])
    ressource_last_month = individu(ressourceName, last_month)

    ressource_interrompue = (ressource_year > 0) * (ressource_last_month == 0)

    # Les ressources interrompues sont abattues différement si elles sont substituées ou non.
    # http://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000020398006&cidTexte=LEGITEXT000006072050

    tx_abat_partiel = parameters(period).chomage.allocations_assurance_chomage.ass.abat_rev_subst_conj
    tx_abat_total = parameters(period).chomage.allocations_assurance_chomage.ass.abat_rev_non_subst_conj

    tx_abat_applique = where(has_ressources_substitution, tx_abat_partiel, tx_abat_total)

    return where(ressource_interrompue, (1 - tx_abat_applique) * ressource_year, ressource_year)


class ass_eligibilite_cumul_individu(Variable):
    value_type = bool
    label = "Eligibilité au cumul de l'ASS avec un revenu d'activité"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = [
        'Article R5425-2 du code du travail',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006072050&idArticle=LEGIARTI000018496568&dateTexte=',
        'https://www.legifrance.gouv.fr/eli/decret/2017/5/5/ETSD1708117D/jo/article_2'
        ]

    def formula_2017_09_01(individu, period):
        douze_mois_precedents = [period.offset(offset) for offset in range(-12, 0 + 1)]
        nb_mois_cumul = 0
        nb_mois_consecutif_sans_activite = 0

        for mois in douze_mois_precedents:
            presence_ressources_activite = individu('salaire_imposable', mois) > 0
            absence_ressources_activite = not_(presence_ressources_activite)
            ass_precondition_remplie = individu('ass_precondition_remplie', mois)
            chomeur = individu('activite', mois) == TypesActivite.chomeur
            absence_aah = not_(individu('aah', mois) > 0)

            # reinitialisation du nombre de mois de cumul après 3 mois consécutif sans activité
            nb_mois_cumul = nb_mois_cumul * (nb_mois_consecutif_sans_activite < 3)
            nb_mois_consecutif_sans_activite = where(absence_ressources_activite * chomeur, nb_mois_consecutif_sans_activite + 1, 0)

            nb_mois_cumul = (
                nb_mois_cumul
                + 1
                * presence_ressources_activite
                * not_(chomeur)
                * ass_precondition_remplie
                * absence_aah
                )

        # si 3 mois de cumul ou moins en comptant le mois courant, droit au cumul au moins courant
        return nb_mois_cumul <= 3


class ass_eligibilite_individu(Variable):
    value_type = bool
    label = "Éligibilité individuelle à l'ASS"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = [
        'Article L5423-1 du code du travail',
        'https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006072050&idArticle=LEGIARTI000006903847&dateTexte=&categorieLien=cid',
        ]

    def formula(individu, period, parameters):
        age_max = parameters(period).chomage.allocations_assurance_chomage.ass.age_max
        sous_age_limite = individu('age_en_mois', period) <= age_max

        demandeur_emploi_non_indemnise = and_(individu('activite', period) == TypesActivite.chomeur, individu('chomage_net', period) == 0)

        ass_precondition_remplie = individu('ass_precondition_remplie', period)

        return demandeur_emploi_non_indemnise * ass_precondition_remplie * sous_age_limite

    def formula_2017_01_01(individu, period, parameters):
        age_max = parameters(period).chomage.allocations_assurance_chomage.ass.age_max
        sous_age_limite = individu('age_en_mois', period) <= age_max

        aah_eligible = individu('aah', period) > 0

        eligible_cumul_ass = individu('ass_eligibilite_cumul_individu', period)

        demandeur_emploi_non_indemnise_et_cumul_accepte = (
            (individu('chomage_net', period) == 0)
            * ((individu('activite', period) == TypesActivite.chomeur) + eligible_cumul_ass)
            )

        ass_precondition_remplie = individu('ass_precondition_remplie', period)

        return not_(aah_eligible) * demandeur_emploi_non_indemnise_et_cumul_accepte * ass_precondition_remplie * sous_age_limite
