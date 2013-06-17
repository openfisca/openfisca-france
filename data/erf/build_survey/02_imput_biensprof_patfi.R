message('Entering 02_imput_biensprof_patfi')
message('Building comparable tables')

library(Hmisc)
library(reshape)
library(xtable)
library(rms)

source('00_config.R')
source('debin.R')
source('prepa_var_patfi.R')

load(patProFil)
load(patMenFil)

# Biens professionnels
sbset3 <- subset(produit04, nature== '3'|nature ==  '4',select= c(ident, nature, montmax, montmin))
str(sbset3)
summary(sbset3)

pat$prona3 <- ifelse((pat$prona=='1'|pat$prona2=='1'), 1, 0)
table(pat$prona3)
## reg d'une variable binaire sur des variables ordinales
pat$prona3<- as.factor(pat$prona3) 
regprof <- glm(prona3 ~ sexepr + agepr + I(agepr**2) + diplopr + occuppr + occupcj + rminter + typmen + tu99, data=pat, family= binomial)
summary(regprof)
pat$prona_imp <- predict(regprof, newdata=pat, type="response")
summary(pat$prona_imp)
pat$dummy[pat$prona_imp < 0.25] <- 0
pat$dummy[pat$prona_imp >= 0.25] <- 1
#View(pat[,c('prona3', 'prona_imp', 'dummy')])
table(pat$dummy)
pat$prona3<- as.numeric(pat$prona3)
table(pat$prona3)

pat$fit <- ifelse((pat$prona3==1)*(pat$prona_imp==1), 1, 0)
table(pat$fit)
## REVOIR- le modèle n'est pas suffisamment robuste
## 0.25 est totalement arbitraire mais permet de retrouver la proportion de menage détenteur de biens prof tel que def par profna3
## dans base ERF prédire 
erf$prona_imp <- predict(regprof, newdata=erf, type="response")
erf$biensprof[erf$prona_imp < 0.25] <- 0
erf$biensprof[erf$prona_imp >= 0.25] <- 1
table(erf$biensprof)

##########################################################################################################################
###########################################################################################################################
### IMPUTATION DU PATRIMOINE FINANCIER en HOTDECK 
## IMPUTER PATFI DANS ERF

# model_fi <- lm(patfi_new ~ sexepr + agepr + I(agepr**2) + diplopr + occuppr + occupcj + logrminter + typmen + tu99, data=pat)
# summary(model)

modellog_fi <-lm(logpatfi_new ~ sexepr + agepr +I(agepr**2) + diplopr + occuppr + occupcj + logrminterdeb + typmen + tu99, data=pat)
summary(modellog_fi)


pat$patfi_predictedlog <- predict(modellog_fi, newdata=pat)

## en LOG 
## 1ere stratégie
erf$patfi_predictedlog <- predict(modellog_fi, newdata=erf)
pat$residusfi <- pat$logpatfi_new - pat$patfi_predictedlog
## ei = logPi - logPipredi
allvars <- c("occuppr", "agepr","occupcj","diplopr","logrminterdeb", "sexepr", "typmen", "tu99")
classes <-  c("typmen", "occuppr")
#matching variables
matchvars <- setdiff(allvars, classes)
gc()

begin.out.nnd <- NND.hotdeck(data.rec=erf,data.don= pat,match.vars=matchvars, don.class=classes, gdist.fun="Gower")
#begin.out.nnd <- NND.hotdeck(data.rec=erf,data.don= pat,match.vars=matchvars, don.class=classes, gdist.fun="Gower", constrained= TRUE, constr.alg= "relax")
#begin.out.nnd <- RANDwNND.hotdeck(data.rec=erf,data.don=pat, weight.don= pat$pond, match.vars=matchvars, don.class=classes, gdist.fun="Gower")

erf <- create.fused(data.rec=erf, data.don=pat ,mtc.ids=begin.out.nnd$mtc.ids, z.vars="residusfi")
rm(matchvars)
summary(erf$patfi_predictedlog)
erf$logpatfi <- erf$patfi_predictedlog + erf$residusfi
## ET PASSAGE EN EXPONENTIELLE POUR AVOIR LA VALEUR DU PATRIMOINE
erf$patfi <- exp(erf$logpatfi)

## Pour ne pas fausser, on effectue les mêmes étapes sur la base pat- pat_prédit+ res
allvars <- c("occuppr", "agepr","occupcj","diplopr","logrminterdeb", "sexepr", "typmen", "tu99")
classes <- c("typmen", "occuppr") 
#matching variables
matchvars <- setdiff(allvars, classes)
gc()
out.nnd <- NND.hotdeck(data.rec=pat,data.don= pat,match.vars=matchvars, don.class= classes, gdist.fun="Gower")
#out.nnd <- NND.hotdeck(data.rec=pat,data.don= pat,match.vars=matchvars, don.class= classes, gdist.fun="Gower", constrained=TRUE, constr.alg= "relax")
#out.nnd <- RANDwNND.hotdeck(data.rec=pat,data.don= pat, weight.don= pat$pond, match.vars=matchvars, don.class= classes, gdist.fun="Gower")

## TODO essayer en random hotdeck
pat <- create.fused(data.rec=pat, data.don=pat ,mtc.ids=out.nnd$mtc.ids, z.vars="residusfi")
rm(matchvars)
pat$imputed <- pat$patfi_predictedlog + pat$residusfi
## ET PASSAGE EN EXPONENTIELLE POUR AVOIR LA VALEUR DU PATRIMOINE
describe(pat$imputed)
pat$patfi_imputed <- exp(pat$imputed)
pat$imputed <- NULL 

############### OBSERVATIONS DES RESULTATS #################################
# categorize le patrimoine imputé dans la base ERF#
cats = c('01', '02','03','04','05','06','07','08','09','10','11','12')
bins = c( 0,3000,7500,15000,30000,45000,75000,105000,150000,225000,300000,450000,5000000)
erf$patfi_cat <- categorize(erf$patfi, seuil=bins, categories=cats )
pat$patfi_cat <- categorize(pat$patfi_imputed, seuil=bins, categories=cats )

describe(erf$patfi)
describe(pat$patfi, weights=pat$pond)
describe(erf$patfi_cat, weights=erf$wprm)
describe(pat$patfi_cat,weights=pat$pond)

### HISTOGRAMME DES PATRIMOINES FINANCIERS DANS LES DEUX BASES

data1 <- data.frame(cat=pat$patfi, w=pat$pond, source="patrimoine")
data2 <- data.frame(cat=erf$patfi_cat, w=erf$wprm, source="erf")
data_plot <- rbind(data1,data2)
p <- ggplot(data_plot)
p + geom_bar(aes(x=cat, weight=w, fill=source), position="dodge") 

# prepare for merging with menagem
patrimf <- data.frame(ident = erf$ident, patfi=erf$patfi, biensprof= erf$biensprof)
load(menm)
menagem <- merge(menagem, patrimf, by="ident",all.x = TRUE)
save(menagem,file=menm)
rm(patrimf,menagem)  


