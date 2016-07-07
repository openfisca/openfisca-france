# -*- coding: utf-8 -*-


import datetime

from openfisca_core import periods
from openfisca_core.tools import assert_near
from openfisca_france.tests.base import tax_benefit_system

from openfisca_france.reforms.landais_piketty_saez import landais_piketty_saez


def test():
    year = 2013
    reform = landais_piketty_saez(tax_benefit_system)
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                max = 30000,
                min = 0,
                name = 'salaire_de_base',
                ),
            ],
        period = periods.period('year', year),
        parent1 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        # parent2 = dict(date_naissance = datetime.date(year - 40, 1, 1)),
        # enfants = [
        #     dict(date_naissance = datetime.date(year - 9, 1, 1)),
        #     dict(date_naissance = datetime.date(year - 9, 1, 1)),
        #     ],
        )

#    reference_simulation = scenario.new_simulation(reference = True)
#

    reform_simulation = scenario.new_simulation()
    reform_assiette_csg = reform_simulation.calculate('assiette_csg')
    reform_impot_revenu_lps = reform_simulation.calculate('impot_revenu_lps')
    assert_near(
        -reform_impot_revenu_lps,
        ((reform_assiette_csg - 10000) * .25 / 30000 + .25) * reform_assiette_csg,
        absolute_error_margin = 0.01,
        )
