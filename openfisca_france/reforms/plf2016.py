# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import formulas, reforms
from ..model.base import *
from ..model.prelevements_obligatoires.impot_revenu import ir


# What if the reform was applied the year before it should

def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'plf2016',
        name = u'Projet de Loi de Finances 2016 appliquée aux revenus 2014',
        reference = tax_benefit_system,
        )

    @Reform.formula
    class decote(formulas.DatedFormulaColumn):
        label = u"Décote IR 2016 appliquée en 2015 sur revenus 2014"
        reference = ir.decote

        @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
        def function_2014(self, simulation, period):
            period = period.start.offset('first-of', 'year').period('year')
            ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
            nb_adult = simulation.calculate('nb_adult', period)
            plf = simulation.legislation_at(period.start).plf2016

            decote_celib = (ir_plaf_qf < plf.decote_seuil_celib) * (plf.decote_seuil_celib - .75 * ir_plaf_qf)
            decote_couple = (ir_plaf_qf < plf.decote_seuil_couple) * (plf.decote_seuil_couple - .75 * ir_plaf_qf)
            return period, (nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple

    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "PLF 2016 sur revenus 2014",
        "children": {
            "decote_seuil_celib": {
                "@type": "Parameter",
                "description": "Seuil de la décôte pour un célibataire",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 1165}],
                },
            "decote_seuil_couple": {
                "@type": "Parameter",
                "description": "Seuil de la décôte pour un couple",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 1192}],
                },
            },
        }
    reference_legislation_json_copy['children']['plf2016'] = reform_legislation_subtree
    return reference_legislation_json_copy


# Counterfactual ie business as usual

def build_counterfactual_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'plf2016_counterfactual',
        name = u'Contrefactuel du PLF 2016 sur les revenus 2015',
        reference = tax_benefit_system,
        )

    @Reform.formula
    class decote(formulas.DatedFormulaColumn):
        label = u"Décote IR 2015 appliquée sur revenus 2015 (contrefactuel)"
        reference = ir.decote

        @dated_function(start = date(2015, 1, 1))
        def function_2015__(self, simulation, period):
            period = period.start.offset('first-of', 'year').period('year')
            ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
            nb_adult = simulation.calculate('nb_adult', period)
            plf2016 = simulation.legislation_at(period.start).plf2016_conterfactual
            decote_seuil_celib = plf2016.decote_seuil_celib
            decote_seuil_couple = plf2016.decote_seuil_couple

            decote_celib = (ir_plaf_qf < decote_seuil_celib) * (decote_seuil_celib - ir_plaf_qf)
            decote_couple = (ir_plaf_qf < decote_seuil_couple) * (decote_seuil_couple - ir_plaf_qf)

            return period, (nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple

    reform = Reform()
    reform.modify_legislation_json(modifier_function = counterfactual_modify_legislation_json)
    return reform


# TODO inflater les paramètres de la décote
# Et vérifier le barème de l'IR
def counterfactual_modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "PLF 2016 sur revenus 2015",
        "children": {
            "decote_seuil_celib": {
                "@type": "Parameter",
                "description": "Seuil de la décôte pour un célibataire",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': 1135}],
                },
            "decote_seuil_couple": {
                "@type": "Parameter",
                "description": "Seuil de la décôte pour un couple",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': 1870}],
                },
            },
        }
    reference_legislation_json_copy['children']['plf2016_conterfactual'] = reform_legislation_subtree
    return reference_legislation_json_copy
