# -*- coding:utf-8 -*-
# Created on 7 avr. 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)

from src.lib.simulation import SurveySimulation
from src.plugins.survey.aggregates import Aggregates
from src.countries.france.data.erf.datatable import ErfsDataTable
from src.countries.france.data.erf import get_of2erf

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

        yr = str(year)
        simu = SurveySimulation()
        simu.set_config(year = yr, country = country)
        simu.set_param()
    
        agg = Aggregates()
        agg.set_simulation(simu)

        erf = ErfsDataTable()
        erf.set_config(year=year)
        menage = erf.tables["menage"]

        print menage.columns
        cols = []
        print year

        of2erf = get_of2erf()
        for col in agg.varlist:
            try:
                erf_var = of2erf[col]
            except:
                erf_var = None
            if erf_var in menage.columns:
                print col, erf_var
                cols += [erf_var]
            else:
                print col + " not found"
            
        df = menage[cols]
        wprm = menage["wprm"]
        for col in df.columns:
            
            tot = (df[col]*wprm).sum()/1e9
            print col, tot
    
    


if __name__ == '__main__':
    build_erf_aggregates()
