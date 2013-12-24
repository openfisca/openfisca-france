# Openfisca
# Rent imputation for renters from regression on 'enquête logement'
# Adds a variable 'loym' to the 'menagem' table

message('Entering 02_imput_loyer')
message('Building comparable tables')
## Variable used for imputation
if (yr == '08'){ # tau99 is not present
  menmVars <- c("ztsam","zperm","zragm","zricm","zrncm","zracm","nb_uci","wprm",
                "so","nbpiec","typmen5","spr","nbenfc","agpr","cstotpr","nat28pr","tu99","aai1",'ident',"pol99","reg")
} else {
  menmVars <- c("ztsam","zperm","zragm","zricm","zrncm","zracm","nb_uci","wprm",
              "so","nbpiec","typmen5","spr","nbenfc","agpr","cstotpr","nat28pr","tu99","aai1",'ident',"pol99","reg","tau99")
}
indmVars <- c("noi",'ident',"lpr","dip11") # TODO check as.numeric
lgtAdrVars <- c("gzc2")
lgtMenVars <- c("sec1","mrcho","mrret","mrsal","mrtns","mdiplo","mtybd","magtr","mcs8","maa1at","qex","muc1")
if (yr=="03"){
lgtMenVars <- c(lgtMenVars,"typse","lmlm","hnph2","mnatior","ident")
lgtAdrVars <- c(lgtAdrVars,"iaat","tu99","ident")
}
if (yr %in% c("06", "07", "08", "09")){
lgtMenVars <- c(lgtMenVars,"mnatio","idlog")
lgtAdrVars <- c(lgtAdrVars,"idlog")  # pas de typse en 2006
lgtLgtVars <- c("lmlm","iaat","tu99","hnph2","idlog")  # pas de typse en 2006
}

## Travail sur la base ERF
## -----------------------
# Table menage
message("preparing erf menage table")
menmVars
erfmenm <- LoadIn(menm, menmVars)
erfmenm <- within(erfmenm,{
  revtot <- ztsam+zperm+zragm+zricm+zrncm+zracm
  nvpr <- revtot/nb_uci
  logt <- as.factor(so)
  })
  # Table individu
message("preparing erf individu table")
erfindm <- LoadIn(eecIndFil, indmVars)
erfindm <- subset(erfindm,lpr==1,select=c(ident,dip11))

# Merge
message("merging erf menage and individu")
erf <- merge(erfmenm, erfindm, by ="ident")
rm(erfmenm,erfindm)

message("compute quantiles")
dec <- wtd.quantile(erf$nvpr,weights=erf$wprm,probs=c(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1))
erf$deci <-  as.factor((1 + (erf$nvpr>=dec[2]) + (erf$nvpr>=dec[3])
                         + (erf$nvpr>=dec[4]) + (erf$nvpr>=dec[5])
                         + (erf$nvpr>=dec[6]) + (erf$nvpr>=dec[7])
                         + (erf$nvpr>=dec[8]) + (erf$nvpr>=dec[9])
                         + (erf$nvpr>=dec[10])))

rm(dec)

message("recode variable for imputation")
erf <- subset(erf, so %in% c(3,4,5),
               select=c(ident,ztsam,zperm,zragm,zricm,zrncm,zracm,
                 nb_uci,logt,nbpiec,typmen5,spr,nbenfc,agpr,cstotpr,
                 nat28pr,tu99,aai1,wprm,nvpr,revtot,dip11,deci))

erf <- upData(erf, rename=c(nbpiec='hnph2',nat28pr='mnatio',aai1='iaat',
                     dip11='mdiplo'))

erf$agpr <- as.integer(erf$agpr)

erf$tmp <- 3

erf$tmp[erf$agpr < 65] <- 2
erf$tmp[erf$agpr < 40] <- 1
erf$magtr <- as.factor(erf$tmp)

erf$mcs8 <- floor(as.integer(erf$cstotpr)/10)
erf$mcs8[erf$mcs8==0] <- NA  # un mcs8=0 est transform? en NA : il y en a donc 1+4 NA's

erf$mtybd <- NA
erf$mtybd[(erf$typmen5==1) & (erf$spr!=2)] <- 1
erf$mtybd[(erf$typmen5==1) & (erf$spr==2)] <- 2
erf$mtybd[erf$typmen5==5]          <- 3
erf$mtybd[erf$typmen5==3]          <- 7
erf$mtybd[erf$nbenfc ==1]          <- 4
erf$mtybd[erf$nbenfc ==2]          <- 5
erf$mtybd[erf$nbenfc >=3]          <- 6
erf$mtybd <- as.factor(erf$mtybd)  # TODO il reste 41 NA's 2003
  
erf$hnph2[erf$hnph2 < 1] <- 1 # 3 logements ont 0 pi?ces !!
erf$hnph2[erf$hnph2 >=6] <- 6  
# table(erf$hnph2, useNA="ifany")
# TODO: il reste un NA 2003
#       il rest un NA en 2008    
erf$hnph2 <- as.factor(erf$hnph2)
tmp <- erf$mnatio
tmp[erf$mnatio %in% c(10)] <- 1
tmp[erf$mnatio %in% c(11,12,13,14,15,21,22,23,24,25,26,27,28,29,31,32,41,42,43,44,45,46,47,48,51,52,62,60)] <- 2  
erf$mnatio <- as.factor(tmp)

tmp <- erf$iaat
tmp[erf$iaat %in% c(1,2,3)] <- 1
tmp[erf$iaat %in% c(4)] <- 2
tmp[erf$iaat %in% c(5)] <- 3
tmp[erf$iaat %in% c(6)] <- 4
tmp[erf$iaat %in% c(7)] <- 5
tmp[erf$iaat %in% c(8)] <- 6
# TODO: comparer logement et erf pour ?tre sur que cela colle
# Il reste un NA en 2003
#    reste un NA en 2008
erf$iaat <- as.factor(tmp)
table(erf$iaat, useNA="ifany")  

tmp <- erf$mdiplo
tmp[erf$mdiplo %in% c(71,"") ]      <- 1
tmp[erf$mdiplo %in% c(70,60,50)]    <- 2
tmp[erf$mdiplo %in% c(41,42,31,33)] <- 3
tmp[erf$mdiplo %in% c(10,11,30)]    <- 4
erf$mdiplo <- as.factor(tmp)

tmp <- erf$tu99   # erf$tu99 is coded from 0 to 8 
tmp[erf$tu99 %in% c(0)] <- 1
tmp[erf$tu99 %in% c(1,2,3)] <- 2
tmp[erf$tu99 %in% c(4,5,6)] <- 3
tmp[erf$tu99 %in% c(7)] <- 4
tmp[erf$tu99 %in% c(8)] <- 5
erf$tu99_recoded <- as.factor(tmp)

tmp <- erf$mcs8
tmp[erf$mcs8 %in% c(1)] <- 1  # TODO 0 ? rajouter 2003 ! 
tmp[erf$mcs8 %in% c(2)] <- 2
tmp[erf$mcs8 %in% c(3)] <- 3
tmp[erf$mcs8 %in% c(4,8)] <- 4
tmp[erf$mcs8 %in% c(5,6,7)] <- 5
erf$mcs8 <- as.factor(tmp)

erf$wprm  <- as.integer(erf$wprm)


erf <- upData(erf, drop=c('cstotpr','agpr','typmen5','nbenfc','spr','tmp','tu99'))

# remove empty levels
erf <- within(erf,{
  logt <- logt[,drop=TRUE]
  magtr <-magtr[,drop=TRUE]
  mcs8 <-mcs8[,drop = TRUE]
  mtybd <-mtybd[,drop = TRUE]
  hnph2 <-hnph2[,drop = TRUE]
  mnatio <-mnatio[,drop = TRUE]
  iaat <-iaat[,drop = TRUE]
  mdiplo <- mdiplo[,drop = TRUE]
  tu99_recoded <-tu99_recoded[,drop = TRUE]
  mcs8 <- mcs8[,drop = TRUE]
})
saveTmp(erf, file = "erf.Rdata")

rm(erf)

## Travail sur la base logement 
## ----------------------------

## Table menage

# 
if (year=="2003"){
  year_lgt = "2003"}

if (year %in% c("2006","2007","2008","2009")){
  year_lgt = "2006"}

message("preparing logement menage table")
lgtmen <- LoadIn(lgtMenFil,lgtMenVars)
lgtmen <- upData(lgtmen, rename=renameidlgt)
lgtmen <- within(lgtmen,{
  mrcho[is.na(mrcho)] <- 0
  mrret[is.na(mrret)] <- 0
  mrsal[is.na(mrsal)] <- 0
  mrtns[is.na(mrtns)] <- 0

  revtot <- mrcho+mrret+mrsal+mrtns # virer les revenus n?gatifs ?
  nvpr   <- (10.0)*revtot/muc1
})
dec <- wtd.quantile(lgtmen$nvpr,weights=lgtmen$qex,probs=c(0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1))
lgtmen <- within(lgtmen,{
  deci <-  as.factor(1 + (nvpr>=dec[2]) 
              + (nvpr>=dec[3])
              + (nvpr>=dec[4]) 
              + (nvpr>=dec[5])
              + (nvpr>=dec[6]) 
              + (nvpr>=dec[7])
              + (nvpr>=dec[8]) 
              + (nvpr>=dec[9])
              + (nvpr>=dec[10]))
})


##Table logement (pas en 2003 mais en 2006) 
str(lgtmen)
if (year_lgt=="2006"){
  message("preparing logement logement table")
  lgtlgt <- LoadIn(lgtLgtFil,lgtLgtVars)
  lgtlgt <- upData(lgtlgt, rename=renameidlgt)
  lgtmen <- merge(lgtmen, lgtlgt, by.x="ident", by.y="ident")
  rm(lgtlgt)
}

data <- subset(lgtmen,sec1==21 | sec1==22|
               sec1==23 | sec1==24 | sec1==30)
rm(lgtmen)
## Conversion etc
data <- within(data,{
  mdiplo  <- as.factor(mdiplo)
  mtybd   <- as.factor(mtybd)
  magtr   <- as.factor(magtr)
  mcs8    <- as.factor(mcs8)
  maa1at  <- as.factor(maa1at)

  # trucs sales pour les cas partiucliers
  if (exists("typse")){     # existe en 2002 pas en 2006
    data$typse   <- as.factor(typse)
  }
})


if (year_lgt=="2006"){     # existe en 2006 pas en 2002
  data <- upData(data, rename=c(mnatio="mnatior"))
}

data <- within(data,{
  mnatior <- as.factor(mnatior)
  mnatior <- mnatior[,drop = TRUE]
  sec1    <- as.factor(sec1)
  sec1    <- sec1[,drop = TRUE]
  
  tmp <- as.character(sec1)
  tmp[sec1 %in% c(21,22,23)] <- 3
  tmp[sec1 %in% c(24)]           <- 4
  tmp[sec1 %in% c(30)]           <- 5
  logt <- as.factor(tmp)
  logt    <- logt[,drop = TRUE]
})

lgtmen <- data
saveTmp(lgtmen,file="lgtmen.Rdata")
rm(lgtmen,data)


## Table adresse
message("preparing logement adresse table")
lgtadr <- LoadIn(lgtAdrFil,lgtAdrVars)
lgtadr <- upData(lgtadr, rename=renameidlgt)

saveTmp(lgtadr,file="lgtadr.Rdata")
rm(lgtadr)

## Merge et cr?ation de nouvelles variables
message("merging logement adresse and menage table")

loadTmp("lgtmen.Rdata")
loadTmp("lgtadr.Rdata")
logement <- merge(lgtmen, lgtadr, by = "ident")
rm(lgtadr,lgtmen)
saveTmp(logement,file="logement.Rdata")

# Cr?ation de nouvelles variables par traitement 
loadTmp("logement.Rdata")
logement <- within(logement,{
  hnph2[hnph2 >=6] <- 6
  hnph2[hnph2 < 1] <- 1
  hnph2 <- as.factor(hnph2)
  hnph2 <- hnph2[,drop = TRUE]

  tmp <- mnatior
  tmp[mnatior %in% c(00,01)] <- 1
  tmp[mnatior %in% c(02,03,04,05,06,07,08,09,10,11)] <- 2
  mnatior <- as.factor(tmp)

  tmp <- iaat
  tmp[iaat %in% c(1,2,3,4,5)] <- 1
  tmp[iaat %in% c(6)] <- 2
  tmp[iaat %in% c(7)] <- 3
  tmp[iaat %in% c(8)] <- 4
  tmp[iaat %in% c(9)] <- 5
  tmp[iaat %in% c(10)]<- 6
# TODO question Cl?ment et le 9 et le 10 ?
  iaat <- as.factor(tmp)

  tmp <- mdiplo
  tmp[mdiplo %in% c(1)] <- 1
  tmp[mdiplo %in% c(2,3,4)] <- 2
  tmp[mdiplo %in% c(5,6,7,8)] <- 3
  tmp[mdiplo %in% c(9)] <- 4
  mdiplo <- as.factor(tmp)

  tmp <- as.numeric(as.character(mtybd))
  tmp[mtybd %in% c(110)] <- 1
  tmp[mtybd %in% c(120)] <- 2
  tmp[mtybd %in% c(200)] <- 3
  tmp[mtybd %in% c(311,321,401)] <- 4
  tmp[mtybd %in% c(312,322,402)] <- 5
  tmp[mtybd %in% c(313,323,403)] <- 6
  tmp[mtybd %in% c(400)] <- 7
  mtybd <- as.factor(tmp)

  tmp <- as.numeric(as.character(tu99)) # tu99 is coded on 8 levels
  tmp[tu99 %in% c(0)] <- 1
  tmp[tu99 %in% c(1,2,3)] <- 2
  tmp[tu99 %in% c(4,5,6)] <- 3
  tmp[tu99 %in% c(7)] <- 4
  tmp[tu99 %in% c(8)] <- 5
  tu99_recoded <- as.factor(tmp)

  tmp <- gzc2
  tmp[gzc2 %in% c(1)] <- 1
  tmp[gzc2 %in% c(2,3,4,5,6)] <- 2
  tmp[gzc2 %in% c(7)] <- 3
  gzc2 <- as.factor(tmp)

  tmp <- magtr
  tmp[magtr %in% c(1,2)] <- 1
  tmp[magtr %in% c(3,4)] <- 2
  tmp[magtr %in% c(5)] <- 3
  magtr <- as.factor(tmp)

  tmp <- mcs8
  tmp[mcs8 %in% c(1)] <- 1
  tmp[mcs8 %in% c(2)] <- 2
  tmp[mcs8 %in% c(3)] <- 3
  tmp[mcs8 %in% c(4,8)] <- 4
  tmp[mcs8 %in% c(5,6,7)] <- 5
  mcs8 <- as.factor(tmp)

  logloy <- log(lmlm)

  mdiplo  <- mdiplo[,drop = TRUE]
  mtybd   <- mtybd[,drop = TRUE]
  magtr   <- magtr[,drop = TRUE]
  mcs8    <- mcs8[,drop = TRUE]
  maa1at  <- maa1at[,drop = TRUE]

})
saveTmp(logement,file="logement.Rdata")
rm(logement)


## Imputation des loyers proprement dite 
## -------------------------------------

message("Compute imputed rents")
library(StatMatch) # loads StatMatch
# library(mice) use md.pattern to locate missing data

loadTmp("erf.Rdata")
loadTmp("logement.Rdata")

logt <- subset(logement,select=c(lmlm,logt , hnph2 , iaat , mdiplo , mtybd , tu99_recoded , magtr , mcs8 , deci, ident))
logt$wprm <- logement$qex
rm(logement)
gc()

erf <- subset(erf,select=c( logt , hnph2 , iaat , mdiplo , mtybd , tu99_recoded , magtr , mcs8 , deci, wprm, ident))

# debug
# derf  <- describe(erf, weights=as.numeric(erf$wprm))
# dlogt <- describe(logt, weights=logt$wprm)   
# 
# for (var in as.list(names(derf))){
#   print("erf")
#   print(derf[[var]]) 
#   print("logt")
#   print(dlogt[[var]]) 
#   print("================")
# }
# rm(var,dlogt,derf)
# gc()

# TODO add md.pattern
erf1 <- na.omit(erf)
logt <- na.omit(logt)
rm(erf)
gc()
allvars <- c("logt", "hnph2", "iaat", "mdiplo", "mtybd", "tu99_recoded", "magtr", "mcs8", "deci")

#donation classes
classes <- c("magtr","tu99_recoded")
#matching variables
matchvars <- setdiff(allvars,classes)
str(erf1)
str(logt)

out.nnd <- NND.hotdeck(data.rec=erf1,data.don=logt,match.vars=matchvars,don.class=classes,gdist.fun="Gower")
fill.erf.nnd <- create.fused(data.rec=erf1, data.don=logt,mtc.ids=out.nnd$mtc.ids, z.vars="lmlm")
rm(allvars,matchvars,classes)

## Check

describe(fill.erf.nnd$lmlm,weights=fill.erf.nnd$wprm)
describe(logt$lmlm,weights=logt$wprm)

erfCDF  <- wtd.Ecdf(fill.erf.nnd$lmlm,weights=fill.erf.nnd$wprm)
logtCDF <- wtd.Ecdf(logt$lmlm,weights=logt$wprm)

#plot(erfCDF$x,erfCDF$ecdf)
#lines(logtCDF$x,logtCDF$ecdf,col=3)

rm(logt,erf1)
gc()
fill.erf.nnd <- upData(fill.erf.nnd, rename=c(lmlm='loym'))


loy_imput = fill.erf.nnd[c('ident','loym')]
rm(fill.erf.nnd, out.nnd)
load(menm)
menagem$loym <- NULL
menagem <- merge(menagem,loy_imput,by='ident',all.x = TRUE)

save(menagem,file=menm)
rm(loy_imput,menagem)

# Cleaning temporary files
#delTmp()
##Ends here

