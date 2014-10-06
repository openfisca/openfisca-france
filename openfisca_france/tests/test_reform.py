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


import copy
import datetime

from openfisca_core import legislations, periods
from openfisca_core.reforms import Reform
import openfisca_france


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def test_parametric_reform(year = 2014):
    dated_legislation_json_src = legislations.generate_dated_legislation_json(
        tax_benefit_system.legislation_json,
        periods.period('year', year),
        )
#    print unicode(json.dumps(dated_legislation_json_src, ensure_ascii = False, indent = 2))

    reform_dated_legislation_json = copy.deepcopy(dated_legislation_json_src)
    assert reform_dated_legislation_json['children']['ir']['children']['bareme']['slices'][0]['rate'] == 0
    reform_dated_legislation_json['children']['ir']['children']['bareme']['slices'][0]['rate'] = 1

    reform = Reform(
        name = "IR_100_tranche_1",
        label = u"Imposition à 100% dès le premier euro et jusqu'à la fin de la 1ère tranche",
        reform_dated_legislation_json = reform_dated_legislation_json,
        reference_dated_legislation_json = dated_legislation_json_src
        )

    scenario = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'sali',
                max = 100000,
                min = 0,
                ),
            ],
        date = datetime.date(year, 1, 1),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        )

    simulation = scenario.new_simulation(debug = True)
    assert max(abs(simulation.calculate('impo') - [0, -7889.20019531, -23435.52929688])) < .01

    scenario.add_reform(reform)
    reform_simulation = scenario.new_reform_simulation(debug = True)
    assert reform_simulation.compact_legislation is not None
    assert max(abs(reform_simulation.calculate('impo') - [0., -13900.20019531, -29446.52929688])) < .0001


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_parametric_reform(2014)
