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
from openfisca_france.model.cotisations_sociales.travail import CAT


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def test_isf_celib(verbose = False):
    """
    test pour un célibataire
    """
    tests_list = [
             {"year" : 2011,
              "input_vars":
                    {
                     "sali": 50000,
                     "b1bc" : 5000,
                     "b1ab": 2500000,
                     "b2nf": 7000,
                    },
              "output_vars" :
                    {
                     "irpp": 7889,
                     "tot_impot": 2144 + 9389 ,
                     "isf_inv_pme": 3500,
                    }
              },
            ]

    passed = True
    for test in tests_list:
        year = test["year"]
        menage = dict()
        foyer_fiscal = dict()
        parent1 = dict(birth = datetime.date(year - 40, 1, 1))

        for variable, value in test['input_vars'].iteritems():

            if variable in ['zone_apl']:
                menage[variable] = value
            elif variable in ['sali', 'b1ab']:
                parent1[variable] = value
            else:
                foyer_fiscal[variable] = value

        simulation = tax_benefit_system.new_scenario().init_single_entity(
            parent1 = parent1,
            foyer_fiscal = foyer_fiscal,
            menage = menage,
            year = year,
            ).new_simulation(debug = True)

        for variable, value in test['output_vars'].iteritems():

            calculated_value = (simulation.calculate(variable)).sum()
            test_assertion = abs(abs(calculated_value) - value) < 1
            expression = "Test failed for variable %s on year %i and case %s: \n OpenFisca value : %s \n Real value : %s \n" % (variable, year, test['input_vars'], abs(calculated_value), value)

            if not test_assertion:
                print expression
                passed = False
            else:
                if verbose:
                    expression = "Test passed for variable %s on year %i and case %s: \n OpenFisca value : %s \n Real value : %s \n" % (variable, year, test['input_vars'], abs(calculated_value), value)
                    print expression

    assert passed, "Test failed for some variables"



if __name__ == '__main__':
    import sys
    import logging
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_isf_celib()

