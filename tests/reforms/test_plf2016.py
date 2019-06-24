# -*- coding: utf-8 -*-

from typing import Callable, Tuple

import numpy
import pytest

from ..cache import tax_benefit_system
from openfisca_core.reforms import Reform
from openfisca_core.simulations import Simulation
from openfisca_france.reforms.plf2016 import (
    plf2016,
    plf2016_counterfactual,
    plf2016_counterfactual_2014,
    )


@pytest.fixture
def simulations(new_scenario) -> Callable[..., Tuple[Simulation]]:
    def _simulations(reform_class: Reform, year: int) -> Tuple[Simulation]:
        scenario = new_scenario(
            reform = reform_class(tax_benefit_system),
            count = 2,
            _max = 18000,
            _min = 0,
            name = "salaire_imposable",
            year = year,
            people = 1,
            )

        return scenario.new_simulation(use_baseline = True), scenario.new_simulation()

    return _simulations


def equal(before: numpy.ndarray, after: numpy.ndarray) -> bool:
    return numpy.all(numpy.equal(before, after))


def not_equal(before: numpy.ndarray, after: numpy.ndarray) -> bool:
    return numpy.any(numpy.not_equal(before, after))


@pytest.mark.parametrize(
    "reform_class, expected", (
        (plf2016, equal),
        (plf2016_counterfactual, not_equal),
        (plf2016_counterfactual_2014, not_equal),
        ),
    )
def test_plf2016(reform_class, expected, simulations, year = 2015):
    actual_simulation, reform_simulation = simulations(reform_class, year)
    actual_impots = actual_simulation.calculate('impots_directs', year)
    reform_impots = reform_simulation.calculate('impots_directs', year)
    assert expected(actual_impots, reform_impots)
