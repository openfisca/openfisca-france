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


from __future__ import division

import datetime

from ..model.base import CAT
from . import base


tests_infos = [
    dict(
        period = year,
        parent1 = dict(
            birth = datetime.date(1972, 1, 1),
            salaire_de_base = 2000,
            effectif_entreprise = 25,
            type_sal = CAT['prive_non_cadre'],
            ),
        menage = dict(
            zone_apl = 1,
            ),
        ) for year in range(2015, 2002, -1)
    ]


def check_run(simulation, period):
    assert simulation.calculate('revdisp') is not None, "Can't compute revdisp on period {}".format(period)
    assert simulation.calculate('salsuperbrut') is not None, "Can't compute salsuperbrut on period {}".format(period)


def test():
    for scenario_arguments in tests_infos:
        simulation = base.tax_benefit_system.new_scenario().init_single_entity(**scenario_arguments).new_simulation(
            debug = False)
        period = scenario_arguments['period']
        yield check_run, simulation, period


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test()
