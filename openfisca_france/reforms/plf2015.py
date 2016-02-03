# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import periods, reforms
from ..model.base import *
from ..model.prelevements_obligatoires.impot_revenu import ir


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'plf2015',
        name = u'Projet de Loi de Finances 2015 appliquée aux revenus 2013',
        reference = tax_benefit_system,
        )

    class decote(Reform.DatedVariable):
        label = u"Décote IR 2015 appliquée sur IR 2014 (revenus 2013)"
        reference = ir.decote

        @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
        def function_2013(self, simulation, period):
            period = period.this_year
            ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
            nb_adult = simulation.calculate('nb_adult', period)
            plf = simulation.legislation_at(period.start).plf2015

            decote_celib = (ir_plaf_qf < plf.seuil_celib) * (plf.seuil_celib - ir_plaf_qf)
            decote_couple = (ir_plaf_qf < plf.seuil_couple) * (plf.seuil_couple - ir_plaf_qf)
            return period, (nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple

    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "PLF 2015 sur revenus 2013 (Décote)",
        "children": {
            "seuil_celib": {
                "@type": "Parameter",
                "description": "Seuil de la décote pour un célibataire",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 1135}],
                },
            "seuil_couple": {
                "@type": "Parameter",
                "description": "Seuil de la décote pour un couple",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2013-01-01', 'stop': u'2013-12-31', 'value': 1870}],
                },
            },
        }
    reform_year = 2013
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
