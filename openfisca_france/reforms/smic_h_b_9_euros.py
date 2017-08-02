# -*- coding: utf-8 -*-

from openfisca_core.reforms import Reform
from openfisca_core import periods


def modify_legislation_json(reference_legislation_json_copy):
    reference_legislation_json_copy.cotsoc.gen.smic_h_b.update(period = periods.period(2013), value = 9)
    return reference_legislation_json_copy


class smic_h_b_9_euros(Reform):
    name = u"Réforme pour simulation ACOSS SMIC horaire brut fixe à 9 euros"

    def apply(self):
        self.modify_legislation_json(modifier_function = modify_legislation_json)

