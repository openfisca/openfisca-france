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


def test_1():
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = "2013-01-01",
        parent1 = dict(
            effectif_entreprise = 3000,
            exposition_accident = 3,
            localisation_entreprise = "75001",
            part_d_alternants = .025,
            salbrut = 3000,
            taille_entreprise = 3,
            type_sal = 0,
            ),
        menage = dict(
            zone_apl = 1,
            ),
        ).new_simulation(debug = True)
    simulation.calculate("allegement_fillon")
    simulation.calculate("maladie_employeur")


non_cadre = dict(
    input_variables = dict(
        effectif_entreprise = 3000,
        exposition_accident = 3,
        localisation_entreprise = "75001",
        part_d_alternants = .025,
        salbrut = 3000,
        taille_entreprise = 3,
        type_sal = 0,
        ),
    output_variables = dict(
        # patronales main d'oeuvre
        contribution_developpement_apprentissage = -5.4,
        contribution_supplementaire_apprentissage = -3,
        taxe_apprentissage = -15,
        contribution_solidarite_autonomie = -9,
        participation_effort_construction = -13.5,
        fnal_tranche_a = -3,
        fnal_tranche_a_plus_20 = -12,
        formation_professionnelle = -48,
        versement_transport = -52.5,
        cotisations_patronales_main_d_oeuvre = -158.4 - 3,
        # -(206.4 -48) formation professionnelle conmptée deux fois
        # - 3 contribution_supplementaire_apprentissage
        cotisations_patronales_main_d_oeuvre_old = -206.4,
        # patronales non contributives
        accident_du_travail = -300,
        famille = -162,
        maladie_employeur = -384,
        cotisations_patronales_non_contributives = -846,
        cotisations_patronales_non_contributives_old = -846,

        # patronales contributives
        agff_tranche_a_employeur = -36,
        ags = -9,
        arrco_tranche_a_employeur = -135,
        assedic_employeur = -120,
        vieillesse_deplafonnee_employeur = -48,
        vieillesse_plafonnee_employeur = -249,
        cotisations_patronales_contributives = -597,
        cotisations_patronales_contributives_old = -597,
        cotisations_patronales = - 158.4 - 3 - 597 - 846,

        agff_tranche_a_employe = -24,
        arrco_tranche_a_employe = -90,
        assedic_employe = -72,
        maladie_employe = -22.5,
        vieillesse_deplafonnee_employe = -3,
        vieillesse_plafonnee_employe = -199.5,
        cotisations_salariales_contributives = -388.5,
        cotisations_salariales_contributives_old = -388.5,
        cotisations_salariales_non_contributives = -22.5,
        cotisations_salariales_non_contributives_old = -22.5,
        cotisations_salariales = -388.5 - 22.5,
        csgsald = -150.32,
        csgsali = -70.74,
        crdssal = -14.74,
        ),
    )

cadre = dict(
    input_variables = dict(
        effectif_entreprise = 3000,
        exposition_accident = 3,
        localisation_entreprise = "75001",
        part_d_alternants = .025,
        salbrut = 6000,
        taille_entreprise = 3,
        type_sal = 1,
        ),
    output_variables = dict(

        contribution_developpement_apprentissage = -10.80,
        taxe_apprentissage = -30,
        contribution_solidarite_autonomie = -18,
        contribution_supplementaire_apprentissage = -6,
        participation_effort_construction = -27,
        fnal_tranche_a = -3.03,
        fnal_tranche_a_plus_20 = -12.12 - 14.85,
        # fnal_tranche_b_plus_20 = -14.85, # Inclus dans fnal_tranche_a_plus_20
        formation_professionnelle = -96,
        versement_transport = -105,
        cotisations_patronales_main_d_oeuvre = - (412.8 - 96) - 6,
        # -(421.8 - 96) formation professionnelle conmptée deux fois
        # - 6 contribution_supplementaire_apprentissage
        cotisations_patronales_main_d_oeuvre_old = -412.8,

        # agff_tranche_a_employe = -24.25,   # TODO: pas de tranche B dans le simulateur IPP
        agff_tranche_a_employeur = -74.96,
        ags = -18,
        apec_employeur = - 2.16,
        cotisation_exceptionnelle_temporaire_employeur = -13.20,
        arrco_tranche_a_employeur = -136.39 - 374.09,
        # agirc_tranche_b_employeur = -374.09,  # Inclus dans arcco
        assedic_employeur = - 121.24 - 118.76,
        # assedic_tranche_a_employeur = -11.24  # Inclus dans assedic
        # assedic_tranche_b_employeur = -118,76  # Inclus dans assedic
        vieillesse_deplafonnee_employeur = -96,
        vieillesse_plafonnee_employeur = -251.57,

        cotisations_patronales_contributives = -1206.4,
        cotisations_patronales_contributives_old = -1206.4,

        accident_du_travail = -600,
        famille = -324,
        maladie_employeur = -768,
        cotisations_patronales_non_contributives = - 1692,
        cotisations_patronales_non_contributives_old = - 1692,
        cotisations_patronales = - 1692 - 1206.4 - (412.8 - 96) - 6,
        maladie_employe = - 45,
        cotisations_salariales_non_contributives = -45,
        cotisations_salariales_non_contributives_old = -45,

        apec_employe = -1.44,
        arrco_tranche_a_employe = -90.93,
        agirc_tranche_b_employe = -228.61,
        # assedic_tranche_a_employe = -72.74  # Inclus dans assedic
        # assedic_tranche_b_employe = -71,26,  # Inclus dans assedic
        assedic_employe = -72.74 - 71.26,
        vieillesse_deplafonnee_employe = -6,
        vieillesse_plafonnee_employe = -201.56,
        cotisations_salariales_contributives = -731.31,
        cotisations_salariales_contributives_old = -731.31,

        cotisations_salariales = -731.31 - 45,
        cotisations_salariales_old = -731.31 - 45,
        csgsald = -300.65,
        csgsali = -141.48,
        crdssal = -29.48,
        ),
    )


test_parameters_list = [non_cadre, cadre]


def test_check():
    from openfisca_core import periods
    for test_parameters in test_parameters_list:
        period = "2012-01"
        parent1 = dict(
            birth = datetime.date(periods.period(period).start.year - 40, 1, 1),
            )
        parent1.update(test_parameters['input_variables'])

        employee_type = 'non cadre' if parent1['type_sal'] == 0 else 'cadre'
        simulation = tax_benefit_system.new_scenario().init_single_entity(
            period = period,
            parent1 = parent1,
            ).new_simulation(debug = True)

        for variable, monthly_amount in test_parameters['output_variables'].iteritems():
            output = simulation.calculate(variable)
#            print variable
#            print output
            yield assert_variable, variable, employee_type, monthly_amount, output


def assert_variable(variable, employee_type, monthly_amount, output):
    assert abs(output - monthly_amount) < .01, \
        "error for {} ({}) : should be {} instead of {} ".format(variable, employee_type, monthly_amount, output)


def test_decomposition():
    from openfisca_core.decompositions import calculate, get_decomposition_json
    import json
    import os
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = "2013-01-01",
        parent1 = dict(
            effectif_entreprise = 3000,
            exposition_accident = 3,
            localisation_entreprise = "75001",
            part_d_alternants = .025,
            salbrut = 3000,
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
    print unicode(
        json.dumps(response, encoding = 'utf-8', ensure_ascii = False, indent = 2)
        )


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_decomposition()
