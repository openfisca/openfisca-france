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

from openfisca_core import periods
from openfisca_france.tests.base import tax_benefit_system


test_case_by_employee_type = dict(
    someone = dict(
        period = "2014-11",
        input_variables = dict(
            assujettie_taxe_salaires = True,
            contrat_de_travail_duree = 1,  # CDD
            contrat_de_travail_arrivee = "2014-11-02",
            effectif_entreprise = 3000,
            # exposition_accident = 3,
            localisation_entreprise = "75014",
            prevoyance_obligatoire_cadre_taux = .0157,
            ratio_alternants = 0,
            redevable_taxe_apprentissage = 0,
            salbrut = {"2014-11": 4600},
            taux_accident_travail = .015,
            taux_versement_transport = .027,
            type_sal = 1,
            ),
        output_variables = dict(
            conge_individuel_formation_cdd = -46,
            contribution_solidarite_autonomie = -13.8,
            participation_effort_construction = -20.70,
            fnal_tranche_a = 0,
            fnal_tranche_a_plus_20 = -23,
            # fnal_tranche_b_plus_20 # Inclus dans fnal_tranche_a_plus_20
            formation_professionnelle = -73.6,
            versement_transport = -124.20,
            # cotisations_patronales_main_d_oeuvre = ,
            agff_tranche_a_employe = -24.20 - 14.18,
            agff_tranche_a_employeur = - 36.30 - 20.48,
            ags = -13.80,
            apec_employeur = - 1.09 - .57,
            cotisation_exceptionnelle_temporaire_employeur = -10.12,
            arrco_tranche_a_employeur = -138.53 - 199.75,
            # agirc_tranche_b_employeur = -199.75,  # Inclus dans arcco
            assedic_employeur = - 120.99 - 63.01,
            # assedic_tranche_a_employeur = -120.99  # Inclus dans assedic
            # assedic_tranche_b_employeur = -63.01  # Inclus dans assedic
            vieillesse_deplafonnee_employeur = -80.5,
            vieillesse_plafonnee_employeur = -255.59,

            # cotisations_patronales_contributives = ,

            accident_du_travail = -69,
            famille = -241.5,
            maladie_employeur = - 588.80,
#            cotisations_patronales = - 2836.38,  # montant juste TODO: A compléter avec presta manquantes
            taxe_salaires = - 197.52 - 27.07 - 315.27,
            prevoyance_obligatoire_cadre = -47.49,

            cotisation_exceptionnelle_temporaire_employe = -5.98,
            maladie_employe = - 34.5,
            # cotisations_salariales_non_contributives = ,

            apec_employe = -.73 - .38,
            arrco_tranche_a_employe = -92.25,
            agirc_tranche_b_employe = - 122.09,
            # assedic_tranche_a_employe = -72.59  # Inclus dans assedic
            # assedic_tranche_b_employe = 37.81,  # Inclus dans assedic
            assedic_employe = -72.59 - 37.81,

            vieillesse_deplafonnee_employe = -11.5,
            vieillesse_plafonnee_employe = -205.68,
            # cotisations_salariales_contributives = ,

            # cotisations_salariales = ,
            csgsald = -232.92,
            csgsali = -109.61,
            crdssal = -22.83,
            ),
        ),
    )


default_period = "2014"


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
    error_margin = .005
    assert abs(output - amount) < error_margin, \
        "error for {} ({}) : should be {} instead of {} ".format(variable_message, employee_type, amount, output)


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
