# -*- coding:utf-8 -*-
# Created on 7 avr. 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)


from src.countries.france.data.erf.datatable import DataCollection
from src.countries.france.data.erf import get_of2erf, get_erf2of
import numpy as np

def build_erf_aggregates(variables = None, year = 2006, unit = 1e6):
    """
    Fetch the relevant aggregates from erf data
    """

    erf = DataCollection(year=year)
    if variables is not None and "wprm" not in variables:
        variables.append("wprm")
    print 'Fetching aggregates from erf %s data' %str(year)
    df = erf.get_of_values(variables=variables, table = "erf_menage")

    of2erf = get_of2erf()
    erf2of = get_erf2of()

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
            df[col] = df[col].sum()/1e6
        except:
            pass

    return df.ix[0:1] # Aggregate so we only need 1 row
    
    


if __name__ == '__main__':
    df = build_erf_aggregates()
    print df.to_string()
