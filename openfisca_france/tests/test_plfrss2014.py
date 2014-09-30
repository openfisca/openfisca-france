# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import copy
import datetime


from openfisca_core import legislations, periods
from openfisca_core.reforms import Reform
from openfisca_france.model.cotisations_sociales import plfrss2014
import openfisca_france


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def test_systemic_reform(year = 2013):

    scenario = tax_benefit_system.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 3,
                name = 'sali',
                max = 100000,
                min = 0,
                ),
            ],
        date = datetime.date(year, 1, 1),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        )

    dated_legislation_json_src = legislations.generate_dated_legislation_json(
        tax_benefit_system.legislation_json,
        datetime.date(year, 1, 1)
        )
    reform_dated_legislation_json = copy.deepcopy(dated_legislation_json_src)

    for key, key_parameters in plfrss2014.dated_legislation_diff.iteritems():
        reform_dated_legislation_json["children"][key] = key_parameters

    entity_class_by_key_plural = plfrss2014.build_entity_class_by_key_plural(TaxBenefitSystem)

    # reform = Reform(
    #     column_by_name = column_by_name,
    #     name = "PLFR2014",
    #     reform_dated_legislation_json = reform_dated_legislation_json,
    #     reference_dated_legislation_json = dated_legislation_json_src,
    #     )
    # assert 'plfr2014' in reform.compact_legislation.__dict__


    simulation = scenario.new_simulation(debug = True)
    result = simulation.calculate('impo')
    assert max(abs(result - [0, -7889.20019531, -23435.52929688])) < .01
    from pprint import pprint
    pprint(result)

    # scenario.add_reform(reform)
    # reform_simulation = scenario.new_reform_simulation(debug = True)
    # reform_result = reform_simulation.calculate('reduction_impot_exceptionnelle')
    # from pprint import pprint
    # pprint(reform_result)


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_systemic_reform()
