# -*- coding: utf-8 -*-

from __future__ import division

from numpy import logical_not as not_, logical_or as or_, round as round_

from openfisca_france.model.base import *  # noqa analysis:ignore

class echelon_bourse(Variable):
    entity = Individu
    column = IntCol
    label = u"Echelon de la bourse perçue (de 0 à 7)"

class boursier(Variable):
    column = BoolCol
    entity = Individu
    label = u"Élève ou étudiant boursier"
