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

from src.countries.france.data.erf.datatable import ErfsDataTable
from pandas.tools.pivot import pivot_table
year = 2006
df = ErfsDataTable(year=year)

print u"05_foyer: extraction des données foyer"
## TODO Comment choisir le rfr n -2 pour éxonération de TH ?
## mnrvka  Revenu TH n-2
## mnrvkh  revenu TH (revenu fiscal de référence)
#
## On récupère les variables du code sif
#vars <- c("noindiv", 'sif', "nbptr", "mnrvka")
vars = ["noindiv", 'sif', "nbptr", "mnrvka", "rbg", "tsrvbg"]
#sif <- LoadIn(erfFoyFil, vars)
sif = df.get_values(variables=vars, table="foyer" )
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
#print sif["rbg"].describe()
#sif["rbg"] = sif["rbg"]*( (sif["tsrvbg"] =='+')-(sif["tsrvbg"] =='-'))
#print sif["rbg"].describe()

#  stamar <- substr(sif,5,5)

sif["stamar"] = sif["sif"].apply(lambda x: str(x)[4:5])

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

sif["birthvous"] = sif["sif"].apply(lambda x: str(x)[5:9])
sif["birthconj"] = sif["sif"].apply(lambda x: str(x)[10:14])

#  caseE <- as.numeric(substr(sif,16,16)=='E')
#  caseF <- as.numeric(substr(sif,17,17)=='F')
#  caseG <- as.numeric(substr(sif,18,18)=='G')
#  caseK <- as.numeric(substr(sif,19,19)=='K')

sif["caseE"] = sif["sif"].apply(lambda x: str(x)[15:16]) == "E"
sif["caseF"] = sif["sif"].apply(lambda x: str(x)[16:17]) == "F"
sif["caseG"] = sif["sif"].apply(lambda x: str(x)[17:18]) == "G"
sif["caseK"] = sif["sif"].apply(lambda x: str(x)[18:19]) == "K"
## TODO: dtype conversion

#  d = 0
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
    sif["caseL"] = sif["sif"].apply(lambda x: str(x)[19:20]) == "L"
    sif["caseP"] = sif["sif"].apply(lambda x: str(x)[20:21]) == "P"
    sif["caseS"] = sif["sif"].apply(lambda x: str(x)[21:22]) == "S"
    sif["caseW"] = sif["sif"].apply(lambda x: str(x)[22:23]) == "W"
    sif["caseN"] = sif["sif"].apply(lambda x: str(x)[23:24]) == "N"
    sif["caseH"] = sif["sif"].apply(lambda x: str(x)[24:28])
    sif["caseT"] = sif["sif"].apply(lambda x: str(x)[28:29]) == "T"
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
    sif["caseP"] = sif["sif"].apply(lambda x: str(x)[20+d:21+d]) == "P"
    sif["caseS"] = sif["sif"].apply(lambda x: str(x)[21+d:22+d]) == "S"
    sif["caseW"] = sif["sif"].apply(lambda x: str(x)[22+d:23+d]) == "W"
    sif["caseN"] = sif["sif"].apply(lambda x: str(x)[23+d:24+d]) == "N"
    sif["caseH"] = sif["sif"].apply(lambda x: str(x)[24+d:28+d])
    sif["caseT"] = sif["sif"].apply(lambda x: str(x)[28+d:29+d]) == "T"

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
    sif["caseL"] = sif["sif"].apply(lambda x: str(x)[19:20]) == "L"
    sif["caseP"] = sif["sif"].apply(lambda x: str(x)[20:21]) == "P"
    sif["caseS"] = sif["sif"].apply(lambda x: str(x)[21:22]) == "S"
    sif["caseW"] = sif["sif"].apply(lambda x: str(x)[22:23]) == "W"
    sif["caseN"] = sif["sif"].apply(lambda x: str(x)[23:24]) == "N"
    # caseH en moins par rapport à 2008 (mais case en L en plus)
    # donc décalage par rapport à 2006
    d = -4
    sif["caseT"] = sif["sif"].apply(lambda x: str(x)[28+d:29+d]) == "T"


#
#  caseX <- as.numeric(substr(sif,34+d,34+d)=='X')
#  dateX <- as.Date(substr(sif,35+d,42+d),'%d%m%Y')
#  caseY <- as.numeric(substr(sif,43+d,43+d)== 'Y')
#  dateY <- as.Date(substr(sif,44+d,51+d),'%d%m%Y')
#  caseZ <- as.numeric(substr(sif,52+d,53+d)== 'Z')
#  dateZ <- as.Date(substr(sif,53+d,60+d),'%d%m%Y')  # ERROR 54+d
#  causeXYZ <- substr(sif,61+d,61+d)
#

sif["caseX"] = sif["sif"].apply(lambda x: str(x)[33+d:34+d]) == "X"
sif["dateX"] = sif["sif"].apply(lambda x: str(x)[34+d:42+d])
sif["caseY"] = sif["sif"].apply(lambda x: str(x)[42+d:43+d]) == "Y"
sif["dateY"] = sif["sif"].apply(lambda x: str(x)[43+d:51+d]) 
sif["caseZ"] = sif["sif"].apply(lambda x: str(x)[51+d:53+d]) == "Z"
sif["dateZ"] = sif["sif"].apply(lambda x: str(x)[53+d:60+d]) 
sif["causeXYZ"] = sif["sif"].apply(lambda x: str(x)[60+d:61+d])

# TODO: convert dateWYZ to appropraite date in pandas
# print sif["dateY"].unique()

#print sif.describe()
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

sif["nbF"] = sif["sif"].apply(lambda x: str(x)[64+d:66+d])
sif["nbG"] = sif["sif"].apply(lambda x: str(x)[67+d:69+d])
sif["nbR"] = sif["sif"].apply(lambda x: str(x)[70+d:72+d])
sif["nbJ"] = sif["sif"].apply(lambda x: str(x)[73+d:75+d])
sif["nbN"] = sif["sif"].apply(lambda x: str(x)[76+d:78+d])
sif["nbH"] = sif["sif"].apply(lambda x: str(x)[79+d:81+d])
sif["nbI"] = sif["sif"].apply(lambda x: str(x)[82+d:84+d])

#  if (year != 2009){
#  nbP <- as.numeric(substr(sif,86+d,87+d))
#  }
#})

if (year != 2009):
    sif["nbP"] = sif["sif"].apply(lambda x: str(x)[85+d:87+d])

#sif$sif <- NULL
#sif$stamar <- NULL
#

del sif["sif"], sif["stamar"]

# RESTART HERE
#table(sif$statmarit)
print sif["statmarit"].value_counts()
print "nombre d'individu différents :", len(sif["noindiv"].value_counts())
#print(length(table(sif$noindiv)))
print len(pivot_table(sif['noindiv']))

#dup <- duplicated(sif$noindiv)
#table(dup)
dup = sif.noindiv.duplicated
#sif <- sif[!dup,]
sif = sif["dup"] == False
#print(length(table(sif$noindiv)))
#
#saveTmp(sif, file = 'sif.Rdata')
#rm(sif)
#gc()
##################################################################
## On ajoute les cases de la déclaration
#foyer_all <- LoadIn(erfFoyFil)
## on ne garde que les cases de la déclaration ('fxzz')
#vars <- names(foyer_all)
#vars <- c("noindiv", vars[grep("^f[0-9]", vars)])
#
#foyer <- foyer_all[vars]
#rm(foyer_all)
#gc()
#noindiv <- list(foyer$noindiv)
#
## On aggrège les déclarations dans le cas où un individu a fait plusieurs déclarations
#foyer <- aggregate(foyer, by = noindiv, FUN = 'sum')
#
## TODO super lent essayer avec http://stackoverflow.com/questions/3685492/r-speeding-up-group-by-operations/3685919#3685919
## library(data.table)
## dtb <- data.table(foyer, key="noindiv")
#
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
#
#varlist = list(list('sali', c('f1aj', 'f1bj', 'f1cj', 'f1dj', 'f1ej')),
#                list('choi', c('f1ap', 'f1bp', 'f1cp', 'f1dp', 'f1ep')),
#               list('fra', c('f1ak', 'f1bk', 'f1ck', 'f1dk', 'f1ek')),
#               list('cho_ld', c('f1ai', 'f1bi', 'f1ci', 'f1di', 'f1ei')),
#               list('ppe_tp_sa', c('f1ax', 'f1bx', 'f1cx', 'f1dx', 'f1qx')),
#               list('ppe_du_sa', c('f1av', 'f1bv', 'f1cv', 'f1dv', 'f1qv')),
#               list('rsti', c('f1as', 'f1bs', 'f1cs', 'f1ds', 'f1es')),
#               list('alr', c('f1ao', 'f1bo', 'f1co', 'f1do', 'f1eo')), 
#
#               list('ppe_tp_ns', c('f5nw', 'f5ow', 'f5pw')),
#               list('ppe_du_ns',  c('f5nv', 'f5ov', 'f5pv')),
#            
#               
#               list('frag_exon', c('f5hn', 'f5in', 'f5jn')),
#               list('frag_impo', c('f5ho', 'f5io', 'f5jo')),    
#               list('arag_exon', c('f5hb', 'f5ib', 'f5jb')),
#               list('arag_impg', c('f5hc', 'f5ic', 'f5jc')),
#               list('arag_defi', c('f5hf', 'f5if', 'f5jf')),
#               list('nrag_exon', c('f5hh', 'f5ih', 'f5jh')),
#               list('nrag_impg', c('f5hi', 'f5ii', 'f5ji')),
#               list('nrag_defi', c('f5hl', 'f5il', 'f5jl')),
#               list('nrag_ajag', c('f5hm', 'f5im', 'f5jm')),
#           
#               list('mbic_exon', c('f5kn', 'f5ln', 'f5mn')),
#               list('abic_exon', c('f5kb', 'f5lb', 'f5mb')),
#               list('nbic_exon', c('f5kh', 'f5lh', 'f5mh')),
#               list('mbic_impv', c('f5ko', 'f5lo', 'f5mo')),
#               list('mbic_imps', c('f5kp', 'f5lp', 'f5mp')),
#               list('abic_impn', c('f5kc', 'f5lc', 'f5mc')),
#               list('abic_imps', c('f5kd', 'f5ld', 'f5md')),
#               list('nbic_impn', c('f5ki', 'f5li', 'f5mi')),
#               list('nbic_imps', c('f5kj', 'f5lj', 'f5mj')),
#               list('abic_defn', c('f5kf', 'f5lf', 'f5mf')),
#               list('abic_defs', c('f5kg', 'f5lg', 'f5mg')),
#               list('nbic_defn', c('f5kl', 'f5ll', 'f5ml')),
#               list('nbic_defs', c('f5km', 'f5lm', 'f5mm')),
#               list('nbic_apch', c('f5ks', 'f5ls', 'f5ms')),
#           
#               list('macc_exon', c('f5nn', 'f5on', 'f5pn')),
#               list('aacc_exon', c('f5nb', 'f5ob', 'f5pb')),
#               list('nacc_exon', c('f5nh', 'f5oh', 'f5ph')),
#               list('macc_impv', c('f5no', 'f5oo', 'f5po')),
#               list('macc_imps', c('f5np', 'f5op', 'f5pp')),
#               list('aacc_impn', c('f5nc', 'f5oc', 'f5pc')),
#               list('aacc_imps', c('f5nd', 'f5od', 'f5pd')),
#               list('aacc_defn', c('f5nf', 'f5of', 'f5pf')),
#               list('aacc_defs', c('f5ng', 'f5og', 'f5pg')),
#               list('nacc_impn', c('f5ni', 'f5oi', 'f5pi')),
#               list('nacc_imps', c('f5nj', 'f5oj', 'f5pj')),
#               list('nacc_defn', c('f5nl', 'f5ol', 'f5pl')),
#               list('nacc_defs', c('f5nm', 'f5om', 'f5pm')),
#               list('mncn_impo', c('f5ku', 'f5lu', 'f5mu')),
#               list('cncn_bene', c('f5sn', 'f5ns', 'f5os')),
#               list('cncn_defi', c('f5sp', 'f5nu', 'f5ou', 'f5sr')), # TODO
#           
#               list('mbnc_exon', c('f5hp', 'f5ip', 'f5jp')),
#               list('abnc_exon', c('f5qb', 'f5rb', 'f5sb')),
#               list('nbnc_exon', c('f5qh', 'f5rh', 'f5sh')),
#               list('mbnc_impo', c('f5hq', 'f5iq', 'f5jq')),
#               list('abnc_impo', c('f5qc', 'f5rc', 'f5sc')),
#               list('abnc_defi', c('f5qe', 'f5re', 'f5se')),
#               list('nbnc_impo', c('f5qi', 'f5ri', 'f5si')),
#               list('nbnc_defi', c('f5qk', 'f5rk', 'f5sk')),
#           
#               list('mbic_mvct', c('f5hu')),
#               list('macc_mvct', c('f5iu')),
#               list('mncn_mvct', c('f5ju')),
#               list('mbnc_mvct', c('f5kz')),
#           
#               list('frag_pvct', c('f5hw', 'f5iw', 'f5jw')),
#               list('mbic_pvct', c('f5kx', 'f5lx', 'f5mx')),
#               list('macc_pvct', c('f5nx', 'f5ox', 'f5px')),
#               list('mbnc_pvct', c('f5hv', 'f5iv', 'f5jv')),
#               list('mncn_pvct', c('f5ky', 'f5ly', 'f5my')),
#           
#               list('mbic_mvlt', c('f5kr', 'f5lr', 'f5mr')),
#               list('macc_mvlt', c('f5nr', 'f5or', 'f5pr')),
#               list('mncn_mvlt', c('f5kw', 'f5lw', 'f5mw')),
#               list('mbnc_mvlt', c('f5hs', 'f5is', 'f5js')),
#           
#               list('frag_pvce', c('f5hx', 'f5ix', 'f5jx')),
#               list('arag_pvce', c('f5he', 'f5ie', 'f5je')),
#               list('nrag_pvce', c('f5hk', 'f5ik', 'f5jk')),
#               list('mbic_pvce', c('f5kq', 'f5lq', 'f5mq')),
#               list('abic_pvce', c('f5ke', 'f5le', 'f5me')),
#               list('nbic_pvce', c('f5kk', 'f5lk', 'f5mk')),
#               list('macc_pvce', c('f5nq', 'f5oq', 'f5pq')),
#               list('aacc_pvce', c('f5ne', 'f5oe', 'f5pe')),
#               list('nacc_pvce', c('f5nk', 'f5ok', 'f5pk')),
#               list('mncn_pvce', c('f5kv', 'f5lv', 'f5mv')),
#               list('cncn_pvce', c('f5so', 'f5nt', 'f5ot')),
#               list('mbnc_pvce', c('f5hr', 'f5ir', 'f5jr')),
#               list('abnc_pvce', c('f5qd', 'f5rd', 'f5sd')),
#               list('nbnc_pvce', c('f5qj', 'f5rj', 'f5sj')),
#               list('demenage' , c('f1ar', 'f1br', 'f1cr', 'f1dr', 'f1er'))) # (déménagement) uniquement en 2006
#
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
#names(foy_ind)
#rm(temp,foyer)
#
#saveTmp(allvars, file = "allvars.Rdata")
#foy_ind <- rename(foy_ind, c(noindiv = "idfoy"))
#saveTmp(foy_ind, file= "foyer_individualise.Rdata")
#rm(foy_ind)