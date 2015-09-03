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

from openfisca_core import periods, reforms

from openfisca_france.tests.base import tax_benefit_system


test_case_by_employee_type = dict(
    annuel = dict(
        input_variables = dict(
            allegement_fillon_mode_recouvrement = 0,
            effectif_entreprise = 3000,
            code_postal_entreprise = "75001",
            salaire_de_base = {  # 9 smic horaire 2011
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
            type_sal = 0,
            ),
        output_variables = dict(
            allegement_fillon = {
                "2011": 3233.51,
                },
            ),
        ),
    circulaire_acoss_2011_regularisation_fin_de_periode = dict(
        input_variables = dict(
            allegement_fillon_mode_recouvrement = 1,
            effectif_entreprise = 3000,
            code_postal_entreprise = "75001",
            salaire_de_base = {  # 9 smic horaire 2011
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
            type_sal = 0,
            ),
        output_variables = dict(
            allegement_fillon = {
                "2011-01": 354.9,
                "2011-02": 354.9,
                "2011-03": 354.9,
                "2011-04": 354.9,
                "2011-05": 354.9,
                "2011-06": 354.9,
                "2011-07": 354.9,
                "2011-08": 354.9,
                "2011-09": 0,
                "2011-10": 354.9,
                "2011-11": 354.9,
                "2011-12": -315.49,  # employeur est redevable
                "2011": 3233.51,
                },
            ),
        ),
    circulaire_acoss_2011_progressif = dict(
        input_variables = dict(
            allegement_fillon_mode_recouvrement = 2,
            effectif_entreprise = 3000,
            code_postal_entreprise = "75001",
            salaire_de_base = {  # 9 smic horaire 2011
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
            type_sal = 0,
            ),
        output_variables = dict(
            allegement_fillon = {
                "2011-01": 354.9,
                "2011-02": 354.9,
                "2011-03": 354.9,
                "2011-04": 354.9,
                "2011-05": 354.9,
                "2011-06": 354.9,
                "2011-07": 354.9,
                "2011-08": 354.9,
                "2011-09": -78.58,
                "2011-10": 355.44,
                "2011-11": 354.39,
                "2011-12": -236.94,
                # "2011": 10 * 354.9 - 78.58 - 236.94,
                },
            ),
        ),
    salarie_2015_5000_euros = dict(
        input_variables = dict(
            allegement_fillon_mode_recouvrement = 2,
            effectif_entreprise = 1,
            code_postal_entreprise = "75001",
            contrat_de_travail_debut = "2015-01-01",
            salaire_de_base = {
                "2015-01": 5000,
                "2015-02": 5000,
                "2015-03": 5000,
                "2015-04": 5000,
                "2015-05": 5000,
                "2015-06": 5000,
                "2015-07": 5000,
                "2015-08": 5000,
                "2015-09": 5000,
                "2015-10": 5000,
                "2015-11": 5000,
                "2015-12": 5000,
                },
            type_sal = 0,
            ),
        output_variables = dict(
            allegement_fillon = {
                "2015-01": 0,
                "2015-02": 0,
                "2015-03": 0,
                "2015-04": 0,
                "2015-05": 0,
                "2015-06": 0,
                "2015-07": 0,
                "2015-08": 0,
                "2015-09": 0,
                "2015-10": 0,
                "2015-11": 0,
                "2015-12": 0,
                },
            ),
        ),
    )


def test_check():
    for employee_type, test_parameters in test_case_by_employee_type.iteritems():
        Reform = reforms.make_reform(
            key = u'smic_h_b_9_euros',
            name = u"Réforme pour simulation ACOSS SMIC horaire brut fixe à 9 euros",
            reference = tax_benefit_system,
            )
        reform = Reform()
        reform.modify_legislation_json(modifier_function = modify_legislation_json)

        simulation_period = 2011
        parent1 = dict(
            birth = datetime.date(periods.period(simulation_period).start.year - 40, 1, 1),
            )
        parent1.update(test_parameters['input_variables'])

        simulation = reform.new_scenario().init_single_entity(
            period = simulation_period,
            parent1 = parent1,
            ).new_simulation(debug = True)

        for variable, amounts in test_parameters['output_variables'].iteritems():
            if isinstance(amounts, dict):
                for period_str, amount in sorted(amounts.iteritems()):
                    output = simulation.calculate_add_divide(variable, period = periods.period(period_str))
                    variable_message = "{} at {}".format(variable, period_str)
                    yield assert_variable, variable_message, employee_type, amount, output
            else:
                output = simulation.calculate(variable)
                variable_message = variable
                amount = amounts
                yield assert_variable, variable_message, employee_type, amount, output


def assert_variable(variable_message, employee_type, amount, output):
    # TODO Use assert_near.
    assert abs(output - amount) < 0.01, \
        "error for {} ({}) : should be {} instead of {} ".format(variable_message, employee_type, amount, output)


def modify_legislation_json(reference_legislation_json_copy):
    # FIXME update_legislation is deprecated.
    reform_legislation_json = reforms.update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ('children', 'cotsoc', 'children', 'gen', 'children', 'smic_h_b', 'values'),
        period = periods.period("year", "2011"),
        value = 9,
        )
    return reform_legislation_json
