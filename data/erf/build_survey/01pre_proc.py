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

from src.countries.france.data.erf.build_survey import save_temp, load_temp

    
def create_indivim(year=2006):
    
    data = DataCollection(year=year)
    #erfmen <- LoadIn(erfMenFil)
    erfmen = data.get_values(table="erf_menage")
    
    #eecmen <- LoadIn(eecMenFil)
    eecmen = data.get_values(table="eec_menage")
    #
    #eecmen$locataire <- ifelse(eecmen$so %in% c(3,4,5),1,0)
    eecmen["locataire"] = eecmen["so"].isin([3,4,5])
    eecmen["locataire"] = eecmen["locataire"].astype("int32")
#    print eecmen["locataire"].dtype
#    print eecmen["locataire"].describe()
    

    #noappar_m <- eecmen[!eecmen$ident %in%  erfmen$ident,]
    noappar_m = eecmen[ not_(eecmen.ident.isin( erfmen.ident.values))]
    print 'describe noappar_m'
    print noappar_m.describe() 

    #
    #erfind <- LoadIn(erfIndFil)
    #eecind <- LoadIn(eecIndFil)
    erfind = data.get_values(table="erf_indivi")
    print 'describe erfind & eecind'
    print erfind.columns
    eecind = data.get_values(table="eec_indivi")
    print eecind.columns

    #transfert <- subset(eecind, lpr==1, select=c("ident","ddipl"))
    transfert = eecind[eecind['lpr'] == 1]
    transfert = transfert.ix[:, ['ident', 'ddipl']]
    print transfert
    
    #noappar_i <- eecind[!eecind$noindiv %in%  erfind$noindiv,]
    #noappar_i <- noappar_i[!duplicated(noappar_i$ident),]
    noappar_i = eecmen[ not_(eecmen.ident.isin( erfmen.ident.values))]
    
#     print eecind.describe() 
    print noappar_i.head()
    print "-----------------------------------------"
    noappar_i = noappar_i.drop_duplicates(cols='ident', take_last = True)
    #TODO: vérifier qu'il n'y a théoriquement pas de doublon
#     print noappar_i

    
    # Vérification que les non-appariés sont les mêmes pour les tables individus 
    # et les tables ménages
    #dif <- setdiff(noappar_i$ident,noappar_m$ident)
    #int <- intersect(noappar_i$ident,noappar_m$ident)
    dif = set(noappar_i.ident).symmetric_difference(noappar_m.ident)
    int = set(noappar_i.ident) & set(noappar_m.ident)
    print "dif, int --------------------------------"
    print dif, int
    
    #str(dif);str(int)
    #rm(noappar_i,noappar_m,dif,int)
    #rm(noappar_i, noappar_m, dif, int)
    del noappar_i, noappar_m, dif, int
    gc.collect()
    
    #TODO: Forget not to uncomment 'dat
#     #menagem <- merge(erfmen,eecmen)
#     #menagem <- merge(menagem,transfert)
    menagem = erfmen.merge(eecmen)
    menagem  = menagem.merge(transfert)
    print "#################################################"
    print menagem
#     
# 
#     #save(menagem,file=menm)
    save_temp(menagem, name="menagem", year=year)
    
#     #rm(erfmen,eecmen,menagem,transfert)
#     #message('menagem saved')
#     #gc()
    del erfmen, eecmen, menagem, transfert
    print 'menagem saved'
    gc.collect()
    
    # int = intersect(names(erfind),names(eecind))
#     int = erfind.columns & eecind.columns
#     print int

    ## Uncomparable tu99 in 2009 ! TODO: remove tu99 in one of them 
    #if (year == 2009){
    #  erfind$tu99 <- NULL
    #  eecind$tu99 <- as.numeric(eecind$tu99)
    #}
    if year == 2009:
        erfind['tu99'] = None
        eecind['tu99'] = float(eecind['tu99'])
    
    #indivim <- merge(eecind,erfind, by = c("noindiv","ident","noi"))
    indivim = eecind.merge(erfind, on = ['noindiv', 'ident', 'noi'], how="outer")
    

    # On recode l'activité de la semaine de référence'
    # actrec:
    #   1: actif occupé non salarié
    #   2: salarié pour une durée non limitée
    #   3: contrat à durée déterminée, intérim, apprentissage, saisonnier
    #   4: chômeur
    #   5: élève, étudiant, stagiaire non rémunéré
    #   6:
    #   7: retraité, préretraité, retiré des affaires
    #   8: autre inactif
    #   9: non renseign?
    # Voir guide méthodo ERFS 2006 page 84
    # TODO: 2003 voir guide méthodo page 170 
    #
    #var_list <- c("acteu", "stc", "contra", "titc", "forter", "mrec", "rstg", "retrai","lien",
    #              "noicon", "noiper", "noimer", "naia", "cohab", "agepr","statut","txtppb",'encadr','prosa')
    var_list = (['acteu', 'stc', 'contra', 'titc', 'forter', 'mrec', 'rstg', 'retrai', 'lien', 'noicon', 
                 'noiper', 'noimer', 'naia', 'cohab', 'agepr', 'statut', 'txtppb', 'encadr', 'prosa'])
    
    #for (var in var_list) {
    #  print(var)
    #  indivim[,var] <- as.numeric(indivim[,var])
    #}
    for var in var_list:
        try:
            indivim[var] = indivim[var].astype("float32")
        except:
            print "%s is missing" %var
    #indivim <- within(indivim,{
    #  actrec <- 0
    #  actrec[which(acteu==1)]             <- 3
    #  actrec[which(acteu==3)]             <- 8
    #  actrec[which(acteu==1 & (stc==1 | stc==3))]                <- 1  
    #  actrec[which(acteu==1 & ((stc==2 & contra==1) | titc==2))] <- 2
    #  actrec[which(acteu==2 | (acteu==3 & mrec==1))]             <- 4 
    #  actrec[which(acteu==3 & (forter==2 | rstg==1))]            <- 5 
    #  actrec[which(acteu==3 & (retrai %in% c(1,2)))]             <- 7 
    #  actrec[which(is.na(actrec))]  <-9 
    #})
    
    indivim['actrec'] = 0
    indivim['actrec'] = where(indivim['acteu'] == 1, 3, indivim['actrec'])
    indivim['actrec'] = where(indivim['acteu'] == 3, 8, indivim['actrec'])
    
    filter1 = and_(indivim['acteu'] == 1, or_(indivim['stc'] == 1, indivim['stc'] == 3))
    indivim['actrec'] = where(filter1 is True, 1, indivim['actrec'])
    
    filter2 = and_(indivim['acteu'] == 1, or_(and_(indivim['stc'] == 2, indivim['contra'] == 1), 
                                              indivim['titc'] == 2))
    indivim['actrec'] = where(filter2 is True, 2, indivim['actrec'])
    
    filter3 = or_(indivim['acteu'] == 2, and_(indivim['acteu'] == 3, indivim['mrec'] == 1))
    indivim['actrec'] = where(filter3 is True, 4, indivim['actrec'])
    
    filter4 = and_(indivim['acteu'] == 3, or_(indivim['forter'] == 2, indivim['rstg'] == 1))
    indivim['actrec'] = where(filter4 is True, 5, indivim['actrec'])
    
    filter5 = and_(indivim['acteu'] == 2, (indivim.retrai.isin([1,2])))
    indivim['actrec'] = where(filter5 is True, 7, indivim['actrec'])
    indivim['actrec'] = where(indivim['acteu'] is None, 9, indivim['actrec'])

    #save(indivim,file=indm)
    #rm(erfind,eecind,indivim)    
    #message('indivim saved')
    #gc()
    
    save_temp(indivim, name="indivim", year=year)
#    store2 = HDFStore('indm.h5')
#    store2.put('indivim', indivim)
    del erfind, eecind, indivim
    print 'indivim saved'
    gc.collect()


def create_enfnn(year=2006):
    data = DataCollection(year=year)
    
    ### Enfant à naître (NN pour nouveaux nés)

    #indVar = c('noi','noicon','noindiv','noiper','noimer','ident','naia','naim','lien','acteu','stc','contra','titc','mrec',
    #           'forter','rstg','retrai','lpr','cohab','sexe','agepr','rga')
    individual_vars = ['noi', 'noicon', 'noindiv', 'noiper', 'noimer', 'ident', 'naia', 'naim', 'lien', 
               'acteu','stc','contra','titc','mrec','forter','rstg','retrai','lpr','cohab','sexe',
               'agepr','rga']
    
    #eeccmp1 <- LoadIn(eecCmp1Fil,indVar)
    #eeccmp2 <- LoadIn(eecCmp2Fil,indVar)
    #eeccmp3 <- LoadIn(eecCmp3Fil,indVar)
    #enfnn <- rbind(eeccmp1,eeccmp2,eeccmp3)
    
    data = DataCollection(year=year)
    eeccmp1 = data.get_values(table="eec_cmp_1", variables=individual_vars)
    eeccmp2 = data.get_values(table="eec_cmp_2", variables=individual_vars)
    eeccmp3 = data.get_values(table="eec_cmp_3", variables=individual_vars)
    tmp = eeccmp1.merge(eeccmp2, how="outer")
    enfnn = tmp.merge(eeccmp3, how="outer")

    #for (var in indVar) {
    #  print(var)
    #  enfnn[,var] <- as.numeric(enfnn[,var])
    #}

    for var in individual_vars:
        print var
        enfnn[var] = enfnn[var].astype('float')
    #rm(eeccmp1,eeccmp2,eeccmp3,var_list)
    del eeccmp1, eeccmp2, eeccmp3, individual_vars
    
    #enfnn <- within(enfnn,{
    #  declar1 <- ''
    #  noidec <- 0
    #  ztsai <- 0 
    #  year <- as.numeric(year)
    #  agepf <- ifelse(naim < 7,year-naia,year-naia-1)
    #  actrec <- 9
    #  quelfic <- "ENF_NN"
    #  persfip <- ""
    #})

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
    print enfnn.describe()
    #save(enfnn,file=enfnnm)
    #rm(enfnn)
    #message('enfnnm saved')
    #gc()
    save_temp(enfnn, name="enfnn", year=year)

#    store_enfnnm = HDFStore('enfnnm.h5')
#    store_enfnnm.put('enfnnm.h5', enfnn)
    del enfnn
    print "enfnnm saved"
    gc.collect()
    
if __name__ == '__main__':
    create_indivim()
    create_enfnn()
