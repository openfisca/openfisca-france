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


import datetime

from openfisca_core import periods
from openfisca_france.tests.base import tax_benefit_system


tests = [
    dict(
        # test sur un revenu des actions soumises à un prélèvement libératoire de
        # 21 % (2DA)
        name = "f2da_2012",
        period = "2012",
        input_variables = dict(
            f2da = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_lib = - (4.5 + 2 + 0.3) * 0.01 * 20000,
            csg_cap_lib = - .082 * 20000,
            crds_cap_lib = - .005 * 20000,
            ),
        ),
    dict(
        name = "f2da_2011",
        period = "2011",
        input_variables = dict(
            f2da = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_lib = - (3.4 + 1.1 + 0.3) * 0.01 * 20000,
            csg_cap_lib = - .082 * 20000,
            crds_cap_lib = - .005 * 20000,
            ),
        ),
    dict(
        name = "f2da_2010",
        period = "2010",
        input_variables = dict(
            f2da = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_lib = - (2.2 + 1.1 + 0.3) * 0.01 * 20000,
            csg_cap_lib = - .082 * 20000,
            crds_cap_lib = - .005 * 20000,
            ),
        ),
    # Célibataire sans enfant
    # test sur un revenu des actions et  parts (2DC)
    dict(
        name = "f2dc_2013",
        period = "2013",
        input_variables = dict(
            f2dc = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_bar = - 1360,
            csg_cap_bar = - 1640,
            crds_cap_bar = - 100,
            ir_plaf_qf = 330,
            irpp = - 0,
            ),
        ),
    dict(
        name = "f2dc_2012",
        period = "2012",
        input_variables = dict(
            f2dc = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_bar = - (4.5 + 2 + 0.3) * 0.01 * 20000,
            csg_cap_bar = - .082 * 20000,
            crds_cap_bar = - .005 * 20000,
            ),
        ),
    dict(
        name = "f2dc_2011",
        period = "2011",
        input_variables = dict(
            f2dc = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_bar = - (3.4 + 1.1 + 0.3) * 0.01 * 20000,
            csg_cap_bar = - .082 * 20000,
            crds_cap_bar = - .005 * 20000,
            ),
        ),
    dict(
        name = "f2dc_2010",
        period = "2010",
        input_variables = dict(
            f2dc = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_bar = - (2.2 + 1.1 + 0.3) * 0.01 * 20000,
            csg_cap_bar = - .082 * 20000,
            crds_cap_bar = - .005 * 20000,
            )
        ),
    # test sur le Revenus imposables des titres non côtés détenus dans le PEA et distributions perçues via
    # votre entreprise donnant droit à abattement (2fu)
    dict(
        name = "f2fu_2013",
        period = "2013",
        input_variables = dict(
            f2fu = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_bar = - 1360,
            csg_cap_bar = - 1640,
            crds_cap_bar = - 100,
            ir_plaf_qf = 330,
            irpp = 0,
            ),
        ),
    # Autres revenus distribués et revenus des structures soumises hors de
    # France à un régime fiscal privilégié (2Go)
    dict(
        name = "f2go_2013",
        period = "2013",
        input_variables = dict(
            f2go = 20000,
            ),
        output_variables = dict(
            rev_cat_rvcm = 25000,
            prelsoc_cap_bar = - 1700,
            csg_cap_bar = - 2050,
            crds_cap_bar = - 125,
            ir_plaf_qf = 2150,
            irpp = - 2150,
            ),
        ),
    dict(
        name = "f2ts_2013",
        period = "2013",
        input_variables = dict(
            f2ts = 20000,
            ),
        output_variables = dict(
            rev_cat_rvcm = 20000,
            prelsoc_cap_bar = - 1360,
            csg_cap_bar = - 1640,
            crds_cap_bar = - 100,
            ir_plaf_qf = 1450,
            irpp = - 1450,
            ),
        ),
    dict(
        name = "f2ts_2012",
        period = "2012",
        input_variables = dict(
            f2ts = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_bar = - (4.5 + 2 + 0.3) * 0.01 * 20000,
            csg_cap_bar = - .082 * 20000,
            crds_cap_bar = - .005 * 20000,
            ),
        ),
    dict(
        name = "f2ts_2011",
        period = "2011",
        input_variables = dict(
            f2ts = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_bar = - (3.4 + 1.1 + 0.3) * 0.01 * 20000,
            csg_cap_bar = - .082 * 20000,
            crds_cap_bar = - .005 * 20000,
            ),
        ),
    dict(
        name = "f2ts_2010",
        period = "2010",
        input_variables = dict(
            f2ts = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_bar = - (2.2 + 1.1 + 0.3) * 0.01 * 20000,
            csg_cap_bar = - .082 * 20000,
            crds_cap_bar = - .005 * 20000,
            ),
        ),
    # test sur les intérêts (2TR)
    dict(
        name = "f2ts_2013",
        period = "2013",
        input_variables = dict(
            f2ts = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_bar = - 1360,
            csg_cap_bar = - 1640,
            crds_cap_bar = - 100,
            ir_plaf_qf = 1450,
            irpp = - 1450,
            ),
        ),
    dict(
        name = "f2ts_2012",
        period = "2012",
        input_variables = dict(
            f2ts = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_bar = - (4.5 + 2 + 0.3) * 0.01 * 20000,
            csg_cap_bar = - .082 * 20000,
            crds_cap_bar = - .005 * 20000,
            ),
        ),
    dict(
        name = "f2ts_2011",
        period = "2011",
        input_variables = dict(
            f2ts = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_bar = - (3.4 + 1.1 + 0.3) * 0.01 * 20000,
            csg_cap_bar = - .082 * 20000,
            crds_cap_bar = - .005 * 20000,
            ),
        ),
    dict(
        name = "f2ts_2010",
        period = "2010",
        input_variables = dict(
            f2ts = 20000,
            ),
        output_variables = dict(
            prelsoc_cap_bar = - (2.2 + 1.1 + 0.3) * 0.01 * 20000,
            csg_cap_bar = - .082 * 20000,
            crds_cap_bar = - .005 * 20000,
            ),
        ),
    # test sur les revenus fonciers (4BA)
    dict(
        name = "f4ba_2013",
        period = "2013",
        input_variables = dict(
            f4ba = 20000,
            ),
        output_variables = dict(
            prelsoc_fon = - 1360,
            csg_fon = - 1640,
            crds_fon = - 100,
            ir_plaf_qf = 1450,
            irpp = - 1450,
            ),
        ),
    dict(
        name = "f4ba_2012",
        period = "2012",
        input_variables = dict(
            f4ba = 20000,
            ),
        output_variables = dict(
            prelsoc_fon = - (4.5 + 2 + 0.3) * 0.01 * 20000,
            csg_fon = - .082 * 20000,
            crds_fon = - .005 * 20000,
            irpp = - 1461,
            ),
        ),
    dict(
        name = "f4ba_2011",
        period = "2011",
        input_variables = dict(
            f4ba = 20000,
            ),
        output_variables = dict(
            prelsoc_fon = - (3.4 + 1.1 + 0.3) * 0.01 * 20000,
            csg_fon = - .082 * 20000,
            crds_fon = - .005 * 20000,
            ),
        ),
    dict(
        name = "f4ba_2010",
        period = "2010",
        input_variables = dict(
            f4ba = 20000,
            ),
        output_variables = dict(
            prelsoc_fon = - (2.2 + 1.1 + 0.3) * 0.01 * 20000,
            csg_fon = - .082 * 20000,
            crds_fon = - .005 * 20000,
            ),
        ),
    # test (3VG) Plus-values de cession de valeurs mobilières, droits
    # sociaux et gains assimilés
    dict(
        name = "f3vg _2013",
        period = "2013",
        input_variables = dict(
            f3vg = 20000,
            ),
        output_variables = dict(
            prelsoc_pv_mo = - 1360,
            csg_pv_mo = - 1640,
            crds_pv_mo = - 100,
            ir_plaf_qf = 1450,
            irpp = - 1450,
            ),
        ),
    dict(
        name = "f3vg _2012",
        period = "2012",
        input_variables = dict(
            f3vg = 20000,
            ),
        output_variables = dict(
            prelsoc_pv_mo = - (4.5 + 2 + 0.3) * 0.01 * 20000,
            csg_pv_mo = - .082 * 20000,
            crds_pv_mo = - .005 * 20000,
            ),
        ),
    dict(
        name = "f3vg _2011",
        period = "2011",
        input_variables = dict(
            f3vg = 20000,
            ),
        output_variables = dict(
            prelsoc_pv_mo = - (3.4 + 1.1 + 0.3) * 0.01 * 20000,
            csg_pv_mo = - .082 * 20000,
            crds_pv_mo = - .005 * 20000,
            ),
        ),
    dict(
        name = "f3vg _2010",
        period = "2010",
        input_variables = dict(
            f3vg = 20000,
            ),
        output_variables = dict(
            prelsoc_pv_mo = - (2.2 + 1.1 + 0.3) * 0.01 * 20000,
            csg_pv_mo = - .082 * 20000,
            crds_pv_mo = - .005 * 20000,
            ),
        ),
    dict(
        name = "f3vg _2006",
        period = "2006",
        input_variables = dict(
            f3vg = 20000,
            ),
        output_variables = dict(
            prelsoc_pv_mo = - 460,
            csg_pv_mo = - 1640,
            crds_pv_mo = - 100,
            ),
        ),
    # test sur les plus-values immobilières (3VZ)
    dict(
        name = "f3vz_2012",
        period = "2012",
        input_variables = dict(
            f3vz = 20000,
            ),
        output_variables = dict(
            prelsoc_pv_immo = - (4.5 + 2 + 0.3) * 0.01 * 20000,
            csg_pv_immo = - .082 * 20000,
            crds_pv_immo = - .005 * 20000,
            ),
        ),
    dict(
        name = "f3vz_2011",
        period = "2011",
        input_variables = dict(
            f3vz = 20000,
            ),
        output_variables = dict(
            prelsoc_pv_immo = - (3.4 + 1.1 + 0.3) * 0.01 * 20000,
            csg_pv_immo = - .082 * 20000,
            crds_pv_immo = - .005 * 20000,
            ),
        ),
    dict(
        name = "f3vz_2010",
        period = "2010",
        input_variables = dict(
            f3vz = 20000,
            ),
        output_variables = dict(
            prelsoc_pv_immo = - (2.2 + 1.1 + 0.3) * 0.01 * 20000,
            csg_pv_immo = - .082 * 20000,
            crds_pv_immo = - .005 * 20000,
            ),
        ),
    dict(
        name = "f2dc_f2ca_2013",
        period = "2013",
        input_variables = dict(
            f2dc = 20000,
            f2ca = 5000,
            ),
        output_variables = dict(
            csg_cap_bar = - 1640,
            crds_cap_bar = - 100,
            prelsoc_cap_bar = - 1360,
            rev_cat_rvcm = 7000,
            irpp = 0,
            ),
        ),
    # Revenus fonciers
    dict(
        name = "f4ba_2013",
        period = "2013",
        input_variables = dict(
            f4ba = 20000,
            ),
        output_variables = dict(
            csg_fon = - 1640,
            crds_fon = - 100,
            prelsoc_fon = - 1360,
            ir_plaf_qf = 1450,
            rev_cat_rfon = 20000,
            irpp = - 1450,
            ),
        ),
    dict(
        name = "f4babcd_2013",
        period = 2013,
        input_variables = dict(
            f4ba = 20000,
            f4bb = 1000,
            f4bc = 1000,
            f4bd = 1000,
            ),
        output_variables = dict(
            csg_fon = - 1394,
            crds_fon = - 85,
            prelsoc_fon = - 1156,
            ir_plaf_qf = 1030,
            rev_cat_rfon = 17000,
            irpp = - 1030,
            ),
        ),
    dict(
        name = "f4babcd_2013",
        period = 2006,
        input_variables = dict(
            f4ba = 20000,
            f4bb = 1000,
            f4bc = 1000,
            f4bd = 1000,
            ),
        output_variables = dict(
            csg_fon = - 1394,
            crds_fon = - 85,
            prelsoc_fon = - 391,
            rev_cat_rfon = 17000,
            irpp = - 1119,
            ),
        ),
    dict(
        name = "f4be_2013",
        period = 2013,
        input_variables = dict(
            f4be = 10000,
            ),
        output_variables = dict(
            csg_fon = - 574,
            crds_fon = - 35,
            prelsoc_fon = - 476,
            rev_cat_rfon = 7000,
            irpp = 0,
            ),
        ),
    ]


def assert_variable(variable, name, monthly_amount, output):
    assert abs(output - monthly_amount) < 1, \
        "error for {} ({}) : should be {} instead of {} ".format(variable, name, monthly_amount, output)


def test_check():
    for test_parameters in tests:
        name = test_parameters["name"]
        period = test_parameters["period"]
        parent1 = dict(
            birth = datetime.date(periods.period(period).start.year - 40, 1, 1),
            )
        foyer_fiscal = dict()
        foyer_fiscal.update(test_parameters['input_variables'])
        simulation = tax_benefit_system.new_scenario().init_single_entity(
            period = period,
            parent1 = parent1,
            foyer_fiscal = foyer_fiscal,
            ).new_simulation(debug = True)

        for variable, monthly_amount in test_parameters['output_variables'].iteritems():
            output = simulation.calculate_add(variable)
            yield assert_variable, variable, name, monthly_amount, output


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)

    import nose
    nose.core.runmodule(argv = [__file__, '-v', 'test_cotsoc_sal_cap.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)
