# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select)

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

        #salaire_individus = simulation.compute_add('salaire_net',period.last_3_months)
        #salaire = self.sum_by_entity(salaire_individus) / 3

        montant_ressource = simulation.calculate('test_base_ressources',period)

        condition_age_individus = simulation.compute('tutorial_condition_age', period)
        condition_age = self.any_by_roles(condition_age_individus)


        nombre_enfant =simulation.calculate('af_nbenf')
        pourcentage_enfant = 0.20*nombre_enfant

        habitant_paris = simulation.calculate('habitant_paris',period)
        eligibilite = (habitant_paris) * condition_age
        montant_base = select([montant_ressource < (smic_mensuel/2), montant_ressource < smic_mensuel], [2000, 1000])
        montant_total = montant_base * (1 + pourcentage_enfant)
        return period,montant_total * eligibilite

class test_base_ressources(Variable):
    column = FloatCol
    label=u"Calcul des ressources"
    entity_class=Familles

    def function(self,simulation,period):
        total_allocations_familiales=simulation.calculate_add('af',period.last_3_months)/3
        test_rsa=simulation.calculate_add('rsa',period.last_3_months)/3
        montant_total_individus=simulation.compute('test_base_ressources_i')
        montat_total_famille= self.sum_by_entity(montant_total_individus)

        result = total_allocations_familiales+test_rsa+montat_total_famille
        return period, result

class test_base_ressources_i(Variable):
    column=FloatCol
    label=u"Calcul des ressources Individu"
    entity_class=Individus

    def function(self,simulation,period):
        salaire_individus_i=simulation.calculate_add('salaire_net',period.last_3_months)/3
        chomage_i=simulation.calculate_add('chonet',period.last_3_months)/3
        montant_stage_i = simulation.calculate_add('indemnites_stage',period.last_3_months)/3

        result = salaire_individus_i+chomage_i+montant_stage_i
        return period, result


class tutorial_condition_age(Variable):
    column = BoolCol
    label = u"Individu éligible à l'aide tutorial"
    entity_class = Individus

    def function(self, simulation, period):
        age=simulation.calculate('age', period)
        condition = (age >= 18) * (age <=25)

        return period, condition


class habitant_paris(Variable):
    column =BoolCol
    label = u"Habitant de paris"
    entity_class =Familles


