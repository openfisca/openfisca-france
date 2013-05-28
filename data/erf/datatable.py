# -*- coding:utf-8 -*-
# Created on 7 avr. 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © #2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)


import os
import gc
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
    
    def get_survey_list(self, year):
        """
        Return a list of survey information stored in a dictionary
        """
        yr = str(year)[2:]
        yr1 = str(year+1)[2:]
        
        erf_tables_to_process = {#"erf_menage" : "menage" + yr,
#                                 "eec_menage" : "mrf" + yr + "e" + yr + "t4",
#                                 "foyer" : "foyer" + yr,
#                                 "erf_indivi" : "indivi" + yr,
#                                 "eec_indivi" : "irf" + yr + "e" + yr + "t4",
                                 "eec_cmp_1" : "icomprf" + yr + "e" + yr1 + "t1",
#                                 "eec_cmp_2" : "icomprf" + yr + "e" + yr1 + "t2",
#                                 "eec_cmp_3" : "icomprf" + yr + "e" + yr1 + "t3"
                                 }
       
        erf = {"name" : "erf",
               "data_dir" : os.path.join(os.path.dirname(DATA_DIR),'R','erf'),
               "tables_to_process" : erf_tables_to_process} 
        
        ## LOGEMENT
        lgt_data_dir = os.path.join(os.path.dirname(DATA_DIR),'R','logement')
        if yr=="03":
            year_lgt = 2003
            lgt_men = "menage"
            lgt_logt = None
            renameidlgt  = dict(ident='ident')
            
        elif yr in ["06","07","08","09"]:
            year_lgt = 2006
            lgt_men = "menage1"
            lgt_lgt = "logement"
            renameidlgt = dict(idlog='ident')
        
        lgt_tables_to_process = {"adresse" : "adresse",
                                 "lgt_menage" : lgt_men,
                                 "lgt_logt" : lgt_lgt,
                                 }
        
        lgt = {"name" : "logement", 
               "data_dir" : lgt_data_dir,
               "tables_to_process" : lgt_tables_to_process}

        # Enquête Patrimoine
        pat_tables_to_process = {"pat_individu" : "individu",
                                 "pat_menage" : "meange",
                                 "pat_produit" : "produit",
                                 "pat_transmission" : "transm"}
       
        pat_data_dir = os.path.join(os.path.dirname(DATA_DIR),'R','patrimoine')       
       
        pat = {"name" : "patrimoine",
               "data_dir" : os.path.join(os.path.dirname(DATA_DIR),'R','patrimoine'),
               "tables_to_process" : pat_tables_to_process}
        
        survey_list = [ erf] #, lgt]  # TODO: prepare RData files for patrimoine
        
        return survey_list

    
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
        else:
            raise Exception("year should be defined")
        
        survey_list = self.get_survey_list(year)
        store = HDFStore(self.hdf5_filename)
        print store
        for survey in survey_list:
            survey_name = survey["name"]
            data_dir = survey["data_dir"]
            tables_to_process = survey["tables_to_process"]
            for destination_table_name, R_table_name in tables_to_process.iteritems(): 
                self.store_survey(survey_name, R_table_name, destination_table_name, data_dir)

    def store_survey(self, survey_name, R_table_name, destination_table_name, data_dir, force_recreation=True):
        """
        Store a R data table in an HDF5 file
        
        Parameters
        ----------

        survey_name : string
                       the name of the survey 
        R_table_name : string
                       the name of the R data table
        destination_table_name : string
                                 the name of the table in the HDFStore
        data_dir : 
        """

        year = self.year
        def get_survey_year(survey_name, year):
            if survey_name == "logement":
                if year == 2003:
                    return 2003
                elif year in range(2006,2010):
                    return 2006
            if survey_name == "patrimoine":
                return 2004
            else:
                return year
            
        print "creating %s" %(destination_table_name) 
        table_Rdata = R_table_name + ".Rdata"
        filename = os.path.join(data_dir, str(get_survey_year(survey_name, year)), table_Rdata)
        print filename
        if not os.path.isfile(filename):
            raise Exception("filename do  not exists")
        
        rpy.r.load(filename)
        stored_table = com.load_data(R_table_name)
        store = HDFStore(self.hdf5_filename)
        store_path = str(self.year)+"/"+destination_table_name
        
        if store_path in store:
            if force_recreation is not True:
                print store_path + "already exists, do not re-create and exit"
                store.close()
            return
  
        store[store_path] = stored_table
        store.close()
        del stored_table
        gc.collect()


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
        store.close() 
        
    def get_values(self, variables=None, table=None):
        """
        Get values
        
        Parameters
        ----------
        variables : list of strings, default None
                  list of variables names, if None return the whole table
        table : string, default None          
                name of the table where to get the variables
        Returns
        -------
        df : DataFrame, default None 
             A DataFrame containing the variables
        """

        store = HDFStore(self.hdf5_filename)
        df = store[str(self.year)+"/"+table]
        # If no variables read the whole table
        if variables is None:
            return df
            
        
        from src.countries.france.data.erf import get_erf2of, get_of2erf
        of2erf = get_of2erf()
        to_be_renamed_variables = set(of2erf.keys()).intersection(variables)
        renamed_variables = []
        
        for variable in to_be_renamed_variables:
            renamed_variables.append(of2erf[variable])
        
        if renamed_variables:
            variables = list( set(variables).difference(to_be_renamed_variables)) + renamed_variables 
        
#        if table is None:
#            for test_table in self.tables.keys:
#                if set(variables) < set(self.tables[test_table].columns):
#                    table = test_table
#                    print "using guessed table :", table
#                    break
#                
#        if table is None:
#            print "varname not found in any tables"
#            df = None
#        else:
        variables = list( set(variables).intersection(df.columns))
        df = df[variables]
        
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
    

def test_set_config():
    for year in range(2006,2007):
        erf = ErfsDataTable(year=year)
        erf.set_config()
        del erf
    
    
def test_reading_stata_tables():
    from pandas.io.stata import StataReader, read_stata # TODO: wait for the next release ...

    filename = os.path.join(DATA_DIR,"erf","2006","Tables complémentaires","icomprf06e07t1.dta")
    reader = StataReader(filename)
    print reader.data()
    
if __name__ == '__main__':
    # test_set_config()
    # build_foyer()
    test_reading_stata_tables()