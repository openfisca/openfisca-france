# -*- coding: utf-8 -*-

from __future__ import division
from datetime import date

from openfisca_core import periods
from openfisca_core.reforms import Reform, update_legislation
from ..model.base import *


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "type": "node",
        "description": u"PLF 2015 sur revenus 2013 (Décote)",
        "children": {
            "seuil_celib": {
                "type": "parameter",
                "description": u"Seuil de la décote pour un célibataire",
                "format": "integer",
                "unit": "currency",
                "values": [
                    {'start': u'2014-01-01', },
                    {'start': u'2013-01-01', 'value': 1135},
                    ],
                },
            "seuil_couple": {
                "type": "parameter",
                "description": u"Seuil de la décote pour un couple",
                "format": "integer",
                "unit": "currency",
                "values": [
                    {'start': u'2014-01-01', },
                    {'start': u'2013-01-01', 'value': 1870},
                    ],
                },
            },
        }
    reform_year = 2013
    reform_period = periods.period(reform_year)

    reference_legislation_json_copy = update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'impot_revenu', 'children', 'bareme', 'brackets', 1, 'rate'),
        period = reform_period,
        value = 0,
        )
    reference_legislation_json_copy = update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'impot_revenu', 'children', 'bareme', 'brackets', 2, 'threshold'),
        period = reform_period,
        value = 9690,
        )

    reference_legislation_json_copy['children']['plf2015'] = reform_legislation_subtree
    return reference_legislation_json_copy


class decote(Variable):
    label = u"Décote IR 2015 appliquée sur IR 2014 (revenus 2013)"
    definition_period = YEAR

    def formula_2013_01_01(self, simulation, period):
        ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
        nb_adult = simulation.calculate('nb_adult', period)
        plf = simulation.legislation_at(period.start).plf2015

        decote_celib = (ir_plaf_qf < plf.seuil_celib) * (plf.seuil_celib - ir_plaf_qf)
        decote_couple = (ir_plaf_qf < plf.seuil_couple) * (plf.seuil_couple - ir_plaf_qf)
        return (nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple


class plf2015(Reform):
    name = u"Projet de Loi de Finances 2015 appliquée aux revenus 2013"

    def apply(self):
        self.update_variable(decote)
        self.modify_legislation_json(modifier_function = modify_legislation_json)
