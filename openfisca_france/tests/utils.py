# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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

import openfisca_france


def process_tests_list(tests_list, verbose = False, monthly_amount = False, default_error_margin = 1, forced_error_margin = None):
    TaxBenefitSystem = openfisca_france.init_country()
    tax_benefit_system = TaxBenefitSystem()

    for test in tests_list:

        if forced_error_margin:
            error_margin = forced_error_margin
        else:
            error_margin = test.pop("error_margin", default_error_margin)

        simulation = simulation_from_test(test)

        for variable, expected_value in test['output_vars'].iteritems():
            calculated_value = (simulation.calculate(variable)).sum() / (1 * (not monthly_amount) + 12 * monthly_amount)
            assert abs(calculated_value - expected_value) < error_margin, u'Variable "{} = {}. Expected: {}'.format(
                variable, calculated_value, expected_value)


def simulation_from_test(test, verbose = False, monthly_amount = False, default_error_margin = 1, forced_error_margin = None):
    TaxBenefitSystem = openfisca_france.init_country()
    tax_benefit_system = TaxBenefitSystem()

    year = test["year"]

    parent1 = dict(birth = datetime.date(year - 40, 1, 1))
    menage = dict()
    foyer_fiscal = dict()
    for variable, value in test['input_vars'].iteritems():

        if variable == "age":
            parent1['birth'] = datetime.date(year - value, 1, 1)
        elif tax_benefit_system.column_by_name[variable].entity == 'men':
            menage[variable] = value
        elif tax_benefit_system.column_by_name[variable].entity == 'ind':
            parent1[variable] = value
#TODO: if the person is a child
        elif tax_benefit_system.column_by_name[variable].entity == 'foy':
            foyer_fiscal[variable] = value

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        date = datetime.date(year , 1, 1),
        parent1 = parent1,
        menage = menage,
        foyer_fiscal = foyer_fiscal,
        ).new_simulation(debug = True)

    return simulation


def check_simulation_variable(description, simulation, variable, expected_value, error_margin):
    calculated_value = (simulation.calculate(variable)).sum()
    assert abs(calculated_value - expected_value) < error_margin, u'Variable "{} = {}. Expected: {}'.format(
        variable, calculated_value, expected_value)
