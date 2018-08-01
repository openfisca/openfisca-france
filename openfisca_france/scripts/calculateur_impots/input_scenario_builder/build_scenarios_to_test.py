#! /usr/bin/env python
# -*- coding: utf-8 -*-


import codecs
import json
import logging
import os
import pkg_resources

from openfisca_core import conv, periods
from openfisca_france.scripts.calculateur_impots import base
from openfisca_france.scripts.calculateur_impots.input_scenario_builder.base import scenario_by_variable

log = logging.getLogger(__name__)


def add_scenario(scenario):
    json_scenario = scenario.to_json()
    return {'scenario': json_scenario}


def create_all_scenarios_to_test(directory, years):
    """
    Fopnction qui génère une série de scénarios cas-types, chacun permettant de tester un dispositif de l'impôt en particulier.
    Les scénarios créés sont stockés sous format JSON dans le dossier 'directory'.
    """
    
    assert os.path.isdir(os.path.join(directory)), 'ERROR : directory {} does not exist'.format(directory)

    for year in years:
        
        scenarios = scenario_by_variable[str(year)]
        
        for variable in scenarios :
            scenario = scenarios[variable]
            json_filename = "test" + '-' + variable + '-' + str(scenario.period.date.year)
            if os.path.isfile(os.path.join(directory, json_filename)):
                log.debug("File {} already exists".format(json_filename))
            with codecs.open(os.path.join(directory, json_filename + '.json'), 'w', encoding = 'utf-8') as fichier:
                json.dump(add_scenario(scenario), fichier, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)
