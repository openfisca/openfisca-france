# -*- coding: utf-8 -*-

from __future__ import division

from numpy import logical_not as not_

from openfisca_france.model.base import *  # noqa analysis:ignore

from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf


class asf_elig_enfant(Variable):
    column = BoolCol(default = False)
    entity = Individu
    label = u"Enfant pouvant ouvrir droit à l'ASF"

    def function(individu, period, legislation):
        period = period.this_month

        age = individu('age', period)
        autonomie_financiere = individu('autonomie_financiere', period)

        pfam = legislation(period).prestations.prestations_familiales

        eligibilite = (
            (age >= pfam.af.age1) * (age < pfam.af.age3) *  # Âge compatible avec les prestations familiales
            not_(autonomie_financiere))  # Ne perçoit pas plus de ressources que "55% du SMIC" au sens CAF

        return period, eligibilite


class asf_elig(Variable):
    column = BoolCol(default = False)
    entity = Famille
    label = u"Éligibilité à l'ASF"

    def function(famille, period):
        period = period.this_month
        pensions_alimentaires_percues = famille.members('pensions_alimentaires_percues', period)
        pas_de_pensions = not_(famille.sum(pensions_alimentaires_percues))

        isole = not_(famille('en_couple', period))
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)

        return period, not_(residence_mayotte) * isole * pas_de_pensions  # Parent isolé et ne résident pas à Mayotte


class asf(Variable):
    calculate_output = calculate_output_add
    column = FloatCol
    entity = Famille
    label = u"Allocation de soutien familial (ASF)"

    def function(famille, period, legislation):
        period = period.this_month

        pfam = legislation(period).prestations.prestations_familiales
        asf_elig = famille('asf_elig', period)
        asf_par_enfant = famille.members('asf_elig_enfant', period) * pfam.af.bmaf * pfam.asf.taux_1_parent
        montant = famille.sum(asf_par_enfant, role = Famille.ENFANT)

        return period, asf_elig * montant
