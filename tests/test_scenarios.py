'''Test scenarios.'''


from openfisca_france.scenarios import init_single_entity

from .cache import tax_benefit_system

import pytest


def test_init_single_entity_parallel_axes():
    '''Test parallel axes scenario initialisation.'''
    year = 2019
    count = 3
    indexes = [0, 1, 2]
    salaire_de_base_axes = [
        dict(
            count = count,
            index = index,
            min = 0,
            max = 15000,
            name = 'salaire_de_base',
            period = year,
            )
        for index in indexes
        ]

    axes = [salaire_de_base_axes]

    scenario_kwargs = dict(
        parent1 = dict(age = 40),
        parent2 = dict(age = 40),
        enfants = [dict(age = 20)],
        axes = axes,
        period = year
        )

    simulation = init_single_entity(tax_benefit_system.new_scenario(), **scenario_kwargs).new_simulation()
    assert simulation.calculate_add('salaire_de_base', year) == pytest.approx([0, 0, 0, 7500, 7500, 7500, 15000, 15000, 15000])
