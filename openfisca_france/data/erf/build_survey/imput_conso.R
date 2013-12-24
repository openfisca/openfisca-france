rm(list = ls())
tabgc()
RVersion =R.Version()
if (RVersion$os != "linux-gnu") {
  setwd("C:/Users/Utilisateur/Dropbox/python_project/mSim/R")
} else {
  setwd("/home/benjello/Dropbox/python_project/mSim/R")}
rm(RVersion)

# Clean everything
getwd()
#imputation famille - ERF
# Load some useful functions

year <- "2006"
year1 <- "2007"
source("./common.R")
source("./00_config.R")

library(Hmisc)
library(car)
library(reshape)
library(foreign)
library(sas7bdat) 
library(ggplot2)
library(StatMatch)

#step1 import data frame
 #BDFmen06  <- read.dta('menage_imput.dta')   
   
#reecrire en ouvrant directement base R  
BDFind06 <-read.dta("C:/Users/Utilisateur/Documents/Data/R/bdf/2006/individu.dta")
BDFmen06 <-read.dta("C:/Users/Utilisateur/Documents/Data/R/bdf/2006/menage.dta") 
BDFcons06 <- read.dta("C:/Users/Utilisateur/Documents/Data/R/bdf/2006/c05d.dta")
# ERFSmen06 <- read.sas7bdat("menage06.sas7bdat")
# EECmen06 <- read.sas7bdat("mrf06e06t4.sas7bdat")
# EECind06 <- read.sas7bdat("irf06e06t4.sas7bdat")

x <- LoadIn(menm)

'nbenf18' %in% colnames(x)

men_vars <- c('ident', 'zperm', 'zragm', 'zricm', 'ztsam', 'zrncm', 'psocm', 'nb_uci',
              'nbinde', 'typmen5', 'tur5',  'spr',  'agpr', 'cstotpr',  'nat28pr', 'wprm')
men_imp <- LoadIn(menm, men_vars) # TODO: better name

ind_vars <- c('lpr', 'dip11', 'ident')
ind_imp <- LoadIn(indm, ind_vars) # TODO: better name
str(ind_imp)
ind_imp <- subset (ind_imp, lpr==1)
#table(ind_imp$lpr, useNA="ifany")

#step 2 susbset,  var used for imputation
# subs_erfs <- subset(ERFSmen06,select=c( ident06, zperm, ztsam,zragm, zricm, zrncm, psocm, nb_UCI,  nbenfch ))
# subs_eec <- subset(EECmen06,select=c( NBENF18, NBINDE, TYPMEN5, TUR5, SPR, AGPR, CSTOTPR,  NAT28PR, ident06))
# subs_eec_indiv <- subset (EECind06, LPR=="1")
# subs_eec_indiv <- subset (subs_eec_indiv, select=c(DIP11, ident06, SP00) )
subs_BDFcons06<- subset(BDFcons06, select=c(ident_men, c01112))#juste pour tester hot deck
BDFmen06 <- subset(BDFmen06, select=c(ident_log, ident_men, pondmen, nhab, situapr,sexepr, revact, revsoc, ocde10, typmen5, strate, agpr, codcspr,cs24pr,cs42pr, dip14pr,  natio7pr))
BDFind06 <- subset(BDFind06,  lienpref=="00", select=c(ident_men, typemploi, statut))

BDF06_imput <- merge(BDFmen06,BDFind06, by= "ident_men" )
BDF06_imput <- merge(BDF06_imput, subs_BDFcons06, by= "ident_men")
   

## Step 3 BDF06 cleaning data+ building comparable var.
BDF06_imput <-   within(BDF06_imput,{
     
dip14 <-dip14pr
dip14pr <-NULL
dip14[dip14 == "20"] <- "10"
dip14[dip14 == "12"] <- "11"
dip14[dip14 == "43"] <- "42"
dip14[dip14 == "44"] <- "50"
dip11 <- dip14
dip14 <- NULL
dip11 <- as.integer(dip11)

natio7pr[natio7pr=="2"]<-"1"
nat28pr <- natio7pr
natio7pr <- NULL
nat28pr <- as.integer(nat28pr)

nbinde <- nhab
nhab <- NULL

cstotpr <-codcspr
cstotpr [cs24pr == "71"] <- "71"
cstotpr [cs24pr == "72"] <- "72"
cstotpr [cs24pr == "73"] <- "73"
cstotpr [cs24pr == "76"] <- "76"
cstotpr [cs24pr == "81"] <- "81"
cstotpr [cs42pr == "84"] <- "84"
cstotpr [cs42pr == "85"] <- "85"
cstotpr [cs42pr == "86"] <- "86"
cs24pr <- NULL
cs42pr <- NULL
codcspr <-NULL
cstotpr <- as.integer(cstotpr)


tur5 <-strate
strate <- NULL
tur5 <- as.integer(tur5)

spr <-sexepr
sexepr <-NULL
spr <- as.integer(spr)

revtot <- revact+revsoc
revact <- NULL
revsoc <- NULL

typemploipr <-typemploi
typemploi <-NULL    

typmen5 <- as.integer(typmen5)

})
   
#describe(BDF06_imput)   

##Step 4 ERF building comparable var.

#nationality
men_imp <-   within(men_imp,{
nat28pr <- as.character(nat28pr)
nat28pr[nat28pr == "10"] <- "1"
nat28pr[nat28pr == "21"|nat28pr == "22"|nat28pr == "23"
       |nat28pr == "24"|nat28pr == "25"|nat28pr == "26"
       |nat28pr == "27"|nat28pr == "28"|nat28pr == "29"|nat28pr == "47"
       |nat28pr == "31"|nat28pr == "32"|nat28pr == "42"] <- "3"
nat28pr[nat28pr == "43"] <- "4"
nat28pr[nat28pr == "11"|nat28pr == "12"|nat28pr == "13"] <- "5"
nat28pr[nat28pr == "14"] <- "6"
nat28pr[nat28pr == "15"|nat28pr == "41"|nat28pr == "44"|nat28pr == "45"
       |nat28pr == "46"|nat28pr == "48"|nat28pr == "51"|nat28pr == "52"|nat28pr == "60"] <- "7"
nat28pr <- as.integer(nat28pr)
})

# income 
men_imp <- within(men_imp,{
  revtot <-  zperm + ztsam +zragm + zricm + zrncm + psocm
  
cstotpr[cstotpr=="74"|cstotpr=="75"]<- "73"
cstotpr[cstotpr=="77"|cstotpr=="78"]<- "76"
cstotpr[cstotpr=="85"|cstotpr=="86"]<- "82"  
cstotpr[cstotpr=="NA"] <- "0" # pb 3 missings
cstotpr <-as.integer(cstotpr)
  })

# merging ind &  men
tot_imput <- merge (men_imp, ind_imp, by="ident")
str (tot_imput$cstotpr)

#income distribution
#(to do with weights)
#summary(BDF06_imput$revtot)
#g <- ggplot(subset(BDFmen06, revtot<150000), aes(x=revtot) )            
#g+stat_bin(binwidth = 1000) 
 #  erf_imput <- subset(data2,data2$revtot>0)   #on exclut les revenus n?gatifs   
#summary(erf_imput$revtot)
#g <- ggplot(subset(pos_revtot, revtot<150000), aes(x=revtot) )            
#g+stat_bin(binwidth = 1000) 

#income decile
## ! A faire!: Ajouter pond?rations
message("compute quantiles")
#on supprime les revenus negatifs
tot_imput <- subset(tot_imput, revtot>=0)
dec_erf <- wtd.quantile(tot_imput$revtot,weights=tot_imput$wprm,probs=c(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1))
dec_bdf <- wtd.quantile(BDF06_imput$revtot,weights=BDF06_imput$pondmen.x,probs=c(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1))


#decileerf <-  quantile(erf_imput$revtot, probs=seq(0,1,0.10))
#decilebdf <-  quantile(BDF06_imput$revtot, probs=seq(0,1,0.10))                     

dec_bdf<-as.data.frame(dec_bdf)
dec_erf <- as.data.frame(dec_erf)

   BDF06_imput[c("deci")] <- NA 
   BDF06_imput <- within(BDF06_imput,{
    deci[revtot>=dec_bdf[1,1]&revtot<dec_bdf[2,1]] <- "1"
    deci[revtot>=dec_bdf[2,1]&revtot<dec_bdf[3,1]] <- "2"
    deci[revtot>=dec_bdf[3,1]&revtot<dec_bdf[4,1]] <- "3"
    deci[revtot>=dec_bdf[4,1]&revtot<dec_bdf[5,1]] <- "4"
    deci[revtot>=dec_bdf[5,1]&revtot<dec_bdf[6,1]] <- "5"
    deci[revtot>=dec_bdf[6,1]&revtot<dec_bdf[7,1]] <- "6"
    deci[revtot>=dec_bdf[7,1]&revtot<dec_bdf[8,1]] <- "7"
    deci[revtot>=dec_bdf[8,1]&revtot<dec_bdf[9,1]] <- "8"
    deci[revtot>=dec_bdf[9,1]&revtot<dec_bdf[10,1]] <- "9"
    deci[revtot>=dec_bdf[10,1]] <- "10"
    deci <-as.integer(deci)
})

tot_imput[c("deci")] <- NA 
tot_imput <- within(tot_imput,{
  deci[revtot>=dec_erf[1,1]&revtot<dec_erf[2,1]] <- "1"
  deci[revtot>=dec_erf[2,1]&revtot<dec_erf[3,1]] <- "2"
  deci[revtot>=dec_erf[3,1]&revtot<dec_erf[4,1]] <- "3"
  deci[revtot>=dec_erf[4,1]&revtot<dec_erf[5,1]] <- "4"
  deci[revtot>=dec_erf[5,1]&revtot<dec_erf[6,1]] <- "5"
  deci[revtot>=dec_erf[6,1]&revtot<dec_erf[7,1]] <- "6"
  deci[revtot>=dec_erf[7,1]&revtot<dec_erf[8,1]] <- "7"
  deci[revtot>=dec_erf[8,1]&revtot<dec_erf[9,1]] <- "8"
  deci[revtot>=dec_erf[9,1]&revtot<dec_erf[10,1]] <- "9"
  deci[revtot>=dec_erf[10,1]] <- "10"
  deci <-as.integer(deci)
})

##QUESTION: que faire avec les missing?
#vérification des missings
#str(tot_imput)
#describe(tot_imput) #3 missing cstotpr
#describe(BDF06_imput)


## Step 5 imputation
str(BDF06_imput)
allvars <- c("revtot","typmen5", "tur5", "spr","nat28pr", "cstotpr" , "agpr", "deci", "nbinde") 

classes <- c("deci", "typmen5")
matchvars <- setdiff(allvars, classes) 
zvars <- c("c01112")

out.nnd <- NND.hotdeck(data.rec=tot_imput,data.don=BDF06_imput,match.vars=allvars,don.class=classes,dist.fun="Gower")
fill.erf.nnd <- create.fused(data.rec=tot_imput, data.don=BDF06_imput,mtc.ids=out.nnd$mtc.ids, z.vars="c01112")
rm(allvars,matchvars,classes)
   
    
   
   



