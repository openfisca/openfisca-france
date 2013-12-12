# -*- coding:utf-8 -*-
# Created on 7 avr. 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © #2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)


import os
import gc
from src import SRC_PATH
from pandas import HDFStore
from src.countries.france.utils import check_consistency
#    Uses rpy2.
#    On MS Windows, The environment variable R_HOME and R_USER should be set

try:   
    import pandas.rpy.common as com 
    import rpy2.rpy_classic as rpy
    rpy.set_default_mode(rpy.NO_CONVERSION)
except:
    pass
from src.countries.france.data.sources.config import DATA_DIR

ERF_HDF5_DATA_DIR = os.path.join(SRC_PATH,'countries','france','data', 'erf')


class SurveyDescription(object):
    """
    An object to describe syrvey data
    """
    def __init__(self):
        self.survey_year = None
        self.tables = dict()


    def insert_table(self, name=None, **kwargs):
        """
        Insert a table in the SurveyDescription
        """
        if name not in self.tables.keys():
            self.tables[name] = dict()
        
        for key, val in kwargs.iteritems():
            if key in ["RData_dir", "RData_filename", "variables"]:
                    self.tables[name][key] = val 
        

class DataCollection(object):
    """
    An object to access variables in a collection of surveys
    """
    def __init__(self, year = 2006):
        super(DataCollection, self).__init__()
        self.year = year # year of the collected data
        self.surveys = {}
        self.hdf5_filename = os.path.join(os.path.dirname(ERF_HDF5_DATA_DIR),'erf','erf.h5')
    
    
    def initialize(self):
        """
        Initialize survey data 
        """

        self.initialize_erf(tables=tables)
#        self.initialize_logement()
        
    def initialize_erf(self, tables=None):
        """
        """

        year = self.year
        erf = SurveyDescription()
        yr = str(year)[2:]
        yr1 = str(year+1)[2:]
        erf_tables_to_process = {
#                                 "erf_menage" : "menage" + yr,
                                 "eec_menage" : "mrf" + yr + "e" + yr + "t4",
#                                  "foyer" : "foyer" + yr,
#                                   "erf_indivi" : "indivi" + yr,
                                "eec_indivi" : "irf" + yr + "e" + yr + "t4",
                                "eec_cmp_1" : "icomprf" + yr + "e" + yr1 + "t1",
                                "eec_cmp_2" : "icomprf" + yr + "e" + yr1 + "t2",
                                "eec_cmp_3" : "icomprf" + yr + "e" + yr1 + "t3"
                                }      
        RData_dir = os.path.join(os.path.dirname(DATA_DIR),'R','erf')
        
        variables = ['noi','noindiv','ident','declar1','quelfic','persfip','declar2','persfipd','wprm',
                     "zsali","zchoi","ztsai","zreti","zperi","zrsti","zalri","zrtoi","zragi","zrici","zrnci",
                     "zsalo","zchoo","ztsao","zreto","zpero","zrsto","zalro","zrtoo","zrago","zrico","zrnco"]

        variables_eec = ['noi','noicon','noindiv','noiper','noimer','ident','naia','naim','lien',
                       'acteu','stc','contra','titc','mrec','forter','rstg','retrai','lpr','cohab','sexe',
                       'agepr','rga','statut', 'txtppb', 'encadr', 'prosa', 'nbsala',  'chpub', 'dip11']
        
        variables_eec_rsa = [ "sp0" + str(i) for i in range(0,10)] + ["sp10", "sp11"] + ['sitant', 'adeben', 
                            'datant', 'raistp', 'amois', 'adfdap' , 'ancentr', 'ancchom', 'dimtyp', 'rabsp', 'raistp',
                             'rdem', 'ancinatm']
        
        variables_eec_aah = ["rc1rev", "maahe"]
        
        variables_eec += variables_eec_rsa + variables_eec_aah
             
        erf_tables = {
            "erf_menage" : {"RData_filename" :  "menage" + yr,
                            "variables" : None},
            "eec_menage" : {"RData_filename" :"mrf" + yr + "e" + yr + "t4",
                            "variables" : None},
            "foyer" :      {"RData_filename" :"foyer" + yr,
                            "variables" : None},
            "erf_indivi" : {"RData_filename" :"indivi" + yr,
                            "variables" : variables},
            "eec_indivi" : {"RData_filename" :"irf" + yr + "e" + yr + "t4",
                            "variables" : variables_eec},
            "eec_cmp_1" :  {"RData_filename" :"icomprf" + yr + "e" + yr1 + "t1",
                            "variables" : variables_eec},
            "eec_cmp_2" :  {"RData_filename" :"icomprf" + yr + "e" + yr1 + "t2",
                            "variables" : variables_eec},
            "eec_cmp_3" :  {"RData_filename" :"icomprf" + yr + "e" + yr1 + "t3",
                            "variables" : variables_eec}}

        RData_dir = os.path.join(os.path.dirname(DATA_DIR),'R','erf')
        
        if tables is None:
            erf_tables_to_process = erf_tables 
        else:
            erf_tables_to_process = tables 
            
        for name in erf_tables_to_process:                
            erf.insert_table(name=name, 
                             RData_filename=RData_filename,
                             RData_dir=RData_dir,
                             variables=variables)
        
        self.surveys["erf"] = erf
        
        
    def initialize_logement(self):
        """
        """
        year = self.year
        lgt = SurveyDescription()
        yr = str(year)[2:]
        yr1 = str(year+1)[2:]
        

        if yr=="03":
            lgt_men = "menage"
            lgt_logt = None
            renameidlgt  = dict(ident='ident')
            
        elif yr in ["06","07","08","09"]:
            lgt_men = "menage1"
            lgt_lgt = "logement"
            renameidlgt = dict(idlog='ident')
        
        lgt_tables_to_process = {"adresse" : "adresse",
                                 "lgt_menage" : lgt_men,
                                 "lgt_logt" : lgt_lgt}
        
        RData_dir = os.path.join(os.path.dirname(DATA_DIR),'R','logement')        
        for name, RData_filename in lgt_tables_to_process.iteritems():
            lgt.insert_table(name=name, 
                             RData_filename=RData_filename,
                             RData_dir=RData_dir)
    
        self.surveys["lgt"] = lgt
    
    
    def initialize_patrimoine(self, year):
        """
        TODO:
        """
        pat_tables_to_process = {"pat_individu" : "individu",
                                 "pat_menage" : "meange",
                                 "pat_produit" : "produit",
                                 "pat_transmission" : "transm"}
       
        pat_data_dir = os.path.join(os.path.dirname(DATA_DIR),'R','patrimoine')       
       
        pat = {"name" : "patrimoine",
               "data_dir" : os.path.join(os.path.dirname(DATA_DIR),'R','patrimoine'),
               "tables_to_process" : pat_tables_to_process}
       

    
    def set_config(self, **kwargs):
        """
        Set configuration parameters
        
        Parameters
        ----------
        year : int, default None
               year of the survey
        """
        if self.year is not None:        
            year = self.year
        else:
            raise Exception("year should be defined")
        
        store = HDFStore(self.hdf5_filename)
        for survey_name, description in self.surveys.iteritems():
            for destination_table_name, tables in description.tables.iteritems():  
                data_dir = tables["RData_dir"]
                R_table_name = tables["RData_filename"]
                try:
                    variables = tables["variables"]
                except:
                    variables = None
                print variables
                self.store_survey(survey_name, R_table_name, destination_table_name, data_dir, variables)

    def store_survey(self, survey_name, R_table_name, destination_table_name, data_dir, variables=None, force_recreation=True):
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
        data_dir : path
                   the directory where to find the RData file
        
        variables : list of string, default None
                    When not None, list of the variables to keep
        """         
        gc.collect()
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

        if variables is not None:

            print store
            print store_path
            print variables
            variables_stored = list(set(variables).intersection(set(stored_table.columns)))
            print list(set(variables).difference((set(stored_table.columns))))
            store[store_path] = stored_table[variables_stored]
        else:
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
        
        diff = set(variables) - set(df.columns)
        if diff:
            raise Exception("The following variable(s) %s are missing" %diff)
        variables = list( set(variables).intersection(df.columns))
        df = df[variables]
        
        return df


    def get_of_value(self, variable, table=None):
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
        df = self.get_of_values([variable], table)
        return df
        
        
    def get_of_values(self, variables=None, table=None):
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
    '''
    Validate check_consistency
    ''' 
    #===========================================================================
    # from pandas import DataFrame
    #res = DataFrame({af_col.name: simulation.output_table.get_value(af_col.name, af_col.entity)})
    # print res
    #===========================================================================
    
    store = HDFStore(os.path.join(os.path.dirname(os.path.join(SRC_PATH,'countries','france','data','erf')),'fichiertest.h5'))
    datatable = store.get('test12')
    test_simu = store.get('test_simu')
    print check_consistency(test_simu, datatable)
        
def test3():
    year=2006
    erf = DataCollection(year=year)
    df = erf.get_of_values(table = "eec_menage")
    from src.lib.simulation import SurveySimulation
    simulation = SurveySimulation()
    simulation.set_config(year=year)
    simulation.set_param()
    simulation.compute() # TODO: this should not be mandatory
    check_consistency(simulation.input_table, df)
        
def test_init():

    for year in range(2009,2010):
        data = DataCollection(year=year)
        data.initialize(tables=["eec_indivi"])
        data.set_config()
    
#def test_reading_stata_tables():
#    from pandas.io.stata import StataReader, read_stata # TODO: wait for the next release ...
#
#    filename = os.path.join(DATA_DIR,"erf","2006","Tables complémentaires","icomprf06e07t1.dta")
#    reader = StataReader(filename)
#    print reader.data()
    
if __name__ == '__main__':
#     test3()
    test_init()
    hdf5_filename = os.path.join(os.path.dirname(ERF_HDF5_DATA_DIR),'erf','erf.h5')
    print hdf5_filename
    store = HDFStore(hdf5_filename)
    print store
#     
#     hdf5_filename = os.path.join(os.path.dirname(ERF_HDF5_DATA_DIR),'erf','erf_old.h5')
#     print hdf5_filename
#     store = HDFStore(hdf5_filename)
#     print store 