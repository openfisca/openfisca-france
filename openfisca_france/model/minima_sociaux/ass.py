# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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

from numpy import maximum as max_, logical_not as not_, logical_or as or_, logical_and as and_

from ..base import *  # noqa


@reference_formula
class ass_eligibilite_i(SimpleFormulaColumn):
    column = BoolCol
    label = u"Éligibilité individuelle à l'ASS"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        activite = simulation.calculate('activite', period)
        ass_precondition_remplie = simulation.calculate('ass_precondition_remplie', period)

        return period, and_(activite == 1, ass_precondition_remplie)


@reference_formula
class ass_base_ressources_i(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressources individuelle de l'ASS"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        previous_year = period.offset(-1)
        salnet = simulation.calculate('salnet', previous_year)
        rstnet = simulation.calculate('rstnet', previous_year)
        pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', previous_year)
        aah = simulation.calculate('aah', previous_year)
        indemnites_stage = simulation.calculate('indemnites_stage', previous_year)
        revenus_stage_formation_pro = simulation.calculate('revenus_stage_formation_pro', previous_year)

        return period, salnet + rstnet + pensions_alimentaires_percues + aah + indemnites_stage + revenus_stage_formation_pro


@reference_formula
class ass_base_ressources(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressources de l'ASS"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        ass_base_ressources_i_holder = simulation.compute('ass_base_ressources_i', period)

        ass_base_ressources_i = self.split_by_roles(ass_base_ressources_i_holder, roles = [CHEF, PART])
        return period, ass_base_ressources_i[CHEF] + ass_base_ressources_i[PART]


@reference_formula
class ass(SimpleFormulaColumn):
    column = FloatCol
    label = u"Montant de l'ASS pour une famille"
    entity_class = Familles

    def function(self, simulation, period):
        '''
        L’Allocation de Solidarité Spécifique (ASS) est une allocation versée aux
        personnes ayant épuisé leurs droits à bénéficier de l'assurance chômage.

        Le prétendant doit avoir épuisé ses droits à l’assurance chômage.
        Il doit être inscrit comme demandeur d’emploi et justifier de recherches actives.
        Il doit être apte à travailler.
        Il doit justifier de 5 ans d’activité salariée au cours des 10 ans précédant le chômage.
        À partir de 60 ans, il doit répondre à des conditions particulières.

        Les ressources prises en compte pour apprécier ces plafonds, comprennent l'allocation de solidarité elle-même
        ainsi que les autres ressources de l'intéressé, et de son conjoint, partenaire pacsé ou concubin,
        soumises à impôt sur le revenu.
        Ne sont pas prises en compte, pour déterminer le droit à ASS :
          l'allocation d'assurance chômage précédemment perçue,
          les prestations familiales,
          l'allocation de logement,
          la majoration de l'ASS,
          la prime forfaitaire mensuelle de retour à l'emploi,
          la pension alimentaire ou la prestation compensatoire due par l'intéressé.

        Conditions de versement de l'ASS majorée
            Pour les allocataires admis au bénéfice de l'ASS majorée (avant le 1er janvier 2004),
            le montant de l'ASS majorée est fixé à 22,07 € par jour.
            Pour mémoire, jusqu'au 31 décembre 2003, pouvaient bénéficier de l'ASS majorée, les allocataires :
            âgés de 55 ans ou plus et justifiant d'au moins 20 ans d'activité salariée,
            ou âgés de 57 ans et demi ou plus et justifiant de 10 ans d'activité salariée,
            ou justifiant d'au moins 160 trimestres de cotisation retraite.
        '''
        period = period.start.offset('first-of', 'month').period('year')
        ass_base_ressources = simulation.calculate('ass_base_ressources', period)
        ass_eligibilite_i_holder = simulation.compute('ass_eligibilite_i', period)
        concub = simulation.calculate('concub', period)
        ass_params = simulation.legislation_at(period.start).minim.ass

        ass_eligibilite_i = self.split_by_roles(ass_eligibilite_i_holder, roles = [CHEF, PART])

        majo = 0  # TODO
        elig = or_(ass_eligibilite_i[CHEF], ass_eligibilite_i[PART])
        plafond_mensuel = ass_params.plaf_seul * not_(concub) + ass_params.plaf_coup * concub
        plafond = plafond_mensuel * 12
        montant_mensuel = 30 * (ass_params.montant_plein * not_(majo) + majo * ass_params.montant_maj)

        revenus = ass_base_ressources + 12 * montant_mensuel

        ass = 12 * montant_mensuel * (revenus <= plafond) + (revenus > plafond) * max_(plafond + 12 * montant_mensuel - revenus, 0)
        ass = ass * elig
        ass = ass * not_(ass / 12 < ass_params.montant_plein)  # pas d'ASS si montant mensuel < montant journalier de base

        return period, ass

