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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE,  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program,  If not, see <http://www.gnu.org/licenses/>.


import datetime

from openfisca_core import periods
from openfisca_france.reforms import landais_piketty_saez
from openfisca_france.tests.base import assert_near, tax_benefit_system


def test():
    year = 2013
    reform = landais_piketty_saez.build_reform(tax_benefit_system)
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                max = 30000,
                min = 0,
                name = 'sali',
                ),
            ],
        period = periods.period('year', year),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
#        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
#        enfants = [
#            dict(birth = datetime.date(year - 9, 1, 1)),
#            dict(birth = datetime.date(year - 9, 1, 1)),
#            ],
        )

#    reference_simulation = scenario.new_simulation(debug = True, reference = True)
#
    error_margin = 0.01

    reform_simulation = scenario.new_simulation(debug = True)
    reform_assiette_csg = reform_simulation.calculate('assiette_csg')
    reform_impot_revenu_lps = reform_simulation.calculate('impot_revenu_lps')
    assert ((abs(
        -reform_impot_revenu_lps - ((reform_assiette_csg - 10000) * .25 / 30000 + .25) * reform_assiette_csg
        )) < error_margin).all(), "Error in LPS reform"


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test()
