from openfisca_core.rates import average_rate, marginal_rate

from openfisca_france.scenarios import init_single_entity

from .cache import tax_benefit_system


def test_average_tax_rate():
    year = 2013
    simulation = init_single_entity(tax_benefit_system.new_scenario(),
        axes = [[
            dict(
                count = 100,
                name = 'salaire_imposable',
                max = 24000,
                min = 0,
                ),
            ]],
        period = year,
        parent1 = dict(age = 40),
        ).new_simulation()
    assert (average_rate(
        target = simulation.calculate('revenu_disponible', period = year),
        varying = simulation.calculate('revenu_disponible', period = year),
        ) == 0).all()


def test_marginal_tax_rate():
    year = 2013
    simulation = init_single_entity(tax_benefit_system.new_scenario(),
        axes = [[
            dict(
                count = 10000,
                name = 'salaire_imposable',
                max = 1000000,
                min = 0,
                ),
            ]],
        period = year,
        parent1 = dict(age = 40),
        ).new_simulation()
    assert (marginal_rate(
        target = simulation.calculate('revenu_disponible', period = year),
        varying = simulation.calculate('revenu_disponible', period = year),
        ) == 0).all()


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_marginal_tax_rate()
    test_average_tax_rate()
