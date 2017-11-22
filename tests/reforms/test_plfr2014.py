# -*- coding: utf-8 -*-

import datetime

from openfisca_core import periods
from openfisca_france.reforms.plfr2014 import plfr2014
from ..cache import tax_benefit_system

def test(year = 2013):
    max_sal = 18000
    count = 2
    people = 1
    reform = plfr2014(tax_benefit_system)
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = count,
                max = max_sal,
                min = 0,
                name = 'salaire_imposable',
                ),
            ],
        period = periods.period(year),
        parent1 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        parent2 = dict(date_naissance = datetime.date(year - 40, 1, 1)) if people >= 2 else None,
        enfants = [
            dict(date_naissance = datetime.date(year - 9, 1, 1)) if people >= 3 else None,
            dict(date_naissance = datetime.date(year - 9, 1, 1)) if people >= 4 else None,
            ] if people >= 3 else None,
        )

    reference_simulation = scenario.new_simulation(use_baseline = True)
    reform_simulation = scenario.new_simulation()
    # error_margin = 1
    impots_directs = reference_simulation.calculate('impots_directs', period = year)
    reform_impots_directs = reform_simulation.calculate('impots_directs', period = year)
