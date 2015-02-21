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


from ..base import *  # noqa


reference_input_variable(base_function = last_duration_last_value, column = FloatCol, entity_class = Individus,
    label = u"Épargne non rémunérée", name = 'epargne_non_remuneree')

reference_input_variable(base_function = last_duration_last_value, column = FloatCol, entity_class = Individus,
    label = u"Intérêts versés pour l'épargne sur livret", name = 'interets_epargne_sur_livrets')

reference_input_variable(base_function = last_duration_last_value, column = FloatCol, entity_class = Individus,
    label = u"Revenus du capital", name = 'revenus_capital')

reference_input_variable(base_function = last_duration_last_value, column = FloatCol, entity_class = Individus,
    label = u"Revenus locatifs", name = 'revenus_locatifs')

reference_input_variable(base_function = last_duration_last_value, column = FloatCol, entity_class = Individus,
    label = u"Valeur locative des biens immobiliers possédés et non loués", name = 'valeur_locative_immo_non_loue')

reference_input_variable(base_function = last_duration_last_value, column = FloatCol, entity_class = Individus,
    label = u"Valeur locative des terrains possédés et non loués", name = 'valeur_locative_terrains_non_loue')
