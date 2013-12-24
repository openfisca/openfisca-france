'''
Created on Nov 29, 2012

@author: Utilisateur
'''

from pandas import HDFStore, Series, DataFrame
from numpy import nan
from numpy.random import randn


def test():
    import gc
    gc.collect()
    from pandas import concat
    store = HDFStore('survey.h5')
    print store.root.survey_2006.table
    df = store.select('survey_2006', columns = 'sali')

    #print DataFrame(df.dtypes).describe()
    sparsified = None
    other = None
    i = 0
    print df.columns
    columns = df.columns.copy()
#    print columns
    return
    
    for colname in columns:
        if i > 10:
            break
        print colname
        col =  df.pop(colname)
        if col.dtype.kind in ['i', 'f']:
            sparsified_col = DataFrame(col).to_sparse(fill_value=0)
            if sparsified_col.density < .1:
                if sparsified is not None:
                    sparsified = concat([sparsified, sparsified_col])
                else:
                    sparsified = sparsified_col
            else:
                if other is not None:
                    other = concat([other, DataFrame(col)], axis = 1)
                else:
                    other = DataFrame(col)
        else:
            if other is not None:
                other = concat([other, DataFrame(col)], axis = 1)
            else:
                other = DataFrame(col)
        gc.collect()
        print i
        i += 1

#    print sparsified.describe()
#
#    print other.describe()
    store.close()


def test2():
    import gc
    gc.collect()
    print 'starting'
    store = HDFStore('survey.h5','r')
    print store
    df = store.select('survey_2006', columns = ['sali'])
    print df
    store.close()

if __name__ == '__main__':
#    from pandas import version
#    print version.version
    test2()