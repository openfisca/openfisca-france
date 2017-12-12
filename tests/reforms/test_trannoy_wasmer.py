
# -*- coding: utf-8 -*-

import datetime


from openfisca_core import periods
from openfisca_core.tools import assert_near
from openfisca_france.reforms.trannoy_wasmer import trannoy_wasmer
from ..cache import tax_benefit_system


def test_charge_loyer():
    year = 2013
    reform = trannoy_wasmer(tax_benefit_system)
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 10,
                max = 30000,
                min = 0,
                name = 'salaire_de_base',
                ),
            ],
        period = periods.period(year),
        parent1 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        parent2 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(date_naissance = datetime.date(year - 9, 1, 1)),
            dict(date_naissance = datetime.date(year - 9, 1, 1)),
            ],
        menage = dict(
            loyer = 1000,
            ),
        )
    reform_simulation = scenario.new_simulation()
    absolute_error_margin = 0.01

    reform_charge_loyer = reform_simulation.calculate('charge_loyer', period = year)
    assert_near(reform_charge_loyer, [1000] * 10, absolute_error_margin = absolute_error_margin)


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_charge_loyer()
