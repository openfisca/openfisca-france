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

from numpy import (floor, maximum as max_, logical_not as not_, logical_and as and_, logical_or as or_)

from ..base import *  # noqa
from ..pfam import nb_enf


@reference_formula
class asf_elig(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"asf_elig"

    def function(self, simulation, period):
        '''
        Eligibilité à l'allocation de soutien familial (ASF)
        '''
        # Note : Cette variable est calculée pour un an, mais si elle est demandée pour une période plus petite, elle
        # répond pour la période demandée.
        this_rolling_year = period.start.offset('first-of', 'month').period('year')
        if period.stop > this_rolling_year.stop:
            period = this_rolling_year

        isol = simulation.calculate('isol', this_rolling_year)
        residence_mayotte = simulation.calculate('residence_mayotte', this_rolling_year)
        caseT_holder = simulation.compute('caseT', this_rolling_year)
        caseL_holder = simulation.compute('caseL', this_rolling_year)
        alr_holder = simulation.compute('alr', this_rolling_year)

        caseT = self.cast_from_entity_to_role(caseT_holder, role = VOUS)
        caseT = self.any_by_roles(caseT)
        caseL = self.cast_from_entity_to_role(caseL_holder, role = VOUS)
        caseL = self.any_by_roles(caseL)
        alr = self.sum_by_entity(alr_holder)

        return period, not_(residence_mayotte) * isol * (caseT | caseL) * not_(alr > 0)


@reference_formula
class asf_nbenf(SimpleFormulaColumn):
    column = PeriodSizeIndependentIntCol(default = 0)
    entity_class = Familles
    label = u"asf_nbenf"

    def function(self, simulation, period):
        '''
        Nombre d'enfants ouvrant l'éligibilité à l'allocation de soutien familial (ASF)
        '''
        # Note : Cette variable est "instantanée" : quelque soit la période demandée, elle retourne la valeur au premier
        # jour, sans changer la période.
        age_holder = simulation.compute('age', period)
        smic55_holder = simulation.compute('smic55', period, accept_other_period = True)
        P = simulation.legislation_at(period.start).fam

        # TODO: Ajouter orphelin recueilli, soustraction à l'obligation d'entretien (et date de celle-ci),
        # action devant le TGI pour complêter l'éligibilité
        age = self.split_by_roles(age_holder, roles = ENFS)
        smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

        return period, nb_enf(age, smic55, P.af.age1, P.af.age3)


@reference_formula
class asf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Allocation de soutien familial"
    url = "http://vosdroits.service-public.fr/particuliers/F815.xhtml"

    def function(self, simulation, period):
        '''
        Allocation de soutien familial

        L’ASF permet d’aider le conjoint survivant ou le parent isolé ayant la garde
        d’un enfant et les familles ayant à la charge effective et permanente un enfant
        orphelin.
        Vous avez au moins un enfant à votre charge. Vous êtes son père ou sa mère et vous vivez seul(e),
        ou vous avez recueilli cet enfant et vous vivez seul ou en couple.

        http://www.caf.fr/aides-et-services/s-informer-sur-les-aides/solidarite-et-insertion/l-allocation-de-soutien-familial-asf
        '''
        period = period.start.period('month').offset('first-of')
        asf_elig = simulation.calculate('asf_elig', period)#, accept_other_period = True)
        asf_nbenf = simulation.calculate('asf_nbenf', period)#, accept_other_period = True)
        P = simulation.legislation_at(period.start).fam

        # TODO: la valeur est annualisé mais l'ASF peut ne pas être versée toute l'année
        return period, asf_elig * max_(0, asf_nbenf * P.af.bmaf * P.asf.taux1)
