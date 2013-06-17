# -*- coding:utf-8 -*-
# Created on 10 juin 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul, Jérôme Santoul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)
# # # OpenFisca

from pandas import DataFrame, concat


def control(dataframe, verbose=False, verbose_columns=None, verbose_length=5, debug=False):
    """
    Function to help debugging the data crunchin' files.
    
    Parameters
    ---------
    verbose: Default False
    Indicates whether to print the dataframe itself or just perform reguler checks.
    
    verbose_columns: List or String
    The columns of the dataframe to print
    
    verbose_length: Int
    the number of rows to print
    """
    
    print 'longueur de la data frame =', len(dataframe.index)
    if debug and (dataframe.duplicated().any()) : 
        print 'Attention : présence de doublons dans la dataframe'
        print 'nb de doublons', len(dataframe[dataframe.duplicated()])
    if not(debug): assert not(dataframe.duplicated().any()), 'présence de lignes en double dans la dataframe'

    empty_columns = []
    for col in dataframe.columns:
        if debug:
            if (dataframe[col].isnull().all()): 
                print 'la colonne %s est vide' %(col)
                empty_columns.append(col)
        else:
            assert not(dataframe[col].isnull().all()), 'la colonne %s est vide' %(col)
    if empty_columns != []: print empty_columns
    print 'vérifications terminées'
    
    if verbose is True:
        print '------ informations détaillées -------'
            
        if verbose_columns is None:
#             print dataframe.head(verbose_length) 
            if dataframe.duplicated().any():
                print dataframe[dataframe.duplicated()].head(verbose_length).to_string()

        else : 
            if dataframe.duplicated(verbose_columns).any():
                print 'nb lignes lignes dupliquées_____', len(dataframe[dataframe.duplicated(verbose_columns)])
                print dataframe[dataframe.duplicated(verbose_columns)].head(verbose_length).to_string()
            print 'colonnes contrôlées ------>', verbose_columns


def check_structure(df):
    print "autant de vous que d'idfoy", (len(df.noindiv)==len(df.index))
    print "autant de quimen = 0 que d'idmen", len(df.idmen)==df["quimen"].value_counts()
    print "autant de quifam = 0 que d'idfam", len(df.idfam)==df["quifam"].value_counts()

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
