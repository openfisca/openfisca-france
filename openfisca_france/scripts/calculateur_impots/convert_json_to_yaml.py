#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import collections
import cStringIO
import hashlib
import json
import logging
import os
import sys

from lxml import etree
from openfisca_core import conv
import yaml

from openfisca_france import init_country
from openfisca_france.scripts.calculateur_impots.base import (
    call_tax_calculator,
    openfisca_variable_name_by_tax_calculator_code,
    transform_scenario_to_tax_calculator_inputs,
    )


app_name = os.path.splitext(os.path.basename(__file__))[0]
html_parser = etree.HTMLParser()
income_taxes_test_cases_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..',
    'french-income-taxes-test-cases', 'test_cases'))
json_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'json'))
log = logging.getLogger(app_name)
TaxBenefitSystem = init_country()
tax_benefit_system = TaxBenefitSystem()
tests_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'calculateur_impots'))
variables_name_file_path = os.path.normpath(os.path.join(income_taxes_test_cases_dir, '..',
    'output_variables_names.yaml'))


# YAML configuration


class folded_unicode(unicode):
    pass


class literal_unicode(unicode):
    pass


def dict_constructor(loader, node):
    return collections.OrderedDict(loader.construct_pairs(node))


def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())


yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dict_constructor)

yaml.add_representer(folded_unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str',
    data, style='>'))
yaml.add_representer(literal_unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str',
    data, style='|'))
yaml.add_representer(collections.OrderedDict, dict_representer)
yaml.add_representer(unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str', data))


# Converters


def input_to_json_data(value, state = None):
    return conv.pipe(
        conv.make_input_to_json(),
        conv.test_isinstance(dict),
        conv.struct(
            dict(
                resultat_officiel = conv.pipe(
                    conv.test_isinstance(dict),
                    conv.uniform_mapping(
                        conv.pipe(
                            conv.test_isinstance(basestring),
                            conv.not_none,
                            ),
                        conv.pipe(
                            conv.test_isinstance(dict),
                            conv.struct(
                                dict(
                                    code = conv.pipe(
                                        conv.test_isinstance(basestring),
                                        conv.not_none,
                                        ),
                                    name = conv.pipe(
                                        conv.test_isinstance(basestring),
                                        conv.not_none,
                                        ),
                                    value = conv.pipe(
                                        conv.test_isinstance(float),
                                        conv.not_none,
                                        ),
                                    ),
                                ),
                            conv.not_none,
                            ),
                        ),
                    conv.not_none,
                    ),
                scenario = conv.pipe(
                    conv.test_isinstance(dict),
                    conv.struct(
                        dict(
                            test_case = conv.pipe(
                                conv.test_isinstance(dict),
                                # For each entity convert its members from a dict to a list.
                                conv.uniform_mapping(
                                    conv.noop,
                                    conv.pipe(
                                        conv.test_isinstance(dict),
                                        conv.function(transform_entity_member_by_id_to_members),
                                        ),
                                    ),
                                ),
                            ),
                        default = conv.noop,
                        ),
                    tax_benefit_system.Scenario.make_json_to_instance(
                        tax_benefit_system = tax_benefit_system),
                    conv.not_none,
                    ),
                ),
            ),
        )(value, state = state or conv.default_state)


def transform_entity_member_by_id_to_members(member_by_id):
    members = []
    for id, member in member_by_id.iteritems():
        assert 'id' not in member or member['id'] == id
        member['id'] = id
        members.append(member)
    return members


# Functions


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    if not os.path.exists(income_taxes_test_cases_dir):
        os.makedirs(income_taxes_test_cases_dir)

    if os.path.exists(tests_dir):
        for filename in os.listdir(tests_dir):
            if filename.endswith(filename):
                os.remove(os.path.join(tests_dir, filename))
    else:
        os.makedirs(tests_dir)

    if os.path.exists(variables_name_file_path):
        with open(variables_name_file_path) as variables_name_file:
            name_by_year_by_code = yaml.load(variables_name_file)
    else:
        name_by_year_by_code = {}

    name_by_year_by_code_changed = False
    for json_filename in sorted(os.listdir(json_dir)):
        if not json_filename.endswith('.json'):
            continue
        log.info(u"Converting file {}...".format(json_filename))
        with open(os.path.join(json_dir, json_filename)) as json_file:
            data = conv.check(input_to_json_data)(json_file.read())
        scenario = data['scenario']
        tax_calculator_inputs = transform_scenario_to_tax_calculator_inputs(scenario)
        tax_year = scenario.period.start.year + 1
        if tax_year <= 2011:
            # Tax calculator is no more available for years before 2011.
            tax_calculator_outputs = collections.OrderedDict()
            tax_calculator_outputs_infos = data['resultat_officiel']
            for code, infos in tax_calculator_outputs_infos.iteritems():
                float_value = infos['value']
                int_value = int(float_value)
                tax_calculator_outputs[code] = int_value if float_value == int_value else float_value
                name = infos['name'].strip().rstrip(u'*').rstrip()
                name = u' '.join(name.split())  # Remove duplicate spaces.
                if name not in (u'', u'?', u'nom inconnu'):
                    name_by_year = name_by_year_by_code.setdefault(code, {})
                    current_name = name_by_year.get(tax_year)
                    if current_name is not None and current_name != name \
                            and not name.lower().endswith(current_name.lower()):
                        log.warning(u'Ignoring rename of variable {} for year {} from:\n  {}\nto:\n  {}'.format(code,
                            tax_year, current_name, name))
                    elif current_name != name:
                        name_by_year[tax_year] = name
                        name_by_year_by_code_changed = True
        else:
            page = call_tax_calculator(tax_year, tax_calculator_inputs)
            page_doc = etree.parse(cStringIO.StringIO(page), html_parser)

            codes_without_name = set()
            tax_calculator_outputs = collections.OrderedDict()
            for element in page_doc.xpath('//input[@type="hidden"][@name]'):
                code = element.get('name')
                name = None
                parent = element.getparent()
                parent_tag = parent.tag.lower()
                if parent_tag == 'table':
                    tr = parent[parent.index(element) - 1]
                    assert tr.tag.lower() == 'tr', tr
                elif parent_tag == 'tr':
                    tr = parent
                elif code == 'NAPCR':
                    name = u'Contributions sociales supplémentaires'
                else:
                    codes_without_name.add(code)
                    continue
                if name is None:
                    while True:
                        name = etree.tostring(tr[1], encoding = unicode, method = 'text').strip().rstrip(u'*').rstrip()
                        if name:
                            name = u' '.join(name.split())  # Remove duplicate spaces.
                            break
                        table = tr.getparent()
                        tr = table[table.index(tr) - 1]
                codes_without_name.discard(code)
                float_value = float(element.get('value').strip())
                int_value = int(float_value)
                tax_calculator_outputs[code] = int_value if float_value == int_value else float_value
                name_by_year = name_by_year_by_code.setdefault(code, {})
                current_name = name_by_year.get(tax_year)
                if current_name is not None and current_name != name \
                        and not name.lower().endswith(current_name.lower()):
                    log.warning(u'Renaming variable {} for year {} from:\n  {}\nto:\n  {}'.format(code, tax_year,
                        current_name, name))
                if current_name != name and (current_name is None or not name.lower().endswith(current_name.lower())):
                    name_by_year[tax_year] = name
                    name_by_year_by_code_changed = True

            assert not codes_without_name, 'Output variables {} have no name in page:\n{}'.format(
                sorted(codes_without_name), page.decode('iso-8859-1').encode('utf-8'))

        # Create or update test for "calculateur impôt".
        sorted_tax_calculator_inputs = collections.OrderedDict(sorted(tax_calculator_inputs.iteritems()))
        income_taxes_test_case_file_path = os.path.join(income_taxes_test_cases_dir, '{}.yaml'.format(
            hashlib.md5(json.dumps(sorted_tax_calculator_inputs)).hexdigest()))
        if os.path.exists(income_taxes_test_case_file_path):
            with open(income_taxes_test_case_file_path) as income_taxes_test_case_file:
                income_taxes_test_case = yaml.load(income_taxes_test_case_file)
                income_taxes_test_case['output_variables'][str(tax_year)] = collections.OrderedDict(sorted(
                    tax_calculator_outputs.iteritems()))
                income_taxes_test_case['output_variables'] = collections.OrderedDict(sorted(
                    income_taxes_test_case['output_variables'].iteritems()))
        else:
            income_taxes_test_case = collections.OrderedDict((
                ('input_variables', sorted_tax_calculator_inputs),
                ('output_variables', collections.OrderedDict((
                    (str(tax_year), collections.OrderedDict(sorted(tax_calculator_outputs.iteritems()))),
                    ))),
                ))
        with open(income_taxes_test_case_file_path, 'w') as income_taxes_test_case_file:
            yaml.dump(income_taxes_test_case, income_taxes_test_case_file, allow_unicode = True,
                default_flow_style = False, indent = 2, width = 120)

        # Create or update YAML file containing the names associated to each result code of "calculateur impôt".
        if name_by_year_by_code_changed:
            variables_name_data = collections.OrderedDict(
                (code, collections.OrderedDict(sorted(name_by_year.iteritems())))
                for code, name_by_year in sorted(name_by_year_by_code.iteritems())
                )
            with open(variables_name_file_path, 'w') as variables_name_file:
                yaml.dump(variables_name_data, variables_name_file, allow_unicode = True, default_flow_style = False,
                    indent = 2, width = 120)
            name_by_year_by_code_changed = False

        # Create or update YAML file containing OpenFisca test.
        main_input_variable_name = json_filename.split('-', 1)[0]
        test = collections.OrderedDict((
            ('name', main_input_variable_name),
            ))
        test.update(scenario.to_json())
        test['period'] = scenario.period.start.year  # Replace period string with an integer.
        test_case = test.pop('test_case', None)
        for entity_name_plural, entity_variables in test_case.iteritems():
            test[entity_name_plural] = entity_variables
        test['output_variables'] = collections.OrderedDict(sorted(
            (variable_name, variable_value)
            for variable_name, variable_value in (
                (openfisca_variable_name_by_tax_calculator_code[code], value)
                for code, value in tax_calculator_outputs.iteritems()
                )
            if variable_name is not None
            ))
        tests_file_path = os.path.join(tests_dir, '{}.yaml'.format(main_input_variable_name))
        if os.path.exists(tests_file_path):
            with open(tests_file_path) as tests_file:
                tests = yaml.load(tests_file)
                tests.append(test)
                tests.sort(key = lambda test: (test['name'], test['period']))
        else:
            tests = [test]
        with open(tests_file_path, 'w') as tests_file:
            yaml.dump(tests, tests_file, allow_unicode = True, default_flow_style = False, indent = 2, width = 120)

    return 0


if __name__ == "__main__":
    sys.exit(main())
