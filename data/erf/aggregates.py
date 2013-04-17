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
    
    
def get_of2erf(year=None):
    of2erf = dict()
    of2erf["csg"] = "csgim"  # imposable, et "csgdm", déductible
#of2erf["csgd"] = "csgdm" 
    of2erf["crds"] = "crdsm"
    of2erf["irpp"] = "zimpom"
    of2erf["ppe"] = "m_ppem"
    of2erf["af"] =  "m_afm"
#af_base
#af_majo
#af_forf
    of2erf["cf"] = "m_cfm"
    of2erf["paje_base"] = "m_pajem"
    of2erf["paje_nais"] = "m_naism"
    of2erf["paje_clca"] = ""
    of2erf["paje_clmg"] = ""
    of2erf["ars"] = "m_arsm"
    of2erf["aeeh"] = "m_aesm" # allocation d'éducation spéciale
    of2erf["asf"] = "m_asfm"
    of2erf["aspa"] = "m_minvm"
    of2erf["aah"] = "m_aahm"
    of2erf["caah"] = "m_caahm"
    of2erf["rsa"] = "m_rmim"
    of2erf["rsa_act"] = ""
    of2erf["aefa"] = "m_crmim"
    of2erf["api"] = "m_apim"
    of2erf["logt"] = "logtm"
    of2erf["alf"] = "m_alfm"
    of2erf["als"] = "m_alsm"
    of2erf["apl"] = "m_aplm"
    return of2erf


if __name__ == '__main__':
    build_erf_aggregates()
