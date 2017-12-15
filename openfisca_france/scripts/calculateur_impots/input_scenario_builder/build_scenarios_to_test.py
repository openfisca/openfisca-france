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
    
        for variable in base.individual_income_variables_to_test + base.household_income_variables_to_test :
            if variable not in base.tax_benefit_system.variables:
                log.info("Variable {} does not exist in the tax_benefit system, no tests were created".format(variable))
                continue
            for amount in tested_income_amounts:
                scenario = define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, variable: amount})
                json_filename = "test" + '-' + variable + '-' + str(scenario.period.date.year)
                if os.path.isfile(os.path.join(directory, json_filename)):
                    log.debug("File {} already exists".format(json_filename))
                with codecs.open(os.path.join(directory, json_filename + '.json'), 'w', encoding = 'utf-8') as fichier:
                    json.dump(add_scenario(scenario), fichier, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)

        # TYPE 2 SCENARIOS
        scenario_by_variable = {
            'abat_65_or_invalid': define_single_worker_scenario(year, {'salaire_imposable': 20000},  caseP = 1, date_naissance = year - 80),
            'caseF': define_family_scenario(year, caseF = 1),
            'caseG': define_single_worker_scenario(year, {'salaire_imposable': 50000}, caseG = 1, statut_marital = u'Veuf', date_naissance = year - 80),
            'caseL': define_single_worker_scenario(year, {'salaire_imposable': 50000}, caseL = 1),
            'caseP': define_family_scenario(year, caseP = 1),
            'caseS': define_family_scenario(year, caseS = 1, date_naissance1 = year - 80),
            'caseT': define_single_parent_scenario(year, caseT = 1),
            'caseW': define_single_worker_scenario(year, {'salaire_imposable': 50000}, caseW = 1, date_naissance = year - 80),
            'decote': define_family_scenario(year, income_amount1 = 25000, income_amount2 = 20000),
            'maj_nbp': define_family_scenario(year, nbG = 1, nbH = 1, nbI = 1, nbR = 1, nbJ = 1),
            'nbG': define_family_scenario(year, nbG = 1),  
            'nbI': define_family_scenario(year, nbI = 1, nbH = 1),
            'nbR': define_family_scenario(year, nbR = 1),
            'plaf_qf': define_family_scenario(year, income_amount1 = 150000, income_amount2 = 100000),
            'ppe': define_family_scenario(year, income_amount1 = 15000, income_amount2 = 10000), 
        }
        
        for variable in scenario_by_variable :
            scenario = scenario_by_variable[variable]
            json_filename = "test" + '-' + variable + '-' + str(scenario.period.date.year)
            if os.path.isfile(os.path.join(directory, json_filename)):
                log.debug("File {} already exists".format(json_filename))
            with codecs.open(os.path.join(directory, json_filename + '.json'), 'w', encoding = 'utf-8') as fichier:
                json.dump(add_scenario(scenario), fichier, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)


def define_single_worker_scenario(year, value_by_variable, date_naissance = 1970, statut_marital = u'Célibataire',
    nbG = 0, nbR = 0, nbH = 0, nbI = 0, nbJ = 0, caseL = 0, caseP = 0, caseF = 0, caseW = 0, caseS = 0, caseG = 0):
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
    assert statut_marital in [u'Célibataire', u'Veuf', u'Divorcé']
    scenario = base.tax_benefit_system.new_scenario() 
    parent1 = {
        "activite": u'Actif occupé',
        "date_naissance": date_naissance,
        "statut_marital": statut_marital,
        }
    enfants = [
        ]
    famille = dict()
    menage = dict()
    foyer_fiscal = dict(
        caseF = caseF,
        caseG = caseG,
        caseL = caseL,
        caseP = caseP,
        caseS = caseS,
        caseW = caseW,
        nbG = nbG,
        nbH = nbH,
        nbJ = nbJ,
        nbI = nbI,
        nbR = nbR,
    )

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

def define_family_scenario(year, date_naissance1 = 1970, date_naissance2 = 1970, income_amount1 = 50000, income_amount2 = 50000, 
    nbG = 0, nbR = 0, nbH = 0, nbI = 0, nbJ = 0, caseL = 0, caseP = 0, caseF = 0, caseW = 0, caseS = 0, caseG = 0):
    """
        Function that creates a scenario from the base tax & benefits system for one entity (a family with 3 children)
        and credit the parents with a given amount of wage.

        Parameters
        ---------
        year:
        Year of income

    """
    scenario = base.tax_benefit_system.new_scenario()
    parent1 = {
        "activite": u'Actif occupé',
        "date_naissance": 1970,
        "statut_marital": u'Marié',
        "salaire_imposable": income_amount1,
        }
    parent2 = {
        "activite": u'Actif occupé',
        "date_naissance": 1970,
        "statut_marital": u'Marié',
        "salaire_imposable": income_amount2,
        }
    enfants = [
        dict(
            activite = u'Étudiant, élève',
            date_naissance = str(year - 20) + '-01-01',
            ),
        dict(
            activite = u'Étudiant, élève',
            date_naissance = str(year - 15) + '-01-01',
            ),
        dict(
            activite = u'Étudiant, élève',
            date_naissance = str(year - 4) + '-01-01',
            ),
        ]
    famille = dict()
    menage = dict()
    foyer_fiscal = dict(
        caseF = caseF,
        caseG = caseG,
        caseL = caseL,
        caseP = caseP,
        caseS = caseS,
        caseW = caseW,
        nbG = nbG,
        nbH = nbH,
        nbI = nbI,
        nbJ = nbJ,
        nbR = nbR,
    )

    scenario.init_single_entity(
        period = year,
        parent1 = parent1,
        parent2 = parent2,
        enfants = enfants,
        famille = famille,
        menage = menage,
        foyer_fiscal = foyer_fiscal,
        )

    scenario.suggest()
    return scenario

def define_single_parent_scenario(year, statut_marital = u'Célibataire', date_naissance = 1970, income_amount1 = 50000, nbG = 0, nbR = 0, 
    nbI = 0, caseL = 0, caseP = 0, caseF = 0, caseW = 0, caseS = 0, caseG = 0, caseT = 1):
    """
        Function that creates a scenario from the base tax & benefits system for one entity (a single parent with 1 child)
        and credit the parents with a given amount of wage.

        Parameters
        ---------
        year:
        Year of income

    """
    assert statut_marital in [u'Célibataire', u'Veuf', u'Divorcé']
    scenario = base.tax_benefit_system.new_scenario()
    parent1 = {
        "activite": u'Actif occupé',
        "date_naissance": date_naissance,
        "statut_marital": statut_marital,
        "salaire_imposable": income_amount1,
        }
    enfants = [
        dict(
            activite = u'Étudiant, élève',
            date_naissance = str(year - 4) + '-01-01',
            ),
        ]
    famille = dict()
    menage = dict()
    foyer_fiscal = dict(
        caseF = caseF,
        caseG = caseG,
        caseL = caseL,
        caseP = caseP,
        caseS = caseS,
        caseT = caseT,
        caseW = caseW,
        nbG = nbG,
        nbI = nbI,
        nbR = nbR,
    )

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