# -*- coding:utf-8 -*-
# Created on 7 avr. 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © #2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)


import os
#    Uses rpy2.
#    On MS Windows, The environment variable R_HOME and R_USER should be set
import pandas.rpy.common as com 
import rpy2.rpy_classic as rpy
rpy.set_default_mode(rpy.NO_CONVERSION)

from src.countries.france.data.sources.config import DATA_DIR


class ErfsDataTable(object):
    """
    An object to acces variables int the ERFS datatables
    """
    def __init__(self):
        super(ErfsDataTable, self).__init__()
        self.year = None # year of the collected data
        self.tables = {}
    
    
    def set_config(self, **kwargs):
        """
        Set configuration parameters
        
        Parameters
        ----------
        year : int, default None
               year of the survey
        """
        for key, val in kwargs.iteritems():
            if key == "year":
                self.year = val
                
        if self.year is not None:        
            year = self.year
            menageXX = "menage" + str(year)[2:]
            menageRdata = menageXX + ".Rdata"
            filename = os.path.join(os.path.dirname(DATA_DIR),'R','erf', str(year), menageRdata)
            rpy.r.load(filename)
            self.tables["menage"] = com.load_data(menageXX)

    def get_value(self, varname, table=None):
        """
        Get value
        
        Parameters
        ----------
        varname : string
                  name of the variable
        table : string, default None          
                name of the table where to get varname
        Returns
        -------
        df : DataFrame, default None 
             A DataFrame containing the variable
        """
        if table is None:
            for test_table in self.tables.keys:
                if varname in self.tables[test_table].columns:
                    table = test_table
                    break
                
        if table is None:
            print "varname not found in any tables"
            return None
        else:
            df = self.tables[table][varname]
            return df   
        
    def get_values(self, varnames, table=None):
        """
        Get value
        
        Parameters
        ----------
        varnames : list
                  list of variables names
        table : string, default None          
                name of the table where to get varname
        Returns
        -------
        df : DataFrame, default None 
             A DataFrame containing the variables
        """
        
        if table is None:
            for test_table in self.tables.keys:
                if set(varnames) < set(self.tables[test_table].columns):
                    table = test_table
                    break
                
        if table is None:
            print "varname not found in any tables"
            return
        else:
            return self.tables[table][varnames]


def test():
    
    erf = ErfsDataTable()
    erf.set_config(year=2006)
    df = erf.get_value("wprm", "menage")
    print df
    df = erf.get_values( ["wprm", "champm"], "menage")
    print df
    
if __name__ == '__main__':
    test()