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


import datetime
import os

from openfisca_core import periods
from openfisca_france.tests import base


def graph(reform_module, year):
    from openfisca_qt.matplotlib import graphs
    from openfisca_france.tests.reforms.utils import init
    import matplotlib.pyplot as plt

    reform_simulation, reference_simulation = init(
        reform_module = reform_module,
        year = year,
        )

    reference_simulation.calculate('revdisp')
    reform_simulation.calculate('revdisp')

    def plot(simulation, reference_simulation = None, filename = None):
        fig = plt.figure()
        axes = plt.gca()
        graphs.draw_bareme(
            simulation = simulation,
            axes = axes,
            x_axis = 'sal',
            reference_simulation = reference_simulation,
            visible_lines = ['revdisp'])
        plt.show()
        if filename:
            fig.savefig('{}.png'.format(filename))

    reform_name = os.path.splitext(os.path.basename(reform_module.__file__))[0]
    filename = "{}_reform".format(reform_name)
    plot(simulation = reform_simulation, filename = filename)

    filename = "{}_reference".format(reform_name)
    plot(simulation = reference_simulation, filename = filename)

    filename = "{}_diff".format(reform_name)
    plot(reform_simulation, reference_simulation, filename = filename)


def init(reform_module = None, year = None, people = 1, max_sal = 30000):
    assert reform_module is not None
    assert year is not None
    reform = reform_module.build_reform(base.tax_benefit_system)
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 200,
                max = max_sal,
                min = 0,
                name = 'sali',
                ),
            ],
        period = periods.period('year', year),
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)) if people >= 2 else None,
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 3 else None,
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 4 else None,
            ] if people >= 3 else None,
        )

    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)
    return reform_simulation, reference_simulation


