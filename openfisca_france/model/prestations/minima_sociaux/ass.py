# -*- coding: utf-8 -*-

from __future__ import division

from numpy import absolute as abs_, logical_and as and_, logical_or as or_

from openfisca_france.model.base import *  # noqa analysis:ignore


class ass_precondition_remplie(Variable):
    value_type = bool
    entity = Individu
    label = u"Éligible à l'ASS"
    definition_period = MONTH


class ass(Variable):
    value_type = float
    label = u"Montant de l'ASS pour une famille"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        ass_base_ressources = famille('ass_base_ressources', period)
        en_couple = famille('en_couple', period)
        ass_params = parameters(period).prestations.minima_sociaux.ass

        ass_eligibilite_i = famille.members('ass_eligibilite_individu', period)
        elig = famille.any(ass_eligibilite_i, role = Famille.PARENT)

        montant_journalier = ass_params.montant_plein
        montant_mensuel = 30 * montant_journalier
        plafond_mensuel = montant_journalier * (ass_params.plaf_seul * not_(en_couple) + ass_params.plaf_coup * en_couple)
        revenus = ass_base_ressources / 12

        ass = min_(montant_mensuel, plafond_mensuel - revenus)
        ass = max_(ass, 0)
        ass = ass * elig
        ass = ass * not_(ass < ass_params.montant_plein)  # pas d'ASS si montant mensuel < montant journalier de base

        return ass


class ass_base_ressources(Variable):
    value_type = float
    label = u"Base de ressources de l'ASS"
    entity = Famille
    definition_period = MONTH

    def formula(famille, period):
        ass_base_ressources_demandeur = famille.demandeur('ass_base_ressources_individu', period)
        ass_base_ressources_conjoint = famille.conjoint('ass_base_ressources_conjoint', period)

        result = ass_base_ressources_demandeur + ass_base_ressources_conjoint
        return result


class ass_base_ressources_individu(Variable):
    value_type = float
    label = u"Base de ressources individuelle de l'ASS"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        # Rolling year
        previous_year = period.start.period('year').offset(-1)
        # N-1
        last_year = period.last_year

        salaire_imposable = individu('salaire_imposable', previous_year, options = [ADD])
        salaire_imposable_this_month = individu('salaire_imposable', period)
        salaire_imposable_interrompu = (salaire_imposable > 0) * (salaire_imposable_this_month == 0)
        # Le Salaire d'une activité partielle est neutralisé en cas d'interruption
        salaire_imposable = (1 - salaire_imposable_interrompu) * salaire_imposable
        retraite_nette = individu('retraite_nette', previous_year, options = [ADD])

        def revenus_tns():
            revenus_auto_entrepreneur = individu('tns_auto_entrepreneur_benefice', previous_year, options = [ADD])

            # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1
            tns_micro_entreprise_benefice = individu('tns_micro_entreprise_benefice', last_year)
            tns_benefice_exploitant_agricole = individu('tns_benefice_exploitant_agricole', last_year)
            tns_autres_revenus = individu('tns_autres_revenus', last_year)

            return revenus_auto_entrepreneur + tns_micro_entreprise_benefice + tns_benefice_exploitant_agricole + tns_autres_revenus

        pensions_alimentaires_percues = individu('pensions_alimentaires_percues', previous_year, options = [ADD])
        pensions_alimentaires_versees_individu = individu(
            'pensions_alimentaires_versees_individu', previous_year, options = [ADD]
            )

        aah = individu('aah', previous_year, options = [ADD])
        indemnites_stage = individu('indemnites_stage', previous_year, options = [ADD])
        revenus_stage_formation_pro = individu('revenus_stage_formation_pro', previous_year, options = [ADD])

        return (
            salaire_imposable + retraite_nette + pensions_alimentaires_percues - abs_(pensions_alimentaires_versees_individu) +
            aah + indemnites_stage + revenus_stage_formation_pro + revenus_tns()
        )


class ass_base_ressources_conjoint(Variable):
    value_type = float
    label = u"Base de ressources individuelle pour le conjoint du demandeur de l'ASS"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        last_month = period.start.period('month').offset(-1)
        # Rolling year
        previous_year = period.start.period('year').offset(-1)
        # N-1
        last_year = period.last_year

        has_ressources_substitution = (
            individu('chomage_net', last_month) +
            individu('indemnites_journalieres', last_month) +
            individu('retraite_nette', last_month)
        ) > 0

        def calculateWithAbatement(ressourceName, neutral_totale = False):
            ressource_year = individu(ressourceName, previous_year, options = [ADD])
            ressource_last_month = individu(ressourceName, last_month)

            ressource_interrompue = (ressource_year > 0) * (ressource_last_month == 0)

            # Les ressources interrompues sont abattues différement si elles sont substituées ou non.
            # http://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000020398006&cidTexte=LEGITEXT000006072050

            tx_abat_partiel = parameters(period).prestations.minima_sociaux.ass.abat_rev_subst_conj
            tx_abat_total = parameters(period).prestations.minima_sociaux.ass.abat_rev_non_subst_conj

            abat_partiel = ressource_interrompue * has_ressources_substitution * (1 - neutral_totale)
            abat_total = ressource_interrompue * (1 - abat_partiel)

            tx_abat_applique = abat_partiel * tx_abat_partiel + abat_total * tx_abat_total

            return (1 - tx_abat_applique) * ressource_year

        salaire_imposable = calculateWithAbatement('salaire_imposable')
        indemnites_stage = calculateWithAbatement('indemnites_stage', neutral_totale = True)
        revenus_stage_formation_pro = calculateWithAbatement('revenus_stage_formation_pro')
        chomage_net = calculateWithAbatement('chomage_net', neutral_totale = True)
        indemnites_journalieres = calculateWithAbatement('indemnites_journalieres')
        aah = calculateWithAbatement('aah')
        retraite_nette = calculateWithAbatement('retraite_nette')
        pensions_alimentaires_percues = calculateWithAbatement('pensions_alimentaires_percues')

        def revenus_tns():
            revenus_auto_entrepreneur = individu('tns_auto_entrepreneur_benefice', previous_year, options = [ADD])

            # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1
            tns_micro_entreprise_benefice = individu('tns_micro_entreprise_benefice', last_year)
            tns_benefice_exploitant_agricole = individu('tns_benefice_exploitant_agricole', last_year)
            tns_autres_revenus = individu('tns_autres_revenus', last_year, options = [ADD])

            return revenus_auto_entrepreneur + tns_micro_entreprise_benefice + tns_benefice_exploitant_agricole + tns_autres_revenus

        pensions_alimentaires_versees_individu = individu('pensions_alimentaires_versees_individu', previous_year, options = [ADD])

        result = (
            salaire_imposable + pensions_alimentaires_percues - abs_(pensions_alimentaires_versees_individu) +
            aah + indemnites_stage + revenus_stage_formation_pro + retraite_nette + chomage_net +
            indemnites_journalieres + revenus_tns()
        )

        return result

class ass_eligibilite_cumul_individu(Variable):
    value_type = bool
    label = u"Eligibilité au cumul de l'ASS avec un revenu d'activité"
    entity = Individu
    definition_period = MONTH
    reference = u"https://www.legifrance.gouv.fr/eli/decret/2017/5/5/ETSD1708117D/jo/article_2"

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
            nb_mois_consecutif_sans_activite = where(absence_ressources_activite * chomeur,
                                                     nb_mois_consecutif_sans_activite + 1, 0)

            nb_mois_cumul = nb_mois_cumul + 1 * presence_ressources_activite * not_(
                chomeur) * ass_precondition_remplie * absence_aah

        # si 3 mois de cumul ou moins en comptant le mois courant, droit au cumul au moins courant
        return nb_mois_cumul <= 3

class ass_eligibilite_individu(Variable):
    value_type = bool
    label = u"Éligibilité individuelle à l'ASS"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        demandeur_emploi_non_indemnise = and_(individu('activite', period) == TypesActivite.chomeur, individu('chomage_net', period) == 0)

        # Indique que l'individu a travaillé 5 ans au cours des 10 dernieres années.
        ass_precondition_remplie = individu('ass_precondition_remplie', period)

        return and_(demandeur_emploi_non_indemnise, ass_precondition_remplie)

    def formula_2017_01_01(individu, period):
        aah_eligible = individu('aah', period) > 0

        demandeur_emploi_non_indemnise = and_(individu('activite', period) == TypesActivite.chomeur, individu('chomage_net', period) == 0)

        # Indique que l'individu a travaillé 5 ans au cours des 10 dernieres années.
        ass_precondition_remplie = individu('ass_precondition_remplie', period)

        return and_(not_(aah_eligible), and_(demandeur_emploi_non_indemnise, ass_precondition_remplie))

    def formula_2017_09_01(individu, period):
        '''
        Reference : https://www.legifrance.gouv.fr/eli/decret/2017/5/5/ETSD1708117D/jo/article_2
        '''
        aah_eligible = individu('aah', period) > 0

        demandeur_emploi_non_indemnise = and_(individu('activite', period) == TypesActivite.chomeur, individu('chomage_net', period) == 0)

        eligible_cumul_ass = individu('ass_eligibilite_cumul_individu', period)

        demandeur_emploi_non_indemnise_et_cumul_accepte = or_(demandeur_emploi_non_indemnise, not_(demandeur_emploi_non_indemnise) * eligible_cumul_ass)

        # Indique que l'individu a travaillé 5 ans au cours des 10 dernieres années.
        ass_precondition_remplie = individu('ass_precondition_remplie', period)

        return and_(not_(aah_eligible), and_(demandeur_emploi_non_indemnise_et_cumul_accepte, ass_precondition_remplie))
