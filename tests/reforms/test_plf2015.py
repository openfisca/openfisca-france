# -*- coding: utf-8 -*-

from ..cache import tax_benefit_system
from openfisca_core import periods
from openfisca_france.scenarios import init_single_entity
from openfisca_france.reforms.plf2015 import plf2015


def test_plf2015(axes, parent1, parent2, enfants):
    reform = plf2015(tax_benefit_system)
    count = 2
    salaire_max = 18000
    salaire_min = 0
    name = "salaire_imposable"
    year = 2013
    people = 1
    error_margin = 1

    scenario = init_single_entity(
        reform.new_scenario(),
        axes = axes(count, salaire_max, salaire_min, name),
        period = periods.period(year),
        parent1 = parent1(year),
        parent2 = parent2(year, people),
        enfants = enfants(year, people),
        )

    reference_simulation = scenario.new_simulation(use_baseline = True)
    reform_simulation = scenario.new_simulation()

    impots_directs = reference_simulation.calculate('impots_directs', period = year)
    reform_impots_directs = reform_simulation.calculate('impots_directs', period = year)
    ir_plaf_qf = reference_simulation.calculate('ir_plaf_qf', period = year)
    reform_ir_plaf_qf = reform_simulation.calculate('ir_plaf_qf', period = year)

    assert max(abs([0, 918] - ir_plaf_qf)) < error_margin
    assert max(abs([0, 911.4] - reform_ir_plaf_qf)) < error_margin
    assert max(abs([0, -869] - impots_directs)) < error_margin
    assert max(abs([0, -911.4 + (1135 - 911.4)] - reform_impots_directs)) < error_margin
