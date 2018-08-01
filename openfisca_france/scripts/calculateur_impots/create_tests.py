#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Create an automatic battery of tests of the income tax legislation in OpenFisca for given tax years """


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
rebuild_option = True
years = range(2014, 2018)


calculateur_impots_path = os.path.join(
    pkg_resources.get_distribution('OpenFisca-France').location,
    'tests', 'calculateur_impots'
    )
scenarios_to_test_directory = os.path.join(calculateur_impots_path, 'scenarios')
output_json_directory = os.path.join(calculateur_impots_path, 'json')
output_yaml_directory = os.path.join(calculateur_impots_path, 'yaml')

if not os.path.exists(os.path.join(scenarios_to_test_directory)):
    log.info("Directory {} does not exist".format(scenarios_to_test_directory))
    log.info("Creating the directory...")
    os.makedirs(os.path.join(scenarios_to_test_directory))
if not os.listdir(os.path.join(scenarios_to_test_directory)):
    log.info("Directory {} is empty".format(scenarios_to_test_directory))
    log.info("Creating new scenarios to test...")
    create_all_scenarios_to_test(scenarios_to_test_directory, years)
if not os.path.exists(os.path.join(output_json_directory)):
    log.info("Directory {} does not exist".format(output_json_directory))
    log.info("Creating the directory...")
    os.makedirs(os.path.join(output_json_directory))
if not os.path.exists(os.path.join(output_yaml_directory)):
    log.info("Directory {} does not exist".format(output_yaml_directory))
    log.info("Creating the directory...")
    os.makedirs(os.path.join(output_yaml_directory))


for filename in sorted(os.listdir(scenarios_to_test_directory)):

    variable_to_test = os.path.basename(filename).split('-')[1]
    period_to_test = os.path.basename(filename).split('.')[0].split('-')[2]
    
    if rebuild_option is False:

        json_filename_prefix = variable_to_test + '-' + period_to_test
        json_filename = [json_file for json_file in os.listdir(output_json_directory) if json_file.startswith(json_filename_prefix)]
        json_exist = (len(json_filename)>0)
        if json_exist:
            log.info("JSON file for scenario {} already exists".format(filename))
            log.info("JSON file and YAML file were not rebuilt")
            continue

    with codecs.open(os.path.join(scenarios_to_test_directory, filename), 'r', encoding = 'utf-8') as fichier:
        input_data = conv.check(input_scenario_to_json)(fichier.read())
        scenario_to_test = input_data['scenario']
        json_filename = step1.create_json(
            scenario = scenario_to_test, 
            directory = output_json_directory, 
            var = variable_to_test, 
            tested = False, 
            rebuild_json = rebuild_option
            )
        if json_filename != None :
            step2.json_to_yaml(
                json_dir = output_json_directory, 
                json_filename = json_filename + '.json', 
                var = variable_to_test, 
                output_dir = output_yaml_directory)