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

from src.countries.france.data.sources.config import DATA_DIR

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
    

def build_erf_aggregates():
    """
    Fetch the relevant aggregates from erf data
    """
#    Uses rpy2.
#    On MS Windows, The environment variable R_HOME and R_USER should be set
    import pandas.rpy.common as com 
    import rpy2.rpy_classic as rpy
    rpy.set_default_mode(rpy.NO_CONVERSION)
    
    country = 'france'
    for year in range(2006,2010):
        menageXX = "menage" + str(year)[2:]
        menageRdata = menageXX + ".Rdata"
        filename = os.path.join(os.path.dirname(DATA_DIR),'R','erf', str(year), menageRdata)
        yr = str(year)
        simu = SurveySimulation()
        simu.set_config(year = yr, country = country)
        simu.set_param()
    
        agg = Aggregates()
        agg.set_simulation(simu)
        # print agg.varlist
        rpy.r.load(filename)

        menage = com.load_data(menageXX)
        cols = []
        print year
        for col in agg.varlist:
            #print col
            erf_var = "m_" + col + "m" 
            if erf_var in menage.columns:
                cols += [erf_var] 

        df = menage[cols]
        wprm = menage["wprm"]
        for col in df.columns:
            
            tot = (df[col]*wprm).sum()/1e9
            print col, tot
    



if __name__ == '__main__':
    pass