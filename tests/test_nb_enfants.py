from copy import deepcopy

from openfisca_france import CountryTaxBenefitSystem as FranceTBS
from openfisca_core.tools import assert_near

from .test_entities import TEST_CASE_AGES, new_simulation
from .cache import tax_benefit_system

def test_nb_enfants():
    test_case = deepcopy(TEST_CASE_AGES)
    simulation = tax_benefit_system.new_scenario().init_from_test_case(
        period = 2013,
        test_case = test_case
    ).new_simulation()
    from openfisca_france.model.prestations.prestations_familiales.base_ressource import nb_enf

    assert_near(nb_enf(simulation.famille, simulation.period.first_month, 3, 18), [2, 0])
    assert_near(nb_enf(simulation.famille, simulation.period.first_month, 19, 50), [0, 1]) # Adults don't count

    test_case['individus'][5]['autonomie_financiere'] = True
    simulation_2 = new_simulation(test_case)

    assert_near(nb_enf(simulation_2.famille, simulation_2.period.first_month, 19, 50), [0, 0])
