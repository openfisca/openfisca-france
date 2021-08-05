from numpy import select, where, logical_not as not_
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

    def formula_2009_08_01(individu, period, parameters):
        P = parameters(period).cs.acs
        age = individu('age', period)
        montant_si_pac = select(
            [(age <= 15) * (age >= 0), age <= 25],
            [P.acs_moins_16_ans, P.acs_16_49_ans]
            )
        montant_si_parent = select(
            [age <= 15, age <= 49, age <= 59, age >= 60],
            [P.acs_moins_16_ans, P.acs_16_49_ans, P.acs_50_59_ans, P.acs_plus_60_ans],
            )
        return where(
            individu.has_role(Famille.PARENT),
            montant_si_parent,
            montant_si_pac
            )


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
        P = parameters(period).cs.acs
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
        cmu_base_ressources = famille('cmu_base_ressources', period)
        acs_plafond = famille('acs_plafond', period)
        acs_montant = famille('acs_montant', period)
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)
        cmu_acs_eligibilite = famille('cmu_acs_eligibilite', period)

        return (
            cmu_acs_eligibilite
            * not_(residence_mayotte)
            * not_(cmu_c)
            * (cmu_base_ressources <= acs_plafond)
            * acs_montant
            )
