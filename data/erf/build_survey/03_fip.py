# -*- coding:utf-8 -*-
# # OpenFisca
# # Some individuals are declared as 'personne à charge' (pac) on 'tax forms' but are not present in the erf or eec tables.
# # We add them to ensure consistency between concepts.
# # Creates a 'fipDat' table containing all these 'fip individuals'
# 
from src.countries.france.data.erf.datatable import ErfsDataTable
from pandas import DataFrame
from numpy import array, where, dtype, NaN #, float32
from pandas import  HDFStore, melt
import gc
import os
from src import SRC_PATH

from subprocess import Popen
from numpy import logical_not as not_
from numpy import logical_and as and_
from numpy import logical_or as or_

def run():
    
# message('03_fip')

    year = 2006
    df = ErfsDataTable(year=year)
    
    print '03_fip'
# # anaisenf: année de naissance des PAC
# erfFoyVar <- c('anaisenf','declar')
# foyer <- LoadIn(erfFoyFil)
# foyer <- LoadIn(erfFoyFil,erfFoyVar)

    erfFoyVar = ['anaisenf', 'declar']
    foyer = df.get_values(table = "foyer")
    foyer = df.get_values(table="foyer", variables=erfFoyVar)
    print "anaisenf: année de naissance des PAC-------------------"
 
 
# #***********************************************************************************************************
    print "message('Step 1 : on recupere les personnes à charge des foyers')"
# #**********************************************************************************************************
# # On traite les cas de déclarations multiples pour ne pas créer de doublon de pac
# # TODO:
# 
# # anaisenf is a string containing letter code of pac (F,G,H,I,J,N,R) and year of birth (example: 'F1990H1992')
# # when a child is invalid, he appears twice in anaisenf (example: F1900G1900 is a single invalid child born in 1990)
# 
# # On récupère toutes les pac des foyers 
# L <- max(nchar(foyer$anaisenf))/5 # nombre de pac maximal
# fip <-data.frame(declar = foyer$declar)

    foyer['anaisenf'] = foyer['anaisenf'].astype('string')
    L = len(max(foyer['anaisenf'], key=len))/5
#     print L, max(foyer['anaisenf'], key=len)
    
    multi_index_columns = [array(['declar']), array(['subtype'])]
    fip = DataFrame(foyer['declar'], columns=multi_index_columns)
#     print fip.head()
#     print fip.tail()

# for (i in c(1:L)){
#   eval(parse(text = paste('fip$typ.',as.character(i),'<- substr(foyer$anaisenf,5*(i-1)+1,5*(i-1)+1)',sep = '')))
#   eval(parse(text = paste('fip$naia.',as.character(i),'<- as.numeric(substr(foyer$anaisenf,5*(i-1)+2,5*(i-1)+5))',sep = '')))
# }


#    Separating the string coding the pac of each HH. Creating a list containing the new variables.

    fip_varlist = []
    for i in range(1,L+1):
        fip[('déclaration', str(i))] = fip[('declar', 'subtype')]
        fip_varlist.append(('type_pac', str(i)))
        fip[('type_pac', str(i))] = foyer['anaisenf'].str[5*(i-1)]
        fip_varlist.append(('naia', str(i)))
        fip[('naia', str(i))] = foyer['anaisenf'].str[5*(i-1)+1:5*(i-1)+5]
        
    del fip[('declar', 'subtype')]

    print "separating data of column anaisenf-------------"
    print fip_varlist
    print fip.head()


# fip <- fip[!is.na(fip$typ.1),]
# fip <- reshape(fip,direction ='long', varying=2:17, sep=".")
# fip <- fip[!is.na(fip$naia),]
# fip <- fip[order(fip$declar,-rank(fip$typ),fip$naia),c('declar','naia','typ')]
# fip$N <- row(fip)[,1]
# str(fip$N) #TODO: what is the point of this command
    print "elimination des foyers fiscaux sans pac--------------------------"
    fip = fip[fip[('type_pac', str(1))] != 'n']
    fip = fip.stack()

#     fip['declar'] = fip['value']
#     del fip['variable'], fip['value']
    fip = fip.sort(columns=['déclaration','naia','type_pac'])
    
    #Clearing missing values and changing data format
    fip = fip[and_(fip['naia'] != '', fip['naia'] != 'an')]
    fip = fip.reset_index()
    fip.columns = ['nb_row', 'no_pac', 'déclaration', 'naia', 'type_pac']
    del fip['no_pac']
#     fip['nb_row'] = fip['nb_row'].astype('str')
#     fip['type_pac'] = fip['type_pac'].astype('str')
#     fip.set_index(keys=['nb_row'])
    print fip.head(10)
    print fip.columns

# library(plyr)
# # on enlève les F pour lesquels il y a un G ;
# tyF <- fip[fip$typ == 'F',]
# tyF <- upData(tyF,drop = c('typ'))
# tyG <- fip[fip$typ == 'G',]
# tyG <- upData(tyG,drop = c('N'))

    print "--------------------------------------"
    tyF = fip[fip['type_pac'] == 'F']
    tyG = fip[fip['type_pac'] == 'G']
    del tyF['type_pac'], tyG['type_pac']
    
# # There are situations where twins are F and G (ERF2009) !
# tyG['dup'] <- FALSE
# tyG['dup'] <- duplicated(tyG[,c("declar","naia")])
# tyF['dup'] <- FALSE
# tyF['dup'] <- duplicated(tyF[,c("declar","naia")])
    tyF['dup'] = False
    tyG['dup'] = False
    tyF.drop_duplicates(cols=('déclaration', 'naia'))
    tyG.drop_duplicates(cols=('déclaration', 'naia'))
    print tyF.head()
    print '----------------------------------------------------'

# tyFG <- join(tyF,tyG, by = c('declar','naia','dup'),type = 'right',match = 'first')
# iden <- tyFG$N
# rm(tyF,tyG,tyFG)
    tyFG = tyF.merge(tyG, on=['déclaration', 'naia', 'dup'])
    iden = tyFG
    del tyF, tyG, tyFG
    print iden.head()
    print "merging done ------------------------------------------"
    
# # on enlève les H pour lesquels il y a un I ;
# tyH <- fip[fip$typ == 'H',]
# tyH <- upData(tyH,drop = c('typ'))
# tyI <- fip[fip$typ == 'I',]
# tyI <- upData(tyI,drop = c('N'))
# tyHI <- join(tyH,tyI, by = c('declar','naia'),type = 'right',match = 'first')
# iden <- c(iden,tyHI$N) #TODO: ça fait quoi ça ?
# rm(tyH,tyI,tyHI,L)

    tyH = fip[fip['type_pac'] == 'H']
    tyI = fip[fip['type_pac'] == 'I']
    tyHI = tyH.merge(tyI, on=['déclaration', 'naia'])
    
    print iden.head()
    print "------------------"
    print tyHI.head()
    print "tyHI done"

# indivifip <- fip[!fip$N %in% iden,c(1:3)];
# rm(foyer,fip)
# table(indivifip$typ,useNA="ifany")

    indivifip = fip[fip['déclaration'] not in iden['déclaration']]
    print "check"
    return
# 
# #************************************************************************************************************/
# message('Step 2 : matching indivifip with eec file')
# #************************************************************************************************************/
# indVar <- c('ident','noi','declar1','declar2','persfip','persfipd','naia','rga','lpr','noindiv','ztsai','ztsao','wprm')
# indivi <- LoadIn(indm,indVar)
# 
# indivi$noidec <- as.numeric(substr(indivi$declar1,1,2))
# 
# pac <- indivi[!is.na(indivi$persfip) & indivi$persfip == 'pac',]
# pac$key1 <- paste(pac$naia,pac$declar1)
# pac$key2 <- paste(pac$naia,pac$declar2)
# indivifip$key <- paste(indivifip$naia,indivifip$declar)
# 
# fip <- indivifip[!indivifip$key %in% pac$key1,]
# fip <- fip[!fip$key %in% pac$key2,]
# 
# # We build a dataframe to link the pac to their type and noindiv
# 
# table(duplicated(pac[,c("noindiv")]))
# pacInd1 <- merge(pac[,c("noindiv","key1","naia")],
#                 indivifip[,c("key","typ")], by.x="key1", by.y="key")
# 
# pacInd2 <- merge(pac[,c("noindiv","key2","naia")],
#                 indivifip[,c("key","typ")], by.x="key2", by.y="key")
# 
# table(duplicated(pacInd1))
# table(duplicated(pacInd2))
# 
# pacInd1 <-rename(pacInd1,c("key1" = "key"))
# pacInd2 <-rename(pacInd2,c("key2" = "key"))
# pacInd <- rbind(pacInd1,pacInd2)
# rm(pacInd1,pacInd2)
# table(duplicated(pacInd[,c("noindiv","typ")]))
# table(duplicated(pacInd$noindiv))
# 
# pacIndiv <- pacInd[!duplicated(pacInd$noindiv),]
# saveTmp(pacIndiv,file="pacIndiv.Rdata")
# rm(pacInd,pacIndiv)
# 
# 
# # We keep the fip in the menage of their parents because it is used in to
# # build the famille. We should build an individual ident for the fip that are
# # older than 18 since they are not in their parents' menage according to the eec
# individec1 <- subset(indivi, (declar1 %in% fip$declar) & (persfip=="vous"))
# individec1 <- individec1[,c("declar1","noidec","ident","rga","ztsai","ztsao")]
# individec1 <- upData(individec1,rename=c(declar1="declar"))
# fip1       <- merge(fip,individec1)
# 
# # TODO: On ne s'occupe pas des declar2 pour l'instant
# # individec2 <- subset(indivi, (declar2 %in% fip$declar) & (persfip=="vous"))
# # individec2 <- individec2[,c("declar2","noidec","ident","rga","ztsai","ztsao")]
# # individec2 <- upData(individec2,rename=c(declar2="declar"))
# # fip2 <-merge(fip,individec2)
# 
# # Il ya des jumeaux et des triplés dans fip1
# # table(duplicated(fip1))
# # table(duplicated(fip2))
# 
# #fip <- rbind(fip1,fip2)
# fip <- fip1
# table(fip$typ)
# 
# # On crée des variables pour mettre les fip dans les familles 99, 98, 97
# fip <- within(fip,{
#   persfip <- 'pac'
#   year <- as.numeric(year)
#   noi <- 99
#   noicon <- NA
#   noindiv <- declar
#   noiper   <- NA
#   noimer   <- NA
#   declar1  <- declar  # TODO declar ?
#   naim     <- 99 
#   lien     <- NA
#   quelfic  <- "FIP"
#   acteu    <- NA   
#   agepf    <- year - naia - 1
#   lpr      <- ifelse(agepf<=20,3,4)  # TODO pas tr?s propre 
#   stc      <- NA
#   contra   <- NA
#   titc     <- NA
#   mrec     <- NA
#   forter   <- NA
#   rstg     <- NA
#   retrai   <- NA
#   cohab    <- NA
#   sexe     <- NA
#   persfip  <- "pac"
#   agepr    <- NA 
#   actrec   <- ifelse(agepf<=15,9,5)})
# 
# ## TODO probleme actrec des enfants fip entre 16 et 20 ans : on ne sait pas s'ils sont étudiants ou salariés */
# ## TODO problème avec les mois des enfants FIP : voir si on ne peut pas remonter à ces valeurs
# 
# ## On gére les noi des jumeaux et des triplés des fip
# 
# while ( any(duplicated( fip[,c("noi","ident")]) ) ) {
#   dup <- duplicated( fip[, c("noi","ident")])
#   tmp <- fip[dup,"noi"]
#   fip[dup, "noi"] <- (tmp-1)    
# }
# 
# fip$idfoy   <- 100*fip$ident + fip$noidec
# fip$noindiv <- 100*fip$ident + fip$noi
# fip$typ <- NULL
# fip$key <- NULL
# 
# 
# table(duplicated(fip$noindiv))
# 
# save(fip,file=fipDat)
# rm(fip,fip1,individec1,indivifip,indivi,pac)
# # rm(fip2,individec2)

if __name__ == '__main__':
    run()