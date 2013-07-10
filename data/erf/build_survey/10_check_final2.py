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
    survey_filename = os.path.join(DATA_SOURCES_DIR,"survey.h5")
     
    store = HDFStore(test_filename)
    survey = HDFStore(survey_filename)
    
    final2 = store.get('survey_2006')
    print survey
    finalT = survey.get('survey_2006')
    
    varlist = ['anref', 'sitant', 'adeben', 'stc', 'retrai', 'contra', 'datant', 'rabs', 'nondic', 'TXTPPB',
               'ancrech', 'RAISTP', 'amois', 'adfdap', 'ancentr', 'anciatm', 'ancchom', 'ident', 'noi', 'dimtyp',
               'RABSP', 'raistp', 'rdem', 'sp10', 'sp11', 'idfoy']
    
    for i in range(0,10):
        varname = 'sp0' + str(i)
        varlist.append(varname)
    
    varlist = set(varlist)
    columns = final2.columns ; 
    columns = set(columns)
    
    print varlist.difference(columns)
    
#     print final2
#     print finalT
# #     control(final2, debug=True, verbose=True, verbose_columns=['idfam', 'quifam'])
# #     control(finalT, debug=True, verbose=True, verbose_columns=['idfam', 'quifam'])
#     print 'FAMILLE--------------'
#     print final2.quifam.value_counts()
#     print finalT.quifam.value_counts()
#     print ''
#     print 'FOYER------------------'
#     print final2.quifoy.value_counts()
#     print finalT.quifoy.value_counts()
#     print ''
#     print 'MENAGES-----------------'
#     print final2.quimen.value_counts()
#     print finalT.quimen.value_counts()
#     
#     print ''
#     print final2.age.describe()
#     print finalT.age.describe()
# #     age_data = final2['age'].value_counts().reset_index()
# #     age_data = age_data.sort_index(by='index', ascending='True')
# #     print age_data.to_string()
# #     print final2.loc[final2['quifam']==2, ['quifam', 'age']].describe()

    return



if __name__ == '__main__':
    final_check()
