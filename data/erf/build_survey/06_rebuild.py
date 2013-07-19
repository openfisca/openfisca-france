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
    

    selection = Series()
    for var in ["zsali", "zchoi", "zrsti", "zalri", "zrtoi", "zragi", "zrici", "zrnci"]:
        varo = var[:-1]+"o"
        test = indivim[var] != indivim[varo]
        if len(selection) == 0:
            selection = test
        else:
            selection = or_(test, selection)


    indivi_i = indivim[selection] 
    indivi_i.rename(columns={"ident" : "idmen",
                     "persfip":"quifoy",  
                     "zsali" : "sali2", # Inclu les salaires non imposables des agents d'assurance
                     "zchoi" : "choi2", 
                     "zrsti" : "rsti2",
                     "zalri" : "alr2"}, inplace=True)
    

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

    print ''
    print "Etape 2 : isolation des FIP"
    fip_imp = indivi.quelfic=="FIP_IMP"
    indivi["idfoy"] = (indivi["idmen"].astype("int64")*100 + 
                       (indivi["declar1"].str[0:2]).convert_objects(convert_numeric=True))
    
    indivi.loc[fip_imp,"idfoy"] = nan
    
## Certains FIP (ou du moins avec revenus imputés) ont un num?ro de déclaration d'impôt ( pourquoi ?)

    
    fip_has_declar = and_(fip_imp, indivi.declar1.notnull())

#    indivi.ix[fip_has_declar, "idfoy"] = ( indivi.ix[fip_has_declar, "idmen"]*100 
#                                        + (indivi.ix[fip_has_declar, "declar1"].str[0:1]).convert_objects(convert_numeric=True) )
    indivi["idfoy"] = where(fip_has_declar, 
                            indivi["idmen"]*100 + indivi["declar1"].str[0:2].convert_objects(convert_numeric=True),
                            indivi["idfoy"])
    
    del fip_has_declar
    

    fip_no_declar = and_(fip_imp, indivi.declar1.isnull())
    del fip_imp
    indivi["idfoy"] = where(fip_no_declar, 
                            indivi["idmen"]*100 + 50,
                            indivi["idfoy"])
    
    indivi_fnd = indivi.loc[fip_no_declar, ["idfoy","noindiv"]]
    

    while any(indivi_fnd.duplicated(cols=["idfoy"])):
        indivi_fnd["idfoy"] = where(indivi_fnd.duplicated(cols=["idfoy"]),
                                    indivi_fnd["idfoy"] + 1,
                                    indivi_fnd["idfoy"])

    assert indivi_fnd["idfoy"].duplicated().value_counts()[False] == len(indivi_fnd["idfoy"]), "Duplicates remaining"    
    assert len(indivi[indivi.duplicated(['noindiv'])]) == 0, "Doublons"


    indivi.loc[fip_no_declar, ["idfoy"]] = indivi_fnd
    del indivi_fnd, fip_no_declar

    print ''
    print 'Etape 3 : Récupération des EE_NRT'
    
    nrt = indivi.quelfic=="EE_NRT"
    indivi.idfoy = where(nrt, indivi.idmen*100 + indivi.noi, indivi.idfoy)
    indivi.loc[nrt,"quifoy"] = "vous"
    del nrt

    pref_or_cref = or_(indivi.lpr==1, indivi.lpr==2)
    adults = and_(indivi.quelfic.isin(["EE","EE_CAF"]),pref_or_cref)  
    indivi.idfoy = where(adults, indivi.idmen*100 + indivi.noi, indivi.idfoy)
    indivi.loc[adults, "quifoy"] = "vous"
    del adults
    assert indivi.loc[or_(indivi.lpr==1, indivi.lpr==2),"idfoy"].notnull().all()

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

#     assert indivi.loc[enf_ee,"idfoy"].notnull().all()
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



# MBJ: issue delt with when moving from R code to python 
## TODO il faut rajouterles enfants_fip et créer un ménage pour les majeurs
## On suit guide méthodo erf 2003 page 135
## On supprime les conjoints FIP et les FIP de 25 ans et plus;
## On conserve les enfants FIP de 19 à 24 ans;
## On supprime les FIP de 18 ans et moins, exceptés les FIP nés en 2002 dans un 
## ménage en 6ème interrogation car ce sont des enfants nés aprés la date d'enquète
## EEC que l'on ne retrouvera pas dans les EEC suivantes.
#
    print '    4.2 : On enlève les individus pour lesquels il manque le déclarant'
    fip = load_temp(name="fipDat", year=year)
    fip["declar"] = nan
    fip["agepf"] = nan


    fip.drop(["actrec", "year", "noidec"],axis=1)
    fip.naia = fip.naia.astype("int32")
    fip.rename( columns=dict(ident = "idmen",
                     persfip="quifoy",  
                     zsali = "sali2", # Inclu les salaires non imposables des agents d'assurance
                     zchoi = "choi2", 
                     zrsti = "rsti2",
                     zalri = "alr2"), inplace=True)


    is_fip_19_25 = and_((year-fip.naia-1)>=19, (year-fip.naia-1)<25)

## TODO: BUT for the time being we keep them in thier vous menage so the following lines are commented
## The idmen are of the form 60XXXX we use idmen 61XXXX, 62XXXX for the idmen of the kids over 18 and less than 25
##fip[is_fip_19_25 ,"idmen"] <- (99-fip[is_fip_19_25,"noi"]+1)*100000 + fip[is_fip_19_25,"idmen"]
##fip[is_fip_19_25 ,"lpr"]  <- 1
#
#indivi <- rbind.fill(indivi,fip[is_fip_19_25,])

    indivi = concat([indivi, fip.loc[is_fip_19_25]])
    del is_fip_19_25
    indivi['age'] = year - indivi.naia - 1
    indivi['agem'] = 12*indivi.age  + 12-indivi.naim

    indivi["quimen"] = 0
    indivi.quimen[indivi.lpr == 1] = 0  
    indivi.quimen[indivi.lpr == 2] = 1
    indivi.quimen[indivi.lpr == 3] = 2
    indivi.quimen[indivi.lpr == 4] = 3    
    indivi['not_pr_cpr'] = nan
    indivi['not_pr_cpr'][indivi['lpr']<=2] = False
    indivi['not_pr_cpr'][indivi['lpr']>2] = True


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
#     TODO problème avec certains idfoy qui n'ont pas de vous
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

## TODO les actrec des fip ne sont pas codées (on le fera à la fin quand on aura rassemblé
## les infos provenant des déclarations)

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
    assert indivi['titc'].notnull().all() , Exception("Problème avec les titc")
    

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
    assert indivi['statut'].isin(range(12)).all(), Exception("statut value over range")
    

#indivi$nbsala <- as.numeric(indivi$nbsala)
#indivi <- within(indivi,{
#  nbsala[is.na(nbsala) ]    <- 0 
#  nbsala[nbsala==99 ] <- 10  # TODO  418 fip à retracer qui sont NA
#})

    print '    6.3 : variable txtppb'
    indivi['txtppb'] = indivi['txtppb'].fillna(0)
    assert indivi['txtppb'].notnull().all()
    
    indivi['nbsala'] = indivi['nbsala'].fillna(0)
    indivi['nbsala'] = indivi['nbsala'].astype('int')
    indivi['nbsala'][indivi['nbsala']==99] = 10
    assert indivi['nbsala'].isin(range(11)).all()

    print '    6.4 : variable chpub et CSP'
    indivi['chpub'].fillna(0, inplace=True)
    indivi['chpub'] = indivi['chpub'].astype('int')
    indivi['chpub'][indivi['chpub'].isnull()] = 0
    print indivi['chpub'].value_counts()
    assert indivi['chpub'].isin(range(11)).all()
    
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
    indivi = indivi.merge(test2, on=['noindiv','idfoy'], how="left")
    indivi['quifoy'] = indivi['quifoy_x']
    indivi['quifoy'] = where(indivi['quifoy_x']==2, indivi['quifoy_y'], indivi['quifoy_x'])
    del indivi['quifoy_x'], indivi['quifoy_y']
    print_id(indivi)
    
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
    print "    loading fip"
    sif = load_temp(name = 'sif', year=year)
    
    print sif.columns
    print "    update final using fip"
    final = final.merge(sif, on=["noindiv"], how="left") 
    #TODO: IL FAUT UNE METHODE POUR GERER LES DOUBLES DECLARATIONS 
    

    print final.columns
    control(final, debug=True)
        
    final['caseP'] = final.caseP.fillna(False) 
    final['caseF'] = final.caseF.fillna(False)
    print_id(final)
    
    save_temp(final, name='final', year=year)
    print 'final sauvegardé'
    del sif, final
    
if __name__ == '__main__':
    year = 2006
    create_totals(year=year)
    create_final(year=year)