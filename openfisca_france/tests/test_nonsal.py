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

from openfisca_france.tests.utils import process_tests_list

def test_nonsal_celib():
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
                      "rev_microsocial": 20000 - 2820,
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

    process_tests_list(tests_list)


def test_nonsal_famille():
    """
    test pour un couple de fonctionnaire
    """
    tests_list = [
# Couple de microentrepreneur
               {"year" : 2013,
              "input_vars":
                    {
                     "ebic_impv" : 20000,
                      "ebic_impv_c" : 10000,
                    },
              "output_vars" :
                     {
                      "rev_microsocial": (20000 + 10000) - (2820 + 1410),
                      "microsocial" : 200 + 100,
                    }
              },
                  ]

    process_tests_list(tests_list)


if __name__ == '__main__':
    import sys
    import logging
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_nonsal_celib()
    test_nonsal_famille()
