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




def test_cotsoc():
    """
    Cotisations sur les revenus du capital
    """

    cotsoc_cap = {
    # test sur un revenu des actions soumises à un prélèvement libératoire de 21 % (2DA)
            "f2da" : [
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_cap_lib":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_cap_lib":-.082 * 20000,
                 "crds_cap_lib":-.005 * 20000 } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_cap_lib":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_lib":-.082 * 20000,
                 "crds_cap_lib":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" : {"prelsoc_cap_lib":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_lib":-.082 * 20000,
                 "crds_cap_lib":-.005 * 20000 } }
                    ],
    # Célibataire sans enfant
    # test sur un revenu des actions et  parts (2DC)
            "f2dc" :[
            {"year" : 2013, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-1360,
                 "csg_cap_bar":-1640,
                 "crds_cap_bar":-100,
                 "ir_plaf_qf": 330,
                 "irpp":-0} },
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
                     ],

    # # test sur le Revenus imposables des titres non côtés détenus dans le PEA et distributions perçues via votre entreprise
    # ## donnant droit à abattement (2fu)
            "f2fu" :[
            {"year" : 2013, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-1360,
                 "csg_cap_bar":-1640,
                 "crds_cap_bar":-100,
                 "ir_plaf_qf": 330,
                 "irpp":0} },
                     ],
    # Autres revenus distribués et revenus des structures soumises hors de France à un régime fiscal privilégié (2Go)
            "f2go" :[
            {"year" : 2013, "amount": 20000,
             "vars" :
                {"rev_cat_rvcm" : 25000,
                 "prelsoc_cap_bar":-1700,
                 "csg_cap_bar":-2050,
                 "crds_cap_bar":-125,
                 "ir_plaf_qf": 2150,
                 "irpp":-2150 } },
                     ],
            "f2ts" :[
            {"year" : 2013, "amount": 20000,
             "vars" :
                {"rev_cat_rvcm" : 20000,
                 "prelsoc_cap_bar":-1360,
                 "csg_cap_bar":-1640,
                 "crds_cap_bar":-100,
                 "ir_plaf_qf": 1450,
                 "irpp":-1450 } },
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
                     ],
    # # test sur les intérêts (2TR)
            "f2tr" :[
            {"year" : 2013, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-1360,
                 "csg_cap_bar":-1640,
                 "crds_cap_bar":-100,
                 "ir_plaf_qf": 1450,
                 "irpp":-1450 } },
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000, } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" :
                {"prelsoc_cap_bar":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_cap_bar":-.082 * 20000,
                 "crds_cap_bar":-.005 * 20000 } },
                     ],
    # # test sur les revenus fonciers (4BA)
            "f4ba":[
            {"year" : 2013, "amount": 20000,
             "vars" :
                {"prelsoc_fon":-1360,
                 "csg_fon":-1640,
                 "crds_fon":-100,
                 "ir_plaf_qf": 1450,
                 "irpp":-1450} },
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_fon":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_fon":-.082 * 20000,
                 "crds_fon":-.005 * 20000,
                 "irpp" :-1461 } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_fon":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_fon":-.082 * 20000,
                 "crds_fon":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" :
                {"prelsoc_fon":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_fon":-.082 * 20000,
                 "crds_fon":-.005 * 20000 } },
                     ],
    # # test (3VG) Plus-values de cession de valeurs mobilières, droits sociaux et gains assimilés
            "f3vg" :[
            {"year" : 2013, "amount": 20000,
             "vars" :
                {"prelsoc_pv_mo":-1360,
                 "csg_pv_mo":-1640,
                 "crds_pv_mo":-100,
                 "ir_plaf_qf": 1450,
                 "irpp":-1450} },
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_pv_mo":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_pv_mo":-.082 * 20000,
                 "crds_pv_mo":-.005 * 20000 } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_pv_mo":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_pv_mo":-.082 * 20000,
                 "crds_pv_mo":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" :
                {"prelsoc_pv_mo":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_pv_mo":-.082 * 20000,
                 "crds_pv_mo":-.005 * 20000 } },
            {"year" : 2006, "amount": 20000,
             "vars" :
                {"prelsoc_pv_mo":-460 ,
                 "csg_pv_mo":-1640,
                 "crds_pv_mo":-100} },
                     ],
    # # test sur les plus-values immobilières (3VZ)
            "f3vz" :[
            {"year" : 2012, "amount": 20000,
             "vars" :
                {"prelsoc_pv_immo":-(4.5 + 2 + 0.3) * 0.01 * 20000,
                 "csg_pv_immo":-.082 * 20000,
                 "crds_pv_immo":-.005 * 20000 } },
            {"year" : 2011, "amount": 20000,
             "vars" :
                {"prelsoc_pv_immo":-(3.4 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_pv_immo":-.082 * 20000,
                 "crds_pv_immo":-.005 * 20000 } },
            {"year" : 2010, "amount": 20000,
             "vars" :
                {"prelsoc_pv_immo":-(2.2 + 1.1 + 0.3) * 0.01 * 20000,
                 "csg_pv_immo":-.082 * 20000,
                 "crds_pv_immo":-.005 * 20000 } },
                     ],
            }

    for revenu, test_list in cotsoc_cap.iteritems():
        for item in test_list:
            year = item["year"]
            amount = item["amount"]

            for var, value in item["vars"].iteritems():
                parent1 = dict(birth = datetime.date(year - 40, 1, 1))
                foyer_fiscal = dict()
                if revenu in ["rsti", "sali"]:
                    parent1[revenu] = value
                elif revenu in ["f2da", "f2dh", "f2dc", "f2ts", "f2tr", "f4ba", "f3vg", "f3vz", "f2fu", "f4ba", "f2go"]:
                    foyer_fiscal[revenu] = amount
                else:
                    print revenu
                    assert False

                TaxBenefitSystem = openfisca_france.init_country()
                tax_benefit_system = TaxBenefitSystem()
                simulation = tax_benefit_system.new_scenario().init_single_entity(
                    parent1 = parent1,
                    foyer_fiscal = foyer_fiscal,
                    year = year,
                    ).new_simulation(debug = True)


                val = simulation.calculate(var)
                difference = abs(val - value)
                passed = (difference < 1)
                if not passed:
                    expression = "Test failed for variable %s on year %i : \n OpenFisca value : %s \n Real value : %s \n" % (var, year, abs(val), value)
                    assert passed, expression

def test_cotsoc_cap_celib(verbose = False):
    """
    test pour un célibataire
    """
    tests_list = [
#   Célibataires (pas de supplément familial de traitement
             {"year" : 2013,
              "input_vars":
                    {"f2dc" : 20000,
                     "f2ca" : 5000,
                    },
              "output_vars" :
                    {
                     "csg_cap_bar":-1640,
                     "crds_cap_bar":-100,
                     "prelsoc_cap_bar":-1360,
                     "rev_cat_rvcm" : 7000,
                     "irpp" : 0,
                    },
              },
# Revenus fonciers
            {"year" : 2013,
              "input_vars":
                    {"f4ba" : 20000,
                    },
              "output_vars" :
                    {"csg_fon":-1640,
                     "crds_fon":-100,
                     "prelsoc_fon":-1360,
                     "ir_plaf_qf" : 1450,
                     "rev_cat_rfon" : 20000,
                     "irpp" :-1450,
                    },
                },
             {"year" : 2013,
              "input_vars":
                    {"f4ba" : 20000,
                     "f4bb" : 1000,
                     "f4bc" : 1000,
                     "f4bd" : 1000,
                    },
              "output_vars" :
                    {"csg_fon":-1394,
                     "crds_fon":-85,
                     "prelsoc_fon":-1156,
                     "ir_plaf_qf" : 1030,
                     "rev_cat_rfon" : 17000,
                     "irpp" :-1030,
                    },
                },
            {"year" : 2006,
              "input_vars":
                    {"f4ba" : 20000,
                     "f4bb" : 1000,
                     "f4bc" : 1000,
                     "f4bd" : 1000,
                    },
              "output_vars" :
                    {"csg_fon":-1394,
                     "crds_fon":-85,
                     "prelsoc_fon":-391,
                     "rev_cat_rfon" : 17000,
                     "irpp" :-1119,
                    },
                },
             {"year" : 2013,
              "input_vars":
                    {
                     "f4be" : 10000,
                    },
              "output_vars" :
                    {"csg_fon":-574,
                     "crds_fon":-35,
                     "prelsoc_fon":-476,
                     "rev_cat_rfon" : 7000,
                     "irpp" : 0,
                    },
                },

        ]
    from openfisca_france.tests.utils import process_tests_list
    process_tests_list(tests_list)


if __name__ == '__main__':
    import  logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)

    import nose
    nose.core.runmodule(argv = [__file__, '-v', 'test_cotsoc_sal_cap.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
