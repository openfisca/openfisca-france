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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# TODO switch to to average tax rates

from __future__ import division

from numpy import logical_not as not_, minimum as min_
from openfisca_core import columns, formulas, reforms

from .. import entities
from ..model.base import PREF
from ..model.prelevements_obligatoires.impot_revenu import charges_deductibles


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'trannoy_wasmer',
        name = u'Loyer comme charge déductible (Trannoy-Wasmer)',
        reference = tax_benefit_system,
        )

    @Reform.formula
    class charges_deduc(formulas.SimpleFormulaColumn):
        label = u"Charge déductibles intégrant la charge pour loyer (Trannoy-Wasmer)"
        reference = charges_deductibles.charges_deduc

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'year').period('year')
            cd1 = simulation.calculate('cd1', period)
            cd2 = simulation.calculate('cd2', period)
            charge_loyer = simulation.calculate('charge_loyer', period)

            return period, cd1 + cd2 + charge_loyer

    @Reform.formula
    class charge_loyer(formulas.SimpleFormulaColumn):
        column = columns.FloatCol
        entity_class = entities.FoyersFiscaux
        label = u"Charge déductible pour paiement d'un loyer"

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'year').period('year')
            loyer_holder = simulation.calculate('loyer', period)
            nbptr = simulation.calculate('nbptr', period)
            loyer = self.cast_from_entity_to_role(loyer_holder, entity = "menage", role = PREF)
            loyer = self.sum_by_entity(loyer)
            charge_loyer = simulation.legislation_at(period.start).charge_loyer

            plaf = charge_loyer.plaf
            plaf_nbp = charge_loyer.plaf_nbp
            plafond = plaf * (not_(plaf_nbp) + plaf * nbptr * plaf_nbp)

            return period, 12 * min_(loyer / 12, plafond)

    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "Charge de loyer",
        "children": {
            "active": {
                "@type": "Parameter",
                "description": u"Activation de la charge",
                "format": "boolean",
                "values": [{'start': u'2002-01-01', 'stop': '2013-12-31', 'value': 1}],
                },
            "plaf": {
                "@type": "Parameter",
                "description": u'Plafond mensuel',
                "format": 'integer',
                "unit": 'currency',
                "values": [{'start': '2002-01-01', 'stop': '2013-12-31', 'value': 1000}],
                },
            "plaf_nbp": {
                "@type": "Parameter",
                "description": u'Ajuster le plafond au nombre de part',
                "format": 'boolean',
                "values": [{'start': '2002-01-01', 'stop': '2013-12-31', 'value': 0}],
                },
            },
        }
    reference_legislation_json_copy['children']['charge_loyer'] = reform_legislation_subtree
    return reference_legislation_json_copy
