# -*- coding: utf-8 -*-

import datetime
import json

from .cache import tax_benefit_system
from openfisca_france.model.base import *


def test_birth():
    year = 2013
    janvier = '2013-01'

    scenario = tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = dict(),
        enfants = [
            dict(),
            dict(date_naissance = datetime.date(year - 12, 1, 1)),
            dict(date_naissance = datetime.date(year - 18, 1, 1)),
            ],
        )
    scenario.suggest()
    json.dumps(scenario.to_json(), ensure_ascii = False, indent = 2)
    simulation = scenario.new_simulation()
    assert (
        simulation.calculate('date_naissance', period = None).tolist() ==
        [
            datetime.date(year - 40, 1, 1),
            datetime.date(year - 10, 1, 1),
            datetime.date(year - 12, 1, 1),
            datetime.date(year - 18, 1, 1),
            ])
    assert (
        simulation.calculate('activite', period = janvier).decode().tolist() ==
        [
            TypesActivite.inactif,
            TypesActivite.etudiant,
            TypesActivite.etudiant,
            TypesActivite.inactif,
            ])
    assert (
        simulation.calculate('age', period = janvier).tolist() ==
        [
            40,
            10,
            12,
            18,
            ])
    assert (
        simulation.calculate('age_en_mois', period = janvier).tolist() ==
        [
            40 * 12,
            10 * 12,
            12 * 12,
            18 * 12,
            ])


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_birth()
