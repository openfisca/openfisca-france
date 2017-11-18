# -*- coding: utf-8 -*-

from __future__ import division

from datetime import date
import os

from ..model.base import *


dir_path = os.path.join(os.path.dirname(__file__), 'parameters')


def modify_parameters(parameters):
    reform_year = 2017
    reform_period = period(reform_year)
    print(reform_period)

    # file_path = os.path.join(dir_path, 'plf2018.yaml')
    # reform_parameters_subtree = load_parameter_file(name='plf2018', file_path=file_path)
    # parameters.add_child('plf2018', reform_parameters_subtree)
    parameters.prelevements_sociaux.contributions.csg.activite.deductible.taux.update(period=reform_period, value=0.068)
    parameters.prelevements_sociaux.contributions.csg.retraite.deductible.taux_plein.update(period=reform_period, value=0.068)
    parameters.prestations.minima_sociaux.aspa.montant_annuel_seul.update(period=reform_period, value=(9638.42+100*12))
    parameters.prestations.minima_sociaux.aspa.montant_annuel_couple.update(period=reform_period, value=(14963.65+100*12))
    parameters.prestations.minima_sociaux.rsa.montant_de_base_du_rsa.update(period=reform_period, value=(545.48+20))
    # parameters.cotsoc.sal.commun.maladie[0].rate.update(period=reform_period, value=0.0)
    # parameters.prelevements_sociaux.cotisations_sociales.chomage.salarie[0].rate.update(period=reform_period, value=0.0)

    return parameters

class plf2018(Reform):
    name = u"Projet de Loi de Finances 2018 appliquée aux revenus 2018"

    def apply(self):
        self.modify_parameters(modifier_function = modify_parameters)
