#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Generates a list of test cases scenarios (year of legislation, household composition, individual incomes) specifically designed to test
    the income tax legislation coded in OpenFisca. The test case scenarios are stored in JSON format. """


import codecs
import json
import logging
import os
import pkg_resources

from openfisca_core import conv
from openfisca_france.scripts.calculateur_impots import base

log = logging.getLogger(__name__)


def add_scenario(scenario):
    json_scenario = scenario.to_json()
    return {'scenario': json_scenario}


def create_all_scenarios_to_test(directory):
    """
    Main function that generates a serie of test-case scenarios that can be used to construct a serie of tests.
    The output tests are stored in separate JSON files in the directory given as argument.

    - TYPE 1 scenarios
    Description : A single childless worker + a fixed amount of wage + a fixed amount of another type of income
    Output : JSON files named "test"-'income_tested'-'year'
    Goal : Test that OpenFisca does takes into account rightfully each of the cells/type of income from the income tax report,
    when computing the income tax (works only for individual incomes)

    - TYPE 2 scenario
    Description :
    Goal : Test that OpenFisca rightfully compute the income tax, taking into account all the complex features of the legislation
    like decote, quotient familial, PPE etc.

    """
    assert os.path.isdir(os.path.join(directory)), 'ERROR : directory {} does not exist'.format(directory)
    years = range(2011,2017)

    for year in years:
        
        # TYPE 1 SCENARIOS
        fixed_wage_amount = 50000
        tested_income_amounts = [20000]
    
        for variable in base.individual_income_variables_to_test:
            for amount in tested_income_amounts:
                scenario = define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, variable: amount})
                json_filename = "test" + '-' + variable + '-' + str(scenario.period.date.year)
                if os.path.isfile(os.path.join(directory, json_filename)):
                    log.debug("File {} already exists".format(json_filename))
                with codecs.open(os.path.join(directory, json_filename + '.json'), 'w', encoding = 'utf-8') as fichier:
                    json.dump(add_scenario(scenario), fichier, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)

        # TYPE 2 SCENARIOS
        # TODO


def define_single_worker_scenario(year, value_by_variable):
    """
        Function that creates a scenario from the base tax & benefits system for one entity (a single childless working person)
        and credit him with some incomes given in arguments.

        Parameters
        ---------
        year:
        Year of income

        value_by_variable:
        List of income variables and associated amounts

    """
    scenario = base.tax_benefit_system.new_scenario() # add_variable(), add_column()
    parent1 = {
        "activite": u'Actif occupé',
        "date_naissance": 1970,
        "statut_marital": u'Célibataire',
        }
    enfants = [
        ]
    famille = dict()
    menage = dict()
    foyer_fiscal = dict()

    for variable, value in value_by_variable.iteritems():
        column = base.tax_benefit_system.variables[variable]
        entity = column.entity.key

        start = 1990
        end = 2050 if column.end is None else column.end.year
        value = value if conv.test_between(start, end)(year)[1] is None else 0

        if entity == 'individu':
            parent1[variable] = value
        elif entity == 'foyer_fiscal':
            foyer_fiscal[variable] = value
        elif entity == 'famille':
            famille[variable] = value
        elif entity == 'menage':
            menage[variable] = value

    scenario.init_single_entity(
        period = year,
        parent1 = parent1,
        enfants = enfants,
        famille = famille,
        menage = menage,
        foyer_fiscal = foyer_fiscal,
        )

    scenario.suggest()
    return scenario