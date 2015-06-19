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

from ...base import *  # noqa analysis:ignore
from numpy import vectorize, absolute as abs_, minimum as min_, maximum as max_


reference_input_variable(
    name ='parisien',
    column = BoolCol,
    entity_class = Menages,
    label = u"Résidant à Paris au moins 3 ans dans les 5 dernières années",
)


# @reference_formula
# class parisien(SimpleFormulaColumn):
#     column = BoolCol
#     label = u"Résident à Paris"
#     entity_class = Menages

#     def function(self, simulation, period):
#         depcom = simulation.calculate('depcom', period)

#         def is_parisien(code_insee):
#             prefix = code_insee[0:2]
#             sufix = code_insee[2:5]
#             result = (prefix == "75") and ((int(sufix) in range(101, 121)) or sufix == "056")
#             return result

#         is_parisien_vec = vectorize(is_parisien)

#         result = is_parisien_vec(depcom)

#         return period, result


@reference_formula
class paris_logement_familles_elig(SimpleFormulaColumn):
    column = BoolCol
    label = u"Eligibilité à Paris-Logement-Familles"
    entity_class = Familles

    def function(self, simulation, period):
        parisien = simulation.calculate('parisien', period)
        statut_occupation = simulation.calculate('statut_occupation', period)
        charge_logement = (
            (statut_occupation == 1) +
            (statut_occupation == 3) +
            (statut_occupation == 4) +
            (statut_occupation == 5) +
            (statut_occupation == 7)
        )

        result = parisien * charge_logement

        return period, result


@reference_formula
class paris_logement_familles_br_i(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressources individuelle pour Paris Logement Famille"
    entity_class = Individus

    def function(self, simulation, period):
        salaire_net = simulation.calculate('salaire_net', period)
        chonet = simulation.calculate('chonet', period)
        rstnet = simulation.calculate('rstnet', period)
        pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', period)
        pensions_alimentaires_versees_individu = simulation.calculate('pensions_alimentaires_versees_individu', period)
        rsa_base_ressources_patrimoine_i = simulation.calculate_add('rsa_base_ressources_patrimoine_i', period)
        indemnites_journalieres_imposables = simulation.calculate('indemnites_journalieres_imposables', period)
        indemnites_stage = simulation.calculate('indemnites_stage', period)
        revenus_stage_formation_pro = simulation.calculate('revenus_stage_formation_pro', period)
        allocation_securisation_professionnelle = simulation.calculate('allocation_securisation_professionnelle', period)
        prestation_compensatoire = simulation.calculate('prestation_compensatoire', period)
        pensions_invalidite = simulation.calculate('pensions_invalidite', period)
        indemnites_chomage_partiel = simulation.calculate('indemnites_chomage_partiel', period)
        bourse_recherche = simulation.calculate('bourse_recherche', period)
        gains_exceptionnels = simulation.calculate('gains_exceptionnels', period)
        tns_total_revenus_net = simulation.calculate_add('tns_total_revenus_net', period)

        result = (
            salaire_net + indemnites_chomage_partiel + indemnites_stage + chonet + rstnet +
            pensions_alimentaires_percues - abs_(pensions_alimentaires_versees_individu) +
            rsa_base_ressources_patrimoine_i + allocation_securisation_professionnelle +
            indemnites_journalieres_imposables + prestation_compensatoire +
            pensions_invalidite + bourse_recherche + gains_exceptionnels + tns_total_revenus_net +
            revenus_stage_formation_pro
        )

        return period, result


@reference_formula
class paris_logement_familles_br(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressource pour Paris Logement Famille"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        paris_logement_familles_br_i_holder = simulation.compute('paris_logement_familles_br_i', period)
        paris_logement_familles_br = self.sum_by_entity(paris_logement_familles_br_i_holder)
        result = paris_logement_familles_br

        return period, result


@reference_formula
class paris_logement_familles(SimpleFormulaColumn):
    column = FloatCol
    label = u"Allocation Paris Logement Familles"
    entity_class = Familles
    url = "http://www.paris.fr/pratique/toutes-les-aides-et-allocations/aides-sociales/paris-logement-familles-prestation-ville-de-paris/rub_9737_stand_88805_port_24193"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        elig = simulation.calculate('paris_logement_familles_elig', period)
        br = simulation.calculate('paris_logement_familles_br', period)
        nbenf = simulation.calculate('af_nbenf', period)
        loyer = simulation.calculate('loyer', period)
        invalide_holder = simulation.compute('invalide', period)
        enfant_handicape = self.any_by_roles(invalide_holder, roles = ENFS)
        P = simulation.legislation_at(period.start).aides_locales.paris.paris_logement_familles

        result = (
            (
                (enfant_handicape * (br <= P.plafond_haut_3enf) + (nbenf >= 3) * (br <= P.plafond_bas_3enf)) *
                (P.montant_haut_3enf + P.montant_haut_enf_sup * max_(nbenf - 3, 0))
            ) +
            (
                ((nbenf >= 3) * (br <= P.plafond_haut_3enf) * (br > P.plafond_bas_3enf)) *
                (P.montant_bas_3enf + P.montant_bas_enf_sup * max_(nbenf - 3, 0))
            ) +
            (
                ((nbenf == 2) * (br <= P.plafond_2enf)) *
                P.montant_2enf
            )
        )

        result = elig * result
        result = min_(result, loyer)

        return period, result
