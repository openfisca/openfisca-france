#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Generates a list of test cases scenarios (year of legislation, household composition, individual incomes) specifically designed to test
    the income tax legislation coded in OpenFisca. The test case scenarios are stored in JSON format. """


import codecs
import json
import logging
import os
import pkg_resources

from openfisca_core import conv, periods
from openfisca_france.scripts.calculateur_impots import base

log = logging.getLogger(__name__)


def add_scenario(scenario):
    json_scenario = scenario.to_json()
    return {'scenario': json_scenario}


def create_all_scenarios_to_test(directory, years):
    """
    Main function that generates a serie of test-case scenarios that can be used to construct tests of income tax simulation.
    The output scenarios are stored in separate JSON files in the directory given as argument.

    - TYPE 1 scenarios
    Description : A single childless worker + a fixed amount of wage + a fixed amount of another type of income/tax reduction
    Goal : Test that OpenFisca does takes into account rightfully each of the variables from the income tax forms (decl. 2042...)

    - TYPE 2 scenario
    Description : Scenarios with various family and income situation to test various things
    Goal : Test that OpenFisca rightfully compute the income tax, taking into account all the complex features of the legislation
    like decote, quotient familial, PPE etc.

    """
    assert os.path.isdir(os.path.join(directory)), 'ERROR : directory {} does not exist'.format(directory)


    fixed_wage_amount = 50000
    tested_income_amount = 20000
    tested_reduction_amount = 500

    for year in years:
        
        # TYPE 1 SCENARIOS

        # for variable in base.individual_income_variables_to_test + base.household_income_variables_to_test :
        #     if variable not in base.tax_benefit_system.variables:
        #         log.info("Variable {} does not exist in the tax_benefit system, no scenarios to test were created".format(variable))
        #         continue
        #     if base.tax_benefit_system.variables[variable].end != None: 
        #         if (periods.period(str(base.tax_benefit_system.variables[variable].end)[:-3]) < periods.period('{}-01'.format(year))):
        #             log.info("Variable {} is not in effect in year {}, no scenarios to tests were created for this year".format(variable, year))
        #             continue
        #     if variable in base.start_date_by_name.keys(): 
        #         if (periods.period(str(base.start_date_by_name[variable])[:-3]) > periods.period('{}-01'.format(year))):
        #             log.info("Variable {} is not in effect in year {}, no scenarios to tests were created for this year".format(variable, year))
        #             continue

        #     scenario = define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, variable: tested_income_amount})
        #     json_filename = "test" + '-' + variable + '-' + str(scenario.period.date.year)
        #     if os.path.isfile(os.path.join(directory, json_filename)):
        #         log.debug("File {} already exists".format(json_filename))
        #     with codecs.open(os.path.join(directory, json_filename + '.json'), 'w', encoding = 'utf-8') as fichier:
        #         json.dump(add_scenario(scenario), fichier, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)


        # TYPE 2 SCENARIOS

        scenario_by_variable = {
            # 'plaf_qf_domtom': TODO,
            # 'reduc_doment': TODO,
            'abat_65_or_invalid': define_single_worker_scenario(year, {'salaire_imposable': 20000},  caseP = 1, date_naissance = year - 80),
            'caseF': define_family_scenario(year, caseF = 1),
            'caseG': define_single_worker_scenario(year, {'salaire_imposable': 50000}, caseG = 1, statut_marital = u'veuf', date_naissance = year - 80),
            'caseL': define_single_worker_scenario(year, {'salaire_imposable': 50000}, caseL = 1),
            'caseP': define_family_scenario(year, caseP = 1),
            'caseS': define_family_scenario(year, caseS = 1, date_naissance1 = year - 80),
            'caseT': define_single_worker_scenario(year,  {'salaire_imposable': fixed_wage_amount}, nb_enfants = 1, nbF = 1, caseT = 1),
            'caseW': define_single_worker_scenario(year, {'salaire_imposable': 50000}, caseW = 1, date_naissance = year - 80),
            'charges_deduc_non_plafonnees_acc75a': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f6ev': 2, 'f6eu': 1000}),
            'charges_deduc_non_plafonnees_deddiv': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f6dd': tested_reduction_amount}),
            #'charges_deduc_non_plafonnees_eparet': TODO
            'charges_deduc_non_plafonnees_reparations': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f6cb': 25000, 'f6hj': 10000 , 'f6hk': 10000}),
            'charges_deduc_non_plafonnees_pens_alim': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f6gi': tested_reduction_amount, 'f6gj': tested_reduction_amount, 'f6el': tested_reduction_amount, 'f6em': tested_reduction_amount, 'f6gp': tested_reduction_amount, 'f6gu': tested_reduction_amount}),
            'credit_preetu': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7uk': 1000, 'f7vo': 2, 'f7td': 3000}, date_naissance = year - 25),
            'credit_saldom': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7db': tested_income_amount, 'f7dq': 1, 'f7dg': 1}),
            'decote': define_family_scenario(year, income_amount1 = 25000, income_amount2 = 20000),
            'f4be': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f4be': 15000}), # régime micro-foncier
            'maj_nbp': define_family_scenario(year, nbF = 1, nbG = 1, nbH = 1, nbI = 1, nbR = 1, nbJ = 1),
            'nbG': define_family_scenario(year, nbG = 1),  
            'nbI': define_family_scenario(year, nbF = 2, nbI = 1, nbH = 1),
            'nbR': define_family_scenario(year, nbR = 1),
            'plaf_qf_caseL': define_single_worker_scenario(year, {'salaire_imposable': 150000}, caseL = 1),
            'plaf_qf_casePF_nbGI': define_family_scenario(year, income_amount1 = 150000, income_amount2 = 100000, caseP = 1, caseF = 1, nbF = 2, nbG = 1, nbH = 1, nbI = 1),
            'plaf_qf_caseT': define_single_worker_scenario(year,  {'salaire_imposable': 150000}, nb_enfants = 1, nbF = 1, caseT = 1),
            'plaf_qf_caseWG': define_single_worker_scenario(year, {'salaire_imposable': 150000}, statut_marital = u'veuf', caseG = 1, caseW = 1),
            'plaf_qf_family': define_family_scenario(year, income_amount1 = 150000, income_amount2 = 100000),
            'ppe': define_family_scenario(year, income_amount1 = 15000, income_amount2 = 10000), 
            'reduc_adhcga': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'abic_impn': fixed_wage_amount, 'f7ff': tested_reduction_amount, 'f7fg': 2}),
            'reduc_autent': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'abic_impn': fixed_wage_amount, 'f7uy': tested_reduction_amount}),
            'reduc_credit_2042pro': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'abic_impn': fixed_wage_amount, 'arag_impg': fixed_wage_amount, 'f8tb': tested_reduction_amount, 'f8tc' : tested_reduction_amount, 'f8te' : tested_reduction_amount, 'f8tg' : tested_reduction_amount, 'f8ts' : tested_reduction_amount, 'f8tz' : tested_reduction_amount, 'f8wa' : tested_reduction_amount, 'f8wb' : tested_reduction_amount, 'f8wc' : tested_reduction_amount, 'f8wd' : tested_reduction_amount, 'f8we' : tested_reduction_amount, 'f8wt' : tested_reduction_amount, 'f8wr' : tested_reduction_amount, 'f8uz' : tested_reduction_amount, 'f8wu' : tested_reduction_amount, 'f8tl' : tested_reduction_amount, 'f8uw' : tested_reduction_amount}), 
            'reduc_duflot_rpinel': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7el': 200000, 'f7qc': 150000, 'f7qe': tested_reduction_amount, 'f7qh': tested_reduction_amount, 'f7qj': tested_reduction_amount, 'f7ql': tested_reduction_amount, 'f7ai': tested_reduction_amount, 'f7gh': tested_reduction_amount, 'f7fi': tested_reduction_amount}),
            'reduc_dfppce' : define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7uf': tested_reduction_amount, 'f7vc': tested_reduction_amount, 'f7xs': 1000, 'f7xt': 1000, 'f7xu': 1000, 'f7xv': 1000, 'f7xw': 1000}),
            'reduc_donapd' : define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7ud': 100, 'f7va': 100}),
            'reduc_ecpess': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount,'f7ea': 1, 'f7eb': 1, 'f7ec': 0, 'f7ef': 0, 'f7eg': 0, 'f7ed': 1}, nb_enfants = 3, nbF = 1, nbH = 2),
            'reduc_intagr': define_single_worker_scenario(year,  {'salaire_imposable': fixed_wage_amount, 'f7um': tested_income_amount, 'f2tr': tested_income_amount}),
            'reduc_malraux': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7ny': tested_reduction_amount, 'f7nx': tested_reduction_amount, 'f7re': tested_reduction_amount, 'f7rf': tested_reduction_amount, 'f7sy': tested_reduction_amount, 'f7sx': tested_reduction_amount}),
            'reduc_saldom' : define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7df': tested_income_amount, 'f7dq': 0, 'f7dg': 0}),
            'reduc_saldom2': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7dd': tested_income_amount, 'f7dl': 1}),
        }
        
        for variable in scenario_by_variable :
            scenario = scenario_by_variable[variable]
            json_filename = "test" + '-' + variable + '-' + str(scenario.period.date.year)
            if os.path.isfile(os.path.join(directory, json_filename)):
                log.debug("File {} already exists".format(json_filename))
            with codecs.open(os.path.join(directory, json_filename + '.json'), 'w', encoding = 'utf-8') as fichier:
                json.dump(add_scenario(scenario), fichier, encoding='utf-8', ensure_ascii=False, indent=2, sort_keys=True)


def define_single_worker_scenario(year, value_by_variable, 
    date_naissance = 1970, statut_marital = u'celibataire', nb_enfants = 0,
    nbF = 0, nbG = 0, nbR = 0, nbH = 0, nbI = 0, nbJ = 0, caseL = 0, caseP = 0, caseF = 0, caseW = 0, caseS = 0, caseG = 0, caseT = 0):
    """
        Function that creates a scenario from the base tax & benefits system for one entity (a single working person)
        and credit him with some incomes given in argument.

        Parameters
        ---------
        year:
        Year of income

        value_by_variable:
        List of income variables and associated amounts

    """
    assert statut_marital in [u'celibataire', u'veuf', u'divorce']
    scenario = base.tax_benefit_system.new_scenario() 
    
    parent1 = {
        "activite": u'actif',
        "date_naissance": date_naissance,
        "statut_marital": statut_marital,
        }

    enfants = []
    while (len(enfants) < nb_enfants):
        enfants.append(dict(
                    activite = u'etudiant',
                    date_naissance = str(year - 10) + '-01-01',
                    ))

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
        nbF = nbF,
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


def define_family_scenario(year, value_by_variable = {}, 
    date_naissance1 = 1970, date_naissance2 = 1970, income_amount1 = 50000, income_amount2 = 50000, nb_enfants = 3,
    nbF = 3, nbG = 0, nbR = 0, nbH = 0, nbI = 0, nbJ = 0, nbN = 0, caseP = 0, caseF = 0, caseW = 0, caseS = 0, caseG = 0):
    """
        Function that creates a scenario from the base tax & benefits system for one entity (a family with 3 children)
        and credit the parents with a given amount of wage.

        Parameters
        ---------
        year:
        Year of income

    """
    
    assert nbF + nbH + nbJ + nbN <= nb_enfants
    assert nbF >= nbG
    assert nbH >= nbI

    scenario = base.tax_benefit_system.new_scenario()

    parent1 = {
        "activite": u'actif',
        "date_naissance": date_naissance1,
        "statut_marital": u'marie',
        "salaire_imposable": income_amount1,
        }
    parent2 = {
        "activite": u'actif',
        "date_naissance": date_naissance2,
        "statut_marital": u'marie',
        "salaire_imposable": income_amount2,
        }

    enfants = [
        dict(
            activite = u'etudiant',
            date_naissance = str(year - 20) + '-01-01',
            ),
        dict(
            activite = u'etudiant',
            date_naissance = str(year - 15) + '-01-01',
            ),
        dict(
            activite = u'etudiant',
            date_naissance = str(year - 4) + '-01-01',
            ),
        ]
    while (len(enfants) < nb_enfants):
        enfants.append(enfants[2])

    famille = dict()
    menage = dict()
    foyer_fiscal = dict(
        caseF = caseF,
        caseG = caseG,
        caseP = caseP,
        caseS = caseS,
        caseW = caseW,
        nbF = nbF,
        nbG = nbG,
        nbH = nbH,
        nbI = nbI,
        nbJ = nbJ,
        nbN = nbN,
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
        parent2 = parent2,
        enfants = enfants,
        famille = famille,
        menage = menage,
        foyer_fiscal = foyer_fiscal,
        )

    scenario.suggest()
    return scenario