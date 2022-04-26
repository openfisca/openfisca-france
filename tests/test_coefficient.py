from openfisca_france import FranceTaxBenefitSystem
from openfisca_france.scenarios import init_single_entity


def test_coefficient_proratisation_only_contract_periods_wide():
    tax_benefit_system = FranceTaxBenefitSystem()
    scenario = tax_benefit_system.new_scenario()
    init_single_entity(scenario, period='2017',  # wide: we simulate for the year
        parent1=dict(salaire_de_base={'2017-11': 2300},
        effectif_entreprise=1,
        code_postal_entreprise='75001',
        categorie_salarie='prive_non_cadre',
        contrat_de_travail_debut={2017: '2017-11-01'},
        contrat_de_travail_fin={2017: '2017-12-01'},
        allegement_fillon_mode_recouvrement='progressif'))
    simulation = scenario.new_simulation()
    assert simulation.calculate('coefficient_proratisation', '2017-11') == 1
    assert simulation.calculate('coefficient_proratisation', '2017-12') == 0
    assert simulation.calculate('coefficient_proratisation', '2017-10') == 0
    assert simulation.calculate_add('coefficient_proratisation', '2017') == 1


def test_coefficient_proratisation_only_contract_periods_narrow():
    tax_benefit_system = FranceTaxBenefitSystem()
    scenario = tax_benefit_system.new_scenario()
    init_single_entity(scenario, period='2017-11',  # narrow: we simulate for the month
        parent1=dict(salaire_de_base={'2017-11': 2300},
        effectif_entreprise=1,
        code_postal_entreprise='75001',
        categorie_salarie='prive_non_cadre',
        contrat_de_travail_debut={2017: '2017-11-01'},
        contrat_de_travail_fin={2017: '2017-12-01'},
        allegement_fillon_mode_recouvrement='progressif'))
    simulation = scenario.new_simulation()
    assert simulation.calculate('coefficient_proratisation', '2017-11') == 1
    assert simulation.calculate('coefficient_proratisation', '2017-12') == 0
    assert simulation.calculate('coefficient_proratisation', '2017-10') == 0
    assert simulation.calculate_add('coefficient_proratisation', '2017') == 1
