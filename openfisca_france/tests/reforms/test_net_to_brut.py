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
from openfisca_core.tools import assert_near

from openfisca_france.tests import base

from openfisca_france.reforms import inversion_revenus


def check_chonet_to_chobrut(count, chobrut_max, chobrut_min, year):
    scenario_args = dict(
        axes = [
            dict(
                count = count,
                name = 'chobrut',
                max = chobrut_max,
                min = chobrut_min,
                ),
            ],
        period = "{}-01".format(year),
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        )
    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        **scenario_args
        ).new_simulation(debug = True)

    chobrut = simulation.get_holder('chobrut').array
    chonet = simulation.calculate('chonet')

    inversion_reform = inversion_revenus.build_reform(base.tax_benefit_system)
    inverse_simulation = inversion_reform.new_scenario().init_single_entity(
        **scenario_args
        ).new_simulation(debug = True)

    inverse_simulation.get_holder('chobrut').delete_arrays()
    inverse_simulation.get_or_new_holder('chonet').array = chonet
    new_chobrut = inverse_simulation.calculate('chobrut')

    assert_near(new_chobrut, chobrut, absolute_error_margin = 0.1)


def test_chonet_to_chobrut():
    count = 101
    chobrut_max = 5000
    chobrut_min = 2000
    for year in range(2006, 2015):
        yield check_chonet_to_chobrut, count, chobrut_max, chobrut_min, year


def check_rstnet_to_rstbrut(count, rstbrut_max, rstbrut_min, year):
    scenario_args = dict(
        axes = [
            dict(
                count = count,
                name = 'rstbrut',
                max = rstbrut_max,
                min = rstbrut_min,
                ),
            ],
        period = "{}-01".format(year),
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        )

    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        **scenario_args
        ).new_simulation(debug = True)

    rstbrut = simulation.get_holder('rstbrut').array
    rstnet = simulation.calculate('rstnet')

    inversion_reform = inversion_revenus.build_reform(base.tax_benefit_system)
    inverse_simulation = inversion_reform.new_scenario().init_single_entity(
        **scenario_args
        ).new_simulation(debug = True)

    inverse_simulation.get_holder('rstbrut').delete_arrays()
    inverse_simulation.get_or_new_holder('rstnet').array = rstnet
    new_rstbrut = inverse_simulation.calculate('rstbrut')

    assert_near(new_rstbrut, rstbrut, absolute_error_margin = 0.1)


def test_rstnet_to_rstbrut():
    count = 101
    rstbrut_max = 5000
    rstbrut_min = 0
    for year in range(2006, 2015):
        yield check_rstnet_to_rstbrut, count, rstbrut_max, rstbrut_min, year


def check_salaire_net_to_salaire_de_base(count, salaire_de_base_max, salaire_de_base_min, type_sal, year):
    period = periods.period("{}-01".format(year))
    scenario_args = dict(
        axes = [
            dict(
                count = count,
                name = 'salaire_de_base',
                max = salaire_de_base_max,
                min = salaire_de_base_min,
                ),
            ],
        period = period,
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            type_sal = type_sal,
            ),
        )

    simulation = base.tax_benefit_system.new_scenario().init_single_entity(
        **scenario_args
        ).new_simulation()

    salaire_de_base = simulation.get_holder('salaire_de_base').array
    smic_horaire = simulation.legislation_at(period.start).cotsoc.gen.smic_h_b
    smic_mensuel = smic_horaire * 35 * 52 / 12
    brut = simulation.get_holder('salaire_de_base').array
    simulation.get_or_new_holder('contrat_de_travail').array = brut < smic_mensuel  # temps plein ou temps partiel
    simulation.get_or_new_holder('heures_remunerees_volume').array = brut // smic_horaire  # temps plein / partiel

    salaire_net = simulation.calculate('salaire_net')

    inversion_reform = inversion_revenus.build_reform(base.tax_benefit_system)
    inverse_simulation = inversion_reform.new_scenario().init_single_entity(
        **scenario_args
        ).new_simulation()

    inverse_simulation.get_holder('salaire_de_base').delete_arrays()
    inverse_simulation.get_or_new_holder('salaire_net').array = salaire_net
    inverse_simulation.get_or_new_holder('contrat_de_travail').array = brut < smic_mensuel  # temps plein / partiel
    inverse_simulation.get_or_new_holder('heures_remunerees_volume').array = (
        (brut // smic_horaire) * (brut < smic_mensuel)
        )
    new_salaire_de_base = inverse_simulation.calculate('salaire_de_base')
    assert_near(new_salaire_de_base, salaire_de_base, absolute_error_margin = 0.1,
        message = 'Failing test for type_sal={}'.format(type_sal))


def test_salaire_net_to_salaire_de_base():
    count = 101
    salaire_de_base_max = 5000
    salaire_de_base_min = 0
    for year in range(2006, 2015):
        for type_sal in [0, 1]:  # CAT._vars:   TODO: work on other categories of employee
            yield check_salaire_net_to_salaire_de_base, count, salaire_de_base_max, salaire_de_base_min, type_sal, year


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    # TOD0 test_chonet_to_chobrut,
    for test in (test_chonet_to_chobrut, test_rstnet_to_rstbrut, test_salaire_net_to_salaire_de_base):
        for function_and_arguments in test():
            function_and_arguments[0](*function_and_arguments[1:])
