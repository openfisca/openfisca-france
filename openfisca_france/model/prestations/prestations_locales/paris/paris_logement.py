# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select, where)

from ....base import *  # noqa analysis:ignore

# Paris Logement pour les personnes agées et les personnes handicapées

class paris_logement(Variable):
    column = FloatCol
    label = u"L'aide Paris Logement"
    entity_class = Familles

    def function(self, simulation, period):
        paris_logement_pa_ph = simulation.calculate('paris_logement_pa_ph', period)
        paris_logement_fam = simulation.calculate('paris_logement_fam', period)
        paris_logement_apd = simulation.calculate('paris_logement_apd', period)

        return period, paris_logement_pa_ph + paris_logement_fam + paris_logement_apd


class paris_logement_pa_ph(Variable):
    column = FloatCol
    label = u"Paris Logement pour les personnes handicapées et les personnes agées"
    entity_class = Familles

    def function(self, simulation, period):
        plafond_pl = simulation.legislation_at(period.start).paris.paris_logement.plafond_pl
        plafond_pl_avec_enf = simulation.legislation_at(period.start).paris.paris_logement.plafond_pl_avec_enf
        aide_pers_isol = simulation.legislation_at(period.start).paris.paris_logement.aide_pers_isol
        aide_couple_ss_enf = simulation.legislation_at(period.start).paris.paris_logement.aide_couple_ss_enf
        aide_couple_avec_enf = simulation.legislation_at(period.start).paris.paris_logement.aide_couple_avec_enf

        paris_base_ressources_commun = simulation.calculate('paris_base_ressources_commun', period)
        aspa = simulation.calculate('paris_base_ressources_aspa', period)
        asi = simulation.calculate('paris_base_ressources_asi', period)
        aah = simulation.calculate('paris_base_ressources_aah', period)
        aide_logement = simulation.calculate('paris_base_ressources_aide_logement', period)
        ressources_familiale = paris_base_ressources_commun + aspa + asi + aah + aide_logement

        personnes_couple = simulation.calculate('concub', period)
        nb_enfants = simulation.calculate('paris_nb_enfants', period)
        paris_logement_elig_pa_ph = simulation.calculate('paris_logement_elig_pa_ph', period)

        plafond = select([(nb_enfants >= 1), (nb_enfants < 1)], [plafond_pl_avec_enf, plafond_pl])
        condition_ressource = ressources_familiale <= plafond
        result = select([personnes_couple * (nb_enfants > 0), personnes_couple,
            ((personnes_couple != 1) * (nb_enfants == 0)), ((personnes_couple != 1) * (nb_enfants >= 1))],
            [aide_couple_avec_enf, aide_couple_ss_enf, aide_pers_isol, 0])
        return period, result * condition_ressource * paris_logement_elig_pa_ph


class paris_logement_elig_pa_ph(Variable):
    column = BoolCol
    label = u"Personne qui est eligible pour l'aide PL pour les personnes agées et les personne handicapées"
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

class paris_logement_fam(Variable):
    column = FloatCol
    label = u"Paris Logement pour les couples avec enfant(s)"
    entity_class = Familles

    def function(self, simulation, period):
        plafond_pl_fam = simulation.legislation_at(period.start).paris.paris_logement.plafond_pl_fam
        aide_pl_fam = simulation.legislation_at(period.start).paris.paris_logement.aide_pl_fam

        paris_base_ressources_commun = simulation.calculate('paris_base_ressources_commun', period)
        rsa = simulation.calculate('paris_base_ressources_rsa', period)
        aah = simulation.calculate('paris_base_ressources_aah', period)
        aide_logement = simulation.calculate('paris_base_ressources_aide_logement', period)
        ressources_familiale = paris_base_ressources_commun + rsa + aah + aide_logement

        personnes_couple = simulation.calculate('concub', period)
        nb_enfants = simulation.calculate('paris_nb_enfants', period)
        paris_logement_elig_fam = simulation.calculate('paris_logement_elig_fam', period)

        condition_ressource = ressources_familiale <= plafond_pl_fam

        result = where(personnes_couple * (nb_enfants > 0), aide_pl_fam, 0)

        return period, result * condition_ressource * paris_logement_elig_fam

class paris_logement_elig_fam(Variable):
    column = BoolCol
    label = u"Personne qui est eligible pour l'aide Paris Logement quand c'est un couple avec enfant(s)"
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
        result = parisien * statut_occupation_elig * (personnes_agees_famille != 1) * (personne_handicap != 1) * charges_logement
        return period, result

class paris_logement_apd(Variable):
    column = FloatCol
    label = u"Paris Logement pour les personnes isolées sans enfant"
    entity_class = Familles

    def function(self, simulation, period):
        plafond = simulation.legislation_at(period.start).paris.paris_logement.plafond_pl_apd
        aide_pl_apd_pers_isol = simulation.legislation_at(period.start).paris.paris_logement.aide_pl_apd_pers_isol
        aide_pl_apd_couple = simulation.legislation_at(period.start).paris.paris_logement.aide_pl_apd_couple

        paris_base_ressources_commun = simulation.calculate('paris_base_ressources_commun', period)

        rsa = simulation.calculate('paris_base_ressources_rsa', period)
        indemnite = simulation.calculate('paris_indemnite_enfant', period)
        aah = simulation.calculate('paris_base_ressources_aah', period)
        aide_logement = simulation.calculate('paris_base_ressources_aide_logement', period)
        ressources_familiale = paris_base_ressources_commun + aah + aide_logement + rsa - indemnite

        personnes_couple = simulation.calculate('concub', period)
        paris_logement_elig_apd = simulation.calculate('paris_logement_elig_apd', period)

        condition_ressource = ressources_familiale <= plafond

        result = where(personnes_couple, aide_pl_apd_couple, aide_pl_apd_pers_isol)

        return period, result * condition_ressource * paris_logement_elig_apd

class paris_logement_elig_apd(Variable):
    column = BoolCol
    label = u"Personne qui est eligible pour l'aide Paris Logement aide aux parisiens en difficultés"
    entity_class = Familles

    def function(self, simulation, period):
        parisien = simulation.calculate('parisien', period)
        personnes_agees = simulation.compute('personnes_agees', period)
        personnes_agees_famille = self.any_by_roles(personnes_agees)
        personne_handicap_individu = simulation.compute('personnes_handicap_paris', period)
        personne_handicap = self.any_by_roles(personne_handicap_individu)
        statut_occupation = simulation.calculate('statut_occupation_famille', period)
        loyer = simulation.calculate('loyer', period)
        nb_enfants = simulation.calculate('paris_nb_enfants', period)

        statut_occupation_elig = (
            (statut_occupation == 3) +
            (statut_occupation == 4) +
            (statut_occupation == 5) +
            (statut_occupation == 7))
        charges_logement = simulation.calculate('condition_taux_effort', period)

        result = parisien * statut_occupation_elig * (personnes_agees_famille != 1) * (personne_handicap != 1) * charges_logement * (loyer > 0) * (nb_enfants == 0)

        return period, result
