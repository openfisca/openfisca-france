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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from openfisca_core.columns import IntCol, FloatCol, BoolCol, EnumCol
from openfisca_qt.gui.qt.QtGui import QDockWidget
from openfisca_qt.gui.qthelpers import MyDoubleSpinBox, MyComboBox


class S:
    name = 0
    birth = 1
    decnum = 2
    decpos = 3
    decbtn = 4
    famnum = 5
    fampos = 6


def BoxFromCol(col):
    if col in [IntCol, FloatCol]:
        MyDoubleSpinBox(prefix = col.label)
    elif col in [EnumCol]:
        MyComboBox(prefix= col.label, choices = col.enum._vars.keys() )


class InfoIndivWidget(QDockWidget):
    def __init__(self, parent = None):
        super(InfoIndivWidget, self).__init__(parent)

        input_cols = []

#        for var in input_cols:
#            BoxFromCol() TODO: finish here
