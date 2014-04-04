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

import numpy as np
import openfisca_france


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def check_1_parent(year = 2013):
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'sali',
                max = 100000,
                min = 0,
                ),
            ],
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        year = year,
        ).new_simulation(debug = True)
    simulation.calculate('revdisp')
    sali = simulation.get_holder('sali').new_test_case_array()
    assert (sali - np.linspace(0, 100000, 3)).all() == 0, sali


def test_1_parent():
    for year in range(2002, 2015):
        yield check_1_parent, year


def check_1_parent_2_enfants(year):
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'sali',
                max = 24000,
                min = 0,
                ),
            ],
        parent1 = dict(
            activite = u'Actif occupé',
            birth = 1970,
            cadre = True,
            statmarit = u'Célibataire',
            ),
        enfants = [
            dict(
                activite = u'Étudiant, élève',
                birth = '1992-02-01',
                ),
            dict(
                activite = u'Étudiant, élève',
                birth = '1990-04-17',
                ),
            ],
        year = year,
        ).new_simulation(debug = True)
    sali = simulation.get_holder('sali').new_test_case_array()
    assert (sali - np.linspace(0, 24000, 3)).all() == 0, sali
    simulation.calculate('revdisp')


def test_1_parent_2_enfants():
    for year in range(2002, 2015):
        yield check_1_parent_2_enfants, year


def check_1_parent_2_enfants_1_column(column_name, year):
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'sali',
                max = 24000,
                min = 0,
                ),
            ],
        parent1 = dict(
            activite = u'Actif occupé',
            birth = 1970,
            cadre = True,
            statmarit = u'Célibataire',
            ),
        enfants = [
            dict(
                activite = u'Étudiant, élève',
                birth = '1992-02-01',
                ),
            dict(
                activite = u'Étudiant, élève',
                birth = '1990-04-17',
                ),
            ],
        year = year,
        ).new_simulation(debug = True)
    simulation.calculate(column_name)


def test_1_parent_2_enfants_1_column():
    for column_name, column in tax_benefit_system.column_by_name.iteritems():
        if not column.survey_only:
            for year in range(2006, 2015):
                yield check_1_parent_2_enfants_1_column, column_name, year


#def check_survey(year = 2013):
#    simulation = tax_benefit_system.new_scenario().init_single_entity(
#        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
#        year = year,
#        ).new_simulation(debug = True)
#    simulation.calculate('revdisp')


# def test_survey():
#    for year in (2013, 2014):
#        yield check_survey, year


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_1_parent()
    test_1_parent_2_enfants()
    test_1_parent_2_enfants_1_column()
