# -*- coding: utf-8 -*-

import datetime

from nose.tools import assert_less

from openfisca_core import periods
from openfisca_france.tests import base


def test(year = 2015):
    for reform_key in ['ayrault_muet']:
        yield run, reform_key, year


def run(reform_key, year):
    max_sal = 18000
    count = 2
    people = 1
    reform = base.get_cached_reform(
        reform_key = reform_key,
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = count,
                max = max_sal,
                min = 0,
                name = 'salaire_imposable',
                ),
            ],
        period = periods.period('year', year),
        parent1 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        parent2 = dict(date_naissance = datetime.date(year - 40, 1, 1)) if people >= 2 else None,
        enfants = [
            dict(date_naissance = datetime.date(year - 9, 1, 1)) if people >= 3 else None,
            dict(date_naissance = datetime.date(year - 9, 1, 1)) if people >= 4 else None,
            ] if people >= 3 else None,
        )

    reference_simulation = scenario.new_simulation(reference = True)
    reform_simulation = scenario.new_simulation()
#    error_margin = 1

    impo = reference_simulation.calculate('impots_directs')
    reform_impo = reform_simulation.calculate('impots_directs')

if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test()
