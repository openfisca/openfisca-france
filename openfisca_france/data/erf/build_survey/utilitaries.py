# -*- coding:utf-8 -*-
# Created on 10 juin 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul, Jérôme Santoul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)
# # # OpenFisca

from pandas import DataFrame, concat

def assert_variable_inrange(name, wrange, table): 
    '''
    Assert if transformed variables are in correct range
    wrange is a list like [minimum, maximum]
    '''
    temp = (table[table[name].notnull()])
    range_1 = wrange[0]
    range_2 = wrange[1]
    for v in temp[name]:
        assert v in range(range_1, range_2), Exception('some non-null values for %s not in wanted %s: %s' %(name, str(wrange), str(v)))
        
def count_NA(name,table): 
    '''Counts the number of Na's in a specified axis'''
    print "count of NA's for %s is %s" %(name, str(sum(table[name].isnull())))

def print_id(df):
    try:
        print "Individus : ", len(df.noindiv), "/", len(df)
    except:
        print "No noindiv"
  
    try:
        # Ici, il doit y avoir autant de vous que d'idfoy
        print "Foyers", len(df.idfoy)
        print df["quifoy"].value_counts()
        if df["idfoy"].isnull().any():        
            print "NaN in idfoy : ", df["idfoy"].isnull().sum()
        if df["quifoy"].isnull().any():        
            print "NaN in quifoy : ", df["quifoy"].isnull().sum() 
    except:
        print "No idfoy or quifoy"
         
    try:
        # Ici, il doit y avoir autant de quimen = 0 que d'idmen
        print "Ménages", len(df.idmen)
        print df["quimen"].value_counts()
        if df["idmen"].isnull().any():        
            print "NaN in idmen : ", df["idmen"].isnull().sum()
        if df["quimen"].isnull().any():        
            print "NaN in quimen : ", df["quimen"].isnull().sum()
    except:
        print "No idmen or quimen"
  
    try:
        # Ici, il doit y avoir autant de quifam = 0 que d'idfam
        print "Familles", len(df.idfam)
        print df["quifam"].value_counts()
        if df["idfam"].isnull().any():        
            print "NaN in idfam : ", df["idfam"].isnull().sum()
        if df["quifam"].isnull().any():        
            print "NaN in quifam : ", df["quifam"].isnull().sum()
    except:
        print "No idfam or quifam"


def control(dataframe, verbose=False, verbose_columns=None, debug=False, verbose_length=5, ignore=None):
    """
    Function to help debugging the data crunchin' files.
    
    Parameters
    ---------
    verbose: Default False
    Indicates whether to print the dataframe itself or just perform reguler checks.
    
    verbose_columns: List
    The columns of the dataframe to print
    
    verbose_length: Int
    the number of rows to print
    """
    std_list = ['idfoy', 'quifoy', 'idmen', 'quimen', 'idfam', 'quifam']
    for var in std_list: 
        try:
            assert var in dataframe.columns
        except:
            raise Exception('the dataframe does not contain the required column %s' %(var))
        
    print 'longueur de la data frame =', len(dataframe.index)
    if debug: 
        print 'nb de doublons', len(dataframe[dataframe.duplicated()])
        print 'nb de doublons idfoy/quifoy', len(dataframe[dataframe.duplicated(cols=['idfoy', 'quifoy'])])
        print 'nb de doublons idmen/quimen', len(dataframe[dataframe.duplicated(cols=['idmen', 'quimen'])])
        print 'nb de doublons idfam/quifam', len(dataframe[dataframe.duplicated(cols=['idfam', 'quifam'])])
        
    if not(debug): 
        assert not(dataframe.duplicated().any()), 'présence de lignes en double dans la dataframe'
        assert ~(dataframe.duplicated(cols=['idfoy', 'quifoy'])).all(), 'duplicate of tuple idfoy/quifoy' 
        assert ~(dataframe.duplicated(cols=['idmen', 'quimen'])).all(), 'duplicate of tuple idmen/quimen'
        assert ~(dataframe.duplicated(cols=['idfam', 'quifam'])).all(), 'duplicate of tupli idfam/quifam'

    empty_columns = []
    for col in dataframe.columns:
        if (dataframe[col].isnull().all()): 
                empty_columns.append(col)
                
    if empty_columns != []: print 'liste des colonnes entièrement vides', empty_columns
    
    if verbose is True:
        print '------ informations détaillées -------'
        print_id(dataframe)
        
        if verbose_columns is None:
#             print dataframe.head(verbose_length) 
            if dataframe.duplicated().any():
                print dataframe[dataframe.duplicated()].head(verbose_length).to_string()


        else : 
            if dataframe.duplicated(verbose_columns).any():
                print 'nb lignes lignes dupliquées_____', len(dataframe[dataframe.duplicated(verbose_columns)])
                print dataframe.loc[:, verbose_columns].describe()
            for col in verbose_columns:
                print 'nombre de NaN dans %s : ' %(col), dataframe[col].isnull().sum()
            print 'colonnes contrôlées ------>', verbose_columns
    print 'vérifications terminées'


def check_structure(df):

    dup = df.noindiv.duplicated().sum()
    if dup > 1:
        print "there are %s duplicated individuals" %dup
        df.drop_duplicates("noindiv", inplace=True)
    
    for entity in ["men", "fam", "foy"]:
        print entity
        qui = 'qui' + entity
        id  = 'id' + entity
    
        if df[qui].isnull().any():
            print "there are NaN in qui%s" %entity
        
        max_entity = df[qui].max().astype("int")
        for position in range(0, max_entity+1):
            test = df[[ qui, id]].groupby(by=id).agg(lambda x: (x==position).sum()) 
            errors = (test[qui] > 1).sum()
            if errors > 0:
                print "There are %s duplicated qui%s = %s" %(errors,entity,position)
        
    
    
