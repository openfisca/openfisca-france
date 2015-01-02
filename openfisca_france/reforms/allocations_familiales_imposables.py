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


from __future__ import division

import copy

from numpy import maximum as max_
import logging

from openfisca_core import formulas, reforms
from openfisca_core.columns import FloatCol
from openfisca_core.accessors import law
from openfisca_france import entities


log = logging.getLogger(__name__)

from openfisca_france.model.base import QUIFOY
VOUS = QUIFOY['vous']


def revenu_brut_global(self, allocations_familiales_imposables, rev_cat, deficit_ante, f6gh, nbic_impm_holder,
                       nacc_pvce_holder, cga = law.ir.rpns.cga_taux2):
    '''
    Revenu brut global
    '''
    # (Total 17)
    # sans les revenus au quotient
    nacc_pvce = self.sum_by_entity(nacc_pvce_holder)
    return max_(
        0,
        allocations_familiales_imposables + rev_cat + f6gh +
        (self.sum_by_entity(nbic_impm_holder) + nacc_pvce) * (1 + cga) - deficit_ante
        )


def revenu_fiscal_de_reference(self, rni, allocations_familiales_imposables, f3va_holder, f3vi_holder, rfr_cd, rfr_rvcm,
                               rpns_exon_holder, rpns_pvce_holder, rev_cap_lib, f3vz, microentreprise):
    '''
    Revenu fiscal de référence
    f3vg -> rev_cat_pv -> ... -> rni
    '''
    f3va = self.sum_by_entity(f3va_holder)
    f3vi = self.sum_by_entity(f3vi_holder)
    rpns_exon = self.sum_by_entity(rpns_exon_holder)
    rpns_pvce = self.sum_by_entity(rpns_pvce_holder)
    return (
        max_(0, rni - allocations_familiales_imposables) +
        rfr_cd + rfr_rvcm + rev_cap_lib + f3vi + rpns_exon + rpns_pvce + f3va + f3vz + microentreprise
        )


def build_new_legislation_nodes():
    return {
        "allocations_familiales_imposables": {
            "@type": "Node",
            "description": "Intégration au revenu imposable des allocations familiales",
            "children": {
                "imposition": {
                    "@type": "Parameter",
                    "description": "Indicatrice d'imposition",
                    "format": "boolean",
                    "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': True}],
                    },
                },
            },
        }


def build_reform_entity_class_by_symbol():

    reform_entity_class_by_symbol = entities.entity_class_by_symbol.copy()
    foyers_fiscaux_class = reform_entity_class_by_symbol['foy']

    class allocations_familiales_imposables(formulas.SimpleFormulaColumn):
        column = FloatCol
        entity_class = foyers_fiscaux_class
        label = u"Allocations familiales imposables"

        def function(self, af_holder, imposition = law.allocations_familiales_imposables.imposition):
            '''
            Allocations familiales imposables
            '''
            af = self.cast_from_entity_to_role(af_holder, role = VOUS)
            af = self.sum_by_entity(af)
            return af * imposition

        def get_output_period(self, period):
            return period.start.offset('first-of', 'month').period('year')

    # update column_by_name
    reform_column_by_name = foyers_fiscaux_class.column_by_name.copy()
    function_by_column_name = dict(
        rbg = revenu_brut_global,
        rfr = revenu_fiscal_de_reference,
        )

    for name, function in function_by_column_name.iteritems():
        column = foyers_fiscaux_class.column_by_name[name]
        reform_column = reforms.replace_simple_formula_column_function(column, function)
        reform_column_by_name[name] = reform_column

    reform_column_by_name['allocations_familiales_imposables'] = allocations_familiales_imposables

    class ReformFoyersFiscaux(foyers_fiscaux_class):
        column_by_name = reform_column_by_name

    reform_entity_class_by_symbol['foy'] = ReformFoyersFiscaux

    return reform_entity_class_by_symbol


def build_reform(tax_benefit_system):
    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)
    reform_legislation_json['children'].update(build_new_legislation_nodes())
    to_entity_class_by_key_plural = lambda entity_class_by_symbol: {
        entity_class.key_plural: entity_class
        for symbol, entity_class in entity_class_by_symbol.iteritems()
        }
    return reforms.Reform(
        entity_class_by_key_plural = to_entity_class_by_key_plural(build_reform_entity_class_by_symbol()),
        legislation_json = reform_legislation_json,
        name = u'Allocations familiales imposables',
        reference = tax_benefit_system,
        )
