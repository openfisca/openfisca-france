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


"""Test YAML files."""


from __future__ import division

import collections
import copy
import logging
import os

from openfisca_core import conv, periods, scenarios
from openfisca_core.tools import assert_near
import numpy as np
import yaml

from openfisca_france.tests import base


log = logging.getLogger(__name__)

options_by_dir = collections.OrderedDict((
    (
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'calculateur_impots')),
        dict(
            calculate_output = False,
            default_absolute_error_margin = 0.5,
            ignore = True,  # TODO: Remove
            reforms = ['inversion_revenus'],
            ),
        ),
    (
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'fiches_de_paie')),
        dict(
            calculate_output = False,
            default_absolute_error_margin = 0.005,
            ),
        ),
    (
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'formulas')),
        dict(
            calculate_output = False,
            default_absolute_error_margin = 0.005,
            ),
        ),
    (
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'formulas_mes_aides')),
        dict(
            calculate_output = False,
            default_absolute_error_margin = 0.005,
            ),
        ),
    (
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'mes-aides.gouv.fr')),
        dict(
            calculate_output = True,
            default_absolute_error_margin = 0.007,
            reforms = ['aides_ville_paris'],
            ),
        ),
    (
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'ui.openfisca.fr')),
        dict(
            calculate_output = False,
            default_absolute_error_margin = 0.005,
            ),
        ),
    ))


# YAML configuration


class folded_unicode(unicode):
    pass


class literal_unicode(unicode):
    pass


def dict_constructor(loader, node):
    return collections.OrderedDict(loader.construct_pairs(node))


yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dict_constructor)

yaml.add_representer(collections.OrderedDict, lambda dumper, data: dumper.represent_dict(
    (copy.deepcopy(key), value)
    for key, value in data.iteritems()
    ))
yaml.add_representer(dict, lambda dumper, data: dumper.represent_dict(
    (copy.deepcopy(key), value)
    for key, value in data.iteritems()
    ))
yaml.add_representer(folded_unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str',
    data, style='>'))
yaml.add_representer(literal_unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str',
    data, style='|'))
yaml.add_representer(np.ndarray, lambda dumper, data: dumper.represent_list(data.tolist()))
yaml.add_representer(periods.Instant, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str', str(data)))
yaml.add_representer(periods.Period, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str', str(data)))
yaml.add_representer(tuple, lambda dumper, data: dumper.represent_list(data))
yaml.add_representer(unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str', data))


# Functions


def assert_near_calculate_output(value, target_value, absolute_error_margin = 0, message = '',
        relative_error_margin = None):
    # Redefinition of assert_near that accepts to compare monthy values with yearly values.
    assert absolute_error_margin is not None or relative_error_margin is not None
    if isinstance(value, (list, tuple)):
        value = np.array(value)
    if isinstance(target_value, (list, tuple)):
        target_value = np.array(target_value)
    if isinstance(message, unicode):
        message = message.encode('utf-8')
    if isinstance(value, np.ndarray):
        if absolute_error_margin is not None:
            assert (abs(target_value - value) <= absolute_error_margin).all() \
                or (abs(target_value - value * 12) <= absolute_error_margin).all() \
                or (abs(target_value - value / 12) <= absolute_error_margin).all(), \
                '{}{} differs from {} with an absolute margin {} > {}'.format(message, value, target_value,
                    abs(target_value - value), absolute_error_margin)
        if relative_error_margin is not None:
            assert (abs(target_value - value) <= abs(relative_error_margin * target_value)).all() \
                or (abs(target_value - value * 12) <= abs(relative_error_margin * target_value)).all() \
                or (abs(target_value - value / 12) <= abs(relative_error_margin * target_value)).all(), \
                '{}{} differs from {} with a relative margin {} > {}'.format(message, value, target_value,
                    abs(target_value - value), abs(relative_error_margin * target_value))
    else:
        if absolute_error_margin is not None:
            assert abs(target_value - value) <= absolute_error_margin \
                or abs(target_value - value * 12) <= absolute_error_margin \
                or abs(target_value - value / 12) <= absolute_error_margin, \
                '{}{} differs from {} with an absolute margin {} > {}'.format(message, value, target_value,
                    abs(target_value - value), absolute_error_margin)
        if relative_error_margin is not None:
            assert abs(target_value - value) <= abs(relative_error_margin * target_value) \
                or abs(target_value - value * 12) <= abs(relative_error_margin * target_value) \
                or abs(target_value - value / 12) <= abs(relative_error_margin * target_value), \
                '{}{} differs from {} with a relative margin {} > {}'.format(message, value, target_value,
                    abs(target_value - value), abs(relative_error_margin * target_value))


def check(yaml_path, name, period_str, test, force):
    scenario = test['scenario']
    scenario.suggest()
    simulation = scenario.new_simulation(debug = True)
    output_variables = test.get(u'output_variables')
    if output_variables is not None:
        output_variables_name_to_ignore = test.get(u'output_variables_name_to_ignore') or set()
        for variable_name, expected_value in output_variables.iteritems():
            if not force and variable_name in output_variables_name_to_ignore:
                continue
            if isinstance(expected_value, dict):
                for requested_period, expected_value_at_period in expected_value.iteritems():
                    assert_near(
                        simulation.calculate(variable_name, requested_period),
                        expected_value_at_period,
                        absolute_error_margin = test.get('absolute_error_margin'),
                        message = u'{}@{}: '.format(variable_name, requested_period),
                        relative_error_margin = test.get('relative_error_margin'),
                        )
            else:
                assert_near(
                    simulation.calculate(variable_name),
                    expected_value,
                    absolute_error_margin = test.get('absolute_error_margin'),
                    message = u'{}@{}: '.format(variable_name, period_str),
                    relative_error_margin = test.get('relative_error_margin'),
                    )


def check_calculate_output(yaml_path, name, period_str, test, force):
    scenario = test['scenario']
    scenario.suggest()
    simulation = scenario.new_simulation(debug = True)
    output_variables = test.get(u'output_variables')
    if output_variables is not None:
        output_variables_name_to_ignore = test.get(u'output_variables_name_to_ignore') or set()
        for variable_name, expected_value in output_variables.iteritems():
            if not force and variable_name in output_variables_name_to_ignore:
                continue
            if isinstance(expected_value, dict):
                for requested_period, expected_value_at_period in expected_value.iteritems():
                    assert_near_calculate_output(
                        simulation.calculate_output(variable_name, requested_period),
                        expected_value_at_period,
                        absolute_error_margin = test.get('absolute_error_margin'),
                        message = u'{}@{}: '.format(variable_name, requested_period),
                        relative_error_margin = test.get('relative_error_margin'),
                        )
            else:
                assert_near_calculate_output(
                    simulation.calculate_output(variable_name),
                    expected_value,
                    absolute_error_margin = test.get('absolute_error_margin'),
                    message = u'{}@{}: '.format(variable_name, period_str),
                    relative_error_margin = test.get('relative_error_margin'),
                    )


def test(force = False, name_filter = None, options_by_path = None):
    if isinstance(name_filter, str):
        name_filter = name_filter.decode('utf-8')
    if options_by_path is None:
        options_by_path = options_by_dir
    for path, options in options_by_path.iteritems():
        if not force and options.get('ignore', False):
            log.info(u'Ignoring {}'.format(path))
            continue
        if not os.path.exists(path):
            log.warning(u'Skipping missing {}'.format(path))
            continue
        if os.path.isdir(path):
            yaml_paths = [
                os.path.join(path, filename)
                for filename in sorted(os.listdir(path))
                if filename.endswith('.yaml')
                ]
        else:
            yaml_paths = [path]

        reform_keys = options.get('reforms')
        tax_benefit_system_for_path = base.get_cached_composed_reform(
            reform_keys = reform_keys,
            tax_benefit_system = base.tax_benefit_system,
            ) if reform_keys is not None else base.tax_benefit_system

        for yaml_path in yaml_paths:
            filename_core = os.path.splitext(os.path.basename(yaml_path))[0]
            with open(yaml_path) as yaml_file:
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
                raise ValueError("Error in test {}:\n{}".format(yaml_path, yaml.dump(tests, allow_unicode = True,
                    default_flow_style = False, indent = 2, width = 120)))

            for test in tests:
                test, error = scenarios.make_json_or_python_to_test(
                    tax_benefit_system = tax_benefit_system_for_path,
                    default_absolute_error_margin = options['default_absolute_error_margin'],
                    )(test)
                if error is not None:
                    embedding_error = conv.embed_error(test, u'errors', error)
                    assert embedding_error is None, embedding_error
                    raise ValueError("Error in test {}:\n{}\nYaml test content: \n{}\n".format(yaml_path, error, yaml.dump(test, allow_unicode = True,
                        default_flow_style = False, indent = 2, width = 120)))

                if not force and test.get(u'ignore', False):
                    continue
                if name_filter is not None and name_filter not in filename_core \
                        and name_filter not in (test.get('name', u'')) \
                        and name_filter not in (test.get('keywords', [])):
                    continue
                checker = check_calculate_output if options['calculate_output'] else check
                yield checker, yaml_path, test.get('name') or filename_core, unicode(test['scenario'].period), test, \
                    force


if __name__ == "__main__":
    import argparse
    import logging
    import sys

    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('paths', help = "path (file or directory) of tests to execute", metavar = 'PATH', nargs = '*')
    parser.add_argument('-f', '--force', action = 'store_true', default = False,
        help = 'force testing of tests with "ignore" flag and formulas belonging to "ignore_output_variables" list')
    parser.add_argument('-n', '--name', default = None, help = "partial name of tests to execute")
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    if args.paths:
        options_by_path = collections.OrderedDict()
        for path in args.paths:
            path = os.path.abspath(path).rstrip(os.sep)
            dir = path if os.path.isdir(path) else os.path.dirname(path)
            options = options_by_dir.get(dir)
            if options is None:
                options = dict(
                    calculate_output = False,
                    default_absolute_error_margin = 0.005,
                    )
            options_by_path[path] = options
    else:
        options_by_path = None

    tests_found = False
    for test_index, (function, yaml_path, name, period_str, test, force) in enumerate(
            test(
                force = args.force,
                name_filter = args.name,
                options_by_path = options_by_path,
                ),
            1):
        keywords = test.get('keywords', [])
        title = "Test {}: {} {}{} - {}".format(
            test_index,
            yaml_path,
            u'[{}] '.format(u', '.join(keywords)).encode('utf-8') if keywords else '',
            name.encode('utf-8'),
            period_str,
            )
        print("=" * len(title))
        print(title)
        print("=" * len(title))
        function(yaml_path, name, period_str, test, force)
        tests_found = True
    if not tests_found:
        print("No test found!")
        sys.exit(1)

    sys.exit(0)
