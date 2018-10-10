# -*- coding: utf-8 -*-

from __future__ import division

import os

from ..model.base import *


dir_path = os.path.join(os.path.dirname(__file__), 'parameters')


def modify_parameters(parameters):
    reform_year = 2013
    reform_period = period(reform_year)

    file_path = os.path.join(dir_path, 'plf2015.yaml')
    reform_parameters_subtree = load_parameter_file(name='plf2015', file_path=file_path)
    parameters.add_child('plf2015', reform_parameters_subtree)

    parameters.impot_revenu.bareme[1].rate.update(period=reform_period, value=0)
    parameters.impot_revenu.bareme[2].threshold.update(period=reform_period, value=9690)

    return parameters


class decote(Variable):
    label = u"Décote IR 2015 appliquée sur IR 2014 (revenus 2013)"
    definition_period = YEAR

    def formula_2013_01_01(foyer_fiscal, period, parameters):
        ir_plaf_qf = foyer_fiscal('ir_plaf_qf', period)
        nb_adult = foyer_fiscal('nb_adult', period)
        plf = parameters(period).plf2015

        decote_celib = (ir_plaf_qf < plf.seuil_celib) * (plf.seuil_celib - ir_plaf_qf)
        decote_couple = (ir_plaf_qf < plf.seuil_couple) * (plf.seuil_couple - ir_plaf_qf)
        return (nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple


class plf2015(Reform):
    name = u"Projet de Loi de Finances 2015 appliquée aux revenus 2013"

    def apply(self):
        self.update_variable(decote)
        self.modify_parameters(modifier_function = modify_parameters)
