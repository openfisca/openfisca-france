# -*- coding:utf-8 -*-
# Created on 27 févr. 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)


from pandas import  HDFStore, read_csv, ExcelFile, concat, DataFrame
import os

DATA_DIR = 'C:/Users/Utilisateur/Documents/Data/'


def csv2hdf5(csv_name, h5_name, dfname, option='frame'):
    table = read_csv(csv_name)
    store = HDFStore(h5_name)
    
    if option == 'frame':
        store.put(dfname, table)
    
    elif option == 'table': # for frame_table à la pytables
        object_cols =  table.dtypes[ table.dtypes == 'object']
        print object_cols.index
        try:
            store.append(dfname,table)
        except:
            print table.get_dtype_counts()
            object_cols =  table.dtypes[ table.dtypes == 'object']
            
            for col in object_cols.index:
                print 'removing object column :', col 
                del table[col] 
        
            store.append(dfname,table)
           
    print store
    store.close() 

def test(h5_name):
    store = HDFStore(h5_name)
    for key in store.keys():
        print key
    
    store.close()
    
        
def build_totals():
    h5_name = "../amounts.h5"
    store = HDFStore(h5_name)
    files = ['logement_tous_regime', 'openfisca_pfam_tous_regimes', 
             'minima_sociaux_tous_regimes', 'IRPP_PPE', 'cotisations_RegimeGeneral' ]
    first = True
    for xlsfile in files:
        xls = ExcelFile(xlsfile + '.xlsx')
        df_a = xls.parse('amounts', na_values=['NA'])
        try:
            df_b   = xls.parse('benef', na_values=['NA']) 
        except:
            df_b = DataFrame()

        if first:
            amounts_df = df_a
            benef_df =  df_b
            first = False
        else:
            amounts_df = concat([amounts_df, df_a])
            benef_df =  concat([benef_df, df_b])
    
    amounts_df, benef_df = amounts_df.set_index("var"), benef_df.set_index("var")
    print amounts_df.to_string()
    print benef_df.to_string()    
    store['amounts'] = amounts_df
    store['benef']   = benef_df
    store.close
    
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
    
    # test for duplicates
#    print df_a.to_string()
#    l = []
#    for x in list(df_a['case']): 
#        if x in l:
#            print x
#        else:
#            l.append(x)
        

    
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


def get_csv_file_name(year):
    
    os.path.dirname(DATA_DIR)
    R_DIR = os.path.join(os.path.dirname(DATA_DIR),'R','openfisca', str(year))
    yr = str(year)[2:]
    fname = os.path.join(R_DIR,"final"+ yr + ".csv")
    return fname


def build_survey_psl():
    year = 2006
    h5_name = '../survey_psl.h5'    
    dfname = 'survey_' + str(year)
    os.path.dirname(DATA_DIR)
    PSL_DIR = os.path.join(os.path.dirname(DATA_DIR),'PSL')
    csv_name = os.path.join(PSL_DIR,"psl_"+ str(year) + ".csv")
    print("Using " + csv_name + " to build " + h5_name)
    csv2hdf5(csv_name, h5_name, dfname)

def build_survey(year, option='frame'):
    h5_name = '../survey.h5'
    dfname = 'survey_' + str(year)
    csv_name = get_csv_file_name(year)
    print("Using " + csv_name + " to build " + h5_name)
    csv2hdf5(csv_name, h5_name, dfname, option=option)

def build_all_surveys( option = 'frame'):
    h5_name = '../survey.h5'    
    try:
        os.remove(h5_name)
    except:
        pass
    for year in range(2006,2010):
        build_survey(year, option=option)
        
def rebuild_all():    
    build_actualisation_group_amounts_h5()
    build_totals()
    build_all_surveys()


def debug():
    year = 2008
    h5_name = '../toto.h5'
    dfname = 'survey_2008'
    csv_name = get_csv_file_name(year)
    table = read_csv(csv_name)
    
    object_cols =  table.dtypes[ table.dtypes == 'object']
    
    print table.get_dtype_counts()
    
    for col in object_cols.index:
        del table[col] 
    
    print table.get_dtype_counts()

#    store = HDFStore(h5_name)
#    store.append(dfname,table)
#    print store


if __name__ == '__main__':

    build_all_surveys()