# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select)

from ....base import *  # noqa analysis:ignore

# Paris forfait familles

class paris_forfait_famille(Variable):
    column = FloatCol
    label = u"Famille qui est eligible à l'aide paris forfait famille "
    entity_class = Familles

    def function(self, simulation, period):
        premier_plafond = simulation.legislation_at(period.start).paris.paris_forfait_famille.premier_plafond
        deuxieme_plafond = simulation.legislation_at(period.start).paris.paris_forfait_famille.deuxieme_plafond
        aide_1er_plafond = simulation.legislation_at(period.start).paris.paris_forfait_famille.aide_1er_plafond
        aide_2eme_plafond = simulation.legislation_at(period.start).paris.paris_forfait_famille.aide_2eme_plafond

        nb_enfants = simulation.calculate('paris_nb_enfants', period)
        parisien = simulation.calculate('parisien', period)
        ressources_mensuelles_famille = simulation.calculate('paris_base_ressources', period)
        montant_aide = select([(ressources_mensuelles_famille <= premier_plafond),
            (ressources_mensuelles_famille <= deuxieme_plafond)], [aide_1er_plafond, aide_2eme_plafond])
        result = (select([(nb_enfants >= 3), (nb_enfants < 3)], [montant_aide, 0])) * parisien
        return period, result
