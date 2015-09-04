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

from openfisca_core import formulas, periods, reforms

from ..model.prelevements_obligatoires.impot_revenu import ir


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'plf2015',
        name = u'Projet de Loi de Finances 2015',
        reference = tax_benefit_system,
        )

    @Reform.formula
    class decote(formulas.SimpleFormulaColumn):
        label = u"Nouvelle décote 2015"
        reference = ir.decote

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'year').period('year')
            ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
            nb_adult = simulation.calculate('nb_adult', period)
            plf = simulation.legislation_at(period.start).plf2015

            decote_celib = (ir_plaf_qf < plf.decote_seuil_celib) * (plf.decote_seuil_celib - ir_plaf_qf)
            decote_couple = (ir_plaf_qf < plf.decote_seuil_couple) * (plf.decote_seuil_couple - ir_plaf_qf)
            return period, (nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple

    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "PLF 2015",
        "children": {
            "decote_seuil_celib": {
                "@type": "Parameter",
                "description": "Seuil de la décôte pour un célibataire",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2013-01-01', 'stop': u'2014-12-31', 'value': 1135}],
                },
            "decote_seuil_couple": {
                "@type": "Parameter",
                "description": "Seuil de la décôte pour un couple",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2013-01-01', 'stop': u'2014-12-31', 'value': 1870}],
                },
            },
        }
    reform_year = 2014
    reform_period = periods.period('year', reform_year)
    # FIXME update_legislation is deprecated.
    reference_legislation_json_copy = reforms.update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'ir', 'children', 'bareme', 'brackets', 1, 'rate'),
        period = reform_period,
        value = 0,
        )
    # FIXME update_legislation is deprecated.
    reference_legislation_json_copy = reforms.update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'ir', 'children', 'bareme', 'brackets', 2, 'threshold'),
        period = reform_period,
        value = 9690,
        )
    reference_legislation_json_copy['children']['plf2015'] = reform_legislation_subtree
    return reference_legislation_json_copy
