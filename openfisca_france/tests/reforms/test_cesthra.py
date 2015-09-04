# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE,  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program,  If not, see <http://www.gnu.org/licenses/>.


import datetime


from openfisca_core import periods
from openfisca_france.tests import base


def test_cesthra_invalidee():
    year = 2012
    period = periods.period('year', year)
    reform = base.get_cached_reform(
        reform_key = 'cesthra_invalidee',
        tax_benefit_system = base.tax_benefit_system,
        )
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 10,
                max = 30000,
                min = 0,
                name = 'salaire_imposable',
                ),
            ],
        period = period,
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)),
            dict(birth = datetime.date(year - 9, 1, 1)),
            ],
        )

    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reference_impo = reference_simulation.calculate('impo')
    assert reference_impo is not None
    reference_revdisp = reference_simulation.calculate('revdisp', period = period)
    assert reference_revdisp is not None

    reform_simulation = scenario.new_simulation(debug = True)
    reform_impo = reform_simulation.calculate('impo')
    assert reform_impo is not None
    reform_revdisp = reform_simulation.calculate('revdisp', period = period)
    assert reform_revdisp is not None


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_cesthra_invalidee()
