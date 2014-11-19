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

from ..model.base import CAT
from . import base


def check_chonet_to_chobrut(count, chobrut_max, chobrut_min, year):
    base_simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = count,
                name = 'chobrut',
                max = chobrut_max,
                min = chobrut_min,
                ),
            ],
        period = year,
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        ).new_simulation(debug = True)

    simulation = base_simulation.clone(debug = False)
    chobrut = simulation.get_holder('chobrut').array
    chonet = simulation.calculate('chonet')

    simulation = base_simulation.clone(debug = True)
    chobrut_holder = simulation.get_holder('chobrut')
    chobrut_holder.delete_arrays()
    simulation.get_or_new_holder('chonet').array = chonet
    new_chobrut = simulation.calculate('chobrut')

    assert (abs(new_chobrut - chobrut) < 0.1).all(), str((chobrut, new_chobrut))


def test_chonet_to_chobrut():
    count = 11
    chobrut_max = 50000
    chobrut_min = 0
    for year in range(2006, 2015):
        yield check_chonet_to_chobrut, count, chobrut_max, chobrut_min, year


def check_rstnet_to_rstbrut(count, rstbrut_max, rstbrut_min, year):
    base_simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = count,
                name = 'rstbrut',
                max = rstbrut_max,
                min = rstbrut_min,
                ),
            ],
        period = year,
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        ).new_simulation(debug = True)

    simulation = base_simulation.clone(debug = False)
    rstbrut = simulation.get_holder('rstbrut').array
    rstnet = simulation.calculate('rstnet')

    simulation = base_simulation.clone(debug = True)
    rstbrut_holder = simulation.get_holder('rstbrut')
    rstbrut_holder.delete_arrays()
    simulation.get_or_new_holder('rstnet').array = rstnet
    new_rstbrut = simulation.calculate('rstbrut')

    assert (abs(new_rstbrut - rstbrut) < 0.1).all(), str((rstbrut, new_rstbrut))


def test_rstnet_to_rstbrut():
    count = 11
    rstbrut_max = 24000
    rstbrut_min = 0
    for year in range(2006, 2015):
        yield check_rstnet_to_rstbrut, count, rstbrut_max, rstbrut_min, year


def check_salnet_to_salbrut(count, salbrut_max, salbrut_min, type_sal, year):
    base_simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = count,
                name = 'salbrut',
                max = salbrut_max,
                min = salbrut_min,
                ),
            ],
        period = year,
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            type_sal = type_sal,
            ),
        ).new_simulation(debug = True)

    simulation = base_simulation.clone(debug = False)
    salbrut = simulation.get_holder('salbrut').array
    salnet = simulation.calculate('salnet')

    simulation = base_simulation.clone(debug = True)
    salbrut_holder = simulation.get_holder('salbrut')
    salbrut_holder.delete_arrays()
    simulation.get_or_new_holder('salnet').array = salnet
    new_salbrut = simulation.calculate('salbrut')

    assert (abs(new_salbrut - salbrut) < 0.1).all(), str((salbrut, new_salbrut))


def test_salnet_to_salbrut():
    count = 11
    salbrut_max = 48000
    salbrut_min = 0
    for year in range(2006, 2015):
        for type_sal in CAT._vars:
            yield check_salnet_to_salbrut, count, salbrut_max, salbrut_min, type_sal, year


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    for test in (test_chonet_to_chobrut, test_rstnet_to_rstbrut, test_salnet_to_salbrut):
        for function_and_arguments in test():
            function_and_arguments[0](*function_and_arguments[1:])
