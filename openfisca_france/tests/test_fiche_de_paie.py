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

from .base import tax_benefit_system


def test_1():
#    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = "2013-01-01",
        parent1 = dict(
            exposition_accident = 3,
            localisation_entreprise = "75001",
            salbrut = 3000,
            taille_entreprise = 3,
            type_sal = 0,
            ),
        menage = dict(
            zone_apl = 1,
            ),
        ).new_simulation(debug = True)
    print simulation.calculate("maladie_employe")


non_cadre = dict(
    input_variables = dict(
        exposition_accident = 3,
        localisation_entreprise = "75001",
        salbrut = 3000,
        taille_entreprise = 3,
        type_sal = 0,
        ),
    output_variables = dict(
        accident_du_travail = -300,
        agff_tranche_a_employeur = -36,
        agff_tranche_a_employe = -24,
        ags = -9,
        arrco_tranche_a_employe = -90,
        arrco_tranche_a_employeur = -135,
        assedic_employe = -72,
        assedic_employeur = -120,
        contribution_solidarite_autonomie = -9,
        csgsald = -150.32,
        csgsali = -70.74,
        crdssal = -14.74,
        famille = -162,
        fnal_tranche_a = -3,
        fnal_tranche_a_plus_20 = -12,
        formation_professionnelle = -48,
        maladie_employe = -22.5,
        maladie_employeur = -384,
        versement_transport = -52.5,
        vieillesse_deplafonnee_employeur = -48,
        vieillesse_plafonnee_employeur = -249,
        vieillesse_deplafonnee_employe = -3,
        vieillesse_plafonnee_employe = -199.5,
        cotisations_patronales_contributives = -597,
        cotisations_patronales_contributives2 = -597,
        ),
    )

cadre = dict(
    input_variables = dict(
        exposition_accident = 3,
        localisation_entreprise = "75001",
        salbrut = 6000,
        taille_entreprise = 3,
        type_sal = 1,
        ),
    output_variables = dict(
        accident_du_travail = -600,
#        agff_tranche_a_employe = -24.25,   # TODO: pas de tranche B dans le simulateur IPP
#        agff_tranche_a_employeur = -36.37,
        ags = -18,
        apec_employe = -1.44,
        apec_employeur	= -2.16,
        arrco_tranche_a_employe = -90.93,
        arrco_tranche_a_employeur = -136.39 - 374.09,
        agirc_tranche_b_employe = -228.61,
#        agirc_tranche_b_employeur = -374.09,  # Inclus dans arcco
        assedic_employe = -72.74 - 71.26,
#        assedic_tranche_a_employe = -72.74  # Inclus dans assedic
#        assedic_tranche_b_employe = -71,26,  # Inclus dans assedic
        assedic_employeur = -121.24 - 118.76 ,
#        assedic_tranche_a_employeur = -11.24  # Inclus dans assedic
#        assedic_tranche_b_employeur = -118,76,  # Inclus dans assedic
        cotisation_exceptionnelle_temporaire_employe = -7.80,
        cotisation_exceptionnelle_temporaire_employeur = -13.20,
        contribution_solidarite_autonomie = -18,
        csgsald = -300.65,
        csgsali = -141.48,
        crdssal = -29.48,
        famille = -324,
        fnal_tranche_a = -3.03,
        fnal_tranche_a_plus_20 = -12.12 - 14.85,
#        fnal_tranche_b_plus_20 = -14.85, # Inclus dans fnal_tranche_a_plus_20
        formation_professionnelle = -96,
        maladie_employe = -45,
        maladie_employeur = -768,
        taxe_apprentissage = -30,
        contribution_developpement_apprentissage = -10.80,
#       contribution_supplementaire_apprentissage
        versement_transport = -105,
        vieillesse_deplafonnee_employe = -6,
        vieillesse_deplafonnee_employeur = -96,
        vieillesse_plafonnee_employe = -201.56,
        vieillesse_plafonnee_employeur = -251.57,
        ),
    )


test_parameters_list = [non_cadre, cadre]


def test_check():
    for test_parameters in test_parameters_list:
        year = 2012
        period = "2012-01"
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            )
        parent1.update(test_parameters['input_variables'])

        employee_type = 'non cadre' if parent1['type_sal'] == 0 else 'cadre'
        simulation = tax_benefit_system.new_scenario().init_single_entity(
            period = "2012-01", #periods.period('year', year),
            parent1 = parent1,
            ).new_simulation(debug = True)

        for variable, monthly_amount in test_parameters['output_variables'].iteritems():
            output = simulation.calculate(variable)
            print variable
            print output
            yield assert_variable, variable, employee_type, monthly_amount, output


def assert_variable(variable, employee_type, monthly_amount, output):
    assert abs(output - monthly_amount) < .01, \
        "error for {} ({}) : should be {} instead of {} ".format(variable, employee_type, monthly_amount, output)


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_check()
