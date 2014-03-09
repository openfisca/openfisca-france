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

import openfisca_france
from openfisca_france.model.cotisations_sociales.travail import CAT


def test_nonsal_celib(verbose = True):
    """
    test pour un célibataire
    """
    tests_list = [
#   Célibataires à partir de : http://www.experts-comptables.fr/csoec/Focus-bases-documentaires/Auto-Entrepreneur/Simulateur-Auto-Entrepreneur-version-entreprise
             {"year" : 2013,
              "input_vars":
                    {
                     "ebic_impv" : 20000,
                    },
              "output_vars" :
                     {
#                      "rev_microsocial": 20000 - 2820, # TODO: BUGGY result
                      "microsocial" : 200,
                    }
              },
            {"year" : 2013,
              "input_vars":
                    {
                     "ebic_imps" : 20000,
                    },
              "output_vars" :
                     {
                      "rev_microsocial": 20000 - 4920,
                      "microsocial" : 340,
                    }
              },
                               {"year" : 2013,
              "input_vars":
                    {
                     "ebnc_impo" : 20000,
                    },
              "output_vars" :
                     {
                      "rev_microsocial": 20000 - 4920,
                      "microsocial" : 440,
                    }
              },
            ]
    from openfisca_france.tests.utils import process_tests_list
    process_tests_list(tests_list, verbose = verbose)

# def test_nonsal_famille():  # TODO: buggy tests CHECK
#     tests_infos = dict(
#         description = u"Couple de microentrepreneur",
#         parent1 = dict(
#             birth = datetime.date(1972, 1, 1),
#             ebic_impv = 20000,
#             ),
#         parent2 = dict(
#             birth = datetime.date(1972, 1, 1),
#             ebic_impv = 10000,
#             ),
#         enfants = [
#             dict(birth = datetime.date(2000, 1, 1)),
#             dict(birth = datetime.date(2009, 1, 1)),
#             ],
#         menage = dict(
#             zone_apl = 1,
#             ),
#         year = 2013,
#         error_margin = 2,
#         expected_values = dict(
#             rev_microsocial = (20000 + 10000) - (2820 + 1410),
#             microsocial = 200 + 100,
#             ),
#         ),
#
#     TaxBenefitSystem = openfisca_france.init_country()
#     tax_benefit_system = TaxBenefitSystem()
#
#     for test_infos in tests_infos:
#         scenario_arguments = test_infos.copy()
#         description = scenario_arguments.pop('description')
#         error_margin = scenario_arguments.pop('error_margin')
#         expected_values = scenario_arguments.pop('expected_values')
#         simulation = tax_benefit_system.new_scenario().init_single_entity(**scenario_arguments).new_simulation(
#             debug = True)
#         for variable, expected_value in expected_values.iteritems():
#             yield check_simulation_variable, description, simulation, variable, expected_value, error_margin


if __name__ == '__main__':
    import sys
    import logging
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    import nose
    nose.core.runmodule(argv = [__file__, '-v'])
