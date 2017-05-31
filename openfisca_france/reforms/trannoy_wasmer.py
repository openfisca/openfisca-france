# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core.reforms import Reform

from ..model.prelevements_obligatoires.impot_revenu import charges_deductibles
from ..model.base import *

def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "Charge de loyer",
        "children": {
            "active": {
                "@type": "Parameter",
                "description": u"Activation de la charge",
                "format": "boolean",
                "values": [
                    {'start': u'2014-01-01', },
                    {'start': u'2002-01-01', 'value': 1},
                    ],
                },
            "plaf": {
                "@type": "Parameter",
                "description": u'Plafond mensuel',
                "format": 'integer',
                "unit": 'currency',
                "values": [
                    {'start': '2014-01-01', },
                    {'start': '2002-01-01', 'value': 1000},
                    ],
                },
            "plaf_nbp": {
                "@type": "Parameter",
                "description": u'Ajuster le plafond au nombre de part',
                "format": 'boolean',
                "values": [
                    {'start': '2014-01-01', },
                    {'start': '2002-01-01', 'value': 0},
                    ],
                },
            },
        }
    reference_legislation_json_copy['children']['charge_loyer'] = reform_legislation_subtree
    return reference_legislation_json_copy

class charges_deduc(Variable):
    label = u"Charge déductibles intégrant la charge pour loyer (Trannoy-Wasmer)"
    definition_period = YEAR

    def formula(self, simulation, period):
        cd1 = simulation.calculate('cd1', period)
        cd2 = simulation.calculate('cd2', period)
        charge_loyer = simulation.calculate('charge_loyer', period)

        return cd1 + cd2 + charge_loyer

class charge_loyer(Variable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Charge déductible pour paiement d'un loyer"
    definition_period = YEAR

    def formula(self, simulation, period):
        nbptr = simulation.calculate('nbptr', period)

        loyer = simulation.foyer_fiscal.declarant_principal.menage('loyer', period, options = [ADD])

        charge_loyer = simulation.legislation_at(period.start).charge_loyer

        plaf = charge_loyer.plaf
        plaf_nbp = charge_loyer.plaf_nbp
        plafond = plaf * (not_(plaf_nbp) + plaf * nbptr * plaf_nbp)

        return 12 * min_(loyer / 12, plafond)


class trannoy_wasmer(Reform):
    name = u'Loyer comme charge déductible (Trannoy-Wasmer)'

    def apply(self):
        self.update_variable(charges_deduc)
        self.add_variable(charge_loyer)
        self.modify_legislation_json(modifier_function = modify_legislation_json)
