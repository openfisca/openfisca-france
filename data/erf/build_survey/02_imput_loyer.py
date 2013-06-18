# -*- coding:utf-8 -*-
# Created on 21 mai 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)


from __future__ import division
from src.countries.france.data.erf.datatable import DataCollection
from src.countries.france.data.erf.build_survey import show_temp, load_temp, save_temp
from src.countries.france.data.erf.build_survey.utilitaries import control
from pandas import DataFrame
from numpy import array, where, NaN
from pandas import concat
import gc
import math
from numpy import logical_not as not_, logical_and as and_
#===============================================================================
# # Openfisca
# # Rent imputation for renters from regression on 'enquête logement'
# # Adds a variable 'loym' to the 'menagem' table
# 
# message('Entering 02_imput_loyer')
# message('Building comparable tables')
def create_imput_loyer(year):
    
    
# message('Building comparable tables')
# ## Variable used for imputation
# if (yr == '08'){ # tau99 is not present
#   menmVars <- c("ztsam","zperm","zragm","zricm","zrncm","zracm","nb_uci","wprm",
#                 "so","nbpiec","typmen5","spr","nbenfc","agpr","cstotpr","nat28pr","tu99","aai1",'ident',"pol99","reg")
# } else {
#   menmVars <- c("ztsam","zperm","zragm","zricm","zrncm","zracm","nb_uci","wprm",
#               "so","nbpiec","typmen5","spr","nbenfc","agpr","cstotpr","nat28pr","tu99","aai1",'ident',"pol99","reg","tau99")
# }
# indmVars <- c("noi",'ident',"lpr","dip11") # TODO check as.numeric
# lgtAdrVars <- c("gzc2")
# lgtMenVars <- c("sec1","mrcho","mrret","mrsal","mrtns","mdiplo","mtybd","magtr","mcs8","maa1at","qex","muc1")
# if (yr=="03"){
# lgtMenVars <- c(lgtMenVars,"typse","lmlm","hnph2","mnatior","ident")
# lgtAdrVars <- c(lgtAdrVars,"iaat","tu99","ident")
# }
# if (yr %in% c("06", "07", "08", "09")){
# lgtMenVars <- c(lgtMenVars,"mnatio","idlog")
# lgtAdrVars <- c(lgtAdrVars,"idlog")  # pas de typse en 2006
# lgtLgtVars <- c("lmlm","iaat","tu99","hnph2","idlog")  # pas de typse en 2006
# }    
#     

# TODO:
# - Garder le code R, c'est plus facile pour débugguer
# - Ne pas garder les camelCase et mettre des espaces autour des " = " et après les ", ". 
# - En général essayer de se conformer au coding style rules énoncées ici: http://www.python.org/dev/peps/pep-0008/
# - Mettre des espaces pour aérer ton code
# - Rajouter des assert pour vérifier certaiens étapes (demander à Jérôme)

    #Variables used for imputation
    df = DataCollection(year=year)
    print 'Démarrer 02_imput_loyer'
    if year == 2008: # Tau99 not present
        menm_vars=["ztsam", "zperm", "zragm", "zricm", "zrncm", "zracm", "nb_uci", "wprm",
                 "so", "nbpiec", "typmen5", "spr", "nbenfc", "agpr", "cstotpr",
                 "nat28pr", "tu99", "aai1", 'ident', "pol99", "reg"]
    else:
        menm_vars = ["ztsam","zperm","zragm","zricm","zrncm","zracm","nb_uci","wprm",
                 "so","nbpiec","typmen5","spr","nbenfc","agpr","cstotpr","nat28pr","tu99","aai1",'ident',"pol99","reg","tau99"]
    
    indm_vars = ["noi",'ident',"lpr","dip11"]
    LgtAdrVars = ["gzc2"]
    LgtMenVars = ["sec1","mrcho","mrret","mrsal","mrtns","mdiplo","mtybd","magtr","mcs8","maa1at","qex","muc1"]
    
    if year == 2003:
        LgtMenVars.extend(["typse","lmlm","hnph2","mnatior","ident"])
        LgtAdrVars.extend(["iaat","tu99","ident"])
    if year < 2010 and year > 2005:
        LgtMenVars.extend(["mnatio","idlog"])
        LgtAdrVars.extend(["idlog"]) # pas de typse en 2006
        LgtLgtVars=["lmlm","iaat","tu99","hnph2","idlog"] # pas de typse en 2006
    
    print year
#===============================================================================
# ## Travail sur la base ERF
# ## -----------------------
# # Table menage
# message("preparing erf menage table")
# menmVars
# erfmenm <- LoadIn(menm, menmVars)
# erfmenm <- within(erfmenm,{
#   revtot <- ztsam+zperm+zragm+zricm+zrncm+zracm
#   nvpr <- revtot/nb_uci
#   logt <- as.factor(so)
#   })
#   # Table individu
# message("preparing erf individu table")
# erfindm <- LoadIn(eecIndFil, indmVars)
# erfindm <- subset(erfindm,lpr==1,select=c(ident,dip11))
#===============================================================================
    #Preparing ERF menages tables
    print show_temp()
    erfmenm = load_temp(name="menagem",year=year) 
    #df.get_values(table="erfmenm",variables=menmVars)
    erfmenm['revtot'] = (erfmenm['ztsam'] + erfmenm['zperm'] + erfmenm['zragm'] + 
                         erfmenm['zricm'] + erfmenm['zrncm'] + erfmenm['zracm'])
    erfmenm['nvpr'] = erfmenm['revtot'] / erfmenm['nb_uci']
    erfmenm['logt']= erfmenm['so']
    #Preparing ERF individuals table
    erfindm = load_temp(name="indivim",year=year) #variables=indmVars)
    print 'ident' in erfindm.columns
    print 'dip11' in erfindm.columns
    print erfindm
#    erfindm=erfindm[['ident', 'dip11']][erfindm['lpr']==1]
    erfindm = erfindm[['ident', 'dip11']][erfindm['lpr']==1]
    print erfindm
    return
#===============================================================================
# '''# Merge
# message("merging erf menage and individu")
# erf <- merge(erfmenm, erfindm, by ="ident")
# rm(erfmenm,erfindm) # Pour remove un objet
# 
# message("compute quantiles")
# dec <- wtd.quantile(erf$nvpr,weights=erf$wprm,probs=c(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1))
# erf$deci <-  as.factor((1 + (erf$nvpr>=dec[2]) + (erf$nvpr>=dec[3])
#                          + (erf$nvpr>=dec[4]) + (erf$nvpr>=dec[5])
#                          + (erf$nvpr>=dec[6]) + (erf$nvpr>=dec[7])
#                          + (erf$nvpr>=dec[8]) + (erf$nvpr>=dec[9])
#                          + (erf$nvpr>=dec[10])))
# 
# rm(dec)'''
#===============================================================================
    #Merging ERF menages and individuals
    erf = erfmenm.merge(erfindm, on='ident')
    #Compute quantiles
    # TODO : quantiles voir dans l'import ci dessous le lien pour comprendre comment le
    # calcul de quantiles fonctionne
    from src.lib.utils import mark_weighted_percentiles 
#===============================================================================
# '''message("recode variable for imputation")
# erf <- subset(erf, so %in% c(3,4,5),
#                select=c(ident,ztsam,zperm,zragm,zricm,zrncm,zracm,
#                  nb_uci,logt,nbpiec,typmen5,spr,nbenfc,agpr,cstotpr,
#                  nat28pr,tu99,aai1,wprm,nvpr,revtot,dip11,deci))
# 
# erf <- upData(erf, rename=c(nbpiec='hnph2',nat28pr='mnatio',aai1='iaat',
#                      dip11='mdiplo'))
    erf=erf[['ident','ztsam','zperm','zragm','zricm','zrncm','zracm',
                 'nb_uci','logt','nbpiec','typmen5','spr','nbenfc','agpr','cstotpr',
                 'nat28pr','tu99','aai1','wprm','nvpr','revtot','dip11','deci']][erf['so'] < 6 and erf['so'] > 2]

    DataFrame().rename(columns={'nbpiec':'hnph2'}) 
    # TODO: utiliser rename
    # TODO: ne traite pas les types comme dans R teste-les pour voir comment pandas les gère 
    for col in erf.columns: # Sorte de rename, pas sûr que ça marche
        if col=='nbpiec':
            col='hnph2'
        if col=='nat28pr':
            col='mnatio'
        if col=='aai1':
            col='iaat'
        if col=='dip11':
            col='mdiplo'
    erf['agpr']=int(erf['agpr'])
    erf['tmp']=3
    if erf['agpr'] < 65:
        erf['tmp']=2
    if erf['agpr'] < 40:
        erf['tmp']=1
    erf['magtr']=erf['tmp']
    erf['mcs8']=math.floor(erf['cstotpr']/10)
    if erf['mcs8'] == 0:
        erf['mcs8']=NaN # Il y a donc 1+4 NAs
        
# erf$agpr <- as.integer(erf$agpr)
# 
# erf$tmp <- 3
# 
# erf$tmp[erf$agpr < 65] <- 2
# erf$tmp[erf$agpr < 40] <- 1
# erf$magtr <- as.factor(erf$tmp)
# 
# erf$mcs8 <- floor(as.integer(erf$cstotpr)/10)
# erf$mcs8[erf$mcs8==0] <- NA  # un mcs8=0 est transform? en NA : il y en a donc 1+4 NA's
    erf['mtybd']=NaN
    erf['mtybd'][erf['typmen5']==1 and erf['spr'] != 2]=1
    erf['mtybd'][erf['typmen5']==1 and erf['spr'] == 2]=2
    erf['mtybd'][erf['typmen5']==5]=3
    erf['mtybd'][erf['typmen5']==3]=7
    erf['mtybd'][erf['nbenfc']==1]=4
    erf['mtybd'][erf['nbenfc']==2]=5
    erf['mtybd'][erf['nbenfc']>=3]=6
# 
# erf$mtybd <- NA
# erf$mtybd[(erf$typmen5==1) & (erf$spr!=2)] <- 1
# erf$mtybd[(erf$typmen5==1) & (erf$spr==2)] <- 2
# erf$mtybd[erf$typmen5==5]          <- 3
# erf$mtybd[erf$typmen5==3]          <- 7
# erf$mtybd[erf$nbenfc ==1]          <- 4
# erf$mtybd[erf$nbenfc ==2]          <- 5
# erf$mtybd[erf$nbenfc >=3]          <- 6
# erf$mtybd <- as.factor(erf$mtybd)  # TODO il reste 41 NA's 2003

    erf['hnph2'][erf['hnph2']<1]=1
    erf['hnph2'][erf['hnph2']>=6]=6
# erf$hnph2[erf$hnph2 < 1] <- 1 # 3 logements ont 0 pi?ces !!
# erf$hnph2[erf$hnph2 >=6] <- 6
    '''pas compris...'''
# # table(erf$hnph2, useNA="ifany")
# # TODO: il reste un NA 2003
# #       il rest un NA en 2008
# erf$hnph2 <- as.factor(erf$hnph2)
    tmp=erf['mnatio']
    tmp[erf['mnatio'] ==10]=1
    tmp[erf['mnatio'] in [11,12,13,14,15,21,22,23,24,25,26,27,28,29,31,32,41,42,43,44,45,46,47,48,51,52,62,60]]=2
    erf['mnatio']=tmp
# tmp <- erf$mnatio
# tmp[erf$mnatio %in% c(10)] <- 1
# tmp[erf$mnatio %in% c(11,12,13,14,15,21,22,23,24,25,26,27,28,29,31,32,41,42,43,44,45,46,47,48,51,52,62,60)] <- 2  
# erf$mnatio <- as.factor(tmp)
    tmp=erf['iaat']
    tmp[erf['mnatio'] in [1,2,3]]=1
    tmp[erf['mnatio'] ==4]=2
    tmp[erf['mnatio'] ==5]=3
    tmp[erf['mnatio'] ==6]=4
    tmp[erf['mnatio'] ==7]=5
    tmp[erf['mnatio'] ==8]=6
    erf['iaat']=tmp
# tmp <- erf$iaat
# tmp[erf$iaat %in% c(1,2,3)] <- 1
# tmp[erf$iaat %in% c(4)] <- 2
# tmp[erf$iaat %in% c(5)] <- 3
# tmp[erf$iaat %in% c(6)] <- 4
# tmp[erf$iaat %in% c(7)] <- 5
# tmp[erf$iaat %in% c(8)] <- 6
# # TODO: comparer logement et erf pour ?tre sur que cela colle
# # Il reste un NA en 2003
# #    reste un NA en 2008
# erf$iaat <- as.factor(tmp)
# table(erf$iaat, useNA="ifany")  
    tmp=erf['mdiplo']
    tmp[erf['mdiplo']in [71,""]]=1
    tmp[erf['mdiplo']in [70,60,50]]=2
    tmp[erf['mdiplo']in [41,42,31,33]]=3
    tmp[erf['mdiplo']in [10,11,30]]=4
    erf['mdiplo']=tmp
# tmp <- erf$mdiplo
# tmp[erf$mdiplo %in% c(71,"") ]      <- 1
# tmp[erf$mdiplo %in% c(70,60,50)]    <- 2
# tmp[erf$mdiplo %in% c(41,42,31,33)] <- 3
# tmp[erf$mdiplo %in% c(10,11,30)]    <- 4
# erf$mdiplo <- as.factor(tmp)
    tmp=erf['tu99']
    tmp[erf['tu99'] ==0]=1
    tmp[erf['tu99'] in [1,2,3]]=2
    tmp[erf['tu99'] in [4,5,6]]=3
    tmp[erf['tu99'] ==7]=4
    tmp[erf['tu99'] ==8]=5
    erf['tu99_recoded']=tmp
# tmp <- erf$tu99   # erf$tu99 is coded from 0 to 8 
# tmp[erf$tu99 %in% c(0)] <- 1
# tmp[erf$tu99 %in% c(1,2,3)] <- 2
# tmp[erf$tu99 %in% c(4,5,6)] <- 3
# tmp[erf$tu99 %in% c(7)] <- 4
# tmp[erf$tu99 %in% c(8)] <- 5
# erf$tu99_recoded <- as.factor(tmp)
    tmp=erf['mcs8']
    tmp[erf['mcs8']==1]=1
    tmp[erf['mcs8']==2]=2
    tmp[erf['mcs8']==3]=3
    tmp[erf['mcs8'] in [4,8]]=4
    tmp[erf['mcs8']in [5,6,7]]=5
    erf['mcs8']=tmp
# tmp <- erf$mcs8
# tmp[erf$mcs8 %in% c(1)] <- 1  # TODO 0 ? rajouter 2003 ! 
# tmp[erf$mcs8 %in% c(2)] <- 2
# tmp[erf$mcs8 %in% c(3)] <- 3
# tmp[erf$mcs8 %in% c(4,8)] <- 4
# tmp[erf$mcs8 %in% c(5,6,7)] <- 5
# erf$mcs8 <- as.factor(tmp)
    erf['wprm']=int(erf['wprm'])
# erf$wprm  <- as.integer(erf$wprm)
# 
    for col in erf.columns: # Sorte de drop, pas sûr que ça marche
        if col=='cstotpr' or col=='agpr' or col=='typmen5' or col=='nbenfc' or col=='spr' or col=='tmp' or col=='tu99':
            del col
# erf <- upData(erf, drop=c('cstotpr','agpr','typmen5','nbenfc','spr','tmp','tu99'))
# 
# # remove empty levels
    erf.dropna(how=['logt','magtr','mcs8','mtybd','hnph2','mnatio','iaat','mdiplo','tu99_recoded'])
# erf <- within(erf,{
#   logt <- logt[,drop=TRUE]
#   magtr <-magtr[,drop=TRUE]
#   mcs8 <-mcs8[,drop = TRUE]
#   mtybd <-mtybd[,drop = TRUE]
#   hnph2 <-hnph2[,drop = TRUE]
#   mnatio <-mnatio[,drop = TRUE]
#   iaat <-iaat[,drop = TRUE]
#   mdiplo <- mdiplo[,drop = TRUE]
#   tu99_recoded <-tu99_recoded[,drop = TRUE]
#   mcs8 <- mcs8[,drop = TRUE]
# })
# saveTmp(erf, file = "erf.Rdata")
# 
# rm(erf)'''
#===============================================================================

if __name__ == '__main__':
    year = 2006
    create_imput_loyer(year=year)
