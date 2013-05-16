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
from src import SRC_PATH
from pandas import HDFStore

ERF_HDF5_DATA_DIR = os.path.join(SRC_PATH,'countries','france','data', 'erf')

class ErfsDataTable(object):
    """
    An object to acces variables int the ERFS datatables
    """
    def __init__(self, year = 2006):
        super(ErfsDataTable, self).__init__()
        self.year = year # year of the collected data
        self.tables = {}
        self.hdf5_filename = os.path.join(os.path.dirname(ERF_HDF5_DATA_DIR),'erf','erf.h5')
    
    def set_config(self, **kwargs):
        """
        Set configuration parameters
        
        Parameters
        ----------
        year : int, default None
               year of the survey
               
        """
        tables = {}

                
        if self.year is not None:        
            year = self.year
            menageXX = "menage" + str(year)[2:]
            erf_menageRdata = menageXX + ".Rdata"
            erf_filename = os.path.join(os.path.dirname(DATA_DIR),'R','erf', str(year), erf_menageRdata)
            rpy.r.load(erf_filename)
            erf_menage = com.load_data(menageXX)
            
            yr = str(year)[2:]
            eec_df_name = "mrf" + yr + "e" + yr + "t4"
            eec_menageRdata = eec_df_name + ".Rdata" 
            eec_filename = os.path.join(os.path.dirname(DATA_DIR),'R','erf', str(year), eec_menageRdata)
            rpy.r.load(eec_filename)
            eec_menage = com.load_data(eec_df_name)
            tables["menage"] = erf_menage.merge(eec_menage) 
            
            foyerXX = "foyer" + str(year)[2:]
            erf_foyerRdata = foyerXX + ".Rdata"
            erf_foyer_filename = os.path.join(os.path.dirname(DATA_DIR),'R','erf', str(year), erf_foyerRdata)
            rpy.r.load(erf_foyer_filename)
            erf_foyer = com.load_data(foyerXX)
            tables["foyer"] = erf_foyer
            
            indiviXX = "indivi" + str(year)[2:]
            erf_indiviRdata = indiviXX + ".Rdata"
            erf_indivi_filename = os.path.join(os.path.dirname(DATA_DIR),'R','erf', str(year), erf_indiviRdata)
            rpy.r.load(erf_indivi_filename)
            erf_indivi = com.load_data(indiviXX)
            tables["indivi"] = erf_indivi

                        
            store = HDFStore(self.hdf5_filename)
            for table in tables:
                store[str(self.year)+"/"+table] = tables[table]
            
            

    def get_value(self, variable, table=None):
        """
        Get value
        
        Parameters
        ----------
        variable : string
                  name of the variable
        table : string, default None          
                name of the table where to get variable
        Returns
        -------
        df : DataFrame, default None 
             A DataFrame containing the variable
        """
        df = self.get_values([variable], table)
        return df
        
    def set_tables(self):
        store = HDFStore(self.hdf5_filename)
        for table_path in store.keys():
            table = table_path[6:]
            self.tables[table] = store[table_path] 
        
    def get_values(self, variables, table=None):
        """
        Get values
        
        Parameters
        ----------
        variables : list of strings
                  list of variables names
        table : string, default None          
                name of the table where to get the variables
        Returns
        -------
        df : DataFrame, default None 
             A DataFrame containing the variables
        """
        
        if not self.tables:
            self.set_tables()
        from src.countries.france.data.erf import get_erf2of, get_of2erf
        of2erf = get_of2erf()
        to_be_renamed_variables = set(of2erf.keys()).intersection(variables)
        renamed_variables = []
        
        for variable in to_be_renamed_variables:
            renamed_variables.append(of2erf[variable])
        
        if renamed_variables:
            variables = list( set(variables).difference(to_be_renamed_variables)) + renamed_variables 
        
        if table is None:
            for test_table in self.tables.keys:
                if set(variables) < set(self.tables[test_table].columns):
                    table = test_table
                    print "using guessed table :", table
                    break
                
        if table is None:
            print "varname not found in any tables"
            df = None
        else:
            variables = list( set(variables).intersection(self.tables[table].columns))
            df = self.tables[table][variables]
        
        # rename variables according to their name in openfisca
        erf2of = get_erf2of()
        to_be_renamed_variables = set(erf2of.values()).intersection(variables)
        if to_be_renamed_variables:
            for var in to_be_renamed_variables:
                df.rename(columns = {var: erf2of[var]}, inplace=True)
        return df 

def test():
    erf = ErfsDataTable()
    # erf.set_config(year=2006)
    erf.set_tables() 
    df = erf.get_value("wprm", "menage")
    print df
    df = erf.get_values( ["typmen15", "nbinde", "af"], "menage")
    print df.head()
    
def build_foyer():
    from src.lib.simulation import SurveySimulation
    country = "france"
    yr = 2006
    simulation = SurveySimulation()
    simulation.set_config(year=yr, country = country)
    input_table = simulation.InputTable
    for col in input_table.columns:
        print col.name
        print col.entity
    
if __name__ == '__main__':
    test()
    # build_foyer()