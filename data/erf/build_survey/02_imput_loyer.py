# -*- coding:utf-8 -*-
# Created on 17 juin 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)


from __future__ import division
from src.countries.france.data.erf.datatable import DataCollection
from src.countries.france.data.erf.build_survey import show_temp, load_temp, save_temp
from src.countries.france.data.erf.build_survey.utilitaries import control
import pandas as pd
from pandas import DataFrame
from numpy import array, where, NaN
from pandas import concat
import gc
import math
from numpy import logical_not as not_, logical_and as and_
from src.lib.utils import mark_weighted_percentiles 

# TODO:
# - Garder le code R, c'est plus facile pour débugguer <------------- OK
# - Ne pas garder les camelCase et mettre des espaces autour des " = " et après les ", ". <------- Fait pour les =, à moitié pour les ,
# - En général essayer de se conformer au coding style rules énoncées ici: http://www.python.org/dev/peps/pep-0008/ <------ OK
# - Mettre des espaces pour aérer ton code <------ OK
# - Rajouter des assert pour vérifier certaiens étapes (demander à Jérôme) <----- Rajouté des "control" après les "merge"
def create_imput_loyer(year):
    
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
    

# menmVars
# erfmenm <- LoadIn(menm, menmVars)
# erfmenm <- within(erfmenm,{
#   revtot <- ztsam+zperm+zragm+zricm+zrncm+zracm
#   nvpr <- revtot/nb_uci
#   logt <- as.factor(so)
#   })
# erfindm <- LoadIn(eecIndFil, indmVars)
# erfindm <- subset(erfindm,lpr==1,select=c(ident,dip11))
    ## Travail sur la base ERF
    #Preparing ERF menages tables
    print show_temp()
    temp1 = load_temp(name = "enfnn", year = year)
    erfmenm = load_temp(name="menagem", year=year) 
    #erfmenm = df.get_values(table=" ",variables=menmVars)
    erfmenm['revtot'] = (erfmenm['ztsam'] + erfmenm['zperm'] + erfmenm['zragm'] + 
                         erfmenm['zricm'] + erfmenm['zrncm'] + erfmenm['zracm'])
    erfmenm['nvpr'] = erfmenm['revtot'] / erfmenm['nb_uci']
    erfmenm['logt'] = erfmenm['so']
    #Preparing ERF individuals table
    erfindm = load_temp(name = "indivim",year=year)
    # erfindm = df.get_values(table = " ", variables = indmVars)
    print 'test un deux'
    print 'aai1' in erfindm.columns or 'aai1' in erfmenm.columns
    print 'ident' in erfindm.columns
    print 'dip11' in erfindm.columns
    erfindm = erfindm[['ident', 'dip11']][erfindm['lpr'] == 1]
# erf <- merge(erfmenm, erfindm, by ="ident")
    print('merging erf menage and individu')
    erf = erfmenm.merge(erfindm, on ='ident', how='outer')
    control(erf)

    
# dec <- wtd.quantile(erf$nvpr,weights=erf$wprm,probs=c(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1))
# erf$deci <-  as.factor((1 + (erf$nvpr>=dec[2]) + (erf$nvpr>=dec[3])
#                          + (erf$nvpr>=dec[4]) + (erf$nvpr>=dec[5])
#                          + (erf$nvpr>=dec[6]) + (erf$nvpr>=dec[7])
#                          + (erf$nvpr>=dec[8]) + (erf$nvpr>=dec[9])
#                          + (erf$nvpr>=dec[10])))
    dec = mark_weighted_percentiles(erf['nvpr'],[1,2,3,4,5,6,7,8,9,10],
                                    erf['wprm'],1,return_quantiles=False) 
    # J'utilise la méthode de wikipedia
    erf['deci'] = (1+dec['nvpr']>1+dec['nvpr']>2+dec['nvpr']>3
                 +dec['nvpr']>4+dec['nvpr']>5+dec['nvpr']>6
                 +dec['nvpr']>7+dec['nvpr']>8+dec['nvpr']>9)
    del dec


# erf <- subset(erf, so %in% c(3,4,5),
#                select=c(ident,ztsam,zperm,zragm,zricm,zrncm,zracm,
#                  nb_uci,logt,nbpiec,typmen5,spr,nbenfc,agpr,cstotpr,
#                  nat28pr,tu99,aai1,wprm,nvpr,revtot,dip11,deci))
# 
# erf <- upData(erf, rename=c(nbpiec='hnph2',nat28pr='mnatio',aai1='iaat',
#                      dip11='mdiplo'))
    erf = erf[['ident','ztsam','zperm','zragm','zricm','zrncm','zracm',
                 'nb_uci','logt','nbpiec','typmen5','spr','nbenfc','agpr','cstotpr',
                 'nat28pr','tu99','aai1','wprm','nvpr','revtot','dip11','deci']][erf['so'] < 6 and erf['so'] > 2]

    erf.rename(columns = {'nbpiec':'hnph2','nat28pr':'mnatio','aai1':'iaat','dip11':'mdiplo'}) 
    # TODO: ne traite pas les types comme dans R teste-les pour voir comment pandas les gère 
    
# erf$agpr <- as.integer(erf$agpr)
# erf$tmp <- 3
# erf$tmp[erf$agpr < 65] <- 2
# erf$tmp[erf$agpr < 40] <- 1
# erf$magtr <- as.factor(erf$tmp)        
    erf['agpr'] = int(erf['agpr'])
    erf['tmp'] = 3
    erf['tmp'][erf['agpr'] < 65] = 2
    erf['tmp'][erf['agpr'] < 40] = 1
    erf['magtr'] = erf['tmp']
    
# erf$mcs8 <- floor(as.integer(erf$cstotpr)/10)
# erf$mcs8[erf$mcs8==0] <- NA  # un mcs8=0 est transform? en NA : il y en a donc 1+4 NA's      
    erf['mcs8'] = math.floor(erf['cstotpr']/10)
    erf['mcs8'][erf['mcs8'] == 0] = NaN # Il y a donc 1+4 NAs
        
# erf$mtybd <- NA
# erf$mtybd[(erf$typmen5==1) & (erf$spr!=2)] <- 1
# erf$mtybd[(erf$typmen5==1) & (erf$spr==2)] <- 2
# erf$mtybd[erf$typmen5==5]          <- 3
# erf$mtybd[erf$typmen5==3]          <- 7
# erf$mtybd[erf$nbenfc ==1]          <- 4
# erf$mtybd[erf$nbenfc ==2]          <- 5
# erf$mtybd[erf$nbenfc >=3]          <- 6        
    erf['mtybd'] = NaN
    erf['mtybd'][erf['typmen5'] == 1 and erf['spr'] != 2] = 1
    erf['mtybd'][erf['typmen5'] == 1 and erf['spr'] == 2] = 2
    erf['mtybd'][erf['typmen5'] == 5] = 3
    erf['mtybd'][erf['typmen5'] == 3] = 7
    erf['mtybd'][erf['nbenfc'] == 1] = 4
    erf['mtybd'][erf['nbenfc'] == 2] = 5
    erf['mtybd'][erf['nbenfc'] >= 3] = 6
    # TODO il reste 41 NA's 2003 
    
# erf$hnph2[erf$hnph2 < 1] <- 1 # 3 logements ont 0 pièces !!
# erf$hnph2[erf$hnph2 >=6] <- 6
    erf['hnph2'][erf['hnph2'] < 1] = 1
    erf['hnph2'][erf['hnph2'] >= 6] = 6

# # table(erf$hnph2, useNA="ifany")
# # TODO: il reste un NA 2003
# #       il rest un NA en 2008
# erf$hnph2 <- as.factor(erf$hnph2)
    # Pour compter les NA
    count = 0
    tmp = pd.isnull(erf['hnph2'])
    for v in tmp:
        if v:
            count += 1
    print "count of NA's for hnph2 is " + str(count)
    del count, tmp

# tmp <- erf$mnatio
# tmp[erf$mnatio %in% c(10)] <- 1
# tmp[erf$mnatio %in% c(11,12,13,14,15,21,22,23,24,25,26,27,28,29,31,32,41,42,43,44,45,46,47,48,51,52,62,60)] <- 2  
# erf$mnatio <- as.factor(tmp)
    tmp = erf['mnatio']
    tmp[erf['mnatio'] == 10] = 1
    tmp[erf['mnatio'] in [11,12,13,14,15,21,22,23,24,25,26,27,28,29,31,32,41,42,43,44,45,46,47,48,51,52,62,60]] = 2
    erf['mnatio'] = tmp
    
# tmp <- erf$iaat
# tmp[erf$iaat %in% c(1,2,3)] <- 1
# tmp[erf$iaat %in% c(4)] <- 2
# tmp[erf$iaat %in% c(5)] <- 3
# tmp[erf$iaat %in% c(6)] <- 4
# tmp[erf$iaat %in% c(7)] <- 5
# tmp[erf$iaat %in% c(8)] <- 6
# erf$iaat <- as.factor(tmp)
    tmp = erf['iaat']
    tmp[erf['mnatio'] in [1,2,3]] = 1
    tmp[erf['mnatio'] == 4] = 2
    tmp[erf['mnatio'] == 5] = 3
    tmp[erf['mnatio'] == 6] = 4
    tmp[erf['mnatio'] == 7] = 5
    tmp[erf['mnatio'] == 8] = 6
    erf['iaat'] = tmp
    
# # Il reste un NA en 2003
# #    reste un NA en 2008
# table(erf$iaat, useNA="ifany") 
    # TODO: comparer logement et erf pour ?tre sur que cela colle
    count = 0
    tmp = pd.isnull(erf['iaat'])
    for v in tmp:
        if v:
            count += 1
    print "count of NA's for iaat is " + str(count)
    del count, tmp

# tmp <- erf$mdiplo
# tmp[erf$mdiplo %in% c(71,"") ]      <- 1
# tmp[erf$mdiplo %in% c(70,60,50)]    <- 2
# tmp[erf$mdiplo %in% c(41,42,31,33)] <- 3
# tmp[erf$mdiplo %in% c(10,11,30)]    <- 4
# erf$mdiplo <- as.factor(tmp) 
    tmp = erf['mdiplo']
    tmp[erf['mdiplo']in [71,""]] = 1
    tmp[erf['mdiplo']in [70,60,50]] = 2
    tmp[erf['mdiplo']in [41,42,31,33]] = 3
    tmp[erf['mdiplo']in [10,11,30]] = 4
    erf['mdiplo'] = tmp
    
# tmp <- erf$tu99   # erf$tu99 is coded from 0 to 8 
# tmp[erf$tu99 %in% c(0)] <- 1
# tmp[erf$tu99 %in% c(1,2,3)] <- 2
# tmp[erf$tu99 %in% c(4,5,6)] <- 3
# tmp[erf$tu99 %in% c(7)] <- 4
# tmp[erf$tu99 %in% c(8)] <- 5
# erf$tu99_recoded <- as.factor(tmp)
    tmp = erf['tu99']
    tmp[erf['tu99'] == 0] = 1
    tmp[erf['tu99'] in [1,2,3]] = 2
    tmp[erf['tu99'] in [4,5,6]] = 3
    tmp[erf['tu99'] == 7] = 4
    tmp[erf['tu99'] == 8] = 5
    erf['tu99_recoded'] = tmp
    
# tmp <- erf$mcs8
# tmp[erf$mcs8 %in% c(1)] <- 1  # TODO 0 ? rajouter 2003 ! 
# tmp[erf$mcs8 %in% c(2)] <- 2
# tmp[erf$mcs8 %in% c(3)] <- 3
# tmp[erf$mcs8 %in% c(4,8)] <- 4
# tmp[erf$mcs8 %in% c(5,6,7)] <- 5
# erf$mcs8 <- as.factor(tmp)
    tmp = erf['mcs8']
    tmp[erf['mcs8'] == 1] = 1
    tmp[erf['mcs8'] == 2] = 2
    tmp[erf['mcs8'] == 3] = 3
    tmp[erf['mcs8'] in [4,8]] = 4
    tmp[erf['mcs8']in [5,6,7]] = 5
    erf['mcs8'] = tmp
    
# erf$wprm  <- as.integer(erf$wprm)
    erf['wprm'] = int(erf['wprm'])

#erf <- upData(erf, drop=c('cstotpr','agpr','typmen5','nbenfc','spr','tmp','tu99'))
    del erf[['cstotpr','agpr','typmen5','nbenfc','spr','tmp','tu99']]
    
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
    erf.dropna(axis = ['logt','magtr','mcs8','mtybd','hnph2','mnatio','iaat','mdiplo','tu99_recoded'],how = 'any')

    ## Travail sur la table logement

    # Table menage
# if (year=="2003"){
#   year_lgt = "2003"}
# 
# if (year %in% c("2006","2007","2008","2009")){
#   year_lgt = "2006"}
    if year == 2003:
        year_lgt = 2003
    if year > 2005 and year < 2009:
        year_lgt = 2006



# message("preparing logement menage table")
# lgtmen <- LoadIn(lgtMenFil,lgtMenVars)
# lgtmen <- upData(lgtmen, rename=renameidlgt)
# J'ignore cette étape pour l'instant ( table correspondante non trouvée ? )
    Lgtmen = load_temp(name = "indivim",year = year) # Je rajoute une étape bidon
    # lgtmen = df.get_values(table = " ", variables = LgtMenVars)
    
# lgtmen <- within(lgtmen,{
#   mrcho[is.na(mrcho)] <- 0
#   mrret[is.na(mrret)] <- 0
#   mrsal[is.na(mrsal)] <- 0
#   mrtns[is.na(mrtns)] <- 0
#   revtot <- mrcho+mrret+mrsal+mrtns 
#   nvpr   <- (10.0)*revtot/muc1
# })    
    Lgtmen.fillna(axis = ['mrcho','mrret','mrsal','mrtns'],value = 0)
    Lgtmen['revtot'] = Lgtmen['mrcho']+Lgtmen['mrret']+Lgtmen['mrsal']+Lgtmen['mrtns'] # Virer les revenus négatifs ?
    Lgtmen['nvpr']=10.0*Lgtmen['revtot']/Lgtmen['muc1']

# dec <- wtd.quantile(lgtmen$nvpr,weights=lgtmen$qex,probs=c(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1))
# lgtmen <- within(lgtmen,{
#   deci <-  as.factor(1 + (nvpr>=dec[2]) 
#               + (nvpr>=dec[3])
#               + (nvpr>=dec[4]) 
#               + (nvpr>=dec[5])
#               + (nvpr>=dec[6]) 
#               + (nvpr>=dec[7])
#               + (nvpr>=dec[8]) 
#               + (nvpr>=dec[9])
#               + (nvpr>=dec[10]))
# })
    dec = mark_weighted_percentiles(Lgtmen['nvpr'],[1,2,3,4,5,6,7,8,9,10],
                                    Lgtmen['qex'],1,return_quantiles=False) 
    # J'utilise la méthode des quantiles wikipedia
    Lgtmen['deci'] = (1+dec['nvpr']>1+dec['nvpr']>2+dec['nvpr']>3
                 +dec['nvpr']>4+dec['nvpr']>5+dec['nvpr']>6
                 +dec['nvpr']>7+dec['nvpr']>8+dec['nvpr']>9)
    del dec
    
    ##Table logement (pas en 2003 mais en 2006)
# str(lgtmen)
# if (year_lgt=="2006"){
#   message("preparing logement logement table")
#   lgtlgt <- LoadIn(lgtLgtFil,lgtLgtVars)
#   lgtlgt <- upData(lgtlgt, rename=renameidlgt)
#   lgtmen <- merge(lgtmen, lgtlgt, by.x="ident", by.y="ident")
#   rm(lgtlgt)
# }
    if year_lgt == 2006:
        print 'preparing logement logement table'
        #lgtlgt=load_temp()
        # lgtlgt = df.get_values(table = " ", variables = LgtLgtVars)
        # Pas saisi l'étape rename
        Lgtmen.merge(lgtlgt, on = 'indent', how = 'outer')

# data <- subset(lgtmen,sec1==21 | sec1==22|
#                sec1==23 | sec1==24 | sec1==30)
    data = Lgtmen[Lgtmen['sec1'] in [21,22,23,24,30]]
    del Lgtmen

# if (year_lgt=="2006"){     # existe en 2006 pas en 2002
#   data <- upData(data, rename=c(mnatio="mnatior"))
# }
    if year_lgt == 2006:
        data.rename(columns = {'mnatio':'mnatior'})
        
# data <- within(data,{
#   mnatior <- as.factor(mnatior)
#   mnatior <- mnatior[,drop = TRUE]
#   sec1    <- as.factor(sec1)
#   sec1    <- sec1[,drop = TRUE]
#   tmp <- as.character(sec1)
#   tmp[sec1 %in% c(21,22,23)] <- 3
#   tmp[sec1 %in% c(24)]           <- 4
#   tmp[sec1 %in% c(30)]           <- 5
#   logt <- as.factor(tmp)
#   logt    <- logt[,drop = TRUE]
# })
# lgtmen <- data
    data.dropna(axis = ['mnatior','sec1'],how = 'any')
    data['tmp'] = data['sec1']
    data['tmp'][data['sec1'] in [21,22,23]] = 3
    data['tmp'][data['sec1'] == 24] = 4
    data['tmp'][data['sec1'] == 30] = 5
    data['logt'] = data['tmp']
    data.dropna(axis = ['logt'],how = 'any')
    Lgtmen=data

# ## Table adresse
# message("preparing logement adresse table")
# lgtadr <- LoadIn(lgtAdrFil,lgtAdrVars)
# lgtadr <- upData(lgtadr, rename=renameidlgt)
    # Je rajoute une étae bidon
    Lgtadr = load_temp(table = "indivim",year = year)
    # Lgtadr = df.get_values(table = " ", variables = LgtAdrVars)
    # pas compris le rename
    
# logement <- merge(lgtmen, lgtadr, by = "ident")    
    # Merge et création de nouvelles variables
    print('Merging logement and menage tables')
    Logement = Lgtmen.merge(Lgtadr, on = 'ident', how = 'inner') # inner par défaut en R
    control(Logement)
    
# logement <- within(logement,{
#   hnph2[hnph2 >=6] <- 6
#   hnph2[hnph2 < 1] <- 1
#   hnph2 <- as.factor(hnph2)
#   hnph2 <- hnph2[,drop = TRUE]    
    Logement['hnph2'][Logement['hnph2'] >= 6] = 6
    Logement['hnph2'][Logement['hnph2'] < 1] = 1
    Logement.dropna(axis = ['hpnh2'],how = 'any')

#   tmp <- mnatior
#   tmp[mnatior %in% c(00,01)] <- 1
#   tmp[mnatior %in% c(02,03,04,05,06,07,08,09,10,11)] <- 2
#   mnatior <- as.factor(tmp)
    # On est dans la même étape within ici et par la suite ( cf code R )
    Logement['tmp'] = Logement['mnatior']
    Logement['tmp'][Logement['mnatior'] in [00,01]] = 1
    Logement['tmp'][Logement['mnatior'] in [02,03,04,05,06,07,08,09,10,11]] = 2 # Aucune idée de ce qui fait planter
    Logement['mnatior'] = Logement['tmp']

#   tmp <- iaat
#   tmp[iaat %in% c(1,2,3,4,5)] <- 1
#   tmp[iaat %in% c(6)] <- 2
#   tmp[iaat %in% c(7)] <- 3
#   tmp[iaat %in% c(8)] <- 4
#   tmp[iaat %in% c(9)] <- 5
#   tmp[iaat %in% c(10)]<- 6
#   iaat <- as.factor(tmp) 
    Logement['tmp'] = Logement['iaat']
    Logement['tmp'][Logement['iaat'] in [1,2,3,4,5]] = 1
    Logement['tmp'][Logement['iaat'] == 6] = 2
    Logement['tmp'][Logement['iaat'] == 7] = 3
    Logement['tmp'][Logement['iaat'] == 8] = 4
    Logement['tmp'][Logement['iaat'] == 9] = 5
    Logement['tmp'][Logement['iaat'] == 10] = 6 # TODO question Clément : et le 9 et le 10 ?
    Logement['iaat'] = Logement['tmp']

#   tmp <- mdiplo
#   tmp[mdiplo %in% c(1)] <- 1
#   tmp[mdiplo %in% c(2,3,4)] <- 2
#   tmp[mdiplo %in% c(5,6,7,8)] <- 3
#   tmp[mdiplo %in% c(9)] <- 4
#   mdiplo <- as.factor(tmp)
    Logement['tmp'] = Logement['mdiplo']
    Logement['tmp'][Logement['mdiplo'] == 1] = 1
    Logement['tmp'][Logement['mdiplo'] in [2,3,4]] = 2
    Logement['tmp'][Logement['mdiplo'] in [5,6,7,8]] = 3
    Logement['tmp'][Logement['mdiplo'] == 9] = 4
    Logement['mdiplo'] = Logement['tmp']

#   tmp <- as.numeric(as.character(mtybd))
#   tmp[mtybd %in% c(110)] <- 1
#   tmp[mtybd %in% c(120)] <- 2
#   tmp[mtybd %in% c(200)] <- 3
#   tmp[mtybd %in% c(311,321,401)] <- 4
#   tmp[mtybd %in% c(312,322,402)] <- 5
#   tmp[mtybd %in% c(313,323,403)] <- 6
#   tmp[mtybd %in% c(400)] <- 7
#   mtybd <- as.factor(tmp)
    Logement['tmp'] = Logement['mtybd']
    Logement['tmp'][Logement['mtybd'] == 110] = 1
    Logement['tmp'][Logement['mtybd'] == 120] = 2
    Logement['tmp'][Logement['mtybd'] == 200] = 3
    Logement['tmp'][Logement['mtybd'] in [311,321,401]] = 4
    Logement['tmp'][Logement['mtybd'] in [312,322,402]] = 5
    Logement['tmp'][Logement['mtybd'] in [313,323,403]] = 6
    Logement['tmp'][Logement['mtybd'] == 400] = 7
    Logement['mtybd'] = Logement['tmp']

#   tmp <- as.numeric(as.character(tu99)) # tu99 is coded on 8 levels
#   tmp[tu99 %in% c(0)] <- 1
#   tmp[tu99 %in% c(1,2,3)] <- 2
#   tmp[tu99 %in% c(4,5,6)] <- 3
#   tmp[tu99 %in% c(7)] <- 4
#   tmp[tu99 %in% c(8)] <- 5
#   tu99_recoded <- as.factor(tmp) 
    Logement['tmp'] = Logement['tu99']
    Logement['tmp'][Logement['tu99'] == 0] = 1
    Logement['tmp'][Logement['tu99'] in [1,2,3]] = 2
    Logement['tmp'][Logement['tu99'] in [4,5,6]] = 3
    Logement['tmp'][Logement['tu99'] == 7] = 4
    Logement['tmp'][Logement['tu99'] == 8] = 5
    Logement['tu99_recoded'] = Logement['tmp']

#   tmp <- gzc2
#   tmp[gzc2 %in% c(1)] <- 1
#   tmp[gzc2 %in% c(2,3,4,5,6)] <- 2
#   tmp[gzc2 %in% c(7)] <- 3
#   gzc2 <- as.factor(tmp) 
    Logement['tmp'] = Logement['gzc2']
    Logement['tmp'][Logement['gzc2'] == 1] = 1
    Logement['tmp'][Logement['gzc2'] in [2,3,4,5,6]] = 2
    Logement['tmp'][Logement['gzc2'] == 7] = 3
    Logement['gzc2'] = Logement['tmp']

#   tmp <- magtr
#   tmp[magtr %in% c(1,2)] <- 1
#   tmp[magtr %in% c(3,4)] <- 2
#   tmp[magtr %in% c(5)] <- 3
#   magtr <- as.factor(tmp)
    Logement['tmp'] = Logement['magtr']
    Logement['tmp'][Logement['magtr'] in [1,2]] = 1
    Logement['tmp'][Logement['magtr'] in [3,4]] = 2
    Logement['tmp'][Logement['magtr'] == 5] = 3
    Logement['magtr'] = Logement['tmp']

#   tmp <- mcs8
#   tmp[mcs8 %in% c(1)] <- 1
#   tmp[mcs8 %in% c(2)] <- 2
#   tmp[mcs8 %in% c(3)] <- 3
#   tmp[mcs8 %in% c(4,8)] <- 4
#   tmp[mcs8 %in% c(5,6,7)] <- 5
#   mcs8 <- as.factor(tmp)
    Logement['tmp'] = Logement['mcs8']
    Logement['tmp'][Logement['mcs8'] == 1] = 1
    Logement['tmp'][Logement['mcs8'] == 2] = 2
    Logement['tmp'][Logement['mcs8'] == 3] = 3
    Logement['tmp'][Logement['mcs8'] in [4,8]] = 4
    Logement['tmp'][Logement['mcs8'] in [5,6,7]] = 5
    Logement['mcs8'] = Logement['tmp']

#   logloy <- log(lmlm)
    Logement['logloy'] = math.log(Logement['lmlm'])

#   mdiplo  <- mdiplo[,drop = TRUE]
#   mtybd   <- mtybd[,drop = TRUE]
#   magtr   <- magtr[,drop = TRUE]
#   mcs8    <- mcs8[,drop = TRUE]
#   maa1at  <- maa1at[,drop = TRUE]
# 
# })
    Logement.dropna(axis = ['mdiplo','mtybd','magtr','mcs8','maa1at'])

    ## Imputation des loyers proprement dite 

# library(StatMatch) # loads StatMatch
# # library(mice) use md.pattern to locate missing data
    # TODO : à suprimer ?
    
# logt <- subset(logement,select=c(lmlm,logt , hnph2 , iaat , mdiplo , mtybd , tu99_recoded , magtr , mcs8 , deci, ident))
# logt$wprm <- logement$qex
# erf <- subset(erf,select=c( logt , hnph2 , iaat , mdiplo , mtybd , tu99_recoded , magtr , mcs8 , deci, wprm, ident))
    print ('Compute imputed rents')
    Logt = Logement[['lmlm','logt' , 'hnph2' , 'iaat' , 'mdiplo' , 'mtybd' , 'tu99_recoded' , 'magtr' , 'mcs8' , 'deci', 'ident']]
    Logt['wprm'] = Logement['qex']
    erf = erf[['logt' , 'hnph2' , 'iaat' , 'mdiplo' , 'mtybd' , 'tu99_recoded' , 'magtr' , 'mcs8' , 'deci', 'wprm' , 'ident']]

# # debug
# # derf  <- describe(erf, weights=as.numeric(erf$wprm))
# # dlogt <- describe(logt, weights=logt$wprm)   
# # 
# # for (var in as.list(names(derf))){
# #   print("erf")
# #   print(derf[[var]]) 
# #   print("logt")
# #   print(dlogt[[var]]) 
# #   print("================")
# # }
    

    # TODO add md.pattern

# erf1 <- na.omit(erf)
# logt <- na.omit(logt)
    erf.dropna(how = 'any') # Si j'ai bien compris ce que l'on fait en R : dropper les lignes avec des NA
    #erf1 = erf # A-t-on toujours besoin de changer le nom du coup ?
    Logt.dropna(how = 'any')
    
# allvars <- c("logt", "hnph2", "iaat", "mdiplo", "mtybd", "tu99_recoded", "magtr", "mcs8", "deci")
# classes <- c("magtr","tu99_recoded")
# matchvars <- setdiff(allvars,classes)
    allvars = ['logt', 'hnph2', 'iaat', 'mdiplo', 'mtybd', 'tu99_recoded', 'magtr', 'mcs8', 'deci']  
    classes = ['magtr', 'tu99_recoded']
    matchvars = list(set(allvars)-set(classes))

# out.nnd <- NND.hotdeck(data.rec=erf1,data.don=logt,match.vars=matchvars,don.class=classes,gdist.fun="Gower")
# fill.erf.nnd <- create.fused(data.rec=erf1, data.don=logt,mtc.ids=out.nnd$mtc.ids, z.vars="lmlm")
    # Je mets ça pour l'instant faute de comprendre au-dessus
    (fill_erf_nnd)=erf 
    del allvars, matchvars, classes

# fill.erf.nnd <- upData(fill.erf.nnd, rename=c(lmlm='loym'))
    (fill_erf_nnd).rename(columns={'lmlm':'loym'})

# loy_imput = fill.erf.nnd[c('ident','loym')]
    loy_imput = (fill_erf_nnd)[['ident','loym']]

# load(menm)
# menagem$loym <- NULL
# menagem <- merge(menagem,loy_imput,by='ident',all.x = TRUE)
# save(menagem,file=menm)
    # Mis en comment block, car à manipuler avec précaution je suppose ( ne souhaite pas faire de conneries )
    #===========================================================================
    # erfmenm = load_temp(name="menagem", year=year) 
    # erfmenm['Loym'] = NaN
    # erfmenm.merge(loy_imput,on='ident',how='left')
    # save_temp(erfmenm, name = "menagem", year=year)
    #===========================================================================

if __name__ == '__main__':
    year = 2006
    create_imput_loyer(year=year)
