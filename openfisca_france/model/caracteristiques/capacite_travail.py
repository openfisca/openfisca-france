# -*- coding: utf-8 -*-

from openfisca_france.model.base import *


class taux_capacite_travail(Variable):
    value_type = float
    default_value = 1.0
    entity = Individu
    label = u"Taux de capacité de travail, appréciée par la commission des droits et de l'autonomie des personnes handicapées (CDAPH)"
    definition_period = MONTH


class taux_incapacite(Variable):
    value_type = float
    entity = Individu
    label = u"Taux d'incapacité"
    definition_period = MONTH