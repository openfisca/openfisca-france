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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import round, maximum as max_

from ..base import *  # noqa
from ..pfam import nb_enf, age_aine


@reference_formula
class af_nbenf(SimpleFormulaColumn):
    column = FloatCol  # TODO: shouldn't be an integer ?
    entity_class = Familles
    label = u"Nombre d'enfants dans la familles au sens des allocations familiales"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period)
        P = simulation.legislation_at(period.start).fam.af

        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
        af_nbenf = nb_enf(age, smic55, P.age1, P.age2)
        return period, af_nbenf


@reference_formula
class af_base(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocations familiales - allocation de base"
    # prestations familiales (brutes de crds)

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        af_nbenf = simulation.calculate('af_nbenf', period)
        P = simulation.legislation_at(period.start).fam

        bmaf = P.af.bmaf
        af_1enf = round(bmaf * P.af.taux.enf1, 2)
        af_2enf = round(bmaf * P.af.taux.enf2, 2)
        af_enf_supp = round(bmaf * P.af.taux.enf3, 2)
        return period, (af_nbenf >= 1) * af_1enf + (af_nbenf >= 2) * af_2enf + max_(af_nbenf - 2, 0) * af_enf_supp


@reference_formula
class af_majo(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocations familiales - majoration pour âge"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        P = simulation.legislation_at(period.start).fam.af

        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
        # TODO: Date d'entrée en vigueur de la nouvelle majoration
        # enfants nés après le "1997-04-30"
        bmaf = P.bmaf
        P_maj = P.maj_age
        af_maj1 = round(bmaf * P_maj.taux1, 2)
        af_maj2 = round(bmaf * P_maj.taux2, 2)
        ageaine = age_aine(age, smic55, P.age1, P.age2)

        def age_sf_aine(age, ag1, ag2, ageaine):
            dum = (ag1 <= ageaine) & (ageaine <= ag2)
            return nb_enf(age, smic55, ag1, ag2) - dum * 1

        nbenf_maj1 = (
            (af_nbenf == 2) * age_sf_aine(age, P_maj.age1, P_maj.age2 - 1, ageaine) +
            nb_enf(age, smic55, P_maj.age1, P_maj.age2 - 1) * (af_nbenf >= 3)
            )
        nbenf_maj2 = (
            (af_nbenf == 2) * age_sf_aine(age, P_maj.age2, P.age2, ageaine) +
            nb_enf(age, smic55, P_maj.age2, P.age2) * (af_nbenf >= 3)
            )
        return period, nbenf_maj1 * af_maj1 + nbenf_maj2 * af_maj2


@reference_formula
class af_forf(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocations familiales - forfait"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age_holder = simulation.compute('age', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        smic55_holder = simulation.compute('smic55', period)
        P = simulation.legislation_at(period.start).fam.af

        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
        bmaf = P.bmaf
        nbenf_forf = nb_enf(age, smic55, P.age3, P.age3)
        af_forfait = round(bmaf * P.taux.forfait, 2)
        return period, ((af_nbenf >= 2) * nbenf_forf) * af_forfait


@reference_formula
class af(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocations familiales - total des allocations"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        af_base = simulation.calculate('af_base', period)
        af_majo = simulation.calculate('af_majo', period)
        af_forf = simulation.calculate('af_forf', period)

        return period, af_base + af_majo + af_forf

