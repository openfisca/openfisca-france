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

def build_erf_aggregates(variables, year):
    """
    Fetch the relevant aggregates from erf data
    """
    country = 'france'         
    erf = DataCollection(year=year)
    if "wprm" not in variables:
        variables.append("wprm")
    print 'Fetching aggregates from erf %s data' %str(year)
    menage = erf.get_of_values(variables=variables, table = "erf_menage")
    
    print menage.columns
    cols = []

    of2erf = get_of2erf()
    erf2of = get_erf2of()
    for col in variables:
        try:
            erf_var = of2erf[col]
        except:
            print "coucouc"
            erf_var = None
        if erf_var in menage.columns:
#                 print col, erf_var
            cols += [erf_var]
        else:
            print col + " not found"
        
    df = menage[cols]
    print df
    df.rename(columns = erf2of, inplace = True)
    wprm = menage["wprm"]
    for col in df.columns:
        df[col] = (df[col]*wprm).sum()/1e9
#             print col, tot
    return df
    
    


if __name__ == '__main__':
    # Doesnt work anymroe
    dfs = build_erf_aggregates()
    dfs[0] = dfs[0][:1]
    print dfs[0].to_string()
