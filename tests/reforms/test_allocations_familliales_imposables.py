from typing import Callable, Tuple

import pytest

from ..cache import tax_benefit_system
from openfisca_core.tools import assert_near
from openfisca_core.simulations import Simulation
from openfisca_france.reforms.allocations_familiales_imposables import (
    allocations_familiales_imposables,
    )


@pytest.fixture
def simulations(new_scenario) -> Callable[..., Tuple[Simulation]]:
    def _simulations(year: int) -> Tuple[Simulation]:
        scenario = new_scenario(
            reform = allocations_familiales_imposables(tax_benefit_system),
            count = 10,
            _max = 30000,
            _min = 0,
            name = 'salaire_imposable',
            year = year,
            people = 4,
            )

        return scenario.new_simulation(use_baseline = True), scenario.new_simulation()

    return _simulations


def test_af(simulations, year = 2012, error = 0.01):
    actual_simulation, reform_simulation = simulations(year)
    actual_af = actual_simulation.calculate_add('af', year)
    reform_af = reform_simulation.calculate_add('af', year)

    assert_near(actual_af, reform_af, absolute_error_margin = error)


def test_af_imposables(simulations, year = 2012, error = 0.01):
    actual_simulation, reform_simulation = simulations(year)
    actual_af = actual_simulation.calculate_add('af', year)
    reform_af_imposables = reform_simulation.calculate(
        'allocations_familiales_imposables',
        year,
        )

    assert_near(actual_af, reform_af_imposables, absolute_error_margin = error)


def test_rbg(simulations, year = 2012, error = 0.01):
    actual_simulation, reform_simulation = simulations(year)
    actual_af = actual_simulation.calculate_add('af', year)
    actual_rbg = actual_simulation.calculate('rbg', year)
    reform_rbg = reform_simulation.calculate('rbg', year)

    assert_near(actual_af + actual_rbg, reform_rbg, absolute_error_margin = error)
