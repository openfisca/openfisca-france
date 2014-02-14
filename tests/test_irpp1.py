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


import nose
from datetime import datetime

import openfisca_france
openfisca_france.init_country()

from openfisca_core.simulations import ScenarioSimulation


def test_irpp():
    """
    test pour un célibataire pour un revenu de 20 000, 50 000 € et 150 000 €
    et des revenus de différentes origines
    """
    dico = {
# test pour un célibataire ayant un revenu salarial (1AJ)
            "sali": [
            {"year" : 2012, "amount": 20000, "irpp":-1181 },
            {"year" : 2011, "amount": 20000, "irpp":-1181 },
            {"year" : 2010, "amount": 20000, "irpp":-1201 },
                    ],
       }


    for revenu, test_list in dico.iteritems():
        for item in test_list:
            year = item["year"]
            amount = item["amount"]
            irpp = item["irpp"]
            simulation = ScenarioSimulation()
            simulation.set_config(year = year, nmen = 1)
            simulation.set_param()
            test_case = simulation.scenario
            if revenu in ["rsti", "sali"]:
                test_case.indiv[0].update({revenu:amount})
            elif revenu in ["f2da", "f2dh", "f2dc", "f2ts", "f2tr", "f4ba", "f3vg", "f3vz"]:
                test_case.declar[0].update({revenu:amount})
            else:
                assert False
            df = simulation.get_results_dataframe(index_by_code = True)
            if not abs(df.loc["irpp"][0] - irpp) < 1:
                print year
                print revenu
                print amount
                print "OpenFisca :", abs(df.loc["irpp"][0])
                print "Real value :", irpp
            assert abs(df.loc["irpp"][0] - irpp) < 1

# TODO: The amounts are wrong
#
# def test_ppe():
#     """
#     test ppe pour un célibataire
#     """
#     dico = {
# # test pour un célibataire ayant un revenu salarial (1AJ)
#             "sali": [
#                 {"year" : 2010, "amount": 12*1000/2, "ppe":-1181 },
#                 {"year" : 2010, "amount": 12*1000, "ppe":-1181 },
#                 {"year" : 2011, "amount": 12*1000/2, "ppe":-42338},
#                 {"year" : 2011, "amount": 12*1000, "ppe":-42338},
#                 ]
#             }
#     for revenu, test_list in dico.iteritems():
#         for item in test_list:
#             year = item["year"]
#             amount = item["amount"]
#             ppe = item["ppe"]
#             simulation = ScenarioSimulation()
#             simulation.set_config(year = year, nmen = 1)
#             simulation.set_param()
#             test_case = simulation.scenario
#             if revenu in ["rsti", "sali"]:
#                 test_case.indiv[0].update({revenu:amount})
#                 test_case.indiv[0].update({"ppe_tp_sa":True})
#             else:
#                 assert False
#             df = simulation.get_results_dataframe(index_by_code=True)
#             if not abs(df.loc["ppe"][0] - ppe) < 1:
#                 print year
#                 print revenu
#                 print amount
#                 print "OpenFisca :", abs(df.loc["ppe"][0])
#                 print "Real value :", ppe
#             assert abs(df.loc["ppe"][0] - ppe) < 1


if __name__ == '__main__':
    test_irpp()
#    test_ppe()
#    nose.core.runmodule(argv=[__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)



