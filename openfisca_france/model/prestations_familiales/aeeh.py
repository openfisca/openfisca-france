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

from numpy import (floor, maximum as max_, logical_not as not_, logical_and as and_, logical_or as or_)
from openfisca_core.accessors import law

from ..base import QUIFAM, QUIFOY


CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
VOUS = QUIFOY['vous']
CONJ = QUIFOY['conj']


def _aeeh_2003_(self, age_holder, inv_holder, isol, categ_inv_holder, P = law.fam):
    '''
    Allocation d'éducation de l'enfant handicapé (Allocation d'éducation spécialisée avant le 1er janvier 2006)

    Ce montant peut être majoré par un complément accordé par la Cdaph qui prend en compte :
    le coût du handicap de l'enfant,
    la cessation ou la réduction d'activité professionnelle d'un ou l'autre des deux parents,
    l'embauche d'une tierce personne rémunérée.

    Une majoration est versée au parent isolé bénéficiaire d'un complément d'Aeeh lorsqu'il cesse ou réduit son activité
    professionnelle ou lorsqu'il embauche une tierce personne rémunérée.
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    categ_inv = self.split_by_roles(categ_inv_holder, roles = ENFS)
    inv = self.split_by_roles(inv_holder, roles = ENFS)

    aeeh = 0
    for enfant in age.iterkeys():
        enfhand = inv[enfant] * (age[enfant] < P.aeeh.age) / 12
        categ = categ_inv[enfant]
        aeeh += enfhand * (P.af.bmaf * (P.aeeh.base +
                              P.aeeh.cpl1 * (categ == 1) +
                              (categ == 2) * (P.aeeh.cpl2 + P.aeeh.maj2 * isol) +
                              (categ == 3) * (P.aeeh.cpl3 + P.aeeh.maj3 * isol) +
                              (categ == 4) * (P.aeeh.cpl4 + P.aeeh.maj4 * isol) +
                              (categ == 5) * (P.aeeh.cpl5 + P.aeeh.maj5 * isol) +
                              (categ == 6) * (P.aeeh.maj6 * isol)) +
                              (categ == 6) * P.aeeh.cpl6)

# L'attribution de l'AEEH de base et de ses compléments éventuels ne fait pas obstacle au
# versement des prestations familiales.
# L'allocation de présence parentale peut être cumulée avec l'AEEH de base, mais pas avec son
# complément ni avec la majoration de parent isolé.
# Tous les éléments de la prestattion de compensation du handicap (PCH) sont également ouverts
# aux bénéficiaires de l'AEEH de base, sous certaines conditions, mais ce cumul est exclusif du
# complément de l'AEEH. Les parents d'enfants handicapés doivent donc choisir entre le versement
# du complément d'AEEH et la PCH.

    # Ces allocations ne sont pas soumis à la CRDS
    return 12 * aeeh  # annualisé


def _aeeh__2002(self, age_holder, inv_holder, categ_inv_holder, P = law.fam):
    '''
    Allocation d'éducation de l'enfant handicapé (Allocation d'éducation spécialisée avant le 1er janvier 2006)

    Ce montant peut être majoré par un complément accordé par la Cdaph qui prend en compte :
    le coût du handicap de l'enfant,
    la cessation ou la réduction d'activité professionnelle d'un ou l'autre des deux parents,
    l'embauche d'une tierce personne rémunérée.

    Une majoration est versée au parent isolé bénéficiaire d'un complément d'Aeeh lorsqu'il cesse ou réduit son activité
    professionnelle ou lorsqu'il embauche une tierce personne rémunérée.
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    categ_inv = self.split_by_roles(categ_inv_holder, roles = ENFS)
    inv = self.split_by_roles(inv_holder, roles = ENFS)

    aeeh = 0
    for enfant in age.iterkeys():
        enfhand = inv[enfant] * (age[enfant] < P.aeeh.age) / 12
        categ = categ_inv[enfant]
        aeeh += 0 * enfhand  # TODO:

# L'attribution de l'AEEH de base et de ses compléments éventuels ne fait pas obstacle au
# versement des prestations familiales.
# L'allocation de présence parentale peut être cumulée avec l'AEEH de base, mais pas avec son
# complément ni avec la majoration de parent isolé.
# Tous les éléments de la prestattion de compensation du handicap (PCH) sont également ouverts
# aux bénéficiaires de l'AEEH de base, sous certaines conditions, mais ce cumul est exclusif du
# complément de l'AEEH. Les parents d'enfants handicapés doivent donc choisir entre le versement
# du complément d'AEEH et la PCH.

    # Ces allocations ne sont pas soumis à la CRDS
    return 12 * aeeh  # annualisé
