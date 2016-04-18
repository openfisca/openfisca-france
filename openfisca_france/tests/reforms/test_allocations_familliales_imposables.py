# -*- coding: utf-8 -*-

import datetime


from openfisca_core import periods
from openfisca_core.tools import assert_near
from openfisca_france.tests import base


def test_allocations_familiales_imposables():
    year = 2012
    reform = base.get_cached_reform(
        reform_key = 'allocations_familiales_imposables',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 10,
                max = 30000,
                min = 0,
                name = 'salaire_imposable',
                ),
            ],
        period = periods.period('year', year),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)),
            dict(birth = datetime.date(year - 9, 1, 1)),
            ],
        )

    reference_simulation = scenario.new_simulation(reference = True)

    absolute_error_margin = 0.01
    af = reference_simulation.calculate_add('af')
    expected_af = [1528.35] * 10
    assert_near(expected_af, af, absolute_error_margin = absolute_error_margin)
    rbg = reference_simulation.calculate('rbg')

    reform_simulation = scenario.new_simulation()
    reform_af = reform_simulation.calculate_add('af')

    assert_near(expected_af, reform_af, absolute_error_margin = absolute_error_margin)
    reform_af_imposables = reform_simulation.calculate('allocations_familiales_imposables')
    assert_near(expected_af, reform_af_imposables, absolute_error_margin = absolute_error_margin)

    reform_rbg = reform_simulation.calculate('rbg')
    assert_near(reform_rbg, rbg + af, absolute_error_margin = absolute_error_margin)


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_allocations_familiales_imposables()
