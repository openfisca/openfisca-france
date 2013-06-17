
## Imputation des loyers proprement dite 
## -------------------------------------

rm(list = ls())
gc()
RVersion =R.Version()
if (RVersion$os != "linux-gnu") {
  setwd("C:/Users/Utilisateur/Dropbox/python_project/mSim/R")
} else {
  setwd("/home/benjello/Dropbox/python_project/mSim/R")}
rm(RVersion)

library(Hmisc)
library(reshape)

# Execute 02_imput_loyer.R
# Execute 03_fip.R
# Execute 04_famille.R
# Execute 05_decl_imput.R

source('00_config.R')
message("Compute imputed rents");
library(StatMatch) # loads StatMatch
# library(mice) use md.pattern to locate missing data
library(ggplot2)

## Some useful functions
match_rent <- function(erf, logt, var, allvars, classes){
  #matching variables
  matchvars <- setdiff(allvars,classes)  
  out.nnd <- NND.hotdeck(data.rec=erf, data.don=logt, 
                         match.vars=matchvars, 
                         don.class=classes,
                         gdist.fun="Gower")
  fill.erf.nnd <- create.fused(data.rec=erf, data.don=logt,mtc.ids=out.nnd$mtc.ids, z.vars=var)  
  return(fill.erf.nnd)
}

compare_ecdf <- function(erf, logt, var){
  var_erf <- erf[,var]
  w_erf <-   erf[,"wprm"]
  erfCDF  <- wtd.Ecdf(var_erf, weights=w_erf)
  erfCDF_data <- data.frame(x=erfCDF$x,cdf=erfCDF$ecdf,survey="erf")
  var_logt <- logt[,var]
  w_logt <-  logt[,"wprm"] 
  logtCDF <- wtd.Ecdf(var_logt,weights=w_logt)
  logtCDF_data <- data.frame(x=logtCDF$x,cdf=logtCDF$ecdf,survey="logt")
  plot_data <- data.frame(rbind(erfCDF_data,logtCDF_data))
  graph <- ggplot(plot_data, aes(x=x,y=cdf, color=survey)) + geom_point()
  describe( var_erf, weights=w_erf)
  describe(var_logt, weights=w_logt)
  return(graph)
}

## preparing data
loadTmp("erf.Rdata");
loadTmp("logement.Rdata");
logt <- subset(logement,select=c(lmlm,logt , hnph2 , iaat , mdiplo , mtybd , tu99_recoded , magtr , mcs8 , deci, ident));
logt$wprm <- logement$qex;
rm(logement);
gc();
erf <- subset(erf,select=c( logt , hnph2 , iaat , mdiplo , mtybd , tu99_recoded , magtr , mcs8 , deci, wprm, ident));


erf<-na.omit(erf)
logt <- na.omit(logt)
## TODO
## Variables are:
##   hnph2       : number of rooms
##   iaat        :   
##   mdiplo      :
##  mtybd        : type de famille
##  tu99_recoded : tranche d'unit? urbaine recod?e
##  mcs8         :
##  deci         : decile of "niveau de vie"

logt <- within(logt, {
  hnph2 <- as.ordered(as.numeric(hnph2))
  deci  <- as.ordered(as.numeric(deci))
  })

erf <- within(erf, {
  hnph2 <- as.ordered(as.numeric(hnph2))
  deci  <- as.ordered(as.numeric(deci))
})
## regression

logt$loglmlm <- log(logt$lmlm)
log_model <- lm(loglmlm ~  logt + hnph2 + iaat + mdiplo + mtybd + tu99_recoded + magtr + mcs8 + deci, data = logt)
linear_model <- lm(lmlm ~  logt + hnph2 + iaat + mdiplo + mtybd + tu99_recoded + magtr + mcs8 + deci, data = logt)

library(MASS)
lambda <- boxcox(linear_model)
lambda.opt <- lambda$x[which.max(lambda$y)]
print(lambda.opt)
library(car)
lambda <- (powerTransform(linear_model,family="bcPower"))$lambda

logt$bclmlm <- (logt$lmlm**lambda-1)/lambda
bc_model <- lm(bclmlm ~  logt + hnph2 + iaat + mdiplo + mtybd + tu99_recoded + magtr + mcs8 + deci, data = logt)
# summary(bc_model)
# plot(bc_model)

crPlots(bc_model)
sig <- summary(log_model)$sigma


## Robust standard errors
library(lmtest)
library(sandwich)
coeftest(log_model, vcov= vcovHC(log_model, method="white2", type="HC1"))

logt$loglmlm_pred = predict(log_model, newdata=logt)
erf$loglmlm_pred = predict(log_model, newdata=erf)

logt$bclmlm_pred = predict(bc_model, newdata=logt)
erf$bclmlm_pred = predict(bc_model, newdata=erf)


## Correcting for convexity for log
logt$lmlm_pred = exp(logt$loglmlm_pred + (sig**2)/2) 
logt$res = logt$lmlm-logt$loglmlm_pred
erf$lmlm_pred = exp(erf$loglmlm_pred + (sig**2)/2)

logt$log_res = logt$loglmlm - logt$loglmlm_pred

## 
logt$lmlm_bc_pred = (1 + lambda*logt$bclmlm)**(1/lambda)
logt$bc_res = logt$bclmlm-logt$bclmlm_pred

## Variables
allvars <- c("logt", "hnph2", "iaat", "mdiplo", "mtybd", "tu99_recoded", "magtr", "mcs8", "deci");
#donation classes
classes <- c("tu99_recoded","deci","iaat");
#matching variables
matchvars <- setdiff(allvars,classes);

## TODO: try RANDwNND.hotdeck


res_fill.erf.nnd <- match_rent(erf,logt, "res", allvars, classes)
res_fill.erf.nnd$lmlm <- res_fill.erf.nnd$lmlm_pred + res_fill.erf.nnd$res

log_res_fill.erf.nnd <- match_rent(erf,logt, "log_res", allvars, classes)

bc_res_fill.erf.nnd <-  match_rent(erf,logt, "bc_res", allvars, classes) 
bc_res_fill.erf.nnd$lmlm <- (1 + lambda*(bc_res_fill.erf.nnd$bclmlm_pred + bc_res_fill.erf.nnd$bc_res))**(1/lambda)


# Comparison of rents by boxcox
g <- compare_ecdf(bc_res_fill.erf.nnd,logt,"lmlm")
g + scale_x_log10()



## CDF of rents 
g <- compare_ecdf(res_fill.erf.nnd,logt,"lmlm")
g + scale_x_log10()

## CDF of rents log res
g <- compare_ecdf(log_res_fill.erf.nnd,logt,"log_res")
g + scale_x_log10()



rm(allvars,matchvars,classes);



allvars <- c("logt", "hnph2", "iaat", "mdiplo", "mtybd", "tu99_recoded", "magtr", "mcs8", "deci");
#donation classes
classes <- c("tu99_recoded","iaat"); # 


bc_impute_rents <- function(imputed, ref, allvars, classes){
  require(car)
  require(MASS)  
  # use formula
  linear_model <- lm(lmlm ~  logt + hnph2 + iaat + mdiplo + mtybd + tu99_recoded + magtr + mcs8 + deci, data = ref)
  lambda <- boxcox(linear_model)
  lambda.opt <- lambda$x[which.max(lambda$y)]
  lambda <- (powerTransform(linear_model,family="bcPower"))$lambda
  logt$bclmlm <- (logt$lmlm**lambda-1)/lambda
  bc_model <- lm(bclmlm ~  logt + hnph2 + iaat + mdiplo + mtybd + tu99_recoded + magtr + mcs8 + deci, data = ref)
  
  ref$bclmlm_pred = predict(bc_model, newdata=ref)
  imputed$bclmlm_pred = predict(bc_model, newdata=imputed)
  
  ref$lmlm_bc_pred = (1 + lambda*ref$bclmlm)**(1/lambda)
  ref$bc_res = ref$bclmlm-ref$bclmlm_pred
    
  bc_res_fill.erf.nnd <-  match_rent(imputed, ref, "bc_res", allvars, classes) 
  bc_res_fill.erf.nnd$lmlm <- (1 + lambda*(bc_res_fill.erf.nnd$bclmlm_pred + bc_res_fill.erf.nnd$bc_res))**(1/lambda)
  return(bc_res_fill.erf.nnd)
  }


set.seed(432)
logt$id <- 1:nrow(logt)
s <- logt[sample(nrow(logt), round(nrow(logt)/2)),]
ref <- logt[!(logt$id %in%  unique(s$id)),]
imputed <- bc_impute_rents(s, ref, allvars, classes)

compare_results(imputed, logt)

compare_results  <- function(imputed, reference){
  imp    <- data.frame(id=as.integer(imputed$id), x=imputed$lmlm) 
  ref    <- data.frame( x0=reference$lmlm, id=as.integer(reference$id))
  errors <- merge(imp,ref, by="id" )
  errors$rel <- errors$x-errors$x0
  errors$relpct <-  errors$rel/errors$x0
  errors$abs <- abs(errors$x-errors$x0)
  errors$abspct <-  errors$abs/errors$x0
  describe(errors[,c("rel","relpct","abs","abspct")])
}


# TODO: add md.pattern
erf1 <- na.omit(erf);
logt <- na.omit(logt);
rm(erf);
gc();

allvars <- c("logt", "hnph2", "iaat", "mdiplo", "mtybd", "tu99_recoded", "magtr", "mcs8", "deci");
#donation classes
classes <- c("magtr","tu99_recoded");

fill.erf.nnd <- match_rent(erf1,logt, "lmlm", allvars, classes)

## Check

describe(fill.erf.nnd$lmlm,weights=fill.erf.nnd$wprm);
describe(logt$lmlm,weights=logt$wprm);

erfCDF  <- wtd.Ecdf(fill.erf.nnd$lmlm,weights=fill.erf.nnd$wprm);
logtCDF <- wtd.Ecdf(logt$lmlm,weights=logt$wprm);
plot(erfCDF$x,erfCDF$ecdf,col=2);
lines(logtCDF$x,logtCDF$ecdf,col=3);


rm(logt,erf1);
gc();
fill.erf.nnd <- upData(fill.erf.nnd, rename=c(lmlm='loym'));


loy_imput = fill.erf.nnd[c('ident','loym')]
rm(fill.erf.nnd);
load(menm)
menagem$loym <- NULL
menagem <- merge(menagem,loy_imput,by='ident',all.x = TRUE)

save(menagem,file=menm);
rm(loy_imput,menagem);


# Cleaning temporary files
#delTmp()
##Ends here



