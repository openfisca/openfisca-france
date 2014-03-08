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


from __future__ import division


import datetime

import openfisca_france
from openfisca_france.tests.utils import process_tests_list


def test_nonsal_celib():
    """
    Test pour un célibataire
    """
    tests_list = [
             {"year" : 2013,
              "input_vars":
                    {
                     "activite": 3,
                     "rsti" : 12500,
                    },
              "output_vars" :
                     {
                      "rst": 12500,
                    }
              },
            ]
    process_tests_list(tests_list)


def test_nonsal_famille(verbose = False):
    """
    """
    tests_list = [
               {"year" : 2013,
              "input_vars":
                    {
                     "birth": datetime.date(1940, 1, 1),
                     "activite": 3,
                     "rsti" : 12500,
                    },
              "output_vars" :
                     {
                     "rst" : 12500,
                    }
              },
                  ]

    passed = True
    for test in tests_list:
        year = test["year"]

    TaxBenefitSystem = openfisca_france.init_country()
    tax_benefit_system = TaxBenefitSystem()
    passed = True
    for test in tests_list:
        year = test["year"]
        parent1 = dict(birth = datetime.date(year - 40, 1, 1))
        parent2 = dict(birth = datetime.date(year - 40, 1, 1))
        menage = dict()
        foyer_fiscal = dict()
        for variable, value in test['input_vars'].iteritems():

            if variable == "age":
                parent1['birth'] = datetime.date(year - value, 1, 1)
                parent2['birth'] = datetime.date(year - value, 1, 1)
            elif tax_benefit_system.column_by_name[variable].entity == 'men':
                menage[variable] = value
            elif tax_benefit_system.column_by_name[variable].entity == 'ind':
                parent1[variable] = value
                parent2[variable] = value
            elif tax_benefit_system.column_by_name[variable].entity == 'foy':
                foyer_fiscal[variable] = value

        simulation = tax_benefit_system.new_scenario().init_single_entity(
            parent1 = parent1,
            parent2 = parent2,
            menage = menage,
            foyer_fiscal = foyer_fiscal,
            year = year,
            ).new_simulation(debug = True)

        for variable, value in test['output_vars'].iteritems():

            computed_value = (simulation.calculate(variable)).sum()
            test_assertion = abs(abs(computed_value) - value) < 1
            expression = "Test failed for variable %s on year %i and case %s: \n OpenFisca value : %s \n Real value : %s \n" % (variable, year, test['input_vars'], abs(computed_value), value)

            if not test_assertion:
                print expression
                passed = False
            else:
                if verbose:
                    expression = "Test passed for variable %s on year %i and case %s: \n OpenFisca value : %s \n Real value : %s \n" % (variable, year, test['input_vars'], abs(computed_value), value)
                    print expression

    assert passed, "Test failed for some variables"


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_nonsal_celib()
    test_nonsal_famille()
