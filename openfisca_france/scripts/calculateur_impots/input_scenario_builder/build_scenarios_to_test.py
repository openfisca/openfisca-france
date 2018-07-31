#! /usr/bin/env python
# -*- coding: utf-8 -*-


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
    Fopnction qui génère une série de scénarios cas-types, chacun permettant de tester un dispositif de l'impôt en particulier.
    Les scénarios créés sont stockés sous format JSON dans le dossier 'directory'.
    """
    
    assert os.path.isdir(os.path.join(directory)), 'ERROR : directory {} does not exist'.format(directory)

    fixed_wage_amount = 50000
    tested_income_amount = 20000
    tested_reduction_amount = 500

    for year in years:
        
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
            'credit_assloy': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f4ba': tested_income_amount, 'f4bf': tested_reduction_amount}),
            'credit_garext': define_family_scenario(year, value_by_variable = {'f7ga': 3000, 'f7ge': 2000}, nb_enfants = 2, nbF = 1, nbH = 1),
            'credit_inthab': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7vt': tested_reduction_amount, 'f7vx': tested_reduction_amount * 2, 'f7vz': tested_reduction_amount * 3}),
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
            'reduc_invlst1': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7uy': 5000}),
            'reduc_invlst2': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7uz': 5000}),
            'reduc_patnat': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7kb': tested_reduction_amount, 'f7kc': tested_reduction_amount, 'f7kd': tested_reduction_amount, 'f7ke': tested_reduction_amount}),
            'reduc_malraux': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7ny': tested_reduction_amount, 'f7nx': tested_reduction_amount, 'f7re': tested_reduction_amount, 'f7rf': tested_reduction_amount, 'f7sy': tested_reduction_amount, 'f7sx': tested_reduction_amount}),
            'reduc_saldom' : define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7df': tested_income_amount, 'f7dq': 0, 'f7dg': 0}),
            'reduc_saldom2': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7dd': tested_income_amount, 'f7dl': 1}),
            'reduc_spfscpi': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7gq': tested_reduction_amount, 'f7fq': tested_reduction_amount * 2, 'f7fm': tested_reduction_amount * 3}),
            'reduc_spfscpi2': define_single_worker_scenario(year, {'salaire_imposable': fixed_wage_amount, 'f7gq': tested_reduction_amount}),
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
    Crée un scénario cas-type d'un célibataire sans enfants avec un certain montant de revenus
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
    Crée un scénario cas-type d'une famille avec enfants avec un certain montant de revenus
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