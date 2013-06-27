# -*- coding:utf-8 -*-
# Created on 21 mai 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)

from pandas import Series, concat, DataFrame
from numpy import (logical_or as or_, logical_not as not_,
                   logical_and as and_, sum, nan, where)
import gc

from src.countries.france.data.erf.datatable import DataCollection
from src.countries.france.data.erf.build_survey import show_temp, load_temp, save_temp
from src.countries.france.data.erf.build_survey.utilitaries import print_id, control

## On part de la table individu de l'ERFS
## on renomme les variables
#load(indm)

def create_totals(year=2006):
    
    print "Creating Totals"
    print "Etape 1 : Chargement des données"
    
    data = DataCollection(year=year)
    indivim = load_temp(name="indivim", year=year)
     
    assert indivim.duplicated(['noindiv']).any() == False, "Présence de doublons"


    # Deals individuals with imputed income : some individuals are in 'erf individu table' but 
    # not in the 'foyer' table. We need to create a foyer for them.
    
    #indivi_i <- subset(indivim,
    #                   zsali != zsalo | zchoi != zchoo |
    #                     zrsti != zrsto | zalri != zalro |  
    #                     zrtoi != zrtoo | zragi != zrago | 
    #                     zrici != zrico | zrnci != zrnco)
    ##   c(zsali,zchoi,ztsai,zreti,zperi,zrsti,zalri,zrtoi,zragi,zrici,zrnci,
    ##     quelfic,noi,ident,naia,noindiv))

    selection = Series()
    for var in ["zsali", "zchoi", "zrsti", "zalri", "zrtoi", "zragi", "zrici", "zrnci"]:
        varo = var[:-1]+"o"
        test = indivim[var] != indivim[varo]
        if len(selection) == 0:
            selection = test
        else:
            selection = or_(test, selection)

#indivi_i <- rename(indivi_i, c(ident = "idmen",
#                               persfip="quifoy",  
#                               zsali = "sali2", # Inclu les salaires non imposables des agents d'assurance
#                               zchoi = "choi2", 
#                               zrsti = "rsti2",
#                               zalri = "alr2"))
#

    indivi_i = indivim[selection] 
    indivi_i.rename(columns={"ident" : "idmen",
                     "persfip":"quifoy",  
                     "zsali" : "sali2", # Inclu les salaires non imposables des agents d'assurance
                     "zchoi" : "choi2", 
                     "zrsti" : "rsti2",
                     "zalri" : "alr2"}, inplace=True)
    
#indivi_i <- within(indivi_i, {
#  quifoy <- ifelse(is.na(quifoy),"vous",quifoy)
#  quelfic <- "FIP_IMP"})
#
#    

    indivi_i["quifoy"] = where(indivi_i["quifoy"].isnull(), "vous", indivi_i["quifoy"])
    indivi_i["quelfic"] = "FIP_IMP"
    
    

## We merge them with the other individuals
#indivim <- rename(indivim, c(ident = "idmen",
#                             persfip = "quifoy",                              
#                             zsali = "sali2", # Inclu les salaires non imposables des agents d'assurance
#                             zchoi = "choi2", 
#                             zrsti = "rsti2",
#                             zalri = "alr2"))
#
#indivi <- rbind(indivim[!(indivim$noindiv %in% indivi_i$noindiv),], indivi_i)
#rm(indivim, indivi_i)
#gc()
#table(indivi$quelfic)
#
    
    indivim.rename( columns= dict(ident = "idmen",
                             persfip = "quifoy",                              
                             zsali = "sali2", # Inclu les salaires non imposables des agents d'assurance
                             zchoi = "choi2", 
                             zrsti = "rsti2",
                             zalri = "alr2"), inplace=True)
    
    if not (set(list(indivim.noindiv)) >  set(list(indivi_i.noindiv)) ):
        raise Exception("Individual ")  
    indivim.set_index("noindiv", inplace=True)
    indivi_i.set_index("noindiv", inplace=True)
    indivi = indivim

    del indivim
    indivi.update(indivi_i)
    
    indivi.reset_index( inplace=True)



#indivi$idfoy <- NA
#
## On récupère le noi du déclarant dans le code de la déclaration
#fip_imp <- (indivi$quelfic=="FIP_IMP")
#indivi[!fip_imp, "idfoy"]  <- as.integer(indivi[!fip_imp, "idmen"])*100 + as.integer(substr(indivi[!fip_imp, "declar1"], 1, 2))
#
#
    print ''
    print "Etape 2 : isolation des FIP"
    fip_imp = indivi.quelfic=="FIP_IMP"
    indivi["idfoy"] = (indivi["idmen"].astype("int64")*100 + 
                       (indivi["declar1"].str[0:2]).convert_objects(convert_numeric=True))
    
    indivi.loc[fip_imp,"idfoy"] = nan
    
## Certains FIP (ou du moins avec revenus imput?s) ont un num?ro de d?claration d'imp?t ( pourquoi ?)
#fip_has_declar <- fip_imp  & (indivi$declar1!="")
#indivi[fip_has_declar, "idfoy"]  <- as.integer(indivi[fip_has_declar, "idmen"])*100 + as.integer(substr(indivi[fip_has_declar, "declar1"], 1, 2))
#rm(fip_has_declar)

    
    fip_has_declar = and_(fip_imp, indivi.declar1.notnull())

#    indivi.ix[fip_has_declar, "idfoy"] = ( indivi.ix[fip_has_declar, "idmen"]*100 
#                                        + (indivi.ix[fip_has_declar, "declar1"].str[0:1]).convert_objects(convert_numeric=True) )
    indivi["idfoy"] = where(fip_has_declar, 
                            indivi["idmen"]*100 + indivi["declar1"].str[0:2].convert_objects(convert_numeric=True),
                            indivi["idfoy"])
    
    del fip_has_declar
    
#
#fip_no_declar <- fip_imp  & (indivi$declar1=="")
#rm(fip_imp)
#indivi[fip_no_declar, "idfoy"]  <- as.integer(indivi[fip_no_declar, "idmen"])*100 + 50
#indivi_fnd <- indivi[fip_no_declar, c("idfoy","noindiv")]

    fip_no_declar = and_(fip_imp, indivi.declar1.isnull())
    del fip_imp
    indivi["idfoy"] = where(fip_no_declar, 
                            indivi["idmen"]*100 + 50,
                            indivi["idfoy"])
    
    indivi_fnd = indivi.loc[fip_no_declar, ["idfoy","noindiv"]]
    
## Some idfoy are duplicated ending with 50
#table(duplicated(indivi_fnd[,"idfoy"]))
## we remove the duplicated idfoy by introducing 51, 52 at the end of idfoy
#while ( any(duplicated( indivi_fnd[,"idfoy"]) ) ) {
#  dup <- duplicated( indivi_fnd[, "idfoy"])
#  tmp <- indivi_fnd[dup,"idfoy"]
#  indivi_fnd[dup, "idfoy"] <- (tmp+1)    
#}

    while any(indivi_fnd.duplicated(cols=["idfoy"])):
        indivi_fnd["idfoy"] = where(indivi_fnd.duplicated(cols=["idfoy"]),
                                    indivi_fnd["idfoy"] + 1,
                                    indivi_fnd["idfoy"])

#    print indivi_fnd.describe()
#    print indivi_fnd.head(10)
    # Check that there is no duplicated left
    assert indivi_fnd["idfoy"].duplicated().value_counts()[False] == len(indivi_fnd["idfoy"]), "Duplicates remaining"    
    assert len(indivi[indivi.duplicated(['noindiv'])]) == 0, "Doublons"

## we check there are some remaining duplicated individuals
#table(duplicated(indivi_fnd$idfoy))
#indivi[fip_no_declar, "idfoy"] <- indivi_fnd[,"idfoy"]
#rm(tmp,indivi_fnd, fip_no_declar)

    indivi.loc[fip_no_declar, ["idfoy"]] = indivi_fnd
    del indivi_fnd, fip_no_declar
#
#
## Il reste des individus qui ne sont ni EE&FIP ni FIP_IMP mais qui sont quelfic EE, EE_CAF, EE_NRT
#
## On crée une déclaration pour les individus dont on n'a pas retrouvé la déclaration d'impôts
## On va affecter ces individus à une déclaration (celle de leur parent ou la leur...)
#
## On crée des feuilles d'impots individuels pour les NRT qui sont normalement sur 
## la feuille de leurs parents (on peut également les éliminer ?)
#nrt <- indivi$quelfic=="EE_NRT"
#indivi[nrt,"idfoy"] <- indivi[nrt,"idmen"]*100 + indivi[nrt,"noi"]
#indivi[nrt,"quifoy"] <- "vous"
#rm(nrt)
#
    print ''
    print 'Etape 3 : Récupération des EE_NRT'
    
    nrt = indivi.quelfic=="EE_NRT"
    indivi.idfoy = where(nrt, indivi.idmen*100 + indivi.noi, indivi.idfoy)
    indivi.loc[nrt,"quifoy"] = "vous"
    del nrt

## On crée un identifiant foyer pour les personne de référence et leurs conjoints des quelfic EE, EE_CAF
#adults <- (indivi$quelfic %in% c("EE","EE_CAF")) & (indivi$lpr==1 | indivi$lpr==2) 
#
#indivi[adults,"idfoy"] <- indivi[adults,"idmen"]*100 + indivi[adults,"noi"]
#indivi[adults,"quifoy"] <- "vous"
#rm(adults)
## les lpr=1,2 sont desormais dans un foyer
#table(is.na(indivi[(indivi$lpr==1 | indivi$lpr==2),"idfoy"]),useNA="ifany")
#
    pref_or_cref = or_(indivi.lpr==1, indivi.lpr==2)
    adults = and_(indivi.quelfic.isin(["EE","EE_CAF"]),pref_or_cref)  
    indivi.idfoy = where(adults, indivi.idmen*100 + indivi.noi, indivi.idfoy)
    indivi.loc[adults, "quifoy"] = "vous"
    del adults
## les lpr=1,2 sont desormais dans un foyer
    assert indivi.loc[or_(indivi.lpr==1, indivi.lpr==2),"idfoy"].notnull().all()

## les lpr==4 sont essentiellement des enfants: on les rattache donc avec leurs parents/pref
#sum(( indivi$quelfic %in% c("EE","EE_CAF")) & (indivi$lpr==4) )
#table( indivi[(indivi$quelfic %in% c("EE","EE_CAF")) & (indivi$lpr==4),"naia"] )
#    print (indivi.loc[and_(indivi.quelfic.isin(["EE","EE_CAF"]), indivi.lpr==4), "naia"]).value_counts()

    

#
### On rattache les enfants à la feuille d'impôt de leurs parents:
## On affecte les enfants (et les lpr==4)  avec leur parent si elles sont monoparentales
## il faut faire un choix pour les autres : on rattache à celui qui paie le plus d'impôts 
#
#enf_ee <-  (indivi$quelfic %in% c("EE","EE_CAF")) & (indivi$lpr==3 | indivi$lpr==4)  
#
#noindper <- 100*indivi$idmen[enf_ee] + indivi$noiper[enf_ee] 
#noindmer <- 100*indivi$idmen[enf_ee] + indivi$noimer[enf_ee]
#length(noindper)
#idfoy <- NA*noindper
#is_pere_vous <- NA*noindper
#is_mere_vous <- NA*noindper
#zimpof_pere <- NA*noindper
#zimpof_mere <- NA*noindper
#foyer <- LoadIn(erfFoyFil,c("noindiv","zimpof"))
#
#
#for (i in 1:length(noindper)) {  
#  if (noindper[i] %in% indivi$noindiv) {
#    is_pere_vous[i] <- ifelse(!is.na(indivi[indivi$noindiv==noindper[i], "quifoy"]), 
#                              indivi[indivi$noindiv==noindper[i], "quifoy"]=="vous",FALSE)} 
#  else {is_pere_vous[i] <- FALSE}
#  if (noindmer[i] %in% indivi$noindiv) {
#    is_mere_vous[i] <- ifelse(!is.na(indivi[indivi$noindiv==noindmer[i], "quifoy"]),
#                              (indivi[indivi$noindiv==noindmer[i], "quifoy"]=="vous"),FALSE)} 
#  else {is_mere_vous[i] <- FALSE}
#  
#  zimpof_pere[i]  <- ifelse(is.na(noindper[i]) | !(noindper[i] %in% foyer$noindiv), 0, foyer[foyer$noindiv==noindper[i],"zimpof"])
#  zimpof_mere[i]  <- ifelse(is.na(noindmer[i]) | !(noindmer[i] %in% foyer$noindiv), 0, foyer[foyer$noindiv==noindmer[i],"zimpof"])
#}
#
#table(is_pere_vous,useNA="ifany")
#table(is_mere_vous,useNA="ifany")
#table(is.na(zimpof_pere))
#table(is.na(zimpof_mere))
#deux_parents <- (is_pere_vous & is_mere_vous)
#table(deux_parents,useNA="ifany")
#

#idfoy <- ifelse(!is.na(noindper),( (is_pere_vous & !deux_parents) | deux_parents*(zimpof_pere>=zimpof_mere))*noindper,0) +
#  ifelse(!is.na(noindmer),( (is_mere_vous & !deux_parents) | deux_parents*(zimpof_pere<zimpof_mere))*noindmer,0)
## les idfoy==0 sont en fait ind?termin?es  
#idfoy <- ifelse(idfoy==0,NA,idfoy)
#table(is.na(idfoy))
#indivi[enf_ee,"idfoy"] <- idfoy
#indivi[enf_ee,"quifoy"] <- 'pac'
#
#rm(deux_parents, is_pere_vous, is_mere_vous, noindper, noindmer, idfoy, zimpof_pere, zimpof_mere, foyer, enf_ee)
#
    print ''
    print 'Etape 4 : Rattachement des enfants aux déclarations'
    
    assert indivi["noindiv"].duplicated().any() == False, "Some noindiv appear twice"
    lpr3_or_lpr4 = or_(indivi.lpr==3, indivi.lpr==4)
    enf_ee = and_(indivi.quelfic.isin(["EE","EE_CAF"]), lpr3_or_lpr4)  
    assert indivi.loc[enf_ee, "noindiv"].notnull().all(), " Some noindiv are not set, which will ruin next stage"
    assert indivi.loc[enf_ee, "noindiv"].duplicated().any() == False, "Some noindiv appear twice"

    pere = DataFrame( {"noindiv_enf" : indivi.noindiv.loc[enf_ee], "noindiv" : 100*indivi.idmen.loc[enf_ee] + indivi.noiper.loc[enf_ee] })
    mere = DataFrame( {"noindiv_enf" : indivi.noindiv.loc[enf_ee], "noindiv" : 100*indivi.idmen.loc[enf_ee] + indivi.noimer.loc[enf_ee] })
    
    foyer = data.get_values(variables=["noindiv","zimpof"], table="foyer" )
    pere  = pere.merge(foyer, how="inner", on="noindiv")
    mere  = mere.merge(foyer, how="inner", on="noindiv")

#     print "Some pere et mere are duplicated because people have two foyers"
#     print pere[pere.duplicated()]
#     print mere[mere.duplicated()]

    df = pere.merge(mere, how="outer", on="noindiv_enf",  suffixes=('_p', '_m'))
    
#     print len(pere)
#     print len(mere)
#     print len(df)
#     ll = df.loc[df["noindiv_enf"].duplicated(), "noindiv_enf"]
#     print df.loc[df["noindiv_enf"].isin(ll)]
#     print df[df.duplicated()]



    print '    4.1 : gestion des personnes dans 2 foyers'
    for col in ["noindiv_p","noindiv_m","noindiv_enf"]:     
        df[col] = df[col].fillna(0,inplace=True) # beacause groupby drop groups with NA in index
    df = df.groupby(by=["noindiv_p","noindiv_m","noindiv_enf"]).sum()
    df.reset_index(inplace=True)

    df["which"] = ""
    df["which"] = where( and_(df.zimpof_m.notnull(), df.zimpof_p.isnull()), "mere", "")
    df["which"] = where( and_(df.zimpof_p.notnull(), df.zimpof_m.isnull()), "pere", "")
    both = and_(df.zimpof_p.notnull(), df.zimpof_m.notnull())
    df["which"] = where( and_(both, df.zimpof_p  > df.zimpof_m), "pere", "mere")
    df["which"] = where( and_(both, df.zimpof_m >= df.zimpof_p), "mere", "pere")
    
    assert df["which"].notnull().all(), "Some enf_ee individuals are not matched with any pere or mere"
    del lpr3_or_lpr4, pere, mere 
    
    df.rename(columns={"noindiv_enf" : "noindiv"}, inplace=True)
    df["idfoy"] = where( df.which=="pere", df.noindiv_p, df.noindiv_m)
    df["idfoy"] = where( df.which=="mere", df.noindiv_m, df.noindiv_p)
    
    assert df["idfoy"].notnull().all()
    
    for col in df.columns:
        if col not in ["idfoy", "noindiv"]:
            del df[col]

    assert indivi.loc[enf_ee,"idfoy"].isnull().all()
    assert df.duplicated().any() == False

    df.set_index("noindiv",inplace=True, verify_integrity=True)
    indivi.set_index("noindiv", inplace=True, verify_integrity=True)

    ind_notnull = indivi["idfoy"].notnull().sum()
    ind_isnull = indivi["idfoy"].isnull().sum()
    indivi = indivi.combine_first(df)
    assert ind_notnull + ind_isnull == (indivi["idfoy"].notnull().sum() + 
                                        indivi["idfoy"].isnull().sum())
        
    indivi.reset_index(inplace=True)
    assert indivi.duplicated().any() == False 




## On enlève les individus pour lesquels il manque le déclarant TODO: à améliorer (peut-être qu'il faut récupérer les deux feuilles d'impôts)
#sum(is.na(indivi$idfoy))
#table(indivi[is.na(indivi$idfoy),c('naia','lpr','quelfic')])
#indivi <- indivi[!is.na(indivi$idfoy),]

# MBJ: issue delt with when moving from R code to python 

#
## TODO il faut rajouterles enfants_fip et créer un ménage pour les majeurs
## On suit guide méthodo erf 2003 page 135
## On supprime les conjoints FIP et les FIP de 25 ans et plus;
## On conserve les enfants FIP de 19 à 24 ans;
## On supprime les FIP de 18 ans et moins, exceptés les FIP nés en 2002 dans un 
## ménage en 6ème interrogation car ce sont des enfants nés aprés la date d'enquète
## EEC que l'on ne retrouvera pas dans les EEC suivantes.
#
#
#load(fipDat)
#fip$declar <- NULL
#fip$agepf <- NULL
#
    print '    4.2 : On enlève les individus pour lesquels il manque le déclarant'
    fip = load_temp(name="fipDat", year=year)
    fip["declar"] = nan
    fip["agepf"] = nan

#fip <- upData(fip,drop=c("year","actrec","noidec"))
#fip <- rename(fip, c(ident = "idmen",
#                     persfip="quifoy",  
#                     zsali = "sali2", # Inclu les salaires non imposables des agents d'assurance
#                     zchoi = "choi2", 
#                     zrsti = "rsti2",
#                     zalri = "alr2"))
#


    fip.drop(["actrec", "year", "noidec"],axis=1)
    fip.naia = fip.naia.astype("int32")
    fip.rename( columns=dict(ident = "idmen",
                     persfip="quifoy",  
                     zsali = "sali2", # Inclu les salaires non imposables des agents d'assurance
                     zchoi = "choi2", 
                     zrsti = "rsti2",
                     zalri = "alr2"), inplace=True)

## TODO: We put the fip kids over 18 in an individual menage 
## (We should do it here because we need initial ident/idmen in famille TODO)
#
#
#is_fip_19_25 <- ((as.integer(year)-fip$naia-1)>=19)  & ((as.integer(year)-fip$naia-1)<25)

    is_fip_19_25 = and_((year-fip.naia-1)>=19, (year-fip.naia-1)<25)
#    print is_fip_19_25
#
## TODO: BUT for the time being we keep them in thier vous menage so the following lines are commented
## The idmen are of the form 60XXXX we use idmen 61XXXX, 62XXXX for the idmen of the kids over 18 and less than 25
##fip[is_fip_19_25 ,"idmen"] <- (99-fip[is_fip_19_25,"noi"]+1)*100000 + fip[is_fip_19_25,"idmen"]
##fip[is_fip_19_25 ,"lpr"]  <- 1
#
#indivi <- rbind.fill(indivi,fip[is_fip_19_25,])

#    print fip.loc[is_fip_19_25]
    
    indivi = concat([indivi, fip.loc[is_fip_19_25]])
    
## on efface les variables inutiles 
#rm(is_fip_19_25)

    del is_fip_19_25

## on crée la date de naissance au format ISO
## Les ages et les ages en mois sont donn?s au 1er janvier de l'enqu?te
#indivi$age <- as.numeric(year) - indivi$naia - 1
    indivi['age'] = year - indivi.naia - 1
    
#
#
## ageq est l'?ge quinquennal obtenu en prenant l'?ge r?volu au 31 d?cembre 
## moins de 25 ans : 0
## 25 ? 29 ans     : 1
## 30 ? 34 ans     : 2
## 35 ? 39 ans     : 3
## 40 ? 44 ans     : 4
## 45 ? 49 ans     : 5
## 50 ? 54 ans     : 6
## 55 ? 59 ans     : 7
## 60 ? 64 ans     : 8
## 65 ? 69 ans     : 9
## 70 ? 74 ans     :10
## 75 ? 79 ans     :11
## 80 ans et plus  :12
#
#indivi$ageq <- (indivi$ag>=25) + (indivi$ag>=30) + (indivi$ag>=35) + 
#  (indivi$ag>=40) + (indivi$ag>=45) + (indivi$ag>=50) + (indivi$ag>=55) + 
#  (indivi$ag>=60) + (indivi$ag>=65) + (indivi$ag>=70) + (indivi$ag>=75) + 
#  (indivi$ag>=80)
#
# REMOVING ageq

## agem âge en mois au 1er janvier de l'année considérée
#indivi$agem <- 12*indivi$age  + (12-indivi$naim)
#

    indivi['agem'] = 12*indivi.age  + 12-indivi.naim

## recode lpr
#table(indivi$lpr, useNA="always")
#indivi$quimen[indivi$lpr == 1] <- 0
#indivi$quimen[indivi$lpr == 2] <- 1
#indivi$quimen[indivi$lpr == 3] <- 2
#indivi$quimen[indivi$lpr == 4] <- 3
#indivi$not_pr_cpr[indivi$lpr <= 2] <- FALSE 
#indivi$not_pr_cpr[indivi$lpr > 2] <- TRUE
    indivi["quimen"] = 0
    indivi.quimen[indivi.lpr == 1] = 0  
    indivi.quimen[indivi.lpr == 2] = 1
    indivi.quimen[indivi.lpr == 3] = 2
    indivi.quimen[indivi.lpr == 4] = 3    
    indivi['not_pr_cpr'] = nan
    indivi['not_pr_cpr'][indivi['lpr']<=2] = False
    indivi['not_pr_cpr'][indivi['lpr']>2] = True


#
## On crée les enf1,enf2 etc   # autre membre du ménage non pref ou cref
#test <- indivi[indivi$not_pr_cpr ,c("quimen","idmen")]
#test$quimen <- 'enf1'
#j = 2
#table(test$quimen)
#while ( any(duplicated(test[,c("quimen","idmen")])) ) {
#  pacstr <- paste('enf', j, sep = '')
#  tmp <- duplicated(test[,c("quimen","idmen")])
#  test[tmp, "quimen"] <- rep(pacstr, times=sum(tmp))
#  print(table(test$quimen))
#  j <- j + 1
#}
#indivi$quimen <- as.character(indivi$quimen)
#indivi[indivi$not_pr_cpr,c("quimen","idmen")] <- test 
#indivi$quimen <- as.factor(indivi$quimen) 
#rm(test,tmp)

    print "    4.3 : Creating non pr=0 and cpr=1 idmen's"
    indivi.reset_index(inplace=True)
    test1 = indivi.ix[indivi['not_pr_cpr']==True,['quimen', 'idmen']]
    test1['quimen'] = 2

    j=2
    while any(test1.duplicated(['quimen', 'idmen'])):
        test1.loc[test1.duplicated(['quimen', 'idmen']), 'quimen'] = j+1
        j += 1

    print_id(indivi)
    indivi.update(test1)

    print_id(indivi)
    
#     indivi.set_index(['quiment']) #TODO: check relevance
#
#
#print_id(indivi)
#
## TODO problème avec certains idfoy qui n'ont pas de vous
## Il y clairement un pb de double déclaration comme le montre test ci-dessous
#all <- unique(indivi$idfoy)                  # all idfoy 
#with <- indivi[indivi$quifoy=="vous","idfoy"] # idfoy with "vous"
#without <- all[!all %in% with]                       # # idfoy without "vous"
#length(without)
##test <- indivi[(indivi$idfoy %in% without) ,c("noindiv","quelfic", "quifoy", "idfoy" ,"lpr","declar1","declar2","persfipd")]
## exemple
##toto <- indivi[indivi$idmen==6020164,c("noindiv","quelfic", "quifoy", "idfoy" ,"lpr","declar1","declar2","persfipd","idmen")]
#
## On cherche si le déclarant donné par la deuxième déclaration est bien un vous et on rattache
#has_declar2 <- (indivi$idfoy %in% without) & !is.na(indivi$declar2)
#decl2_idfoy <- as.integer(indivi[has_declar2, "idmen"])*100 + as.integer(substr(indivi[has_declar2, "declar2"], 1, 2))
#indivi[has_declar2, "idfoy"] <- ifelse(decl2_idfoy %in% with, decl2_idfoy, NA)   
#
#rm(all,with,without, has_declar2)
    print ''
    print "Etape 5 : Gestion des idfoy qui n'ont pas de vous"
    all = indivi.drop_duplicates('idfoy')
    with_ = indivi.loc[indivi['quifoy']=='vous', 'idfoy']
    without = all[not_(all.idfoy.isin(with_.values))]
    
    print 'On cherche si le déclarant donné par la deuxième déclaration est bien un vous'
    has_declar2 = and_((indivi.idfoy.isin(without.idfoy.values)), indivi.declar2.notnull())
    decl2_idfoy = (indivi.loc[has_declar2, 'idmen'].astype('int')*100 + 
                    indivi.loc[has_declar2, "declar2"].str[0:2].astype('int'))
    indivi.loc[has_declar2, 'idfoy'] = where(decl2_idfoy.isin(with_.values), decl2_idfoy, None)
    del all,with_,without, has_declar2
    
## TODO dans un premier temps on élimine les idfoy restant
#idfoyList <- unique(indivi[indivi$quifoy=="vous","idfoy"])
#indivi <- indivi[indivi$idfoy %in% idfoyList,]
#rm(idfoyList)
#
#print_id(indivi)
#
#saveTmp(indivi, file= "indivi_tmp.Rdata")
#loadTmp(file= "indivi_tmp.Rdata")
#myvars <- names(indivi) %in% c("noindiv", "noi", "idmen", "idfoy", "quifoy", "wprm",
#                               "age","agem","quimen","quelfic","actrec","ageq",
#                               "nbsala","titc","statut","txtppb","chpub","prosa","encadr"
#                               )
#
#indivi <- indivi[myvars]
    print '    5.1 : Elimination idfoy restant'
    idfoyList = indivi.loc[indivi['quifoy']=="vous", 'idfoy'].drop_duplicates()
    indivi = indivi[indivi.idfoy.isin(idfoyList.values)]
    del idfoyList
    print_id(indivi)
    
    myvars = ["noindiv", "noi", "idmen", "idfoy", "quifoy", "wprm",
                            "age","agem","quelfic","actrec", "quimen",
                            "nbsala","titc","statut","txtppb","chpub","prosa","encadr"]
    
    if not(len(set(myvars).difference(set(indivi.columns))) == 0):
        print set(myvars).difference(set(indivi.columns))
                  
    assert len(set(myvars).difference(set(indivi.columns))) == 0

    indivi = indivi.loc[:, myvars]

## activite      # actif occupé 0, chômeur 1, étudiant/élève 2, retraité 3, autre inactif 4  
## recodée ? partir de actrec
### actrec: (voir prep_proc)
###   1: actif occup? non salari?
###   2: salari? pour une dur?e non limit?
###   3: contrat ? dur?e d?termin?e, int?rim, apprentissage, saisonnier
###   4: ch?meur
###   5: ?l?ve, ?tudiant, stagiaire non r?mun?r?
###   6:
###   7: retrait?, pr?retrait?, retir? des affaires
###   8: autre inactif
###   9: non renseign?
#
## TODO les actrec des fip ne sont pas codées (on le fera à la fin quand on aura rassemblé
## les infos provenant des déclarations)
#
#table(indivi[,c("actrec","age")],useNA="ifany")
#indivi$activite <- NA 
#indivi <- within(indivi,{
#  activite[which(actrec<=3) ] <- 0
#  activite[which(actrec==4) ] <- 1
#  activite[which(actrec==5) ] <- 2
#  activite[which(actrec==7) ] <- 3
#  activite[which(actrec==8) ] <- 4
#  activite[which(age<=13)]    <- 2  # ce sont en fait les actrec=9
#})
#table(indivi[,"activite"],useNA="ifany")
#
## TITC
## Statut, pour les agents de l'Etat des collectivités locales, ou des hôpitaux
## Sans objet (CHPUB<>'1','2','3') ou non renseigné
## 1 Elève fonctionnaire ou stagiaire
## 2 Agent titulaire
## 3 Contractuel
#
#indivi <- within(indivi,{
#  titc[is.na(titc) ] <- 0
#  })
##table(indivi$titc,useNA="ifany")
    print ''
    print 'Etape 6 : Création des variables descriptives'
    print '    6.1 : variable activité'
    indivi['activite'] = None
    indivi['activite'][indivi['actrec']<=3] = 0
    indivi['activite'][indivi['actrec']==4] = 1
    indivi['activite'][indivi['actrec']==5] = 2
    indivi['activite'][indivi['actrec']==7] = 3
    indivi['activite'][indivi['actrec']==8] = 4
    indivi['activite'][indivi['age']<=13] = 2 # ce sont en fait les actrec=9
    print indivi['activite'].value_counts()
    # TODO: MBJ problem avec les actrec 
    
    
    indivi['titc'][indivi['titc'].isnull()] = 0
#    print indivi['titc'].isnull().value_counts()
    assert indivi['titc'].notnull().all() , Exception("Problème avec les titc")
    
## STATUT
## Statut détaillé mis en cohérence avec la profession
## Sans objet (ACTOP='2')
## 11 Indépendants
## 12 Employeurs
## 13 Aides familiaux
## 21 Intérimaires
## 22 Apprentis
## 33 CDD (hors Etat, coll.loc.), hors contrats aides
## 34 Stagiaires et contrats aides (hors Etat, coll.loc.)
## 35 Autres contrats (hors Etat, coll.loc.)
## 43 CDD (Etat, coll.loc.), hors contrats aides
## 44 Stagiaires et contrats aides (Etat, coll.loc.)
## 45 Autres contrats (Etat, coll.loc.)
#
#indivi$statut <- as.numeric(indivi$statut)
#
#indivi <- within(indivi,{
#  statut[is.na(statut) ] <- 0
#  statut[statut == 11 ] <- 1
#  statut[statut == 12 ] <- 2
#  statut[statut == 13 ] <- 3
#  statut[statut == 21 ] <- 4
#  statut[statut == 22 ] <- 5
#  statut[statut == 33 ] <- 6
#  statut[statut == 34 ] <- 7
#  statut[statut == 35 ] <- 8
#  statut[statut == 43 ] <- 9
#  statut[statut == 44 ] <- 10
#  statut[statut == 45 ] <- 11
#  })
#table(indivi$statut,useNA="ifany")  

    print '    6.2 : variable statut'
    indivi['statut'][indivi['statut'].isnull()] = 0
    indivi['statut'] = indivi['statut'].astype('int')
    indivi['statut'][indivi['statut']==11] = 1
    indivi['statut'][indivi['statut']==12] = 2
    indivi['statut'][indivi['statut']==13] = 3
    indivi['statut'][indivi['statut']==21] = 4
    indivi['statut'][indivi['statut']==22] = 5
    indivi['statut'][indivi['statut']==33] = 6
    indivi['statut'][indivi['statut']==34] = 7
    indivi['statut'][indivi['statut']==35] = 8
    indivi['statut'][indivi['statut']==43] = 9
    indivi['statut'][indivi['statut']==44] = 10
    indivi['statut'][indivi['statut']==45] = 11
    #print indivi['statut'].value_counts()
    assert indivi['statut'].isin(range(12)).all(), Exception("statut value over range")
    
##TXTPPB
## Sans objet (ACTOP='2') ou non renseigné
## 1 Moins d'un mi-temps (50%)
## 2 Mi-temps (50%)
## 3 Entre 50 et 80%
## 4 80%
## 5 Plus de 80%
#
#indivi <- within(indivi,{
#  txtppb[is.na(txtppb) ] <- 0
#})
#  
## NBSALA
## Nombre de salariés dans l'établissement de l'emploi actuel
## Sans objet (ACTOP='2') ou non renseigné
## 1 Aucun salarié
## 2 1 ou 4 salariés
## 3 5 à 9 salariés
## 4 10 à 19 salariés
## 5 20 à 49 salariés
## 6 50 à 199 salariés
## 7 200 à 499 salariés
## 8 500 à 999 salariés
## 9 1000 salariés ou plus
## 99 Ne sait pas

#indivi$nbsala <- as.numeric(indivi$nbsala)
#indivi <- within(indivi,{
#  nbsala[is.na(nbsala) ]    <- 0 
#  nbsala[nbsala==99 ] <- 10  # TODO  418 fip à retracer qui sont NA
#})
#table(indivi$nbsala,useNA='ifany')
    print '    6.3 : variable txtppb'
    indivi['txtppb'] = indivi['txtppb'].fillna(0)
    assert indivi['txtppb'].notnull().all()
    
    indivi['nbsala'] = indivi['nbsala'].fillna(0)
    indivi['nbsala'] = indivi['nbsala'].astype('int')
    indivi['nbsala'][indivi['nbsala']==99] = 10
    assert indivi['nbsala'].isin(range(11)).all()


## CHPUB
## Nature de l'employeur principal
## Sans objet (n'est pas salarié)
## 1 Etat
## 2 Collectivités locales, HLM
## 3 Hôpitaux publics
## 4 Particulier
## 5 Entreprise publique (La Poste, EDF-GDF, etc.)
## 6 Entreprise privée, association
#table(indivi$chpub,useNA='ifany')
#indivi$chpub <- as.numeric(indivi$chpub)
#indivi <- within(indivi,{
#  chpub[is.na(chpub) ]    <- 0   # TODO  418 fip à retracer qui sont NA
#})
    print '    6.4 : variable chpub et CSP'
    indivi['chpub'].fillna(0, inplace=True)
    indivi['chpub'] = indivi['chpub'].astype('int')
    indivi['chpub'][indivi['chpub'].isnull()] = 0
    print indivi['chpub'].value_counts()
    assert indivi['chpub'].isin(range(11)).all()
    
    
## 1 Manoeuvre ou ouvrier spécialisé
## 2 Ouvrier qualifié ou hautement qualifié
## 3 Technicien
## 4 Employé de bureau, de commerce, personnel de services, personnel de catégorie C ou D
## 5 Agent de maîtrise, maîtrise administrative ou commerciale VRP (non cadre) personnel de
## catégorie B
## 7 Ingénieur, cadre (à l'exception des directeurs généraux ou de ses adjoints directs)
## personnel de catégorie A
## 8 Directeur général, adjoint direct
## 9 Autre
#
#indivi$cadre <- 0  # 0 as NA

#indivi <- within(indivi,{
#  prosa[is.na(prosa) ]    <- 0
#  cadre[prosa==7 | prosa==8 ] <- 1
#  cadre[prosa==9 & encadr==1] <- 1 
#})
    indivi['cadre'] = 0
    indivi['prosa'][indivi['prosa'].isnull()] = 0
    assert indivi['prosa'].notnull().all()
    print indivi['encadr'].value_counts()
    
    # encadr : 1=oui, 2=non
    indivi['encadr'].fillna(2, inplace=True)
    assert indivi['encadr'].notnull().all()
    indivi['cadre'][or_(indivi['prosa']==7, indivi['prosa']==8)] = 1
    indivi['cadre'][and_(indivi['prosa']==9, indivi['encadr']==1)] = 1
    print "cadre"
    print indivi['cadre'].value_counts()
    assert indivi['cadre'].isin(range(2)).all()
    
#
### 
#######################################################################################
## on vérifie qu'il ne manque pas d'information sur les liens avec la personne de r?f?rence
#
#print(length(table(indivi$idmen)))
#table(indivi$quimen, useNA="ifany")
#
#print(length(table(indivi$idfoy)))
#table(indivi$quifoy, useNA="ifany")   # On en a 1430 vous qui viennent de FIP_IMP
#
## On cr?e les pac1,pac2 etc
##sum(is.na(indivi$idfoy))
#test <- indivi[indivi$quifoy=="pac",c("quifoy","idfoy")]
#test$quifoy <- 'pac1'
#j = 2
#table(test$quifoy)
#while ( any(duplicated(test[,c("quifoy","idfoy")])) ) {
#  pacstr <- paste('pac', j, sep = '')
#  tmp <- duplicated(test[,c("quifoy","idfoy")])
#  test[tmp, "quifoy"] <- rep(pacstr, times=sum(tmp))
#  #  print(table(test$quifoy))
#  j <- j + 1
#}
#
#indivi$quifoy <- as.character(indivi$quifoy)
#indivi[indivi$quifoy=="pac",c("quifoy","idfoy")] <- test 
#indivi$quifoy <- as.factor(indivi$quifoy) 
#rm(test,tmp,fip)
#
#print_id(indivi)
#
#saveTmp(indivi, file= "indivi.Rdata")
    print ''
    print "Etape 7 : on vérifie qu'il ne manque pas d'info sur les liens avec la personne de référence"
    
    print 'nb de doublons idfam/quifam', len(indivi[indivi.duplicated(cols=['idfoy', 'quifoy'])])

    print 'On crée les n° de personnes à charge'
    assert indivi['idfoy'].notnull().all()
    print_id(indivi)
    indivi['quifoy2'] = 2
    indivi['quifoy2'][indivi['quifoy']=='vous'] = 0
    indivi['quifoy2'][indivi['quifoy']=='conj'] = 1
    indivi['quifoy2'][indivi['quifoy']=='pac'] = 2
    
    
    del indivi['quifoy']
    indivi['quifoy'] = indivi['quifoy2']
    del indivi['quifoy2']
    
    print_id(indivi)
    test2 = indivi.loc[indivi['quifoy']==2, ['quifoy', 'idfoy','noindiv']]
    print_id(test2)
    
    j=2
    while test2.duplicated(['quifoy', 'idfoy']).any():
        test2.loc[test2.duplicated(['quifoy', 'idfoy']), 'quifoy'] = j
        j += 1
    
    print_id(test2)
    #indivi['quifoy'] = indivi['quifoy'].astype('str')
    indivi = indivi.merge(test2, on=['noindiv','idfoy'], how="left")
    indivi['quifoy'] = indivi['quifoy_x']
    indivi['quifoy'] = where(indivi['quifoy_x']==2, indivi['quifoy_y'], indivi['quifoy_x'])
    del indivi['quifoy_x'], indivi['quifoy_y']
    print_id(indivi)
    
#    indivi['quifoy'][indivi['quifoy'] == 2] = test2['quifoy']
    del test2, fip 
    print 'nb de doublons idfam/quifam', len(indivi[indivi.duplicated(cols=['idfoy', 'quifoy'])])
    print_id(indivi)
    
#####################################################################################
## On ajoute les idfam et quifam
#load(famc)
#
#tot2 <- merge(indivi, famille, by = c('noindiv'), all.x = TRUE)
#rm(famille)
#print_id(tot2)
#
### Les idfam des enfants FIP qui ne font plus partie des familles forment des famille seuls 
#tot2[is.na(tot2$quifam), "idfam"] <- tot2[is.na(tot2$quifam), "noindiv"]
#tot2[is.na(tot2$quifam), "quifam"] <- 0
#print_id(tot2)
#saveTmp(tot2, file = "tot2.Rdata")
#rm(indivi,tot2)
#
## on merge les variables de revenus (foyer_aggr) avec les identifiants précédents
## load foyer 
#loadTmp(file = "tot2.Rdata")
#loadTmp(file= "foyer_aggr.Rdata")
#
#tot3 <- merge(tot2, foyer, all.x = TRUE)
#print_id(tot3) # OK
#saveTmp(tot3, file= "tot3.Rdata")
#rm(tot3,tot2,foyer)
#
    print ''
    print 'Etape 8 : création des fichiers totaux'
    famille = load_temp(name='famc', year=year)


    
    print '    8.1 : création de tot2 & tot3'
    tot2 = indivi.merge(famille, on='noindiv', how='inner')
#     del famille # TODO: MBJ increase in number of menage/foyer when merging with family ...
    del famille
    

    control(tot2, debug=True, verbose=True)
    assert tot2['quifam'].notnull().all()
    
    save_temp(tot2, name='tot2', year=year)
    del indivi
    print '    tot2 saved'
    
#     #On combine les variables de revenu
#     foyer = load_temp(name='foy_ind', year=year)
#     print " INTERSERCT THE POOCHAY"
#     tot2["idfoy"] = tot2["idfoy"][tot2["idfoy"].notnull()] +1
#     print "pingas"
#     print sorted(tot2.loc[tot2.idfoy.notnull(),"idfoy"].astype('int').unique())[0:10]
#     print "pocchay"
#     print sorted(foyer["idfoy"].unique())[0:10]
#     print "final flash"
#     print 602062550.0 in foyer["idfoy"].values
#     print len(list(set(tot2["idfoy"].unique()) & set(foyer["idfoy"].unique())))
#     print tot2.quifoy.value_counts()
    #tot2.update(foyer)
    tot2.merge(foyer, how = 'left')
    
    tot2 = tot2[tot2.idmen.notnull()]
#     tot2['idfoy'] += 1

    print_id(tot2)
    
    tot3 = tot2
    # TODO: check where they come from
    tot3 = tot3.drop_duplicates(cols='noindiv')
    print len(tot3)
    
    #Block to remove any unwanted duplicated pair
    print "    check tot3"
    control(tot3, debug=True, verbose=True)
    tot3 = tot3.drop_duplicates(cols=['idfoy', 'quifoy'])
    tot3 = tot3.drop_duplicates(cols=['idfam', 'quifam'])
    tot3 = tot3.drop_duplicates(cols=['idmen', 'quimen'])
    tot3 = tot3.drop_duplicates(cols='noindiv')
    control(tot3)
    
## On ajoute les variables individualisables
#loadTmp("foyer_individualise.Rdata") # foy_ind
#loadTmp("tot3.Rdata")
#loadTmp("allvars.Rdata")
#loadTmp("sif.Rdata")
#
#vars2 <- setdiff(names(tot3),  allvars)
#tot3 <- tot3[,vars2]
#
#print_id(tot3)
#final <- merge(tot3, foy_ind, by = c('idfoy', 'quifoy'), all.x = TRUE)
#
#print_id(final)
#rm(tot3, foy_ind)
#table(final[final$quifoy=="vous", "noindiv"] %in% sif$noindiv)
#
    print '    8.2 : On ajoute les variables individualisables'
    
    allvars = load_temp(name = 'ind_vars_to_remove', year=year)
    vars2 = set(tot3.columns).difference(set(allvars))
    tot3 = tot3[list(vars2)]
    print len(tot3)

    
    assert not(tot3.duplicated(cols=['noindiv']).any()), "doublon dans tot3['noindiv']"
    lg_dup = len(tot3[tot3.duplicated(['idfoy', 'quifoy'])])
    assert lg_dup == 0, "%i pairs of idfoy/quifoy in tot3 are duplicated" %(lg_dup)
    
    save_temp(tot3, name='tot3', year=year)
    control(tot3)
    
    del tot2, allvars, tot3, vars2
    print 'tot3 sauvegardé'




    gc.collect()
    


def create_final(year=None):
    if year is None:
        raise Exception("A year is needed")
    print 'création de final'
    foy_ind = load_temp(name = 'foy_ind', year=year)
    tot3 = load_temp(name='tot3', year=year)


    foy_ind.set_index(['idfoy', 'quifoy'], inplace=True)
    tot3.set_index(['idfoy', 'quifoy'], inplace=True)
    final = concat([tot3, foy_ind], join_axes=[tot3.index], axis=1)
    final.reset_index(inplace=True)
    foy_ind.reset_index(inplace=True)
    tot3.reset_index(inplace=True)
        
#     tot3 = tot3.drop_duplicates(cols=['idfam', 'quifam'])
    final = final[final.idmen.notnull()]

    control(final, verbose=True)
    del tot3, foy_ind
    gc.collect()
    
#final <- merge(final, sif, by = c('noindiv'), all.x = TRUE)
#print_id(final)
#saveTmp(final,"final.Rdata")
#
#loadTmp("final.Rdata")
#
#rm(sif,final)
#gc()
    print "    loading fip"
    
    sif = load_temp(name = 'sif', year=year)
    
#     sifcols = sif.columns
#     sifcols = [col for col in sifcols if col != "noindiv"]
#     for col in sifcols:
#         final[col] = nan
    
    print sif.columns
    print "    update final using fip"
    final = final.merge(sif, on=["noindiv"], how="left") 
    #TODO: IL FAUT UNE METHODE POUR GERER LES DOUBLES DECLARATIONS 
    
    print 'check doublons', len(final[final.duplicated(['noindiv'])])

    print final.columns
    control(final, debug=True)
        
#     final = final[final.caseP.notnull()]
    final['caseP'] = final.caseP.fillna(False) 
    print final['caseP'].value_counts()
    print_id(final)
    
    save_temp(final, name='final', year=year)
    print 'final sauvegardé'
    del sif, final
    
if __name__ == '__main__':
#    create_totals()
    create_final()