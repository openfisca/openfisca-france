import datetime

from openfisca_core import periods
from openfisca_core.reforms import Reform
from openfisca_core.tools import assert_near

from openfisca_france.scenarios import init_single_entity

from ..cache import tax_benefit_system

simulation_year = 2013
simulation_period = periods.period(simulation_year)


def modify_parameters(parameters):
    parameters.impot_revenu.bareme_ir_depuis_1945.bareme[0].rate.update(period=simulation_period, value=1)
    return parameters


class ir_100_tranche_1(Reform):
    name = "Imposition à 100% dès le premier euro et jusqu'à la fin de la 1ère tranche"

    def apply(self):
        self.modify_parameters(modifier_function = modify_parameters)


def test_parametric_reform():
    reform = ir_100_tranche_1(tax_benefit_system)

    scenario = init_single_entity(reform.new_scenario(),
        axes = [[
            dict(
                count = 3,
                name = 'salaire_imposable',
                max = 100000,
                min = 0,
                ),
            ]],
        period = simulation_period,
        parent1 = dict(date_naissance = datetime.date(simulation_year - 40, 1, 1)),
        )

    reference_simulation = scenario.new_simulation(use_baseline = True)
    assert_near(reference_simulation.calculate('impots_directs', period = simulation_period), [0, -7889.20019531, -23435.52929688],
        absolute_error_margin = 1)

    reform_simulation = scenario.new_simulation()
    assert_near(
        reform_simulation.calculate('impots_directs', simulation_period),
        [0, -13900.20019531, -29446.52929688],
        absolute_error_margin = 1,
        )


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_parametric_reform()
