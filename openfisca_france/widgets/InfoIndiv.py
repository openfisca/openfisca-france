# -*- coding: utf-8 -*-

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
