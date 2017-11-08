# -*- coding: utf-8 -*-

from __future__ import division


import datetime

from openfisca_core import periods
from openfisca_core.reforms import Reform, update_legislation

from cache import tax_benefit_system


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_json = update_legislation(
        legislation_json = reference_legislation_json_copy,
        path = ['children', 'cotsoc', 'children', 'gen', 'children', 'smic_h_b', 'values'],
        period = periods.period(2013),
        value = 9,
        )
    return reform_legislation_json


test_case_by_employee_type = dict(
    annuel = dict(
        input_variables = dict(
            allegement_fillon_mode_recouvrement = 0,
            effectif_entreprise = 3000,
            code_postal_entreprise = "75001",
            salaire_de_base = {  # 9 smic horaire 2013
                "2013-01": 35 * 52 / 12 * 9,
                "2013-02": 35 * 52 / 12 * 9,
                "2013-03": 35 * 52 / 12 * 9,
                "2013-04": 35 * 52 / 12 * 9,
                "2013-05": 35 * 52 / 12 * 9,
                "2013-06": 35 * 52 / 12 * 9,
                "2013-07": 35 * 52 / 12 * 9,
                "2013-08": 35 * 52 / 12 * 9,
                "2013-09": 35 * 52 / 12 * 9 + 1000,
                "2013-10": 35 * 52 / 12 * 9,
                "2013-11": 35 * 52 / 12 * 9,
                "2013-12": 35 * 52 / 12 * 9 * 2,
                },
            categorie_salarie = 0,
            ),
        output_variables = dict(
            allegement_fillon = {
                "2013": 3233.51,
                },
            ),
        ),
    circulaire_acoss_2013_regularisation_fin_de_periode = dict(
        input_variables = dict(
            allegement_fillon_mode_recouvrement = 1,
            effectif_entreprise = 3000,
            code_postal_entreprise = "75001",
            salaire_de_base = {  # 9 smic horaire 2013
                "2013-01": 35 * 52 / 12 * 9,
                "2013-02": 35 * 52 / 12 * 9,
                "2013-03": 35 * 52 / 12 * 9,
                "2013-04": 35 * 52 / 12 * 9,
                "2013-05": 35 * 52 / 12 * 9,
                "2013-06": 35 * 52 / 12 * 9,
                "2013-07": 35 * 52 / 12 * 9,
                "2013-08": 35 * 52 / 12 * 9,
                "2013-09": 35 * 52 / 12 * 9 + 1000,
                "2013-10": 35 * 52 / 12 * 9,
                "2013-11": 35 * 52 / 12 * 9,
                "2013-12": 35 * 52 / 12 * 9 * 2,
                },
            categorie_salarie = 0,
            ),
        output_variables = dict(
            allegement_fillon = {
                "2013-01": 354.9,
                "2013-02": 354.9,
                "2013-03": 354.9,
                "2013-04": 354.9,
                "2013-05": 354.9,
                "2013-06": 354.9,
                "2013-07": 354.9,
                "2013-08": 354.9,
                "2013-09": 0,
                "2013-10": 354.9,
                "2013-11": 354.9,
                "2013-12": -315.49,  # employeur est redevable
                "2013": 3233.51,
                },
            ),
        ),
    circulaire_acoss_2013_progressif = dict(
        input_variables = dict(
            allegement_fillon_mode_recouvrement = 2,
            effectif_entreprise = 3000,
            code_postal_entreprise = "75001",
            salaire_de_base = {  # 9 smic horaire 2013
                "2013-01": 35 * 52 / 12 * 9,
                "2013-02": 35 * 52 / 12 * 9,
                "2013-03": 35 * 52 / 12 * 9,
                "2013-04": 35 * 52 / 12 * 9,
                "2013-05": 35 * 52 / 12 * 9,
                "2013-06": 35 * 52 / 12 * 9,
                "2013-07": 35 * 52 / 12 * 9,
                "2013-08": 35 * 52 / 12 * 9,
                "2013-09": 35 * 52 / 12 * 9 + 1000,
                "2013-10": 35 * 52 / 12 * 9,
                "2013-11": 35 * 52 / 12 * 9,
                "2013-12": 35 * 52 / 12 * 9 * 2,
                },
            categorie_salarie = 0,
            ),
        output_variables = dict(
            allegement_fillon = {
                "2013-01": 354.9,
                "2013-02": 354.9,
                "2013-03": 354.9,
                "2013-04": 354.9,
                "2013-05": 354.9,
                "2013-06": 354.9,
                "2013-07": 354.9,
                "2013-08": 354.9,
                "2013-09": -78.58,
                "2013-10": 355.44,
                "2013-11": 354.39,
                "2013-12": -236.94,
                # "2013": 10 * 354.9 - 78.58 - 236.94,
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
            categorie_salarie = 0,
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


class smic_h_b_9_euros(Reform):
    name = u"Réforme pour simulation ACOSS SMIC horaire brut fixe à 9 euros"

    def apply(self):
        self.modify_legislation_json(modifier_function = modify_legislation_json)


def test_check():
    reform = smic_h_b_9_euros(tax_benefit_system)

    for employee_type, test_parameters in test_case_by_employee_type.iteritems():
        simulation_period = 2013
        parent1 = dict(
            date_naissance = datetime.date(periods.period(simulation_period).start.year - 40, 1, 1),
            )
        parent1.update(test_parameters['input_variables'])

        simulation = reform.new_scenario().init_single_entity(
            period = simulation_period,
            parent1 = parent1,
            ).new_simulation()

        for variable, amounts in test_parameters['output_variables'].iteritems():
            if isinstance(amounts, dict):
                for period_str, amount in sorted(amounts.iteritems()):
                    output = simulation.calculate_add(variable, period = periods.period(period_str))
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

