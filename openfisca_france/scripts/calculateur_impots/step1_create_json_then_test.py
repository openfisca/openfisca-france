#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import codecs
import hashlib
import json
import os

from openfisca_france.scripts.calculateur_impots.compare_openfisca_impots import compare

log = logging.getLogger(__name__)


def add_official(scenario, tested = False):
    json_scenario = scenario.to_json()
    fields, _ = compare(scenario, tested, verbose = False)
    fields.pop("Annee", None)
    fields.pop("Type", None)
    fields.pop("blanc", None)
    return {'scenario': json_scenario, 'resultat_officiel': fields}


def create_json(scenario, directory, var = "", tested = False, rebuild_json = False):
    """
        Function that export a given scenario and the result of the official DGFiP income tax simulation applied to this scenario,
        into a .JSON file.

        Parameters
        ----------
        scenario:
        The scenario from which to compute the simulation and to export.

        directory:
        The directory in which to store the .JSON file created.

        var: Default = ""
        The variable that the scenario aims to test

        tested: Default = True
        If tested = True, it will return the output of the test

        rebuild_json: Default = False
        If rebuild_json = True, the JSON file is rebuilt if already existing

    """

    assert os.path.exists(directory)

    json_scenario = scenario.to_json()
    string_scenario = json.dumps(json_scenario, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)
    json_filename = var + '-' + str(scenario.period.date.year) + '-' + hashlib.sha256(string_scenario).hexdigest()
    
    if not (os.path.isfile(os.path.join(directory, json_filename + '.json'))):
        with codecs.open(os.path.join(directory, json_filename + '.json'), 'w', encoding = 'utf-8') as fichier:
            json.dump(add_official(scenario, tested), fichier, encoding = 'utf-8', ensure_ascii = False, indent = 2,
                sort_keys = True)
    elif rebuild_json:
        os.remove(os.path.join(directory, json_filename + '.json'))
        with codecs.open(os.path.join(directory, json_filename + '.json'), 'w', encoding = 'utf-8') as fichier:
            json.dump(add_official(scenario, tested), fichier, encoding = 'utf-8', ensure_ascii = False, indent = 2,
                sort_keys = True)
        log.info("The JSON file {} already exists and was rebuilt".format(json_filename))
    else:
        log.info("The JSON file {} already exists and was not modified".format(json_filename))
        compare(scenario, tested, verbose = True)
    
    if add_official(scenario, tested)['resultat_officiel'] == {}:
        os.remove(os.path.join(directory, json_filename + '.json'))
        log.info("No outputs found in the JSON file {} : the file was deleted".format(json_filename))
        return None

    return json_filename