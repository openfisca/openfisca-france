# -*- coding: utf-8 -*-

import datetime

from openfisca_france.scenarios import init_single_entity

from .cache import tax_benefit_system

import pytest


scenarios_arguments = [
    dict(
        period = year,
        parent1 = dict(
            date_naissance = datetime.date(1972, 1, 1),
            salaire_de_base = 2000,
            effectif_entreprise = 25,
            categorie_salarie = "prive_non_cadre",
            ),
        parent2 = dict(
            date_naissance = datetime.date(1972, 1, 1),
            ),
        menage = dict(
            zone_apl = "zone_1",
            ),
        )
    for year in range(2006, 2020)
    ]


@pytest.mark.parametrize("scenario_arguments", scenarios_arguments)
def test_basics(scenario_arguments):
    scenario = tax_benefit_system.new_scenario()
    init_single_entity(scenario, **scenario_arguments)
    simulation = scenario.new_simulation(debug = False)
    period = scenario_arguments['period']
    assert simulation.calculate('revenu_disponible', period = period) is not None, "Can't compute revenu_disponible on period {}".format(period)
    assert simulation.calculate_add('salaire_super_brut', period = period) is not None, \
        "Can't compute salaire_super_brut on period {}".format(period)


def test_init_single_entity_parallel_axes():
    year = 2019
    count = 3
    indexes = [0, 1]
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
        axes = axes,
        period = year
        )

    simulation = init_single_entity(tax_benefit_system.new_scenario(), **scenario_kwargs).new_simulation()
    assert simulation.calculate_add('salaire_de_base', year) == pytest.approx([0, 0, 7500, 7500, 15000, 15000])
