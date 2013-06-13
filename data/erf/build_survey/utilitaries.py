# -*- coding:utf-8 -*-
# Created on 10 juin 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul, Jérôme Santoul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)
# # # OpenFisca

from pandas import DataFrame, concat


def control(dataframe, verbose=False, verbose_columns=None, verbose_length=5):
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
    for col in dataframe.columns:
        assert not(dataframe[col].isnull().all()), 'la colonne %s est vide' %(col)
    print 'présence de doublons dans la dataframe ?', (dataframe.duplicated().any())
    print 'vérifications terminées'
    
    if verbose is True:
        print '------ informations détaillées -------'
        if dataframe.duplicated().any()==True:
            print 'lignes dupliquées_____'
            print dataframe[dataframe.duplicated()].head()
        if verbose_columns is None:
            print 'dataframe________'
            print dataframe.head(verbose_length)
        else:
            print 'colonnes contrôlées', verbose_columns
            for col in verbose_columns:
                print col
                print dataframe[col].head(verbose_length)



def print_id(df):
    print "Individus : ", len(df.noindiv), "/", len(df)
  
    try:
        # Ici, il doit y avoir autant de vous que d'idfoy
        print "Foyers", len(df.idfoy)
        print df["quifoy"].value_counts()
    except:
        print "No idfoy or quifoy"
         
    try:
        # Ici, il doit y avoir autant de quimen = 0 que d'idmen
        print "Ménages", len(df.idmen)
        print df["quimen"].value_counts()
    except:
        print "No idmen or quimen"
  
    try:
        # Ici, il doit y avoir autant de quifam = 0 que d'idfam
        print "Familles", len(df.idfam)
        print df["quifam"].value_counts()
    except:
        print "No idfam or quifam"
