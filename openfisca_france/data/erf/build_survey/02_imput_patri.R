#rm(list = ls())
# RVersion =R.Version()
# if (RVersion$os != "linux-gnu") {
#   setwd("C:/Users/Utilisateur/Dropbox/python_project/mSim/R")
# } else {
#   setwd("/home/benjello/Dropbox/python_project/mSim/R")}
# rm(RVersion)

message('Entering 02_imput_patri')
message('Building comparable tables')

library(Hmisc)
library(reshape)
library(StatMatch)
library(ggplot2)
library(lmtest)
library(optmatch)
library(xtable)

source('00_config.R')
source('debin.R')
source('prepa_var_patrimoine.R')


model <- lm(pat_new~ sexepr + agepr + I(agepr**2) + diplopr + occuppr + occupcj + rminter + typmen + tu99, data=pat)
summary(model)
modellog <-lm(logpat_new ~ sexepr + agepr +I(agepr**2) + diplopr + occuppr + occupcj + logrminterdeb + typmen + tu99, data=pat)

allvars <- c("occuppr", "agepr","occupcj","diplopr","logrminterdeb", "sexepr", "typmen", "tu99")
#donation 
classes <-  c("typmen", "occuppr")
################################################################################################
## define function impute_patri d'imputation du patrimoine
impute_patri <- function(imputed, ref, allvars, classes){
  require(car)
  require(MASS)  
  # use formula
  modellog <- lm(logpat_new ~ sexepr + agepr +I(agepr**2) + diplopr + occuppr + occupcj + logrminterdeb + typmen, data=ref)
  ref$patri_predictedlog <- predict(modellog, newdata=ref)
  imputed$patri_predictedlog<- predict(modellog, newdata=imputed)
  ref$res = ref$logpat_new-ref$patri_predictedlog
  matchvars <- setdiff(allvars, classes)
  gc()
  twice.out.nnd <- NND.hotdeck(data.rec=imputed,data.don= ref,match.vars=matchvars, don.class= classes, gdist.fun="Manhattan")
  
  imputed <- create.fused(data.rec=imputed, data.don=ref ,mtc.ids=twice.out.nnd$mtc.ids, z.vars="res")
  rm(matchvars)
  imputed$final <- imputed$patri_predictedlog + imputed$res
  ## ET PASSAGE EN EXPONENTIELLE POUR AVOIR LA VALEUR DU PATRIMOINE
 imputed$finalexp <- exp(imputed$final)
  return(imputed)
}

###################################################################################################
# IMPUTATIONS DANS ERF 
# 
# imputed<-impute_patri(erf, pat, allvars, classes)
# sum(is.na(imputed$residuslog1))
pat$patri_predictedlog <- predict(modellog, newdata=pat)


## en LOG 
## 1ere stratégie
erf$patri_predictedlog <- predict(modellog, newdata=erf)
pat$residuslog1 <- pat$logpat_new - pat$patri_predictedlog
## ei = logPi - logPipredi
## hotdeck
allvars <- c("occuppr", "agepr","occupcj","diplopr","logrminterdeb", "sexepr", "typmen", "tu99")
classes <- c("typmen", "diplopr") 
#matching variables
matchvars <- setdiff(allvars, classes)
gc()

begin.out.nnd <- NND.hotdeck(data.rec=erf,data.don= pat,match.vars=matchvars, don.class=classes, gdist.fun="Gower")
#begin.out.nnd <- NND.hotdeck(data.rec=erf,data.don= pat,match.vars=matchvars, don.class=classes, gdist.fun="Gower", constrained= TRUE, constr.alg= "relax")
#begin.out.nnd <- RANDwNND.hotdeck(data.rec=erf,data.don=pat, weight.don= pat$pond, match.vars=matchvars, don.class=classes, gdist.fun="Gower")


erf <- create.fused(data.rec=erf, data.don=pat ,mtc.ids=begin.out.nnd$mtc.ids, z.vars="residuslog1")
rm(matchvars)
erf$final <- erf$patri_predictedlog + erf$residuslog1
## ET PASSAGE EN EXPONENTIELLE POUR AVOIR LA VALEUR DU PATRIMOINE
erf$finalexp <- exp(erf$final)

## Pour ne pas fausser, on effectue les mêmes étapes sur la base pat- pat_prédit+ res
allvars <- c("occuppr", "agepr","occupcj","diplopr","logrminterdeb", "sexepr", "typmen", "tu99")
classes <- c("typmen", "diplopr") 
#matching variables
matchvars <- setdiff(allvars, classes)
gc()
out.nnd <- NND.hotdeck(data.rec=pat,data.don= pat,match.vars=matchvars, don.class= classes, gdist.fun="Gower")
#out.nnd <- NND.hotdeck(data.rec=pat,data.don= pat,match.vars=matchvars, don.class= classes, gdist.fun="Gower", constrained=TRUE, constr.alg= "relax")
#out.nnd <- RANDwNND.hotdeck(data.rec=pat,data.don= pat, weight.don= pat$pond, match.vars=matchvars, don.class= classes, gdist.fun="Gower")

# Error in NND.hd(rec = l.rec[[h]], don = l.don[[h]], dfun = dist.fun, constr = constrained,  : 
#   The pairmatch() function in package 'optmatch' requires the no. 
# of donors to be greater or equal than the no. of recipients

pat <- create.fused(data.rec=pat, data.don=pat ,mtc.ids=out.nnd$mtc.ids, z.vars="residuslog1")
rm(matchvars)
pat$final <- pat$patri_predictedlog + pat$residuslog1
## ET PASSAGE EN EXPONENTIELLE POUR AVOIR LA VALEUR DU PATRIMOINE
describe(pat$final)
pat$finalexp <- exp(pat$final)

# categorize le patrimoine imputé dans la base ERF#
cats = c('01', '02','03','04','05','06','07','08','09','10','11','12')
bins = c( 0,3000,7500,15000,30000,45000,75000,105000,150000,225000,300000,450000,5000000)
erf$patri_cat <- categorize(erf$finalexp, seuil=bins, categories=cats )

describe(erf$finalexp)
describe(pat$patri, weights=pat$pond)
describe(erf$patri_cat, weights=erf$wprm)
describe(erf$patri_cat)
pat$patri_cat <- categorize(pat$finalexp, seuil=bins, categories=cats )

#describe(pat$patri_cat, weights=pat$pond)


############################################################################################
## counting the nb of patrimoine correspondants aux redevables de l'isf
## tranches de ISF 2005
## dans base PAT

pat$zz <- ifelse((pat$pat_new <= 732000),0,1)
pat$zza <- ifelse((732000 <= pat$pat_new)*(pat$pat_new <= 1180000), 0, 1) 
pat$zzb <- ifelse((1180000 <= pat$pat_new)*(pat$pat_new <= 2339000), 0, 1) 
pat$zzc <- ifelse((2339000<= pat$pat_new)*(pat$pat_new <= 3661000), 0, 1) 
pat$zzd <- ifelse((3661000<= pat$pat_new)*(pat$pat_new <= 7017000), 0, 1)
pat$zze <- ifelse((7017000<= pat$pat_new)*(pat$pat_new <= 15255000),0,1)
pat$zzf <- ifelse((15255000<= pat$pat_new),0,1)

## dans base ERF synthétique

erf$zz <- ifelse((erf$finalexp <= 732000),0,1)
erf$zza <- ifelse((732000 <= erf$finalexp)*(erf$finalexp <= 1180000), 0, 1) 
erf$zzb <- ifelse((1180000 <= erf$finalexp)*(erf$finalexp <= 2339000), 0, 1) 
erf$zzc <- ifelse((2339000<= erf$finalexp)*(erf$finalexp <= 3661000), 0, 1) 
erf$zzd <- ifelse((3661000<= erf$finalexp)*(erf$finalexp <= 7017000), 0, 1)
erf$zze <- ifelse((7017000<= erf$finalexp)*(erf$finalexp <= 15255000),0,1)
erf$zzf <- ifelse((15255000<= erf$finalexp),0,1)


## there exist weighted table
##normwt= TRUE make weights sum to length(x)
wtd.table(erf$zza, weights=erf$wprm)

wtd.table(pat$zz, weights=pat$pond)

## multiplie par combien pour avoir l'ensemble de la population (fiscale)?
## COMPARER AUX CHIFFRES PARAM ISF DE L'ANNEXE SIMULATEUR DE PIKETTY (dropbox)
#using RANDwDHD
# 649101/(649101+22230779 )
# [1] 0.02836995
# > 376652.1 /(376652.1 +22920226.4)
# [1] 0.01616749

############################################################################################
### SORT THE QUANTILE FOR PAT_NEW
wtd.quantile(pat$pat_new, weights= pat$pond, normwt=TRUE, na.rm=TRUE)
### sort the quantile for erf pat
wtd.quantile(erf$finalexp, weights= erf$wprm, normwt=TRUE, na.rm=TRUE)
#####################################
describe(erf$zza, weights=erf$wprm)
describe(pat$zza, weights=pat$pond)
table(erf$zza, useNA='ifany')
table(pat$zza, useNA='ifany')

##end of hotdeck

## HISTOGRAMME et Pourcentages 
## histogramme de patri et densité pondérée (pat_new) dans PAT
## histogramme de patri_cat dans ERF et densité pondérée de finalexp
## histogramme de patri et densitéd pondérée de finalexp dans PAT
### treat x var as numeric to obtain an overall density

data1 <- data.frame(cat=pat$patri, w=pat$pond, source="patrimoine")
data2 <- data.frame(cat=erf$patri_cat, w=erf$wprm, source="erf")

data_plot <- rbind(data1,data2)
p <- ggplot(data_plot)
p + geom_bar(aes(x=cat, weight=w, fill=source), position="dodge") 

# prepare for merging with menagem
patrim <- data.frame(ident = erf$ident, patri=erf$finalexp)
load(menm)
menagem <- merge(menagem, patrim, by="ident",all.x = TRUE)
save(menagem,file=menm)
rm(patrim,menagem)  





