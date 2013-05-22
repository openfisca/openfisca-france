# -*- coding:utf-8 -*-
# Created on 16 mai 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © #2013 Clément Schaff, Mahdi Ben Jelloul
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
from src.countries.france.data.erf.datatable import ErfsDataTable
from pandas import DataFrame
from numpy import array

year = 2006
df = ErfsDataTable(year=year)
df.set_config()
#erfmen <- LoadIn(erfMenFil)
erfmen = df.get_values(table="erf_menage")

#eecmen <- LoadIn(eecMenFil)
eecmen = df.get_values(table="eec_menage")
#
#eecmen$locataire <- ifelse(eecmen$so %in% c(3,4,5),1,0)
eecmen["locataire"] = eecmen["so"].isin([3,4,5])
eecmen["locataire"] = eecmen["locataire"].astype("int32")
print eecmen["locataire"].dtype
print eecmen["locataire"].describe()

#noappar_m <- eecmen[!eecmen$ident %in%  erfmen$ident,]
#
#erfind <- LoadIn(erfIndFil)
#eecind <- LoadIn(eecIndFil)
erfind = df.get_values(table="erf_individu")
print erfind
eecind = df.get_values(table="eec_individu")
print eecind
#
#transfert <- subset(eecind, lpr==1, select=c("ident","ddipl"))
transfert = eecind.loc(array(eecind.index.get_level_values(1) == 1), ['ident', 'ddipl']) #TODO: soumettre à Mahdi pour vérification

#noappar_i <- eecind[!eecind$noindiv %in%  erfind$noindiv,]
#noappar_i <- noappar_i[!duplicated(noappar_i$ident),]
noappar_i = array([x not in erfind['noindiv'] for x in eecind['noindiv']])
noappar_i = noappar_i.delete() #How do you do the removal of duplicated elements ??


# Vérification que les non-appariés sont les mêmes pour les tables individus 
# et les tables ménages
#dif <- setdiff(noappar_i$ident,noappar_m$ident)
#int <- intersect(noappar_i$ident,noappar_m$ident)
dif = set(noappar_i.ident).symmetric_difference(noappar_m.ident)
int = set(noappar_i.ident) & set(noappar_m.ident)


#str(dif);str(int)
str(dif) ; str(int)
#rm(noappar_i,noappar_m,dif,int)
#rm(noappar_i, noappar_m, dif, int) #TODO: What do your want to remove

#gc() # TODO : do we have garbage collection ?


#menagem <- merge(erfmen,eecmen)
#menagem <- merge(menagem,transfert)
menagem = erfmen.merge(eecmen)
menagem  = menagem.merge(transfert)

#save(menagem,file=menm) #TODO: Save in h5 ?

#rm(erfmen,eecmen,menagem,transfert)
#message('menagem saved')
#gc()
#
#
# int = intersect(names(erfind),names(eecind))
int = erfind.columns & eecind.columns
print int

## Uncomparable tu99 in 2009 ! TODO remove tu99 in one of them 
#if (year == 2009){
#  erfind$tu99 <- NULL
#  eecind$tu99 <- as.numeric(eecind$tu99)
#}
#indivim <- merge(eecind,erfind, by = c("noindiv","ident","noi"))
indivim = eecind.merge(erfind, on = ['noindiv', 'ident', 'noi'])
#
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
# TODO 2003 voir guide méthodo page 170 
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
    print var
    indivim[var] = float(indivim[var])

#TODO: est_ce une boucle ou autre-chose
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
#
#
#
#save(indivim,file=indm)
#rm(erfind,eecind,indivim)
#message('indivim saved')
#gc()
#
#
#
### Enfant à naître (NN pour nouveaux nés)
#
#indVar = c('noi','noicon','noindiv','noiper','noimer','ident','naia','naim','lien','acteu','stc','contra','titc','mrec',
#           'forter','rstg','retrai','lpr','cohab','sexe','agepr','rga')
#
#
#eeccmp1 <- LoadIn(eecCmp1Fil,indVar)
#eeccmp2 <- LoadIn(eecCmp2Fil,indVar)
#eeccmp3 <- LoadIn(eecCmp3Fil,indVar)
#enfnn <- rbind(eeccmp1,eeccmp2,eeccmp3)
#
#for (var in indVar) {
#  print(var)
#  enfnn[,var] <- as.numeric(enfnn[,var])
#}
#
#rm(eeccmp1,eeccmp2,eeccmp3,var_list)
#
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
#
#enfnn <- enfnn[(enfnn$naia==enfnn$year & enfnn$naim>=10) | (enfnn$naia==enfnn$year+1 & enfnn$naim<=5),]
#
#save(enfnn,file=enfnnm)
#
#rm(enfnn)
#message('enfnnm saved')
#gc()