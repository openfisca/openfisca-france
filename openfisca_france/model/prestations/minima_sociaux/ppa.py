# -*- coding: utf-8 -*-

from __future__ import division

from ...base import *  # noqa analysis:ignore

from numpy import maximum as max_, round as round_, minimum as min_, logical_not as not_, where, select

class ppa_eligibilite(Variable):
    column = BoolCol
    entity_class = Familles
    label = u"Eligibilité à la PPA pour un mois"

    def function(self, simulation, period):
        period = period.this_month
        P = simulation.legislation_at(period.start)
        age_min = P.minim.ppa.age_min
        condition_age_individus = simulation.calculate('age', period) >= age_min
        condition_age = self.any_by_roles(condition_age_individus)
        elig = condition_age

        return period, elig

class ppa_montant_forfaitaire_familial_non_majore(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Montant forfaitaire familial (sans majoration)"

    def function(self, simulation, period):
        period = period.this_month
        nb_parents = simulation.calculate('nb_par', period)
        nb_enfants = simulation.calculate('nb_enfant_rsa', period)
        ppa_majoree_eligibilite = simulation.calculate('rsa_majore_eligibilite', period)
        rmi = simulation.legislation_at(period.start).minim.rmi
        nb_personnes = nb_parents + nb_enfants

        taux_non_majore = (
            1 +
            (nb_personnes >= 2) * rmi.txp2 +
            (nb_personnes >= 3) * rmi.txp3 +
            (nb_personnes >= 4) * where(nb_parents == 1, rmi.txps, rmi.txp3) + # Si nb_par == 1, pas de conjoint, la 4e personne est un enfant, donc le taux est de 40%.
            max_(nb_personnes - 4, 0) * rmi.txps
            )

        return period, rmi.rmi * taux_non_majore

class ppa_montant_forfaitaire_familial_majore(Variable):
    column = FloatCol
    entity_class = Familles
    label = u"Montant forfaitaire familial (avec majoration)"

    def function(self, simulation, period):
        nb_enfants = simulation.calculate('nb_enfant_rsa', period)
        rmi = simulation.legislation_at(period.start).minim.rmi
        taux_majore = rmi.majo_rsa.pac0 + rmi.majo_rsa.pac_enf_sup * nb_enfants

        return period, rmi.rmi * taux_majore
