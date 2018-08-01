#! /usr/bin/env python
# -*- coding: utf-8 -*-


from openfisca_core import conv, periods
from openfisca_france.scripts.calculateur_impots import base



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