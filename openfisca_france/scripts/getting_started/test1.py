# -*- coding: utf-8 -*-

import datetime

from openfisca_france import init_country

TaxBenefitSystem = init_country()
tax_benefit_system = TaxBenefitSystem()

year = 2015

scenario = tax_benefit_system.new_scenario()
scenario.init_single_entity(
    period = year,
    parent1 = dict(
        birth = datetime.date(year - 30, 1, 1),
        salaire_de_base = 15000,
        ),
    enfants = [
        dict(birth = datetime.date(year - 10, 1, 1)),
        dict(birth = datetime.date(year - 12, 1, 1)),
        dict(birth = datetime.date(year - 18, 1, 1)),
        ],
    )

simulation = scenario.new_simulation()
af = simulation.calculate('af', '2015-01')
print af
