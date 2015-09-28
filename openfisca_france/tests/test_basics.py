# -*- coding: utf-8 -*-

from __future__ import division

import datetime

from openfisca_france.model.base import CAT
from openfisca_france.tests import base


tests_infos = [
    dict(
        period = year,
        parent1 = dict(
            birth = datetime.date(1972, 1, 1),
            salaire_de_base = 2000,
            effectif_entreprise = 25,
            type_sal = CAT['prive_non_cadre'],
            ),
        menage = dict(
            zone_apl = 1,
            ),
        ) for year in range(2015, 2002, -1)
    ]


def check_run(simulation, period):
    assert simulation.calculate('revdisp') is not None, "Can't compute revdisp on period {}".format(period)
    assert simulation.calculate('salsuperbrut') is not None, "Can't compute salsuperbrut on period {}".format(period)


def test():
    for scenario_arguments in tests_infos:
        simulation = base.tax_benefit_system.new_scenario().init_single_entity(**scenario_arguments).new_simulation(
            debug = False)
        period = scenario_arguments['period']
        yield check_run, simulation, period


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test()
