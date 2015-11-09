# -*- coding: utf-8 -*-

import openfisca_france
from openfisca_france.reforms import plfr2014

tax_benefit_system = openfisca_france.init_tax_benefit_system()
reformed_tax_benefit_system = plfr2014.build_reform(tax_benefit_system)

scenario = reformed_tax_benefit_system.new_scenario()
scenario.init_single_entity(
    period = 2013,
    parent1 = dict(
        age = 40,
        salaire_imposable = 13795,
        ),
    )

simulation = scenario.new_simulation(reference = True)
impo = simulation.calculate('impo', '2013')
print impo

reform_simulation = scenario.new_simulation()
reform_impo = reform_simulation.calculate('impo', '2013')
print reform_impo
