# -*- coding: utf-8 -*-

from typing import Callable, Tuple

import numpy
import pytest

from ..cache import tax_benefit_system
from openfisca_core.simulations import Simulation
from openfisca_france.reforms.cesthra_invalidee import cesthra_invalidee


@pytest.fixture
def simulations(new_scenario) -> Callable[..., Tuple[Simulation]]:
    def _simulations(year: int) -> Tuple[Simulation]:
        scenario = new_scenario(
            reform = cesthra_invalidee(tax_benefit_system),
            count = 10,
            _max = 30000,
            _min = 0,
            name = "salaire_imposable",
            year = year,
            people = 4,
            )

        return scenario.new_simulation(use_baseline = True), scenario.new_simulation()

    return _simulations


def test_cesthra_impots_directs(simulations, year = 2012):
    actual_simulation, reform_simulation = simulations(year)
    actual_impots = actual_simulation.calculate('impots_directs', year)
    reform_impots = reform_simulation.calculate('impots_directs', year)
    assert numpy.all(numpy.equal(actual_impots, reform_impots))


def test_cesthra_revdisp(simulations, year = 2012):
    actual_simulation, reform_simulation = simulations(year)
    actual_revdisp = actual_simulation.calculate('revenu_disponible', year)
    reform_revdisp = reform_simulation.calculate('revenu_disponible', year)
    assert numpy.all(numpy.equal(actual_revdisp, reform_revdisp))
