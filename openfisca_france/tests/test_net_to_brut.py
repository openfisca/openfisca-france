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

from pandas import DataFrame

import openfisca_france
openfisca_france.init_country(start_from = "brut")

from openfisca_core.simulations import ScenarioSimulation
from openfisca_france.model.cotisations_sociales.travail import CAT

def test_case_study(year = 2013, verbose = False):
    '''
    Tests that _salbrut which computes "salaire brut" from "imposable" yields an amount compatbe
    with the one obtained from running openfisca satrting with a "salaire brut"
    '''

    for type_sal_category in ['prive_non_cadre', 'prive_cadre']:  # , 'public_titulaire_etat']:
        simulation = ScenarioSimulation()
        maxrev = 50000
        simulation.set_config(year = year, reforme = False, nmen = 11, maxrev = maxrev, x_axis = 'salbrut')
        simulation.scenario.indiv[0]['salbrut'] = maxrev
        simulation.scenario.indiv[0]['type_sal'] = CAT[type_sal_category]
        if type_sal_category == 'public_titulaire_etat':
            from openfisca_france.model.cotisations_sociales.travail import TAUX_DE_PRIME
            simulation.scenario.indiv[0]['primes'] = TAUX_DE_PRIME * maxrev

        simulation.set_param()

        df = simulation.get_results_dataframe(index_by_code = True)

        from openfisca_france.model.inversion_revenus import _salbrut_from_salnet
        df_b2n = df.transpose()

        if verbose:
            print df_b2n.to_string()

        salnet = df_b2n['salnet'].get_values()
        hsup = simulation.input_table.table['hsup'].get_values()
        type_sal = simulation.input_table.table['type_sal'].get_values()
        primes = simulation.input_table.table['hsup'].get_values()

        defaultP = simulation.P_default
        from pandas import DataFrame
        df_n2b = DataFrame({'salnet': salnet, 'salbrut' : _salbrut_from_salnet(salnet, hsup, type_sal, defaultP) })

        if verbose:
            print df_n2b.to_string()

        for var in ['salnet', 'salbrut']:
            passed = ((df_b2n[var] - df_n2b[var]).abs() < .01).all()

            if (not passed) or type_sal_category in ['public_titulaire_etat']:
                print (df_b2n / 12).to_string()
                print (df_n2b / 12).to_string()

            assert passed, "difference in %s for %s" % (var, type_sal_category)


def test_cho_rst(year = 2013, verbose = False):
    '''
    Tests that _chobrut which computes "chômage brut" from "net" yields an amount compatible
    with the one obtained from running openfisca satrting with a "chômage brut"
    '''
    remplacement = {'chonet' : 'chobrut', 'rstnet': 'rstbrut'}

    for var, varbrut in remplacement.iteritems():

        simulation = ScenarioSimulation()
        maxrev = 24000
        simulation.set_config(year = year, reforme = False, nmen = 11, maxrev = maxrev, x_axis = varbrut)
        simulation.set_param()
        df = simulation.get_results_dataframe(index_by_code = True)

        df_b2n = df.transpose()

        varnet = df_b2n[var].get_values()
        csg_rempl = varnet * 0 + 3

        defaultP = simulation.P_default

        if var == "chonet":
            from openfisca_france.model.inversion_revenus import _chobrut_from_chonet as _varnet_to_brut
        elif var == "rstnet":
            from openfisca_france.model.inversion_revenus import _rstbrut_from_rstnet as _varnet_to_brut

        df_n2b = DataFrame({var: varnet, varbrut : _varnet_to_brut(varnet, csg_rempl, defaultP) })

        if verbose:
            print df_n2b.to_string()
            print df_b2n.to_string()

        for variable in [var, varbrut]:
            passed = ((df_b2n[variable] - df_n2b[variable]).abs() < 1).all()

            if (not passed) or verbose:
                print "Brut to net"
                print (df_b2n[[varbrut, var]] / 12).to_string()
                print "Net to brut"
                print (df_n2b / 12).to_string()

            assert passed, "difference in %s " % (var)



if __name__ == '__main__':
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
#    test_case_study(2013, verbose = True)
    test_cho_rst(2013, verbose = False)
