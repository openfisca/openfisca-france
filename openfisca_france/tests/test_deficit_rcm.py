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


def test_deficit_rcm():
    """
    test pour un célibataire pour un revenu salarial de 20 000 €
    """

#   DÉFICITS DES REVENUS DE CAPITAUX MOBILIERS 2DC, 2AA, 2AL, 2AM, 2AN, 2AQ, 2AR
    tests_list = [
              {"year" : 2009,
              "input_vars":
                    {
                     "sali" : 20000,
                    'f2dc':5000,
                    'f2aa':1000,
                    'f2al':1000,
		   	        'f2am':1000,
                    'f2an':1000,
                    'f2aq':1000,
                    'f2ar':1000
                    },
              "output_vars" :
                    {
                     "irpp":-1086,
                    },
              },
              {"year" : 2010,
              "input_vars":
                    {
                     "sali" : 20000,
                    'f2dc':5000,
                    'f2aa':1000,
                    'f2al':1000,
		   	        'f2am':1000,
                    'f2an':1000,
                    'f2aq':1000,
                    'f2ar':1000
                    },
              "output_vars" :
                    {
                     "irpp":-1181,
                    },
              },
              {"year" : 2011,
              "input_vars":
                    {
                     "sali" : 20000,
                    'f2dc':5000,
                    'f2aa':1000,
                    'f2al':1000,
		   	        'f2am':1000,
                    'f2an':1000,
                    'f2aq':1000,
                    'f2ar':1000
                    },
              "output_vars" :
                    {
                     "irpp":-1181,
                    },
              },
              {"year" : 2012,
              "input_vars":
                    {
                     "sali" : 20000,
                    'f2dc':5000,
                    'f2aa':1000,
                    'f2al':1000,
		   	        'f2am':1000,
                    'f2an':1000,
                    'f2aq':1000,
                    'f2ar':1000
                    },
              "output_vars" :
                    {
                     "irpp":-1181,
                    },
              },
              {"year" : 2013,
              "input_vars":
                    {
                     "sali" : 20000,
                    'f2dc':5000,
                    'f2aa':1000,
                    'f2al':1000,
		   	        'f2am':1000,
                    'f2an':1000,
                    'f2aq':1000,
                    'f2ar':1000
                    },
              "output_vars" :
                    {
                     "irpp":-1170,
                    },
              },]
    from openfisca_france.tests.utils import process_tests_list
    process_tests_list(tests_list, verbose = False)


if __name__ == '__main__':
    import sys
    import logging
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
#    import nose
#    nose.core.runmodule(argv = [__file__, '-v'])
#    nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
    test_deficit_rcm()
