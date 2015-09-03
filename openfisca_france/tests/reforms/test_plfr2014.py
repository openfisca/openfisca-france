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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE,  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program,  If not, see <http://www.gnu.org/licenses/>.


import datetime

from openfisca_core.tools import assert_near

from openfisca_france.tests import base


def test_plfr2014():
    year = 2013
    reform = base.get_cached_reform(
        reform_key = 'plfr2014',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 10,
                max = 13795 * (1 + .1) * (1 + .03),
                min = 13795 * (1 + .1) * (1 - .03),
                name = 'salaire_imposable',
                ),
            ],
        period = year,
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        )

    reference_simulation = scenario.new_simulation(debug = True, reference = True)

    absolute_error_margin = 1

    rfr = reference_simulation.calculate('rfr')
    expected_rfr = [13247, 13338, 13429, 13520, 13611, 13703, 13793, 13884, 13975, 14066]
    assert_near(expected_rfr, rfr, absolute_error_margin = absolute_error_margin)

    impo = reference_simulation.calculate('impo')
    expected_impo = [-249.11, -268.22, -287.33, -306.44, -325.55, -344.87, -363.77, -382.88, -401.99, -421.1]
    assert_near(expected_impo, impo, absolute_error_margin = absolute_error_margin)

    reform_simulation = scenario.new_simulation(debug = True)
    reform_reduction_impot_exceptionnelle = reform_simulation.calculate('reduction_impot_exceptionnelle')
    expected_reform_reduction_impot_exceptionnelle = [350, 350, 350, 350, 350, 350, 350, 261, 170, 79]
    assert_near(expected_reform_reduction_impot_exceptionnelle, reform_reduction_impot_exceptionnelle,
        absolute_error_margin = absolute_error_margin)

    reform_rfr = reform_simulation.calculate('rfr')
    # rfr must be the same than before reform.
    assert_near(expected_rfr, reform_rfr, absolute_error_margin = absolute_error_margin)

    reform_impo = reform_simulation.calculate('impo')
    expected_reform_impo = [0, 0, 0, 0, 0, 0, 0, -121.88, -231.99, -342.1]
    assert_near(expected_reform_impo, reform_impo, absolute_error_margin = absolute_error_margin)


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_plfr2014()
