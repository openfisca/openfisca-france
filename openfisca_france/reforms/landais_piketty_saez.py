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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# TODO switch to to average tax rates

from __future__ import division

import copy

from numpy import maximum as max_
import logging

from openfisca_core import formulas, reforms
from openfisca_core.columns import FloatCol
from openfisca_core.accessors import law
from openfisca_france import entities


log = logging.getLogger(__name__)

from openfisca_france.model.base import QUIFAM, QUIFOY

VOUS = QUIFOY['vous']
CHEF = QUIFAM['chef']


############################################################################
# # Impôt Landais, Piketty, Saez
############################################################################


def revenu_disponible(self, rev_trav_holder, pen_holder, rev_cap_holder, impot_revenu_lps_holder,
                      psoc_holder):
    '''
    Revenu disponible - ménage
    'men'
    '''
    impot_revenu_lps = self.sum_by_entity(impot_revenu_lps_holder)
    pen = self.sum_by_entity(pen_holder)
    psoc = self.cast_from_entity_to_role(psoc_holder, role = CHEF)
    psoc = self.sum_by_entity(psoc)
    rev_cap = self.sum_by_entity(rev_cap_holder)
    rev_trav = self.sum_by_entity(rev_trav_holder)

    return rev_trav + pen + rev_cap + impot_revenu_lps + psoc


def build_new_legislation_nodes():
    return {
        "landais_piketty_saez": {
            "@type": "Node",
            "description": "Impôt à base large proposé par Landais, Piketty et Saez",
            "children": {
                "bareme": {
                    "@type": "Scale",
                    "unit": "currency",
                    "description": "Barème de l'impôt",
                    "rates_kind": "average",
                    "brackets": [
                        {
                            "rate": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .02}],
                            "threshold": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 1100}],
                            },
                        {
                            "rate": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .1}],
                            "threshold": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 2200}],
                            },
                        {
                            "rate": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .13}],
                            "threshold": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 5000}],
                            },
                        {
                            "rate": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .25}],
                            "threshold": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 10000}],
                            },
                        {
                            "rate": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .5}],
                            "threshold": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 40000}],
                            },
                        {
                            "rate": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .6}],
                            "threshold": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 100000}],
                            },
                        ],
                    },
                "imposition": {
                    "@type": "Parameter",
                    "description": "Indicatrice d'imposition",
                    "format": "boolean",
                    "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': True}],
                    },
                "credit_enfant": {
                    "@type": "Parameter",
                    "description": u"Crédit d'impôt forfaitaire par enfant",
                    "format": "integer",
                    "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 0}],
                    },
                "reduc_enfant": {
                    "@type": "Parameter",
                    "description": u"Réduction d'impôt forfaitaire par enfant",
                    "format": "integer",
                    "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 0}],
                    },
                "abatt_enfant": {
                    "@type": "Parameter",
                    "description": u"Abattement forfaitaire sur le revenu par enfant",
                    "format": "integer",
                    "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 0}],
                    },
                "reduc_conj": {
                    "@type": "Parameter",
                    "description": u"Réduction d'impôt forfaitaire si conjoint",
                    "format": "integer",
                    "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 0}],
                    },
                "abatt_conj": {
                    "@type": "Parameter",
                    "description": u"Abattement forfaitaire sur le revenu si conjoint",
                    "format": "integer",
                    "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 0}],
                    },
                },
            },
        }


def build_reform_entity_class_by_symbol():

    reform_entity_class_by_symbol = entities.entity_class_by_symbol.copy()
    individus_class = reform_entity_class_by_symbol['ind']
    menages_class = reform_entity_class_by_symbol['men']

    class assiette_csg(formulas.SimpleFormulaColumn):
        column = FloatCol
        entity_class = individus_class
        label = u"Assiette de la CSG"

        def function(self, salbrut, chobrut, rstbrut, rev_cap_bar_holder, rev_cap_lib_holder):
            '''
            Assiette de la csg
            '''
            rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = VOUS)
            rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)
            return salbrut + chobrut + rstbrut + rev_cap_bar + rev_cap_lib

        def get_output_period(self, period):
            return period.start.offset('first-of', 'month').period('year')

    class impot_revenu_lps(formulas.SimpleFormulaColumn):
        column = FloatCol
        entity_class = individus_class
        label = u"Impôt individuel sur l'ensemble de l'assiette de la csg, comme proposé par Landais, Piketty et Saez"

        def function(self, assiette_csg, nbF_holder, nbH_holder, statmarit, lps = law.landais_piketty_saez):
            '''
            Impôt individuel sur l'ensemble de l'assiette de la csg, comme proposé par
            Landais, Piketty, Saez (2011)
            '''
            nbF = self.cast_from_entity_to_role(nbF_holder, role = VOUS)
            nbH = self.cast_from_entity_to_role(nbH_holder, role = VOUS)
            nbEnf = (nbF + nbH / 2)
            ae = nbEnf * lps.abatt_enfant
            re = nbEnf * lps.reduc_enfant
            ce = nbEnf * lps.credit_enfant
            couple = (statmarit == 1) | (statmarit == 5)
            ac = couple * lps.abatt_conj
            rc = couple * lps.reduc_conj
            return -max_(0, lps.bareme.calc(max_(assiette_csg - ae - ac, 0)) - re - rc) + ce

        def get_output_period(self, period):
            return period.start.offset('first-of', 'month').period('year')

    # update column_by_name
    reform_menages_column_by_name = menages_class.column_by_name.copy()
    function_by_column_name = dict(
        revdisp = revenu_disponible,
        )

    for name, function in function_by_column_name.iteritems():
        column = menages_class.column_by_name[name]
        reform_column = reforms.clone_simple_formula_column_with_new_function(column, function)
        reform_menages_column_by_name[name] = reform_column

    class ReformMenages(menages_class):
        column_by_name = reform_menages_column_by_name

    reform_entity_class_by_symbol['men'] = ReformMenages

    reform_individus_column_by_name = individus_class.column_by_name.copy()
    reform_individus_column_by_name['assiette_csg'] = assiette_csg
    reform_individus_column_by_name['impot_revenu_lps'] = impot_revenu_lps

    class ReformIndividus(individus_class):
        column_by_name = reform_individus_column_by_name
    reform_entity_class_by_symbol['ind'] = ReformIndividus

    return reform_entity_class_by_symbol


def build_reform(tax_benefit_system):
    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)
    reform_legislation_json['children'].update(build_new_legislation_nodes())
    # from openfisca_core import conv, legislations
    # conv.check(legislations.validate_legislation_json)(reform_legislation_json)
    to_entity_class_by_key_plural = lambda entity_class_by_symbol: {
        entity_class.key_plural: entity_class
        for symbol, entity_class in entity_class_by_symbol.iteritems()
        }
    return reforms.Reform(
        entity_class_by_key_plural = to_entity_class_by_key_plural(build_reform_entity_class_by_symbol()),
        legislation_json = reform_legislation_json,
        name = u'Landais Piketty Saez',
        reference = tax_benefit_system,
        )
