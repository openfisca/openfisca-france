#! /usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import logging
import os

from openfisca_core import conv
import yaml

from openfisca_france.scripts.calculateur_impots.subprogs import *


log = logging.getLogger(__name__)


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


def json_to_yaml(json_dir, json_filename, var, output_dir):
    """
    Function that convert a JSON file into a YAML file containing a test in a syntax understandable by OpenFisca
    A test = a name, a period, a test case scenario, and output variables

    Parameters
    ---------- 
    json_dir:
    The directory containing the input JSON file

    json_filename:
    The name of the input JSON file (the file must contain a field 'resultat_officiel' and a field 'scenario')

    var:
    The variable tested (ex: chomage_imposable, aac_defn, f2ch ..)

    output_dir:
    The output directory where to stock the output YAML file

    """
    
    assert os.path.exists(output_dir)

    log.info(u"Converting file {}...".format(json_filename))
    with open(os.path.join(json_dir, json_filename)) as json_file:
        data = conv.check(input_to_json_data)(json_file.read()) 

    scenario = data['scenario']

    log.info(u"Creating the YAML test from file {}...".format(json_filename))
    test = collections.OrderedDict((
            ('name', var),
        ))
    test.update(scenario.to_json())
    test['period'] = scenario.period.start.year
    test['absolute_error_margin'] = 1
    test_case = test.pop('test_case', None)
    for entity_name_plural, entity_variables in test_case.iteritems():
        test[entity_name_plural] = entity_variables
    test['output_variables'] = collections.OrderedDict(sorted(
        (value_by_key['openfisca_name'], value_by_key['value'])
            for code, value_by_key in data['resultat_officiel'].iteritems()
            if value_by_key['openfisca_name'] is not None
        ))

    tests_file_path = os.path.join(output_dir, '{}.yaml'.format(var))
    if os.path.exists(tests_file_path):
        with open(tests_file_path) as tests_file:
            tests = yaml.load(tests_file)
            add_new_test = True
            for i in range (0,len(tests)):
                if (test['name'] == tests[i]['name']) & (test['period'] == tests[i]['period']):
                    add_new_test = False
                    log.debug("The test was not added to the file because a test with same name and period already exists")
            if add_new_test:    
                tests.append(test)
                tests.sort(key = lambda test: (test['name'], test['period']))
    else:
        tests = [test]

    with open(tests_file_path, 'w') as tests_file:
        yaml.dump(tests, tests_file, allow_unicode = True, default_flow_style = False, indent = 2, width = 120)