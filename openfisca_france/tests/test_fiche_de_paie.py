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

import datetime

from openfisca_core import periods
from openfisca_france.tests.base import tax_benefit_system
from openfisca_france.tests.fiche_de_paie import modules


def test_1():
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = "2013-12",
        parent1 = dict(
            effectif_entreprise = 3000,
            exposition_accident = 3,
            code_postal_entreprise = "75001",
            ratio_alternants = .025,
            salaire_de_base = {"2013-01:12": 12 * 3000},
            taille_entreprise = 3,
            type_sal = 1,
            ),
        menage = dict(
            zone_apl = 1,
            ),
        ).new_simulation(debug = True)
    simulation.calculate("agff_tranche_a_employe", period = "2013-12")


def iter_scenarios():
    for module in modules:
        local = dict()
        execfile(module, {}, local)
        yield local['tests'][0]


def simple_check(tests):
    for test_parameters in tests:
        test_name = test_parameters["name"]
        period = test_parameters["period"]
        parent1 = dict(
            birth = datetime.date(periods.period(period).start.year - 40, 1, 1),
            )
        parent1.update(test_parameters['input_variables'])
        simulation = tax_benefit_system.new_scenario().init_single_entity(
            period = period,
            parent1 = parent1,
            ).new_simulation(debug = True)

        for variable_name, expected_value in test_parameters['output_variables'].iteritems():
            if isinstance(expected_value, dict):
                for item_period, item_value in expected_value.iteritems():
                    check_variable(simulation, variable_name, test_name, item_period, item_value)
            else:
                check_variable(simulation, variable_name, test_name, period, expected_value)


def test_check():
    for test_parameters in iter_scenarios():
        test_name = test_parameters["name"]
        period = test_parameters["period"]
        parent1 = dict(
            birth = datetime.date(periods.period(period).start.year - 40, 1, 1),
            )
        parent1.update(test_parameters['input_variables'])
        simulation = tax_benefit_system.new_scenario().init_single_entity(
            period = period,
            parent1 = parent1,
            ).new_simulation(debug = True)

        for variable_name, expected_value in test_parameters['output_variables'].iteritems():
            if isinstance(expected_value, dict):
                for item_period, item_value in expected_value.iteritems():
                    yield check_variable, simulation, variable_name, test_name, item_period, item_value
            else:
                yield check_variable, simulation, variable_name, test_name, period, expected_value


def check_variable(simulation, variable_name, test_name, period, expected_value):
    output_value = simulation.calculate(variable_name, period)
    assert abs(output_value - expected_value) < 1, "error for {} ({}) : should be {} instead of {} ".format(
        variable_name, test_name, expected_value, output_value)


def test_decomposition(print_decomposition = False):
    from openfisca_core.decompositions import calculate, get_decomposition_json
    import json
    import os
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = "2013-01",
        parent1 = dict(
            effectif_entreprise = 3000,
            exposition_accident = 3,
            code_postal_entreprise = "75001",
            ratio_alternants = .025,
            salaire_de_base = {"2013": 12 * 3000},
            taille_entreprise = 3,
            type_sal = 0,
            ),
        menage = dict(
            zone_apl = 1,
            ),
        ).new_simulation(debug = True)

    xml_file_path = os.path.join(
        tax_benefit_system.DECOMP_DIR,
        "fiche_de_paie_decomposition.xml"
        )

    decomposition_json = get_decomposition_json(xml_file_path, tax_benefit_system)
    response = calculate(simulation, decomposition_json)
    if print_decomposition:
        print unicode(
            json.dumps(response, encoding = 'utf-8', ensure_ascii = False, indent = 2)
            )


if __name__ == '__main__':
    import argparse
    import logging
    import sys

    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-t', '--test', action = 'append', help = "filename of single YAML test to execute")
    parser.add_argument('-n', '--name', action = 'append', help = "names of variables to calculate")
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    for function, simulation, variable_name, test_name, expected_value in test_check():
        if args.test and test_name not in args.test:
            continue
        if args.name and variable_name not in args.name:
            continue
        function(simulation, variable_name, test_name, expected_value)

#    test_decomposition(print_decomposition = True)
