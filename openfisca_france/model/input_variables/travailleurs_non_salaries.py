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


from openfisca_core.columns import FloatCol, EnumCol
from openfisca_core.enumerations import Enum

from ..base import build_column


build_column('tns_chiffre_affaires_micro_entreprise', FloatCol(entity = 'ind', is_permanent = True, label = u"Chiffre d'affaires de micro-entreprise ou assimilée"))
build_column('tns_autres_revenus', FloatCol(entity = 'ind', is_permanent = True, label = u"Autres revenus non salariés"))

build_column('tns_type_structure', EnumCol(
    entity = 'ind',
    enum = Enum([u'auto_entrepreneur', u'micro_entreprise']),
    default = 1,
    label = u"Type de structure associée au travailleur non salarié"))

build_column('tns_type_activite', EnumCol(
    entity = 'ind',
    enum = Enum([u'achat_revente', u'bic', u'bnc']),
    label = u"Valeur locative des biens immobiliés possédés et non loués"))
