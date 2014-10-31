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


import openfisca_france
from openfisca_france.reforms import plf2015
from openfisca_france.tests.reforms.utils import init

TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()


def test(year = 2014):

    reform_simulation, reference_simulation = init(plf2015, year)
    error_margin = 0.01
    impo = reference_simulation.calculate('impo')
    print impo
    reform_impo = reform_simulation.calculate('impo')
    print reform_impo


if __name__ == '__main__':
#    test()
    from openfisca_france.tests.reforms.utils import graph
    graph(plf2015, 2014)