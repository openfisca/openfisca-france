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

from ..model.base import CAT
from . import base


def check_simulation_monthly_variable(description, simulation, variable, expected_value, error_margin):
    calculated_value = (simulation.calculate(variable)).sum()  # monthly values
    assert abs(calculated_value - expected_value) < error_margin, u'Variable "{} = {}. Expected: {}'.format(
        variable, calculated_value, expected_value)


def test():
    # Comparaison avec la fiche de paie IPP calculée avec une cotisation transport correspondant à Paris ((.026)
    # alors qu'Openfisca la caclule pour Lyon (.0175)
    tests_infos = [
        dict(
            period = "2012-01",
            description = u"Célibataire public_titulaire_etat",
            parent1 = dict(
                birth = datetime.date(1972, 1, 1),
                depcom_entreprise = "69381",
                primes_fonction_publique = 500,
                traitement_indiciaire_brut = 2000,
                taille_entreprise = 3,  # TODO fix this
                type_sal = CAT['public_titulaire_etat'],
                ),
            menage = dict(
                zone_apl = 1,
                ),

            error_margin = 1,
            expected_values = dict(

                fnal = -8 - 2,
                versement_transport = -2000 * 0.0175,  # = 35
                cotisations_employeur_main_d_oeuvre = -45,

                allocations_temporaires_invalidite = -6.6,
                mmid_employeur = -194,
                famille = -108,
                contribution_solidarite_autonomie = - 6,
                cotisations_employeur_non_contributives = -314.6,
                # mmid_employeur, famille, fnal, versement_transport,
                # allocations_temporaires_invalidite contribution_solidarite_autonomie

                rafp_employeur = -20,
                pension_civile_employeur = -1371.80,
                cotisations_employeur_contributives = - 1371.80 - 20,
                # pension_civile_employeur, rafp_employeur

                cotisations_employeur = -(1371.80 + 6.6 + 20 + 194 + 108 + 2 + 8 + 2000 * 0.0175 + 6),
                # pension, ati, rafp, maladie, famille, fnal1, fnal2, transport csa,

                pension_civile_salarie = -167.80,
                rafp_salarie = -20,
                cotisations_salariales_contributives = - (167.80 + 20),
                # pension rafp

                contribution_exceptionnelle_solidarite = - 23.72,
                cotisations_salariales_non_contributives = - 23.72,

                cotisations_salariales = -(167.80 + 20 + 23.72),
                # pension, rafp, cotisation exceptionnelle de solidarité

                csg_deductible_salaire = -128.28,
                csg_imposable_salaire = -60.36,
                crds_salaire = -12.58,
                indemnite_residence = 60,
                salaire_net = 2147.26,
                salsuperbrut = 4328.40 + 2000 * (0.0175 - 0.026),  # Correction transport
                ),
            ),
        dict(
            period = "2012-01",
            description = u"Célibataire public_titulaire_territoriale",
            parent1 = dict(
                birth = datetime.date(1972, 1, 1),
                depcom_entreprise = "69381",
                primes_fonction_publique = 500,
                traitement_indiciaire_brut = 2000,
                taille_entreprise = 3,  # TODO fix this
                type_sal = CAT['public_titulaire_territoriale'],
                ),
            menage = dict(
                zone_apl = 1,
                ),

            error_margin = 1,
            expected_values = dict(
                fnal = -8 -2 ,
                versement_transport = -2000 * 0.0175,
                cotisations_employeur_main_d_oeuvre = -45,

                allocations_temporaires_invalidite = -10,
                mmid_employeur = -230,
                famille = -108,
                contribution_solidarite_autonomie = - 6,
                cotisations_employeur_non_contributives  = -( 230 + 108 + 10 + 6),

                pension_civile_employeur = -546,
                rafp_employeur = -20,
                cotisations_employeur_contributives = -(546 + 20),

                cotisations_employeur = -(546 + 10 + 20 + 230 + 108 + 2 + 8 + 2000 * 0.0175 + 6),
                # pension, ati, rafp, maladie, famille, fnal1, fnal2, csa,

                pension_civile_salarie = -167.80,
                rafp_salarie = -20,
                cotisations_salariales_contributives = - (167.80 + 20),

                # pension rafp

                contribution_exceptionnelle_solidarite = -23.72,
                cotisations_salariales_non_contributives = - 23.72,

                cotisations_salariales = -(167.80 + 20 + 23.72),
                csg_deductible_salaire = -128.28,
                csg_imposable_salaire = -60.36,
                crds_salaire = -12.58,
                indemnite_residence = 60,
                salaire_net = 2147.26,
                salsuperbrut = 3542 + 2000 * (0.0175 - 0.026),
                ),
            ),
        dict(
            period = "2012-01",
            description = u"Célibataire public_titulaire_hospitaliere",
            parent1 = dict(
                birth = datetime.date(1972, 1, 1),
                depcom_entreprise = "69381",
                primes_fonction_publique = 500,
                traitement_indiciaire_brut = 2000,
                taille_entreprise = 3,  # TODO fix this
                type_sal = CAT['public_titulaire_hospitaliere'],
                ),
            menage = dict(
                zone_apl = 1,
                ),

            error_margin = 1,
            expected_values = dict(

                fnal = -8 - 2,
                versement_transport = -2000 * 0.0175,
                cotisations_employeur_main_d_oeuvre = -45,

                allocations_temporaires_invalidite = -10,
                mmid_employeur = -230,
                famille = -108,
                contribution_solidarite_autonomie = - 6,
                cotisations_employeur_non_contributives = -354,
                # cotisations_employeur_non_contributives = -(10 + 230 + 108 + 2 + 8 + 2000 * 0.0175 + 6),
                # pension,  ati, rafp, maladie, famille, feh, fnal1, fnal2, transport, csa

                pension_civile_employeur = -546,
                fonds_emploi_hospitalier = -20,
                rafp_employeur = -20,
                cotisations_employeur_contributives = -(546 + 20 + 20),
                # pension,  rafp, feh
                cotisations_employeur = -(546 + 10 + 20 + 230 + 108 + 20 + 2 + 8 + 2000 * 0.0175 + 6),

                pension_civile_salarie = -167.80,
                rafp_salarie = -20,

                cotisations_salariales_contributives = - (167.80 + 20),

                contribution_exceptionnelle_solidarite = - 23.72,
                cotisations_salariales_non_contributives = - 23.72,

                cotisations_salariales = -(167.80 + 20 + 23.72),

                csg_deductible_salaire = -128.28,
                csg_imposable_salaire = -60.36,
                crds_salaire = -12.58,
                indemnite_residence = 60,
                salaire_net = 2147.26,
                salsuperbrut = 3562 + 2000 * (0.0175 - 0.026),
                ),
            ),
        dict(
            period = "2012-01",
            description = u"Célibataire public_non_titulaire",
            parent1 = dict(
                birth = datetime.date(1972, 1, 1),
                depcom_entreprise = "69381",
                primes_fonction_publique = 500,
                salaire_de_base = 2000,
                taille_entreprise = 3,  # TODO fix this
                type_sal = CAT['public_non_titulaire'],
                ),
            menage = dict(
                zone_apl = 1,
                ),

            error_margin = 1,
            expected_values = dict(

                fnal = - 10.24 - 2.56,
                versement_transport = -2560 * 0.0175,
                cotisations_employeur_main_d_oeuvre =  - 10.24 - 2.56 - 2560 * 0.0175,

                vieillesse_deplafonnee_employeur = -40.96,
                vieillesse_plafonnee_employeur = -212.48,
                pension_civile_employeur = 0,
                rafp_employeur = 0,
                ircantec_employeur = -90.24,  # TODO: Trouver source extérieur site IPP buggé
                contribution_solidarite_autonomie = - 7.68,
                cotisations_employeur_contributives = -343.68,  # -40.96 -212.48 -90.24 - 7.68

                cotisations_employeur_non_contributives = -465.92 - 7.68,

                cotisations_employeur = -(
                    212.48 + 40.96 + 90.24 + 327.68 + 138.24 + 2.56 + 10.24 + 2560 * 0.0175 + 7.68
                    ),

                pension_civile_salarie = 0,
                rafp_salarie = 0,
                ircantec_salarie = - 60.16,  # TODO: Trouver source extérieur site IPP buggé
                vieillesse_deplafonnee_salarie = -2.56,
                vieillesse_plafonnee_salarie = -170.24,
                cotisations_salariales_contributives = -232.96,

                contribution_exceptionnelle_solidarite = -23.16,
                mmid_salarie = -19.20,

                cotisations_salariales_non_contributives = - 23.16 - 19.20,

                cotisations_salariales = -(170.24 + 2.56 + 60.16 + 19.20 + 23.16),
                # viel_plaf viel_deplaf ircantecA maladie, cot excep de solidarite
                # cotisations_salariales_contributives = -(170.24 + 2.56 + 58.24),
                # viel_plaf viel_deplaf ircantecA

                csg_deductible_salaire = -128.28,
                csg_imposable_salaire = -60.36,
                crds_salaire = -12.58,
                indemnite_residence = 60,
                # salaire_net = 2091.20, # TODO: Trouver source extérieur site IPP buggé
                # salsuperbrut = 3367.36 + 2560 * (0.0175 - 0.026),
                ),
            ),
        dict(
            period = "2012-01",
            description = u"Couple 1 fonctionnaire public_titulaire_etat 2 enfants",
            parent1 = dict(
                birth = datetime.date(1972, 1, 1),
                depcom_entreprise = "69381",
                primes_fonction_publique = 500,
                traitement_indiciaire_brut = 2000,
                taille_entreprise = 3,  # TODO fix this
                type_sal = CAT['public_titulaire_etat'],
                ),
            parent2 = dict(
                birth = datetime.date(1972, 1, 1),
                ),
            enfants = [
                dict(birth = datetime.date(2000, 1, 1)),
                dict(birth = datetime.date(2009, 1, 1)),
                ],
            menage = dict(
                zone_apl = 1,
                ),

            error_margin = 2,
            expected_values = dict(
                fnal = -8 - 2,
                versement_transport = -2000 * 0.0175,  # = 35
                cotisations_employeur_main_d_oeuvre = -45,

                allocations_temporaires_invalidite = -6.6,
                mmid_employeur = -194,
                famille = -108,
                contribution_solidarite_autonomie = - 6,
                cotisations_employeur_non_contributives = -314.6,

                pension_civile_employeur = -1371.80,
                rafp_employeur = -20,
                cotisations_employeur_contributives = - 1371.80 - 20,

                cotisations_employeur = -(1371.80 + 6.6 + 20 + 194 + 108 + 2 + 8 + 2000 * 0.0175 + 6),
                # pension, ati, rafp, maladie, famille, fnal1, fnal2, csa,

                pension_civile_salarie = -167.80,
                rafp_salarie = -20,
                cotisations_salariales_contributives = -187.8,

                contribution_exceptionnelle_solidarite = - 23.72,
                cotisations_salariales_non_contributives = -23.72,
                cotisations_salariales = -(167.80 + 20 + 23.72),

                crds_salaire = -12.93,
                csg_deductible_salaire = -131.94,
                csg_imposable_salaire = -62.09,
                indemnite_residence = 60,
                # salaire_net = 2213.83,
                salsuperbrut = 4401.44 + 2000 * (.0175 - .026),
                supp_familial_traitement = 73.04,
                ),
            ),
        dict(
            period = "2012-01",
            description = u"Couple 2 fonctionnaires public_titulaire_etat 2 enfants",
            parent1 = dict(
                birth = datetime.date(1972, 1, 1),
                depcom_entreprise = "69381",
                primes_fonction_publique = 500,
                traitement_indiciaire_brut = 2000,
                taille_entreprise = 3,  # TODO fix this
                type_sal = CAT['public_titulaire_etat'],
                ),
            parent2 = dict(
                birth = datetime.date(1972, 1, 1),
                depcom_entreprise = "69381",
                primes_fonction_publique = 500,
                traitement_indiciaire_brut = 2000,
                taille_entreprise = 3,  # TODO fix this
                type_sal = CAT['public_titulaire_etat'],
                ),
            enfants = [
                dict(birth = datetime.date(2000, 1, 1)),
                dict(birth = datetime.date(2009, 1, 1)),
                ],
            menage = dict(
                zone_apl = 2,
                ),

            error_margin = 2,
            expected_values = dict(
                # pension,  ati, rafp, maladie, famille, fnal1, fnal2, csa,

                fnal = - 8 * 2 - 2 * 2,
                versement_transport = -2000 * 0.0175 * 2,  # = 35
                cotisations_employeur_main_d_oeuvre = -45 * 2,


                pension_civile_employeur = -1371.80 * 2,
                rafp_employeur = -20 * 2,
                cotisations_employeur_contributives = -2783.6,

                allocations_temporaires_invalidite = -6.6 * 2,
                mmid_employeur = -194 * 2,
                famille = -108 * 2,
                contribution_solidarite_autonomie = - 6 * 2,
                cotisations_employeur_non_contributives = -617.2 - 6 * 2,

                cotisations_employeur = -(1371.80 + 6.6 + 20 + 194 + 108 + 2 + 8 + 2000 * 0.0175 + 6) * 2,

                pension_civile_salarie = -167.80 * 2,
                rafp_salarie = -20 * 2,
                cotisations_salariales_contributives = -375.6,

                contribution_exceptionnelle_solidarite = -23.72 * 2,
                cotisations_salariales_non_contributives = -23.72 * 2,

                cotisations_salariales = -422.24,

                crds_salaire = -12.93 * 2,
                # csg_deductible_salaire = -131.94 * 2, # TODO: Gérer un seulf sft
                # csg_imposable_salaire = -62.09 * 2,  # # TODO: Gérer un seulf sft
                indemnite_residence = 240 * 2 / 12,
                salsuperbrut = (2000 + 500 + 20 + 1751.4) * 2 + 73.04,
                supp_familial_traitement = 73.04,
                ),
            ),
        ]
    for test_infos in tests_infos:
        scenario_arguments = test_infos.copy()
        description = scenario_arguments.pop('description')
        error_margin = scenario_arguments.pop('error_margin')
        expected_values = scenario_arguments.pop('expected_values')
        simulation = base.tax_benefit_system.new_scenario().init_single_entity(**scenario_arguments).new_simulation(
            debug = True)
        for variable, expected_value in expected_values.iteritems():
            yield check_simulation_monthly_variable, description, simulation, variable, expected_value, error_margin


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    import nose
    nose.core.runmodule(argv = [__file__, '-v', '-i test_cotsoc_fonc.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
