# -*- coding: utf-8 -*-

from __future__ import division

import datetime


from openfisca_core import periods

from openfisca_france.reforms import inversion_revenus
from openfisca_france.model.base import CAT
from openfisca_france.tests.base import assert_near, tax_benefit_system


def test_cho(year = 2014):
    period = periods.period("{}-01".format(year))
    single_entity_kwargs = dict(
        axes = [dict(count = 101, max = 2000, min = 0, name = 'chomage_brut')],
        period = period,
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        )
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        **single_entity_kwargs).new_simulation(debug = True)
    brut = simulation.get_holder('chomage_brut').array
    imposable = simulation.calculate('chomage_imposable')

    inversion_reform = inversion_revenus.build_reform(tax_benefit_system)
    inverse_simulation = inversion_reform.new_scenario().init_single_entity(
        **single_entity_kwargs).new_simulation(debug = True)

    inverse_simulation.get_holder('chomage_brut').delete_arrays()
    inverse_simulation.get_or_new_holder('chomage_imposable_pour_inversion').array = imposable.copy()
    new_brut = inverse_simulation.calculate('chomage_brut')
    assert_near(new_brut, brut, absolute_error_margin = 1)


def test_retraite(year = 2014):
    period = periods.period("{}-01".format(year))
    single_entity_kwargs = dict(
        axes = [dict(count = 101, max = 2000, min = 0, name = 'retraite_brute')],
        period = period,
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            ),
        )
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        **single_entity_kwargs
        ).new_simulation(debug = True)
    brut = simulation.get_holder('retraite_brute').array
    imposable = simulation.calculate('retraite_imposable')

    inversion_reform = inversion_revenus.build_reform(tax_benefit_system)
    inverse_simulation = inversion_reform.new_scenario().init_single_entity(
        **single_entity_kwargs).new_simulation(debug = True)

    inverse_simulation.get_holder('retraite_brute').delete_arrays()
    inverse_simulation.get_or_new_holder('retraite_imposable_pour_inversion').array = imposable.copy()
    new_brut = inverse_simulation.calculate('retraite_brute')
    assert_near(new_brut, brut, absolute_error_margin = 1)


def check_sal(type_sal, year = 2014):
    period = periods.period("{}-01".format(year))
    single_entity_kwargs = dict(
        axes = [dict(count = 101, max = 2000, min = 40, name = 'salaire_de_base')],  # TODO: min = 0
        period = period,
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            type_sal = type_sal,
            ),
        )
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        **single_entity_kwargs
        ).new_simulation(debug = False)
    brut = simulation.get_holder('salaire_de_base').array
    smic_horaire = simulation.legislation_at(period.start).cotsoc.gen.smic_h_b
    smic_mensuel = smic_horaire * 35 * 52 / 12
    brut = simulation.get_holder('salaire_de_base').array
    simulation.get_or_new_holder('contrat_de_travail').array = brut < smic_mensuel  # temps plein ou temps partiel
    simulation.get_or_new_holder('heures_remunerees_volume').array = brut // smic_horaire  # temps plein ou partiel

    imposable = simulation.calculate('salaire_imposable')

    inversion_reform = inversion_revenus.build_reform(tax_benefit_system)
    inverse_simulation = inversion_reform.new_scenario().init_single_entity(
        **single_entity_kwargs).new_simulation(debug = True)

    inverse_simulation.get_holder('salaire_de_base').delete_arrays()
    inverse_simulation.get_or_new_holder('salaire_imposable_pour_inversion').array = imposable.copy()
    inverse_simulation.get_or_new_holder('contrat_de_travail').array = brut < smic_mensuel  # temps plein ou partiel
    inverse_simulation.get_or_new_holder('heures_remunerees_volume').array = (
        (brut // smic_horaire) * (brut < smic_mensuel)
        )

    new_brut = inverse_simulation.calculate('salaire_de_base')
    assert_near(new_brut, brut, absolute_error_margin = 1)


def test_sal(year = 2014):
    for type_sal_category in ('prive_non_cadre', 'prive_cadre'):  # , 'public_titulaire_etat'):
        yield check_sal, CAT[type_sal_category], year


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_cho()
    test_retraite()
    for function, type_sal, year in test_sal():
        function(type_sal, year)
