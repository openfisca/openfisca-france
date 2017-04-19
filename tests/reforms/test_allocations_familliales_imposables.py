# -*- coding: utf-8 -*-

import datetime


from openfisca_core import periods
from openfisca_core.tools import assert_near

from openfisca_france.reforms.allocations_familiales_imposables import allocations_familiales_imposables
from ..cache import tax_benefit_system


def test_allocations_familiales_imposables():
    year = 2012
    reform = allocations_familiales_imposables(tax_benefit_system)
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 10,
                max = 30000,
                min = 0,
                name = 'salaire_imposable',
                ),
            ],
        period = periods.period(year),
        parent1 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        parent2 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(date_naissance = datetime.date(year - 9, 1, 1)),
            dict(date_naissance = datetime.date(year - 9, 1, 1)),
            ],
        )

    reference_simulation = scenario.new_simulation(reference = True)

    absolute_error_margin = 0.01
    af = reference_simulation.calculate_add('af', year)
    expected_af = [(12 * 399.0) * .32] * 10  # Pas de hangement de BMAF en cours d'année
    assert_near(expected_af, af, absolute_error_margin = absolute_error_margin)
    rbg = reference_simulation.calculate('rbg', year)

    reform_simulation = scenario.new_simulation()
    reform_af = reform_simulation.calculate_add('af', year)

    assert_near(expected_af, reform_af, absolute_error_margin = absolute_error_margin)
    reform_af_imposables = reform_simulation.calculate('allocations_familiales_imposables', year)
    assert_near(expected_af, reform_af_imposables, absolute_error_margin = absolute_error_margin)

    reform_rbg = reform_simulation.calculate('rbg', year)
    assert_near(reform_rbg, rbg + af, absolute_error_margin = absolute_error_margin)


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_allocations_familiales_imposables()
