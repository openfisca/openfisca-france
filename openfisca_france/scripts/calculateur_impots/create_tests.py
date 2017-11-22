#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Launch an automatic battery of tests of the income tax legislation in OpenFisca for a given tax year. """


import logging

import codecs
import os
import pkg_resources

from openfisca_core import conv

from openfisca_france.scripts.calculateur_impots.subprogs import input_scenario_to_json
from openfisca_france.scripts.calculateur_impots.input_scenario_builder.build_scenarios_to_test import create_all_scenarios_to_test
from openfisca_france.scripts.calculateur_impots import (
    step1_create_json_then_test as step1,
    step2_convert_json_to_yaml as step2,
    )

log = logging.getLogger(__name__)



calculateur_impots_path =  os.path.join(pkg_resources.get_distribution('OpenFisca-France').location,
    'openfisca_france', 'tests', 'calculateur_impots')
scenarios_to_test_directory = os.path.join(calculateur_impots_path, 'scenarios')
output_json_directory = os.path.join(calculateur_impots_path, 'json')
output_yaml_directory = os.path.join(calculateur_impots_path, 'yaml')

assert os.path.isdir(os.path.join(scenarios_to_test_directory)), 'ERROR : directory {} does not exist'.format(scenarios_to_test_directory)
if not os.listdir(os.path.join(scenarios_to_test_directory)):
    log.debug("WARNING : directory {} is empty".format(scenarios_to_test_directory))
    log.debug("Creating new scenarios to test...")
    create_all_scenarios_to_test(scenarios_to_test_directory)

for filename in sorted(os.listdir(scenarios_to_test_directory)):
    with codecs.open(os.path.join(scenarios_to_test_directory, filename), 'r', encoding = 'utf-8') as fichier:
        input_data = conv.check(input_scenario_to_json)(fichier.read())
        scenario_to_test = input_data['scenario']
        variable_to_test = os.path.basename(filename).split('-',5)[1]
        json_filename = step1.create_json(scenario_to_test, directory = output_json_directory, var = variable_to_test, tested = True, rebuild_json = True)
        step2.json_to_yaml(output_json_directory, json_filename + '.json', variable_to_test, output_yaml_directory)