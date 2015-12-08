# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select)

from ....base import *  # noqa analysis:ignore

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


class paris_logement_familles_br_i(Variable):
    column = FloatCol
    label = u"Base de ressources individuelle pour Paris Logement Famille"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        last_year = period.last_year
        salaire_net = simulation.calculate('salaire_net', period)
        chonet = simulation.calculate('chonet', period)
        rstnet = simulation.calculate('rstnet', period)
        pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', period)
        pensions_alimentaires_versees_individu = simulation.calculate(
            'pensions_alimentaires_versees_individu', period)
        rsa_base_ressources_patrimoine_i = simulation.calculate_add('rsa_base_ressources_patrimoine_i', period)
        indemnites_journalieres_imposables = simulation.calculate('indemnites_journalieres_imposables', period)
        indemnites_stage = simulation.calculate('indemnites_stage', period)
        revenus_stage_formation_pro = simulation.calculate('revenus_stage_formation_pro', period)
        allocation_securisation_professionnelle = simulation.calculate(
            'allocation_securisation_professionnelle', period)
        prestation_compensatoire = simulation.calculate('prestation_compensatoire', period)
        pensions_invalidite = simulation.calculate('pensions_invalidite', period)
        indemnites_chomage_partiel = simulation.calculate('indemnites_chomage_partiel', period)
        bourse_recherche = simulation.calculate('bourse_recherche', period)
        gains_exceptionnels = simulation.calculate('gains_exceptionnels', period)

        def revenus_tns():
            revenus_auto_entrepreneur = simulation.calculate_add('tns_auto_entrepreneur_benefice', period)

            # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1
            tns_micro_entreprise_benefice = simulation.calculate('tns_micro_entreprise_benefice', last_year) / 12
            tns_benefice_exploitant_agricole = simulation.calculate('tns_benefice_exploitant_agricole', last_year) / 12
            tns_autres_revenus = simulation.calculate('tns_autres_revenus', last_year) / 12

            return revenus_auto_entrepreneur + tns_micro_entreprise_benefice + tns_benefice_exploitant_agricole + tns_autres_revenus

        result = (
            salaire_net + indemnites_chomage_partiel + indemnites_stage + chonet + rstnet +
            pensions_alimentaires_percues - abs_(pensions_alimentaires_versees_individu) +
            rsa_base_ressources_patrimoine_i + allocation_securisation_professionnelle +
            indemnites_journalieres_imposables + prestation_compensatoire +
            pensions_invalidite + bourse_recherche + gains_exceptionnels + revenus_tns() +
            revenus_stage_formation_pro
            )

        return period, result

class paris_logement_familles_br(Variable):
    column = FloatCol
    label = u"Base de ressource pour Paris Logement Famille"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        paris_logement_familles_br_i_holder = simulation.compute('paris_logement_familles_br_i', period)
        paris_logement_familles_br = self.sum_by_entity(paris_logement_familles_br_i_holder)
        result = paris_logement_familles_br

        return period, result
