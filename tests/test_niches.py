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

import sys
import logging
import nose

import openfisca_france
openfisca_france.init_country()

from openfisca_core.simulations import ScenarioSimulation
from openfisca_france.model.cotisations_sociales.travail import CAT


def test_niches():
    """
    test pour un célibataire pour un revenu de 20 000 € 
    et des revenus de différentes origines
    """

#    test charges déductibles: pensions alimentaires "f6gi","f6gj","f6el","f6em","f6gp","f6gu".
    tests_list = [
#   Test pour un célibataire ayant un revenu salarial (1AJ) et pas de PA
             {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 50000,
                    },
              "output_vars" :
                    {
                     "irpp":-7934,
                    },
              },
             {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                    },
              "output_vars" :
                    {
                     "irpp":-1181,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                    },
              "output_vars" :
                    {
                     "irpp":-1181,
                    },
              },
#   Test pour un célibataire ayant un revenu salarial (1AJ) et pas un PA de type 6GI
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gi" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp":-819,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gi" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp":-860,
                    },
              },
#   Test pour un célibataire ayant un revenu salarial (1AJ) et pas un PA de type 6EL
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6el" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp":-913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6el" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp":-929,
                    },
              },
#   Test pour un célibataire ayant un revenu salarial (1AJ) et pas un PA de type 6gj
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gj" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp":-819,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gj" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp":-860,
                    },
              },
#   Test pour un célibataire ayant un revenu salarial (1AJ) et pas un PA de type 6em
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6em" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp":-913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6em" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp":-929,
                    },
              },
#   Test pour un célibataire ayant un revenu salarial (1AJ) et pas un PA de type 6gp
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gp" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp":-819,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gp" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp":-860,
                    },
              },
#   Test pour un célibataire ayant un revenu salarial (1AJ) et pas un PA de type 6gu
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gu" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp":-913,
                    },
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                     "f6gu" : 1800,
                    },
              "output_vars" :
                    {
                     "irpp":-929,
                    },
              },
            ]


    for test in tests_list:

        year = test["year"]
        simulation = ScenarioSimulation()
        simulation.set_config(year = test["year"], nmen = 1)
        simulation.set_param()

        test_case = simulation.scenario
        for variable, value in test['input_vars'].iteritems():
            if variable in ['sali']:
                test_case.indiv[0].update({ variable: value})
            else:
                test_case.declar[0].update({ variable: value})

        df = simulation.get_results_dataframe(index_by_code = True)

        passed = True
        for variable, value in test['output_vars'].iteritems():

            computed_value = (simulation.output_table.table[variable]).sum()
            test_assertion = abs(abs(computed_value) - value) < 1
            expression = "Test failed for variable %s on year %i : \n OpenFisca value : %s \n Real value : %s \n" % (variable, year, abs(computed_value), value)

            if not test_assertion:
                print expression
                passed = True
            assert passed, "Test failed for some variables"


if __name__ == '__main__':
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_niches()
#    nose.core.runmodule(argv = [__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
