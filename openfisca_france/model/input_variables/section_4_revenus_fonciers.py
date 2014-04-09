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
import datetime

from openfisca_core.columns import IntCol

from base import build_column_couple


column_by_name = collections.OrderedDict((
    # Revenus fonciers
    build_column_couple('f4ba', IntCol(entity = 'foy',
                    label = u"Revenus fonciers imposables",
                    val_type = "monetary",
                    cerfa_field = u'4BA')),

    build_column_couple('f4bb', IntCol(entity = 'foy',
                    label = u"Déficit imputable sur les revenus fonciers",
                    val_type = "monetary",
                    cerfa_field = u'4BB')),

    build_column_couple('f4bc', IntCol(entity = 'foy',
                    label = u"Déficit imputable sur le revenu global",
                    val_type = "monetary",
                    cerfa_field = u'4BC')),

    build_column_couple('f4bd', IntCol(entity = 'foy',
                    label = u"Déficits antérieurs non encore imputés",
                    val_type = "monetary",
                    cerfa_field = u'4BD')),

    build_column_couple('f4be', IntCol(entity = 'foy',
                    label = u"Micro foncier: recettes brutes sans abattement",
                    val_type = "monetary",
                    cerfa_field = u'4BE')),

    # Prime d'assurance loyers impayés
    build_column_couple('f4bf', IntCol(entity = 'foy',
                    label = u"Primes d'assurance pour loyers impayés des locations conventionnées",
                    val_type = "monetary",
                    cerfa_field = u'4BF')),

    build_column_couple('f4bl', IntCol(entity = 'foy', label = u"", end = datetime.date(2009, 12, 31))),  # TODO: cf 2010 2011

    ))
