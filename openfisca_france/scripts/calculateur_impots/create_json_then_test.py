#! /usr/bin/env python
# -*- coding: utf-8 -*-
# ######### DESCRIPTION ############
# Ce script crée un fichier json comprenant le scenario et le résultat officiel de la simulation, à partir d'une
# variable
# Que le fichier existe déjà ou non, ce script teste ensuite si le résultat officiel correspond au résultat OpenFisca
# Si un long message d'erreur apparaît, il faut supprimer le fichier créé (qui est vide)
# On attribue la valeur 1500 à la variable à tester dans le scenario, constitué d'une personne seule avec un salaire de
# 24000
# TODO: générer des tests aléatoires : on prend 5 valeurs au hasard pour autant de variables et on crée un .json. On
# s'arrête d'en créer quand on trouve une erreur dans OpenFisca (qu'on affiche).


import sys

from openfisca_core import conv

from . import base, generate_json


def define_scenario(year, column_code):
    scenario = base.tax_benefit_system.new_scenario()
    column = base.tax_benefit_system.column_by_name[column_code]
    entity = column.entity

    start = 1990 if column.start is None else column.start.year
    end = 2050 if column.end is None else column.end.year
    value = 1500 if conv.test_between(start, end)(year)[1] is None else 0
    parent1 = {
        "activite": u'Actif occupé',
        "date_naissance": 1970,
        "salaire_imposable": 24000,
        "statmarit": u'Célibataire',
        }
    enfants = [
        # dict(
        #     activite = u'Étudiant, élève',
        #     date_naissance = '2002-02-01',
        #     ),
        # dict(
        #     activite = u'Étudiant, élève',
        #     date_naissance = '2000-04-17',
        #     ),
        ]
    famille = dict()
    menage = dict()
    foyer_fiscal = dict()
    if entity == 'ind':
        parent1[column_code] = value
    elif entity == 'foy':
        foyer_fiscal[column_code] = value
    elif entity == 'fam':
        famille[column_code] = value
    elif entity == 'men':
        menage[column_code] = value
    scenario.init_single_entity(
        period = year,
        parent1 = parent1,
        # parent2 = dict(),
        enfants = enfants,
        famille = famille,
        menage = menage,
        foyer_fiscal = foyer_fiscal,
        )
    scenario.suggest()
    return scenario


def main():
    # for column_code in (
    #     'f7nu', 'f7nv', 'f7nw', 'f7nx', 'f7oz', 'f7pa', 'f7pb', 'f7pc', 'f7pe', 'f7pf', 'f7pg', 'f7pi', 'f7pj',
    #     'f7pk', 'f7pm', 'f7pn', 'f7po', 'f7pp', 'f7pq', 'f7ps', 'f7pt', 'f7pu', 'f7pv', 'f7px', 'f7py', 'f7rg',
    #     'f7rh', 'f7rj', 'f7rk', 'f7rl', 'f7rm', 'f7rn', 'f7rp', 'f7rq', 'f7rr', 'f7rs', 'f7ru', 'f7rv', 'f7rw',
    #     'f7rx', 'f7pz', 'f7qz', 'f7qe', 'f7qf', 'f7qg', 'f7qo', 'f7qp', 'f7qv', 'f7mm', 'f7ma', 'f7mb', 'f7mn',
    #     'f7lg', 'f7lh', 'f7ks', 'f7kt', 'f7li', 'f7mc', 'f7ku'): # jusqu'en 2012
    # for column_code in (
    #     'fhsa', 'fhsb', 'fhsf', 'fhsg', 'fhsc', 'fhsh', 'fhsd', 'fhsi', 'fhsk', 'fhsl', 'fhsp', 'fhsq', 'fhsm',
    #     'fhsr', 'fhsn', 'fhss', 'fhsu', 'fhsv', 'fhsw', 'fhsx', 'fhsz', 'fhta', 'fhtb', 'fhtc', 'fhoz', 'fhpa',
    #     'fhpb', 'fhpc', 'fhpe', 'fhpf', 'fhpg', 'fhpi', 'fhpj', 'fhpk', 'fhpm', 'fhpn', 'fhpo', 'fhpp', 'fhpq',
    #     'fhps', 'fhpt', 'fhpu', 'fhpv', 'fhpx', 'fhpy', 'fhrg', 'fhrh', 'fhrj', 'fhrk', 'fhrl', 'fhrm', 'fhrn',
    #     'fhrp', 'fhrq', 'fhrr', 'fhrs', 'fhru', 'fhrv', 'fhrw', 'fhrx', 'fhpz', 'fhqz', 'fhqe', 'fhqf', 'fhqg',
    #     'fhqo', 'fhqp', 'fhqv', 'fhmm', 'fhma', 'fhmb', 'fhmn', 'fhlg', 'fhlh', 'fhks', 'fhkt', 'fhli', 'fhmc',
    #     'fhku'): # 2013 uniquement
    while True:
        column_code = raw_input("Which variable would you like to test ? ")
        assert column_code in base.tax_benefit_system.column_by_name, "This variable doesn't exist"
        for year in range(2006, 2007):
            scenario = define_scenario(year, column_code)
            generate_json.export_json(scenario, var = column_code, tested = True)


if __name__ == "__main__":
    sys.exit(main())
