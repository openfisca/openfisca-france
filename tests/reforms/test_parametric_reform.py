# -*- coding: utf-8 -*-

import datetime

from openfisca_core import periods, reforms
from openfisca_core.reforms import Reform
from openfisca_core.tools import assert_near

from ..cache import tax_benefit_system

simulation_year = 2013
simulation_period = periods.period(simulation_year)


def modify_legislation_json(reference_legislation_json_copy):
    reference_legislation_json_copy.impot_revenu.bareme[0].rate.update(period=simulation_period, value=1)
    return reference_legislation_json_copy


class ir_100_tranche_1(Reform):
    name = u"Imposition à 100% dès le premier euro et jusqu'à la fin de la 1ère tranche"

    def apply(self):
        self.modify_legislation_json(modifier_function = modify_legislation_json)


def test_parametric_reform():
    reform = ir_100_tranche_1(tax_benefit_system)

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

    reference_simulation = scenario.new_simulation(use_baseline = True)
    assert_near(reference_simulation.calculate('impots_directs', period = simulation_period), [0, -7889.20019531, -23435.52929688],
        absolute_error_margin = .01)

    reform_simulation = scenario.new_simulation()
    assert_near(
        reform_simulation.calculate('impots_directs', simulation_period),
        [0, -13900.20019531, -29446.52929688],
        absolute_error_margin = .01,
        )


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_parametric_reform()
