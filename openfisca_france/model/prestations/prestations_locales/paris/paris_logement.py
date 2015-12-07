# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select)

from ...base import *  # noqa analysis:ignore

class paris_logement(Variable):
	column=FloatCol
	label=u"Paris Logement"
	entity_class=Familles

	def function(self,simulation,period):


class personnes_agees(Variable):
	column=BoolCol
	label=u"Personne âgée"
	entity_class=Individus

	def function(self,simulation,period):
		age = simulation.calculate('age',period)
		condition_age = (age=>65)
		return period, condition_age

	
	
