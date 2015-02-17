#! /usr/bin/env python
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


from __future__ import division

import os
import sys

import numpy as np
from openfisca_core import conv
# from openfisca_core.tools import assert_near
import openfisca_france
import yaml


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def assert_near2(value, target_value, error_margin = 1, message = ''):
    if isinstance(value, (list, tuple)):
        value = np.array(value)
    if isinstance(target_value, (list, tuple)):
        target_value = np.array(target_value)
    if isinstance(message, unicode):
        message = message.encode('utf-8')
    if isinstance(value, np.ndarray):
        if error_margin <= 0:
            assert (target_value == value).all() or (target_value == value * 12).all() \
                or (target_value == value / 12).all(), '{}{} differs from {}'.format(message, value, target_value)
        else:
            assert (target_value - error_margin < value).all() and (value < target_value + error_margin).all() \
                or (target_value - error_margin < value * 12).all() \
                and (value * 12 < target_value + error_margin).all() \
                or (target_value - error_margin < value / 12).all() \
                and (value / 12 < target_value + error_margin).all(), \
                '{}{} differs from {} with a margin {} >= {}'.format(message, value, target_value,
                    abs(value - target_value), error_margin)
    else:
        if error_margin <= 0:
            assert target_value == value or target_value == value * 12 or target_value == value / 12, \
                '{}{} differs from {}'.format(message, value, target_value)
        else:
            assert target_value - error_margin < value < target_value + error_margin \
                or target_value - error_margin < value * 12 < target_value + error_margin \
                or target_value - error_margin < value / 12 < target_value + error_margin, \
                '{}{} differs from {} with a margin {} >= {}'.format(message, value, target_value,
                    abs(value - target_value), error_margin)


def check(test_number, test_name, scenario_data, output_variables):
    scenario = conv.check(tax_benefit_system.Scenario.make_json_to_instance(
        tax_benefit_system = tax_benefit_system,
        ))(scenario_data)
    scenario.suggest()
    simulation = scenario.new_simulation(debug = True)
    if output_variables is not None:
        for variable_name, expected_value in output_variables.iteritems():
            assert_near2(simulation.calculate(variable_name, accept_other_period = True), expected_value,
                error_margin = 0.007, message = "{}: ".format(variable_name))


def test():
    dir_path = os.path.join(os.path.dirname(__file__), 'mes-aides.gouv.fr')
    for file_name in sorted(os.listdir(dir_path), key = lambda name: int(name.split('_', 2)[1])):
        if not file_name.endswith('.yaml'):
            continue
        test_number = file_name.split('_', 2)[1]
        with open(os.path.join(dir_path, file_name)) as yaml_file:
            test = yaml.load(yaml_file)
            if test.pop('ignore', False):
                continue
            test_name = test.pop('name')
            test.pop('description')
            output_variables = test.pop('output_variables')
            scenario_data = dict(
                period = test.pop('period'),
                test_case = test,
                )
            yield check, test_number, test_name, scenario_data, output_variables


if __name__ == "__main__":
    import argparse
    import logging

    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-n', '--number', default = None, help = "number of single test to execute")
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    for function, test_number, test_name, scenario_data, output_variables in test():
        if args.number is not None and args.number != test_number:
            continue
        print("=" * 120)
        print("Test {}: {}".format(test_number, test_name.encode('utf-8')))
        print("=" * 120)
        function(test_number, test_name, scenario_data, output_variables)
