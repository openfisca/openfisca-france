# -*- coding: utf-8 -*-

import datetime

from openfisca_core import periods, reforms

from openfisca_france.tests.base import assert_near, tax_benefit_system


def test_parametric_reform():

    def modify_legislation_json(reference_legislation_json_copy):
        # FIXME update_legislation is deprecated.
        reform_legislation_json = reforms.update_legislation(
            legislation_json = reference_legislation_json_copy,
            path = ('children', 'ir', 'children', 'bareme', 'brackets', 0, 'rate'),
            period = simulation_period,
            value = 1,
            )
        return reform_legislation_json

    simulation_year = 2013
    simulation_period = periods.period('year', simulation_year)
    Reform = reforms.make_reform(
        key = 'ir_100_tranche_1',
        name = u"Imposition à 100% dès le premier euro et jusqu'à la fin de la 1ère tranche",
        reference = tax_benefit_system,
        )
    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)

    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'salaire_imposable',
                max = 100000,
                min = 0,
                ),
            ],
        period = simulation_period,
        parent1 = dict(date_naissance = datetime.date(simulation_year - 40, 1, 1)),
        )

    reference_simulation = scenario.new_simulation(reference = True)
    assert_near(reference_simulation.calculate('impo'), [0, -7889.20019531, -23435.52929688],
        absolute_error_margin = .01)

    reform_simulation = scenario.new_simulation()
    assert_near(reform_simulation.calculate('impo'), [0, -13900.20019531, -29446.52929688],
        absolute_error_margin = .0001)


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_parametric_reform()
