# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import absolute as abs_, maximum as max_, minimum as min_, logical_not as not_, logical_or as or_, logical_and as and_

from ...base import *  # noqa analysis:ignore


build_column('ass_precondition_remplie', BoolCol(entity = "ind", label = u"Éligible à l'ASS"))


@reference_formula
class ass(SimpleFormulaColumn):
    column = FloatCol
    label = u"Montant de l'ASS pour une famille"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        ass_base_ressources = simulation.calculate('ass_base_ressources', period)
        ass_eligibilite_i_holder = simulation.compute('ass_eligibilite_i', period)
        concub = simulation.calculate('concub', period)
        ass_params = simulation.legislation_at(period.start).minim.ass

        ass_eligibilite_i = self.split_by_roles(ass_eligibilite_i_holder, roles = [CHEF, PART])

        elig = or_(ass_eligibilite_i[CHEF], ass_eligibilite_i[PART])
        montant_journalier = ass_params.montant_plein
        montant_mensuel = 30 * montant_journalier
        plafond_mensuel = montant_journalier * (ass_params.plaf_seul * not_(concub) + ass_params.plaf_coup * concub)
        revenus = ass_base_ressources / 12

        ass = min_(montant_mensuel, plafond_mensuel - revenus)
        ass = max_(ass, 0)
        ass = ass * elig
        ass = ass * not_(ass < ass_params.montant_plein)  # pas d'ASS si montant mensuel < montant journalier de base

        return period, ass


@reference_formula
class ass_base_ressources(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressources de l'ASS"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        ass_base_ressources_i_holder = simulation.compute('ass_base_ressources_i', period)
        ass_base_ressources_demandeur = self.filter_role(ass_base_ressources_i_holder, role = CHEF)
        ass_base_ressources_conjoint_holder = simulation.compute('ass_base_ressources_conjoint', period)
        ass_base_ressources_conjoint = self.filter_role(ass_base_ressources_conjoint_holder, role = PART)

        result = ass_base_ressources_demandeur + ass_base_ressources_conjoint
        return period, result


@reference_formula
class ass_base_ressources_i(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressources individuelle de l'ASS"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        previous_year = period.start.period('year').offset(-1)

        sali = simulation.calculate_add('sali', previous_year)
        rstnet = simulation.calculate('rstnet', previous_year)
        tns_auto_entrepreneur_benefice = simulation.calculate_add('tns_auto_entrepreneur_benefice', previous_year)
        tns_micro_entreprise_benefice = simulation.calculate_add('tns_micro_entreprise_benefice', period)
        tns_benefice_exploitant_agricole = simulation.calculate('tns_benefice_exploitant_agricole', period)
        tns_autres_revenus = simulation.calculate('tns_autres_revenus', period)
        pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', previous_year)
        pensions_alimentaires_versees_individu = simulation.calculate('pensions_alimentaires_versees_individu', previous_year)

        aah = simulation.calculate_add('aah', previous_year)
        indemnites_stage = simulation.calculate('indemnites_stage', previous_year)
        revenus_stage_formation_pro = simulation.calculate('revenus_stage_formation_pro', previous_year)

        return period, (
            sali + rstnet + pensions_alimentaires_percues - abs_(pensions_alimentaires_versees_individu) +
            aah + indemnites_stage + revenus_stage_formation_pro + tns_auto_entrepreneur_benefice +
            tns_micro_entreprise_benefice + tns_benefice_exploitant_agricole + tns_autres_revenus
        )


@reference_formula
class ass_base_ressources_conjoint(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressources individuelle pour le conjoint du demandeur de l'ASS"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        previous_year = period.start.period('year').offset(-1)
        last_month = period.start.period('month').offset(-1)

        has_ressources_substitution = (
            simulation.calculate('chonet', last_month) +
            simulation.calculate('indemnites_journalieres', last_month) +
            simulation.calculate('rstnet', last_month)
        ) > 0

        def calculateWithAbatement(ressourceName):
            ressource_year = simulation.calculate_add(ressourceName, previous_year)
            ressource_last_month = simulation.calculate(ressourceName, last_month)

            ressource_interrompue = (ressource_year > 0) * (ressource_last_month == 0)

            # Les ressources interrompues sont abattues différement si elles sont substituées ou non.
            # http://www.legifrance.gouv.fr/affichCodeArticle.do?idArticle=LEGIARTI000020398006&cidTexte=LEGITEXT000006072050

            abat_res_interrompues_substituees = simulation.legislation_at(period.start).minim.ass.abat_rev_subst_conj
            abat_res_interrompues_non_substituees = simulation.legislation_at(period.start).minim.ass.abat_rev_non_subst_conj

            abat_reel = ressource_interrompue * (
                has_ressources_substitution * abat_res_interrompues_substituees +
                (1 - has_ressources_substitution) * abat_res_interrompues_non_substituees)

            return (1 - abat_reel) * ressource_year

        sali = calculateWithAbatement('sali')
        indemnites_stage = calculateWithAbatement('indemnites_stage')
        revenus_stage_formation_pro = calculateWithAbatement('revenus_stage_formation_pro')
        chonet = calculateWithAbatement('chonet')
        indemnites_journalieres = calculateWithAbatement('indemnites_journalieres')
        aah = calculateWithAbatement('aah')
        rstnet = calculateWithAbatement('rstnet')
        pensions_alimentaires_percues = calculateWithAbatement('pensions_alimentaires_percues')
        tns_auto_entrepreneur_benefice = calculateWithAbatement('tns_auto_entrepreneur_benefice')

        tns_micro_entreprise_benefice = simulation.calculate_add('tns_micro_entreprise_benefice', period)
        tns_benefice_exploitant_agricole = simulation.calculate('tns_benefice_exploitant_agricole', period)
        tns_autres_revenus = simulation.calculate('tns_autres_revenus', period)
        pensions_alimentaires_versees_individu = simulation.calculate_add('pensions_alimentaires_versees_individu', previous_year)

        result = (
            sali + pensions_alimentaires_percues - abs_(pensions_alimentaires_versees_individu) +
            aah + indemnites_stage + revenus_stage_formation_pro + rstnet + chonet +
            indemnites_journalieres + tns_auto_entrepreneur_benefice + tns_micro_entreprise_benefice +
            tns_benefice_exploitant_agricole + tns_autres_revenus
        )

        return period, result


@reference_formula
class ass_eligibilite_i(SimpleFormulaColumn):
    column = BoolCol
    label = u"Éligibilité individuelle à l'ASS"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        # 1 si demandeur d'emploi
        activite = simulation.calculate('activite', period)

        # Indique que l'user a travaillé 5 ans au cours des 10 dernieres années.
        ass_precondition_remplie = simulation.calculate('ass_precondition_remplie', period)

        are_perceived_this_month = simulation.calculate('chonet', period)

        return period, and_(and_(activite == 1, ass_precondition_remplie), are_perceived_this_month == 0)
