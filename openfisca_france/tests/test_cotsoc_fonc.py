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

import sys
import datetime
import logging
import nose
import pdb

import openfisca_france
openfisca_france.init_country(start_from = "brut")

from openfisca_core.simulations import ScenarioSimulation
from openfisca_france.model.cotisations_sociales.travail import CAT


def test_cotsoc_celib():
    """
    test pour un célibataire
    """
    # Comparaison avec la fiche de paie IPP calculé avec une cotisation transport correspondant à Paris ((.026)
    # alors qu'Openfisca la cacule pour Lyon (.0175)
    tests_list = [
#   Célibataires (pas de supplément familial de traitement
             {"year" : 2012,
              "input_vars":
                    {
                     "type_sal" : CAT["public_titulaire_etat"],
                     "salbrut" : 12 * 2000,
                     "primes" : 12 * 500,
                     "zone_apl": 1,
                    },
              "output_vars" :
                    {
                     "indemnite_residence": 60,
                     "cot_pat_pension_civile": 1371.80,
                     "cot_sal_pension_civile": 167.80,
                     "cot_sal_rafp": 20,
                     "cot_pat_rafp": 20,
                     "cotpat_transport": 2000 * 0.0175,
                     "cotpat" : 1371.80 + 6.6 + 20 + 194 + 108 + 2 + 8 + 2000 * 0.0175 + 6,
#                               pension,  ati, rafp, maladie, famille, fnal1, fnal2, csa,
                     "cotsal" : 167.80 + 20 + 23.72,
#                               pension rafp
                     "salsuperbrut": 4328.40 + 2000 * (0.0175 - 0.026),  # Correction transport
                     "csgsald" : 128.28,
                     "csgsali" : 60.36,
                     "crdssal": 12.58,
                     "salnet": 2147.26,
                    }
              },
             {"year" : 2012,
              "input_vars":
                    {
                     "type_sal" : CAT["public_titulaire_territoriale"],
                     "salbrut" : 12 * 2000,
                     "primes" : 12 * 500,
                     "zone_apl": 1,
                    },
              "output_vars" :
                    {
                     "indemnite_residence": 60,
                     "cot_pat_pension_civile": 546,
                     "cot_sal_pension_civile": 167.80,
                     "cot_sal_rafp": 20,
                     "cot_pat_rafp": 20,
                     "cotpat_transport": 2000 * 0.0175,
                     "cotpat" : 546 + 10 + 20 + 230 + 108 + 2 + 8 + 2000 * 0.0175 + 6,
#                               pension,  ati, rafp, maladie, famille, fnal1, fnal2, csa,
                     "cotsal" : 167.80 + 20 + 23.72,
#                               pension rafp, fds
                     "csgsald" : 128.28,
                     "csgsali" : 60.36,
                     "crdssal": 12.58,
                     "salsuperbrut": 3542 + 2000 * (0.0175 - 0.026),
                     "salnet": 2147.26,
                    }
              },
             {"year" : 2012,
              "input_vars":
                    {
                     "type_sal" : CAT["public_titulaire_hospitaliere"],
                     "salbrut" : 12 * 2000,
                     "primes" : 12 * 500,
                     "zone_apl": 1,
                    },
              "output_vars" :
                    {
                     "indemnite_residence": 60,
                     "cot_pat_pension_civile": 546,
                     "cot_sal_pension_civile": 167.80,
                     "cot_sal_rafp": 20,
                     "cot_pat_rafp": 20,
                     "cotpat_transport": 2000 * 0.0175,
                     "cotpat" : 546 + 10 + 20 + 230 + 108 + 20 + 2 + 8 + 2000 * 0.0175 + 6,
#                               pension,  ati, rafp, maladie, famille, feh, fnal1, fnal2, transport, csa
                     "cotpat_contrib": 546 + 20 + 20,
#                               pension,  rafp, feh
                     "cotsal" : 167.80 + 20 + 23.72,
#                               pension, rafp, except de solidarité
                     "csgsald" : 128.28,
                     "csgsali" : 60.36,
                     "crdssal": 12.58,
                     "salsuperbrut": 3562 + 2000 * (0.0175 - 0.026),  # second term is correction of transport
                     "salnet": 2147.26,
                    }
              },
             {"year" : 2011,
              "input_vars":
                    {
                     "type_sal" : CAT["public_non_titulaire"],
                     "salbrut" : 12 * 2000,
                     "primes" : 12 * 500,
                     "zone_apl": 1,
                    },
              "output_vars" :
                    {
                     "indemnite_residence": 60,
                     "cot_pat_pension_civile": 0,
                     "cot_sal_pension_civile": 0,
                     "cot_sal_rafp": 0,
                     "cot_pat_rafp": 0,
                     "cotpat_transport": 2560 * .0175,
                     "cotpat" : 212.48 + 40.96 + 90.24 + 327.68 + 138.24 + 2.56 + 10.24 + 2560 * 0.0175 + 7.68,
                     "cotsal" : 170.24 + 2.56 + 58.24 + 19.20 + 23.16,
#                              viel_plaf viel_deplaf ircantecA maladie, cot excep de solidarite
                     "cotsal_contrib": 170.24 + 2.56 + 58.24,
#                                      viel_plaf viel_deplaf ircantecA
                     "csgsald" : 128.28,
                     "csgsali" : 60.36,
                     "crdssal": 12.58,
                     "salsuperbrut": 3367.36 + 2000 * (0.0175 - 0.026),
                     "salnet": 2091.20,
                    }
              },
            ]

    passed = True
    for test in tests_list:
        year = test["year"]
        simulation = ScenarioSimulation()
        simulation.set_config(year = test["year"], nmen = 1)
        simulation.set_param()

        test_case = simulation.scenario
        for variable, value in test['input_vars'].iteritems():
            if variable in ['zone_apl']:
                test_case.menage[0].update({ variable: value})
            else:
                test_case.indiv[0].update({ variable: value})

        df = simulation.get_results_dataframe(index_by_code = True)
        simulation.output_table.calculate_prestation(simulation.prestation_by_name['salnet'])
        simulation.output_table.calculate_prestation(simulation.prestation_by_name['sal'])

        for variable, value in test['output_vars'].iteritems():

            computed_value = (simulation.output_table.table[variable] / 12).sum()
            test_assertion = abs(abs(computed_value) - value) < 1
            expression = "Test failed for variable %s on year %i and case %s: \n OpenFisca value : %s \n Real value : %s \n" % (variable, year, test['input_vars'], abs(computed_value), value)

            if not test_assertion:
                print expression
                passed = False

    assert passed, "Test failed for some variables"


def test_cotsoc_famille():
    """
    test pour un couple de fonctionnaire
    """
    tests_list = [
#  Famille avec 2 enfants
             {"year" : 2012,
              "input_vars":
                    {
                     "type_sal" : CAT["public_titulaire_etat"],
                     "salbrut" : 12 * 2000,
                     "primes" : 12 * 500,
                     "zone_apl": 1,
                    },
              "output_vars" :
                    {
                     "cot_pat_pension_civile": 1371.80,
                     "cot_sal_pension_civile": 167.80,
                     "cot_sal_rafp": 20,
                     "cot_pat_rafp": 20,
                     "csgsald" : 131.94,
                     "csgsali" : 62.09,
                     "indemnite_residence": 60,
                     "supp_familial_traitement":73.04,
                     "crdssal": 12.93,
                     "cotpat_transport": 2000 * 0.0175,
                     "cotpat" : 1371.80 + 6.6 + 20 + 194 + 108 + 2 + 8 + 2000 * 0.0175 + 6,
#                               pension,  ati, rafp, maladie, famille, fnal1, fnal2, csa,
                     "cotsal" : 167.80 + 20 + 24.45,  # cot excep de solidarité
#                               pension rafp
                     "salsuperbrut": 4401.44 + 2000 * (.0175 - .026),
                     "salnet": 2213.83,
                    }
              },
            {"year" : 2012,
              "input_vars":
                    {
                     "type_sal" : CAT["public_titulaire_etat"],
                     "salbrut" : 12 * 2000,
                     "primes" : 12 * 500,
                     "type_sal_c" : CAT["public_titulaire_etat"],
                     "salbrut_c" : 12 * 2000,
                     "primes_c" : 12 * 500,
                     "zone_apl": 2,

                    },
              "output_vars" :
                    {
                     "cot_pat_pension_civile": 1371.80 * 2,
                     "cot_sal_pension_civile": 167.80 * 2,
                     "cot_sal_rafp": 20 * 2,
                     "cot_pat_rafp": 20 * 2,
                     "csgsald" : 131.94 * 2,
                     "csgsali" : 62.09 * 2,
                     "indemnite_residence": 240 * 2 / 12,
                     "supp_familial_traitement":73.04,
                     "crdssal": 12.93 * 2,
                     "cotpat_transport": 2000 * 0.0175 * 2,
                     "cotpat" : (1371.80 + 6.6 + 20 + 194 + 108 + 2 + 8 + 2000 * 0.0175 + 6) * 2,
#                               pension,  ati, rafp, maladie, famille, fnal1, fnal2, csa,
                     "cotsal" : (167.80 + 20 + 24.45) * 2 ,  # cot excep de solidarité
#                               pension rafp
                     "salsuperbrut": (2000 + 500 + 20 + 1751.4) * 2 + 73.04,
                     "salnet": (2000 + 500 + 20 - 131.94 - 62.09 - 12.93 - (167.80 + 20 + 24.45)) * 2 + 73.04,
                    }
              },
                  ]

    passed = True
    for test in tests_list:

        year = test["year"]
        simulation = ScenarioSimulation()
        simulation.set_config(year = test["year"], nmen = 1)
        simulation.set_param()

        test_case = simulation.scenario

        test_case.addIndiv(1, datetime.date(1975, 1, 1), 'conj', 'part')
        test_case.addIndiv(2, datetime.date(2000, 1, 1), 'pac', 'enf')
        test_case.addIndiv(3, datetime.date(2009, 1, 1), 'pac', 'enf')

        for variable, value in test['input_vars'].iteritems():

            if variable in ['zone_apl']:
                test_case.menage[0].update({ variable: value})
            elif variable in ['type_sal', 'salbrut', 'primes']:
                test_case.indiv[0].update({ variable: value})
            elif variable in ['type_sal_c', 'salbrut_c', 'primes_c']:
                test_case.indiv[1].update({ variable[:-2] : value})
            else:
                print "Variable non prise en charge : ", variable
                pdb.set_trace()

        df = simulation.get_results_dataframe(index_by_code = True)
        simulation.output_table.calculate_prestation(simulation.prestation_by_name['salnet'])
        simulation.output_table.calculate_prestation(simulation.prestation_by_name['sal'])

        for variable, value in test['output_vars'].iteritems():

            computed_value = (simulation.output_table.table[variable] / 12).sum()
            test_assertion = abs(abs(computed_value) - value) < 2
            expression = "Test failed for variable %s on year %i and case %s: \n OpenFisca value : %s \n Real value : %s \n" % (variable, year, test['input_vars'], abs(computed_value), value)

            if not test_assertion:
                print expression
                passed = False

    assert passed, "Test failed for some variables"


if __name__ == '__main__':
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_cotsoc_celib()
#    test_cotsoc_famille()
#    nose.core.runmodule(argv = [__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)

