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


from ...base import *  # noqa analysis:ignore


build_column('alr', IntCol(label = u"Pensions alimentaires perçues",
               val_type = "monetary",
               cerfa_field = {QUIFOY['vous']: u"1AO",
                              QUIFOY['conj']: u"1BO",
                              QUIFOY['pac1']: u"1CO",
                              QUIFOY['pac2']: u"1DO",
                              QUIFOY['pac3']: u"1EO",
                              }))  # (f1ao, f1bo, f1co, f1do, f1eo)
build_column('alr_decl', BoolCol(label = u"Pension déclarée", default = True))
