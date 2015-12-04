# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_)

from ...base import *  # noqa analysis:ignore

class tutorial(Variable):
    column =FloatCol
    label = u"Tutorial"
    entity_class =Familles

    def function(self, simulation, period):
        law = simulation.legislation_at(period.start)
        smic_horaire = law.cotsoc.gen.smic_h_b
        smic_heure_mensuel = law.cotsoc.gen.nb_heure_travail_mensuel
        smic_mensuel = smic_horaire*smic_heure_mensuel

        age=simulation.calculate('age',period)
        salaire=simulation.calculate_add('salaire_net',period.last_3_months)/3
        habitant_paris = simulation.calculate('habitant_paris',period)
        eligibilite = (age >= 18) * (age <=25)*(salaire<=smic_mensuel)*(habitant_paris)
        return period, eligibilite * 1000

class habitant_paris(Variable):
    column =BoolCol
    label = u"Habitant de paris"
    entity_class =Familles
