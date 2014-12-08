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


from openfisca_france.tests.base import tax_benefit_system


#def test_1():
#    simulation = tax_benefit_system.new_scenario().init_single_entity(
#        period = "2013-01-01",
#        parent1 = dict(
#            effectif_entreprise = 3000,
#            exposition_accident = 3,
#            localisation_entreprise = "75001",
#            ratio_alternants = .025,
#            salbrut = 3000,
#            taille_entreprise = 3,
#            type_sal = 0,
#            ),
#        menage = dict(
#            zone_apl = 1,
#            ),
#        ).new_simulation(debug = True)
#    simulation.calculate("allegement_fillon")
#    simulation.calculate("maladie_employeur")

test_case_by_employee_type = dict(
    exemple_circ_acoss_2011 = dict(
        input_variables = dict(
            effectif_entreprise = 3000,
            localisation_entreprise = "75001",
            salbrut = { # 9 smic horaire 2011
                "2011-01": 35 * 52 / 12 * 9,
                "2011-02": 35 * 52 / 12 * 9,
                "2011-03": 35 * 52 / 12 * 9,
                "2011-04": 35 * 52 / 12 * 9,
                "2011-05": 35 * 52 / 12 * 9,
                "2011-06": 35 * 52 / 12 * 9,
                "2011-07": 35 * 52 / 12 * 9,
                "2011-08": 35 * 52 / 12 * 9,
                "2011-09": 35 * 52 / 12 * 9 + 1000,
                "2011-10": 35 * 52 / 12 * 9,
                "2011-11": 35 * 52 / 12 * 9,
                "2011-12": 35 * 52 / 12 * 9 * 2,
                },
            taille_entreprise = 3,
            type_sal = 0,
            ),
        output_variables = dict(
            allegement_fillon = 3233.51,
#            allegement_fillon_anticipe = {
#                "2011-01": 354.9,
#                "2011-02": 354.9,
#                "2011-03": 354.9,
#                "2011-04": 354.9,
#                "2011-05": 354.9,
#                "2011-06": 354.9,
#                "2011-07": 354.9,
#                "2011-08": 354.9,
#                "2011-09": 0,
#                "2011-10": 354.9,
#                "2011-11": 354.9,
#                "2011-12": 325.49,
#            }
            ),
        ),
#    cadre = dict(
#        input_variables = dict(
#            effectif_entreprise = 3000,
#            exposition_accident = 3,
#            localisation_entreprise = "75001",
#            ratio_alternants = .025,
#            salbrut = 6000,
#            taille_entreprise = 3,
#            type_sal = 1,
#            ),
#        output_variables = dict(
#            ),
#        )
)


def test_check():
    from openfisca_core import periods
    for employee_type,  test_parameters in test_case_by_employee_type.iteritems():
        period = "2011"
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
                    variable_message = "{} at {}".format(variable, period)
                    yield assert_variable, variable_message, employee_type, amount, output
            else:
                output = simulation.calculate(variable)
                variable_message = variable
                amount = amounts
                yield assert_variable, variable_message, employee_type, amount, output


def assert_variable(variable_message, employee_type, amount, output):
    print variable_message
    print output
    assert abs(output - amount) < .01, \
        "error for {} ({}) : should be {} instead of {} ".format(variable_message, employee_type, amount, output)


