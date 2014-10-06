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
## Ce programme teste tous les fichiers .json créés par un script et renvoie les erreurs d'OpenFisca

import datetime
import json
import os
import sys


from biryani1.baseconv import check


import openfisca_france
from openfisca_france.scripts.compare_openfisca_impots import compare_variable


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def compare_json(json_file):
    content = json.load(json_file)
    try:
        official_result = content['resultat_officiel']
    except:
        print json.dumps(json_file, encoding = 'utf-8', ensure_ascii = False, indent = 2)
    json_scenario = content['scenario']

    scenario = check(tax_benefit_system.Scenario.make_json_to_instance(
        tax_benefit_system = tax_benefit_system))(json_scenario)

    if 'year' not in json_scenario:
        print json.dumps(json_scenario, encoding = 'utf-8', ensure_ascii = False, indent = 2)
        date = datetime.datetime.strptime(json_scenario['date'], "%Y-%m-%d")
        year = date.year
    else:
        year = json_scenario['year']

    totpac = scenario.test_case['foyers_fiscaux'].values()[0].get('personnes_a_charge')
    simulation = scenario.new_simulation()

    for code, field in official_result.iteritems():
        return compare_variable(code, field, simulation, totpac, json_file, year)


def test():
    path = os.path.join(os.path.dirname(__file__), 'json')
    for json_file_path in os.listdir(path):
        with open(os.path.join(path, json_file_path)) as json_file:
            yield compare_json, json_file


if __name__ == "__main__":
    sys.exit(test())
