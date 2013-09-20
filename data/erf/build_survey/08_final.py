# -*- coding:utf-8 -*-
# Created on 21 mai 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)

from __future__ import division
from numpy import where, NaN, random, logical_or as or_, unique 
from src.countries.france.data.erf.build_survey import show_temp, load_temp, save_temp
from src.countries.france.data.erf.build_survey.utilitaries import print_id, control, check_structure
from numpy import logical_and as and_, logical_not as not_
from pandas import read_csv, HDFStore
import os
import gc


def final(year=2006):

##***********************************************************************/
    print('08_final: derniers réglages')
##***********************************************************************/
# 
# loadTmp("final.Rdata")
# # On définit comme célibataires les individus dont on n'a pas retrouvé la déclaration
# final$statmarit[is.na(final$statmarit)] <- 2
# table(final$statmarit, useNA='ifany')
# 
    import gc
    gc.collect()
    final = load_temp("final", year=year)
    print 'check doublons', len(final[final.duplicated(['noindiv'])])
    final.statmarit = where(final.statmarit.isnull(), 2, final.statmarit)
# 



# # activite des fip
# table(final[final$quelfic=="FIP","activite"],useNA="ifany")
# summary(final[final$quelfic=="FIP",c("activite","choi","sali","alr","rsti","age")] )
# # activite      # actif occup? 0, ch?meur 1, ?tudiant/?l?ve 2, retrait? 3, autre inactif 4
# 
# final_fip <- final[final$quelfic=="FIP",]
# final_fip <- within(final_fip,{
#   choi <- ifelse(is.na(choi),0,choi)
#   sali <- ifelse(is.na(sali),0,sali)
#   alr <- ifelse(is.na(alr),0,alr)
#   rsti <- ifelse(is.na(rsti),0,rsti)
#   activite <- 2 # TODO comment choisr la valeur par d?faut ?
#   activite <- ifelse(choi > 0,1,activite)
#   activite <- ifelse(sali > 0,0,activite)
#   activite <- ifelse(age  >= 21, 2,activite) # ne peuvent être rattach?s que les ?tudiants  
# })
# final[final$quelfic=="FIP",]<- final_fip
# table(final_fip[,c("age","activite")])
# rm(final_fip)
# 
# print_id(final)
# saveTmp(final, file= "final.Rdata")
#
    print '    gestion des FIP de final'
    final_fip = final.loc[final.quelfic=="FIP", ["choi", "sali", "alr", "rsti","age"]]
    
    print set(["choi", "sali", "alr", "rsti"]).difference(set(final_fip.columns))
    for var in  ["choi", "sali", "alr", "rsti"]:
        final_fip[var].fillna(0, inplace=True)
        assert final_fip[var].notnull().all(), "some NaN are remaining in column %s" %(var)
    
    
    final_fip["activite"] = 2 # TODO comment choisr la valeur par défaut ?
    final_fip.activite = where(final_fip.choi > 0, 1, final_fip.activite)
    final_fip.activite = where(final_fip.sali > 0, 0, final_fip.activite)
    final_fip.activite = where(final_fip.age > 21, 2, final_fip.activite)  # ne peuvent être rattach?s que les ?tudiants  

    final.update(final_fip)
    save_temp(final, name="final", year=year)
    print '    final has been updated with fip'
 
# loadTmp("final.Rdata")
# load(menm)
# menagem <- rename(menagem, c("ident"="idmen","loym"="loyer"))
# menagem$cstotpragr <- floor(menagem$cstotpr/10)
# 
    from math import floor

    menagem = load_temp(name="menagem", year=year)
    menagem.rename(columns=dict(ident="idmen",loym="loyer"), inplace=True)
    menagem["cstotpragr"] = menagem["cstotpr"].apply(lambda x: floor(x/10))    
# 
# # 2008 tau99 removed TODO: check ! and check incidence
# if (year == "2008") {
#  vars <- c("loyer", "tu99", "pol99", "reg","idmen", "so", "wprm", "typmen15", "nbinde","ddipl","cstotpragr","champm","zthabm")
# } else {
#   vars <- c("loyer", "tu99", "pol99", "tau99", "reg","idmen", "so", "wprm", "typmen15", "nbinde","ddipl","cstotpragr","champm","zthabm")
# }
# 
# famille_vars <- c("m_afeamam", "m_agedm","m_clcam", "m_colcam", 'm_mgamm', 'm_mgdomm')

    if year == 2008:
        vars = ["loyer", "tu99", "pol99", "reg","idmen", "so", "wprm", "typmen15",
                 "nbinde","ddipl","cstotpragr","champm","zthabm"]
    else:
        vars = ["loyer", "tu99", "pol99", "tau99", "reg","idmen", "so", "wprm", 
                "typmen15", "nbinde","ddipl","cstotpragr","champm","zthabm"]
    famille_vars = ["m_afeamam", "m_agedm","m_clcam", "m_colcam", 'm_mgamm', 'm_mgdomm']


# if ("naf16pr" %in% names(menagem)) {
#   naf16pr <- factor(menagem$naf16pr)
#   levels(naf16pr) <-  0:16
#   menagem$naf16pr <- as.character(naf16pr)
#   menagem[is.na(menagem$naf16pr), "naf16pr" ] <- "-1"  # Sans objet 
#   vars <- c(vars,"naf16pr")
# } else if ("nafg17npr" %in% names(menagem)) {
#   # TODO: pb in 2008 with xx
#   if (year == "2008"){
#     menagem[ menagem$nafg17npr == "xx" & !is.na(menagem$nafg17npr), "nafg17npr"] <- "00"
#   }
#   nafg17npr <- factor(menagem$nafg17npr)  
#   levels(nafg17npr) <-  0:17
#   menagem$nafg17npr <- as.character(nafg17npr)
#   menagem[is.na(menagem$nafg17npr), "nafg17npr" ] <- "-1"  # Sans objet
# }
# 


#TODO: TODO: pytohn translation needed
#    if "naf16pr" in menagem.columns:
#        naf16pr <- factor(menagem$naf16pr)
#   levels(naf16pr) <-  0:16
#   menagem$naf16pr <- as.character(naf16pr)
#   menagem[is.na(menagem$naf16pr), "naf16pr" ] <- "-1"  # Sans objet 
#   vars <- c(vars,"naf16pr")
# } else if ("nafg17npr" %in% names(menagem)) {
#   # TODO: pb in 2008 with xx
#   if (year == "2008"){
#     menagem[ menagem$nafg17npr == "xx" & !is.na(menagem$nafg17npr), "nafg17npr"] <- "00"
#   }
#   nafg17npr <- factor(menagem$nafg17npr)  
#   levels(nafg17npr) <-  0:17
#   menagem$nafg17npr <- as.character(nafg17npr)
#   menagem[is.na(menagem$nafg17npr), "nafg17npr" ] <- "-1"  # Sans objet
# }



# # TODO: 2008tau99 is not present should be provided by 02_loy.... is it really needed
# all_vars <- union(vars,famille_vars)
# available_vars <- all_vars[union(vars,famille_vars) %in% names(menagem)]
# loyersMenages <- menagem[,available_vars]
# 
    all_vars = vars + famille_vars
    
    print all_vars
    print  set(menagem.columns)
    available_vars = list( set(all_vars).intersection(set(menagem.columns)))
    
    loyersMenages = menagem.xs(available_vars,axis=1)


# 
# # Recodage de typmen15: modalités de 1:15
# table(loyersMenages$typmen15, useNA="ifany")
# loyersMenages <- within(loyersMenages, {
#   typmen15[typmen15==10 ] <- 1
#   typmen15[typmen15==11 ] <- 2
#   typmen15[typmen15==21 ] <- 3
#   typmen15[typmen15==22 ] <- 4
#   typmen15[typmen15==23 ] <- 5
#   typmen15[typmen15==31 ] <- 6
#   typmen15[typmen15==32 ] <- 7
#   typmen15[typmen15==33 ] <- 8
#   typmen15[typmen15==41 ] <- 9
#   typmen15[typmen15==42 ] <- 10
#   typmen15[typmen15==43 ] <- 11
#   typmen15[typmen15==44 ] <- 12
#   typmen15[typmen15==51 ] <- 13
#   typmen15[typmen15==52 ] <- 14
#   typmen15[typmen15==53 ] <- 15
# })
# 
# 
# TODO: MBJ UNNECESSARY ?
    
# 
# # Pb avec ddipl, pas de modalités 2: on décale les chaps >=3
# # Cependant on fait cela après avoir fait les traitement suivants
# table(loyersMenages$ddipl, useNA="ifany")
# # On convertit les ddipl en numeric
# loyersMenages$ddipl <- as.numeric(loyersMenages$ddipl)
# table(loyersMenages$ddipl, useNA="ifany")
# #   On met les non renseignés ie, NA et "" à sans diplome (modalité 7)
# loyersMenages[is.na(loyersMenages$ddipl), "ddipl"] <- 7
# 
# loyersMenages[loyersMenages$ddipl>1, "ddipl"] <- loyersMenages$ddipl[loyersMenages$ddipl>1]-1
# 


    loyersMenages.ddipl = where(loyersMenages.ddipl.isnull(), 7, loyersMenages.ddipl)
    loyersMenages.ddipl = where(loyersMenages.ddipl>1, 
                                loyersMenages.ddipl-1,
                                loyersMenages.ddipl)
    loyersMenages.ddipl.astype("int32")
# 
# table(final$actrec,useNA="ifany")
# final$act5 <- NA    
# final <- within(final, {
#   act5[which(actrec==1) ] <- 2 # ind?pendants
#   act5[which(actrec==2) ] <- 1 # salari?s
#   act5[which(actrec==3) ] <- 1 # salari?s
#   act5[which(actrec==4) ] <- 3 # ch?meur
#   act5[which(actrec==7) ] <- 4 # retrait?
#   act5[which(actrec==8) ] <- 5 # autres inactifs
# })
# table(final$act5,useNA="ifany")
# 


    final.act5 = NaN    

    final.act5 = where(final.actrec==1, 2, final.act5) # indépendants
    final.act5 = where(final.actrec.isin([2,3]), 1, final.act5)  # salariés

    final.act5 = where(final.actrec==4, 3, final.act5) # chômeur
    final.act5 = where(final.actrec==7, 4, final.act5) # retraité
    final.act5 = where(final.actrec==8, 5, final.act5) # autres inactifs
    print final.act5.value_counts() # TODO : 29 retraités ?

#     assert final.act5.notnull().all(), 'there are NaN inside final.act5'

# final$wprm <- NULL # with the intention to extract wprm from menage to deal with FIPs
# final$tax_hab <- final$zthabm # rename zthabm to tax_hab
# final$zthabm <- NULL
# 
# final2 <- merge(final, loyersMenages, by="idmen", all.x=TRUE)
    print '    création de final2'
    del final["wprm"]
    gc.collect()
    final.rename(columns=dict(zthabm="tax_hab"), inplace=True) # rename zthabm to tax_hab
    final2 = final.merge(loyersMenages, on="idmen", how="left") # TODO: Check
    print loyersMenages.head()
    gc.collect()
    print_id(final2)
        
# 
# # TODO: merging with patrimoine
# rm(menagem,final)
# 
# # table(final2$activite,useNA="ifany")
# # table(final2$alt,useNA="ifany")
# 
# saveTmp(final2, file= "final2.Rdata")
# 
# loadTmp("final2.Rdata")
# names(final2)
# print_id(final2)
# 
# 
# # set zone_apl using zone_apl_imputation_data
# apl_imp <- read.csv("./zone_apl/zone_apl_imputation_data.csv")
# 
# if (year == "2008") {
#   zone_apl <- final2[, c("tu99", "pol99", "reg")]
# } else {
#   zone_apl <- final2[, c("tu99", "pol99", "tau99", "reg")]
# }
# 
# for (i in 1:length(apl_imp[,"TU99"])) {
#   tu <- apl_imp[i,"TU99"]
#   pol <- apl_imp[i,"POL99"]
#   tau <- apl_imp[i,"TAU99"]
#   reg <- apl_imp[i,"REG"]
#   #  print(c(tu,pol,tau,reg))
#   
#   if (year == "2008") {
#     indices <- (final2["tu99"] == tu & final2["pol99"] == pol  & final2["reg"] == reg)
#     selection <-  (apl_imp["TU99"] == tu & apl_imp["POL99"] == pol & apl_imp["REG"] == reg)
#   } else {
#     indices <- (final2["tu99"] == tu & final2["pol99"] == pol & final2["tau99"] == tau & final2["reg"] == reg)
#     selection <-  (apl_imp["TU99"] == tu & apl_imp["POL99"] == pol & apl_imp["TAU99"] == tau & apl_imp["REG"] == reg) 
#   }
#   z <- runif(sum(indices))
#   probs <- apl_imp[selection , c("proba_zone1", "proba_zone2")]
#   #  print(probs)
#   final2[indices,"zone_apl"] <- 1 + (z>probs[,'proba_zone1']) + (z>(probs[,'proba_zone1']+probs[,'proba_zone2']))
#   rm(indices, probs)
# }
# 

    print '    traitement des zones apl'
    apl_imp = read_csv("../../zone_apl/zone_apl_imputation_data.csv")

    print apl_imp.head(10)
    if year == 2008:
        zone_apl = final2.xs(["tu99", "pol99", "reg"], axis=1)
    else:
        zone_apl = final2.xs(["tu99", "pol99", "tau99", "reg"], axis=1)
        
    for i in range(len(apl_imp["TU99"])):
        tu = apl_imp["TU99"][i]
        pol = apl_imp["POL99"][i]
        tau = apl_imp["TAU99"][i]
        reg = apl_imp["REG"][i]

    if year == 2008:
        indices = and_(and_(final2["tu99"] == tu, final2["pol99"] == pol),
                       final2["reg"] == reg)
        selection = and_(and_(apl_imp["TU99"] == tu, apl_imp["POL99"] == pol),
                         apl_imp["REG"] == reg)
    else:
        indices = and_(and_(final2["tu99"] == tu, final2["pol99"] == pol),
                       and_(final2["tau99"] == tau, final2["reg"] == reg))
        selection = and_(and_(apl_imp["TU99"] == tu, apl_imp["POL99"] == pol),
                         and_(apl_imp["TAU99"] == tau, apl_imp["REG"] == reg))
    
    z = random.uniform(size=indices.sum())
    print len(z)
    print len(indices)

    print len(indices)/len(z)
    probs = apl_imp.loc[selection , ["proba_zone1", "proba_zone2"]]
    print probs
    print probs['proba_zone1'].values

    proba_zone_1 =  probs['proba_zone1'].values[0]
    proba_zone_2 =  probs['proba_zone2'].values[0]
    
    final2["zone_apl"] = 3
    final2["zone_apl"][indices] = ( 1 + (z>proba_zone_1) +
                                       (z>(proba_zone_1 + proba_zone_2))) 
    del indices, probs
    
#     control(final2, verbose=True, debug=True, verbose_length=15)
    
    print '    performing cleaning on final2'
    print 'nombre de sali nuls', len(final2[final2['sali'].isnull()])
    print "nombre d'âges nuls", len(final2[final2.age.isnull()])
    print "longueur de final2 avant purge", len(final2)
#     columns_w_nan = []
#     for col in final2.columns:
#         if final2[final2['idfoy'].notnull()][col].isnull().any() and not final2[col].isnull().all():
#             columns_w_nan.append(col)
#     print columns_w_nan
    print 'check doublons', len(final2[final2.duplicated(['noindiv'])])
    print final2.age.isnull().sum()

#     print final2.loc[final2.duplicated('noindiv'), ['noindiv', 'quifam']].to_string() 
    #TODO: JS: des chefs de famille et conjoints en double il faut trouver la source des ces doublons !
#     final2 = final2.drop_duplicates(['noindiv'])
    
    final2 = final2[not_(final2.age.isnull())]
    print "longueur de final2 après purge", len(final2)
    print_id(final2)
    
# 
# # var <- names(foyer)
# #a1 <- c('f7rb', 'f7ra', 'f7gx', 'f2aa', 'f7gt', 'f2an', 'f2am', 'f7gw', 'f7gs', 'f8td', 'f7nz', 'f1br', 'f7jy', 'f7cu', 'f7xi', 'f7xo', 'f7xn', 'f7xw', 'f7xy', 'f6hj', 'f7qt', 'f7ql', 'f7qm', 'f7qd', 'f7qb', 'f7qc', 'f1ar', 'f7my', 'f3vv', 'f3vu', 'f3vt', 'f7gu', 'f3vd', 'f2al', 'f2bh', 'f7fm', 'f8uy', 'f7td', 'f7gv', 'f7is', 'f7iy', 'f7il', 'f7im', 'f7ij', 'f7ik', 'f1er', 'f7wl', 'f7wk', 'f7we', 'f6eh', 'f7la', 'f7uh', 'f7ly', 'f8wy', 'f8wx', 'f8wv', 'f7sb', 'f7sc', 'f7sd', 'f7se', 'f7sf', 'f7sh', 'f7si',  'f1dr', 'f7hs', 'f7hr', 'f7hy', 'f7hk', 'f7hj', 'f7hm', 'f7hl', 'f7ho', 'f7hn', 'f4gc', 'f4gb', 'f4ga', 'f4gg', 'f4gf', 'f4ge', 'f7vz', 'f7vy', 'f7vx', 'f7vw', 'f7xe', 'f6aa', 'f1cr', 'f7ka', 'f7ky', 'f7db', 'f7dq', 'f2da')
# #a2 <- setdiff(a1,names(foyer))
# #b1 <- c('pondfin', 'alt', 'hsup', 'ass_mat', 'zone_apl', 'inactif', 'ass', 'aer', 'code_postal', 'activite', 'type_sal', 'jour_xyz', 'boursier', 'etr', 'partiel1', 'partiel2', 'empl_dir', 'gar_dom', 'categ_inv', 'opt_colca', 'csg_taux_plein','coloc') 
# # hsup feuille d'impot
# # boursier pas dispo
# # inactif etc : extraire cela des donn?es clca etc
# 
# # tester activit? car 0 vaut actif
# table(is.na(final2$activite),useNA="ifany")
# 
# saveTmp(final2, file= "final2.Rdata")


    from src.countries.france.data.erf.build_survey.utilitaries import check_structure
    control(final2, debug=True)
    print final2.age.isnull().sum()
    final2 = final2.drop_duplicates(cols='noindiv')
    
    print '    Filter to manage the new 3-tables structures:'
    # On récupère les foyer, famille, ménages qui ont un chef :
    liste_men = unique(final2.loc[final2['quimen']==0,'idmen'].values)
    liste_fam = unique(final2.loc[final2['quifam']==0,'idfam'].values)
    liste_foy = unique(final2.loc[final2['quifoy']==0,'idfoy'].values)
    
    #On ne conserve dans final2 que ces foyers là :
    print 'final2 avant le filtrage' ,len(final2)
    final2 = final2.loc[final2.idmen.isin(liste_men), :]
    final2 = final2.loc[final2.idfam.isin(liste_fam), :]
    final2 = final2.loc[final2.idfoy.isin(liste_foy), :]
    print 'final2 après le filtrage', len(final2)
    
    check_structure(final2)
    
    from src.countries.france import DATA_SOURCES_DIR
    test_filename = os.path.join(DATA_SOURCES_DIR,"test.h5") 
    store = HDFStore(test_filename)
    store['survey_'+ str(year)] = final2
    print 'fin du traitement des données'
    
if __name__ == '__main__':
    final()
