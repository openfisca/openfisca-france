'''
Created on Nov 29, 2012

@author: Utilisateur
'''

from pandas import HDFStore, Series, DataFrame
from numpy import nan
from numpy.random import randn


def test():
    store = HDFStore('survey.h5')
    print store
    df = store['survey_2006']
#    density = dict()
#    print df.dtypes
#    df2 = df.to_sparse(fill_value=0)
#    print df2.density
    n = 0
    for col in df.columns:
        try:
            #print type(df[col])
            x = DataFrame(df[col])
            x = x.to_sparse(fill_value=0)
            if (x.density < .001):
                n +=1  
                df[col] = df[col].to_sparse(fill_value=0)
                print col
                print df[col].density
                DataFrame().to
        except:
            pass
    print n
#    for col in df.columns:
#        x = df[col]
#        print x
    store.close()



def test_doc():
    
    ts = Series(randn(10))
    ts[2:-2] = nan
    sts = ts.to_sparse()
    print sts
    print sts.density

def test_doc2():

    df = DataFrame(randn(10000, 4))
    df.ix[:9998] = 0
    sdf = df.to_sparse(fill_value=0)
    print sdf
    print sdf.index
    print sdf[1].density

    ts = Series({'x' :randn(10)})
    ts[2:-2] = nan
    sts = ts.fillna(0).to_sparse(fill_value=0)
    print sts.index
    sts = sts.reindex()
    print sts.density
    print sts._sparse
    
if __name__ == '__main__':
    from pandas import version
    print version.version
    test_doc2()