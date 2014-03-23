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


def test_age_from_agem():
    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(agem = 40 * 12 + 6),
        year = year,
        ).new_simulation(debug = True)
    assert simulation.calculate('age') == 40


def test_age_from_birth():
    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        year = year,
        ).new_simulation(debug = True)
    assert simulation.calculate('age') == 40
    assert simulation.calculate('agem') == 40 * 12


def test_agem_from_age():
    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(age = 40),
        year = year,
        ).new_simulation(debug = True)
    assert simulation.calculate('agem') == 40 * 12


def test_agem_from_birth():
    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        year = year,
        ).new_simulation(debug = True)
    assert simulation.calculate('agem') == 40 * 12
    assert simulation.calculate('age') == 40


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_age_from_agem()
    test_age_from_birth()
    test_agem_from_age()
    test_agem_from_birth()
