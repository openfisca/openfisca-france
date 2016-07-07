# -*- coding: utf-8 -*-

from __future__ import division

from numpy import logical_not as not_

from openfisca_france.model.base import *  # noqa analysis:ignore

from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf


class asf_elig_enfant(Variable):
    column = BoolCol(default = False)
    entity_class = Individus
    label = u"Enfant pouvant ouvrir droit à l'ASF"

    def function(self, simulation, period):
        period = period.this_month

        age = simulation.calculate('age', period)
        autonomie_financiere = simulation.calculate('autonomie_financiere', period)

        pfam = simulation.legislation_at(period.start).fam

        eligibilite = (
            (age >= pfam.af.age1) * (age < pfam.af.age3) *  # Âge compatible avec les prestations familiales
            not_(autonomie_financiere))  # Ne perçoit pas plus de ressources que "55% du SMIC" au sens CAF

        return period, eligibilite


class asf_elig(Variable):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Éligibilité à l'ASF"

    def function(self, simulation, period):
        period = period.this_month
        pensions_alimentaires_percues_holder = simulation.compute('pensions_alimentaires_percues', period)
        pensions_alimentaires_percues = self.sum_by_entity(pensions_alimentaires_percues_holder)

        isole = not_(simulation.calculate('en_couple', period))
        residence_mayotte = simulation.calculate('residence_mayotte', period)

        return period, not_(residence_mayotte) * isole * not_(pensions_alimentaires_percues)  # Parent isolé et ne résident pas à Mayotte


class asf(Variable):
    calculate_output = calculate_output_add
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation de soutien familial (ASF)"

    def function(self, simulation, period):
        period = period.this_month

        pfam = simulation.legislation_at(period.start).fam
        asf_elig = simulation.calculate('asf_elig', period)
        asf_par_enfant = simulation.calculate('asf_elig_enfant', period) * pfam.af.bmaf * pfam.asf.taux1
        montant = self.sum_by_entity(asf_par_enfant, roles = ENFS)

        return period, asf_elig * montant
