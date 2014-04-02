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


from . import  data1, data2, data3, data4, data5, data6, data7, data8, data_survey

column_by_name = data1.column_by_name.copy()

for col_by_name in [
    data2.column_by_name,
    data3.column_by_name,
    data4.column_by_name,
    data5.column_by_name,
    data6.column_by_name,
    data7.column_by_name,
    data8.column_by_name,
    data_survey.column_by_name,
    ]:

    column_by_name.update(col_by_name)
