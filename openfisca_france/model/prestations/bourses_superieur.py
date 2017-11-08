# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france.model.base import *  # noqa analysis:ignore

class echelon_bourse(Variable):
    entity = Individu
    column = IntCol
    label = u"Echelon de la bourse perçue (de 0 à 7)"
    definition_period = MONTH


class boursier(Variable):
    column = BoolCol
    entity = Individu
    label = u"Élève ou étudiant boursier"
    definition_period = MONTH
