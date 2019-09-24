from numpy import select, where
from openfisca_france.model.base import (
    Enum,
    Variable,
    Individu,
    Famille,
    MONTH,
    set_input_divide_by_period,
    )


class complementaire_sante_solidaire_montant_i(Variable):
    value_type = float
    entity = Individu
    label = "Montant de la complémentaire santé solidaire attribué à une personne en cas d'éligibilité de la famille"
    definition_period = MONTH

    def formula(individu, period, parameters):
        P = parameters(period).cmu.complementaire_sante_solidaire
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


class complementaire_sante_solidaire_montant(Variable):
    value_type = float
    entity = Famille
    label = "Montant du complémentaire santé solidaire en cas d'éligibilité"
    definition_period = MONTH

    def formula(famille, period, parameters):
        cmu_c_etendue_montant_i = famille.members('complementaire_sante_solidaire_montant_i', period)
        return famille.sum(cmu_c_etendue_montant_i)



class complementaire_sante_solidaire(Variable):
    value_type = float
    label = "Montant (annuel) de la complémentaire santé solidaire"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2019_11_01(famille, period):
        cmu_c = famille('cmu_c', period)
        cmu_base_ressources = famille('cmu_base_ressources', period)
        cmu_c_etendue_plafond = famille('acs_plafond', period)
        cmu_c_etendue_montant = famille('complementaire_sante_solidaire_montant', period)
        residence_mayotte = famille.demandeur.menage('residence_mayotte', period)
        cmu_acs_eligibilite = famille('cmu_acs_eligibilite', period)
        acs = famille('acs', period)

        return (
            cmu_acs_eligibilite
            * not_(residence_mayotte)
            * not_(cmu_c)
            * (acs == 0)
            * (cmu_base_ressources <= cmu_c_etendue_plafond)
            * cmu_c_etendue_montant
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
