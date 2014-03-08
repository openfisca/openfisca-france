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


def check_af2(year):
    '''
    test avec 2 enfants
    de moins de 11 ans
    montant AF annuel brut de CRDS
    '''
    expected_af_by_year = {2006: 1412.64, 2007: 1436.64, 2008: 1451.04, 2009: 1494.48}

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)),
            dict(birth = datetime.date(year - 9, 1, 1)),
            ],
        year = year,
        ).new_simulation(debug = True)
    af_array = simulation.calculate('af')
    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
        expected_af_by_year[year])


def test_af2():
    for year in range(2006, 2010):
        yield check_af2, year


def check_af2b(year):
    ''' test avec 2 enfants
    un de 14 ans en 2006 et un de 16 ans en 2006
    pas de majo pour le premier, majo 11 ans pour le second
    montant AF annuel brut de CRDS
    '''
    expected_af_by_year = {2006: 1809.96, 2007: 1840.68, 2008: 2176.56, 2009: 2241.72}

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(1992, 1, 1)),
            dict(birth = datetime.date(1990, 1, 1)),
            ],
        year = year,
        ).new_simulation(debug = True)
    af_array = simulation.calculate('af')
    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
        expected_af_by_year[year])


def test_af2b():
    for year in range(2006, 2010):
        yield check_af2b, year


def check_af2c(year):
    '''
    test avec 2 enfants
    un de 15 ans en 2006 et un de 18 ans en 2006
    pas de majo pour le premier, majo 11 ans pour le second
    montant AF annuel brut de CRDS
    '''
    expected_af_by_year = {2006: 1809.96, 2007 : 2154.96, 2008: 0.0, 2009: 0.0}

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(1991, 1, 1)),
            dict(birth = datetime.date(1988, 1, 1)),
            ],
        year = year,
        ).new_simulation(debug = True)
    af_array = simulation.calculate('af')
    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
        expected_af_by_year[year])


def test_af2c():
    for year in range(2006, 2010):
        yield check_af2c, year


def check_af2m(year):
    '''
    test avec 2 enfants
    de plus de 16 ans et donc la majo pour âge pour le second
    montant AF annuel brut de CRDS
    '''
    expected_af_by_year = {2006: 2118.96, 2007: 2154.96, 2008: 2176.56, 2009: 2241.72}

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(1990, 1, 1)),
            dict(birth = datetime.date(1990, 1, 1)),
            ],
        year = year,
        ).new_simulation(debug = True)
    af_array = simulation.calculate('af')
    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
        expected_af_by_year[year])


def test_af2m():
    for year in range(2006, 2010):
        yield check_af2m, year


def check_af3(year):
    '''
    test avec 3 enfants
    de moins de 11 ans
    montant AF annuel brut de CRDS
    '''
    expected_af_by_year = {2006: 3222.60, 2007: 3277.32, 2008: 3310.08, 2009: 3409.32}

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(2003, 1, 1)),
            dict(birth = datetime.date(2004, 1, 1)),
            dict(birth = datetime.date(2005, 1, 1)),
            ],
        year = year,
        ).new_simulation(debug = True)
    af_array = simulation.calculate('af')
    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
        expected_af_by_year[year])


def test_af3():
    for year in range(2006, 2010):
        yield check_af3, year


def check_af3m(year):
    '''
    test avec 3 enfants
    de plus de 14 ans et donc avec 3 majo pour âge
    montant AF annuel brut de CRDS
    '''
    expected_af_by_year = {2006: 5341.56, 2007: 5432.28, 2008: 5486.64, 2009: 5651.04}

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(1990, 1, 1)),
            dict(birth = datetime.date(1990, 1, 1)),
            dict(birth = datetime.date(1990, 1, 1)),
            ],
        year = year,
        ).new_simulation(debug = True)
    af_array = simulation.calculate('af')
    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
        expected_af_by_year[year])


def test_af3m():
    for year in range(2006, 2010):
        yield check_af3m, year


def check_af3m1(year):
    '''
    test avec 3 enfants
    2 bb et 1+ 14 ans (1 majo pour âge) + test limite inf du forfait puisqu'il a 19 ans en 2009
    montant AF annuel brut de CRDS
    '''
    expected_af_by_year = {2006: 3928.92, 2007 : 3995.64, 2008: 4035.60, 2009: 4156.56}

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(1990, 1, 1)),
            dict(birth = datetime.date(2005, 1, 1)),
            dict(birth = datetime.date(2005, 1, 1)),
            ],
        year = year,
        ).new_simulation(debug = True)
    af_array = simulation.calculate('af')
    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
        expected_af_by_year[year])


def test_af3m1():
    for year in range(2006, 2010):
        yield check_af3m1, year


def check_af31f06(year):
    '''
    test avec 3 enfants
    2 bébés et un de 20 ans en 2006  puis 20 ans en 2008 et enfin 20 ans en 2009(test forfait)
    montant AF annuel brut de CRDS
    '''
    expected_af_by_year = {2006: 2305.80, 2007: 1436.64, 2008: 1451.04, 2009: 1494.48}

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(1986, 1, 1)),
            dict(birth = datetime.date(2005, 1, 1)),
            dict(birth = datetime.date(2005, 1, 1)),
            ],
        year = year,
        ).new_simulation(debug = True)
    af_array = simulation.calculate('af')
    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
        expected_af_by_year[year])


def test_af31f06():
    for year in range(2006, 2010):
        yield check_af31f06, year


def check_af31f08(year):
    '''
    montant AF annuel brut de CRDS
    '''
    expected_af_by_year = {2006: 3928.92, 2007 : 3995.64, 2008: 2368.56, 2009: 1494.48}

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(1988, 1, 1)),
            dict(birth = datetime.date(2005, 1, 1)),
            dict(birth = datetime.date(2005, 1, 1)),
            ],
        year = year,
        ).new_simulation(debug = True)
    af_array = simulation.calculate('af')
    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
        expected_af_by_year[year])


def test_af31f08():
    for year in range(2006, 2010):
        yield check_af31f08, year


def check_af31f09(year):
    '''
    montant AF annuel brut de CRDS
    '''
    expected_af_by_year = {2006: 3928.92, 2007: 3995.64, 2008: 4035.60, 2009: 2439.48}

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(1989, 1, 1)),
            dict(birth = datetime.date(2005, 1, 1)),
            dict(birth = datetime.date(2005, 1, 1)),
            ],
        year = year,
        ).new_simulation(debug = True)
    af_array = simulation.calculate('af')
    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
        expected_af_by_year[year])


def test_af31f09():
    for year in range(2006, 2010):
        yield check_af31f09, year


def check_af3bis(year):
    '''
    3 enfants, un de  14 ans en 2007, un de 20 ans en 2008 et un bb
    donc,1majo en 2006, 2 majo en 2007 et un forfait en 08 (pas de majo pour l'ainé de 2 enf à charge)
    montant AF annuel brut de CRDS
    '''
    expected_af_by_year = {2006: 4326.24, 2007 : 4399.68, 2008: 2368.56, 2009: 1494.48}

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(1988, 1, 1)),
            dict(birth = datetime.date(1993, 1, 1)),
            dict(birth = datetime.date(2005, 1, 1)),
            ],
        year = year,
        ).new_simulation(debug = True)
    af_array = simulation.calculate('af')
    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
        expected_af_by_year[year])


def test_af3bis():
    for year in range(2006, 2010):
        yield check_af3bis, year


def check_af3ter(year):
    '''
    3 enfants, un de 19 ans en 2006, un de 19 ans en 2007, et un bb
    donc 2 majo en 2006, 1 forfait en 2007,
    rien en  2008 (car pas 3 enf a charge en 2007 du coups n'a plus droit au forfait)
    rien en 2009
    montant AF annuel brut de CRDS
    '''
    expected_af_by_year = {2006: 4635.24, 2007 : 2345.04, 2008: 0.0, 2009: 0.0}

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(1987, 1, 1)),
            dict(birth = datetime.date(1988, 1, 1)),
            dict(birth = datetime.date(2005, 1, 1)),
            ],
        year = year,
        ).new_simulation(debug = True)
    af_array = simulation.calculate('af')
    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
        expected_af_by_year[year])


def test_af3ter():
    for year in range(2006, 2010):
        yield check_af3ter, year


def check_af3qua(year):
    '''
    3 enfants, un de 15 ans en 06, un de 18 ans en 06 et un bb
    donc  majo 11 ans et une majo 16 ans en 2006, 2 majo 16 ans en 2007,
    1 forfait 20 ans en  2008 et les al seules pour 2 enf en 2009
    montant AF annuel brut de CRDS
    '''
    expected_af_by_year = {2006: 4326.24, 2007 : 4713.96, 2008: 2368.56, 2009: 1494.48}

    simulation = tax_benefit_system.new_scenario().init_single_entity(
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(1988, 1, 1)),
            dict(birth = datetime.date(1991, 1, 1)),
            dict(birth = datetime.date(2005, 1, 1)),
            ],
        year = year,
        ).new_simulation(debug = True)
    af_array = simulation.calculate('af')
    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
        expected_af_by_year[year])


def test_af3qua():
    for year in range(2006, 2010):
        yield check_af3qua, year


#def check_af5(year):
#    '''
#    test avec 5 enfants
#    de moins de 11 ans
#    montant AF annuel brut de CRDS
#    '''
#    expected_af_by_year = {2006: 6842.40, 2007 : 6958.68, 2008: 7028.16, 2009: 7239.12}

#    simulation = tax_benefit_system.new_scenario().init_single_entity(
#        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
#        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
#        enfants = [
#            dict(birth = datetime.date(2000, 1, 1)),
#            dict(birth = datetime.date(2001, 1, 1)),
#            dict(birth = datetime.date(2002, 1, 1)),
#            dict(birth = datetime.date(2003, 1, 1)),
#            dict(birth = datetime.date(2004, 1, 1)),
#            ],
#        year = year,
#        ).new_simulation(debug = True)
#    af_array = simulation.calculate('af')
#    assert abs(af_array[0] - expected_af_by_year[year]) < 1e-3, 'Got: {}. Expected {}'.format(af_array,
#        expected_af_by_year[year])


#def test_af5():
#    for year in range(2006, 2010):
#        yield check_af5, year


if __name__ == '__main__':
    import logging
    import sys

    import nose

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    nose.core.runmodule(argv = [__file__, '-v', '-i test_*.py'])
#    nose.core.runmodule(argv = [__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit = False)

