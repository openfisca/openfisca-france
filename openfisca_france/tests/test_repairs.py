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
import json

from nose.tools import assert_equal

from . import base


def test_2_parents_2_enfants():
    year = 2013
    scenario = base.tax_benefit_system.new_scenario().init_from_attributes(
        test_case = dict(
            individus = [
                dict(),
                dict(birth = datetime.date(year - 30, 1, 1)),
                dict(),
                dict(birth = datetime.date(year - 18, 1, 1)),
                ],
            ),
        repair = True,
        year = year,
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), encoding = 'utf-8', ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation(debug = True)
    assert_equal(
        simulation.calculate('birth').tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 30, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite').tolist(),
        [
            4,
            4,
            2,
            4,
            ],
        )
    assert_equal(
        simulation.calculate('age').tolist(),
        [
            40,
            30,
            10,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois').tolist(),
        [
            40 * 12,
            30 * 12,
            10 * 12,
            18 * 12,
            ],
        )


def test_famille_1_parent_3_enfants():
    year = 2013
    scenario = base.tax_benefit_system.new_scenario().init_from_attributes(
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
                dict(birth = datetime.date(year - 12, 1, 1)),
                dict(birth = datetime.date(year - 18, 1, 1)),
                ],
            ),
        repair = True,
        year = year,
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), encoding = 'utf-8', ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation(debug = True)
    assert_equal(
        simulation.calculate('birth').tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 12, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite').tolist(),
        [
            4,
            2,
            2,
            4,
            ],
        )
    assert_equal(
        simulation.calculate('age').tolist(),
        [
            40,
            10,
            12,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois').tolist(),
        [
            40 * 12,
            10 * 12,
            12 * 12,
            18 * 12,
            ],
        )


def test_famille_2_parents_2_enfants():
    year = 2013
    scenario = base.tax_benefit_system.new_scenario().init_from_attributes(
        test_case = dict(
            familles = [
                dict(
                    parents = [0, 1],
                    enfants = [2, 3],
                    ),
                ],
            individus = [
                dict(),
                dict(birth = datetime.date(year - 30, 1, 1)),
                dict(),
                dict(birth = datetime.date(year - 18, 1, 1)),
                ],
            ),
        repair = True,
        year = year,
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), encoding = 'utf-8', ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation(debug = True)
    assert_equal(
        simulation.calculate('birth').tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 30, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite').tolist(),
        [
            4,
            4,
            2,
            4,
            ],
        )
    assert_equal(
        simulation.calculate('age').tolist(),
        [
            40,
            30,
            10,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois').tolist(),
        [
            40 * 12,
            30 * 12,
            10 * 12,
            18 * 12,
            ],
        )


def test_foyer_fiscal_1_declarant_3_personnes_a_charge():
    year = 2013
    scenario = base.tax_benefit_system.new_scenario().init_from_attributes(
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
                dict(birth = datetime.date(year - 12, 1, 1)),
                dict(birth = datetime.date(year - 18, 1, 1)),
                ],
            ),
        repair = True,
        year = year,
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), encoding = 'utf-8', ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation(debug = True)
    assert_equal(
        simulation.calculate('birth').tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 12, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite').tolist(),
        [
            4,
            2,
            2,
            4,
            ],
        )
    assert_equal(
        simulation.calculate('age').tolist(),
        [
            40,
            10,
            12,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois').tolist(),
        [
            40 * 12,
            10 * 12,
            12 * 12,
            18 * 12,
            ],
        )


def test_foyer_fiscal_2_declarants_2_personnes_a_charge():
    year = 2013
    scenario = base.tax_benefit_system.new_scenario().init_from_attributes(
        test_case = dict(
            foyers_fiscaux = [
                dict(
                    declarants = [0, 1],
                    personnes_a_charge = [2, 3],
                    ),
                ],
            individus = [
                dict(),
                dict(birth = datetime.date(year - 30, 1, 1)),
                dict(),
                dict(birth = datetime.date(year - 18, 1, 1)),
                ],
            ),
        repair = True,
        year = year,
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), encoding = 'utf-8', ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation(debug = True)
    assert_equal(
        simulation.calculate('birth').tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 30, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite').tolist(),
        [
            4,
            4,
            2,
            4,
            ],
        )
    assert_equal(
        simulation.calculate('age').tolist(),
        [
            40,
            30,
            10,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois').tolist(),
        [
            40 * 12,
            30 * 12,
            10 * 12,
            18 * 12,
            ],
        )


def test_menage_1_personne_de_reference_3_enfants():
    year = 2013
    scenario = base.tax_benefit_system.new_scenario().init_from_attributes(
        test_case = dict(
            individus = [
                dict(),
                dict(),
                dict(birth = datetime.date(year - 12, 1, 1)),
                dict(birth = datetime.date(year - 18, 1, 1)),
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
    simulation = scenario.new_simulation(debug = True)
    assert_equal(
        simulation.calculate('birth').tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 12, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite').tolist(),
        [
            4,
            2,
            2,
            4,
            ],
        )
    assert_equal(
        simulation.calculate('age').tolist(),
        [
            40,
            10,
            12,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois').tolist(),
        [
            40 * 12,
            10 * 12,
            12 * 12,
            18 * 12,
            ],
        )


def test_menage_1_personne_de_reference_1_conjoint_2_enfants():
    year = 2013
    scenario = base.tax_benefit_system.new_scenario().init_from_attributes(
        test_case = dict(
            individus = [
                dict(),
                dict(birth = datetime.date(year - 30, 1, 1)),
                dict(),
                dict(birth = datetime.date(year - 18, 1, 1)),
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
    simulation = scenario.new_simulation(debug = True)
    assert_equal(
        simulation.calculate('birth').tolist(),
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 30, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 18, 1, 1),
            ],
        )
    assert_equal(
        simulation.calculate('activite').tolist(),
        [
            4,
            4,
            2,
            4,
            ],
        )
    assert_equal(
        simulation.calculate('age').tolist(),
        [
            40,
            30,
            10,
            18,
            ],
        )
    assert_equal(
        simulation.calculate('age_en_mois').tolist(),
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
