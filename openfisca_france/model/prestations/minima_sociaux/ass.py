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

from numpy import absolute as abs_, maximum as max_, logical_not as not_, logical_or as or_, logical_and as and_

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

        majo = 0  # Majoration pas encore implémentée aujourd'hui
        elig = or_(ass_eligibilite_i[CHEF], ass_eligibilite_i[PART])
        plafond_mensuel = ass_params.plaf_seul * not_(concub) + ass_params.plaf_coup * concub
        montant_mensuel = 30 * (ass_params.montant_plein * not_(majo) + majo * ass_params.montant_maj)
        revenus = ass_base_ressources / 12 + montant_mensuel
        ass = montant_mensuel * (revenus <= plafond_mensuel) + (revenus > plafond_mensuel) * max_(plafond_mensuel + montant_mensuel - revenus, 0)
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
        pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', previous_year)
        pensions_alimentaires_versees_individu = simulation.calculate('pensions_alimentaires_versees_individu', previous_year)

        aah = simulation.calculate('aah', previous_year)
        indemnites_stage = simulation.calculate('indemnites_stage', previous_year)
        revenus_stage_formation_pro = simulation.calculate('revenus_stage_formation_pro', previous_year)

        return period, sali + rstnet + pensions_alimentaires_percues - abs_(pensions_alimentaires_versees_individu) + aah + indemnites_stage + revenus_stage_formation_pro


@reference_formula
class ass_base_ressources_conjoint(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressources individuelle pour le conjoint du demandeur de l'ASS"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        previous_year = period.start.period('year').offset(-1)
        last_month = period.start.period('month').offset(-1)

        sali = simulation.calculate_add('sali', previous_year)
        sali_last_month = simulation.calculate('sali', last_month)
        sali_this_month = simulation.calculate('sali', period)

        rstnet = simulation.calculate('rstnet', previous_year)
        pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', previous_year)
        pensions_alimentaires_versees_individu = simulation.calculate('pensions_alimentaires_versees_individu', previous_year)
        aah = simulation.calculate('aah', previous_year)
        indemnites_stage = simulation.calculate('indemnites_stage', previous_year)
        revenus_stage_formation_pro = simulation.calculate('revenus_stage_formation_pro', previous_year)
        chonet = simulation.calculate('chonet', previous_year)
        indemnites_journalieres = simulation.calculate_add('indemnites_journalieres', previous_year)
        abat_res_interrompues_substituees = simulation.legislation_at(period.start).minim.ass.abat_rev_subst_conj
        abat_res_interrompues_non_substituees = 1
        has_ressources_substitution = (rstnet + chonet + indemnites_journalieres) > 0
        sali_interrompu = (sali > 0) * (sali_last_month == 0)
        sali_interrompu_this_month = (sali > 0) * (sali_last_month > 0) * (sali_this_month == 0)

        # Les ressources interrompues sont abattues différement si elles sont substituées ou non.
        # Dans le cas de ressources interrompues le mois en cours, on suppose qu'elles sont substitues
        abat_reel = (
            sali_interrompu * (
                has_ressources_substitution * abat_res_interrompues_substituees +
                (1 - has_ressources_substitution) * abat_res_interrompues_non_substituees
            ) +
            sali_interrompu_this_month * abat_res_interrompues_substituees
        )

        result = (
            (1 - abat_reel) * sali + pensions_alimentaires_percues - abs_(pensions_alimentaires_versees_individu) +
            aah + indemnites_stage + revenus_stage_formation_pro + rstnet + chonet + indemnites_journalieres
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
