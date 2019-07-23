# -*- coding: utf-8 -*-

from openfisca_france.model.base import *


class echelon_bourse(Variable):
    entity = Individu
    value_type = int
    label = "Echelon de la bourse perçue (de 0 à 7)"
    definition_period = MONTH


class boursier(Variable):
    value_type = bool
    entity = Individu
    label = "Élève ou étudiant boursier"
    definition_period = MONTH
