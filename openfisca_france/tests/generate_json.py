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


import codecs
import copy
import hashlib
import json
import os
import sys

from openfisca_france.scripts.compare_openfisca_impots import compare
import openfisca_france

#TODO: vérifier que tous les import sont nécessaires, demander à manou flake8
TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def define_scenario():
    year = 2013
    scenario = tax_benefit_system.new_scenario()
    scenario.init_single_entity(
        parent1 = dict(
            activite = u'Actif occupé',
            birth = 1970,
            cadre = True,
            sali = 24000,
            statmarit = u'Célibataire',
            ),
        enfants = [
            dict(
                activite = u'Étudiant, élève',
                birth = '2002-02-01',
                ),
            dict(
                activite = u'Étudiant, élève',
                birth = '2000-04-17',
                ),
            ],
        foyer_fiscal = dict(
                f8ta =0,
            ),
        year = year,
        )
    scenario.suggest()
    return scenario


def add_official(scenario, fichier, tested = False):
    json_scenario = scenario.to_json()
    fields = compare(scenario, tested, fichier)
    return { 'scenario' : json_scenario , 'resultat_officiel' : fields }
    

def export_json(scenario, var = "", tested = True):
    json_scenario = scenario.to_json()
    string_scenario = json.dumps(json_scenario,encoding='utf-8',ensure_ascii=False,indent=2,sort_keys=True)
    h = var + hashlib.sha256(string_scenario).hexdigest() 
    if not os.path.isfile(os.path.join('json', h + '.json')):#TODO: scenario > single entity
        with codecs.open(os.path.join('json', h + '.json'),'w', encoding='utf-8') as fichier: 
            json.dump(add_official(scenario, h, tested), fichier, encoding='utf-8', ensure_ascii=False, indent=2,
                sort_keys=True) 
    else:
        compare(scenario, tested, h) 


def main():
    scenario = define_scenario()
    export_json(scenario)


if __name__ == "__main__":
    sys.exit(main())
