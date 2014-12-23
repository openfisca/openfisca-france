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

from . import utils


def test_isf_celibataire(verbose = False):
    tests_list = [
        {
            "year": 2013,
            "input_vars": {
                "sal": 50000,
                "b1bc": 5000,
                "b1ab": 2500000,
                "b2nf": 7000,
                },
            "output_vars": {
                "irpp": - 7889,
                "isf_inv_pme": 3500,
                # "tot_impot": 2144 + 7889,  # TODO: check this value
                },
            },
        ]
    for check in utils.process_tests_list(tests_list):
        yield check
