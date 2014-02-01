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

import sys

import logging

import openfisca_france
openfisca_france.init_country(start_from = "brut")

from openfisca_core.simulations import ScenarioSimulation

from openfisca_france.model.cotisations_sociales.travail import CAT

def test_case_study(year = 2013, verbose = False):
    for type_sal_category in ['prive_non_cadre', 'prive_cadre']:

        simulation = ScenarioSimulation()
        simulation.set_config(year = year, reforme = False, nmen = 5, maxrev = 20000, x_axis = 'salbrut')
        # Add husband/wife on the same tax sheet (foyer).
    #    simulation.scenario.addIndiv(1, datetime.date(1975, 1, 1), 'conj', 'part')
        simulation.scenario.indiv[0]['type_sal'] = CAT[type_sal_category]
        simulation.set_param()

        # The aefa prestation can be disabled by uncommenting the following line:
        # simulation.disable_prestations( ['aefa'])
        df = simulation.get_results_dataframe(index_by_code = True)


        from openfisca_france.model.cotisations_sociales.travail import _salbrut
        df_b2i = df.transpose()
        if verbose:

            print df_b2i.to_string()

        sali = df_b2i['sal'].get_values()
        hsup = simulation.input_table.table['hsup'].get_values()
        type_sal = simulation.input_table.table['type_sal'].get_values()

        defaultP = simulation.P_default
        from pandas import DataFrame
        df_i2b = DataFrame({'sal': sali, 'salbrut' : _salbrut(sali, hsup, type_sal, defaultP)})

        if verbose:
            print df_i2b.to_string()


        for var in ['sal', 'salbrut']:
            test = ((df_b2i[var] - df_i2b[var]).abs() < .01).all()

            if not test:
                print df_b2i.to_string()
                print df_i2b.to_string()

            assert test, "difference in %s for " % (var, type_sal_category)


if __name__ == '__main__':
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_case_study(2013, verbose = False)
