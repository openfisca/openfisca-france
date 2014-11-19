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

from ..model.cotisations_sociales.travail import CAT
from . import base


def check_simulation_monthly_variable(description, simulation, variable, expected_value, error_margin):
    calculated_value = (simulation.calculate(variable) / 12).sum()  # monthly values
    assert abs(calculated_value - expected_value) < error_margin, u'Variable "{} = {}. Expected: {}'.format(
        variable, calculated_value, expected_value)


def test():
    # Comparaison avec la fiche de paie IPP calculée avec une cotisation transport correspondant à Paris ((.026)
    # alors qu'Openfisca la caclule pour Lyon (.0175)
    tests_infos = [
        dict(
            period = 2012,
            description = u"Célibataire public_titulaire_etat",
            parent1 = dict(
                birth = datetime.date(1972, 1, 1),
                primes_fonction_publique = 12 * 500,
                salbrut = 12 * 2000,
                type_sal = CAT['public_titulaire_etat'],
                ),
            menage = dict(
                zone_apl = 1,
                ),

            error_margin = 1,
            expected_values = dict(
                cotpat = -(1371.80 + 6.6 + 20 + 194 + 108 + 2 + 8 + 2000 * 0.0175 + 6),
                # pension, ati, rafp, maladie, famille, fnal1, fnal2, csa,
                cot_pat_pension_civile = -1371.80,
                cot_pat_rafp = -20,
                cotpat_transport = -2000 * 0.0175,
                cotsal = -(167.80 + 20 + 23.72),
                # pension, rafp
                cot_sal_pension_civile = -167.80,
                cot_sal_rafp = -20,
                csgsald = -128.28,
                csgsali = -60.36,
                crdssal = -12.58,
                indemnite_residence = 60,
                salnet = 2147.26,
                salsuperbrut = 4328.40 + 2000 * (0.0175 - 0.026),  # Correction transport
                ),
            ),
        dict(
            period = 2012,
            description = u"Célibataire public_titulaire_territoriale",
            parent1 = dict(
                birth = datetime.date(1972, 1, 1),
                primes_fonction_publique = 12 * 500,
                salbrut = 12 * 2000,
                type_sal = CAT['public_titulaire_territoriale'],
                ),
            menage = dict(
                zone_apl = 1,
                ),

            error_margin = 1,
            expected_values = dict(
                cotpat = -(546 + 10 + 20 + 230 + 108 + 2 + 8 + 2000 * 0.0175 + 6),
                # pension, ati, rafp, maladie, famille, fnal1, fnal2, csa,
                cot_pat_pension_civile = -546,
                cot_pat_rafp = -20,
                cotpat_transport = -2000 * 0.0175,
                cotsal = -(167.80 + 20 + 23.72),
                # pension, rafp
                cot_sal_pension_civile = -167.80,
                cot_sal_rafp = -20,
                csgsald = -128.28,
                csgsali = -60.36,
                crdssal = -12.58,
                indemnite_residence = 60,
                salnet = 2147.26,
                salsuperbrut = 3542 + 2000 * (0.0175 - 0.026),
                ),
            ),
        dict(
            period = 2012,
            description = u"Célibataire public_titulaire_hospitaliere",
            parent1 = dict(
                birth = datetime.date(1972, 1, 1),
                primes_fonction_publique = 12 * 500,
                salbrut = 12 * 2000,
                type_sal = CAT['public_titulaire_hospitaliere'],
                ),
            menage = dict(
                zone_apl = 1,
                ),

            error_margin = 1,
            expected_values = dict(
                cotpat = -(546 + 10 + 20 + 230 + 108 + 20 + 2 + 8 + 2000 * 0.0175 + 6),
                # pension,  ati, rafp, maladie, famille, feh, fnal1, fnal2, transport, csa
                cotpat_contrib = -(546 + 20 + 20),
                # pension,  rafp, feh
                cot_pat_pension_civile = -546,
                cot_pat_rafp = -20,
                cotpat_transport = -2000 * 0.0175,
                cotsal = -(167.80 + 20 + 23.72),
                # pension, rafp, except de solidarité
                cot_sal_pension_civile = -167.80,
                cot_sal_rafp = -20,
                csgsald = -128.28,
                csgsali = -60.36,
                crdssal = -12.58,
                indemnite_residence = 60,
                salnet = 2147.26,
                salsuperbrut = 3562 + 2000 * (0.0175 - 0.026),
                ),
            ),
        dict(
            period = 2011,
            description = u"Célibataire public_non_titulaire",
            parent1 = dict(
                birth = datetime.date(1972, 1, 1),
                primes_fonction_publique = 12 * 500,
                salbrut = 12 * 2000,
                type_sal = CAT['public_non_titulaire'],
                ),
            menage = dict(
                zone_apl = 1,
                ),

            error_margin = 1,
            expected_values = dict(
                # cotpat = 212.48 + 40.96 + 90.24 + 327.68 + 138.24 + 2.56 + 10.24 + 2560 * 0.0175 + 7.68,
                cot_pat_pension_civile = 0,
                cot_pat_rafp = 0,
                cotpat_transport = -2560 * 0.0175,
                # cotsal = -(170.24 + 2.56 + 58.24 + 19.20 + 23.16),
                # viel_plaf viel_deplaf ircantecA maladie, cot excep de solidarite
                cotsal_contrib = -(170.24 + 2.56 + 58.24),
                # viel_plaf viel_deplaf ircantecA
                cot_sal_pension_civile = 0,
                cot_sal_rafp = 0,
                # csgsald = 128.28,
                csgsali = -60.36,
                crdssal = -12.58,
                indemnite_residence = 60,
                # salnet = 2091.20,
                # salsuperbrut = 3367.36 + 2000 * (0.0175 - 0.026),
                ),
            ),
        dict(
            period = 2012,
            description = u"Couple 1 fonctionnaire public_titulaire_etat 2 enfants",
            parent1 = dict(
                birth = datetime.date(1972, 1, 1),
                primes_fonction_publique = 12 * 500,
                salbrut = 12 * 2000,
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
                cotpat = -(1371.80 + 6.6 + 20 + 194 + 108 + 2 + 8 + 2000 * 0.0175 + 6),
                # pension, ati, rafp, maladie, famille, fnal1, fnal2, csa,
                cot_pat_pension_civile = -1371.80,
                cot_pat_rafp = -20,
                cotpat_transport = -2000 * 0.0175,
                cotsal = -(167.80 + 20 + 24.45),  # cot excep de solidarité
                # pension rafp
                cot_sal_pension_civile = -167.80,
                cot_sal_rafp = -20,
                crdssal = -12.93,
                csgsald = -131.94,
                csgsali = -62.09,
                indemnite_residence = 60,
                salnet = 2213.83,
                salsuperbrut = 4401.44 + 2000 * (.0175 - .026),
                supp_familial_traitement = 73.04,
                ),
            ),
        dict(
            period = 2012,
            description = u"Couple 2 fonctionnaires public_titulaire_etat 2 enfants",
            parent1 = dict(
                birth = datetime.date(1972, 1, 1),
                primes_fonction_publique = 12 * 500,
                salbrut = 12 * 2000,
                type_sal = CAT['public_titulaire_etat'],
                ),
            parent2 = dict(
                birth = datetime.date(1972, 1, 1),
                primes_fonction_publique = 12 * 500,
                salbrut = 12 * 2000,
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
                cotpat = -(1371.80 + 6.6 + 20 + 194 + 108 + 2 + 8 + 2000 * 0.0175 + 6) * 2,
                # pension,  ati, rafp, maladie, famille, fnal1, fnal2, csa,
                cot_pat_pension_civile = -1371.80 * 2,
                cot_pat_rafp = -20 * 2,
                cotpat_transport = -2000 * 0.0175 * 2,
                # cotsal = -(167.80 + 20 + 24.45) * 2 ,  # cot excep de solidarité
                # pension rafp
                cot_sal_pension_civile = -167.80 * 2,
                cot_sal_rafp = -20 * 2,
                crdssal = -12.93 * 2,
                # csgsald = -131.94 * 2,
                # csgsali = -62.09 * 2,
                indemnite_residence = 240 * 2 / 12,
                # salnet = -(2000 + 500 + 20 - 131.94 - 62.09 - 12.93 - (167.80 + 20 + 24.45)) * 2 + 73.04,
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
