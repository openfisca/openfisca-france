'''
Created on Nov 29, 2012

@author: Utilisateur
'''

from pandas import HDFStore, Series, DataFrame
from numpy import nan
from numpy.random import randn


def test():
    store = HDFStore('survey_old.h5')
    print store
    df = store['survey_2006']
    density = dict()
    df2 = df.to_sparse(fill_value=0)
    print df2.density
#    for col in df.columns:
#        print col
#        x = DataFrame(df[col])
#        x = x.to_sparse(fill_value=0)
#        print x
#        print x.density
    store.close()

def test_doc():
    
    ts = Series(randn(10))
    ts[2:-2] = nan
    sts = ts.to_sparse()
    print sts
    print sts.density
    
    print ts.fillna(0).to_sparse(fill_value=0).density
    df = DataFrame(randn(10000, 4))
    df.ix[:9998] = nan
    sdf = df.to_sparse()
    print sdf
    print sdf.density

if __name__ == '__main__':
     
    test()