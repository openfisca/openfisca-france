# -*- coding:utf-8 -*-
# Created on 7 avr. 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)

from src.lib.simulation import SurveySimulation
from src.plugins.survey.aggregates import Aggregates
from src.countries.france.data.erf.datatable import DataCollection
from src.countries.france.data.erf import get_of2erf, get_erf2of
import numpy as np

def build_erf_aggregates(variables = None, year = 2006):
    """
    Fetch the relevant aggregates from erf data
    """
    country = 'france'         
    erf = DataCollection(year=year)
    if variables is not None and "wprm" not in variables:
        variables.append("wprm")
    print 'Fetching aggregates from erf %s data' %str(year)
    df = erf.get_of_values(variables=variables, table = "erf_menage")
    
#     print menage.columns
#     cols = []

    of2erf = get_of2erf()
    erf2of = get_erf2of()
#     for col in variables:
#         try:
#             erf_var = of2erf[col]
#         except:
#             print "coucouc"
#             erf_var = None
#         if erf_var in menage.columns:
# #                 print col, erf_var
#             cols += [erf_var]
#         else:
#             print col + " not found"
        
#     df = menage[cols]
    print df
    df.rename(columns = erf2of, inplace = True)
    wprm = df["wprm"]
    for col in df.columns:
        try:
            df[col] = df[col].astype(np.float64)
        except:
            pass
    df = df.mul(wprm, axis = 0)
    for col in list(set(df.columns) - set(['ident', 'wprm'])):
        try:
            df[col] = df[col].sum()/1e9
        except:
            pass
#             print col, tot
    return df.ix[0:1] # Aggregate so we only need 1 row
    
    


if __name__ == '__main__':
    df = build_erf_aggregates()
    print df.to_string()
