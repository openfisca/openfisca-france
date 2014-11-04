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


import matplotlib.pyplot as plt


import datetime

from openfisca_core import periods
import openfisca_france
from openfisca_qt.matplotlib import graphs


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def show_revdisp(year = 2013, max_sal = 30000, people = 1, filename = None):
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = periods.period('year', year),
        parent1 = dict(
            birth = datetime.date(year - 40, 1, 1),
            sali = max_sal),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)) if people >= 2 else None,
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 3 else None,
            dict(birth = datetime.date(year - 9, 1, 1)) if people >= 4 else None,
            ] if people >= 3 else None,
        ).new_simulation(debug = True, reference = True)

    fig = plt.figure()
    axes = plt.gca()
    graphs.draw_waterfall(
        simulation = simulation,
        axes = axes,
        visible = ["revdisp", "sal"],
        )
    plt.show()
    if filename:
        fig.savefig('{}.png'.format(filename))

if __name__ == '__main__':
    show_revdisp(filename = "waterfall")
