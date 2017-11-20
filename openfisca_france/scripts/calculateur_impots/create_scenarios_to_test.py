#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Generates a list of scenarios (year of legislation, household composition, individual incomes) to test, stored in JSON format."""

import sys
import codecs
import json
import os
import pkg_resources

from openfisca_france.scripts.calculateur_impots.step0_define_scenarios_to_test import define_single_worker_scenario
from openfisca_france.scripts.calculateur_impots import base


def add_scenario(scenario):
    json_scenario = scenario.to_json()
    return {'scenario': json_scenario}

def main():
    year = 2016

    directory = os.path.join(
        pkg_resources.get_distribution('OpenFisca-France').location,
        'openfisca_france',
        'tests',
        'calculateur_impots',
        'scenarios',
        )

    # Creation des scénarios pour tester la prise en compte de chaque cases de la déclaration dans calcul IRPP
    amounts = [20000]
    variable_to_test = ["chomage_imposable"] # TODO : compléter la liste (variables de ir.py ? toutes les cases ?)

    for variable in variable_to_test:
        for amount in amounts:

            scenario = define_single_worker_scenario(year, {'salaire_imposable': 50000, variable: amount})
            json_scenario = scenario.to_json()
            json_filename = "test" + '-' + variable + '-' + "of" + '-' + str(amount) + '-' + "in" + '-' + str(scenario.period.date.year)
            # string_scenario = json.dumps(json_scenario, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)
            with codecs.open(os.path.join(directory, json_filename + '.json'), 'w', encoding = 'utf-8') as fichier:
                print(fichier)
                json.dump(add_scenario(scenario), fichier, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)

    # Création des scénarios pour tester de chaque dispositifs particuliers (décôte, QF, PPE etc.) dans calcul IRPP


if __name__ == "__main__":
    sys.exit(main())
