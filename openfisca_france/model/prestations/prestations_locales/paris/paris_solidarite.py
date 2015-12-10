# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_,  logical_not as not_,  absolute as abs_,  minimum as min_,  select)

from ....base import *  # noqa analysis:ignore

# Paris solidarité pour les personnes agées et les personnes handicapées

class paris_logement_psol(Variable):
    column = FloatCol
    label = u"Personne qui est eligible pour l'aide PSOL"
    entity_class = Familles

    def function(self, simulation, period):
        parisien = simulation.calculate('parisien', period)
        personnes_agees = simulation.compute('personnes_agees', period)
        personnes_agees_famille = self.any_by_roles(personnes_agees)
        personne_handicap_individu = simulation.compute('personnes_handicap_paris', period)
        personne_handicap = self.any_by_roles(personne_handicap_individu)
        condition_montant_aide_psol = simulation.calculate('condition_montant_aide_psol', period)
        result = parisien * (personnes_agees_famille + personne_handicap)
        return period, result * condition_montant_aide_psol

class condition_montant_aide_psol(Variable):
    column = FloatCol
    label = u"Montant de l'aide PSOL"
    entity_class = Familles

    def function(self, simulation, period):
        personnes_couple = simulation.calculate('concub', period)
        ressources_mensuelles_famille = simulation.calculate('paris_base_ressources', period)
        plafond_psol = select([personnes_couple, (personnes_couple != 1)], [1430, 900])
        condition_ressource = ressources_mensuelles_famille <= plafond_psol
        result = select([condition_ressource, (condition_ressource != 1)], [(900 - ressources_mensuelles_famille), 0])
        return period, result
