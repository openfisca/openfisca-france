# -*- coding:utf-8 -*-
# Created on 27 févr. 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)


from pandas import  HDFStore, ExcelFile, concat, DataFrame
import os
from openfisca_core.simulations import SurveySimulation
from src.plugins.survey.aggregates import Aggregates

def test_h5():
    store = HDFStore("amounts.h5")
    df_a = store['amounts']
    df_b = store['benef']
    
    print df_a.to_string()
    print df_b.to_string() 
    store.close()
    
if __name__ == '__main__':
    test_h5()
    