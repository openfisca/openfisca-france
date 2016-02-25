# -*- coding: utf-8 -*-

from __future__ import division

from ...base import *  # noqa analysis:ignore

from numpy import maximum as max_, round as round_, minimum as min_, logical_not as not_, where, select

class ppa_eligibilite(Variable):
    column = BoolCol
    entity_class = Familles
    label = u"Eligibilité à la PPA pour un mois"

    def function(self, simulation, period):
        period = period.this_month
        P = simulation.legislation_at(period.start)
        age_min = P.minim.ppa.age_min
        condition_age_individus = simulation.calculate('age', period) >= age_min
        condition_age = self.any_by_roles(condition_age_individus)
        elig = condition_age

        return period, elig

