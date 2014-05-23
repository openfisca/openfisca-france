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


import openfisca_france
import sys
from generate_json import export_json

TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def define_scenario(year, column_code):
    scenario = tax_benefit_system.new_scenario()
    column = tax_benefit_system.column_by_name[column_code]
    entity = column.entity

    parent1 = {
        "activite": u'Actif occupé',
        "birth": 1970,
        "cadre": True,
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
        parent1[column_code] = 1500
    elif entity == 'foy':
        foyer_fiscal[column_code] = 1500
    elif entity == 'fam':
        famille[column_code] = 1500
    elif entity == 'men':
        menage[column_code] = 1500

    scenario.init_single_entity(
        parent1 = parent1,
        parent2 = dict(),
        enfants = enfants,
        famille = famille,
        menage = menage,
        foyer_fiscal = foyer_fiscal,
        year = year,
        )
    scenario.suggest()
    return scenario


def main():
    column_code = raw_input("Which variable would you like to test ? ")
    assert column_code in tax_benefit_system.column_by_name, "This variable doesn't exist"
    for year in range(2005,2014):
        scenario = define_scenario(year,column_code)  
        export_json(scenario, True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
