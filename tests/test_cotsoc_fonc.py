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
import logging
import nose

import openfisca_france
openfisca_france.init_country(start_from = "brut")

from openfisca_core.simulations import ScenarioSimulation
from openfisca_france.model.cotisations_sociales.travail import CAT


def test_cotsoc():
    """
    test pour un célibataire pour un revenu de 20 000, 50 000 € et 150 000 €
    et des revenus de différentes origines
    """


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
                     "cot_pat_pension_civile": 1371.80,
                     "cot_sal_pension_civile": 167.80,
                     "cot_sal_rafp": 20,
                     "cot_pat_rafp": 20,
                     "csgsald" : 128.28,
                     "csgsali" : 60.36,
                     "indemnite_residence": 60,
                     "crdssal": 12.58,
                     "cotpat_transport": 52,
                     "cotpat" : 1371.80 + 6.6 + 20 + 194 + 108 + 2 + 8 + 52 + 6,
#                               pension,  ati, rafp, maladie, famille, fnal1, fnal2, csa,
                     "cotsal" : 167.80 + 20 ,  # 23.72
#                               pension rafp
                     "salsuperbrut": 4328.40,
                     "salnet": 2147.26,
                    }
              },  # TODO: fds et versement transport
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
                     "cot_pat_pension_civile": 546,
                     "cot_sal_pension_civile": 167.80,
                     "cot_sal_rafp": 20,
                     "cot_pat_rafp": 20,
                     "indemnite_residence": 60,
                     "cotpat_transport": 52,
                     "cotpat" : 546 + 10 + 20 + 230 + 108 + 2 + 8 + 52 + 6,
#                               pension,  ati, rafp, maladie, famille, fnal1, fnal2, csa,
                     "cotsal" : 167.80 + 20 ,  # 23.72
#                               pension rafp
                     "csgsald" : 128.28,
                     "csgsali" : 60.36,
                     "crdssal": 12.58,
                     "salsuperbrut": 3542,
                     "salnet": 2147.26,
                    }
              },  # TODO: fds et versement transport
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
                     "cot_pat_pension_civile": 546,
                     "cot_sal_pension_civile": 167.80,
                     "cot_sal_rafp": 20,
                     "cot_pat_rafp": 20,
                     "indemnite_residence": 60,
                     "cotpat_transport": 52,
                     "cotpat" : 546 + 10 + 20 + 230 + 108 + 2 + 8 + 52 + 6,
#                               pension,  ati, rafp, maladie, famille, fnal1, fnal2, csa,
                     "cotsal" : 167.80 + 20 ,  # 23.72
#                               pension rafp
                     "csgsald" : 128.28,
                     "csgsali" : 60.36,
                     "crdssal": 12.58,
                     "salsuperbrut": 3542,
                     "salnet": 2147.26,
                    }
              },  # TODO: fds et versement transport
             {"year" : 2012,
              "input_vars":
                    {
                     "type_sal" : CAT["public_non_titulaire"],
                     "salbrut" : 12 * 2000,
                     "primes" : 12 * 500,
                     "zone_apl": 1,
                    },
              "output_vars" :
                    {
                     "cot_pat_pension_civile": 0,
                     "cot_sal_pension_civile": 0,
                     "cot_sal_rafp": 0,
                     "cot_pat_rafp": 0,
                     "indemnite_residence": 60,
                     "cotpat_transport": 52,
                     "cotpat" : 546 + 10 + 20 + 230 + 108 + 2 + 8 + 52 + 6,
#                               pension,  ati, rafp, maladie, famille, fnal1, fnal2, csa,
                     "cotsal" : 170.24 + 2.56 + 52.42 + 19.20 ,  # 23.16 cot excep de solidarite
#                              viel_plaf viel_deplaf ircantecA maladie
                     "csgsald" : 128.28,
                     "csgsali" : 60.36,
                     "crdssal": 12.58,
                     "salsuperbrut": 3367.36,
                     "salnet": 2091.20,
                    }
              },  # TODO: fds et versement transport
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


if __name__ == '__main__':
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_cotsoc()
#    nose.core.runmodule(argv = [__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
