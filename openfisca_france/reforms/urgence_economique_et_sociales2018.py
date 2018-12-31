# -*- coding: utf-8 -*-

from __future__ import division
from ..model.base import *


class ressources_urgence(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH

    def formula_2013_01_01(famille, period, parameters):
        ppa = famille('ppa_versee', period)
        salaires_i = famille.members('salaire_net', period)
        salaires = famille.sum(salaires_i)
        return ppa + salaires


class urgence_economique_et_sociales2018(Reform):
    name = u"Hausse du pouvoir d'achat de 100 en janvier 2019"

    def apply(self):
        self.add_variable(ressources_urgence)
