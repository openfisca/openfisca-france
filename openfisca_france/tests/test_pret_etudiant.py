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


from . import utils


def test_pret_etudiant():
    # test pour un célibataire pour un revenu salarial de 20 000 €

    # CRÉDIT D'IMPÔTS PRÊTS ÉTUDIANTS 7UK, 7VO, 7TD
    tests_list = [
        {
            "year": 2005,
            "input_vars": {
                "cho": 0,
                "sal": 20000,
                'f7uk': 4000,
                'f7vo': 1},
            "output_vars": {
                "irpp": - 1137,
                },
            },
        {
            "year": 2006,
            "input_vars": {
                "cho": 0,
                "sal": 20000,
                'f7uk': 4000,
                'f7vo': 1},
            "output_vars": {
                "irpp": - 759,
                },
            },
        {
            "year": 2007,
            "input_vars": {
                "cho": 0,
                "sal": 20000,
                'f7uk': 4000,
                'f7vo': 1},
            "output_vars": {
                "irpp": - 743,
                },
            },
        {
            "year": 2008,
            "input_vars": {
                "cho": 0,
                "sal": 20000,
                'f7td': 2000,
                'f7uk': 4000,
                'f7vo': 1},
            "output_vars": {
                "irpp": - 706,
                },
            },
        {
            "year": 2009,
            "input_vars": {
                "cho": 0,
                "sal": 20000,
                'f7td': 2000,
                'f7uk': 4000,
                'f7vo': 1},
            "output_vars": {
                "irpp": - 701,
                },
            },
        {
            "year": 2010,
            "input_vars": {
                "cho": 0,
                "sal": 20000,
                'f7td': 2000,
                'f7uk': 4000,
                'f7vo': 1},
            "output_vars": {
                "irpp": - 681,
                },
            },
        {
            "year": 2011,
            "input_vars": {
                "cho": 0,
                "sal": 20000,
                'f7td': 2000,
                'f7uk': 4000,
                'f7vo': 1},
            "output_vars": {
                "irpp": - 681,
                },
            },
        {
            "year": 2012,
            "input_vars": {
                "cho": 0,
                "sal": 20000,
                'f7td': 2000,
                'f7uk': 4000,
                'f7vo': 1},
            "output_vars": {
                "irpp": - 681,
                },
            },
        {
            "year": 2013,
            "input_vars": {
                "cho": 0,
                "sal": 20000,
                'f7td': 2000,
                'f7uk': 4000,
                'f7vo': 1},
            "output_vars": {
                "irpp": - 670,
                },
            },
        ]

    for check in utils.process_tests_list(tests_list):
        yield check


if __name__ == '__main__':
    import sys
    import logging
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
#    import nose
#    nose.core.runmodule(argv = [__file__, '-v'])
#    nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
    test_pret_etudiant()
