# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select)

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
        print personnes_agees_famille
        personne_handicap_individu = simulation.compute('personnes_handicap_paris', period)
        personne_handicap = self.any_by_roles(personne_handicap_individu)
        print personne_handicap
        condition_montant_aide_agee = simulation.calculate('condition_montant_aide_agee', period)
        condition_montant_aide_handicape = simulation.calculate('condition_montant_aide_handicape', period)
        print condition_montant_aide_agee
        print condition_montant_aide_handicape
        result = parisien * (personnes_agees_famille + personne_handicap)
        print result
        choix_condition = select([personnes_agees_famille, personne_handicap],
            [condition_montant_aide_agee, condition_montant_aide_handicape])
        return period, result * choix_condition

class condition_montant_aide_agee(Variable):
    column = FloatCol
    label = u"Montant de l'aide PSOL pour les personnes âgées"
    entity_class = Familles

    def function(self, simulation, period):
        montant_seul_annuel = simulation.legislation_at(period.start).minim.aspa.montant_seul
        montant_couple_annuel = simulation.legislation_at(period.start).minim.aspa.montant_couple
        plafond_seul_psol = simulation.legislation_at(period.start).paris.paris_solidarite.plafond_seul_psol
        plafond_couple_psol = simulation.legislation_at(period.start).paris.paris_solidarite.plafond_couple_psol

        montant_seul = montant_seul_annuel / 12
        montant_couple = montant_couple_annuel / 12
        personne_handicap_individu = simulation.compute('personnes_handicap_paris', period)
        personne_handicap = self.any_by_roles(personne_handicap_individu)
        personnes_couple = simulation.calculate('concub', period)
        ressources_mensuelles = simulation.calculate('paris_base_ressources', period)

        plafond_psol = select([personnes_couple, (personnes_couple != 1)], [plafond_couple_psol, plafond_seul_psol])

        ressources_mensuelles_min = select([(personnes_couple != 1) * (ressources_mensuelles <= plafond_psol) *
            (personne_handicap != 1),
            personnes_couple * (ressources_mensuelles <= plafond_psol) * (personne_handicap != 1),
            (ressources_mensuelles >= plafond_psol) * (personne_handicap != 1), personne_handicap],
            [montant_seul, montant_couple, ressources_mensuelles, ressources_mensuelles])

        result = select([((personnes_couple != 1) * (ressources_mensuelles_min <= plafond_psol)),
            personnes_couple * (ressources_mensuelles_min <= plafond_psol),
            ((personnes_couple != 1) + personnes_couple) * (ressources_mensuelles_min >= plafond_psol)],
            [(plafond_seul_psol - ressources_mensuelles_min), (plafond_couple_psol - ressources_mensuelles_min), 0])
        return period, result

class condition_montant_aide_handicape(Variable):
    column = FloatCol
    label = u"Montant de l'aide PSOL pour les personnes handicapées"
    entity_class = Familles

    def function(self, simulation, period):
        aah = simulation.legislation_at(period.start).minim.aah.montant
        print aah
        plafond_seul_psol = simulation.legislation_at(period.start).paris.paris_solidarite.plafond_seul_psol
        print plafond_seul_psol
        plafond_couple_psol = simulation.legislation_at(period.start).paris.paris_solidarite.plafond_couple_psol

        personne_handicap_individu = simulation.compute('personnes_handicap_paris', period)
        personne_handicap = self.any_by_roles(personne_handicap_individu)
        personnes_couple = simulation.calculate('concub', period)
        ressources_mensuelles = simulation.calculate('paris_base_ressources', period)
        print ressources_mensuelles

        plafond_psol = select([personnes_couple, (personnes_couple != 1)], [plafond_couple_psol, plafond_seul_psol])

        ressources_mensuelles_min = select([(ressources_mensuelles <= aah) * personne_handicap,
            (ressources_mensuelles >= aah) * personne_handicap], [aah, ressources_mensuelles])
        print ressources_mensuelles_min

        result = select([((personnes_couple != 1) * (ressources_mensuelles_min <= plafond_psol)),
            personnes_couple * (ressources_mensuelles_min <= plafond_psol),
            ((personnes_couple != 1) + personnes_couple) * (ressources_mensuelles_min >= plafond_psol)],
            [(plafond_seul_psol - ressources_mensuelles_min), (plafond_couple_psol - ressources_mensuelles_min), 0])
        print result
        return period, result
