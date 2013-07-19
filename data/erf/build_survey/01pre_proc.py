# -*- coding:utf-8 -*-
# Created on 16 mai 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)
## OpenFisca
## Merge individu and menage tables from eec and erf, keeping all observations 
## erf tables are a subset of eec tables (no observation in erf not in eec)
## and adding some variables at the menage table that may be useful later on (ddip,lpr)
#
## Prepare the some useful merged tables
#
print('Entering 01_pre_proc')
#
## Menages et Individus
#
from src.countries.france.data.erf.datatable import DataCollection

from numpy import where
import gc

from numpy import logical_not as not_
from numpy import logical_and as and_
from numpy import logical_or as or_
from numpy import nan

from src.countries.france.data.erf.build_survey import save_temp, load_temp

    
def create_indivim(year=2006):
    
    data = DataCollection(year=year)
    erfmen = data.get_values(table="erf_menage")
    eecmen = data.get_values(table="eec_menage")
    
    print sorted(eecmen.columns)
    eecmen["locataire"] = eecmen["so"].isin([3,4,5])
    eecmen["locataire"] = eecmen["locataire"].astype("int32")
    noappar_m = eecmen[ not_(eecmen.ident.isin( erfmen.ident.values))]
    print 'describe noappar_m'
    print noappar_m.describe() 

    erfind = data.get_values(table="erf_indivi")
    eecind = data.get_values(table="eec_indivi")
    print eecind.columns
    print erfind.columns

    transfert = eecind[eecind['lpr'] == 1]
    transfert = transfert.ix[:, ['ident', 'ddipl']]
    print transfert
    
    #noappar_i <- eecind[!eecind$noindiv %in%  erfind$noindiv,]
    #noappar_i <- noappar_i[!duplicated(noappar_i$ident),]
    noappar_i = eecmen[ not_(eecmen.ident.isin( erfmen.ident.values))]
    
    noappar_i = noappar_i.drop_duplicates(cols='ident', take_last = True)
    #TODO: vérifier qu'il n'y a théoriquement pas de doublon

    
    dif = set(noappar_i.ident).symmetric_difference(noappar_m.ident)
    int = set(noappar_i.ident) & set(noappar_m.ident)
    print "dif, int --------------------------------"
    print dif, int
    
    del noappar_i, noappar_m, dif, int
    gc.collect()
    
    #TODO: Forget not to uncomment 'dat
#     #menagem <- merge(erfmen,eecmen)
#     #menagem <- merge(menagem,transfert)
    menagem = erfmen.merge(eecmen)
    menagem  = menagem.merge(transfert)

    save_temp(menagem, name="menagem", year=year)
    del erfmen, eecmen, menagem, transfert
    print 'menagem saved'
    gc.collect()
    
    if year == 2009:
        #erfind['tu99'] = None
        #eecind['tu99'] = float(eecind['tu99'])
        erfind['tu99'] = NaN
    
    #indivim <- merge(eecind,erfind, by = c("noindiv","ident","noi"))
    indivim = eecind.merge(erfind, on = ['noindiv', 'ident', 'noi'], how="outer")
    

    var_list = (['acteu', 'stc', 'contra', 'titc', 'forter', 'mrec', 'rstg', 'retrai', 'lien', 'noicon', 
                 'noiper', 'noimer', 'naia', 'cohab', 'agepr', 'statut', 'txtppb', 'encadr', 'prosa'])
    
    for var in var_list:
        try:
            indivim[var] = indivim[var].astype("float32")
        except:
            print "%s is missing" %var
    
    
    indivim['actrec'] = 0
    indivim['actrec'] = where(indivim['acteu'] == 1, 3, indivim['actrec'])
    indivim['actrec'] = where(indivim['acteu'] == 3, 8, indivim['actrec'])
    
    filter1 = and_(indivim['acteu'] == 1, or_(indivim['stc'] == 1, indivim['stc'] == 3))
    indivim['actrec'] = where(filter1, 1, indivim['actrec'])
    
    filter2 = and_(indivim['acteu'] == 1, or_(and_(indivim['stc'] == 2, indivim['contra'] == 1), 
                                              indivim['titc'] == 2))
    indivim['actrec'] = where(filter2, 2, indivim['actrec'])
    
    filter3 = or_(indivim['acteu'] == 2, and_(indivim['acteu'] == 3, indivim['mrec'] == 1))
    indivim['actrec'] = where(filter3, 4, indivim['actrec'])
    
    filter4 = and_(indivim['acteu'] == 3, or_(indivim['forter'] == 2, indivim['rstg'] == 1))
    indivim['actrec'] = where(filter4, 5, indivim['actrec'])
    
    filter5 = and_(indivim['acteu'] == 2, (indivim.retrai.isin([1,2])))
    indivim['actrec'] = where(filter5, 7, indivim['actrec'])
    indivim['actrec'] = where(indivim['acteu'].isnull(), 9, indivim['actrec'])
    
    save_temp(indivim, name="indivim", year=year)
    del erfind, eecind, indivim
    print 'indivim saved'
    gc.collect()

    

def create_enfnn(year=2006):
    data = DataCollection(year=year)
    
    ### Enfant à naître (NN pour nouveaux nés)

    individual_vars = ['noi', 'noicon', 'noindiv', 'noiper', 'noimer', 'ident', 'naia', 'naim', 'lien', 
               'acteu','stc','contra','titc','mrec','forter','rstg','retrai','lpr','cohab','sexe',
               'agepr','rga']
    
    #enfnn <- rbind(eeccmp1,eeccmp2,eeccmp3)
    
    data = DataCollection(year=year)
    eeccmp1 = data.get_values(table="eec_cmp_1", variables=individual_vars)
    eeccmp2 = data.get_values(table="eec_cmp_2", variables=individual_vars)
    eeccmp3 = data.get_values(table="eec_cmp_3", variables=individual_vars)
    tmp = eeccmp1.merge(eeccmp2, how="outer")
    enfnn = tmp.merge(eeccmp3, how="outer")


    for var in individual_vars:
        print var
        enfnn[var] = enfnn[var].astype('float')
    del eeccmp1, eeccmp2, eeccmp3, individual_vars
    
    print enfnn.describe()
    enfnn['declar1'] = ''
    enfnn['noidec'] = 0
    enfnn['ztsai'] = 0
    enfnn['year'] = year
    enfnn['year'] = enfnn['year'].astype("float32")
    enfnn['agepf'] = where(enfnn['naim'] < 7, enfnn['year'] - enfnn['naia'], 
                           enfnn['year'] - enfnn['naia'] - 1) 
    enfnn['actrec'] = 9
    enfnn['quelfic'] = 'ENF_NN'
    enfnn['persfip'] = ""
    
    #enfnn <- enfnn[(enfnn$naia==enfnn$year & enfnn$naim>=10) | (enfnn$naia==enfnn$year+1 & enfnn$naim<=5),]
    enfnn = enfnn[or_(and_(enfnn['naia'] == enfnn['year'], enfnn['naim'] >= 10), 
                      and_(enfnn['naia'] == enfnn['year'] + 1, enfnn['naim'] <= 5) )]
    save_temp(enfnn, name="enfnn", year=year)

    del enfnn
    print "enfnnm saved"
    gc.collect()
    
def manually_remove_errors(year=2006):
    '''
    This method is here because some oddities can make it through the controls throughout the procedure
    It is here to remove all these individual errors that compromise the process.
    GL,HF
    '''
    
    if year==2006:
        indivim = load_temp(name="indivim", year=year)
        indivim.lien[indivim.noindiv==603018905] = 2
        indivim.noimer[indivim.noindiv==603018905] = 1
        print indivim[indivim.noindiv==603018905].to_string()
        save_temp(indivim, name="indivim", year=year)
    
if __name__ == '__main__':
    year = 2006
    create_indivim()
    create_enfnn()
    manually_remove_errors(year=year)
