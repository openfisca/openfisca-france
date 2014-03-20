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

import numpy as np
import datetime
from pandas import DataFrame

import openfisca_france
from openfisca_france.model.cotisations_sociales.travail import CAT, TAUX_DE_PRIME
from openfisca_france import surveys

TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def test_case_study(year = 2013, verbose = False):
    '''
    Tests that _salbrut which computes "salaire brut" from "imposable" yields an amount compatible
    with the one obtained from running openfisca satrting with a "salaire brut"
    '''
    for type_sal_num, type_sal_category in CAT._vars.iteritems():
        max_rev = 48000
        min_rev = 0
        count = 11
        parent1 = dict(
            age = np.array(40).repeat(count),
            type_sal = np.array(type_sal_num).repeat(count)
            )
        parent1.update(
            dict(
                salbrut = np.linspace(min_rev, max_rev, count),
                primes = TAUX_DE_PRIME * np.linspace(min_rev, max_rev, count) * (type_sal_num >= 2),
                )
            )
        simulation = surveys.new_simulation_from_array_dict(
            array_dict = parent1,
            tax_benefit_system = tax_benefit_system,
            year = year,
            )

#         simulation = tax_benefit_system.new_scenario().init_single_entity(
#             axes = [
#                 dict(name = 'salbrut', max = maxrev, min = 0, count = 11),
#                 dict(name = 'salbrut', max = maxrev, min = 0, count = 11) ],
#             parent1 = dict(
#                 birth = datetime.date(year - 40, 1, 1),
# #                salbrut = maxrev,
# #                primes = TAUX_DE_PRIME * maxrev if type_sal_category == 'public_titulaire_etat' else None,
#                 type_sal = CAT[type_sal_category],
#                 ),
#             year = year,
#            ).new_simulation(debug = True)

        df_b2n = DataFrame(dict(salnet = simulation.calculate('salnet'),
                                salbrut = simulation.calculate('salbrut'),
                                primes = simulation.calculate('primes')
                                ))
#        from openfisca_france.model.inversion_revenus import _salbrut_from_salnet
        from openfisca_france.model.inversion_revenus import _num_salbrut_from_salnet, _primes_from_salbrut
        saln = df_b2n['salnet'].get_values()
        hsup = simulation.calculate('hsup')
        type_sal = simulation.calculate('type_sal')
        primes = simulation.calculate('primes')
        defaultP = simulation.default_compact_legislation
        df_n2b = DataFrame(
            {
                'salnet': saln,
#                'salbrut' : _salbrut_from_salnet(saln, hsup, type_sal, defaultP),
                'salbrut' : _num_salbrut_from_salnet(saln, hsup, type_sal, defaultP),
            }
        )
        df_n2b['primes'] = _primes_from_salbrut(df_n2b['salbrut'], type_sal)

        for var in ['salnet', 'salbrut']:
            passed = ((df_b2n[var] - df_n2b[var]).abs() < .01).all()

            if (not passed) or verbose:
                print "Brut to net"
                print (df_b2n[['salbrut', 'salnet', 'primes' ]] / 12).to_string()
                print "Net to brut"
                print (df_n2b / 12).to_string()
                assert passed, "difference in %s for %s" % (var, type_sal_category)


def test_cho_rst(year = 2013, verbose = False):
    '''
    Tests that _chobrut which computes "chômage brut" from "net" yields an amount compatible
    with the one obtained from running openfisca starting with a "chômage brut"
    '''
    remplacement = {'chonet' : 'chobrut', 'rstnet': 'rstbrut'}

    for var, varbrut in remplacement.iteritems():

        maxrev = 24000

        simulation = tax_benefit_system.new_scenario().init_single_entity(
            axes = [ dict(name = varbrut, max = maxrev, min = 0, count = 11) ],
            parent1 = {
                'birth' : datetime.date(year - 40, 1, 1),
                varbrut : maxrev,
                },
            year = year,
            ).new_simulation(debug = True)

        df_b2n = DataFrame({var: simulation.calculate(var),
                            varbrut : simulation.calculate(varbrut),
                            })

        varn = df_b2n[var].get_values()
        csg_rempl = simulation.calculate('csg_rempl')
        defaultP = simulation.default_compact_legislation
        if var == "chonet":
            from openfisca_france.model.inversion_revenus import _chobrut_from_chonet as _varn_to_brut
            from openfisca_france.model.inversion_revenus import _num_chobrut_from_chonet as _num_varn_to_brut
        elif var == "rstnet":
            from openfisca_france.model.inversion_revenus import _rstbrut_from_rstnet as _varn_to_brut
            from openfisca_france.model.inversion_revenus import _num_rstbrut_from_rstnet as _num_varn_to_brut

        num_varbrut = varbrut + "_num"
        df_n2b = DataFrame({var: varn, varbrut : _varn_to_brut(varn, csg_rempl, defaultP), num_varbrut: _num_varn_to_brut(varn, csg_rempl, defaultP)})

        if verbose:
            print df_n2b.to_string()
            print df_b2n.to_string()

        for variable in [var, varbrut]:
            passed = ((df_b2n[variable] - df_n2b[variable]).abs() < 1).all()

            if passed:
                passed = ((df_b2n[varbrut] - df_n2b[num_varbrut]).abs() < 1).all()

            if (not passed) or verbose:
                print "Brut to imposable"
                print (df_b2n[[varbrut, var ]] / 12).to_string()
                print "Imposable to brut"
                print (df_n2b / 12).to_string()

            assert passed, "difference in %s " % (var)



if __name__ == '__main__':
    import sys
    import logging
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
#    import nose
#    nose.core.runmodule(argv = [__file__, '-v'])
#    test_case_study(2013, verbose = True)
    test_cho_rst(2013, verbose = True)
