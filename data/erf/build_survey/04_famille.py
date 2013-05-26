# OpenFisca
# Retreives the families 
# Creates 'idfam' and 'quifam' variables

##***********************************************************************/
message('04_famille: construction de la table famille')
##***********************************************************************/

## On suit la méthode décrite dans le Guide ERF_2002_rétropolée page 135

if (year=="2006") {
  smic = 1254
  } else if (year=="2007") {
    smic = 1280    
  } else if (year=="2008") {
     smic = 1308    
  } else if (year=="2009") {
    smic = 1337
  } else {
    message("smic non défini")
  }

indVar = c('noi','noicon','noindiv','noiper','noimer','ident','declar1','naia','naim','lien','quelfic','acteu','stc','contra','titc','mrec',
            'forter','rstg','retrai','lpr','cohab','ztsai','sexe','persfip','agepr','rga','actrec')

# TODO check if we can remove acteu forter etc since dealt with in 01_pre_proc 

indivi <- LoadIn(indm,indVar)


indivi <- within(indivi,{
          year <- as.numeric(year)
          noidec <- as.numeric(substr(declar1,1,2))
          agepf <- ifelse(naim < 7, year-naia ,year-naia-1)
          })

table(indivi$acteu)

##on enlève les enfants en nourrice...*/
indivi2 <- subset(indivi,lien==6 & agepf <  16 & quelfic=='EE','noindiv')
indivi <- indivi[!indivi$noindiv %in% indivi2$noindiv,]
rm(indivi2)


## Enfant à naître (NN pour nouveaux nés)
indVar = c('noi','noicon','noindiv','noiper','noimer','ident','declar1','naia','naim','lien','quelfic','acteu','stc','contra','titc','mrec',
           'forter','rstg','retrai','lpr','cohab','ztsai','sexe','persfip','agepr','rga','actrec',
           "agepf","noidec","year")

enfnn <- LoadIn(enfnnm,indVar)
## Remove duplicated  noindiv because some rga are different
enfnn <- enfnn[!duplicated(enfnn[,"noindiv"]),]
## On enlève les enfants à naitre qui ne sont pas les enfants de la personne de référence
enfnn <- subset(enfnn,lpr==3)
enfnn <- enfnn[(!enfnn$noindiv %in% indivi$noindiv),]

# PB with vars "agepf"  "noidec" "year"  
base <- rbind(indivi,enfnn)
setdiff(names(indivi),names(enfnn))

table(base$quelfic)

dup <- duplicated(base[,c("noindiv")])
#dup <- duplicated(base)
table(dup)

str(base)

base <- within(base,{
  noindiv<- 100*ident + noi
  m15 <- (agepf<16) 
  p16m20 <- ((agepf>=16) & (agepf<=20))
  p21 <- (agepf>=21)
  ztsai[is.na(ztsai)] <- 0
  smic55 <- (ztsai>= smic*12*0.55)   ##55% du smic mensuel brut */
  famille <- 0
  kid <- FALSE})


##******************************************************************************************************************/
message('Etape 1: On cherche les enfants ayant père et/ou mère')
pr <- subset(base,lpr==1,c('ident','noi'))
pr$noifam <- 100*pr$ident + pr$noi
pr <- pr[c('ident','noifam')]

nof01 <- subset(base,(lpr %in% c(1,2) )|(lpr==3 & m15) | (lpr==3 & (p16m20 & !smic55) )) 
nof01 <- merge(pr,nof01,by ='ident')
nof01 <- within(nof01,{
  famille <- 10
  kid <-(lpr==3 & m15) | (lpr==3 & (p16m20 & !smic55 ) )
  })
famille <- nof01
table(famille$famille,useNA='ifany')
rm(nof01)
##******************************************************************************************************************/
message('Etape 2a')
## l'identifiant est le noi de l'homme
## cohab=1  vit en couple
## cohab=2 ou cohab=0 ne vit pas en couple
hcouple <- base[(!base$noindiv %in% famille$noindiv),] 
hcouple <- subset(hcouple,(cohab==1) & (lpr>=3) & (sexe==1))
hcouple <- within(hcouple,{
  noifam=100*ident + noi ## l'identifiant est la personne de référence du ménage  */
	famille = 21 })

message('Etape 2b')
fcouple<- base[!base$noindiv %in% famille$noindiv,]
fcouple <- subset(fcouple,(cohab==1) & (lpr>=3) & (sexe==2))
fcouple <- within(fcouple,{
	noifam <- 100*ident + noicon ## l'identifiant est le conjoint du ménage  */
	famille <- 22 })

famcom<- merge(fcouple['noifam'],hcouple['noifam'])
fcouple <- merge(famcom,fcouple)

famille <- rbind(famille,hcouple,fcouple)
dup <- duplicated(famille$noindiv)
table(dup)
table(famille$famille,useNA='ifany')
rm(hcouple,fcouple,famcom)

##******************************************************************************************************************/
message('Etape 3: personnes seules')
message(' 3.1 personnes seules 1')
seul1 <- base[(!base$noindiv %in% famille$noindiv),] 
seul1 <- subset(seul1,(lpr %in% c(3,4)) & ( (p16m20 & smic55)|p21 ) & (cohab==1) & (sexe==2))
if (nrow(seul1) > 0){
  seul1 <- within(seul1,{noifam <- 100*ident+noi
                       famille <- 31})
  famille <- rbind(famille,seul1)
  dup <- duplicated(famille$noindiv)
  table(dup)
}

message('  3.2 personnes seules 2')
seul2 <- base[(!base$noindiv %in% famille$noindiv),] 
seul2 <- subset(seul2,(lpr %in% c(3,4)) & p16m20 & smic55 & (cohab!=1))
seul2 <- within(seul2,{noifam <- 100*ident+noi
                     famille <- 32})
famille <- rbind(famille,seul2)

message(' 3.3 personnes seules 3')
seul3 <- base[(!base$noindiv %in% famille$noindiv),] 
seul3 <- subset(seul3,(lpr %in% c(3,4)) & p21 & cohab!=1)
	## TODO CHECK erreur dans le guide méthodologique ERF 2002 lpr 3,4 au lieu de 3 seulement */
seul3 <- within(seul3,{noifam=100*ident+noi
	                     famille = 33})
famille <- rbind(famille,seul3)
dup <- duplicated(famille$noindiv)
table(dup)

message(' 3.4 personnes seules 4')
seul4 <- base[(!base$noindiv %in% famille$noindiv),] 
seul4 <- subset(seul4,(lpr==4) & p16m20 & !smic55 & noimer==0 & noiper==0 & persfip=="vous")

if (nrow(seul4) >0 ) {  # 2006, 2009 pas de personne seule (sans enfant fip)
  seul4 <- within(seul4,{noifam = 100*ident + noi
	                     famille = 34})
}

famille <- rbind(famille,seul4)
dup <- duplicated(famille$noindiv)
table(dup)

table(famille$famille,useNA='ifany')
rm(seul1,seul2,seul3,seul4)

##******************************************************************************************************************/
message('Etape 4')  
message(' 4.1 enfant avec mère')
avec_mere <- base[(!base$noindiv %in% famille$noindiv),] 
avec_mere <- subset(avec_mere,((lpr=4) & ( (p16m20=1) | (m15=1))) & noimer!=0)

avec_mere <- within(avec_mere,{noifam=100*ident + noimer
             famille=41
             kid=TRUE})

## on récupère les mères */
mereid <- upData(avec_mere['noifam'], rename = c(noifam = 'noindiv'));
mereid <- unique(mereid)

mere <- merge(mereid,base)
mere <- within(mere,{noifam=100*ident + noi
                     famille=42})
# TODO il y a deux mères qui ne sont pas dans les individus (problème des conjoints fip ? MBJ ne comprends pas) : 
dim(mereid)
dim(mere)
# TODO on préfère  donc enlever leurs enfants
avec_mere <- avec_mere[avec_mere$noifam %in% mere$noifam,]


famille <- famille[(!famille$noindiv %in% mere$noindiv),] 

## on récupère les conjoints des mères */
conj_mereid <- mere[mere$noicon!=0,c('ident','noicon','noifam')]

conj_mereid$noindiv = 100*conj_mereid$ident + conj_mereid$noicon
conj_mereid <- conj_mereid[c('noindiv','noifam')]

conj_mere <- merge(conj_mereid,base)
conj_mere$famille <- 43

famille <- famille[(!famille$noindiv %in% conj_mere$noindiv),] 
famille <- rbind(famille,avec_mere,mere,conj_mere)

dup <- duplicated(famille$noindiv)
table(dup)
table(famille$famille,useNA='ifany')
rm(avec_mere,mere,mereid,conj_mere,conj_mereid)

message(' 4.2 enfants avec père')
avec_pere <- base[(!base$noindiv %in% famille$noindiv),] 
avec_pere <- subset(avec_pere,((lpr=4) & ( (p16m20=1) | (m15=1))) & noiper!=0)
avec_pere <- within(avec_pere,{noifam=100*ident + noiper
             famille=44
             kid=TRUE})

## on récupère les pères  pour leur attribuer une famille propre */
pereid <- upData(avec_pere['noifam'], rename = c(noifam = 'noindiv'));
pereid <- unique(pereid)
pere <- merge(pereid,base)
pere <- within(pere,{noifam=100*ident + noi
                       famille=45})

famille <- famille[(!famille$noindiv %in% pere$noindiv),] 

## on récupère les conjoints des pères */
conj_pereid <- pere[pere$noicon!=0,c('ident','noicon','noifam')]
conj_pereid$noindiv = 100*conj_pereid$ident + conj_pereid$noicon
conj_pereid <- conj_pereid[c('noindiv','noifam')]

conj_pere <- merge(conj_pereid,base)
if (nrow(conj_pere) >0) conj_pere$famille <- 46
# 2006: erreur pas de conjoint de père ?

famille <- famille[(!famille$noindiv %in% conj_pere$noindiv),] 
famille <- rbind(famille,avec_pere,pere,conj_pere)
dup <- duplicated(famille$noindiv)
table(dup)

table(famille$famille,useNA='ifany')
rm(avec_pere,pere,pereid,conj_pere,conj_pereid)

##* 42. enfants avec déclarant */
avec_dec <- base[(!base$noindiv %in% famille$noindiv),] 
avec_dec <- subset(avec_dec,(persfip=="pac") & (lpr=4) &  ( (p16m20&!smic55) | (m15=1 )))
avec_dec <- within(avec_dec,{noifam = 100*ident + noidec
            famille=47
            kid=TRUE})

## on récupère les déclarants pour leur attribuer une famille propre */
decid <- upData(avec_dec['noifam'], rename = c(noifam = 'noindiv'));
decid <- unique(decid)

dec <- merge(decid,base)
dec <- within(dec,{noifam=100*ident + noi
                   famille=48})

famille <- famille[(!famille$noindiv %in% dec$noindiv),] 
famille <- rbind(famille,avec_dec,dec)
dup <- duplicated(famille$noindiv)
table(dup)

table(famille$famille,useNA='ifany')
rm(dec,decid,avec_dec)


##******************************************************************************************************************/
## famille etape 5 : enfants fip */ 
message('Etape 5 : enfants fip')
# On rajoute les enfants fip 
# (on le fait ici pour que cela n'interfère pas avec les recherches précédentes)
fip <- LoadIn(fipDat)

indVar = c('noi','noicon','noindiv','noiper','noimer','ident','declar1','naia','naim','lien','quelfic','acteu','stc','contra','titc','mrec',
            'forter','rstg','retrai','lpr','cohab','ztsai','sexe','persfip','agepr','rga')

fip <- fip[c(indVar,'actrec','agepf','noidec','year')]

table(duplicated(fip$noindiv))

## Variables auxilaires présentes dans base qu'il faut rajouter aux fip'
## WARNING les noindiv des fip sont construits sur les ident des déclarants
## pas d'orvelap possible avec les autres noindiv car on a des noi =99, 98, 97 ,...'
names(fip)

fip <- within(fip,{
  m15 <- (agepf<16) 
  p16m20 <- ((agepf>=16) & (agepf<=20))
  p21 <- (agepf>=21)
  ztsai[is.na(ztsai)] <- 0
  smic55 <- (ztsai >= smic*12*0.55)   ## 55% du smic mensuel brut */
  famille <- 0
  kid <- FALSE
})

dup<-duplicated(fip$noindiv)
table(dup)

base <- rbind(base,fip)
table(base$quelfic)

enfant_fip <- base[(!base$noindiv %in% famille$noindiv),] 
enfant_fip <- subset(enfant_fip, (quelfic=="FIP") & (( (agepf %in% c(19,20)) & !smic55 ) | (naia==year & rga=='6')) )  # TODO check year ou year-1 !

enfant_fip <- within(enfant_fip,{
                     noifam=100*ident+noidec
                     famille=50
                     kid=TRUE})
#                     ident=NA}) # TODO : je ne sais pas quoi mettre un NA fausse les manips suivantes 
famille <- rbind(famille,enfant_fip)

# TODO: En 2006 on peut faire ce qui suit car tous les parents fip sont déjà dans une famille
parent_fip <- famille[famille$noindiv %in% enfant_fip$noifam,]
any(enfant_fip$noifam %in% parent_fip$noindiv)
parent_fip <- within(parent_fip,{
                     noifam <- noindiv
                     famille <- 51
                     kid <- FALSE})
famille[famille$noindiv %in% enfant_fip$noifam,] <- parent_fip
# TODO: quid du conjoint ?
dup <- duplicated(famille$noindiv)
table(dup)

table(famille$famille,useNA='ifany')
rm(enfant_fip,fip,parent_fip)
  
##******************************************************************************************************************/
message('Etape 6 : non attribué')
non_attribue1 <- base[(!base$noindiv %in% famille$noindiv),] 
non_attribue1 <- subset(non_attribue1,
                        (quelfic!="FIP") & (m15 | (p16m20&(lien %in% c(1,2,3,4) & agepr>=35)))
                        )
# On rattache les moins de 15 ans avec la PR (on a déjà éliminé les enfants en nourrice)                         
non_attribue1 <- merge(pr,non_attribue1)
non_attribue1 <- within(non_attribue1,{
  famille <- ifelse(m15,61,62)
	kid <- TRUE })

rm(pr)
famille <- rbind(famille,non_attribue1)
dup <- duplicated(famille$noindiv)
table(dup)
rm(non_attribue1)
table(famille$famille, useNA="ifany")

non_attribue2 <- base[(!base$noindiv %in% famille$noindiv) & (base$quelfic!="FIP"),] 
non_attribue2 <- within(non_attribue2,{
  noifam <- 100*ident+noi # l'identifiant est celui du jeune */
	kid<-FALSE
	famille<-63})

famille <- rbind(famille,non_attribue2)
dup <- duplicated(famille$noindiv)
table(dup)
rm(non_attribue2)
table(famille$famille, useNA="ifany")
rm(base)
table(duplicated(famille$noifam))

##******************************************************************************************************************/
## Sauvegarde de la table famille */  

# TODO nettoyer les champs qui ne servent plus à rien

famille <- within(famille,{
  idec <- paste(substr(declar1,4,11),substr(declar1,1,2),sep = '-') # TODO remove me ?
	chef <- (noifam == ident*100+noi)
})
table(famille$chef,useNA="ifany")
# On a bien autant de famille que de chef de famille 

famille$kid <- as.numeric(famille$kid)

famille <- famille[order(famille$noifam,famille$kid,!famille$chef,famille$naia,famille$naim),]
famille$chef <- as.numeric(famille$chef)

famille$rang = unsplit(lapply(split(famille$kid,famille$noifam),cumsum),famille$noifam)

dup <- duplicated(famille$noindiv)
table(dup)

famille$quifam[famille$chef == 1] <- 0
famille$quifam[(famille$chef == 0) & (famille$kid ==0)] <- 1
famille$quifam[famille$kid == 1] <- 1 + famille$rang[famille$kid == 1]
famille <- subset(famille, select = c(noindiv, quifam, noifam))
famille <- rename(famille, c(noifam = "idfam"))

length(unique(famille$idfam))
table(famille$quifam,useNA="ifany")
sum(table(famille$quifam,useNA="ifany"))

print(length(table(famille$noindiv)))

# Vérifications des duplicats dans famille (même noindiv)
dup <- duplicated(famille[,c("idfam","quifam")])
table(dup,useNA="ifany")

save(famille,file=famc)
rm(famille, indivi, enfnn)
gc()
