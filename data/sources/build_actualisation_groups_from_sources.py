# -*- coding:utf-8 -*-
# Created on 27 févr. 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)


from pandas import  HDFStore, ExcelFile
    
def build_actualisation_group_vars_h5():
    h5_name = "../actualisation_groups.h5"
    store = HDFStore(h5_name)
    xls = ExcelFile('actualisation_groups.xls')
    df = xls.parse('data', na_values=['NA'])
    store['vars'] = df
    print df.to_string()
    print store
    from numpy import unique
    coeff_list = sorted(unique(df['coeff'].dropna()))
    print coeff_list
    groups = {}
    for coeff in coeff_list:
        groups[coeff] = list(df[ df['coeff']==coeff ]['var'])
    print groups
    store.close()

def build_actualisation_group_names_h5():
    h5_name = "../actualisation_groups.h5"
    store = HDFStore(h5_name)
    xls = ExcelFile('actualisation_groups.xls')
    df = xls.parse('defs', na_values=['NA'])
    store['names'] = df
    print df.to_string()
    store.close()

def build_actualisation_group_amounts_h5():
    h5_name = "../actualisation_groups.h5"
    store = HDFStore(h5_name)
    xls = ExcelFile('actualisation_groups.xls')
    df_a = xls.parse('amounts', na_values=['NA'])
    df_a = df_a.set_index(['case'], drop= True)
    df_b = xls.parse('benef', na_values=['NA'])
    df_c = xls.parse('corresp', na_values=['NA'])
    store['amounts'] = df_a
    store['benef']   = df_b
    store['corresp'] = df_c
    print df_a.to_string()
    print df_a.columns
    store.close()

def build_actualisation_groups():
    build_actualisation_group_vars_h5()
    build_actualisation_group_names_h5()

if __name__ == '__main__':
    pass