# -*- coding: utf-8 -*-

import datetime

from nose.tools import assert_less
from numpy.testing import assert_array_almost_equal

from openfisca_core import periods
from openfisca_france.tests import base


def test_dossier_de_presse_1():
    # Célibataire sans enfants1 part : revenu mensuel net = 1593 IR2015 = 1138 IR2016 = 828
    year = 2015
    reform = base.get_cached_reform(
        reform_key = 'plf2016',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        period = periods.period('year', year),
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            salaire_imposable = 1651.5 * 12
            ),
        )
    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)
    error_margin = 2

    impo = reference_simulation.calculate('impo')
    reform_impo = reform_simulation.calculate('impo')
    assert_less((abs(-828 - impo)), error_margin)
    assert_less((abs(-1138 - reform_impo)), error_margin)


def test_dossier_de_presse_2():
    # Couple, sans enfants, retraités 2 parts : revenu mensuel net : 2960 IR2015 = 1911 #IR2016 = 1428
    year = 2015
    reform = base.get_cached_reform(
        reform_key = 'plf2016',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        period = periods.period('year', year),
        parent1 = dict(
            birth = datetime.date(year - 70, 1, 1),
            rst = 1530.75 * 12,
            statmarit = 1
            ),
        parent2 = dict(
            birth = datetime.date(year - 65, 1, 1),
            rst = 1530.75 * 12,
            statmarit = 1
            ),
        )
    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)
    error_margin = 2

    assert reference_simulation.calculate('nbptr') == 2
    assert reform_simulation.calculate('nbptr') == 2

    impo = reference_simulation.calculate('impo')
    reform_impo = reform_simulation.calculate('impo')
    assert_less((abs(-1428 - impo)), error_margin)
    assert_less((abs(-1911 - reform_impo)), error_margin)


def test_dossier_de_presse_3():
    # Couple, deux enfants, salariés 3 parts: revenu mensuel net : 3800 IR 2015 : 1879 IR 2016 : 1372
    year = 2015
    reform = base.get_cached_reform(
        reform_key = 'plf2016',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        period = periods.period('year', year),
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            statmarit = 1,
            salaire_imposable = 3938.5 * 12
            ),
        parent2 = dict(
            birth = datetime.date(year - 39, 1, 1),
            statmarit = 1,
            ),
        enfants = [
            dict(birth = datetime.date(year - 10, 1, 1)),
            dict(birth = datetime.date(year - 9, 1, 1)),
            ],
        )
    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)
    error_margin = 3

    assert reference_simulation.calculate('nbptr') == 3
    assert reform_simulation.calculate('nbptr') == 3

    impo = reference_simulation.calculate('impo')
    reform_impo = reform_simulation.calculate('impo')
    assert_less((abs(-1372 - impo)), error_margin)
    assert_less((abs(-1879 - reform_impo)), error_margin)


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)

    # test_dossier_de_presse_1()
    # test_dossier_de_presse_2()
    test_dossier_de_presse_3()