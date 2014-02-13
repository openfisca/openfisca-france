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
import datetime
import logging

import openfisca_france
openfisca_france.init_country(start_from = "brut")

from openfisca_core.simulations import ScenarioSimulation
from openfisca_france.model.cotisations_sociales.travail import CAT


def test_nonsal_celib():
    """
    test pour un célibataire
    """
    tests_list = [
#   Célibataires à partir de : http://www.experts-comptables.fr/csoec/Focus-bases-documentaires/Auto-Entrepreneur/Simulateur-Auto-Entrepreneur-version-entreprise
             {"year" : 2013,
              "input_vars":
                    {
                     "ebic_impv" : 20000,
                    },
              "output_vars" :
                     {
                      "rev_microsocial": 20000-2820, 
                      "microsocial" : 200,
                    }
              },
            {"year" : 2013,
              "input_vars":
                    {
                     "ebic_imps" : 20000,
                    },
              "output_vars" :
                     {
                      "rev_microsocial": 20000-4920, 
                      "microsocial" : 340,
                    }
              },
                               {"year" : 2013,
              "input_vars":
                    {
                     "ebnc_impo" : 20000,
                    },
              "output_vars" :
                     {
                      "rev_microsocial": 20000-4920, 
                      "microsocial" : 440,
                    }
              },
            ]

    passed = True
    for test in tests_list:
        year = test["year"]
        simulation = ScenarioSimulation()
        simulation.set_config(year = test["year"], nmen = 1)
        simulation.set_param()

        test_case = simulation.scenario
        for variable, value in test['input_vars'].iteritems():
                if variable in ['ebic_impv', 'ebic_imps', 'ebnc_impo']:
                    test_case.indiv[0].update({variable: value})
                else:
                    print variable
                    assert False

        for variable, value in test['output_vars'].iteritems():
            df = simulation.get_results_dataframe(index_by_code = True)
            if variable in df.columns:
                val = df.loc[variable][0]
            else:
                val = simulation.output_table.table[variable][0]
            to_test = abs(val - value)
            if not (to_test < 1):
                print "Il y a une différence : ", to_test
                print "Pour le scénario", test['input_vars']
                print year
                print variable
                print "OpenFisca :", val
                print "Real value :", value , "\n \n"

    assert passed, "Test failed for some variables"


def test_nonsal_famille():
    """
    test pour un couple de fonctionnaire
    """
    tests_list = [
# Couple de microentrepreneur
               {"year" : 2013,
              "input_vars":
                    {
                     "ebic_impv" : 20000,
                      "ebic_impv_c" : 10000,
                    },
              "output_vars" :
                     {
                      "rev_microsocial": (20000 + 10000) - (2820 + 1410), 
                      "microsocial" : 200 + 100,
                    }
              },
                  ]
    
    passed = True
    for test in tests_list:
        year = test["year"]
        simulation = ScenarioSimulation()
        simulation.set_config(year = test["year"], nmen = 1)
        simulation.set_param()
        test_case = simulation.scenario
        test_case.addIndiv(1, datetime.date(1975, 1, 1), 'conj', 'part')
        
        for variable, value in test['input_vars'].iteritems():
                if variable in ['ebic_impv', 'ebic_imps', 'ebnc_impo']:
                    test_case.indiv[0].update({variable: value})
                elif variable in ['ebic_impv_c', 'ebic_imps_c', 'ebnc_impo_c']:
                    test_case.indiv[1].update({variable[:-2]: value})
                else:
                    print variable
                    assert False

        for variable, value in test['output_vars'].iteritems():
            df = simulation.get_results_dataframe(index_by_code = True)
            if variable in df.columns:
                val = df.loc[variable][0]
            else:
                val = simulation.output_table.table[variable][0]
            to_test = abs(val - value)
            if not (to_test < 1):
                print "Il y a une différence : ", to_test
                print "Pour le scénario", test['input_vars']
                print year
                print variable
                print "OpenFisca :", val
                print "Real value :", value , "\n \n"

    assert passed, "Test failed for some variables"


if __name__ == '__main__':
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_nonsal_celib()
    test_nonsal_famille()
