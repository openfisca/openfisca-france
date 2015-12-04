# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_)

from ...base import *  # noqa analysis:ignore

class tutorial(Variable):
	column =FloatCol
	label = u"Tutorial"
	entity_class =Familles

	def function(self, simulation, period):
		age=simulation.calculate('age',period)
		salaire=simulation.calculate_add('salaire_net',period.last_3_months)
		habitant_paris = simulation.calculate('habitant_paris',period)
		eligibilite = (age >= 18) * (age <=25)*(salaire<=3000)*(habitant_paris)
		return period, eligibilite * 1000

class habitant_paris(Variable):
	column =BoolCol
	label = u"Habitant de paris"
	entity_class =Familles
