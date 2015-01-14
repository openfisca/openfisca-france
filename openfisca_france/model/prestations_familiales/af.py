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

from numpy import round, maximum as max_, minimum as min_

from ..base import *  # noqa
from ..pfam import nb_enf, age_aine


@reference_formula
class af_nbenf(SimpleFormulaColumn):
    column = FloatCol  # TODO: shouldn't be an integer ?
    entity_class = Familles
    label = u"Nombre d'enfants dans la famille au sens des allocations familiales"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period.offset(-1))
        P = simulation.legislation_at(period.start).fam.af

        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)
        af_nbenf = nb_enf(age, smic55, P.age1, P.age2)

        return period, af_nbenf


@reference_formula
class af_base(DatedFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Allocations familiales - allocation de base"
    # prestations familiales (brutes de crds)

    @dated_function(start = date(2002, 1, 1), stop = date(2015, 6, 30))
    def function_2002(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        af_nbenf = simulation.calculate('af_nbenf', period)
        P = simulation.legislation_at(period.start).fam

        bmaf = P.af.bmaf
        af_1enf = round(bmaf * P.af.taux.enf1, 2)
        af_2enf = round(bmaf * P.af.taux.enf2, 2)
        af_enf_supp = round(bmaf * P.af.taux.enf3, 2)
        return period, (af_nbenf >= 1) * af_1enf + (af_nbenf >= 2) * af_2enf + max_(af_nbenf - 2, 0) * af_enf_supp

    @dated_function(start = date(2015, 7, 1))
    def function_2015(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        af_nbenf = simulation.calculate('af_nbenf', period)
        br_pf = simulation.calculate('br_pf', period.start.offset('first-of', 'year').period('year').offset(-2)) / 12

        legislation_af = simulation.legislation_at(period.start).fam.af
        bmaf = legislation_af.bmaf
        modulation = legislation_af.modulation

        af_1enf = round(bmaf * legislation_af.taux.enf1, 2)
        af_2enf = round(bmaf * legislation_af.taux.enf2, 2)
        af_enf_supp = round(bmaf * legislation_af.taux.enf3, 2)

        montant_base = (af_nbenf >= 1) * af_1enf + (af_nbenf >= 2) * af_2enf + max_(af_nbenf - 2, 0) * af_enf_supp

        plafond1 = modulation.plafond1 + (max_(af_nbenf - 2, 0)) * modulation.enfant_supp
        plafond2 = modulation.plafond2 + (max_(af_nbenf - 2, 0)) * modulation.enfant_supp

        depassement_plafond1 = max_(br_pf - plafond1, 0)
        depassement_plafond2 = max_(br_pf - plafond2, 0)

        montant_servi = (montant_base -
            (br_pf > plafond1) * min_(depassement_plafond1, montant_base * modulation.taux1) -
            (br_pf > plafond2) * min_(depassement_plafond2, montant_base * modulation.taux2)
            )

        return period, montant_servi


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

