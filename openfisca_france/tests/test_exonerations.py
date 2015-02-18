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


test_case_by_employee_type = dict(
    exoneration_cotisations_patronales_zfu = dict(
        input_variables = dict(
            contrat_de_travail_arrivee = "2011-01-01",
            effectif_entreprise = {
                "2014:15": 20 * 15,
                },
            salaire_de_base = {  # 9 smic horaire 2011
                "2014": 35 * 52 * 9.53,
                "2015": 35 * 52 * 9.61,
                "2016": 35 * 52 * 9.61,
                },
            zone_franche_urbaine = {
                "2014:15": True,
                },
            type_sal = 0,
            ),
        output_variables = dict(
            exoneration_cotisations_patronales_zfu = {
                "2014": 35 * 52 * 9.53 * .301,
                "2014-01": 35 * 52 * 9.53 * .301 / 12,
#                "2015": 35 * 52 * 9.61 * .281 * 8 / 12,
                "2015-01": 35 * 52 * 9.61 * .3015 * .6 / 12,
                "2015-09": 35 * 52 * 9.61 * .3015 * .6 / 12,
                "2016": 35 * 52 * 9.61 * .3015 * .4,
                }
            ),
        ),
    exonearation_cotisations_patronales_zrr_smic = dict(
        input_variables = dict(
            contrat_de_travail_arrivee = "2010-05-01",
            effectif_entreprise = 20,
            salaire_de_base = {  # 9 smic horaire 2011
                "2014": 35 * 52 * 9.53,
                "2015": 35 * 52 * 9.61,
                },
            zone_revitalisation_rurale = {
                "2014:5": True,
                },
            type_sal = 0,
            ),
        output_variables = dict(
            exoneration_cotisations_patronales_zrr= {
                "2014": 35 * 52 * 9.53 * .281,
                "2014-01": 35 * 52 * 9.53 * .281 / 12,
#                "2015": 35 * 52 * 9.61 * .281 * 8 / 12,
                "2015-01": 35 * 52 * 9.61 * .281 / 12,
                "2015-09": 0,
                "2016": 0}
            ),
        ),
    exonearation_cotisations_patronales_zrr_1p4_smic = dict(
        input_variables = dict(
            contrat_de_travail_arrivee = "2010-05-01",
            effectif_entreprise = 20,
            salaire_de_base = {  # 9 smic horaire 2011
                "2014": 35 * 52 * 9.53 * 1.4,
                "2015": 35 * 52 * 9.61 * 1.4,
                },
            zone_revitalisation_rurale = {
                "2014:5": True,
                },
            type_sal = 0,
            ),
        output_variables = dict(
            exoneration_cotisations_patronales_zrr = {
                "2014": 35 * 52 * 9.53 * 1.4 * .281,
                "2014-01": 35 * 52 * 9.53 * 1.4 * .281 / 12,
#                "2015": 35 * 52 * 9.61 * 1.4 * .281 * 8 / 12,
                "2015-01": 35 * 52 * 9.61 * 1.4 * .281 / 12,
                "2015-09": 0,
                "2016": 0,
                }
            ),
        ),
    exonearation_cotisations_patronales_zrr_2p5_smic = dict(
        input_variables = dict(
            contrat_de_travail_arrivee = "2010-05-01",
            effectif_entreprise = 20,
            salaire_de_base = {  # 9 smic horaire 2011
                "2014": 35 * 52 * 9.53 * 2.5,
                "2015": 35 * 52 * 9.61 * 2.5,
                },
            zone_revitalisation_rurale = {
                "2014:5": True,
                },
            type_sal = 0,
            ),
        output_variables = dict(
            exoneration_cotisations_patronales_zrr= {
                "2014": 35 * 52 * 9.53 * 2.5 * 0,
                "2014-01": 35 * 52 * 9.53 * 2.5 * 0 / 12,
#                "2015": 35 * 52 * 9.61 * 2.5 * .281 * 8 / 12,
                "2015-01": 35 * 52 * 9.61 * 1.4 * 0 / 12,
                "2015-09": 0,
                "2016": 0}
            ),
        ),
    creation_zrr = dict(
        input_variables = dict(
            contrat_de_travail_arrivee = "2014-03-10",
            effectif_entreprise = 20,
            entreprise_benefice = {
                "2014:10": 1 * 10,
                },
            salaire_de_base = {  # 9 smic horaire 2011
                "2014": 35 * 52 * 9.53,
                "2015": 35 * 52 * 9.64,
                },
            zone_revitalisation_rurale = {
                "2014:10": True,
                },
            type_sal = 0,
            ),
        output_variables = dict(
            exoneration_is_creation_zrr = {
                "2014": 1,
                "2015": 1,
                "2016": 1,
                "2017": 1,
                "2018": 1,
                "2019": .75,
                "2020": .50,
                "2021": .25,
                }
            ),
        ),
    )


def test_check():
    for employee_type, test_parameters in test_case_by_employee_type.iteritems():

        simulation_period = 2011
        parent1 = dict(
            birth = datetime.date(periods.period(simulation_period).start.year - 40, 1, 1),
            )
        parent1.update(test_parameters['input_variables'])
        simulation = tax_benefit_system.new_scenario().init_single_entity(
            period = simulation_period,
            parent1 = parent1,
            ).new_simulation(debug = True)

        for variable, amounts in test_parameters['output_variables'].iteritems():
            if isinstance(amounts, dict):
                for period_str, amount in sorted(amounts.iteritems()):
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
