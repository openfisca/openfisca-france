# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import datetime

from openfisca_core import periods
from openfisca_core.tools import assert_near

from . import base


def check_calculation(variable, calculated_value, expected_value, error_margin):
    assert_near(calculated_value, expected_value, absolute_error_margin = error_margin)


def process_tests_list(tests_list, monthly_amount = False, default_error_margin = 1, forced_error_margin = None):
    for test in tests_list:
        error_margin = forced_error_margin if forced_error_margin else test.pop("error_margin", default_error_margin)
        simulation = simulation_from_test(test)
        for variable, expected_value in test['output_vars'].iteritems():
            calculated_value = simulation.calculate(variable).sum() / (1 * (not monthly_amount) + 12 * monthly_amount)
            yield check_calculation, variable, calculated_value, expected_value, error_margin


def simulation_from_test(test, monthly_amount = False, default_error_margin = 1, forced_error_margin = None):
    year = test["year"]
    parent1 = dict(birth = datetime.date(year - 40, 1, 1))
    menage = dict()
    foyer_fiscal = dict()
    for variable, value in test['input_vars'].iteritems():
        if variable == "age":
            parent1['birth'] = datetime.date(year - value, 1, 1)
        elif base.tax_benefit_system.column_by_name[variable].entity == 'men':
            menage[variable] = value
        elif base.tax_benefit_system.column_by_name[variable].entity == 'ind':
            parent1[variable] = value
# TODO: if the person is a child
        elif base.tax_benefit_system.column_by_name[variable].entity == 'foy':
            foyer_fiscal[variable] = value

    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = parent1,
        menage = menage,
        foyer_fiscal = foyer_fiscal,
        ).new_simulation(debug = True)

    return simulation


def check_simulation_variable(description, simulation, variable, expected_value, error_margin):
    calculated_value = simulation.calculate(variable).sum()
    yield check_calculation, variable, calculated_value, expected_value, error_margin


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def zip_period_with_values(period_str, values):
    period = periods.period(period_str)
    size = period.size
    if not isinstance(values, list):
        assert is_number(values)
        casted_values = [values / size] * size
    else:
        if size < len(values) and size == 1:
            size = len(values)
        casted_values = values
    period_list = [str(period.start.period(period.unit).offset(index)) for index in range(size)]
    return dict(zip(period_list, casted_values))
