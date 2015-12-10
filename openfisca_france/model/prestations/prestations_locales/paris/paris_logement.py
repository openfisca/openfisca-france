# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select)

from ....base import *  # noqa analysis:ignore

# Paris Logement pour les personnes agées et les personnes handicapées

class paris_logement(Variable):
    column = FloatCol
    label = u"Paris Logement"
    entity_class = Familles

    def function(self, simulation, period):
        plafond_pl = simulation.legislation_at(period.start).paris.paris_logement.plafond_pl
        plafond_pl_avec_enf = simulation.legislation_at(period.start).paris.paris_logement.plafond_pl_avec_enf
        aide_pers_isol = simulation.legislation_at(period.start).paris.paris_logement.aide_pers_isol
        aide_couple_ss_enf = simulation.legislation_at(period.start).paris.paris_logement.aide_couple_ss_enf
        aide_couple_avec_enf = simulation.legislation_at(period.start).paris.paris_logement.aide_couple_avec_enf

        ressources_familiale = simulation.calculate('paris_base_ressources', period)
        personnes_couple = simulation.calculate('concub', period)
        nb_enfants = simulation.calculate('paris_nb_enfants', period)
        paris_logement_elig = simulation.calculate('paris_logement_elig', period)

        plafond = select([(nb_enfants >= 1), (nb_enfants < 1)], [plafond_pl_avec_enf, plafond_pl])
        condition_ressource = ressources_familiale <= plafond
        result = select([personnes_couple * (nb_enfants > 0), personnes_couple,
            (personnes_couple != 1) * (nb_enfants == 0)],
            [aide_couple_avec_enf, aide_couple_ss_enf, aide_pers_isol])

        return period, result * condition_ressource * paris_logement_elig


class paris_logement_elig(Variable):
    column = BoolCol
    label = u"Personne qui est eligible pour l'aide PL"
    entity_class = Familles

    def function(self, simulation, period):
        parisien = simulation.calculate('parisien', period)
        personnes_agees = simulation.compute('personnes_agees', period)
        personnes_agees_famille = self.any_by_roles(personnes_agees)
        personne_handicap_individu = simulation.compute('personnes_handicap_paris', period)
        personne_handicap = self.any_by_roles(personne_handicap_individu)
        statut_occupation = simulation.calculate('statut_occupation_famille', period)
        statut_occupation_elig = (
            (statut_occupation == 3) +
            (statut_occupation == 4) +
            (statut_occupation == 5) +
            (statut_occupation == 7))
        charges_logement = simulation.calculate('condition_taux_effort', period)
        result = parisien * statut_occupation_elig * (personnes_agees_famille + personne_handicap) * charges_logement
        return period, result


class condition_taux_effort(Variable):
    column = BoolCol
    label = u"Charges de Logement"
    entity_class = Familles

    def function(self, simulation, period):
        taux_effort = simulation.legislation_at(period.start).paris.paris_logement.taux_effort
        loyer = simulation.calculate('loyer', period)
        ressources_mensuelles = simulation.calculate('paris_base_ressources', period)
        condition_loyer = loyer >= (ressources_mensuelles * taux_effort)
        return period, condition_loyer
