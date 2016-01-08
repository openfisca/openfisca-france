# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select, where)

from ....base import *  # noqa analysis:ignore

class paris_complement_sante(Variable):
    column = FloatCol
    label = u"L'aide Paris Energie Famille"
    entity_class = Familles

    def function(self, simulation, period):

        result = 1

        return period, result


class paris_complement_sante_i(Variable):
    column = FloatCol
    label = u"Ressources Individuelles"
    entity_class = Individus

    def function(self, simulation, period):
        paris_base_ressources_commun_i = simulation.calculate('paris_base_ressources_commun_i', period)
        aah = simulation.calculate('aah')

        ressources_demandeur = paris_base_ressources_commun_i + aah

        return period, ressources_demandeur
