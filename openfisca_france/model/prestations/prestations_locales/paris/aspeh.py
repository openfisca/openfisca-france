# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select)

from ....base import *  # noqa analysis:ignore

# Allocation de soutien aux parents d’enfants handicapés

class paris_logement_aspeh(Variable):
    column = FloatCol
    label = u"Famille qui est eligible à l'Allocation de soutien aux parents d’enfants handicapés"
    entity_class = Familles

    def function(self, simulation, period):
        plafond_aspeh = simulation.legislation_at(period.start).paris.aspeh.plafond_aspeh
        aide_aspeh = simulation.legislation_at(period.start).paris.aspeh.aide_aspeh

        parisien = simulation.calculate('parisien', period)
        enfant_handicape = simulation.calculate('paris_enfant_handicape', period)
        enfant = self.any_by_roles(enfant_handicape)
        ressources_mensuelles_famille = simulation.calculate('paris_base_ressources', period)

        result = (select([ressources_mensuelles_famille <= plafond_aspeh, ressources_mensuelles_famille > plafond_aspeh],
            [aide_aspeh, 0])) * parisien * enfant
        return period, result
