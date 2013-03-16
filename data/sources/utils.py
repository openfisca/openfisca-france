# -*- coding:utf-8 -*-
# Created on 27 févr. 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)

from pandas import  HDFStore, read_csv

def csv2hdf5(csv_name, h5_name, dfname, option='frame'):
    """
    Convert a csv file to a dataframe in a hdf5
    
    Parameters:
    
    csv_name: string
              csv file name
    h5_name : string
              hdf5 file name
    dfname  : string
              dataframe name
    option  : string, 'frame' or 'table', default to 'frame'
              stoing type in the pytable
    """
    
    table = read_csv(csv_name)
    store = HDFStore(h5_name)
    
    if option == 'frame':
        store.put(dfname, table)
    
    elif option == 'table': # for frame_table à la pytables
        object_cols =  table.dtypes[ table.dtypes == 'object']
        print object_cols.index
        try:
            store.append(dfname,table)
        except:
            print table.get_dtype_counts()
            object_cols =  table.dtypes[ table.dtypes == 'object']
            
            for col in object_cols.index:
                print 'removing object column :', col 
                del table[col] 
        
            store.append(dfname,table)
           
    print store
    store.close() 

def test_hdf5(h5_name):
    store = HDFStore(h5_name)
    for key in store.keys():
        print key
    
    store.close()
    
        
if __name__ == '__main__':
    pass