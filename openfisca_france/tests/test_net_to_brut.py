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


import numpy as np

import openfisca_france
from openfisca_france import surveys
from openfisca_france.model.cotisations_sociales.travail import CAT, TAUX_DE_PRIME


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def check_chonet_to_chobrut(count, chobrut_max, chobrut_min, year):
    simulation = surveys.new_simulation_from_array_dict(
        array_dict = dict(
            age = np.array(40).repeat(count),
            chobrut = np.linspace(chobrut_min, chobrut_max, count),
            ),
        debug = True,
        tax_benefit_system = tax_benefit_system,
        year = year,
        )
    chobrut_holder = simulation.get_holder('chobrut')
    chobrut = chobrut_holder.array
    chonet = simulation.calculate('chonet')
    # Now that net has been computed, remove brut and recompute it from net.
    del chobrut_holder.array
    new_chobrut = simulation.calculate('chobrut')
    assert abs(new_chobrut - chobrut).all() < 0.1, str((chobrut, new_chobrut))


def test_chonet_to_chobrut():
    count = 11
    chobrut_max = 24000
    chobrut_min = 0
    for year in range(2006, 2015):
        yield check_chonet_to_chobrut, count, chobrut_max, chobrut_min, year


def check_rstnet_to_rstbrut(count, rstbrut_max, rstbrut_min, year):
    simulation = surveys.new_simulation_from_array_dict(
        array_dict = dict(
            age = np.array(40).repeat(count),
            rstbrut = np.linspace(rstbrut_min, rstbrut_max, count),
            ),
        debug = True,
        tax_benefit_system = tax_benefit_system,
        year = year,
        )
    rstbrut_holder = simulation.get_holder('rstbrut')
    rstbrut = rstbrut_holder.array
    rstnet = simulation.calculate('rstnet')
    # Now that net has been computed, remove brut and recompute it from net.
    del rstbrut_holder.array
    new_rstbrut = simulation.calculate('rstbrut')
    assert abs(new_rstbrut - rstbrut).all() < 0.1, str((rstbrut, new_rstbrut))


def test_rstnet_to_rstbrut():
    count = 11
    rstbrut_max = 24000
    rstbrut_min = 0
    for year in range(2006, 2015):
        yield check_rstnet_to_rstbrut, count, rstbrut_max, rstbrut_min, year


def check_salnet_to_salbrut(count, salbrut_max, salbrut_min, type_sal, year):
    simulation = surveys.new_simulation_from_array_dict(
        array_dict = dict(
            age = np.array(40).repeat(count),
            primes = TAUX_DE_PRIME * np.linspace(salbrut_min, salbrut_max, count) * (type_sal >= 2),
            salbrut = np.linspace(salbrut_min, salbrut_max, count),
            type_sal = np.array(type_sal).repeat(count),
            ),
        debug = True,
        tax_benefit_system = tax_benefit_system,
        year = year,
        )
    salbrut_holder = simulation.get_holder('salbrut')
    salbrut = salbrut_holder.array
    salnet = simulation.calculate('salnet')
    # Now that net has been computed, remove brut and recompute it from net.
    del salbrut_holder.array
    new_salbrut = simulation.calculate('salbrut')
    assert abs(new_salbrut - salbrut).all() < 0.1, str((salbrut, new_salbrut))


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
