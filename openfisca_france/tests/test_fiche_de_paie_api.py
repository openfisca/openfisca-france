# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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


from __future__ import division

import collections
import datetime
import json
import urllib2

from openfisca_core import periods
from openfisca_france.tests.test_fiche_de_paie import test_parameters_list, assert_variable


def compute(variable, period, test_parameters):
    parent1 = dict(
        birth = datetime.date(periods.period(period).start.year - 40, 1, 1).year,
        nom_individu = "Personne 1",
        )
    parent1.update(test_parameters['input_variables'])
    test_case = {
        "familles": {
            "1": {
                "parents": [
                    "1"
                    ],
                },
            },
        "foyers_fiscaux": {
            "1": {
                "declarants": [
                    "1"
                    ],
                }
            },
        "menages": {
            "1": {
                "personne_de_reference": "1",
                }
            },
        "individus": {
            "1": parent1,
            }
        }

    simulation = dict(
        # intermediate_variables = True,
        scenarios = [dict(
            test_case = test_case,
            period = period,
            )],
        #    validate = True,
        variables = test_parameters['output_variables'].keys(),
        )
    # request = urllib2.Request('http://localhost:2014/api/1/calculate', headers = {
    request = urllib2.Request('http://api-test.openfisca.fr/api/1/calculate', headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'OpenFisca-Notebook',
        })
    try:
        response = urllib2.urlopen(request, json.dumps(simulation))
    except urllib2.HTTPError as response:
        print response.read()
        raise
    response_text = response.read()
    response_dict = json.loads(response_text, object_pairs_hook = collections.OrderedDict)
    tree = response_dict['value']
    individu = dict(*tree)['individus']['1']
    return individu[variable][period]


def test_check():
    for test_parameters in test_parameters_list:
        period = "2012-01"
        for variable, monthly_amount in test_parameters['output_variables'].iteritems():
            name = test_parameters["name"]
            period = test_parameters["period"]
            output = compute(variable, period, test_parameters)
            yield assert_variable, variable, name, monthly_amount, output


 #   print response_text
#
#if __name__ == '__main__':
#    import logging
#    import sys
#
#    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
#    test_decomposition(print_decomposition = True)
