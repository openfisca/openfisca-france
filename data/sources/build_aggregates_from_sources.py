# -*- coding:utf-8 -*-
# Created on 27 févr. 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)


from pandas import  HDFStore, ExcelFile, concat, DataFrame
import os
from src.lib.simulation import SurveySimulation
from src.plugins.survey.aggregates import Aggregates



def build_totals():
    h5_name = "../amounts.h5"
    store = HDFStore(h5_name)
    files = ['logement_tous_regime', 'pfam_tous_regimes', 
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
    


    
def test():
    country = "france"
    for year in range(2006,2007):
 
        yr = str(year)
        simu = SurveySimulation()
        simu.set_config(year = yr, country = country)
        simu.set_param()
    
        agg = Aggregates()
        agg.set_simulation(simu)
 
        for col in agg.varlist:
            print col

if __name__ == '__main__':
    test()