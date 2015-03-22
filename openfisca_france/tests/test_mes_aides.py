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

import collections
import os

import numpy as np
from openfisca_core import conv, scenarios
from openfisca_france.tests.base import tax_benefit_system
import yaml


# YAML configuration


def dict_constructor(loader, node):
    return collections.OrderedDict(loader.construct_pairs(node))


yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dict_constructor)


# Functions


def assert_near2(value, target_value, absolute_error_margin = 0, message = '', relative_error_margin = None):
    # Redefinition of assert_near that accepts to compare monthy values with yearly values.
    assert absolute_error_margin is not None or relative_error_margin is not None
    if isinstance(value, (list, tuple)):
        value = np.array(value)
    if isinstance(target_value, (list, tuple)):
        target_value = np.array(target_value)
    if isinstance(message, unicode):
        message = message.encode('utf-8')
    if isinstance(value, np.ndarray):
        if absolute_error_margin is not None and absolute_error_margin <= 0 \
                or relative_error_margin is not None and relative_error_margin <= 0:
            assert (target_value == value).all() or (target_value == value * 12).all() \
                or (target_value == value / 12).all(), '{}{} differs from {}'.format(message, value, target_value)
        else:
            if absolute_error_margin is not None:
                assert (abs(target_value - value) < absolute_error_margin).all() \
                    or (abs(target_value - value * 12) < absolute_error_margin).all() \
                    or (abs(target_value - value / 12) < absolute_error_margin).all(), \
                    '{}{} differs from {} with an absolute margin {} >= {}'.format(message, value, target_value,
                        abs(target_value - value), absolute_error_margin)
            if relative_error_margin is not None:
                assert (abs(target_value - value) < abs(relative_error_margin * target_value)).all() \
                    or (abs(target_value - value * 12) < abs(relative_error_margin * target_value)).all() \
                    or (abs(target_value - value / 12) < abs(relative_error_margin * target_value)).all(), \
                    '{}{} differs from {} with a relative margin {} >= {}'.format(message, value, target_value,
                        abs(target_value - value), abs(relative_error_margin * target_value))
    elif absolute_error_margin is not None and absolute_error_margin <= 0 \
            or relative_error_margin is not None and relative_error_margin <= 0:
        assert target_value == value or target_value == value * 12 or target_value == value / 12, \
            '{}{} differs from {}'.format(message, value, target_value)
    else:
        if absolute_error_margin is not None:
            assert abs(target_value - value) < absolute_error_margin \
                or abs(target_value - value * 12) < absolute_error_margin \
                or abs(target_value - value / 12) < absolute_error_margin, \
                '{}{} differs from {} with an absolute margin {} >= {}'.format(message, value, target_value,
                    abs(target_value - value), absolute_error_margin)
        if relative_error_margin is not None:
            assert abs(target_value - value) < abs(relative_error_margin * target_value) \
                or abs(target_value - value * 12) < abs(relative_error_margin * target_value) \
                or abs(target_value - value / 12) < abs(relative_error_margin * target_value), \
                '{}{} differs from {} with a relative margin {} >= {}'.format(message, value, target_value,
                    abs(target_value - value), abs(relative_error_margin * target_value))


def check(name, period_str, test):
    scenario = test['scenario']
    scenario.suggest()
    simulation = scenario.new_simulation(debug = True)
    output_variables = test.get(u'output_variables')
    if output_variables is not None:
        for variable_name, expected_value in output_variables.iteritems():
            if isinstance(expected_value, dict):
                for requested_period, expected_value_at_period in expected_value.iteritems():
                    assert_near2(
                        simulation.calculate(variable_name, requested_period, accept_other_period = True),
                        expected_value_at_period,
                        absolute_error_margin = test.get('absolute_error_margin'),
                        message = u'{}@{}: '.format(variable_name, requested_period),
                        relative_error_margin = test.get('relative_error_margin'),
                        )
            else:
                assert_near2(
                    simulation.calculate(variable_name, accept_other_period = True),
                    expected_value,
                    absolute_error_margin = test.get('absolute_error_margin'),
                    message = u'{}@{}: '.format(variable_name, period_str),
                    relative_error_margin = test.get('relative_error_margin'),
                    )


def test(name_filter = None):
    if isinstance(name_filter, str):
        name_filter = name_filter.decode('utf-8')
    dir_path = os.path.join(os.path.dirname(__file__), 'mes-aides.gouv.fr')
    for filename in sorted(os.listdir(dir_path)):
        if not filename.endswith('.yaml'):
            continue
        filename_core = os.path.splitext(filename)[0]
        with open(os.path.join(dir_path, filename)) as yaml_file:
            tests = yaml.load(yaml_file)
        tests, error = conv.pipe(
            conv.make_item_to_singleton(),
            conv.uniform_sequence(
                conv.noop,
                drop_none_items = True,
                ),
            )(tests)
        if error is not None:
            embedding_error = conv.embed_error(tests, u'errors', error)
            assert embedding_error is None, embedding_error
            conv.check((tests, error))  # Generate an error.

        for test in tests:
            test, error = scenarios.make_json_or_python_to_test(tax_benefit_system,
                default_absolute_error_margin = 0.007)(test)
            if error is not None:
                embedding_error = conv.embed_error(test, u'errors', error)
                assert embedding_error is None, embedding_error
                conv.check((test, error))  # Generate an error.

            if test.get(u'ignore', False):
                continue
            if name_filter is not None and name_filter not in filename_core \
                    and name_filter not in (test.get('name', u'')) \
                    and name_filter not in (test.get('keywords', [])):
                continue
            yield check, test.get('name') or filename_core, unicode(test['scenario'].period), test


if __name__ == "__main__":
    import argparse
    import logging
    import sys

    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-n', '--name', default = None, help = "partial name of tests to execute")
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    for test_index, (function, name, period_str, test) in enumerate(test(name_filter = args.name), 1):
        keywords = test.get('keywords', [])
        title = "Test {}: {}{} - {}".format(
            test_index,
            u'[{}] '.format(u', '.join(keywords)).encode('utf-8') if keywords else '',
            name.encode('utf-8'),
            period_str,
            )
        print("=" * len(title))
        print(title)
        print("=" * len(title))
        function(name, period_str, test)
