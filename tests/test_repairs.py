# -*- coding: utf-8 -*-

import datetime
import json

from nose.tools import assert_equal

from cache import tax_benefit_system
from openfisca_france.model.base import *


def test_2_parents_2_enfants():
    year = 2013
    janvier = '2013-01'

    scenario = tax_benefit_system.new_scenario().init_from_attributes(
        test_case = dict(
            individus = [
                dict(),
                dict(date_naissance = datetime.date(year - 30, 1, 1)),
                dict(),
                dict(date_naissance = datetime.date(year - 18, 1, 1)),
                ],
            ),
        repair = True,
        year = year,
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), encoding = 'utf-8', ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation()
    assert_equal(
        simulation.calculate('date_naissance', period = None).tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 30, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite', period=janvier).decode().tolist(),
        [
            TypesActivite.inactif,
            TypesActivite.inactif,
            TypesActivite.etudiant,
            TypesActivite.inactif,
            ],
        )
    assert_equal(
        simulation.calculate('age', period=janvier).tolist(),
        [
            40,
            30,
            10,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois', period=janvier).tolist(),
        [
            40 * 12,
            30 * 12,
            10 * 12,
            18 * 12,
            ],
        )


def test_famille_1_parent_3_enfants():
    year = 2013
    janvier = '2013-01'

    scenario = tax_benefit_system.new_scenario().init_from_attributes(
        test_case = dict(
            familles = [
                dict(
                    parents = [0],
                    enfants = [1, 2, 3],
                    ),
                ],
            individus = [
                dict(),
                dict(),
                dict(date_naissance = datetime.date(year - 12, 1, 1)),
                dict(date_naissance = datetime.date(year - 18, 1, 1)),
                ],
            ),
        repair = True,
        year = year,
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), encoding = 'utf-8', ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation()
    assert_equal(
        simulation.calculate('date_naissance', period = None).tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 12, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite', period=janvier).decode().tolist(),
        [
            TypesActivite.inactif,
            TypesActivite.etudiant,
            TypesActivite.etudiant,
            TypesActivite.inactif,
            ],
        )
    assert_equal(
        simulation.calculate('age', period=janvier).tolist(),
        [
            40,
            10,
            12,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois', period=janvier).tolist(),
        [
            40 * 12,
            10 * 12,
            12 * 12,
            18 * 12,
            ],
        )


def test_famille_2_parents_2_enfants():
    year = 2013
    janvier = '2013-01'

    scenario = tax_benefit_system.new_scenario().init_from_attributes(
        test_case = dict(
            familles = [
                dict(
                    parents = [0, 1],
                    enfants = [2, 3],
                    ),
                ],
            individus = [
                dict(),
                dict(date_naissance = datetime.date(year - 30, 1, 1)),
                dict(),
                dict(date_naissance = datetime.date(year - 18, 1, 1)),
                ],
            ),
        repair = True,
        year = year,
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), encoding = 'utf-8', ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation()
    assert_equal(
        simulation.calculate('date_naissance', period = None).tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 30, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite', period=janvier).decode().tolist(),
        [
            TypesActivite.inactif,
            TypesActivite.inactif,
            TypesActivite.etudiant,
            TypesActivite.inactif,
            ],
        )
    assert_equal(
        simulation.calculate('age', period=janvier).tolist(),
        [
            40,
            30,
            10,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois', period=janvier).tolist(),
        [
            40 * 12,
            30 * 12,
            10 * 12,
            18 * 12,
            ],
        )


def test_foyer_fiscal_1_declarant_3_personnes_a_charge():
    year = 2013
    janvier = '2013-01'

    scenario = tax_benefit_system.new_scenario().init_from_attributes(
        test_case = dict(
            foyers_fiscaux = [
                dict(
                    declarants = [0],
                    personnes_a_charge = [1, 2, 3],
                    ),
                ],
            individus = [
                dict(),
                dict(),
                dict(date_naissance = datetime.date(year - 12, 1, 1)),
                dict(date_naissance = datetime.date(year - 18, 1, 1)),
                ],
            ),
        repair = True,
        year = year,
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), encoding = 'utf-8', ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation()
    assert_equal(
        simulation.calculate('date_naissance', period = None).tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 12, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite', period=janvier).decode().tolist(),
        [
            TypesActivite.inactif,
            TypesActivite.etudiant,
            TypesActivite.etudiant,
            TypesActivite.inactif,
            ],
        )
    assert_equal(
        simulation.calculate('age', period=janvier).tolist(),
        [
            40,
            10,
            12,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois', period=janvier).tolist(),
        [
            40 * 12,
            10 * 12,
            12 * 12,
            18 * 12,
            ],
        )


def test_foyer_fiscal_2_declarants_2_personnes_a_charge():
    year = 2013
    janvier = '2013-01'

    scenario = tax_benefit_system.new_scenario().init_from_attributes(
        test_case = dict(
            foyers_fiscaux = [
                dict(
                    declarants = [0, 1],
                    personnes_a_charge = [2, 3],
                    ),
                ],
            individus = [
                dict(),
                dict(date_naissance = datetime.date(year - 30, 1, 1)),
                dict(),
                dict(date_naissance = datetime.date(year - 18, 1, 1)),
                ],
            ),
        repair = True,
        year = year,
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), encoding = 'utf-8', ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation()
    assert_equal(
        simulation.calculate('date_naissance', period=janvier).tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 30, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite', period=janvier).decode().tolist(),
        [
            TypesActivite.inactif,
            TypesActivite.inactif,
            TypesActivite.etudiant,
            TypesActivite.inactif,
            ],
        )
    assert_equal(
        simulation.calculate('age', period=janvier).tolist(),
        [
            40,
            30,
            10,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois', period=janvier).tolist(),
        [
            40 * 12,
            30 * 12,
            10 * 12,
            18 * 12,
            ],
        )


def test_menage_1_personne_de_reference_3_enfants():
    year = 2013
    janvier = '2013-01'

    scenario = tax_benefit_system.new_scenario().init_from_attributes(
        test_case = dict(
            individus = [
                dict(),
                dict(),
                dict(date_naissance = datetime.date(year - 12, 1, 1)),
                dict(date_naissance = datetime.date(year - 18, 1, 1)),
                ],
            menages = [
                dict(
                    personne_de_reference = 0,
                    enfants = [1, 2, 3],
                    ),
                ],
            ),
        repair = True,
        year = year,
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), encoding = 'utf-8', ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation()
    assert_equal(
        simulation.calculate('date_naissance', period = None).tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 12, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite', period=janvier).decode().tolist(),
        [
            TypesActivite.inactif,
            TypesActivite.etudiant,
            TypesActivite.etudiant,
            TypesActivite.inactif,
            ],
        )
    assert_equal(
        simulation.calculate('age', period=janvier).tolist(),
        [
            40,
            10,
            12,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois', period=janvier).tolist(),
        [
            40 * 12,
            10 * 12,
            12 * 12,
            18 * 12,
            ],
        )


def test_menage_1_personne_de_reference_1_conjoint_2_enfants():
    year = 2013
    janvier = '2013-01'

    scenario = tax_benefit_system.new_scenario().init_from_attributes(
        test_case = dict(
            individus = [
                dict(),
                dict(date_naissance = datetime.date(year - 30, 1, 1)),
                dict(),
                dict(date_naissance = datetime.date(year - 18, 1, 1)),
                ],
            menages = [
                dict(
                    personne_de_reference = 0,
                    conjoint = 1,
                    enfants = [2, 3],
                    ),
                ],
            ),
        repair = True,
        year = year,
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), encoding = 'utf-8', ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation()
    assert_equal(
        simulation.calculate('date_naissance', period = None).tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 30, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite', period=janvier).decode().tolist(),
        [
            TypesActivite.inactif,
            TypesActivite.inactif,
            TypesActivite.etudiant,
            TypesActivite.inactif,
            ],
        )
    assert_equal(
        simulation.calculate('age', period=janvier).tolist(),
        [
            40,
            30,
            10,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois', period=janvier).tolist(),
        [
            40 * 12,
            30 * 12,
            10 * 12,
            18 * 12,
            ],
        )


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_2_parents_2_enfants()
    test_famille_1_parent_3_enfants()
    # test_famille_2_parent_2_enfants()
    test_foyer_fiscal_1_declarant_3_personnes_a_charge()
    test_foyer_fiscal_2_declarants_2_personnes_a_charge()
    test_menage_1_personne_de_reference_3_enfants()
    test_menage_1_personne_de_reference_1_conjoint_2_enfants()
