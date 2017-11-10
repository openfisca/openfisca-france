# -*- coding: utf-8 -*-

from openfisca_core.reforms import Reform, update_legislation
from openfisca_core import periods


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_json = update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ['children', 'cotsoc', 'children', 'gen', 'children', 'smic_h_b', 'values'],
        period = periods.period(2013),
        value = 9,
        )
    return reform_legislation_json


class smic_h_b_9_euros(Reform):
    name = u"Réforme pour simulation ACOSS SMIC horaire brut fixe à 9 euros"

    def apply(self):
        self.modify_legislation_json(modifier_function = modify_legislation_json)

