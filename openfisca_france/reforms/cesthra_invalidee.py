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

import logging

from numpy import maximum as max_

from openfisca_core import formulas, reforms
from openfisca_france.model.impot_revenu import ir
from openfisca_france import entities


log = logging.getLogger(__name__)

from openfisca_france.model.base import QUIFOY
VOUS = QUIFOY['vous']


class cesthra(formulas.SimpleFormulaColumn):
    label = u"Contribution exceptionnelle de solidarité sur les très hauts revenus d'activité"
    # PLF 2013 (rejeté) : 'taxe à 75%'

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        sal_holder = simulation.calculate("sal", period)
        law_cesthra = simulation.legislation_at(period.start).cesthra
        sal = self.split_by_roles(sal_holder)

        cesthra = 0
        for rev in sal.itervalues():
            cesthra += max_(rev - law_cesthra.seuil, 0) * law_cesthra.taux
        return cesthra


class irpp(formulas.SimpleFormulaColumn):
    label = u"Impôt sur le revenu des personnes physiques (réformée pour intégrer la cesthra)"
    reference = ir.irpp

    def function(self, simulation, period):
        '''
        Montant après seuil de recouvrement (hors ppe)
        '''
        period = period.start.offset('first-of', 'month').period('year')
        iai = simulation.calculate('iai', period)
        credits_impot = simulation.calculate('credits_impot', period)
        cehr = simulation.calculate('cehr', period)
        cesthra = simulation.calculate('cesthra', period = period)
        P = simulation.legislation_at(period.start).ir.recouvrement

        pre_result = iai - credits_impot + cehr + cesthra
        return period, ((iai > P.seuil) *
            ((pre_result < P.min) * (pre_result > 0) * iai * 0 +
            ((pre_result <= 0) + (pre_result >= P.min)) * (- pre_result)) +
            (iai <= P.seuil) * ((pre_result < 0) * (-pre_result) +
            (pre_result >= 0) * 0 * iai))


# Reform legislation

reform_legislation_subtree = {
    "cesthra": {
        "@type": "Node",
        "description": "Contribution execptionnelle sur les très hauts revenus d'activité",
        "children": {
            "seuil": {
                "@type": "Parameter",
                "description": "Seuil",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2012-01-01', 'stop': u'2013-12-31', 'value': 1000000}],
                },
            "taux": {
                "@type": "Parameter",
                "description": "Taux",
                "format": "rate",
                "unit": "currency",
                "values": [{'start': u'2012-01-01', 'stop': u'2013-12-31', 'value': .75}],
                },
            },
        },
    }


def build_reform(tax_benefit_system):
    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)
    reform_legislation_json['children'].update(reform_legislation_subtree)

    # Update formulas
    reform_entity_class_by_key_plural = reforms.clone_entity_classes(entities.entity_class_by_key_plural)
    ReformFoyersFiscaux = reform_entity_class_by_key_plural['foyers_fiscaux']
    ReformFoyersFiscaux.column_by_name['irpp'] = irpp
    ReformFoyersFiscaux.column_by_name['cesthra'] = cesthra

    return reforms.Reform(
        entity_class_by_key_plural = reform_entity_class_by_key_plural,
        legislation_json = reform_legislation_json,
        name = u"Contribution execptionnelle sur les très hauts revenus d'activité (invalidée par le CC)",
        reference = tax_benefit_system,
        )
