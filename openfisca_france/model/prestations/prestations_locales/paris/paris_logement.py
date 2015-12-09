# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select)

from ....base import *  # noqa analysis:ignore
#Critères relatifs à PL (PA et PH)
class paris_logement(Variable):
	column=FloatCol
	label=u"Paris Logement"
	entity_class=Familles

	def function(self,simulation,period):
		ressources_familiale=simulation.calculate('paris_logement_familles_br',period)
		personnes_couple=simulation.calculate('concub',period)
		paris_nb_enfants= simulation.compute('paris_nb_enfants',period)
		nb_enfants=self.sum_by_entity(paris_nb_enfants)
		plafond=select([(nb_enfants>=1),(nb_enfants<1)],[1600,1140])
		condition_ressource= ressources_familiale<=plafond
		result=select([(nb_enfants>0),(personnes_couple),(personnes_couple!=1)],[116,95,84])
		return period, result*condition_ressource


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

class paris_logement_elig(Variable):
	column=BoolCol
	label=u"Personne qui est eligible pour l'aide PL"
	entity_class=Familles

	def function(self,simulation,period):
		parisien = simulation.calculate('parisien',period)
		personnes_agees=simulation.compute('personnes_agees',period)
		personnes_agees_famille = self.any_by_roles(personnes_agees)
		personne_handicap_individu=simulation.compute('personnes_handicap_paris',period)
		personne_handicap = self.any_by_roles(personne_handicap_individu)
		personnes_couple=simulation.calculate('concub',period)
		statut_occupation = simulation.calculate('statut_occupation_famille',period)
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


# Critères relatifs à PSOL (PA et PH)

class paris_logement_psql(Variable):
	column=FloatCol
	label=u"Personne qui est eligible pour l'aide PSQL"
	entity_class=Familles

	def function(self,simulation,period):
		parisien = simulation.calculate('parisien',period)
		personnes_agees=simulation.compute('personnes_agees',period)
		personnes_agees_famille = self.any_by_roles(personnes_agees)
		personne_handicap_individu=simulation.compute('personnes_handicap_paris',period)
		personne_handicap = self.any_by_roles(personne_handicap_individu)
		condition_montant_aide_psql=simulation.calculate('condition_montant_aide_psql',period)
		result=parisien*(personnes_agees_famille+personne_handicap)
		return period, result*condition_montant_aide_psql

class condition_montant_aide_psql(Variable):
	column=FloatCol
	label=u"Montant de l'aide PSQL"
	entity_class=Familles

	def function(self,simulation,period):
		personnes_couple=simulation.calculate('concub',period)
		ressources_mensuelles_famille=simulation.calculate('paris_logement_familles_br',period)
		plafond_psql=select([personnes_couple,(personnes_couple!=1)],[1430,900])
		condition_ressource= ressources_mensuelles_famille<=plafond_psql
		#condition_aide_psql= 900-ressources_mensuelles_famille
		result=select([condition_ressource,(condition_ressource!=1)],[(900-ressources_mensuelles_famille),0])
		return period,result

# Paris forfait familles

class paris_forfait_famille(Variable):
	column=FloatCol
	label=u"Famille qui est eligible à l'aide paris forfait famille "
	entity_class=Familles

	def function(self,simulation,period):
		nb_enfants=simulation.calculate('paris_nb_enfants',period)
		ressources_mensuelles_famille=simulation.calculate('paris_logement_familles_br',period)
		montant_aide=select([(ressources_mensuelles_famille<=3000),(ressources_mensuelles_famille<=5000)],[305,200])
		result=select([(nb_enfants>=3),(nb_enfants<3)],[montant_aide,0])
		return period,result

# Allocation de soutien aux parents d’enfants handicapés

class paris_logement_elig_aspeh(Variable):
	column=FloatCol
	label=u"Famille qui est eligible à l'Allocation de soutien aux parents d’enfants handicapés"
	entity_class=Familles

	def function(self,simulation,period):
		pass