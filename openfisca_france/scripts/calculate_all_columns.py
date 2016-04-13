# -*- coding: utf-8 -*-

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
                name = 'salaire_imposable',
                max = 100000,
                min = 0,
                ),
            ],
        period = year,
        parent1 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        ).new_simulation(debug = True)
    simulation.calculate('revdisp')
    salaire_imposable = simulation.get_holder('salaire_imposable').new_test_case_array(simulation.period)
    assert (salaire_imposable - np.linspace(0, 100000, 3) == 0).all(), 'salaire_imposable: {}'.format(salaire_imposable)


def test_1_parent():
    for year in range(2002, 2015):
        yield check_1_parent, year


def check_1_parent_2_enfants(year):
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'salaire_imposable',
                max = 24000,
                min = 0,
                ),
            ],
        period = year,
        parent1 = dict(
            activite = u'Actif occupé',
            date_naissance = 1970,
            statmarit = u'Célibataire',
            ),
        enfants = [
            dict(
                activite = u'Étudiant, élève',
                date_naissance = '1992-02-01',
                ),
            dict(
                activite = u'Étudiant, élève',
                date_naissance = '1990-04-17',
                ),
            ],
        ).new_simulation(debug = True)
    salaire_imposable = simulation.get_holder('salaire_imposable').new_test_case_array(simulation.period)
    assert (salaire_imposable - np.linspace(0, 24000, 3) == 0).all(), 'salaire_imposable: {}'.format(salaire_imposable)
    simulation.calculate('revdisp')


def test_1_parent_2_enfants():
    for year in range(2002, 2015):
        yield check_1_parent_2_enfants, year


def check_1_parent_2_enfants_1_column(column_name, year):
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'salaire_imposable',
                max = 24000,
                min = 0,
                ),
            ],
        period = year,
        parent1 = dict(
            activite = u'Actif occupé',
            date_naissance = 1970,
            statmarit = u'Célibataire',
            ),
        enfants = [
            dict(
                activite = u'Étudiant, élève',
                date_naissance = '1992-02-01',
                ),
            dict(
                activite = u'Étudiant, élève',
                date_naissance = '1990-04-17',
                ),
            ],
        ).new_simulation(debug = True)
    simulation.calculate(column_name)


def test_1_parent_2_enfants_1_column():
    for column_name, column in tax_benefit_system.column_by_name.iteritems():
        if not column.survey_only:
            for year in range(2006, 2015):
                yield check_1_parent_2_enfants_1_column, column_name, year


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    check_1_parent()
    test_1_parent()
    test_1_parent_2_enfants()
    test_1_parent_2_enfants_1_column()
