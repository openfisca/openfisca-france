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

from nose.tools import assert_less

from openfisca_core import periods
from openfisca_france.tests import base


def test(year = 2014):
    max_sal = 20000
    count = 2
    people = 1
    reform = base.get_cached_reform(
        reform_key = 'plf2015',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = count,
                max = max_sal,
                min = 0,
                name = 'salaire_imposable',
                ),
            ],
        period = periods.period('year', year),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)) if people >= 2 else None,
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 3 else None,
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 4 else None,
            ] if people >= 3 else None,
        )

    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)

    error_margin = 0.1
    impo = reference_simulation.calculate('impo')
    reform_impo = reform_simulation.calculate('impo')
    print impo
    print reform_impo
    boum
    assert_less(max(abs(impo - reform_impo)), error_margin)


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test()
