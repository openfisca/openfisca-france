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


import json
import os
import sys

from biryani1.baseconv import check
import numpy as np
import openfisca_france
from openfisca_france.scripts.compare_openfisca_impots import compare_variable


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def test():
    path = os.path.join(os.path.dirname(__file__), 'json')
    err = 1
    for fichier in os.listdir(path):
        with open(os.path.join(path, fichier)) as officiel:
            try:
                content = json.load(officiel)
            except:
                print fichier
            official_result = content['resultat_officiel']
            json_scenario = content['scenario']

            scenario = check(tax_benefit_system.Scenario.make_json_to_instance(
                tax_benefit_system = tax_benefit_system))(json_scenario)

            year = json_scenario['year']
            totpac = scenario.test_case['foyers_fiscaux'].values()[0].get('personnes_a_charge')

            simulation = scenario.new_simulation()

            for code, field in official_result.iteritems():
                compare_variable(code, field, simulation, totpac, fichier, year)
                if compare_variable(code, field, simulation, totpac, fichier, year):
                    err = 0
    assert err, "Erreur"


if __name__ == "__main__":
    sys.exit(test())
