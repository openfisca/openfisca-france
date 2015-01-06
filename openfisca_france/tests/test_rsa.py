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


# Ne pas oublier d'intégrer la paje quand on simule le cas type sur le site de la cnaf pour les enfants de moins de
# 3 ans


import datetime

from openfisca_core.tools import assert_near
from . import base


def test_rsa_celibataire():
    # test rsa pour un célibataire avec différents sali

    tests_list = [
        {"year": 2014, "amount": 0, "rsa": 439},
        {"year": 2014, "amount": 5000, "rsa": 281},
        {"year": 2014, "amount": 10000, "rsa": 123},
        {"year": 2014, "amount": 12000, "rsa": 59},
        {"year": 2014, "amount": 13000, "rsa": 28},
        {"year": 2014, "amount": 14000, "rsa": 0},
        {"year": 2014, "amount": 15000, "rsa": 0},
        {"year": 2014, "amount": 20000, "rsa": 0},
        ]
    error_margin = 1
    year = 2014
    age = 29
    revenu = "salnet"
    for test in tests_list:
        amount = test["amount"]
        simulation = base.tax_benefit_system.new_scenario().init_single_entity(
            period = year - 1,
            parent1 = {
                'birth': datetime.date(year - age + 1, 1, 1),
                revenu: amount,
                },
            ).new_simulation(debug = True)
        calculated_rsa = simulation.calculate('rsa', "{}-01".format(year))
        yield assert_near, calculated_rsa, test['rsa'], error_margin


def test_rsa_couple():
    # test pour un célibataire avec son age variant entre 18 et 25 ans
    tests_list = [
        {
            "year": 2014,
            "parent1": {
                "salnet": 0,
                "age": 29,
                },
            "parent2": {
                "salnet": 0,
                "age": 29,
                },
            "rsa": 629,
            },
        {
            "year": 2014,
            "parent1": {
                "salnet": 5000,
                "age": 29,
                },
            "parent2": {
                "salnet": 0,
                "age": 29,
                },
            "rsa": 471,
            },
        {
            "year": 2014,
            "parent1": {
                "salnet": 10000,
                "age": 29,
                },
            "parent2": {
                "salnet": 0,
                "age": 29,
                },
            "rsa": 312,
            },
        {
            "year": 2014,
            "parent1": {
                "salnet": 12000,
                "age": 29,
                },
            "parent2": {
                "salnet": 0,
                "age": 29,
                },
            "rsa": 249,
            },
        {
            "year": 2014,
            "parent1": {
                "salnet": 13000,
                "age": 29,
                },
            "parent2": {
                "salnet": 0,
                "age": 29,
                },
            "rsa": 217,
            },
        {
            "year": 2014,
            "parent1": {
                "salnet": 14000,
                "age": 29,
                },
            "parent2": {
                "salnet": 0,
                "age": 29,
                },
            "rsa": 186,
            },
        {
            "year": 2014,
            "parent1": {
                "salnet": 15000,
                "age": 29,
                },
            "parent2": {
                "salnet": 0,
                "age": 29,
                },
            "rsa": 154,
            },
        {
            "year": 2014,
            "parent1": {
                "salnet": 16000,
                "age": 29,
                },
            "parent2": {
                "salnet": 0,
                "age": 29,
                },
            "rsa": 122,
            },
        {
            "year": 2014,
            "parent1": {
                "salnet": 17000,
                "age": 29,
                },
            "parent2": {
                "salnet": 0,
                "age": 29,
                },
            "rsa": 91,
            },
        {
            "year": 2014,
            "parent1": {
                "salnet": 18000,
                "age": 29,
                },
            "parent2": {
                "salnet": 0,
                "age": 29,
                },
            "rsa": 59,
            },
        {
            "year": 2014,
            "parent1": {
                "salnet": 19000,
                "age": 29,
                },
            "parent2": {
                "salnet": 0,
                "age": 29,
                },
            "rsa": 27,
            },
        {
            "year": 2014,
            "parent1": {
                "salnet": 9000,
                "age": 29,
                },
            "parent2": {
                "salnet": 11000,
                "age": 29,
                },
            "rsa": 0,
            },
        # test si le déclarant a moins 25 ans  et le conjoint plus de 25
        {
            "year": 2014,
            "parent1": {
                "salnet": 400 * 12,
                "age": 21,
                },
            "parent2": {
                "salnet": 3000 * 12,
                "age": 21,
                },
            "rsa": 0,
            },
        # test pour moins de 25 ans pour les deux
        {
            "year": 2014,
            "parent1": {
                "salnet": 400 * 12,
                "age": 21,
                },
            "parent2": {
                "salnet": 3000 * 12,
                "age": 21,
                },
            "rsa": 0,
            },
        # test pour un parent isolé avec 1 enfant de 2 ans
        # {
        #     "year": 2014,
        #     "parent1": {
        #         "salnet": 5000,
        #         "age": 29,
        #         },
        #     "enfants": [
        #         dict(age = 2),
        #         ],
        #     "rsa": 550,
        #     },
        # test pour un couple avec un enfant de moins de 3 ans
        # Problème avec site de la cnaf pour changer les revenus
        {
            "year": 2014,
            "parent1": {
                "salnet": 0,
                "age": 29,
                },
            "parent2": {
                "salnet": 0,
                "age": 29,
                },
            "enfants": [
                dict(age = 2),
                ],
            "rsa": 565,
            # "paje": 184.62,
            },
        # TODO: Do not pass
        # {
        #     "year": 2014,
        #     "parent1": {
        #         "salnet": 5000,
        #         "age": 29,
        #         },
        #     "parent2": {
        #         "salnet": 0,
        #         "age": 29,
        #         },
        #     "enfants": [
        #         dict(age = 2),
        #         ],
        #     "rsa": 444,  # Unsure about the value
        #     },
        # TODO: do not pass
        # {
        #     "year": 2014,
        #     "parent1": {
        #         "salnet": 10000,
        #         "age": 29,
        #         },
        #     "parent2": {
        #         "salnet": 0,
        #         "age": 29,
        #         },
        #     "enfants": [
        #         dict(age = 2),
        #         ],
        #     "rsa": 565,  # TODO: check that value
        #     },
        # "revenu": [
        #     {"year": 2014, "amountdéclarant": 0, "amountconjoint":0,   "rsa": 750  },
        #     {"year": 2014, "amountdéclarant": 5000, "amountconjoint":0,   "rsa": 592  },
        #     {"year": 2014, "amountdéclarant": 10000, "amountconjoint":0,   "rsa": 434  },
        #     {"year": 2014, "amountdéclarant": 12000, "amountconjoint":0,   "rsa": 370  },
        #     {"year": 2014, "amountdéclarant": 13000, "amountconjoint":0,   "rsa": 339  },
        #     {"year": 2014, "amountdéclarant": 14000, "amountconjoint":0,   "rsa": 307  },
        #     {"year": 2014, "amountdéclarant": 15000, "amountconjoint":0,   "rsa": 275  },
        #     {"year": 2014, "amountdéclarant": 16000, "amountconjoint":0,   "rsa": 244  },
        #     {"year": 2014, "amountdéclarant": 17000, "amountconjoint":0,   "rsa": 212  },
        #     {"year": 2014, "amountdéclarant": 18000, "amountconjoint":0,   "rsa": 180 },
        #     {"year": 2014, "amountdéclarant": 19000, "amountconjoint":0,   "rsa": 149  },
        #     {"year": 2014, "amountdéclarant": 20000, "amountconjoint":0,   "rsa": 117  },
        #     {"year": 2014, "amountdéclarant": 21000, "amountconjoint":0,   "rsa": 85 },
        #     {"year": 2014, "amountdéclarant": 22000, "amountconjoint":0,   "rsa": 54  },
        #     {"year": 2014, "amountdéclarant": 23000, "amountconjoint":0,   "rsa": 22  },
        #     {"year": 2014, "amountdéclarant": 24000, "amountconjoint":0,   "rsa": 0 },
        #     ],
        # test pour enfants ayant entre 3 et 13 ans
        {
            "year": 2014,
            "parent1": {
                "salnet": 0,
                "age": 29,
                },
            "parent2": {
                "salnet": 0,
                "age": 29,
                },
            "enfants": [
                dict(age = 10),
                ],
            "rsa": 750,
            },
        ]

    error_margin = 1
    for test in tests_list:
        print test
        test = test.copy()
        year = test.pop('year')
        test['period'] = year - 1
        target_rsa = test.pop("rsa")  # enlève rsa du dictionnaire et l'assigne a calculated_rsa
        scenario = base.tax_benefit_system.new_scenario().init_single_entity(**test)
        scenario.suggest()
        simulation = scenario.new_simulation(debug = True)
        calculated_rsa = simulation.calculate('rsa', "{}-01".format(year))
        yield assert_near, calculated_rsa, target_rsa, error_margin


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)

    test_rsa_celibataire()
    test_rsa_couple()


# TODO:  Reste des tests RSA codés par Thimothés à coder sous forme de test


# import datetime
#
#
# def check_rsa(amount, irpp, revenu, simulation, year):
#    calculated_irpp = simulation.calculate('irpp')
#    assert abs(calculated_irpp - irpp) < 1, "Error in irpp for revenu {} = {} in year {}: Got {}, expected {}".format(
#        revenu, amount, year, calculated_irpp, irpp)
#
#
#
#
#
#
#
#
# def test_rsa():
#    """
#    test pour un célibataire pour un revenu de 0,  5000, 10000, 12000, 13 000, 14 000, 15 000 €
#    et des revenus de différentes origines
#    """
#    dico = {
# # test pour un célibataire ayant un revenu salarial (1AJ)
#            "revenu": [
#            {"year": 2014, "amount": 0,  "rsa": 439  },
#            {"year": 2014, "amount": 5000, "rsa": 281  },
#            {"year": 2014, "amount": 10000, "rsa": 123},
#            {"year": 2014, "amount": 12000, "rsa": 59},
#            {"year": 2014, "amount": 13000, "rsa": 28},
#            {"year": 2014, "amount": 14000, "rsa": 0},
#            {"year": 2014, "amount": 15000, "rsa": 0},        ],
#
#
# #  rsa pour un couple
#    """
#    test pour un couple dont seul le déclarant a un revenu, pour un revenu de ,  5000, 10000, 12000, 13 000, 14 000,
#    15 000 € et des revenus de différentes origines
#    """
#
# # test pour un couple ayant un revenu salarial (1AJ)
#            "revenu": [
#            {"year": 2014, "amountdéclarant": 0, "amountconjoint":0,   "rsa": 629  },
#            {"year": 2014, "amountdéclarant": 5000, "amountconjoint":0,   "rsa": 471  },
#            {"year": 2014, "amountdéclarant": 10000, "amountconjoint":0,   "rsa": 312  },
#            {"year": 2014, "amountdéclarant": 12000, "amountconjoint":0,   "rsa": 249  },
#            {"year": 2014, "amountdéclarant": 13000, "amountconjoint":0,   "rsa": 217  },
#            {"year": 2014, "amountdéclarant": 14000, "amountconjoint":0,   "rsa": 186  },
#            {"year": 2014, "amountdéclarant": 15000, "amountconjoint":0,   "rsa": 154  },
#            {"year": 2014, "amountdéclarant": 16000, "amountconjoint":0,   "rsa": 122  },
#            {"year": 2014, "amountdéclarant": 17000, "amountconjoint":0,   "rsa": 91  },
#            {"year": 2014, "amountdéclarant": 18000, "amountconjoint":0,   "rsa": 59  },
#            {"year": 2014, "amountdéclarant": 19000, "amountconjoint":0,   "rsa": 27  },
#            {"year": 2014, "amountdéclarant": 20000, "amountconjoint":0,   "rsa": 0  },
#                    ],
#
# # rsa_couple_1enfant_entre_0_et_3_ans():
#    """
#    test pour un couple avec 1 enfant de moins de 3 ans, dont seul le déclarant a un revenu, pour un revenu de 0, 5000,
#    10000, 12000, 13 000, 14 000, 15 000, 16 OOO, 17 000, 18 000, 19 000, 20 000, 22 000, 23 000, 24 000 €
#    et des revenus de différentes origines
#    """
# # test pour un couple avec 1 enfant de moins de 3 ans ayant un revenu salarial (1AJ)
#            "revenu": [
#            {"year": 2014, "amountdéclarant": 0, "amountconjoint":0,   "rsa": 750  },
#            {"year": 2014, "amountdéclarant": 5000, "amountconjoint":0,   "rsa": 592  },
#            {"year": 2014, "amountdéclarant": 10000, "amountconjoint":0,   "rsa": 434  },
#            {"year": 2014, "amountdéclarant": 12000, "amountconjoint":0,   "rsa": 370  },
#            {"year": 2014, "amountdéclarant": 13000, "amountconjoint":0,   "rsa": 339  },
#            {"year": 2014, "amountdéclarant": 14000, "amountconjoint":0,   "rsa": 307  },
#            {"year": 2014, "amountdéclarant": 15000, "amountconjoint":0,   "rsa": 275  },
#            {"year": 2014, "amountdéclarant": 16000, "amountconjoint":0,   "rsa": 244  },
#            {"year": 2014, "amountdéclarant": 17000, "amountconjoint":0,   "rsa": 212  },
#            {"year": 2014, "amountdéclarant": 18000, "amountconjoint":0,   "rsa": 180 },
#            {"year": 2014, "amountdéclarant": 19000, "amountconjoint":0,   "rsa": 149  },
#            {"year": 2014, "amountdéclarant": 20000, "amountconjoint":0,   "rsa": 117  },
#            {"year": 2014, "amountdéclarant": 21000, "amountconjoint":0,   "rsa": 85 },
#            {"year": 2014, "amountdéclarant": 22000, "amountconjoint":0,   "rsa": 54  },
#            {"year": 2014, "amountdéclarant": 23000, "amountconjoint":0,   "rsa": 22  },
#            {"year": 2014, "amountdéclarant": 24000, "amountconjoint":0,   "rsa": 0 },
#                        ],
#
#
# #  rsa_couple_2enfants_entre_0_et_3_ans():
#    """
#    test pour un couple avec 2 enfants de moins de 3 ans, dont seul le déclarant a un revenu, pour un revenu de 0,
#    5000, 10000,  15 000, 20 000, 25 000, 30 000 €
#    et des revenus de différentes origines
#    """
# # test pour un couple avec 2 enfant de moins de 3 ans ayant un revenu salarial (1AJ)
#            "revenu": [
#
#            {"year": 2014, "amountdéclarant": 0, "amountconjoint":0,   "rsa": 900  },
#            {"year": 2014, "amountdéclarant": 5000, "amountconjoint":0,   "rsa": 742  },
#            {"year": 2014, "amountdéclarant": 10000, "amountconjoint":0,   "rsa": 584  },
#            {"year": 2014, "amountdéclarant": 15000, "amountconjoint":0,   "rsa": 425  },
#            {"year": 2014, "amountdéclarant": 20000, "amountconjoint":0,   "rsa": 267  },
#            {"year": 2014, "amountdéclarant": 25000, "amountconjoint":0,   "rsa": 109  },
#            {"year": 2014, "amountdéclarant": 30000, "amountconjoint":0,   "rsa": 0  },
#                    ],
#
# # rsa_couple_3enfants_entre_0_et_3_ans:
#    """
#    test pour un couple avec 3 enfants de moins de 3 ans, dont seul le déclarant a un revenu, pour un revenu de 0,
#    5000, 10000,  15 000, 20 000, 25 000, 30 000, 35 000 €
#    et des revenus de différentes origines
#    """
#
# # test pour un couple avec 2 enfant de moins de 3 ans ayant un revenu salarial (1AJ)
#            "revenu": [
#
#            {"year": 2014, "amountdéclarant": 0, "amountconjoint":0,   "rsa":  1100 },
#            {"year": 2014, "amountdéclarant": 5000, "amountconjoint":0,   "rsa": 942  },
#            {"year": 2014, "amountdéclarant": 10000, "amountconjoint":0,   "rsa":  783 },
#            {"year": 2014, "amountdéclarant": 15000, "amountconjoint":0,   "rsa": 625  },
#            {"year": 2014, "amountdéclarant": 20000, "amountconjoint":0,   "rsa":  466 },
#            {"year": 2014, "amountdéclarant": 25000, "amountconjoint":0,   "rsa": 308  },
#            {"year": 2014, "amountdéclarant": 30000, "amountconjoint":0,   "rsa": 150  },
#            {"year": 2014, "amountdéclarant": 35000, "amountconjoint":0,   "rsa":  0 },
#                    ],
#            }
#
#
#
#
#
#
#    for revenu, test_list in dico.iteritems():
#        for item in test_list:
#            year = item["year"]
#            amount = item["amount"]
#            irpp = item["irpp"]
#            fiscal_values = ["f2da", "f2dh", "f2dc", "f2ts", "f2tr", "f4ba", "f3vg", "f3vz"]
#
# #            if revenu != "f2dc":
# #                continue
#
#            if revenu in ["rsti", "salnet"]:
#
#                simulation = base.tax_benefit_system.new_scenario().init_single_entity(
#                    period = year,
#                    parent1 = {'birth': datetime.date(year - 40, 1, 1),
#                               revenu: amount,
#                               },
#                    ).new_simulation(debug = True)
#            elif revenu in fiscal_values:
#                simulation = base.tax_benefit_system.new_scenario().init_single_entity(
#                    period = year,
#                    parent1 = {'birth': datetime.date(year - 40, 1, 1),
#                               },
#                    foyer_fiscal = {revenu: amount},
#                    ).new_simulation(debug = True)
#
#            yield check_rsa, amount, irpp, revenu, simulation, year
#
#
# if __name__ == '__main__':
#    import logging
#    import sys
#    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
# #    import nose
# #    nose.core.runmodule(argv = [__file__, '-v'])
# #    nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
#
#    for function_and_arguments in test_rsa():
#        function_and_arguments[0](*function_and_arguments[1:])
