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


from __future__ import division

from numpy import logical_not as not_

from ...base import *  # noqa analysis:ignore

# from .base_ressource import nb_enf


@reference_formula
class asf_elig_i(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Individus
    label = u"Éligibilité à l'ASF (individuelle)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        age = simulation.calculate('age', period)
        smic55 = simulation.calculate('smic55', period)
        pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', period)

        pfam = simulation.legislation_at(period.start).fam

        eligibilite = (
            (age >= pfam.af.age1) * (age <= pfam.af.age3) * # Âge compatible avec les prestations familiales
            not_(smic55) * # Ne perçoit pas plus de ressources que "55% du SMIC" au sens CAF
            (pensions_alimentaires_percues == 0)) # Ne perçoit pas de pension alimentaire

        return period, eligibilite

@reference_formula
class asf_i(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Individus
    label = u"Montant à verser à l'individu pour l'ASF"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        asf_elig_i = simulation.calculate('asf_elig_i', period)
        pfam = simulation.legislation_at(period.start).fam

        return period, asf_elig_i * pfam.af.bmaf * pfam.asf.taux1


@reference_formula
class asf_elig(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Éligibilité à l'ASF"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        isol = simulation.calculate('isol', period)
        residence_mayotte = simulation.calculate('residence_mayotte', period)

        return period, not_(residence_mayotte) * isol # Parent isolé et ne résident pas à Mayotte


@reference_formula
class asf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation de soutien familial (ASF)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        asf_elig = simulation.calculate('asf_elig', period)
        asf_i_holder = simulation.compute('asf_i', period)
        montant = self.sum_by_entity(asf_i_holder, roles = ENFS)

        return period, asf_elig * montant
