from typing import Callable, Tuple

import pytest

from ..cache import tax_benefit_system
from openfisca_core.simulations import Simulation
from openfisca_france.reforms.plf2015 import plf2015


@pytest.fixture
def simulations(new_scenario) -> Callable[..., Tuple[Simulation]]:
    def _simulations(year: int) -> Tuple[Simulation]:
        scenario = new_scenario(
            reform = plf2015(tax_benefit_system),
            count = 2,
            _max = 18000,
            _min = 0,
            name = "salaire_imposable",
            year = year,
            people = 1,
            )

        return scenario.new_simulation(use_baseline = True), scenario.new_simulation()

    return _simulations


def test_plf2015_impots_directs(simulations, year = 2013, error = 1):
    actual_simulation, reform_simulation = simulations(year)
    actual_impots = actual_simulation.calculate('impots_directs', year)
    reform_impots = reform_simulation.calculate('impots_directs', year)
    assert max(abs([0, -869] - actual_impots)) < error
    assert max(abs([0, -911.4 + (1135 - 911.4)] - reform_impots)) < error


def test_plf2015_ir_plaf_qf(simulations, year = 2013, error = 1):
    actual_simulation, reform_simulation = simulations(year)
    actual_ir_plaf_qf = actual_simulation.calculate('ir_plaf_qf', year)
    reform_ir_plaf_qf = reform_simulation.calculate('ir_plaf_qf', year)
    assert max(abs([0, 918] - actual_ir_plaf_qf)) < error
    assert max(abs([0, 911.4] - reform_ir_plaf_qf)) < error
