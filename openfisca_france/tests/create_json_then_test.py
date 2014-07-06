#! /usr/bin/env python
# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

########### DESCRIPTION ############
## Ce script crée un fichier json comprenant le scenario et le résultat officiel de la simulation, à partir d'une variable
## Que le fichier existe déjà ou non, ce script teste ensuite si le résultat officiel correspond au résultat OpenFisca
## Si un long message d'erreur apparaît, il faut supprimer le fichier créé (qui est vide)
## On attribue la valeur 1500 à la variable à tester dans le scenario, constitué d'une personne seule avec un salaire de 24000
#TODO: générer des tests aléatoires : on prend 5 valeurs au hasard pour autant de variables et on crée un .json. On s'arrête d'en créer quand on trouve une erreur dans OpenFisca (qu'on affiche).

import openfisca_france
import sys
from generate_json import export_json
import os
from datetime import date

from openfisca_core import conv
TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def define_scenario(year, column_code):
    scenario = tax_benefit_system.new_scenario()
    column = tax_benefit_system.column_by_name[column_code]
    entity = column.entity

    start = 1990 if column.start == None else column.start.year
    end = 2050 if column.end == None else column.end.year
    value = 1500 if conv.test_between(start, end)(year)[1] == None else 0
    parent1 = {
        "activite": u'Actif occupé',
        "birth": 1970,
        "sali": 24000,
        "statmarit": u'Célibataire',
        }
    enfants = [
#        dict(
#            activite = u'Étudiant, élève',
#            birth = '2002-02-01',
#            ),
#        dict(
#            activite = u'Étudiant, élève',
#            birth = '2000-04-17',
#            ),
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
        parent1 = parent1,
#        parent2 = dict(),
        enfants = enfants,
        famille = famille,
        menage = menage,
        foyer_fiscal = foyer_fiscal,
        year = year,
        )
    scenario.suggest()
    return scenario


def main():
#    for column_code in ('f7nu', 'f7nv', 'f7nw', 'f7nx', 'f7oz', 'f7pa', 'f7pb', 'f7pc', 'f7pe', 'f7pf', 'f7pg', 'f7pi', 'f7pj', 'f7pk', 'f7pm', 'f7pn', 'f7po', 'f7pp', 'f7pq', 'f7ps', 'f7pt', 'f7pu', 'f7pv', 'f7px', 'f7py', 'f7rg', 'f7rh', 'f7rj', 'f7rk', 'f7rl', 'f7rm', 'f7rn', 'f7rp', 'f7rq', 'f7rr', 'f7rs', 'f7ru', 'f7rv', 'f7rw', 'f7rx', 'f7pz', 'f7qz', 'f7qe', 'f7qf', 'f7qg', 'f7qo', 'f7qp', 'f7qv', 'f7mm', 'f7ma', 'f7mb', 'f7mn', 'f7lg', 'f7lh', 'f7ks', 'f7kt', 'f7li', 'f7mc', 'f7ku'): # jusqu'en 2012
#    for column_code in ('fhsa', 'fhsb', 'fhsf', 'fhsg', 'fhsc', 'fhsh', 'fhsd', 'fhsi', 'fhsk', 'fhsl', 'fhsp', 'fhsq', 'fhsm', 'fhsr', 'fhsn', 'fhss', 'fhsu', 'fhsv', 'fhsw', 'fhsx', 'fhsz', 'fhta', 'fhtb', 'fhtc', 'fhoz', 'fhpa', 'fhpb', 'fhpc', 'fhpe', 'fhpf', 'fhpg', 'fhpi', 'fhpj', 'fhpk', 'fhpm', 'fhpn', 'fhpo', 'fhpp', 'fhpq', 'fhps', 'fhpt', 'fhpu', 'fhpv', 'fhpx', 'fhpy', 'fhrg', 'fhrh', 'fhrj', 'fhrk', 'fhrl', 'fhrm', 'fhrn', 'fhrp', 'fhrq', 'fhrr', 'fhrs', 'fhru', 'fhrv', 'fhrw', 'fhrx', 'fhpz', 'fhqz', 'fhqe', 'fhqf', 'fhqg', 'fhqo', 'fhqp', 'fhqv', 'fhmm', 'fhma', 'fhmb', 'fhmn', 'fhlg', 'fhlh', 'fhks', 'fhkt', 'fhli', 'fhmc', 'fhku'): # 2013 uniquement
    while 1:
        column_code = raw_input("Which variable would you like to test ? ")
        assert column_code in tax_benefit_system.column_by_name, "This variable doesn't exist"        
        for year in range(2007,2014):
            scenario = define_scenario(year,column_code)
            export_json(scenario, var = column_code, tested = True)

if __name__ == "__main__":
    sys.exit(main())
