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

from numpy import (round, floor, maximum as max_, logical_not as not_, logical_and as and_, logical_or as or_)
from openfisca_core.accessors import law

from ..input_variables.base import QUIFAM, QUIFOY
from ..pfam import nb_enf, age_aine

CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
VOUS = QUIFOY['vous']
CONJ = QUIFOY['conj']


def _af_nbenf(self, age_holder, smic55_holder, P = law.fam.af):
    '''
    Nombre d'enfants dans la familles au sens des allocations familiales
    'fam'
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

    af_nbenf = nb_enf(age, smic55, P.age1, P.age2)
    return af_nbenf


def _af_base(af_nbenf, P = law.fam):
    '''
    Allocations familiales - allocation de base
    'fam'
    '''
    bmaf = P.af.bmaf
    # prestations familiales (brutes de crds)
    af_1enf = round(bmaf * P.af.taux.enf1, 2)
    af_2enf = round(bmaf * P.af.taux.enf2, 2)
    af_enf_supp = round(bmaf * P.af.taux.enf3, 2)
    af_base = (af_nbenf >= 1) * af_1enf + (af_nbenf >= 2) * af_2enf + max_(af_nbenf - 2, 0) * af_enf_supp
    return 12 * af_base  # annualisé


def _af_majo(self, age_holder, smic55_holder, af_nbenf, P = law.fam.af):
    '''
    Allocations familiales - majoration pour âge
    'fam'
    '''
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


    nbenf_maj1 = ((af_nbenf == 2) * age_sf_aine(age, P_maj.age1, P_maj.age2 - 1, ageaine)
                   + nb_enf(age, smic55, P_maj.age1, P_maj.age2 - 1) * (af_nbenf >= 3))
    nbenf_maj2 = ((af_nbenf == 2) * age_sf_aine(age, P_maj.age2, P.age2, ageaine)
                   + nb_enf(age, smic55, P_maj.age2, P.age2) * (af_nbenf >= 3))

    af_majo = nbenf_maj1 * af_maj1 + nbenf_maj2 * af_maj2

    return 12 * af_majo  # annualisé


def _af_forf(self, age_holder, af_nbenf, smic55_holder, P = law.fam.af):
    '''
    Allocations familiales - forfait
    'fam'
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

    bmaf = P.bmaf
    nbenf_forf = nb_enf(age, smic55, P.age3, P.age3)
    af_forfait = round(bmaf * P.taux.forfait, 2)
    return 12 * ((af_nbenf >= 2) * nbenf_forf) * af_forfait  # annualisé

# def _af(af_base, af_majo, af_forf, _freq = {"af_base" : "year"}):
def _af(af_base, af_majo, af_forf):
    '''
    Allocations familiales - total des allocations
    'fam'
    '''
    return af_base + af_majo + af_forf
