# -*- coding: utf-8 -*-

from ..model.base import *


def modify_parameters(parameters):
    parameters.cotsoc.gen.smic_h_b.update(period = period(2013), value = 9)
    return parameters


class smic_h_b_9_euros(Reform):
    name = "Réforme pour simulation ACOSS SMIC horaire brut fixe à 9 euros"

    def apply(self):
        self.modify_parameters(modifier_function = modify_parameters)
