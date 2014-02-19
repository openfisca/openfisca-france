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

import OpenFisca
from OpenFisca.comparator import compare, dic_ipp2of, run_OF
import os
dirname = os.path.dirname(__file__) 


def test_from_taxipp( selection = "famille_modeste", threshold = 1, list_input = None, list_output = None, verbose = False):
    # selection : dernier mot avant le .dta : "actif-chomeur", "ISF", "famille_modeste"
    def list_dta(date):
        input = []
        output = []
        for filename in os.listdir(dirname + "\\base_IPP"):
            path_file = dirname + '/base_IPP/' + filename
            if filename.startswith("base_IPP_input") and filename.endswith(selection + ".dta"):
                input += [path_file]   
            if filename.startswith("base_IPP_output") and filename.endswith(selection + ".dta"):
                output += [path_file]     
        return input, output

    if not list_input :
        list_input, list_output = list_dta(selection)

    elif not list_output:
        list_output = []
        for i in range(len(list_input)): 
            list_output += [list_input[i].replace('input', 'output')]
            
    dic_input,dic_output =  dic_ipp2of()
    last_param_scenar = "rien"
    for i in range(len(list_input)) :
        input = list_input[i]
        output = list_output[i]
        simulation, openfisca_output, param_scenario = run_OF(dic_input, path_dta_input = input, option= 'list_dta')
        if str(param_scenario) != str(last_param_scenar) :
            pbs = compare(output, openfisca_output, dic_output, param_scenario, simulation, threshold, verbose = verbose)
            try : 
                assert len(pbs) == 1
            except :
               print  " Avec la base dta ", input, "\n  et un seuil de ", threshold, ", les problèmes suivants ont été identifiés : \n ", pbs
            last_param_scenar = param_scenario
        else:
            pass

if __name__ == '__main__':
    test_from_taxipp(verbose = True) #list_input = ['base_IPP_input_concubin_10-02-14 16h37.dta'],