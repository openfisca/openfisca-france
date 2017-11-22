# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france.model.base import *  # noqa analysis:ignore

from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf


class asf_elig_enfant(Variable):
    value_type = bool
    entity = Individu
    label = u"Enfant pouvant ouvrir droit à l'ASF"
    definition_period = MONTH

    def formula(individu, period, parameters):
        age = individu('age', period)
        autonomie_financiere = individu('autonomie_financiere', period)

        pfam = parameters(period).prestations.prestations_familiales

        eligibilite = (
            (age >= pfam.af.age1) * (age < pfam.af.age3) *  # Âge compatible avec les prestations familiales
            not_(autonomie_financiere))  # Ne perçoit pas plus de ressources que "55% du SMIC" au sens CAF

        return eligibilite


class asf_elig(Variable):
    value_type = bool
    entity = Famille
    label = u"Éligibilité à l'ASF"
    definition_period = MONTH

    def formula(famille, period):
        pensions_alimentaires_percues = famille.members('pensions_alimentaires_percues', period)
        pas_de_pensions = not_(famille.sum(pensions_alimentaires_percues))

        isole = not_(famille('en_couple', period))
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)

        return not_(residence_mayotte) * isole * pas_de_pensions  # Parent isolé et ne résident pas à Mayotte


class asf(Variable):
    calculate_output = calculate_output_add
    value_type = float
    entity = Famille
    label = u"Allocation de soutien familial (ASF)"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        pfam = parameters(period).prestations.prestations_familiales
        asf_elig = famille('asf_elig', period)
        asf_par_enfant = famille.members('asf_elig_enfant', period) * pfam.af.bmaf * pfam.asf.taux_1_parent
        montant = famille.sum(asf_par_enfant, role = Famille.ENFANT)

        return asf_elig * montant
