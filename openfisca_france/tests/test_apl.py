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


import datetime

import openfisca_france


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def test_zone_1():
    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        date = datetime.date(year, 1, 1),
        menage = dict(
            code_postal = 75014,
            ),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        ).new_simulation(debug = True)
    assert simulation.calculate('zone_apl') == 1


def test_zone_2():
    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        date = datetime.date(year, 1, 1),
        menage = dict(
            code_postal = 69001,
            ),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        ).new_simulation(debug = True)
    assert simulation.calculate('zone_apl') == 2


def test_zone_3():
    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        date = datetime.date(year, 1, 1),
        menage = dict(
            code_postal = 87620,
            ),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        ).new_simulation(debug = True)
    assert simulation.calculate('zone_apl') == 3


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_zone_1()
    test_zone_2()
    test_zone_3()
