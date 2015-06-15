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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from ...base import *  # noqa analysis:ignore
from numpy import vectorize


reference_input_variable(
    name ='test_precondition_remplie',
    column = BoolCol,
    entity_class = Familles,
    label = u"Critère d'éligibilité",
)


@reference_formula
class parisien(SimpleFormulaColumn):
    column = BoolCol
    label = u"Parisien"
    entity_class = Familles

    def function(self, simulation, period):
        depcom = simulation.calculate('depcom', period)
        print(depcom)

        def is_parisien(code_insee):
            prefix = code_insee[0:2]
            sufix = code_insee[2:5]
            result = (prefix == "75") and ((int(sufix) in range(101, 121)) or sufix == "056")
            return result

        is_parisien_vec = vectorize(is_parisien)

        result = is_parisien_vec(depcom)

        return period, result


@reference_formula
class test_paris(SimpleFormulaColumn):
    column = FloatCol
    label = u"Montant de l'aide"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        parisien = simulation.calculate('parisien', period)
        print(parisien)

        result = parisien * 1000

        return period, result
