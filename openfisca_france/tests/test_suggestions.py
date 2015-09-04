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
import json

from nose.tools import assert_equal

from . import base


def test_birth():
    year = 2013
    scenario = base.tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = dict(),
        enfants = [
            dict(),
            dict(birth = datetime.date(year - 12, 1, 1)),
            dict(birth = datetime.date(year - 18, 1, 1)),
            ],
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), encoding = 'utf-8', ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation(debug = True)
    assert_equal(
        simulation.calculate('birth').tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 12, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite').tolist(),
        [
            4,
            2,
            2,
            4,
            ],
        )
    assert_equal(
        simulation.calculate('age').tolist(),
        [
            40,
            10,
            12,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois').tolist(),
        [
            40 * 12,
            10 * 12,
            12 * 12,
            18 * 12,
            ],
        )


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_birth()
