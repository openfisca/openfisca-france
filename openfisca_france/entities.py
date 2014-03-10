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


import collections

from openfisca_core import entities


class Familles(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    key_plural = 'familles'
    key_singular = 'famille'
    symbol = 'fam'


class FoyersFiscaux(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    key_plural = 'foyers_fiscaux'
    key_singular = 'foyer_fiscal'
    symbol = 'foy'


class Individus(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    is_persons_entity = True
    key_plural = 'individus'
    key_singular = 'individu'
    symbol = 'ind'


class Menages(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    key_plural = 'menages'
    key_singular = 'menage'
    symbol = 'men'


entity_class_by_symbol = dict(
    fam = Familles,
    foy = FoyersFiscaux,
    ind = Individus,
    men = Menages,
    )

