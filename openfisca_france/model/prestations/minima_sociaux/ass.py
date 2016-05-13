# -*- coding: utf-8 -*-

from __future__ import division

from numpy import (absolute as abs_, logical_and as and_, logical_not as not_, logical_or as or_, maximum as max_,
                   minimum as min_)

from ...base import *  # noqa analysis:ignore


class ass_precondition_remplie(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Éligible à l'ASS"




class ass(Variable):
    column = FloatCol
    label = u"Montant de l'ASS pour une famille"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month

        ass_base_ressources = simulation.calculate('ass_base_ressources', period)
        ass_eligibilite_i_holder = simulation.compute('ass_eligibilite_individu', period)
        en_couple = simulation.calculate('en_couple', period)
        ass_params = simulation.legislation_at(period.start).minim.ass

        ass_eligibilite_i = self.split_by_roles(ass_eligibilite_i_holder, roles = [CHEF, PART])

        elig = or_(ass_eligibilite_i[CHEF], ass_eligibilite_i[PART])
        montant_journalier = ass_params.montant_plein
        montant_mensuel = 30 * montant_journalier
        plafond_mensuel = montant_journalier * (ass_params.plaf_seul * not_(en_couple) + ass_params.plaf_coup * en_couple)
        revenus = ass_base_ressources / 12

        ass = min_(montant_mensuel, plafond_mensuel - revenus)
        ass = max_(ass, 0)
        ass = ass * elig
        ass = ass * not_(ass < ass_params.montant_plein)  # pas d'ASS si montant mensuel < montant journalier de base

        return period, ass


class ass_base_ressources(Variable):
    column = FloatCol
    label = u"Base de ressources de l'ASS"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        ass_base_ressources_i_holder = simulation.compute('ass_base_ressources_individu', period)
        ass_base_ressources_demandeur = self.filter_role(ass_base_ressources_i_holder, role = CHEF)
        ass_base_ressources_conjoint_holder = simulation.compute('ass_base_ressources_conjoint', period)
        ass_base_ressources_conjoint = self.filter_role(ass_base_ressources_conjoint_holder, role = PART)

        result = ass_base_ressources_demandeur + ass_base_ressources_conjoint
        return period, result


class ass_base_ressources_individu(Variable):
    column = FloatCol
    label = u"Base de ressources individuelle de l'ASS"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        # Rolling year
        previous_year = period.start.period('year').offset(-1)
        # N-1
        last_year = period.last_year

        salaire_imposable = simulation.calculate_add('salaire_imposable', previous_year)
        salaire_imposable_this_month = simulation.calculate('salaire_imposable', period)
        salaire_imposable_interrompu = (salaire_imposable > 0) * (salaire_imposable_this_month == 0)
        # Le Salaire d'une activité partielle est neutralisé en cas d'interruption
        salaire_imposable = (1 - salaire_imposable_interrompu) * salaire_imposable
        retraite_nette = simulation.calculate('retraite_nette', previous_year)

        def revenus_tns():
            revenus_auto_entrepreneur = simulation.calculate_add('tns_auto_entrepreneur_benefice', previous_year)

            # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1
            tns_micro_entreprise_benefice = simulation.calculate('tns_micro_entreprise_benefice', last_year)
            tns_benefice_exploitant_agricole = simulation.calculate('tns_benefice_exploitant_agricole', last_year)
            tns_autres_revenus = simulation.calculate('tns_autres_revenus', last_year)

            return revenus_auto_entrepreneur + tns_micro_entreprise_benefice + tns_benefice_exploitant_agricole + tns_autres_revenus

        pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', previous_year)
        pensions_alimentaires_versees_individu = simulation.calculate(
            'pensions_alimentaires_versees_individu', previous_year
            )

        aah = simulation.calculate_add('aah', previous_year)
        indemnites_stage = simulation.calculate('indemnites_stage', previous_year)
        revenus_stage_formation_pro = simulation.calculate('revenus_stage_formation_pro', previous_year)

        return period, (
            salaire_imposable + retraite_nette + pensions_alimentaires_percues - abs_(pensions_alimentaires_versees_individu) +
            aah + indemnites_stage + revenus_stage_formation_pro + revenus_tns()
        )


class ass_base_ressources_conjoint(Variable):
    column = FloatCol
    label = u"Base de ressources individuelle pour le conjoint du demandeur de l'ASS"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        last_month = period.start.period('month').offset(-1)
        # Rolling year
        previous_year = period.start.period('year').offset(-1)
        # N-1
        last_year = period.last_year

        has_ressources_substitution = (
            simulation.calculate('chomage_net', last_month) +
            simulation.calculate('indemnites_journalieres', last_month) +
            simulation.calculate('retraite_nette', last_month)
        ) > 0

        def calculateWithAbatement(ressourceName, neutral_totale = False):
            ressource_year = simulation.calculate_add(ressourceName, previous_year)
            ressource_last_month = simulation.calculate(ressourceName, last_month)

            ressource_interrompue = (ressource_year > 0) * (ressource_last_month == 0)

            # Les ressources interrompues sont abattues différement si elles sont substituées ou non.
            # http://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000020398006&cidTexte=LEGITEXT000006072050

            tx_abat_partiel = simulation.legislation_at(period.start).minim.ass.abat_rev_subst_conj
            tx_abat_total = simulation.legislation_at(period.start).minim.ass.abat_rev_non_subst_conj

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
            revenus_auto_entrepreneur = simulation.calculate_add('tns_auto_entrepreneur_benefice', previous_year)

            # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1
            tns_micro_entreprise_benefice = simulation.calculate('tns_micro_entreprise_benefice', last_year)
            tns_benefice_exploitant_agricole = simulation.calculate('tns_benefice_exploitant_agricole', last_year)
            tns_autres_revenus = simulation.calculate('tns_autres_revenus', last_year)

            return revenus_auto_entrepreneur + tns_micro_entreprise_benefice + tns_benefice_exploitant_agricole + tns_autres_revenus

        pensions_alimentaires_versees_individu = simulation.calculate_add('pensions_alimentaires_versees_individu', previous_year)

        result = (
            salaire_imposable + pensions_alimentaires_percues - abs_(pensions_alimentaires_versees_individu) +
            aah + indemnites_stage + revenus_stage_formation_pro + retraite_nette + chomage_net +
            indemnites_journalieres + revenus_tns()
        )

        return period, result


class ass_eligibilite_individu(Variable):
    column = BoolCol
    label = u"Éligibilité individuelle à l'ASS"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month

        # 1 si demandeur d'emploi
        activite = simulation.calculate('activite', period)

        # Indique que l'user a travaillé 5 ans au cours des 10 dernieres années.
        ass_precondition_remplie = simulation.calculate('ass_precondition_remplie', period)

        are_perceived_this_month = simulation.calculate('chomage_net', period)

        return period, and_(and_(activite == 1, ass_precondition_remplie), are_perceived_this_month == 0)
