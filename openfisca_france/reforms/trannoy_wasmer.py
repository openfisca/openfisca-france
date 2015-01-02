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

import copy

import logging

from numpy import logical_not as not_, minimum as min_

from openfisca_core import reforms
from openfisca_core.accessors import law
from openfisca_core.columns import FloatCol
from openfisca_core.formulas import SimpleFormulaColumn


from openfisca_france import entities


log = logging.getLogger(__name__)

from openfisca_france.model.base import QUIMEN


PREF = QUIMEN['pref']


def _charges_deduc(cd1, cd2, charge_loyer):
    return cd1 + cd2 + charge_loyer


def build_reform_entity_class_by_symbol():

    reform_entity_class_by_symbol = entities.entity_class_by_symbol.copy()
    foyers_fiscaux_class = reform_entity_class_by_symbol['foy']

    class charge_loyer(SimpleFormulaColumn):
        column = FloatCol
        entity_class = foyers_fiscaux_class
        label = u"Charge déductible pour paiement d'un loyer"

        def function(self, loyer_holder, nbptr, charge_loyer = law.charge_loyer):
            loyer = self.cast_from_entity_to_role(loyer_holder, role = PREF)
            loyer = self.sum_by_entity(loyer)

            plaf = charge_loyer.plaf
            plaf_nbp = charge_loyer.plaf_nbp
            plafond = plaf * (not_(plaf_nbp) + plaf * nbptr * plaf_nbp)
            return 12 * charge_loyer.active * min_(loyer / 12, plafond)

        def get_output_period(self, period):
            return period.start.offset('first-of', 'year').period('year')

    # update column_by_name
    reform_column_by_name = foyers_fiscaux_class.column_by_name.copy()
    function_by_column_name = dict(
        charges_deduc = _charges_deduc,
        )

    for name, function in function_by_column_name.iteritems():
        column = foyers_fiscaux_class.column_by_name[name]
        reform_column = reforms.clone_simple_formula_column_with_new_function(column, function)
        reform_column_by_name[name] = reform_column

    reform_column_by_name['charge_loyer'] = charge_loyer

    class ReformFoyersFiscaux(foyers_fiscaux_class):
        column_by_name = reform_column_by_name

    reform_entity_class_by_symbol['foy'] = ReformFoyersFiscaux

    return reform_entity_class_by_symbol


def build_new_legislation_nodes():
    return {
        "charge_loyer": {
            "@type": "Node",
            "description": "Charge de loyer",
            "children": {
                "active": {
                    "@type": "Parameter",
                    "description": "Activation de la charge",
                    "format": "bool",
                    "values": [{'start': u'2002-01-01', 'stop': '2013-12-31', 'value': 1}],
                    },
                "plaf": {
                    "@type": "Parameter",
                    "description": 'Plafond mensuel',
                    "format": 'integer',
                    "unit": 'currency',
                    "values": [{'start': '2002-01-01', 'stop': '2013-12-31', 'value': 1000}],
                    },
                "plaf_nbp": {
                    "@type": "Parameter",
                    "description": 'Ajuster le plafond au nombre de part',
                    "format": 'bool',
                    "values": [{'start': '2002-01-01', 'stop': '2013-12-31', 'value': 0}],
                    },
                },
            }
        }


def build_reform(tax_benefit_system):

    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)

    reform_legislation_json['children'].update(build_new_legislation_nodes())

    to_entity_class_by_key_plural = lambda entity_class_by_symbol: {
        entity_class.key_plural: entity_class
        for symbol, entity_class in entity_class_by_symbol.iteritems()
        }

    reform = reforms.Reform(
        entity_class_by_key_plural = to_entity_class_by_key_plural(build_reform_entity_class_by_symbol()),
        legislation_json = reform_legislation_json,
        name = u'Loyer comme charge déductible (Trannoy-Wasmer)',
        reference = tax_benefit_system,
        )
    return reform
