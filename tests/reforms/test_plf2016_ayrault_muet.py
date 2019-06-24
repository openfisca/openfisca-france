# -*- coding: utf-8 -*-

import numpy

from ..cache import tax_benefit_system
from openfisca_core import periods
from openfisca_france.scenarios import init_single_entity
from openfisca_france.reforms.plf2016_ayrault_muet import ayrault_muet


def test_plf2016_ayrault_muet(axes, parent1, parent2, enfants):
    reform = ayrault_muet(tax_benefit_system)
    count = 2
    salaire_max = 18000
    salaire_min = 0
    name = "salaire_imposable"
    year = 2015
    people = 1

    scenario = init_single_entity(
        reform.new_scenario(),
        axes = axes(count, salaire_max, salaire_min, name),
        period = periods.period(year),
        parent1 = parent1(year),
        parent2 = parent2(year, people),
        enfants = enfants(year, people),
        )

    reference_simulation = scenario.new_simulation(use_baseline = True)
    impots_reference = reference_simulation.calculate('impots_directs', period = year)

    reform_simulation = scenario.new_simulation()
    impots_reforme = reform_simulation.calculate('impots_directs', period = year)

    assert numpy.all(numpy.equal(impots_reference, impots_reforme))
