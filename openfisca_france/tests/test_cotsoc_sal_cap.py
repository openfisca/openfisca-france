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


import openfisca_france
openfisca_france.init_country()
from openfisca_core.simulations import ScenarioSimulation


def test_cotsoc():
    """
    test pour un célibataire pour un revenu de 20 000, 50 000 € et 150 000 €
    et des revenus de différentes origines
    """
    dico = {
# test pour un célibataire ayant un revenu salarial (1AJ)
#            "sali": [
#            {"year" : 2010, "amount": 20000, "irpp":-1181 },
#            {"year" : 2011, "amount": 20000, "irpp":-1181 },
#            {"year" : 2010, "amount": 50000, "irpp":-7934 },
#            {"year" : 2011, "amount": 50000, "irpp":-7934 },
#            {"year" : 2010, "amount": 150000, "irpp":-42338},
#            {"year" : 2011, "amount": 150000, "irpp":-42338}
#                    ],
# test pour un retraité célibataire ayant une pension (1AS)
#            "rsti": [
#            {"year" : 2010, "amount": 20000, "irpp":-1181 },
#            {"year" : 2011, "amount": 20000, "irpp":-1181 },
#            {"year" : 2010, "amount": 50000, "irpp":-8336 },
#            {"year" : 2011, "amount": 50000, "irpp":-8336 },
#            {"year" : 2010, "amount": 150000, "irpp":-46642 },
#            {"year" : 2011, "amount": 150000, "irpp":-46642 },
#                    ],
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
# # test sur un revenu (2DH) issu des produits d'assurance vie
# # et de capitalisation soumis au prélèvement libératoire de 7.5 %
#            "f2dh" :[
#            {"year" : 2010, "amount": 20000, "irpp":345},
#            {"year" : 2011, "amount": 20000, "irpp":345},
#            {"year" : 2010, "amount": 50000, "irpp":345},
#            {"year" : 2011, "amount": 50000, "irpp":345},
#            {"year" : 2010, "amount": 150000, "irpp":345},
#            {"year" : 2011, "amount": 150000, "irpp":345},
# Célibataire sans enfant                   ],
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


    for revenu, test_list in dico.iteritems():
        for item in test_list:
            year = item["year"]
            amount = item["amount"]

            for var, value in item["vars"].iteritems():
                simulation = ScenarioSimulation()
                simulation.set_config(year = year, nmen = 1)
                simulation.set_param()

#                 from openfisca_qt.scripts.cecilia import complete_2012_param  # TODO: FIXME when 2012 done
#                 if year == 2012:
#                     complete_2012_param(simulation.P)

                test_case = simulation.scenario
                if revenu in ["rsti", "sali"]:
                    test_case.indiv[0].update({revenu: amount})
                elif revenu in ["f2da", "f2dh", "f2dc", "f2ts", "f2tr", "f4ba", "f3vg", "f3vz", "f2fu", "f4ba", "f2go"]:
                    test_case.declar[0].update({revenu: amount})
                else:
                    print revenu
                    assert False
                df = simulation.get_results_dataframe(index_by_code = True)
                if var in df.columns:
                    val = df.loc[var][0]
                else:
                    val = simulation.output_table.table[var][0]
                test = abs(val - value)
                if not (test < 1):
                    print test
                    print year
                    print revenu
                    print amount
                    print var
                    print "OpenFisca :", val
                    print "Real value :", value
                # assert test < 1

def test_cotsoc_cap_celib():
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

    passed = True
    for test in tests_list:
        year = test["year"]
        simulation = ScenarioSimulation()
        simulation.set_config(year = test["year"], nmen = 1)
        simulation.set_param()

        test_case = simulation.scenario
        for variable, value in test['input_vars'].iteritems():
                if variable in []:
                    test_case.indiv[0].update({ variable: value})
                elif variable in ["f2da", "f2dh", "f2dc", "f2ts", "f2tr", "f4ba", "f3vg", "f3vz", "f2fu", "f4ba", "f2go", "f2dc", "f2ca", "f4ba", "f4bb", "f4bc", "f4bd", "f4be", "f4bf"]:
                    test_case.declar[0].update({variable: value})
                else:
                    print variable
                    assert False

        for variable, value in test['output_vars'].iteritems():
            df = simulation.get_results_dataframe(index_by_code = True)
            if variable in df.columns:
                val = df.loc[variable][0]
            else:
                val = simulation.output_table.table[variable][0]
            difference = abs(val - value)
            passed = (difference < 1)
            if not passed:
                print "Il y a une différence : ", difference
                print "Pour le scénario", test['input_vars']
                print year
                print variable
                print "OpenFisca :", val
                print "Real value :", value , "\n \n"
                expression = "Test failed for variable %s on year %i and case %s: \n OpenFisca value : %s \n Real value : %s \n" % (variable, year, test['input_vars'], abs(val), value)
                assert passed, expression

if __name__ == '__main__':
    import  logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_cotsoc()
    test_cotsoc_cap_celib()
#    import nose
#    nose.core.runmodule(argv = [__file__, '-v', '-i test_cotsoc_sal_cap.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
