# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select, where)

from ....base import *  # noqa analysis:ignore

class paris_energie_famille(Variable):
    column = FloatCol
    label = u"L'aide Paris Energie Famille"
    entity_class = Familles

    def function(self, simulation, period):

        result = 1

        return period, result
