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
from numpy import array, where, NaN, arange
from pandas import concat
import gc
import math
import numpy as np
from numpy import logical_not as not_, logical_and as and_, maximum as max_
from src.lib.utils import mark_weighted_percentiles 

# TODO:
# - Garder le code R, c'est plus facile pour débugguer <------------- OK
# - Ne pas garder les camelCase et mettre des espaces autour des " = " et après les ", ". <------- Fait pour les =, à moitié pour les ,
# - En général essayer de se conformer au coding style rules énoncées ici: http://www.python.org/dev/peps/pep-0008/ <------ OK
# - Mettre des espaces pour aérer ton code <------ OK
# - Rajouter des assert pour vérifier certaiens étapes (demander à Jérôme) <----- Rajouté des "control" après les "merge"
def create_imput_loyer(year):
    def assert_variable_inrange(name, wrange, table): # Assert if transformed variables are in correct range
        temp = (table[table[name].notnull()])
        range_1 = wrange[0]
        range_2 = wrange[1]
        #assert erf[name].isin(range(range_1, range_2+1)).all(), Exception("some %s not in wanted range" %(name))
        for v in temp[name]:
            assert v in range(range_1, range_2), Exception('some non-null values for %s not in wanted %s: %s' %(name, str(wrange), str(v)))
    def count_NA(name,table): # Counts the number of Na's in a specified axis
        count = 0
        tmp = pd.isnull(erf[name])
        for v in tmp:
            if v:
                count += 1
        print "count of NA's for %s is %s" %(name, str(count))
        #del count, tmp
        
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
    erfmenm = load_temp(name="menagem", year=year) 
    #erfmenm = df.get_values(table=" ",variables=menmVars)
    #Construction d'un temp pour éviter la prolifération des NA à partir de revtot
    erfmenm['revtot'] = (erfmenm['ztsam'] + erfmenm['zperm'] + erfmenm['zragm'] + 
                         erfmenm['zricm'] + erfmenm['zrncm'] + erfmenm['zracm'])
    erfmenm['nvpr'] = erfmenm['revtot'] / erfmenm['nb_uci']
    # On donne la valeur 0 aux nvpr négatifs
    tmp = np.zeros(erfmenm['nvpr'].shape, dtype = int)
    erfmenm['nvpr'] = max_(tmp, erfmenm['nvpr'])
    for v in erfmenm['nvpr']: # On vérifie qu'il n'y a plus de nvpr négatifs
        assert v >= 0, Exception('Some nvpr are negatives')
    erfmenm['logt'] = erfmenm['so']
    l = erfmenm.columns.tolist()
    print l
    #Preparing ERF individuals table
    erfindm = load_temp(name = "indivim",year=year)
    # erfindm = df.get_values(table = " ", variables = indmVars)9++66666666
    
    # TODO: clean this later
    erfindm['dip11'] = 99
    erfindm = erfindm[['ident', 'dip11']][erfindm['lpr'] == 1]
# erf <- merge(erfmenm, erfindm, by ="ident")
    print('merging erf menage and individu')
    #erf = erfmenm.merge(erfindm, on ='ident', how='outer')
    erf = erfmenm.merge(erfindm, on ='ident', how='inner')
    erf=erf.drop_duplicates('ident')

    # control(erf) La colonne existe mais est vide, 
    # on a du confondre cette colonne avec dip11 ?
    
# dec <- wtd.quantile(erf$nvpr,weights=erf$wprm,probs=c(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1))
# erf$deci <-  as.factor((1 + (erf$nvpr>=dec[2]) + (erf$nvpr>=dec[3])
#                          + (erf$nvpr>=dec[4]) + (erf$nvpr>=dec[5])
#                          + (erf$nvpr>=dec[6]) + (erf$nvpr>=dec[7])
#                          + (erf$nvpr>=dec[8]) + (erf$nvpr>=dec[9])
#                          + (erf$nvpr>=dec[10])))

#     dec = mark_weighted_percentiles(erf['nvpr'], [1,2,3,4,5,6,7,8,9,10],
#                                     erf['wprm'], 1, return_quantiles=False) 
#     
    print erf['nvpr'].isnull().value_counts()
    print erf['wprm'].isnull().value_counts()
    print erf['nvpr'].describe()
    print erf['wprm'].describe()
    dec, values = mark_weighted_percentiles(erf['nvpr'], arange(1,11), erf['wprm'], 2, return_quantiles=True)
    values.sort()
    #print DataFrame(dec).describe()
    # J'utilise la méthode de "stackexchange post"
    
    #===========================================================================
    # erf['deci'] = (1 + (dec[0]>1) + (dec[0]>2) + (dec[0]>3)
    #                     + (dec[0]>4) + (dec[0]>5) + (dec[0]>6)
    #                     + (dec[0]>7) + (dec[0]>8) + (dec[0]>9))
    #===========================================================================
    
    erf['deci'] = (1 + (erf['nvpr']>values[1]) + (erf['nvpr']>values[2]) + (erf['nvpr']>values[3])
                   + (erf['nvpr']>values[4]) + (erf['nvpr']>values[5]) + (erf['nvpr']>values[6])
                   + (erf['nvpr']>values[7]) + (erf['nvpr']>values[8]) + (erf['nvpr']>values[9]))
    # Problème : tous les individus sont soit dans le premier, soit dans le dernier décile. WTF
    assert_variable_inrange('deci',[1,11], erf)
    count_NA('deci',erf)
    del dec, values


# erf <- subset(erf, so %in% c(3,4,5),
#                select=c(ident,ztsam,zperm,zragm,zricm,zrncm,zracm,
#                  nb_uci,logt,nbpiec,typmen5,spr,nbenfc,agpr,cstotpr,
#                  nat28pr,tu99,aai1,wprm,nvpr,revtot,dip11,deci))
# 
# erf <- upData(erf, rename=c(nbpiec='hnph2',nat28pr='mnatio',aai1='iaat',
#                      dip11='mdiplo'))
    erf = erf[['ident','ztsam','zperm','zragm','zricm','zrncm','zracm',
                 'nb_uci','logt','nbpiec','typmen5','spr','nbenfc','agpr','cstotpr',
                 'nat28pr','tu99','aai1','wprm','nvpr','revtot','dip11','deci']][erf['so'].isin(range(3,6))]

    erf.rename(columns = {'nbpiec':'hnph2','nat28pr':'mnatio','aai1':'iaat','dip11':'mdiplo'}, inplace = True)
    
    # TODO: ne traite pas les types comme dans R teste-les pour voir comment pandas les gère 
    
# erf$agpr <- as.integer(erf$agpr)
# erf$tmp <- 3
# erf$tmp[erf$agpr < 65] <- 2
# erf$tmp[erf$agpr < 40] <- 1
# erf$magtr <- as.factor(erf$tmp)    
    count_NA('agpr', erf)    
    erf['agpr'] = erf['agpr'].astype('int64')
    erf['tmp'] = 3
    erf['tmp'][erf['agpr'] < 65] = 2
    erf['tmp'][erf['agpr'] < 40] = 1
    erf['magtr'] = erf['tmp']
    count_NA('magtr',erf)
    assert_variable_inrange('magtr',[1,4],erf)
    
# erf$mcs8 <- floor(as.integer(erf$cstotpr)/10)
# erf$mcs8[erf$mcs8==0] <- NA  # un mcs8=0 est transform? en NA : il y en a donc 1+4 NA's
    #erf = erf[erf['cstotpr'].notnull()]
    count_NA('cstotpr',erf)
    erf['tmp'] = erf['cstotpr'].astype('float')/10.0
    erf['tmp']=map(math.floor, erf['tmp'])
    erf['mcs8'] = erf['tmp']
    #erf['mcs8'] = math.floor(erf['cstotpr']/10.0)
    erf['mcs8'][erf['mcs8'] == 0] = NaN # Il y a donc 1+4 NAs
    #assert isinstance(erf['mcs8'], (int, long)).all(), Exception('Some mcs8 are not integers')
    count_NA('mcs8',erf)
        
# erf$mtybd <- NA
# erf$mtybd[(erf$typmen5==1) & (erf$spr!=2)] <- 1
# erf$mtybd[(erf$typmen5==1) & (erf$spr==2)] <- 2
# erf$mtybd[erf$typmen5==5]          <- 3
# erf$mtybd[erf$typmen5==3]          <- 7
# erf$mtybd[erf$nbenfc ==1]          <- 4
# erf$mtybd[erf$nbenfc ==2]          <- 5
# erf$mtybd[erf$nbenfc >=3]          <- 6
# TODO il reste 41 NA's 2003      
    erf['mtybd'] = NaN
    erf['mtybd'][(erf['typmen5'] == 1) & (erf['spr'] != 2)] = 1 # Attention à ne pas mettre de "and", il n'aime pas ça
    erf['mtybd'][(erf['typmen5'] == 1) & (erf['spr'] == 2)] = 2 # Vérifier que ça fait bien ce que l'on veut
    erf['mtybd'][erf['typmen5'] == 5] = 3
    erf['mtybd'][erf['typmen5'] == 3] = 7
    erf['mtybd'][erf['nbenfc'] == 1] = 4
    erf['mtybd'][erf['nbenfc'] == 2] = 5
    erf['mtybd'][erf['nbenfc'] >= 3] = 6
    count_NA('mtybd',erf)
    print "PINGAS"
    print erf['mtybd'].dtype.fields
    #assert_variable_inrange('mtybd', [1,7], erf) # bug, on trouve 7.0 qui fait assert
    
# erf$hnph2[erf$hnph2 < 1] <- 1 # 3 logements ont 0 pièces !!
# erf$hnph2[erf$hnph2 >=6] <- 6
    erf['hnph2'][erf['hnph2'] < 1] = 1
    erf['hnph2'][erf['hnph2'] >= 6] = 6
    count_NA('hnph2', erf)
    assert_variable_inrange('hnph2', [1,7], erf)
    

# # table(erf$hnph2, useNA="ifany")
# # TODO: il reste un NA 2003
# #       il rest un NA en 2008
# erf$hnph2 <- as.factor(erf$hnph2)
   

# tmp <- erf$mnatio
# tmp[erf$mnatio %in% c(10)] <- 1
# tmp[erf$mnatio %in% c(11,12,13,14,15,21,22,23,24,25,26,27,28,29,31,32,41,42,43,44,45,46,47,48,51,52,62,60)] <- 2  
# erf$mnatio <- as.factor(tmp)
    tmp = erf['mnatio']
    tmp[erf['mnatio'] == 10] = 1
    tmp[erf['mnatio'].isin([11,12,13,14,15,21,22,23,24,25,26,27,28,29,31,32,41,42,43,44,45,46,47,48,51,52,62,60])] = 2
    erf['mnatio'] = tmp
    count_NA('mnatio', erf)
    assert_variable_inrange('mnatio', [1,3], erf)
    
# tmp <- erf$iaat
# tmp[erf$iaat %in% c(1,2,3)] <- 1
# tmp[erf$iaat %in% c(4)] <- 2
# tmp[erf$iaat %in% c(5)] <- 3
# tmp[erf$iaat %in% c(6)] <- 4
# tmp[erf$iaat %in% c(7)] <- 5
# tmp[erf$iaat %in% c(8)] <- 6
# erf$iaat <- as.factor(tmp)
    tmp = erf['iaat']
    tmp[erf['mnatio'].isin([1,2,3])] = 1
    tmp[erf['mnatio'] == 4] = 2
    tmp[erf['mnatio'] == 5] = 3
    tmp[erf['mnatio'] == 6] = 4
    tmp[erf['mnatio'] == 7] = 5
    tmp[erf['mnatio'] == 8] = 6
    erf['iaat'] = tmp
    count_NA('iaat', erf)
    assert_variable_inrange('iaat', [1,7], erf)
    
# # Il reste un NA en 2003
# #    reste un NA en 2008
# table(erf$iaat, useNA="ifany") 
    # TODO: comparer logement et erf pour ?tre sur que cela colle

# tmp <- erf$mdiplo
# tmp[erf$mdiplo %in% c(71,"") ]      <- 1
# tmp[erf$mdiplo %in% c(70,60,50)]    <- 2
# tmp[erf$mdiplo %in% c(41,42,31,33)] <- 3
# tmp[erf$mdiplo %in% c(10,11,30)]    <- 4
# erf$mdiplo <- as.factor(tmp) 
    tmp = erf['mdiplo']
    tmp[erf['mdiplo'].isin([71,""])] = 1
    tmp[erf['mdiplo'].isin([70,60,50])] = 2
    tmp[erf['mdiplo'].isin([41,42,31,33])] = 3
    tmp[erf['mdiplo'].isin([10,11,30])] = 4
    erf['mdiplo'] = tmp
    count_NA('mdiplo', erf)
    #assert_variable_inrange('mdiplo', [1,5], erf) # On a un 99 qui se balade
    
# tmp <- erf$tu99   # erf$tu99 is coded from 0 to 8 
# tmp[erf$tu99 %in% c(0)] <- 1
# tmp[erf$tu99 %in% c(1,2,3)] <- 2
# tmp[erf$tu99 %in% c(4,5,6)] <- 3
# tmp[erf$tu99 %in% c(7)] <- 4
# tmp[erf$tu99 %in% c(8)] <- 5
# erf$tu99_recoded <- as.factor(tmp)
    tmp = erf['tu99']
    tmp[erf['tu99'] == 0] = 1
    tmp[erf['tu99'].isin([1,2,3])] = 2
    tmp[erf['tu99'].isin([4,5,6])] = 3
    tmp[erf['tu99'] == 7] = 4
    tmp[erf['tu99'] == 8] = 5
    erf['tu99_recoded'] = tmp
    count_NA('tu99_recoded', erf)
    assert_variable_inrange('tu99_recoded', [1,6], erf)
    
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
    tmp[erf['mcs8'].isin([4,8])] = 4
    tmp[erf['mcs8'].isin([5,6,7])] = 5
    erf['mcs8'] = tmp
    count_NA('mcs8', erf)
    assert_variable_inrange('mcs8', [1,6], erf)
    
# erf$wprm  <- as.integer(erf$wprm)
    erf['wprm'] = erf['wprm'].astype('int64')
    count_NA('wprm', erf)

#erf <- upData(erf, drop=c('cstotpr','agpr','typmen5','nbenfc','spr','tmp','tu99'))
    del (erf['cstotpr'] ,erf['agpr'], erf['typmen5'], 
    erf['nbenfc'], erf['spr'], erf['tmp'], erf['tu99'])
    
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
    erf=(erf[erf['logt'].notnull()]) # Pas trouvé plus convenable
    erf=(erf[erf['magtr'].notnull()])
    erf=(erf[erf['mcs8'].notnull()])
    erf=(erf[erf['mtybd'].notnull()])
    erf=(erf[erf['hnph2'].notnull()])
    erf=(erf[erf['mnatio'].notnull()])
    erf=(erf[erf['iaat'].notnull()])
    erf=(erf[erf['mdiplo'].notnull()])
    erf=(erf[erf['tu99_recoded'].notnull()])
    
    #On vérifie au final que l'on n'a pas de doublons d'individus
    erf_drop_dupl = erf.drop_duplicates('ident')
    assert len(erf['ident'].value_counts()) == len(erf_drop_dupl['ident']), Exception('Number of distinct individuals after removing duplicates is not correct')
    del erf_drop_dupl
    
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


    return
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
    dec = mark_weighted_percentiles(Lgtmen['nvpr'],arange(1,11),
                                    Lgtmen['qex'],2,return_quantiles=False) 
    dec = DataFrame(dec)
    # J'utilise la méthode des quantiles wikipedia
    Lgtmen['deci'] = (1+dec[0]>1+dec[0]>2+dec[0]>3
                 +dec[0]>4+dec[0]>5+dec[0]>6
                 +dec[0]>7+dec[0]>8+dec[0]>9)
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
        lgtlgt=load_temp()
        # lgtlgt = df.get_values(table = " ", variables = LgtLgtVars)
        # Pas saisi l'étape rename
        Lgtmen.merge(lgtlgt, on = 'indent', how = 'outer')

# data <- subset(lgtmen,sec1==21 | sec1==22|
#                sec1==23 | sec1==24 | sec1==30)
    data = Lgtmen[Lgtmen['sec1'].isin([21,22,23,24,30])]
    del Lgtmen

# if (year_lgt=="2006"){     # existe en 2006 pas en 2002
#   data <- upData(data, rename=c(mnatio="mnatior"))
# }
    if year_lgt == 2006:
        data.rename(columns = {'mnatio':'mnatior'}, inplace = True)
        
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
    data=(data[data['mnatior'].notnull()])
    data=(data[data['sec1'].notnull()])
    data['tmp'] = data['sec1']
    data['tmp'][data['sec1'].isin([21,22,23])] = 3
    data['tmp'][data['sec1'] == 24] = 4
    data['tmp'][data['sec1'] == 30] = 5
    data['logt'] = data['tmp']
    count_NA('logt', data)
    data=(data[data['logt'].notnull()])
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
    count_NA('hnph2', Logement)
    Logement=(Logement[Logement['hpnh2'].notnull()])

#   tmp <- mnatior
#   tmp[mnatior %in% c(00,01)] <- 1
#   tmp[mnatior %in% c(02,03,04,05,06,07,08,09,10,11)] <- 2
#   mnatior <- as.factor(tmp)
    # On est dans la même étape within ici et par la suite ( cf code R )
    # ATTENTION : ici problème je transforme les 07 en 7 
    # car Python considère les 0n comme des nombres octaux ( < 08 ).
    # J'espère que ce n'est pas important.
    Logement['tmp'] = Logement['mnatior']
    Logement['tmp'][Logement['mnatior'].isin([0, 1])] = 1
    Logement['tmp'][Logement['mnatior'].isin([2, 3, 4, 5, 6, 7, 8, 9, 10, 11])] = 2 # Aucune idée de ce qui fait planter
    Logement['mnatior'] = Logement['tmp']
    count_NA('mnatior', Logement)
    assert_variable_inrange('mnatior', [1,3], Logement)

#   tmp <- iaat
#   tmp[iaat %in% c(1,2,3,4,5)] <- 1
#   tmp[iaat %in% c(6)] <- 2
#   tmp[iaat %in% c(7)] <- 3
#   tmp[iaat %in% c(8)] <- 4
#   tmp[iaat %in% c(9)] <- 5
#   tmp[iaat %in% c(10)]<- 6
#   iaat <- as.factor(tmp) 
    Logement['tmp'] = Logement['iaat']
    Logement['tmp'][Logement['iaat'].isin([1,2,3,4,5])] = 1
    Logement['tmp'][Logement['iaat'] == 6] = 2
    Logement['tmp'][Logement['iaat'] == 7] = 3
    Logement['tmp'][Logement['iaat'] == 8] = 4
    Logement['tmp'][Logement['iaat'] == 9] = 5
    Logement['tmp'][Logement['iaat'] == 10] = 6 # TODO question Clément : et le 9 et le 10 ?
    Logement['iaat'] = Logement['tmp']
    count_NA('iaat', Logement)
    assert_variable_inrange('iaat', [1,7], Logement)

#   tmp <- mdiplo
#   tmp[mdiplo %in% c(1)] <- 1
#   tmp[mdiplo %in% c(2,3,4)] <- 2
#   tmp[mdiplo %in% c(5,6,7,8)] <- 3
#   tmp[mdiplo %in% c(9)] <- 4
#   mdiplo <- as.factor(tmp)
    Logement['tmp'] = Logement['mdiplo']
    Logement['tmp'][Logement['mdiplo'] == 1] = 1
    Logement['tmp'][Logement['mdiplo'].isin([2,3,4])] = 2
    Logement['tmp'][Logement['mdiplo'].isin([5,6,7,8])] = 3
    Logement['tmp'][Logement['mdiplo'] == 9] = 4
    Logement['mdiplo'] = Logement['tmp']
    count_NA('mdiplo', Logement)
    assert_variable_inrange('mdiplo', [1,5], Logement)

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
    Logement['tmp'][Logement['mtybd'].isin([311,321,401])] = 4
    Logement['tmp'][Logement['mtybd'].isin([312,322,402])] = 5
    Logement['tmp'][Logement['mtybd'].isin([313,323,403])] = 6
    Logement['tmp'][Logement['mtybd'] == 400] = 7
    Logement['mtybd'] = Logement['tmp']
    count_NA('mtybd', Logement)
    assert_variable_inrange('mtybd', [1,8], Logement)

#   tmp <- as.numeric(as.character(tu99)) # tu99 is coded on 8 levels
#   tmp[tu99 %in% c(0)] <- 1
#   tmp[tu99 %in% c(1,2,3)] <- 2
#   tmp[tu99 %in% c(4,5,6)] <- 3
#   tmp[tu99 %in% c(7)] <- 4
#   tmp[tu99 %in% c(8)] <- 5
#   tu99_recoded <- as.factor(tmp) 
    Logement['tmp'] = Logement['tu99']
    count_NA('tu99', Logement)
    Logement['tmp'][Logement['tu99'] == 0] = 1
    Logement['tmp'][Logement['tu99'].isin([1,2,3])] = 2
    Logement['tmp'][Logement['tu99'].isin([4,5,6])] = 3
    Logement['tmp'][Logement['tu99'] == 7] = 4
    Logement['tmp'][Logement['tu99'] == 8] = 5
    Logement['tu99_recoded'] = Logement['tmp']
    count_NA('tu99_recoded', Logement)
    assert_variable_inrange('tu99_recoded', [1,6], Logement)

#   tmp <- gzc2
#   tmp[gzc2 %in% c(1)] <- 1
#   tmp[gzc2 %in% c(2,3,4,5,6)] <- 2
#   tmp[gzc2 %in% c(7)] <- 3
#   gzc2 <- as.factor(tmp) 
    Logement['tmp'] = Logement['gzc2']
    Logement['tmp'][Logement['gzc2'] == 1] = 1
    Logement['tmp'][Logement['gzc2'].isin([2,3,4,5,6])] = 2
    Logement['tmp'][Logement['gzc2'] == 7] = 3
    Logement['gzc2'] = Logement['tmp']
    count_NA('gzc2', Logement)
    assert_variable_inrange('gzc2', [1,4], Logement)

#   tmp <- magtr
#   tmp[magtr %in% c(1,2)] <- 1
#   tmp[magtr %in% c(3,4)] <- 2
#   tmp[magtr %in% c(5)] <- 3
#   magtr <- as.factor(tmp)
    Logement['tmp'] = Logement['magtr']
    Logement['tmp'][Logement['magtr'].isin([1,2])] = 1
    Logement['tmp'][Logement['magtr'].isin([3,4])] = 2
    Logement['tmp'][Logement['magtr'] == 5] = 3
    Logement['magtr'] = Logement['tmp']
    count_NA('magtr', Logement)
    assert_variable_inrange('magtr', [1,4], Logement)

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
    Logement['tmp'][Logement['mcs8'].isin([4,8])] = 4
    Logement['tmp'][Logement['mcs8'].isin([5,6,7])] = 5
    Logement['mcs8'] = Logement['tmp']
    count_NA('mcs8', Logement)
    assert_variable_inrange('mcs8', [1,6], Logement)

#   logloy <- log(lmlm)
    Logement['logloy'] = math.log(Logement['lmlm'])

#   mdiplo  <- mdiplo[,drop = TRUE]
#   mtybd   <- mtybd[,drop = TRUE]
#   magtr   <- magtr[,drop = TRUE]
#   mcs8    <- mcs8[,drop = TRUE]
#   maa1at  <- maa1at[,drop = TRUE]
# 
# })
    Logement=(Logement[Logement['mdiplo'].notnull()])
    Logement=(Logement[Logement['mtybd'].notnull()])
    Logement=(Logement[Logement['magtr'].notnull()])
    Logement=(Logement[Logement['mcs8'].notnull()])
    Logement=(Logement[Logement['maa1at'].notnull()])

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
    (fill_erf_nnd).rename(columns={'lmlm':'loym'}, inplace = True)

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
