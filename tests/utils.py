# -*- coding: utf-8 -*-

import datetime

from openfisca_core import periods
from openfisca_core.tools import assert_near
from nose.tools import nottest

from .cache import tax_benefit_system


def check_calculation(variable, calculated_value, expected_value, error_margin):
    assert_near(calculated_value, expected_value, absolute_error_margin = error_margin)

@nottest  # this function should not be considered as a test by nosetests
def process_tests_list(tests_list, monthly_amount = False, default_error_margin = 1, forced_error_margin = None):
    for test in tests_list:
        error_margin = forced_error_margin if forced_error_margin else test.pop("error_margin", default_error_margin)
        simulation = simulation_from_test(test)
        for variable, expected_value in test['output_vars'].items():
            calculated_value = simulation.calculate(variable).sum() / (1 * (not monthly_amount) + 12 * monthly_amount)
            yield check_calculation, variable, calculated_value, expected_value, error_margin

@nottest  # this function should not be considered as a test by nosetests
def simulation_from_test(test, monthly_amount = False, default_error_margin = 1, forced_error_margin = None):
    year = test["year"]
    parent1 = dict(date_naissance = datetime.date(year - 40, 1, 1))
    menage = dict()
    foyer_fiscal = dict()
    for variable, value in test['input_vars'].items():
        if variable == "age":
            parent1['date_naissance'] = datetime.date(year - value, 1, 1)
        elif tax_benefit_system.variables[variable].entity == 'men':
            menage[variable] = value
        elif tax_benefit_system.variables[variable].entity == 'ind':
            parent1[variable] = value
# TODO: if the person is a child
        elif tax_benefit_system.variables[variable].entity == 'foy':
            foyer_fiscal[variable] = value

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = parent1,
        menage = menage,
        foyer_fiscal = foyer_fiscal,
        ).new_simulation()

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
