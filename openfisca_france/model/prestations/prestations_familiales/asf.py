# -*- coding: utf-8 -*-

from __future__ import division

from numpy import logical_not as not_

from ...base import *  # noqa analysis:ignore

# from .base_ressource import nb_enf


@reference_formula
class asf_elig_enfant(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Individus
    label = u"Enfant pouvant ouvrir droit à l'ASF"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        age = simulation.calculate('age', period)
        smic55 = simulation.calculate('smic55', period)

        pfam = simulation.legislation_at(period.start).fam

        eligibilite = (
            (age >= pfam.af.age1) * (age <= pfam.af.age3) *  # Âge compatible avec les prestations familiales
            not_(smic55))  # Ne perçoit pas plus de ressources que "55% du SMIC" au sens CAF

        return period, eligibilite

@reference_formula
class asf_enfant(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Montant du droit à l'ASF ouvert par l'enfant"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        asf_elig_enfant = simulation.calculate('asf_elig_enfant', period)
        pfam = simulation.legislation_at(period.start).fam

        return period, asf_elig_enfant * pfam.af.bmaf * pfam.asf.taux1


@reference_formula
class asf_elig(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Éligibilité à l'ASF"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        pensions_alimentaires_percues_holder = simulation.compute('pensions_alimentaires_percues', period)
        pensions_alimentaires_percues = self.sum_by_entity(pensions_alimentaires_percues_holder)

        isol = simulation.calculate('isol', period)
        residence_mayotte = simulation.calculate('residence_mayotte', period)

        return period, not_(residence_mayotte) * isol * not_(pensions_alimentaires_percues)  # Parent isolé et ne résident pas à Mayotte


@reference_formula
class asf(SimpleFormulaColumn):
    calculate_output = calculate_output_add
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation de soutien familial (ASF)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        asf_elig = simulation.calculate('asf_elig', period)
        asf_enfant_holder = simulation.compute('asf_enfant', period)
        montant = self.sum_by_entity(asf_enfant_holder, roles = ENFS)

        return period, asf_elig * montant
