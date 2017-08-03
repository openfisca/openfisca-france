# -*- coding: utf-8 -*-

from __future__ import division

from datetime import date
import os

from openfisca_core import periods, legislations
from openfisca_core.reforms import Reform
from ..model.base import *


dir_path = os.path.dirname(__file__)


def modify_legislation(reference_legislation_copy):
    reform_year = 2013
    reform_period = periods.period(reform_year)

    file_path = os.path.join(dir_path, 'plf2015.yaml')
    reform_legislation_subtree = legislations.load_file(name='plf2015', file_path=file_path)
    reference_legislation_copy.add_child('plf2015', reform_legislation_subtree)

    reference_legislation_copy.impot_revenu.bareme[1].rate.update(period=reform_period, value=0)
    reference_legislation_copy.impot_revenu.bareme[2].threshold.update(period=reform_period, value=9690)

    return reference_legislation_copy


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
        self.modify_legislation(modifier_function = modify_legislation)
