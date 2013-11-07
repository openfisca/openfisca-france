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

#
## Menages et Individus
#
from src.countries.france.data.erf.datatable import DataCollection

from numpy import where
import gc

from numpy import nan 

from src.countries.france.data.erf.build_survey import save_temp, load_temp
import pdb
    
def create_indivim(year=2006):
    '''
    '''
    # load
    data = DataCollection(year=year)
    erfmen = data.get_values(table="erf_menage")
    eecmen = data.get_values(table="eec_menage")
    print sorted(eecmen.columns)
    
    erfind = data.get_values(table="erf_indivi")
    eecind = data.get_values(table="eec_indivi")
    print eecind.columns
    print erfind.columns   
    
    # travail sur la cohérence entre les bases
    noappar_m = eecmen[ ~(eecmen.ident.isin( erfmen.ident.values))]
    print 'describe noappar_m'
    print noappar_m.describe()     
        
    noappar_i = eecmen[ ~(eecmen.ident.isin( erfmen.ident.values))]
    noappar_i = noappar_i.drop_duplicates(cols='ident', take_last = True)
    #TODO: vérifier qu'il n'y a théoriquement pas de doublon

    dif = set(noappar_i.ident).symmetric_difference(noappar_m.ident)
    int = set(noappar_i.ident) & set(noappar_m.ident)
    print "dif, int --------------------------------"
    print dif, int
    del noappar_i, noappar_m, dif, int
    gc.collect()
        
    #fusion enquete emploi et source fiscale
    menagem = erfmen.merge(eecmen)
    indivim = eecind.merge(erfind, on = ['noindiv', 'ident', 'noi'], how="inner")

    # optimisation des types? Controle de l'existence en passant
    #TODO: minimal dtype
    var_list = (['acteu', 'stc', 'contra', 'titc', 'forter', 'mrec', 'rstg', 'retrai', 'lien', 'noicon', 
                 'noiper', 'noimer', 'naia', 'cohab', 'agepr', 'statut', 'txtppb', 'encadr', 'prosa'])
    for var in var_list:
        try:
            indivim[var] = indivim[var].astype("float32")
        except:
            print "%s is missing" %var
    
    # création de variables
    ## actrec
    indivim['actrec'] = 0
    #TODO: pas de 6 ?!!
    filter1 = (indivim['acteu'] == 1) & (indivim['stc'].isin([1,3]))
    indivim['actrec'][filter1] = 1
    filter2 = (indivim['acteu'] == 1) & (((indivim['stc'] == 2) & (indivim['contra'] == 1)) | (indivim['titc'] == 2))
    indivim['actrec'][filter2] = 2
    indivim['actrec'][indivim['acteu'] == 1] =  3
    filter4 = (indivim['acteu'] == 2) | ((indivim['acteu'] == 3) & (indivim['mrec'] == 1))
    indivim['actrec'][filter4] = 4
    filter5 = (indivim['acteu'] == 3) & ((indivim['forter'] == 2) | (indivim['rstg'] == 1))
    indivim['actrec'][filter5] = 5
    filter7 = (indivim['acteu'] == 3) & ((indivim['retrai'] == 1) | (indivim['retrai'] == 2))
    indivim['actrec'][filter7] = 7
    indivim['actrec'][indivim['acteu'] == 3] =  8
    indivim['actrec'][indivim['acteu'].isnull()] =  9
    print indivim['actrec'].value_counts()
    # tu99 
    if year == 2009:
        #erfind['tu99'] = None
        #eecind['tu99'] = float(eecind['tu99'])
        erfind['tu99'] = NaN   
        
    ## locataire
    menagem["locataire"] = menagem["so"].isin([3,4,5])
    menagem["locataire"] = menagem["locataire"].astype("int32")
    ## ?? c'est bizarre d'avoir besoin du diplome de la personne de référence,
    ## ce serait mieux de faire le merge quand on a besoin seulement
    ## laissons à la table individuel ce qui doit l'être
    
#    NOTE pas de ddipl en year=2006 visiblement
#    transfert = indivim.ix[indivim['lpr'] == 1, ['ident', 'ddipl']]
#    print transfert
#    #TODO: Forget not to uncomment 'dat
##     #menagem <- merge(erfmen,eecmen)
##     #menagem <- merge(menagem,transfert)
#    menagem  = menagem.merge(transfert)
    
    # correction
    def _manually_remove_errors():
        '''
        This method is here because some oddities can make it through the controls throughout the procedure
        It is here to remove all these individual errors that compromise the process.
        GL,HF
        '''
        
        if year==2006:
            indivim.lien[indivim.noindiv==603018905] = 2
            indivim.noimer[indivim.noindiv==603018905] = 1
            print indivim[indivim.noindiv==603018905].to_string()
            
    _manually_remove_errors()

    # save
    save_temp(menagem, name="menagem", year=year)
    del erfmen, eecmen, menagem #, transfert
    print 'menagem saved'
    gc.collect()
    save_temp(indivim, name="indivim", year=year)
    del erfind, eecind
    print 'indivim saved'
    gc.collect()

    

def create_enfnn(year=2006):
    '''
    '''
    #load
    data = DataCollection(year=year)
    ### Enfant à naître (NN pour nouveaux nés)
    individual_vars = ['noi', 'noicon', 'noindiv', 'noiper', 'noimer', 'ident', 'naia', 'naim', 'lien', 
               'acteu','stc','contra','titc','mrec','forter','rstg','retrai','lpr','cohab','sexe',
               'agepr','rga']
    data = DataCollection(year=year)
    eeccmp1 = data.get_values(table="eec_cmp_1", variables=individual_vars)
    eeccmp2 = data.get_values(table="eec_cmp_2", variables=individual_vars)
    eeccmp3 = data.get_values(table="eec_cmp_3", variables=individual_vars)
    tmp = eeccmp1.merge(eeccmp2, how="outer")
    enfnn = tmp.merge(eeccmp3, how="outer")

    # optimisation des types? Controle de l'existence en passant
    # pourquoi pas des int quand c'est possible
    #TODO: minimal dtype
    for var in individual_vars:
        print var
        enfnn[var] = enfnn[var].astype('float')
    del eeccmp1, eeccmp2, eeccmp3, individual_vars
 
    # création de variables   
    print enfnn.describe()
    enfnn['declar1'] = ''
    enfnn['noidec'] = 0
    enfnn['ztsai'] = 0
    enfnn['year'] = year
    enfnn['year'] = enfnn['year'].astype("float32") # -> integer ?
    enfnn['agepf'] = enfnn['year'] - enfnn['naia']
    enfnn['agepf'][enfnn['naim'] >= 7] -= 1 
    enfnn['actrec'] = 9
    enfnn['quelfic'] = 'ENF_NN'
    enfnn['persfip'] = ""
    
    #selection
    #enfnn <- enfnn[(enfnn$naia==enfnn$year & enfnn$naim>=10) | (enfnn$naia==enfnn$year+1 & enfnn$naim<=5),]
    enfnn = enfnn[((enfnn['naia'] == enfnn['year']) & (enfnn['naim'] >= 10)) | 
                      ((enfnn['naia'] == enfnn['year'] + 1) & (enfnn['naim'] <= 5))]
    #save
    save_temp(enfnn, name="enfnn", year=year)
    del enfnn
    print "enfnnm saved"
    gc.collect()
    
    
if __name__ == '__main__':
    print('Entering 01_pre_proc')
    import time
    deb = time.clock()
    year = 2006
    create_indivim()
    create_enfnn()
    print time.clock() - deb