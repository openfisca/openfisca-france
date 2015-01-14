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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import os
import pkg_resources
import sys

from nose.tools import assert_equal

from .ipp.taxipp_utils import build_ipp2of_variables, run_OF, compare


openfisca_france_location = pkg_resources.get_distribution('openfisca-france').location
ipp_dir = os.path.join(openfisca_france_location, 'openfisca_france', 'tests', 'ipp')


def list_dta(selection):
    if selection is None:
        selection = ""
    input = []
    output = []
    for filename in os.listdir(os.path.join(ipp_dir, "base_IPP")):
        file_path = os.path.join(ipp_dir, 'base_IPP', filename)
        if filename.startswith("base_IPP_input") and filename.endswith(selection + ".dta"):
            input.append(file_path)
        elif filename.startswith("base_IPP_output") and filename.endswith(selection + ".dta"):
            output.append(file_path)

    return input, output


def comparison_taxipp(selection = None, threshold = 2, verbose = False):
    assert selection is not None, "selection should be not None"
    list_input, list_output = list_dta(selection)
    ipp2of_input_variables, ipp2of_output_variables = build_ipp2of_variables()
    last_param_scenario = "rien"
    for input_file_path, output_file_path in zip(list_input, list_output):
        print input_file_path
        check_comparison(ipp2of_input_variables, input_file_path, output_file_path, ipp2of_output_variables,
                         last_param_scenario, threshold, verbose)


def test_from_taxipp(threshold = 2, list_input = None, list_output = None, verbose = False):
    # selection : dernier mot avant le .dta : "actif-chomeur", "ISF", "famille_modeste"
    if list_input is None:
        list_input, list_output = list_dta(selection = None)
    elif list_output is None:
        list_output = [
            file_path.replace('input', 'output')
            for file_path in list_input
            ]
    ipp2of_input_variables, ipp2of_output_variables = build_ipp2of_variables()
    last_param_scenario = "rien"
    for input_file_path, output_file_path in zip(list_input, list_output):
        yield check_comparison, ipp2of_input_variables, input_file_path, output_file_path, ipp2of_output_variables, \
            last_param_scenario, threshold, verbose


def check_comparison(ipp2of_input_variables, input_file_path, output_file_path, ipp2of_output_variables,
                     last_param_scenario = "rien", threshold = 1, verbose = False):
    simulation, param_scenario = run_OF(ipp2of_input_variables, path_dta_input = input_file_path, option = 'list_dta')
    if str(param_scenario) != str(last_param_scenario):
        pbs = compare(output_file_path, ipp2of_output_variables, param_scenario, simulation, threshold,
                      verbose = verbose)
        assert_equal(len(pbs), 0, u"input_file_path={!r}, threshold={!r}, pbs={!r}".format(
            input_file_path, threshold, pbs))
        last_param_scenario = param_scenario


if __name__ == '__main__':
    import logging
    logging.basicConfig(level = logging.DEBUG, stream = sys.stdout)
    comparison_taxipp(selection = "_marie_actif-chomeur", verbose = True)
