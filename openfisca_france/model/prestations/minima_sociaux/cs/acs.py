from numpy import logical_not as not_
from openfisca_france.model.base import (
    Variable,
    Individu,
    Famille,
    MONTH,
    set_input_divide_by_period,
    )


class acs_montant_i(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'ACS attribué à une personne en cas d'éligibilité de la famille"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2005_01_01(individu, period, parameters):
        age = individu('age', period)
        bareme = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.cs.acs.bareme

        return (age >= 0) * bareme.calc(age)


class acs_montant(Variable):
    value_type = float
    entity = Famille
    label = "Montant de l'ACS attribué à une famille en cas d'éligibilité"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2009_08_01(famille, period, parameters):
        acs_montant_i = famille.members('acs_montant_i', period)
        return famille.sum(acs_montant_i)


class acs_plafond(Variable):
    value_type = float
    entity = Famille
    label = "Plafond annuel de ressources pour l'éligibilité à l'ACS"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        P = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.cs.acs
        cmu_c_plafond = famille('cmu_c_plafond', period)

        return cmu_c_plafond * (1 + P.majoration_plafond_acs)


class acs(Variable):
    value_type = float
    label = "Montant (annuel) de l'ACS"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2021-05-01'

    def formula_2019_11_01(famille, period):
        return

    def formula(famille, period):
        cmu_c = famille('cmu_c', period)
        css_cmu_base_ressources = famille('css_cmu_base_ressources', period)
        acs_plafond = famille('acs_plafond', period)
        acs_montant = famille('acs_montant', period)
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)
        css_cmu_acs_eligibilite = famille('css_cmu_acs_eligibilite', period)

        return (
            css_cmu_acs_eligibilite
            * not_(residence_mayotte)
            * not_(cmu_c)
            * (css_cmu_base_ressources <= acs_plafond)
            * acs_montant
            )
