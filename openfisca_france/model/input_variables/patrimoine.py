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

from openfisca_core.columns import FloatCol

from ..base import build_column_couple, column_by_name


column_by_name.update(collections.OrderedDict((
    build_column_couple('interets_epargne_sur_livrets', FloatCol(is_permanent = True, entity = 'ind', label = u"Intérêts versés pour l'épargne sur livret")),
    build_column_couple('epargne_non_remuneree', FloatCol(is_permanent = True, entity = 'ind', label = u"Épargne non rémunérée")),
    build_column_couple('revenus_capital', FloatCol(entity = 'ind', label = u"Revenus du capital")),
    build_column_couple('valeur_locative_immo_non_loue', FloatCol(is_permanent = True, entity = 'ind', label = u"Valeur locative des biens immobiliés possédés et non loués")),
    build_column_couple('valeur_locative_terrains_non_loue', FloatCol(is_permanent = True, entity = 'ind', label = u"Valeur locative des terrains possédés et non loués")),
    build_column_couple('revenus_locatifs', FloatCol(entity = 'ind', label = u"Revenus locatifs")),
    )))
