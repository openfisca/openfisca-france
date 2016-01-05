# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select, where)

from ....base import *  # noqa analysis:ignore

class paris_complement_sante(Variable):
    column = FloatCol
    label = u"L'aide Complémentaire Santé Paris"
    entity_class = Familles

    def function(self, simulation, period):
        plafond_pers_isol_cs = simulation.legislation_at(period.start).paris.complement_sante.plafond_pers_isol_cs
        plafond_couple_cs = simulation.legislation_at(period.start).paris.complement_sante.plafond_couple_cs
        montant_aide_cs = simulation.legislation_at(period.start).paris.complement_sante.montant_aide_cs

        parisien = simulation.calculate('parisien', period)
        personnes_agees_i = simulation.compute('paris_personnes_agees', period)
        personnes_agees = self.any_by_roles(personnes_agees_i)
        personnes_handicape_i = simulation.compute('personnes_handicap_paris', period)
        personnes_handicap = self.any_by_roles(personnes_handicape_i)
        concub = simulation.calculate('concub', period)
        cmu_c = simulation.calculate('cmu_c', period)
        acs_montant = simulation.calculate('acs_montant', period)
        aspa = simulation.calculate('aspa', period)
        ass = simulation.calculate('ass', period)
        asi = simulation.calculate('asi', period)
        aide_logement = simulation.calculate('aide_logement', period)
        ressources_i = simulation.compute('paris_complement_sante_i', period)
        ressources = self.split_by_roles(ressources_i, roles = [CHEF, PART])

        ressources_pers_isol = ressources[CHEF] + aspa + ass + asi + aide_logement

        ressources_couple = ressources[CHEF] + ressources[PART]

        ressources_couple += aspa + ass + asi + aide_logement

        plafond = where(concub, plafond_couple_cs, plafond_pers_isol_cs)

        montant_pers_handicap = where(parisien * personnes_handicap * (concub != 1) *
            (ressources_pers_isol <= plafond) * (montant_aide_cs >= acs_montant),
            montant_aide_cs - acs_montant, 0)

        montant_couple = where(parisien * concub * (personnes_handicap + personnes_agees) *
            (acs_montant != 0) * (ressources_couple <= plafond), montant_aide_cs - acs_montant, 0)

        montant_couple_ss_acs = where(parisien * concub * (personnes_handicap + personnes_agees) *
            (acs_montant == 0) * (cmu_c != 1) * (ressources_couple <= plafond), montant_aide_cs, 0)

        return period, montant_pers_handicap + montant_couple + montant_couple_ss_acs


class paris_complement_sante_i(Variable):
    column = FloatCol
    label = u"Ressources Individuelles"
    entity_class = Individus

    def function(self, simulation, period):
        paris_base_ressources_commun_i = simulation.calculate('paris_base_ressources_commun_i', period)
        aah = simulation.calculate('aah')

        ressources_demandeur = paris_base_ressources_commun_i + aah

        return period, ressources_demandeur
