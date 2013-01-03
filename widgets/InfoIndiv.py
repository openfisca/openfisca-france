# -*- coding:utf-8 -*-
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

"""
openFisca, Logiciel libre de simulation du système socio-fiscal français
Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

This file is part of openFisca.

    openFisca is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    openFisca is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with openFisca.  If not, see <http://www.gnu.org/licenses/>.
"""

from src.qt.QtGui import (QDockWidget)




from src.core.columns import IntCol, FloatCol, BoolCol, EnumCol

class S:
    name = 0
    birth = 1
    decnum = 2
    decpos = 3
    decbtn = 4
    famnum = 5
    fampos = 6

from src.core.qthelpers import MyDoubleSpinBox, MyComboBox

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
        