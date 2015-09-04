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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from ...base import *  # noqa analysis:ignore

build_column('indemnites_journalieres_maternite', FloatCol(entity = 'ind', label = u"Indemnités journalières de maternité"))
build_column('indemnites_journalieres_paternite', FloatCol(entity = 'ind', label = u"Indemnités journalières de paternité"))
build_column('indemnites_journalieres_adoption', FloatCol(entity = 'ind', label = u"Indemnités journalières d'adoption"))
build_column('indemnites_journalieres_maladie', FloatCol(entity = 'ind', label = u"Indemnités journalières de maladie"))
build_column('indemnites_journalieres_accident_travail', FloatCol(entity = 'ind', label = u"Indemnités journalières d'accident du travail"))
build_column('indemnites_journalieres_maladie_professionnelle', FloatCol(entity = 'ind', label = u"Indemnités journalières de maladie professionnelle"))


@reference_formula
class indemnites_journalieres(SimpleFormulaColumn):
    column = FloatCol
    label = u"Total des indemnités journalières"
    entity_class = Individus

    def function(self, simulation, period):
        indemnites_journalieres_maternite = simulation.calculate('indemnites_journalieres_maternite', period)
        indemnites_journalieres_paternite = simulation.calculate('indemnites_journalieres_paternite', period)
        indemnites_journalieres_adoption = simulation.calculate('indemnites_journalieres_adoption', period)
        indemnites_journalieres_maladie = simulation.calculate('indemnites_journalieres_maladie', period)
        indemnites_journalieres_accident_travail = simulation.calculate('indemnites_journalieres_accident_travail', period)
        indemnites_journalieres_maladie_professionnelle = simulation.calculate('indemnites_journalieres_accident_travail', period)
        result = indemnites_journalieres_maternite + indemnites_journalieres_paternite + indemnites_journalieres_adoption + indemnites_journalieres_maladie + indemnites_journalieres_accident_travail + indemnites_journalieres_maladie_professionnelle

        return period, result


@reference_formula
class indemnites_journalieres_imposables(SimpleFormulaColumn):
    column = FloatCol
    label = u"Total des indemnités journalières imposables"
    entity_class = Individus
    url = "http://vosdroits.service-public.fr/particuliers/F3152.xhtml"

    def function(self, simulation, period):
        indemnites_journalieres = simulation.calculate('indemnites_journalieres', period)
        indemnites_journalieres_accident_travail = simulation.calculate('indemnites_journalieres_accident_travail', period)
        indemnites_journalieres_maladie_professionnelle = simulation.calculate('indemnites_journalieres_accident_travail', period)
        result = indemnites_journalieres - 0.5 * (
            indemnites_journalieres_accident_travail + indemnites_journalieres_maladie_professionnelle
        )

        return period, result
