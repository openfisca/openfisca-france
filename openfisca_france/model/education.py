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


from __future__ import division

from numpy import (zeros, maximum as max_, minimum as min_, logical_not as not_, logical_or as or_)
from numpy.core.defchararray import startswith

from .base import *  # noqa
from .pfam import nb_enf


SCOLARITE_INCONNUE = 0
SCOLARITE_COLLEGE = 1
SCOLARITE_LYCEE = 2


reference_input_variable(
    column = EnumCol(
        enum = Enum(
            [
                u"Inconnue",
                u"Collège",
                u"Lycée"
                ],
            ),
        default = 0
        ),
    entity_class = Individus,
    label = u"Scolarité de l'enfant : collège, lycée...",
    name = "scolarite",
    )


@reference_formula
class bourse_college(SimpleFormulaColumn):
    column = FloatCol
    label = u"Montant de la bourse de collège"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        rfr = simulation.calculate('rfr', period.start.offset('first-of', 'year').period('year').offset(-2))
        age_holder = simulation.compute('age', period)
        scolarite_holder = simulation.compute('scolarite', period)
        P = simulation.legislation_at(period.start).bourses_education.bourse_college

        ages = self.split_by_roles(age_holder, roles = ENFS)
        nb_enfants = zeros(len(rfr))
        for key, age in ages.iteritems():
            nb_enfants += age >= 0

        plafond_taux_1 = P.plafond_taux_1 + P.plafond_taux_1 * nb_enfants * P.coeff_enfant_supplementaire
        plafond_taux_2 = P.plafond_taux_2 + P.plafond_taux_2 * nb_enfants * P.coeff_enfant_supplementaire
        plafond_taux_3 = P.plafond_taux_3 + P.plafond_taux_3 * nb_enfants * P.coeff_enfant_supplementaire

        eligible_taux_3 = rfr < plafond_taux_3
        eligible_taux_2 = not_(eligible_taux_3) * (rfr < plafond_taux_2)
        eligible_taux_1 = not_(or_(eligible_taux_2, eligible_taux_3)) * (rfr < plafond_taux_1)

        scolarites = self.split_by_roles(scolarite_holder, roles = ENFS)
        nb_enfants_college = zeros(len(rfr))
        for key, scolarite in scolarites.iteritems():
            nb_enfants_college += scolarite == SCOLARITE_COLLEGE

        montant = (
            eligible_taux_3 * P.montant_taux_3 +
            eligible_taux_2 * P.montant_taux_2 +
            eligible_taux_1 * P.montant_taux_1
            )

        montant *= nb_enfants_college

        return period, montant

