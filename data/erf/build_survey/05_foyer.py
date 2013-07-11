# -*- coding:utf-8 -*-
# Created on 21 mai 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)


## OpenFisca
## Retreives data from erf foyer 
## Creates sif and foyer_aggr
#
#
###***********************************************************************/
#message('05_foyer: extraction des données foyer')
###***********************************************************************/
#

from __future__ import division

import numpy
import re
from src.countries.france.data.erf.datatable import DataCollection
from src.countries.france.data.erf.build_survey import show_temp, load_temp, save_temp
from pandas import DataFrame, concat
import gc
from pandas import Series

from src.countries.france.data.erf.build_survey.utilitaries import print_id

def sif(year=2006):
    data = DataCollection(year=year)
    print u"05_foyer: extraction des données foyer"
    ## TODO Comment choisir le rfr n -2 pour éxonération de TH ?
    ## mnrvka  Revenu TH n-2
    ## mnrvkh  revenu TH (revenu fiscal de référence)
    #
    ## On récupère les variables du code sif
    #vars <- c("noindiv", 'sif', "nbptr", "mnrvka")
    vars = ["noindiv", 'sif', "nbptr", "mnrvka", "rbg", "tsrvbg"]
    #sif <- LoadIn(erfFoyFil, vars)
    sif = data.get_values(variables=vars, table="foyer" )
    #sif$statmarit <- 0
    sif['statmarit'] = 0
    
    print sif
    
    ## for (index in 60:80){
    ##    print(index)  
    ##    print(table(substr(sif$sif,index,index)))
    ## }
    
    
    #
    #
    ## Pb with some 2 sifs that are misaligned
    ## index = 61
    ## sif[substr(sif$sif,index,index)=="F", "noindiv"]
    ## sif$sif[sif$noindiv == sif[substr(sif$sif,index,index)=="F", "noindiv"]]
    ## sif$sif[sif$noindiv == sif[substr(sif$sif,index,index)=="F", "noindiv"]+1]
    #
    ## index = 62
    ## sif[substr(sif$sif,index,index)=="G", "noindiv"]
    ## sif$sif[sif$noindiv == sif[substr(sif$sif,index,index)=="G", "noindiv"]]
    ## sif$sif[1]
    #
    #if (year==2009){
    #  # problem with one entry in 2009 
    #  length  <- nchar(sif$sif[1])
    #  old_sif <- sif$sif[sif$noindiv == 901803201]
    #  new_sif <- paste(substr(old_sif,1,59), substr(old_sif,61,length),"0", sep="")   
    #  sif$sif[sif$noindiv == 901803201] <- new_sif
    #  old_sif <- sif$sif[sif$noindiv == 900872201]
    #  new_sif <- paste(substr(old_sif,1,58), " ", substr(old_sif,59,length), sep="")
    #  sif$sif[sif$noindiv == 900872201] <- new_sif
    #  rm(old_sif,new_sif)
    #}
    if year == 2009:
        old_sif = sif['sif'][sif['noindiv'] == 901803201]
        new_sif = old_sif.str[0:59] + old_sif.str[60:] + "0"
        sif['sif'][sif['noindiv'] == 901803201] = new_sif
        old_sif = sif['sif'][sif['noindiv'] == 900872201]
        new_sif = old_sif.str[0:58] + " " + old_sif.str[58:]
        sif['sif'][sif['noindiv'] == 900872201] = new_sif
        del old_sif, new_sif
    #
    #
    ## for (index in 60:80){
    ##     print(index)  
    ##     print(table(substr(sif$sif,index,index)))
    ## }
    #
    #
    #
    #sif <- within(sif,{
    ##  rbg = rbg*((tsrvbg =='+')-(tsrvbg =='-'))
    print sif["rbg"].describe()
    sif["rbg"] = sif["rbg"]*( (sif["tsrvbg"]=='+')-(sif["tsrvbg"] =='-'))
    print sif["rbg"].describe()
    
    #  stamar <- substr(sif,5,5)
    
    sif["stamar"] = sif["sif"].str[4:5]
    
    # Converting marital status
    
    #  statmarit[stamar =="M"] <- 1
    #  statmarit[stamar =="C"] <- 2
    #  statmarit[stamar =="D"] <- 3
    #  statmarit[stamar =="V"] <- 4
    #  statmarit[stamar =="O"] <- 5
    
    statmarit_dict = {"M": 1, "C" : 2, "D" : 3, "V" : 4, "O": 5}
    for key , val in statmarit_dict.iteritems():
        sif["statmarit"][ sif.stamar == key] = val 
        
    #  birthvous <- as.numeric(substr(sif,6,9))
    #  birthconj <- as.numeric(substr(sif,11,14))
    #
    

    sif["birthvous"] = sif["sif"].str[5:9]
    sif["birthconj"] = sif["sif"].str[10:14]
    
    #  caseE <- as.numeric(substr(sif,16,16)=='E')
    #  caseF <- as.numeric(substr(sif,17,17)=='F')
    #  caseG <- as.numeric(substr(sif,18,18)=='G')
    #  caseK <- as.numeric(substr(sif,19,19)=='K')
    
    sif["caseE"] = sif["sif"].str[15:16] == "E"
    sif["caseF"] = sif["sif"].str[16:17] == "F"
    sif["caseG"] = sif["sif"].str[17:18] == "G"
    sif["caseK"] = sif["sif"].str[18:19] == "K"
    

    d = 0
    #
    #  if (year %in% c(2006,2007)){   
    #    caseL <- as.numeric(substr(sif,20,20)=='L')
    #    caseP <- as.numeric(substr(sif,21,21)=='P')
    #    caseS <- as.numeric(substr(sif,22,22)=='S')
    #    caseW <- as.numeric(substr(sif,23,23)=='W')
    #    caseN <- as.numeric(substr(sif,24,24)=='N')
    #    caseH <- as.numeric(substr(sif,25,28))
    #    caseT <- as.numeric(substr(sif,29,29) == 'T')
    #  }
    
    if year in [2006,2007]:
        sif["caseL"] = sif["sif"].str[19:20] == "L"
        sif["caseP"] = sif["sif"].str[20:21] == "P"
        sif["caseS"] = sif["sif"].str[21:22] == "S"
        sif["caseW"] = sif["sif"].str[22:23] == "W"
        sif["caseN"] = sif["sif"].str[23:24] == "N"
        sif["caseH"] = sif["sif"].str[24:28]
        sif["caseT"] = sif["sif"].str[28:29] == "T"
    #  
    #  if (year == 2008){
    #    d = - 1 # fin de la case L
    #    caseP <- as.numeric(substr(sif,21+d,21+d)=='P')
    #    caseS <- as.numeric(substr(sif,22+d,22+d)=='S')
    #    caseW <- as.numeric(substr(sif,23+d,23+d)=='W')
    #    caseN <- as.numeric(substr(sif,24+d,24+d)=='N')
    #    caseH <- as.numeric(substr(sif,25+d,28+d))
    #    caseT <- as.numeric(substr(sif,29+d,29+d)=='T')
    #  }
    #  
    if year in [2008]:
        d = - 1 # fin de la case L
        sif["caseP"] = sif["sif"].str[20+d:21+d] == "P"
        sif["caseS"] = sif["sif"].str[21+d:22+d] == "S"
        sif["caseW"] = sif["sif"].str[22+d:23+d] == "W"
        sif["caseN"] = sif["sif"].str[23+d:24+d] == "N"
        sif["caseH"] = sif["sif"].str[24+d:28+d]
        sif["caseT"] = sif["sif"].str[28+d:29+d] == "T"
    
    #  if (year == 2009){
    #    # retour de la case L par rapport à 2008 (donc on retrouve 2006)    
    #    caseL <- as.numeric(substr(sif,20,20)=='L')
    #    caseP <- as.numeric(substr(sif,21,21)=='P')
    #    caseS <- as.numeric(substr(sif,22,22)=='S')
    #    caseW <- as.numeric(substr(sif,23,23)=='W')
    #    caseN <- as.numeric(substr(sif,24,24)=='N')
    #    # caseH en moins par rapport à 2008 (mais case en L en plus)
    #    # donc décalage par rapport à 2006
    #    d = -4
    #    caseT <- as.numeric(substr(sif,29+d,29+d)=='T')
    #  }
    
    if year in [2009]:
        sif["caseL"] = sif["sif"].str[19:20] == "L"
        sif["caseP"] = sif["sif"].str[20:21] == "P"
        sif["caseS"] = sif["sif"].str[21:22] == "S"
        sif["caseW"] = sif["sif"].str[22:23] == "W"
        sif["caseN"] = sif["sif"].str[23:24] == "N"
        # caseH en moins par rapport à 2008 (mais case en L en plus)
        # donc décalage par rapport à 2006
        d = -4
        sif["caseT"] = sif["sif"].str[28+d:29+d] == "T"
    
    
    #
    #  caseX <- as.numeric(substr(sif,34+d,34+d)=='X')
    #  dateX <- as.Date(substr(sif,35+d,42+d),'%d%m%Y')
    #  caseY <- as.numeric(substr(sif,43+d,43+d)== 'Y')
    #  dateY <- as.Date(substr(sif,44+d,51+d),'%d%m%Y')
    #  caseZ <- as.numeric(substr(sif,52+d,53+d)== 'Z')
    #  dateZ <- as.Date(substr(sif,53+d,60+d),'%d%m%Y')  # ERROR 54+d
    #  causeXYZ <- substr(sif,61+d,61+d)
    #
    
    sif["caseX"] = sif["sif"].str[33+d:34+d] == "X"
    sif["dateX"] = sif["sif"].str[34+d:42+d]
    sif["caseY"] = sif["sif"].str[42+d:43+d] == "Y"
    sif["dateY"] = sif["sif"].str[43+d:51+d] 
    sif["caseZ"] = sif["sif"].str[51+d:53+d] == "Z"
    sif["dateZ"] = sif["sif"].str[52+d:60+d] 
    sif["causeXYZ"] = sif["sif"].str[60+d:61+d]
    
    # TODO: convert dateXYZ to appropriate date in pandas
    # print sif["dateY"].unique()
    
    
    #  nbptr <- nbptr/100
    #  rfr_n_2 <- mnrvka
    
    sif["nbptr"] =  sif["nbptr"]/100
    sif["rfr_n_2"] = sif["mnrvka"]
    
    #  nbF <- as.numeric(substr(sif,65+d,66+d))
    #  nbG <- as.numeric(substr(sif,68+d,69+d))
    #  nbR <- as.numeric(substr(sif,71+d,72+d))
    #  nbJ <- as.numeric(substr(sif,74+d,75+d))
    #  nbN <- as.numeric(substr(sif,77+d,78+d))
    #  nbH <- as.numeric(substr(sif,80+d,81+d))
    #  nbI <- as.numeric(substr(sif,83+d,84+d))
    
    sif["nbF"] = sif["sif"].str[64+d:66+d]
    sif["nbG"] = sif["sif"].str[67+d:69+d]
    sif["nbR"] = sif["sif"].str[70+d:72+d]
    sif["nbJ"] = sif["sif"].str[73+d:75+d]
    sif["nbN"] = sif["sif"].str[76+d:78+d]
    sif["nbH"] = sif["sif"].str[79+d:81+d]
    sif["nbI"] = sif["sif"].str[82+d:84+d]
    
    #  if (year != 2009){
    #  nbP <- as.numeric(substr(sif,86+d,87+d))
    #  }
    #})
    
    if (year != 2009):
        sif["nbP"] = sif["sif"].str[85+d:87+d]
    
    #sif$sif <- NULL
    #sif$stamar <- NULL
    #
    
    del sif["sif"], sif["stamar"]
    
    
    #table(sif$statmarit)
    print sif["statmarit"].value_counts()
    
    #print(length(table(sif$noindiv)))
    print "Number of individuals :", len(sif["noindiv"])
    print "Number of distinct individuals :", len(sif["noindiv"].value_counts())
    
    #dup <- duplicated(sif$noindiv)
    #table(dup)
    #sif <- sif[!dup,]
    #print(length(table(sif$noindiv)))
    
    sif_drop_duplicated = sif.drop_duplicates("noindiv")
    assert len(sif["noindiv"].value_counts()) == len(sif_drop_duplicated["noindiv"]), Exception("Number of distinct individuals after removing duplicates is not correct")
    
    print 'Saving sif'
    save_temp(sif, name='sif', year=year)
    del sif
    gc.collect()
    #saveTmp(sif, file = 'sif.Rdata')
    #rm(sif)
    #gc()
    ##################################################################


def foyer_all(year=2006):

    ## On ajoute les cases de la déclaration
    #foyer_all <- LoadIn(erfFoyFil)
    data = DataCollection(year=year)
    foyer_all = data.get_values(table="foyer" )
    
    ## on ne garde que les cases de la déclaration ('fxzz')
    #vars <- names(foyer_all)
    #vars <- c("noindiv", vars[grep("^f[0-9]", vars)])
    #
    
    vars = foyer_all.columns
    regex = re.compile("^f[0-9]")
    vars = [x for x in vars if regex.match(x)]
    
    #foyer <- foyer_all[vars]
    #rm(foyer_all)
    #gc()
    #noindiv <- list(foyer$noindiv)
    #

    foyer = foyer_all[vars + ["noindiv"]]

    del foyer_all
    gc.collect()
    
    #
    ## On aggrège les déclarations dans le cas où un individu a fait plusieurs déclarations
    #foyer <- aggregate(foyer, by = noindiv, FUN = 'sum')
    #print foyer.describe()["f1aj"].to_string()
    foyer = foyer.groupby("noindiv", as_index=False).aggregate(numpy.sum)
    #
    #print foyer.describe()["f1aj"].to_string()
    #print foyer.describe()["noindiv"].to_string()
    #

    print_id(foyer)

    ## noindiv have been summed over original noindiv which are now in Group.1
    #foyer$noindiv <- NULL
    #foyer <- rename(foyer, c(Group.1 = 'noindiv'))
    ## problème avec les dummies ()
    #
    #saveTmp(foyer, file= "foyer_aggr.Rdata")
    #
    #
    #############################################################################
    ## On récupère les variables individualisables
    #loadTmp("foyer_aggr.Rdata")
    #
    #individualisable <- function(table, var, vars, qui){
    #  print(var)
    #  print(vars)
    #  temp <- table[c('noindiv', vars)]
    #  n = length(qui)
    #  names(temp)[2:(n+1)] <- qui
    #  temp$newvar <- NULL
    #  temp2 <- melt(temp, id = 'noindiv', variable_name = 'quifoy')
    #  temp2 <- transform(temp2, quifoy = as.character(quifoy))
    #  temp2 <- transform(temp2, noindiv = as.character(noindiv))
    #  str(temp2)
    #  rename(temp2, c(value = var))
    #}
    
    
    var_dict = {'sali': ['f1aj', 'f1bj', 'f1cj', 'f1dj', 'f1ej'],
                'choi': ['f1ap', 'f1bp', 'f1cp', 'f1dp', 'f1ep'],
               'fra': ['f1ak', 'f1bk', 'f1ck', 'f1dk', 'f1ek'],
               'cho_ld': ['f1ai', 'f1bi', 'f1ci', 'f1di', 'f1ei'],
               'ppe_tp_sa': ['f1ax', 'f1bx', 'f1cx', 'f1dx', 'f1qx'],
               'ppe_du_sa': ['f1av', 'f1bv', 'f1cv', 'f1dv', 'f1qv'],
               'rsti': ['f1as', 'f1bs', 'f1cs', 'f1ds', 'f1es'],
               'alr': ['f1ao', 'f1bo', 'f1co', 'f1do', 'f1eo'], 
               'f1tv': ['f1tv', 'f1uv'], 
               'f1tw': ['f1tw', 'f1uw'], 
               'f1tx': ['f1tx', 'f1ux'], 
               'ppe_tp_ns': ['f5nw', 'f5ow', 'f5pw'],
               'ppe_du_ns':  ['f5nv', 'f5ov', 'f5pv'],
               'frag_exon': ['f5hn', 'f5in', 'f5jn'],
               'frag_impo': ['f5ho', 'f5io', 'f5jo'],    
               'arag_exon': ['f5hb', 'f5ib', 'f5jb'],
               'arag_impg': ['f5hc', 'f5ic', 'f5jc'],
               'arag_defi': ['f5hf', 'f5if', 'f5jf'],
               'nrag_exon': ['f5hh', 'f5ih', 'f5jh'],
               'nrag_impg': ['f5hi', 'f5ii', 'f5ji'],
               'nrag_defi': ['f5hl', 'f5il', 'f5jl'],
               'nrag_ajag': ['f5hm', 'f5im', 'f5jm'], 
               'mbic_exon': ['f5kn', 'f5ln', 'f5mn'],
               'abic_exon': ['f5kb', 'f5lb', 'f5mb'],
               'nbic_exon': ['f5kh', 'f5lh', 'f5mh'],
               'mbic_impv': ['f5ko', 'f5lo', 'f5mo'],
               'mbic_imps': ['f5kp', 'f5lp', 'f5mp'],
               'abic_impn': ['f5kc', 'f5lc', 'f5mc'],
               'abic_imps': ['f5kd', 'f5ld', 'f5md'],
               'nbic_impn': ['f5ki', 'f5li', 'f5mi'],
               'nbic_imps': ['f5kj', 'f5lj', 'f5mj'],
               'abic_defn': ['f5kf', 'f5lf', 'f5mf'],
               'abic_defs': ['f5kg', 'f5lg', 'f5mg'],
               'nbic_defn': ['f5kl', 'f5ll', 'f5ml'],
               'nbic_defs': ['f5km', 'f5lm', 'f5mm'],
               'nbic_apch': ['f5ks', 'f5ls', 'f5ms'],
               'macc_exon': ['f5nn', 'f5on', 'f5pn'],
               'aacc_exon': ['f5nb', 'f5ob', 'f5pb'],
               'nacc_exon': ['f5nh', 'f5oh', 'f5ph'],
               'macc_impv': ['f5no', 'f5oo', 'f5po'],
               'macc_imps': ['f5np', 'f5op', 'f5pp'],
               'aacc_impn': ['f5nc', 'f5oc', 'f5pc'],
               'aacc_imps': ['f5nd', 'f5od', 'f5pd'],
               'aacc_defn': ['f5nf', 'f5of', 'f5pf'],
               'aacc_defs': ['f5ng', 'f5og', 'f5pg'],
               'nacc_impn': ['f5ni', 'f5oi', 'f5pi'],
               'nacc_imps': ['f5nj', 'f5oj', 'f5pj'],
               'nacc_defn': ['f5nl', 'f5ol', 'f5pl'],
               'nacc_defs': ['f5nm', 'f5om', 'f5pm'],
               'mncn_impo': ['f5ku', 'f5lu', 'f5mu'],
               'cncn_bene': ['f5sn', 'f5ns', 'f5os'],
               'cncn_defi': ['f5sp', 'f5nu', 'f5ou', 'f5sr'], # TODO: check
               'mbnc_exon': ['f5hp', 'f5ip', 'f5jp'],
               'abnc_exon': ['f5qb', 'f5rb', 'f5sb'],
               'nbnc_exon': ['f5qh', 'f5rh', 'f5sh'],
               'mbnc_impo': ['f5hq', 'f5iq', 'f5jq'],
               'abnc_impo': ['f5qc', 'f5rc', 'f5sc'],
               'abnc_defi': ['f5qe', 'f5re', 'f5se'],
               'nbnc_impo': ['f5qi', 'f5ri', 'f5si'],
               'nbnc_defi': ['f5qk', 'f5rk', 'f5sk'],
               'mbic_mvct': ['f5hu'],
               'macc_mvct': ['f5iu'],
               'mncn_mvct': ['f5ju'],
               'mbnc_mvct': ['f5kz'],           
               'frag_pvct': ['f5hw', 'f5iw', 'f5jw'],
               'mbic_pvct': ['f5kx', 'f5lx', 'f5mx'],
               'macc_pvct': ['f5nx', 'f5ox', 'f5px'],
               'mbnc_pvct': ['f5hv', 'f5iv', 'f5jv'],
               'mncn_pvct': ['f5ky', 'f5ly', 'f5my'],
               'mbic_mvlt': ['f5kr', 'f5lr', 'f5mr'],
               'macc_mvlt': ['f5nr', 'f5or', 'f5pr'],
               'mncn_mvlt': ['f5kw', 'f5lw', 'f5mw'],
               'mbnc_mvlt': ['f5hs', 'f5is', 'f5js'],
               'frag_pvce': ['f5hx', 'f5ix', 'f5jx'],
               'arag_pvce': ['f5he', 'f5ie', 'f5je'],
               'nrag_pvce': ['f5hk', 'f5lk', 'f5jk'],
               'mbic_pvce': ['f5kq', 'f5lq', 'f5mq'],
               'abic_pvce': ['f5ke', 'f5le', 'f5me'],
               'nbic_pvce': ['f5kk', 'f5ik', 'f5mk'],
               'macc_pvce': ['f5nq', 'f5oq', 'f5pq'],
               'aacc_pvce': ['f5ne', 'f5oe', 'f5pe'],
               'nacc_pvce': ['f5nk', 'f5ok', 'f5pk'],
               'mncn_pvce': ['f5kv', 'f5lv', 'f5mv'],
               'cncn_pvce': ['f5so', 'f5nt', 'f5ot'],
               'mbnc_pvce': ['f5hr', 'f5ir', 'f5jr'],
               'abnc_pvce': ['f5qd', 'f5rd', 'f5sd'],
               'nbnc_pvce': ['f5qj', 'f5rj', 'f5sj'],
               'demenage' : ['f1ar', 'f1br', 'f1cr', 'f1dr', 'f1er']}  # (déménagement) uniquement en 2006
   

#
#varlist = list(list('sali', c('f1aj', 'f1bj', 'f1cj', 'f1dj', 'f1ej')),
#                list('choi', c('f1ap', 'f1bp', 'f1cp', 'f1dp', 'f1ep')),
#               list('fra', c('f1ak', 'f1bk', 'f1ck', 'f1dk', 'f1ek')),
# ......
#               list('mbnc_pvce', c('f5hr', 'f5ir', 'f5jr')),
#               list('abnc_pvce', c('f5qd', 'f5rd', 'f5sd')),
#               list('nbnc_pvce', c('f5qj', 'f5rj', 'f5sj')),
#               list('demenage' , c('f1ar', 'f1br', 'f1cr', 'f1dr', 'f1er'))) # (déménagement) uniquement en 2006
#
    vars_sets = [ set(var_list) for var_list in var_dict.values() ]
    eligible_vars = (set().union(*vars_sets)).intersection( set(list(foyer.columns)))

    print "From %i variables, we keep %i eligibles variables"   %( len(set().union(*vars_sets)), len(eligible_vars))
    qui = ['vous', 'conj', 'pac1', 'pac2', 'pac3']
    err = 0
    err_vars = {}
    
    foy_ind = DataFrame()
    
    for individual_var, foyer_vars in var_dict.iteritems():
        try:
            selection = foyer[foyer_vars + ["noindiv"]]
        except KeyError:
            # Testing if at least one variable of foyers_vars is in the eligible list
            presence = [ x  in eligible_vars for x in foyer_vars ]
            var_present = any(presence)
            if not var_present:
                print individual_var + " is not present"
                continue
            else:
                # Shrink the list
                foyer_vars_cleaned = [var for var,present in zip(foyer_vars, presence) if present is True]                    
                selection = foyer[foyer_vars_cleaned + ["noindiv"]]

        # Reshape the dataframe        
        selection.rename(columns=dict(zip(foyer_vars, qui)), inplace=True)
        selection.set_index("noindiv", inplace=True)
        selection.columns.name = "quifoy"

        selection = selection.stack()
        selection.name = individual_var
        selection = selection.reset_index() # A Series cannot see its index resetted to produce a DataFrame
        selection = selection.set_index(["quifoy", "noindiv"])
        selection = selection[selection[individual_var] !=0]
#        print len(selection)
        
        if len(foy_ind) == 0:
            foy_ind = selection
        else:

            foy_ind = concat([foy_ind, selection], axis=1, join='outer')
    
    foy_ind.reset_index(inplace=True)
    
    print "foy_ind"
    print foy_ind.describe().to_string()

    
#not_first <- FALSE
#allvars = c()
#for (v in varlist){ 
#  vars = intersect(v[[2]],names(foyer)) # to deal with variabes that are not present
#  if (length(vars) > 0) {
#    allvars <-  c(allvars, vars) 
#    qui <- c('vous', 'conj', 'pac1', 'pac2', 'pac3')
#    n <- length(vars)
#    temp <- individualisable(foyer, v[[1]], vars, qui[1:n])
#    if (not_first) {
#      print('merge')
#      foy_ind <- merge(temp, foy_ind, by = c('noindiv', 'quifoy'), all = TRUE)
#      names(foy_ind)
#    }
#    else   {
#      print('init')
#      foy_ind <- temp
#      not_first <- TRUE
#    }
#  }
#}    

    ind_vars_to_remove = Series(list(eligible_vars))
    save_temp(ind_vars_to_remove, name='ind_vars_to_remove', year=year)
    foy_ind.rename(columns={"noindiv" : "idfoy"}, inplace=True)
    
    print_id(foy_ind)
    foy_ind['quifoy'][foy_ind['quifoy']=='vous'] = 0
    foy_ind['quifoy'][foy_ind['quifoy']=='conj'] = 1
    foy_ind['quifoy'][foy_ind['quifoy']=='pac1'] = 2
    foy_ind['quifoy'][foy_ind['quifoy']=='pac2'] = 3
    foy_ind['quifoy'][foy_ind['quifoy']=='pac3'] = 4
    
    assert foy_ind['quifoy'].isin(range(5)).all(), 'présence de valeurs aberrantes dans quifoy'

    print 'saving foy_ind'
    print_id(foy_ind)    
    save_temp(foy_ind, name="foy_ind", year = year)
    show_temp()
    return
    
#names(foy_ind)
#rm(temp,foyer)
#
#saveTmp(allvars, file = "allvars.Rdata")
#foy_ind <- rename(foy_ind, c(noindiv = "idfoy"))
#saveTmp(foy_ind, file= "foyer_individualise.Rdata")
#rm(foy_ind)


if __name__ == '__main__':
    year = 2006
    sif(year=year)
    foyer_all(year=year)
