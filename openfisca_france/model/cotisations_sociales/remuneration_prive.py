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


from __future__ import division


import logging

from openfisca_core.columns import EnumCol, FloatCol
from openfisca_core.formulas import SimpleFormulaColumn


from ..base import CAT, QUIFAM, QUIFOY, QUIMEN
from ..base import Individus, reference_formula


log = logging.getLogger(__name__)


CHEF = QUIFAM['chef']
PREF = QUIMEN['pref']
VOUS = QUIFOY['vous']


@reference_formula
class avantages_en_nature(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Avantages en nature"

    def function(self, avantages_en_nature_valeur_reelle, avantages_en_nature_valeur_forfaitaire):
        return avantages_en_nature_valeur_reelle + avantages_en_nature_valeur_forfaitaire

    def get_output_period(self, period):
        return period


@reference_formula
class avantages_en_nature_valeur_forfaitaire(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Evaluation fofaitaire des avantages en nature "

    # TODO:
    def function(self, avantages_en_nature_valeur_reelle):
        return avantages_en_nature_valeur_reelle * 0

    def get_output_period(self, period):
        return period
