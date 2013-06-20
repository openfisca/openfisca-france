# -*- coding:utf-8 -*-
# Created on 20 juin 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul, Jérôme Santoul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)

from __future__ import division
from numpy import where, NaN, random, logical_or as or_ 
from src.countries.france.data.erf.build_survey import show_temp, load_temp, save_temp
from src.countries.france.data.erf.build_survey.utilitaries import print_id, control, check_structure
from numpy import logical_and as and_
from pandas import read_csv, HDFStore
from src.countries.france import DATA_SOURCES_DIR
import os


def final_check(year=2006):
    test_filename = os.path.join(DATA_SOURCES_DIR,"test.h5") 
    store = HDFStore(test_filename)
    final2 = store.get('survey_2006')
    age_data = final2['age'].value_counts().reset_index()
    age_data = age_data.sort_index(by='index', ascending='True')
    print age_data.to_string()

    pass



if __name__ == '__main__':
    final_check()
