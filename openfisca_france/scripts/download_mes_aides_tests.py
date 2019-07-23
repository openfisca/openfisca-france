#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Download tests from Ludwig (https://mes-aides.gouv.fr/tests/).

Usage examples:
    python openfisca_france/scripts/download_mes_aides_tests.py

    python openfisca_france/scripts/download_mes_aides_tests.py --test-ids xxx
    python openfisca_france/scripts/download_mes_aides_tests.py --test-ids xxx yyy ...

    python openfisca_france/scripts/download_mes_aides_tests.py --api-base-url http://localhost:9000
"""


import argparse
import json
import logging
import os
import sys

import requests
import yaml


# Globals


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)

source_file_dir_name = os.path.dirname(os.path.abspath(__file__))
tests_dir_path = os.path.abspath(os.path.join(source_file_dir_name, '..', 'tests', 'mes-aides.gouv.fr'))


# Functions


def fetch_json(url):
    r = requests.get(url, headers = {'User-Agent': 'OpenFisca-Script {}'.format(app_name)})
    return r.json()


def fetch_situation(api_base_url, situation_id):
    url = '{}/api/situations/{}/openfisca-request'.format(api_base_url, situation_id)
    log.info('fetch situation: GET "{}"'.format(url))
    return fetch_json(url)


def fetch_tests(api_base_url):
    url = '{}/api/public/acceptance-tests'.format(api_base_url)
    log.info('fetch tests: GET "{}"'.format(url))
    return fetch_json(url)


def iter_yaml_items(api_base_url, test):
    test_case = fetch_situation(api_base_url = api_base_url, situation_id = test['scenario']['situationId'])
    log.info('ID: {} [{}] {}'.format(test['_id'], ', '.join(sorted(test['keywords'])), test['name']))
    yield 'name', test['name'], None
    yield 'keywords', sorted(test['keywords']), None
    description = test.get('description', None)
    description_style = '|' if description is not None and len(description.split('\n')) > 1 else None
    yield 'description', description, description_style
    relative_error_margin = {
        'accepted-exact': 0.,
        'accepted-2pct': 0.02,
        'accepted-10pct': 0.1,
        }[test['currentStatus']]
    if relative_error_margin > 0:
        yield 'relative_error_margin', relative_error_margin, None
    yield 'individus', test_case['individus'], None
    yield 'familles', test_case['familles'], None
    yield 'foyers_fiscaux', test_case['foyers_fiscaux'], None
    yield 'menages', test_case['menages'], None
    yield 'output_variables', {
        expected_result['code']: expected_result['expectedValue']
        for expected_result in test['expectedResults']
        }, None


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('--api-base-url', default = 'https://mes-aides.gouv.fr', help = 'Ludwig API base URL')
    parser.add_argument('--output-dir', default = tests_dir_path, help = 'Where to write the tests')
    parser.add_argument('--tests-json', default = None, help = 'Do not download tests, use given file')
    parser.add_argument('--test-ids', default = None, help = 'Download only those IDs', nargs = '+')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = 'Increase output verbosity')
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)
    logging.getLogger("requests").setLevel(logging.WARNING)

    if not os.path.isdir(args.output_dir):
        os.makedirs(args.output_dir)

    existing_yaml_files_name = set(os.listdir(args.output_dir))

    if args.tests_json is None:
        tests_json = fetch_tests(api_base_url = args.api_base_url)
    else:
        log.info('load tests JSON file "{}"'.format(args.tests_json))
        with open(args.tests_json) as tests_json_file:
            tests_json_str = tests_json_file.read()
            tests_json = json.loads(tests_json_str)

    for test_json in tests_json:
        if args.test_ids is not None and test_json['_id'] not in args.test_ids:
            continue

        assert test_json['currentStatus'] in ('accepted-exact', 'accepted-2pct', 'accepted-10pct', 'rejected')
        if test_json['currentStatus'] == 'rejected':
            return
        last_execution = test_json['lastExecution']
        assert test_json['currentStatus'] == last_execution['status']
        if any('expectedValue' in result and 'status' in result and result['status'] not in ('accepted-exact', 'accepted-2pct') for result in last_execution['results']):
            log.info('Test "{}" doesn\'t return the expected value (yet), so skip it.'.format(test_json['_id']))
            continue

        # Write test_yaml to output_dir_path
        yaml_file_name = 'test_mes_aides_{}.yaml'.format(test_json['_id'])
        yaml_file_path = os.path.join(args.output_dir, yaml_file_name)
        with open(yaml_file_path, 'w') as yaml_file:
            for yaml_key, yaml_value, default_style in iter_yaml_items(api_base_url = args.api_base_url,
                    test = test_json):
                yaml.safe_dump({yaml_key: yaml_value}, yaml_file, allow_unicode = True, encoding = 'utf-8',
                    default_flow_style = False, default_style = default_style, indent = 2, width = 120)

        if yaml_file_name in existing_yaml_files_name:
            existing_yaml_files_name.remove(yaml_file_name)

        # Verify YAML syntax of generated file.
        with open(yaml_file_path, 'r') as yaml_file:
            scenario = yaml.load(yaml_file)
        assert isinstance(scenario, dict), (yaml_file_path, scenario, test_json)

    if args.test_ids is None:
        for file_name in sorted(existing_yaml_files_name):
            log.info('Deleting obsolete test: "{}"'.format(file_name))
            file_path = os.path.join(args.output_dir, file_name)
            os.remove(file_path)

    return 0


if __name__ == '__main__':
    sys.exit(main())
