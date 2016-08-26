# -*- coding: utf-8 -*-

from __future__ import division

import datetime

from openfisca_core import periods

from openfisca_france.simulations import Simulation

from openfisca_france.model.base import CAT
from openfisca_france.tests import base

scenarios = [
    dict(
        period=year,
        parent1=dict(
            date_naissance=datetime.date(1972, 1, 1),
            salaire_de_base=2000,
            effectif_entreprise=25,
            categorie_salarie=CAT['prive_non_cadre'],
            ),
        menage=dict(
            zone_apl=1,
            ),
        )
    for year in range(2006, 2016)
    ]


def check_run(simulation, period):
    assert simulation.calculate('revdisp', period) is not None, "Can't compute revdisp on period {}".format(period)
    assert simulation.calculate('salaire_super_brut', period) is not None, \
        "Can't compute salaire_super_brut on period {}".format(period)


def test_basics():
    for scenario in scenarios:
        simulation = Simulation(base.tax_benefit_system, scenario)
        period = periods.period(scenario['period'])
        yield check_run, simulation, period


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
    for _, simulation, period in test_basics():
        check_run(simulation, period)
    print u'OpenFisca-France basic test was executed successfully.'.encode('utf-8')
