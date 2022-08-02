'''Basic test of all covered years.'''

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
            categorie_salarie = 'prive_non_cadre',
            ),
        parent2 = dict(
            date_naissance = datetime.date(1972, 1, 1),
            ),
        menage = dict(
            zone_apl = 'zone_1',
            ),
        )
    for year in range(2006, 2020)
    ]


@pytest.mark.parametrize('scenario_arguments', scenarios_arguments)
def test_basics(scenario_arguments):
    '''Basic test for a specific year.

    Args:
        scenario_arguments (dict): Arguments to initialize scenario.
    '''
    scenario = tax_benefit_system.new_scenario()
    init_single_entity(scenario, **scenario_arguments)
    simulation = scenario.new_simulation(debug = False)
    period = scenario_arguments['period']
    assert simulation.calculate('revenu_disponible', period = period) is not None, "Can't compute revenu_disponible on period {}".format(period)
    assert simulation.calculate_add('salaire_super_brut', period = period) is not None,\
        "Can't compute salaire_super_brut on period {}".format(period)
