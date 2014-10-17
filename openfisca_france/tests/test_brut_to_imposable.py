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

from pandas import DataFrame

from openfisca_core import periods
from ..model.cotisations_sociales.travail import CAT, TAUX_DE_PRIME
from ..model import inversion_revenus
from . import base


def test_sal(year = 2014, verbose = False):
    # Tests that _salbrut which computes "salaire brut" from "imposable" yields an amount compatible
    # with the one obtained from running openfisca starting with a "salaire brut"

    maxrev = 24000
    period = periods.period('year', year)
    for type_sal_category in ['prive_non_cadre', 'prive_cadre']:  # ,['public_titulaire_etat']
        simulation = base.tax_benefit_system.new_scenario().init_single_entity(
            axes = [dict(name = 'salbrut', max = maxrev, min = 0, count = 11)],
            period = period,
            parent1 = dict(
                birth = datetime.date(year - 40, 1, 1),
                type_sal = CAT[type_sal_category],
                ),
            ).new_simulation(debug = True)

        # Brut to imposable
        if type_sal_category == 'public_titulaire_etat':
            primes_values = TAUX_DE_PRIME * simulation.get_holder('salbrut').array

            primes_holder = simulation.get_or_new_holder('primes')
            primes_holder.array = primes_values

        df_b2i = DataFrame(dict(sal = simulation.calculate('sal'),
                                salbrut = simulation.calculate('salbrut'),
                                ))

        # Imposable to brut
        sali = df_b2i['sal'].get_values()

        hsup = simulation.calculate('hsup')
        type_sal = simulation.calculate('type_sal')
        # primes = simulation.calculate('primes')

        defaultP = simulation.get_reference_compact_legislation(periods.start_instant(period))
        df_i2b = DataFrame({
            'sal': sali,
            'salbrut': inversion_revenus._salbrut_from_sali(sali, hsup, type_sal, defaultP),
            })

        for var in ['sal', 'salbrut']:
            passed = ((df_b2i[var] - df_i2b[var]).abs() < .01).all()

        if (not passed) or type_sal_category in ['public_titulaire_etat'] or verbose:
            print "Brut to imposable"
            print (df_b2i[['salbrut', 'sal']] / 12).to_string()
            print "Imposable to brut"
            print (df_i2b / 12).to_string()

            assert passed, "difference in %s for %s" % (var, type_sal_category)


def test_cho_rst(year = 2014, verbose = False):
    # Tests that _chobrut which computes "chômage brut" from "imposable" yields an amount compatbe
    # with the one obtained from running openfisca satrting with a "chômage brut"

    period = periods.period('year', year)
    remplacement = {'cho': 'chobrut', 'rst': 'rstbrut'}

    for var, varbrut in remplacement.iteritems():
        maxrev = 24000

        simulation = base.tax_benefit_system.new_scenario().init_single_entity(
            axes = [dict(name = varbrut, max = maxrev, min = 0, count = 11)],
            period = period,
            parent1 = dict(
                birth = datetime.date(year - 40, 1, 1),
                ),
            ).new_simulation(debug = True)

        df_b2i = DataFrame({
            var: simulation.calculate(var),
            varbrut: simulation.calculate(varbrut),
            })

        vari = df_b2i[var].get_values()
        csg_rempl = vari * 0 + 3

        defaultP = simulation.get_reference_compact_legislation(period)
        if var == "cho":
            _vari_to_brut = inversion_revenus._chobrut_from_choi
        elif var == "rst":
            _vari_to_brut = inversion_revenus._rstbrut_from_rsti
        else:
            assert False, u'Unsupported value for var: {!r}'.format(var)

        df_i2b = DataFrame({var: vari, varbrut: _vari_to_brut(vari, csg_rempl, defaultP)})

        if verbose:
            print df_i2b.to_string()
            print df_b2i.to_string()

        for variable in [var, varbrut]:
            passed = ((df_b2i[variable] - df_i2b[variable]).abs() < 1).all()

            if (not passed) or verbose:
                print "Brut to imposable"
                print (df_b2i[[varbrut, var]] / 12).to_string()
                print "Imposable to brut"
                print (df_i2b / 12).to_string()

                assert passed, "difference in %s " % (var)


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_sal(2013, verbose = False)
    test_cho_rst(2014, verbose = True)
