from typing import Callable, Tuple

import numpy
import pytest

from ..cache import tax_benefit_system
from openfisca_core.simulations import Simulation
from openfisca_france.reforms.plfr2014 import plfr2014


@pytest.fixture
def simulations(new_scenario) -> Callable[..., Tuple[Simulation]]:
    def _simulations(year: int) -> Tuple[Simulation]:
        scenario = new_scenario(
            reform = plfr2014(tax_benefit_system),
            count = 2,
            _max = 18000,
            _min = 0,
            name = "salaire_imposable",
            year = year,
            people = 1,
            )

        return scenario.new_simulation(use_baseline = True), scenario.new_simulation()

    return _simulations


def test_plf2014(simulations, year = 2013):
    actual_simulation, reform_simulation = simulations(year)
    actual_impots = actual_simulation.calculate('impots_directs', year)
    reform_impots = reform_simulation.calculate('impots_directs', year)
    assert numpy.all(numpy.equal(actual_impots, reform_impots))
