# -*- coding: utf-8 -*-

import openfisca_france

tax_benefit_system = openfisca_france.init_tax_benefit_system()

scenario = tax_benefit_system.new_scenario()
scenario.init_single_entity(
    period = 2015,
    parent1 = dict(
        age = 30,
        salaire_de_base = 15000,
        ),
    enfants = [
        dict(age = 10),
        dict(age = 12),
        dict(age = 18),
        ],
    )

simulation = scenario.new_simulation()
af = simulation.calculate('af', '2015-01')
print af
