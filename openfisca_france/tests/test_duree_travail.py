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


default_period = "2014"

test_case_by_employee_type = dict(
    premiere_paie = dict(
        period = "2010-04",
        input_variables = dict(
            effectif_entreprise = 3000,
            localisation_entreprise = "75001",
            salaire_de_base = {
                "2010-04:9": 9 * 1500,
                },
            contrat_de_travail_arrivee = datetime.date(2010, 4, 19),
            taille_entreprise = 3,
            type_sal = 0,
            ),
        output_variables = dict(
            salaire_de_base = {
                "2010:05": 1500,
                "2010:06": 1500,
                },
            nombre_jours_calendaires = 12,
            ),
        ),
    )


def test_check():
    for employee_type, test_parameters in test_case_by_employee_type.iteritems():

        period = test_parameters.get("period", default_period)
        parent1 = dict(
            birth = datetime.date(periods.period(period).start.year - 40, 1, 1),
            )
        parent1.update(test_parameters['input_variables'])

        simulation = tax_benefit_system.new_scenario().init_single_entity(
            period = period,
            parent1 = parent1,
            ).new_simulation(debug = True)

        for variable, amounts in test_parameters['output_variables'].iteritems():
            if isinstance(amounts, dict):
                for period_str, amount in amounts.iteritems():
                    output = simulation.calculate(variable, period = periods.period(period_str))
                    variable_message = "{} at {}".format(variable, period_str)
                    yield assert_variable, variable_message, employee_type, amount, output
            else:
                output = simulation.calculate(variable)
                variable_message = variable
                amount = amounts
                yield assert_variable, variable_message, employee_type, amount, output


def assert_variable(variable_message, employee_type, amount, output):
    assert abs(output - amount) < .01, \
        "error for {} ({}) : should be {} instead of {} ".format(variable_message, employee_type, amount, output)
