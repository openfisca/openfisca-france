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
import nose
import pdb

import openfisca_france
openfisca_france.init_country()#start_from = "brut")

from openfisca_core.simulations import ScenarioSimulation
from openfisca_france.model.cotisations_sociales.travail import CAT


def test_isf_celib():
    """
    test pour un célibataire
    """
    # Comparaison avec la fiche de paie IPP calculé avec une cotisation transport correspondant à Paris ((.026)
    # alors qu'Openfisca la cacule pour Lyon (.0175)
    tests_list = [
#   Célibataires (pas de supplément familial de traitement
             {"year" : 2013,
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
        simulation = ScenarioSimulation()
        simulation.set_config(year = test["year"], nmen = 1)
        simulation.set_param()

        test_case = simulation.scenario
        for variable, value in test['input_vars'].iteritems():
            if variable in ['zone_apl']:
                test_case.menage[0].update({ variable: value})
            else:
                test_case.indiv[0].update({ variable: value})

        df = simulation.get_results_dataframe(index_by_code = True)
        for var, value in test['output_vars'].iteritems():
            
            if var in df.columns:
                val = df.loc[var][0]
            else:
                val = simulation.output_table.table[var][0]
                
            test_assertion = abs(abs(val) - value) < 1
#            expression = "Test failed for variable %s on year %i and case %s: \n OpenFisca value : %s \n Real value : %s \n" % (variable, year, test['input_vars'], abs(computed_value), value)

            if not test_assertion:
                print year
                print var
                print "OpenFisca :", val
                print "Real value :", value
                passed = False

    assert passed, "Test failed for some variables"




if __name__ == '__main__':
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_isf_celib()

