from numpy import select, where, logical_not as not_
from openfisca_france.model.base import (
    Enum,
    Variable,
    Individu,
    Famille,
    MONTH,
    set_input_divide_by_period,
    )


class css_participation_forfaitaire_montant_i(Variable):
    value_type = float
    entity = Individu
    label = "Montant de la participation forfaitaire d'une personne"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        P = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.cs.css.montant
        age = individu('age', period)
        salarie_regime_alsace_moselle = individu('salarie_regime_alsace_moselle', period)
        regime = where(
            salarie_regime_alsace_moselle,
            RegimeComplementaireSanteSolidaire.alsace_moselle,
            RegimeComplementaireSanteSolidaire.france,
            )
        tranche = select(
            [
                age < 30,
                age <= 49,
                age <= 59,
                age <= 69,
                age > 69,
                ],
            [
                TranchesComplementaireSanteSolidaire.cmu_moins_30_ans,
                TranchesComplementaireSanteSolidaire.cmu_30_49_ans,
                TranchesComplementaireSanteSolidaire.cmu_50_59_ans,
                TranchesComplementaireSanteSolidaire.cmu_60_69_ans,
                TranchesComplementaireSanteSolidaire.cmu_plus_69_ans,
                ],
            )
        return P[regime][tranche]


class css_participation_forfaitaire_montant(Variable):
    value_type = float
    entity = Famille
    label = "Montant de participation forfaitaire d'une famille en cas d'éligibilité"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        css_participation_forfaitaire_i = famille.members('css_participation_forfaitaire_montant_i', period)
        return famille.sum(css_participation_forfaitaire_i)


class css_participation_forfaitaire(Variable):
    value_type = float
    label = 'Montant annuel de la participation forfaitaire à la CSS'
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2019_11_01(famille, period):
        cmu_c = famille('cmu_c', period)
        css_cmu_base_ressources = famille('css_cmu_base_ressources', period)
        css_plafond = famille('acs_plafond', period)
        css_participation_forfaitaire_montant = famille('css_participation_forfaitaire_montant', period)
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)
        css_cmu_acs_eligibilite = famille('css_cmu_acs_eligibilite', period)
        acs = famille('acs', period)

        return (
            css_cmu_acs_eligibilite
            * not_(residence_mayotte)
            * not_(cmu_c)
            * (acs == 0)
            * (css_cmu_base_ressources <= css_plafond)
            * css_participation_forfaitaire_montant
            )


class RegimeComplementaireSanteSolidaire(Enum):
    france = 'France'
    alsace_moselle = 'Alsace Moselle'


class TranchesComplementaireSanteSolidaire(Enum):
    cmu_moins_30_ans = 'Moins de 30 ans'
    cmu_30_49_ans = 'Entre 30 et 49 ans'
    cmu_50_59_ans = 'Entre 50 et 59 ans'
    cmu_60_69_ans = 'Entre 60 et 69 ans'
    cmu_plus_69_ans = 'Plus de 69 ans'
