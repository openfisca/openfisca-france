
rm(list = ls())
RVersion =R.Version()
if (RVersion$os != "linux-gnu") {
  setwd("C:/Users/Utilisateur/Dropbox/python_project/mSim/R")
} else {
  setwd("/home/benjello/Dropbox/python_project/mSim/R")}
rm(RVersion)

message('Entering 02_imput_residence_principale')
message('Building comparable tables')

source('00_config.R')
source('debin.R')

library(Hmisc)
library(reshape)
library(StatMatch)
library(ggplot2)
library(MASS)
library(rms)

# load(lgtMenFil)
# loadTmp("erf.Rdata");
# loadTmp("logement.Rdata");
# summary(menage1$bpl2)
# str(menage1$bpl2)
# wtd.table(menage1$soc[menage1$bpl2>0], weights= menage1$qex)
# ?wtd.table
# 10%

## merging table adresse et menage1 pour ajouter var= tu99
load("~/Data/R/logement/2006/menage1.Rdata")
load("~/Data/R/logement/2006/adresse.Rdata")


# SOC Table : MENAGE
# STATUT D'OCCUPATION DU LOGEMENT
# 0 Propriétaire non-accédant
# 1 Accédant à la propriété
# 2 Locataire d'un logement loué vide
# 3 Autre locataire (logé en meublé, hôtel ou garni), sous-locataire
# 4 Fermier ou métayer
# 5 Logé gratuitement

logmt1 <- subset(menage1, soc==0|soc==1|soc==4, select=c(soc,idlog, bpl2, msexe, mag, msituac, mdiplo, msitua, mtyad, qex, mrd_bis))
logmt_adresse <- subset (adresse, select= c(idlog, tu99))
logmt2 <- merge(logmt1,logmt_adresse, by="idlog")
describe(logmt2$soc)
wtd.table(logmt2$bpl2, weights=logmt2$qex)
describe(logmt2$bpl2)
sum(logmt2$bpl2[!is.na(logmt2$bpl2)] < 50000)

logmt <- subset(logmt2, !is.na(bpl2))

## see directly to add on logement.dta
rm(menage1)
rm(adresse)
rm(logmt1)
rm(logmt_adresse)

# USING Tmp files from imput-loyer
# loadTmp("lgtmen.Rdata");
# loadTmp("lgtadr.Rdata");
# logement <- merge(lgtmen, lgtadr, by = "ident");
# rm(lgtadr,lgtmen);
# saveTmp(logement,file="logement.Rdata");
# loadTmp("logement.Rdata");
# summary(logement$ident)
# View(logement$ident)
# summary(logmt)
# 'ident' dans logement= idlog.

###################################################
summary(logmt)
table(logmt$msitua, useNA='ifany')
table(logmt$msituac, useNA='ifany')
table(logmt$mtyad, useNA='ifany')
## préparation de la table logmt

### tranches urbaines en 5 postes (attention: recoding different from tu99_recoded) (voir ci-dessous en ERF pour def)
logmt <- within(logmt, {
  tu99[tu99==1|tu99==3] <- 2
  tu99[tu99==4|tu99==5] <- 3
  tu99[tu99==6|tu99==7] <- 4
  tu99[tu99==0] <- 1
  tu99[tu99==8] <- 5
})
table(logmt$tu99, useNA='ifany')

# travaille sur les var situa, situac et acteu5cj et pr
"La variable ACTEU5 est une recomposition de l'activité au sens BIT52 de la personne en 5 modalités :
  '1' = « salarié »,
'2' = « indépendant »,
'3' = « chômeur »,
'4' = « retraité »,
'5' = « autre inactif »,
calculée à partir des variables de l' EEC : ACTEU6 et STATUT et de l'ERFS-EEC : CS8COR.
La variable ACTEU5 est dans la table INDIVI06. Les variables ACTEU5PR et ACTEU5CJ (pour la personne de référence et le conjoint) sont dans la table MENAGE06."

# MSITUA Table : MENAGE
# OCCUPATION PRINCIPALE DE LA PERSONNE DE REFERENCE
# 1 Occupe actuellement un emploi
# 2 Apprenti sous contrat ou en stage rémunéré --> 1 
# 3 Etudiante, élève, en formation ou en stage rémunéré --> 5
# 4 Chômeur (inscrit ou non à l'ANPE) --> 3 
# 5 Retraité ou retiré des affaires ou en préretraite --> 4
# 6 Femme ou homme au foyer--> 5 
# 7 Autre situation (personne handicapée, ...) --> 5

logmt <- within(logmt, {
  msitua[msitua==3|msitua==7|msitua==6] <- 9
  msitua[msitua==2] <- 1
  msitua[msitua==4] <- 3
  msitua[msitua==5] <- 4
  msitua[msitua==9] <- 5
})

logmt <- within(logmt, {
  msituac[msituac==3|msituac==7|msituac==6] <- 9
  msituac[msituac==2] <- 1
  msituac[msituac==4] <- 3
  msituac[msituac==5] <- 4
  msituac[msituac==9] <- 5
})

## qd situation occup cj='na' set to 0
logmt$msituac[is.na(logmt$msituac)] <- 0
table(logmt$msituac, useNA='ifany')

## typmen 
# Recode patrimoine typmen to match erf typmen coding
# 1 Personne seule
# 2 Couple sans enfant -> 3
# 3 Couple avec 1 enfant -> 4
# 4 Couple avec 2 enfants -> 4
# 5 Couple avec 3 enfants ou plus -> 4
# 6 Famille monoparentale -> 2
# 7 Autre cas -> 5

#in enquête logement
# MTYAD Table : MENAGE
# TYPE DE MENAGE SELON LE TYPE DE LA FAMILLE PRINCIPALE ET LE NOMBRE D'ENFANTS (*)
# 110 Homme vivant seul --> 1
# 120 Femme vivant seule --> 1
# 200 Ménage de plusieurs personnes sans famille --> 5
# 311 Homme avec un enfant (*) 
# 312 ......avec deux enfants (*)
# 313 ..... avec trois enfants ou plus (*)
# 321 Femme avec un enfant (*)
# 322 ..... avec deux enfants (*)
# 323 ..... avec trois enfants ou plus (*)
# 400 Couple sans enfant (*)
# 401 ...... avec un enfant (*)
# 402 ...... avec deux enfants (*)
# 403 ...... avec trois enfants ou plus (*)

logmt <- within(logmt, {
  mtyad[mtyad==110|mtyad==120] <- 1
  mtyad[mtyad==200] <- 5
  mtyad[mtyad==400] <- 3
  mtyad[mtyad==311|mtyad==312|mtyad==313|mtyad==321|mtyad==322|mtyad==323] <- 2
  mtyad[mtyad==401|mtyad==402|mtyad==403] <- 4
})

# enq ERF
# DDIPL
# Diplôme le plus élevé obtenu (7 postes)
# Diplôme non déclaré
# 1 Diplôme supérieur
# 3 Baccalauréat + 2 ans
# 4 Baccalauréat ou brevet professionnel ou autre diplôme de ce niveau
# 5 CAP, BEP ou autre diplôme de ce niveau
# 6 Brevet des collèges
# 7 Aucun diplôme ou CEP
# in enquête logmt
# DIPLOME LE PLUS ELEVE OBTENU PAR LA PERSONNE DE REFERENCE
# 1 Aucun diplôme --> 7
# 2 Certificat d'études primaires (CEP) --> 7
# 3 Brevet d'études du 1er cycle (BEPC) ou BE, ou brevet des collèges --> 6
# 4 CAP, BEP ou autre diplôme de ce niveau --> 5
# 5 Baccalauréat professionnel --> 4 
# 6 Baccalauréat technique ou technologique --> 4
# 7 Baccalauréat général --> 4
# 8 Bac+2 --> 3
# 9 Supérieur à BAC+2 --> 1

logmt <- within(logmt, {
  mdiplo[mdiplo==1|mdiplo==2] <- 11
  mdiplo[mdiplo==3] <- 13
  mdiplo[mdiplo==4] <- 17
  mdiplo[mdiplo==7|mdiplo==6|mdiplo==5] <- 4
  mdiplo[mdiplo==8] <- 3
  mdiplo[mdiplo==11] <- 7
  mdiplo[mdiplo==13] <- 6
  mdiplo[mdiplo==17] <- 5
  mdiplo[mdiplo==9] <- 1
})

## renames var in logmt
logmt$occuppr <- logmt$msitua
logmt$occupcj <- logmt$msituac
logmt$sexepr <- logmt$msexe
logmt$agepr <- logmt$mag
logmt$diplopr<- logmt$mdiplo
logmt$typmen <- logmt$mtyad
logmt$rminter <- logmt$mrd_bis
logmt$logrminter <- log(logmt$mrd_bis)

describe(logmt$rminter)
str(logmt$rminter)

## get rid of 'old_names' vars
logmt$idlog <- NULL
logmt$mrd_bis<- NULL
logmt$msexe<- NULL
logmt$mtyad <- NULL
logmt$msituac <- NULL
logmt$msitua <- NULL
logmt$mdiplo<- NULL
logmt$mag <- NULL

names(logmt)

#treat them as factor ?
logmt$tu99 <- as.factor(logmt$tu99)
logmt$diplopr <- as.factor(logmt$diplopr)
logmt$typmen <- as.factor(logmt$typmen)
logmt$sexepr<- as.factor(logmt$sexepr)
logmt$occuppr <- as.factor(logmt$occuppr)
logmt$occupcj<- as.factor(logmt$occupcj)
logmt$rminter <- as.character(logmt$rminter)


## préparation de la table ERF
load(menm)
str(menagem)
table(menagem$so, useNA='ifany')

erf <- subset(menagem, select= c(ident, spr, agepr, ddipl, acteu5pr, acteu5cj, ztsam, zperm, typmen5, wprm, tu99))
erf <- subset(menagem,so==1|so==2, select= c(ident, spr, agepr, ddipl, acteu5pr, acteu5cj, ztsam, zperm, typmen5, wprm, tu99))
rm(menagem)


## revenus dans base ERF
erf$rev_men <- erf$ztsam+ erf$zperm
erf$ztsam <- NULL
erf$zperm <- NULL
cats = c('01', '02','03','04','05','06','07','08','09','10')
seuils = c( 0,9754,13335,16900,20540,25037, 29969, 35262, 42560,55000)
erf$rev_men_cat <- categorize(erf$rev_men, seuil=seuils, categories=cats )
# IN ENQU LGT
# MRD_BIS Table : MENAGE
# REVENU ANNUEL TOTAL PERÇU PAR LE MENAGE EN FRANCE METRO
# - en déciles - redressé - corrigée
# 1 Moins de 9 754 
# 2 De 9 754  à moins de 13 335 
# 3 De 13 335  à moins de 16 900 
# 4 De 16 900  à moins de 20 540 
# 5 De 20 540  à moins de 25 037 
# 6 De 25 037  à moins de 29 969 
# 7 De 29 969  à moins de 35 262 
# 8 De 35 262  à moins de 42 560 
# 9 De 42 560  à moins de 55 000 
# 10 55 000  et plus


## recoding tu99
# 1 Commune rurale
# 2 Moins de 20 000 habitants
# 3 De 20 000 à 100 000 habitants
# 4 Plus de 100 000 habitants
# 5 Agglomération parisienne hors Paris et Ville de Paris 

# Tranche d'unité urbaine en 9 postes
# 0 Commune rurale --> 1 
# 1 Unité urbaine de moins de 5 000 habitants --> 2
# 2 Unité urbaine de 5 000 à 9 999 habitants --> 2
# 3 Unité urbaine de 10 000 à 19 999 habitants --> 2
# 4 Unité urbaine de 20 000 à 49 999 habitants --> 3
# 5 Unité urbaine de 50 000 à 99 999 habitants --> 3
# 6 Unité urbaine de 100 000 à 199 999 habitants --> 4
# 7 Unité urbaine de 200 000 à 1 999 999 habitants --> 4
# 8 Unité urbaine de Paris --> 5

table(erf$tu99, useNA='ifany')

erf <- within(erf, {
  tu99[tu99==1|tu99==3] <- 2
  tu99[tu99==4|tu99==5] <- 3
  tu99[tu99==6|tu99==7] <- 4
  tu99[tu99==0] <- 1
  tu99[tu99==8] <- 5
})

erf$acteu5pr[erf$acteu5pr==2] <- 1
erf$acteu5cj[erf$acteu5cj==2] <- 1
table(erf$acteu5pr, useNA='ifany')
table(erf$acteu5cj, useNA='ifany')
erf$acteu5cj[is.na(erf$acteu5cj)] <- 0


## conversion names
erf$occuppr <- erf$acteu5pr
erf$occupcj <- erf$acteu5cj
erf$sexepr <- erf$spr
erf$diplopr <- erf$ddipl
erf$rminter <- erf$rev_men_cat
erf$rminterdeb <-erf$rev_men
erf$logrminterdeb <- log(erf$rev_men)
erf$typmen <- erf$typmen5

##
erf$typmen5 <- NULL
erf$acteu5pr<- NULL
erf$acteu5cj<- NULL
erf$spr <- NULL
erf$ddipl <- NULL
erf$rev_men_cat <- NULL

erf$occuppr <- as.factor(erf$occuppr)
erf$occupcj <- as.factor(erf$occupcj)
erf$sexepr <- as.factor(erf$sexepr)
erf$diplopr <- as.factor(erf$diplopr) 
erf$typmen <- as.factor(erf$typmen)
#erf$agepr_cat <- as.factor(erf$agepr_cat)
erf$tu99 <- as.factor(erf$tu99)

describe(erf$typmen)
describe(logmt$typmen)

names(erf)
# TODO: should it be ordered ?
erf$rminter <-as.factor(as.ordered(erf$rminter))

## imputation de la valeur de résidence principale

## BOXCOX
bc <- boxcox(bpl2 ~ sexepr + agepr + I(agepr**2) + diplopr + occuppr + occupcj + rminter + typmen + tu99 , data=logmt)
##
# Assume "bc" is an object returned by boxcox(...), you can do
## value for lambda
with(bc, x[which.max(y)])

## change in log
logmt$logbpl2 <- log(logmt$bpl2) 


# DEBINAGE DE RMINTER DANS LA BASE LOGMT
cats = c('1','2','3','4','5','6','7','8','9','10')
seuils = c( 0,9754,13335,16900,20540,25037,29969,35262,42560,55000,215600)
logmt$rminterdeb <- debin(logmt$rminter, categories = cats, bins = seuils)
## produit trop de NA's
#log 
logmt$logrminterdeb <- log(logmt$rminterdeb)

describe(logmt$rminterdeb)
str(logmt$logrminterdeb)
str(logmt)
model <- lm(bpl2 ~ sexepr + agepr + I(agepr**2) + diplopr + occuppr + occupcj + rminter + typmen + tu99, data=logmt)
summary(model)
## reg log-log
modellog <-lm(logbpl2 ~ sexepr + agepr +I(agepr**2) + diplopr + occuppr + occupcj + logrminterdeb + typmen + tu99, data=logmt)
summary(modellog)

wtd.table(logmt$typmen[logmt$bpl2>0])

## TEST ## 
allvars <- c("occuppr", "agepr","occupcj","diplopr","logrminterdeb", "sexepr", "typmen")
#donation 
classes <-  c("typmen", "occuppr")
describe(logmt$typmen)

## HOTDECK sur résidus 
logmt$res_princ_pred <- predict(modellog, newdata=logmt)
xtabs(~ typmen+ bpl2, data=logmt)
## en LOG 
## 1ere stratégie
describe(erf$occuppr)
describe(logmt$occuppr)

erf$res_princ_pred <- predict(modellog, newdata=erf)
logmt$residuslog1 <- logmt$logbpl2 - logmt$res_princ_pred
describe(logmt$bpl2)
describe(logmt$residuslog1)
## ei = logPi - logPipredi
## hotdeck
allvars <- c("occuppr", "agepr","occupcj","diplopr","logrminterdeb", "sexepr", "typmen")
classes <- c("typmen", "diplopr") 
#matching variables
matchvars <- setdiff(allvars, classes)
gc()
residence.out.nnd <- NND.hotdeck(data.rec=erf,data.don= logmt ,match.vars=matchvars, don.class=classes, gdist.fun="Gower")
#residence.out.nnd <- NND.hotdeck(data.rec=erf,data.don= logmt,match.vars=matchvars, don.class=classes, gdist.fun="Gower", constrained= TRUE, constr.alg= "relax")
#residence.out.nnd <- RANDwNND.hotdeck(data.rec=erf,data.don=logmt, weigth.don= logmt$qex, match.vars=matchvars, don.class=classes, gdist.fun="Gower")

erf <- create.fused(data.rec=erf, data.don=logmt ,mtc.ids=residence.out.nnd$mtc.ids, z.vars="residuslog1")
rm(matchvars)
erf$final <- erf$res_princ_pred + erf$residuslog1
## ET PASSAGE EN EXPONENTIELLE POUR AVOIR LA VALEUR DU PATRIMOINE
erf$finalexp <- exp(erf$final)
sum(is.na(erf$residuslog1))
sum(is.na(erf$final))
describe(erf$finalexp)

## Pour ne pas fausser, on effectue les mêmes étapes sur la base pat- pat_prédit+ res
allvars <- c("occuppr", "agepr","occupcj","diplopr","logrminterdeb", "sexepr", "typmen")
classes <- c("typmen", "diplopr") 
#matching variables
matchvars <- setdiff(allvars, classes)
gc()
logmt.out.nnd <- NND.hotdeck(data.rec=logmt, data.don=logmt, match.vars=matchvars, don.class= classes, gdist.fun="Gower")
#out.nnd <- NND.hotdeck(data.rec=pat,data.don= logmt, match.vars=matchvars, don.class= classes, gdist.fun="Gower", constrained=TRUE, constr.alg= "relax")
#logmt.out.nnd <- RANDwNND.hotdeck(data.rec=logmt, data.don=logmt, weight.don= logmt$qex, match.vars=matchvars, don.class= classes, gdist.fun="Gower")

# Error in NND.hd(rec = l.rec[[h]], don = l.don[[h]], dfun = dist.fun, constr = constrained,  : 
#   The pairmatch() function in package 'optmatch' requires the no. 
# of donors to be greater or equal than the no. of recipients

logmt <- create.fused(data.rec=logmt, data.don=logmt ,mtc.ids= logmt.out.nnd$mtc.ids, z.vars="residuslog1")
rm(matchvars)
logmt$final <- logmt$res_princ_pred + logmt$residuslog1
## ET PASSAGE EN EXPONENTIELLE POUR AVOIR LA VALEUR DU PATRIMOINE
logmt$finalexp <- exp(logmt$final)

## checking the number of NA's
sum(is.na(logmt$res_princ_pred))
sum(is.na(logmt$residuslog1))
sum(is.na(logmt$finalexp))


## CATEGORISER PR COMPARER
## categoriser?
#erf$res_princ <- categorize(erf$finalexp, seuil=bins, categories=cats)

#describe(erf$finalexp)
describe(logmt$bpl2, weights=logmt$qex)
describe(logmt$finalexp, weights=logmt$qex)
describe(erf$finalexp, weights=erf$wprm)

# describe(erf$patri_cat)
# pat$patri_cat <- categorize(pat$finalexp, seuil=bins, categories=cats )

## OBSERVATIONS DES DISTRIBUTIONS
## CDF avec log
erfCDF  <- wtd.Ecdf(erf$res_princ_pred,weights=erf$wprm);
logmtCDF <- wtd.Ecdf(logmt$res_princ_pred,weights=logmt$pond);
erfCDF_data <- data.frame(x=erfCDF$x,cdf=erfCDF$ecdf,survey="erf")
logmtCDF_data <- data.frame(x=logmtCDF$x,cdf=logmtCDF$ecdf,survey="logmt")
plot_data <- data.frame(rbind(erfCDF_data,logmtCDF_data))
ggplot(plot_data, aes(x=x,y=cdf, color=survey)) + geom_point()

# describe(erf$patri_predictedlog,weights=erf$wprm)
# describe(pat$patri_predictedlog,weights=logmt$pond)

## CDF sans log
erfCDF  <- wtd.Ecdf(erf$finalexp,weights=erf$wprm);
logmtCDF <- wtd.Ecdf(logmt$finalexp,weights=logmt$qex);
logmtpredCDF <- wtd.Ecdf(logmt$res_princ_pred,weights=logmt$qex);
erfCDF_data <- data.frame(x=erfCDF$x,cdf=erfCDF$ecdf,survey="erf")
logmtCDF_data <- data.frame(x=logmtCDF$x,cdf=logmtCDF$ecdf,survey="logmt")
logmtpredCDF_data <- data.frame(x=logmtpredCDF$x,cdf=logmtpredCDF$ecdf,survey="logmtpred")
plot_data <- data.frame(rbind(erfCDF_data,logmtCDF_data,logmtpredCDF_data))
ggplot(plot_data, aes(x=x,y=cdf, color=survey)) + geom_point() + scale_x_log10()


# prepare for merging with menagem
res_princ_file<- data.frame(ident = erf$ident, res_princ=erf$finalexp)
load(menm)
menagem <- merge(menagem, res_princ_file, by="ident",all.x = TRUE)
save(menagem,file=menm)
rm(res_princ_file,menagem)  


## ETUDE DU RESTE= PATRI - PATFI - RES_PRINC
# load(menm)
# menagem$reste <- menagem$patri - menagem$res_princ - menagem$patfi
# #View(menagem[,c('res_princ','patri','patfi', 'reste')])
# menagem$reste[menagem$reste <= 0] <- 0
# m <- ggplot(menagem, aes(x=reste))
# m + geom_histogram(aes(weight = wprm)) 
# m + geom_histogram(aes(y = ..count..))
# summary(menagem$reste)
# summary(menagem)
# menagem$zz <- ifelse((menagem$reste <= 732000),0,1)
# table(menagem$zz)
