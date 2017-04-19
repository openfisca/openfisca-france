# -*- coding: utf-8 -*-

import datetime


from openfisca_core import periods
from openfisca_france.reforms.cesthra_invalidee import cesthra_invalidee
from ..cache import tax_benefit_system


def test_cesthra_invalidee():
    year = 2012
    period = periods.period(year)
    reform = cesthra_invalidee(tax_benefit_system)
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 10,
                max = 30000,
                min = 0,
                name = 'salaire_imposable',
                ),
            ],
        period = period,
        parent1 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        parent2 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(date_naissance = datetime.date(year - 9, 1, 1)),
            dict(date_naissance = datetime.date(year - 9, 1, 1)),
            ],
        )

    reference_simulation = scenario.new_simulation(reference = True)
    reference_impo = reference_simulation.calculate('impots_directs', period = period)
    assert reference_impo is not None
    reference_revenu_disponible = reference_simulation.calculate('revenu_disponible', period = period)
    assert reference_revenu_disponible is not None

    reform_simulation = scenario.new_simulation()
    reform_impots_directs = reform_simulation.calculate('impots_directs', period = period)
    assert reform_impots_directs is not None
    reform_revenu_disponible = reform_simulation.calculate('revenu_disponible', period = period)
    assert reform_revenu_disponible is not None


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_cesthra_invalidee()
