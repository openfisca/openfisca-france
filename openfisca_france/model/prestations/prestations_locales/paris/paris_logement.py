# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select)

from ....base import *  # noqa analysis:ignore

class paris_logement(Variable):
	column=FloatCol
	label=u"Paris Logement"
	entity_class=Familles

	def function(self,simulation,period):
		return period, 0


class personnes_agees(Variable):
	column=BoolCol
	label=u"Personne âgée"
	entity_class=Individus

	def function(self,simulation,period):
		age = simulation.calculate('age',period)
		condition_age = (age>=65)
		return period, condition_age

class personnes_handicap_paris(Variable):
	column=BoolCol
	label=u"Personne qui possède l'AAH"
	entity_class=Individus

	def function(self,simulation,period):
		aah=simulation.calculate('aah',period)
		condition_aah = aah>0
		return period,condition_aah

class parisien(Variable):
        column = BoolCol
        entity_class = Familles
        label = u"Résidant à Paris au moins 3 ans dans les 5 dernières années"

class paris_logement_elig(Variable):
	column=BoolCol
	label=u"Personne qui est eligible"
	entity_class=Familles

	def function(self,simulation,period):
		parisien = simulation.calculate('parisien',period)
		personnes_agees=simulation.compute('personnes_agees',period)
		personnes_agees_famille = self.any_by_roles(personnes_agees)
		personne_handicap_individu=simulation.compute('personnes_handicap_paris',period)
		personne_handicap = self.any_by_roles(personne_handicap_individu)
		personnes_couple=simulation.calculate('concub',period)
		statut_occupation = simulation.calculate('statut_occupation',period)
		statut_occupation_elig =(
			(statut_occupation==3) +
			(statut_occupation==4) +
			(statut_occupation==5) +
			(statut_occupation==7)
			)
		charges_logement=simulation.calculate('condition_taux_effort',period)
		result=parisien*statut_occupation_elig*(personnes_agees_famille+personne_handicap)*charges_logement
		return period, result

class paris_nb_enfants(Variable):
	column=FloatCol
	label=u"Nombre d'enfant dans la famille"
	entity_class=Familles

	def function(self,simulation,period):
		nb_enfants=simulation.compute('plf_enfant',period)
		paris_nb_enfants=self.sum_by_entity(nb_enfants)
		return period, paris_nb_enfants

class condition_taux_effort(Variable):
	column=BoolCol
	label=u"Charges de Logement"
	entity_class=Familles

	def function(self,simulation,period):
		loyer=simulation.calculate('loyer',period)
		ressources_mensuelles=simulation.calculate('paris_logement_familles_br',period)
		condition_loyer=loyer>=(ressources_mensuelles*0.3)
		return period,condition_loyer