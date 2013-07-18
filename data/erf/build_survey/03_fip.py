# -*- coding:utf-8 -*-
# OpenFisca

from src.countries.france.data.erf.datatable import DataCollection
from src.countries.france.data.erf.build_survey import show_temp, load_temp, save_temp
from src.countries.france.data.erf.build_survey.utilitaries import control, check_structure
from pandas import DataFrame
from numpy import array, where, NaN
from pandas import concat
import gc

from numpy import logical_not as not_, logical_and as and_


# Some individuals are declared as 'personne à charge' (pac) on 'tax forms' 
# but are not present in the erf or eec tables.
# We add them to ensure consistency between concepts.

def create_fip(year = 2006): # message('03_fip')
    """
    Creates a 'fipDat' table containing all these 'fip individuals'
    """
    
    df = DataCollection(year=year)
    
    print 'Démarrer 03_fip'
# # anaisenf: année de naissance des PAC
# erfFoyVar <- c('anaisenf','declar')
# foyer <- LoadIn(erfFoyFil)
# foyer <- LoadIn(erfFoyFil,erfFoyVar)

    # anaisenf is a string containing letter code of pac (F,G,H,I,J,N,R) and year of birth (example: 'F1990H1992')
    # when a child is invalid, he appears twice in anaisenf (example: F1900G1900 is a single invalid child born in 1990)    
    
    erfFoyVar = ['declar', 'anaisenf']
    foyer = df.get_values(table="foyer", variables=erfFoyVar)
    from src.countries.france.data.erf.build_survey.utilitaries import print_id
    print_id(foyer)
#    control(foyer, verbose=True, verbose_length=10, debug=True)
 
 
# #***********************************************************************************************************
# # print "Step 1 : on recupere les personnes à charge des foyers"
# #**********************************************************************************************************
# # On traite les cas de declarations multiples pour ne pas créer de doublon de pac
# 
# 
# # On récupère toutes les pac des foyers 
# L <- max(nchar(foyer$anaisenf))/5 # nombre de pac maximal
# fip <-data.frame(declar = foyer$declar)
# for (i in c(1:L)){
#   eval(parse(text = paste('fip$typ.',as.character(i),'<- substr(foyer$anaisenf,5*(i-1)+1,5*(i-1)+1)',sep = '')))
#   eval(parse(text = paste('fip$naia.',as.character(i),'<- as.numeric(substr(foyer$anaisenf,5*(i-1)+2,5*(i-1)+5))',sep = '')))
# }
# fip <- fip[!is.na(fip$typ.1),]
# fip <- reshape(fip,direction ='long', varying=2:17, sep=".")
# fip <- fip[!is.na(fip$naia),]
# fip <- fip[order(fip$declar,-rank(fip$typ),fip$naia),c('declar','naia','typ')]
# fip$N <- row(fip)[,1]
# str(fip$N)

    print "Etape 1 : on recupere les personnes à charge des foyers"
    print "    1.1 : Création des codes des enfants"
    foyer['anaisenf'] = foyer['anaisenf'].astype('string')    
    nb_pac_max = len(max(foyer['anaisenf'], key=len))/5
    print "il ya a au maximum %s pac par foyer" %nb_pac_max
    
# Separating the string coding the pac of each "déclaration". 
# Creating a list containing the new variables.
    
    # Creating the multi_index for the columns
    multi_index_columns = []
    for i in range(1,nb_pac_max +1):        
        pac_tuples_list = [(i, 'declaration'), (i, 'type_pac'), (i, 'naia')]
        multi_index_columns += pac_tuples_list 
        
    from pandas import MultiIndex 
    columns= MultiIndex.from_tuples(multi_index_columns, names=['pac_number', 'variable'])    
    from numpy.random import randn
    fip = DataFrame(randn(len(foyer), 3*nb_pac_max),  columns=columns)
    fip.fillna(NaN, inplace=True)
    
    for i in range(1,nb_pac_max+1):
        fip[(i, 'declaration')] = foyer['declar'].values
        fip[(i,'type_pac')] = foyer['anaisenf'].str[5*(i-1)]
        fip[(i,'naia')] = foyer['anaisenf'].str[5*(i-1)+1:5*(i)]
        
    fip = fip.stack("pac_number")
    fip.reset_index(inplace=True)
    del fip["level_0"]

#     print fip.describe()
#     print fip.head().to_string()

    print "    1.2 : elimination des foyers fiscaux sans pac"
    
    #Clearing missing values and changing data format
    fip = fip.sort(columns=['declaration','naia','type_pac'])
    fip.set_index(["declaration","pac_number"], inplace=True)
    # print fip["naia"].value_counts()
    fip = fip[and_(fip['type_pac'].notnull(), (fip['naia'] != 'an') & (fip['naia'] != ''))]
    fip = fip.reset_index()
    del fip['pac_number']

#    control(fip, debug=True, verbose=True, verbose_columns=['naia'])
  

# library(plyr)
# # on enlève les F pour lesquels il y a un G ;
# tyF <- fip[fip$typ == 'F',]
# tyF <- upData(tyF,drop = c('typ'))
# tyG <- fip[fip$typ == 'G',]
# tyG <- upData(tyG,drop = c('N'))
# # There are situations where twins are F and G (ERF2009) !
# tyG['dup'] <- FALSE
# tyG['dup'] <- duplicated(tyG[,c("declar","naia")])
# tyF['dup'] <- FALSE
# tyF['dup'] <- duplicated(tyF[,c("declar","naia")])
# tyFG <- join(tyF,tyG, by = c('declar','naia','dup'),type = 'right',match = 'first')
# iden <- tyFG$N
# rm(tyF,tyG,tyFG)

    print "    1.3 : on enlève les individus F pour lesquels il existe un individu G"

    tyFG = fip[fip.type_pac.isin(['F', 'G'])] #Filtre pour ne travailler que sur F & G
    
    tyFG['same_pair'] = tyFG.duplicated(cols=['declaration', 'naia'], take_last=True)
    tyFG['is_twin'] = tyFG.duplicated(cols=['declaration', 'naia', 'type_pac'])
    tyFG['to_keep'] = (not_(tyFG['same_pair']) | (tyFG['is_twin']))
    #Note : On conserve ceux qui ont des couples déclar/naia différents et les jumeaux 
    #puis on retire les autres (à la fois F et G)
    print len(tyFG),'/', len(tyFG[tyFG['to_keep']])
    print 'longueur fip', len(fip)
    
    fip['to_keep'] = NaN
    fip.update(tyFG)
    print 'enfants F & G traités'
    

    print "    1.4 : on enlève les H pour lesquels il y a un I"
    tyHI = fip[fip.type_pac.isin(['H', 'I'])]
    tyHI['same_pair'] = tyHI.duplicated(cols=['declaration', 'naia'], take_last=True)
    tyHI['is_twin'] = tyHI.duplicated(cols=['declaration', 'naia', 'type_pac'])
    tyHI['to_keep'] = not_(tyHI['same_pair']) | (tyHI['is_twin'])
    
    fip.update(tyHI)
    fip['to_keep'] = fip['to_keep'].fillna(True)
    print 'nb lines to keep/nb initial lines'
    print len(fip[fip['to_keep']]), '/', len(fip)

    indivifip = fip[fip['to_keep']]; del indivifip['to_keep'], fip, tyFG, tyHI

#    control(indivifip, debug=True)



# #************************************************************************************************************/
    print ''
    print 'Step 2 : matching indivifip with eec file'
# #************************************************************************************************************/
# indVar <- c('ident','noi','declar1','declar2','persfip','persfipd','naia','rga','lpr','noindiv','ztsai','ztsao','wprm')
# indivi <- LoadIn(indm,indVar)

#     indvar_erf = ['ident','noi','declar1','declar2','persfip','persfipd', 'noindiv','ztsai',
#                   'ztsao','wprm']
#     indvar_eec = ['ident','noi','naia','rga','lpr', 'noindiv']
#     
#     erf_indivi = df.get_values(variables = indvar_erf, table = 'erf_indivi') #WARNING: Pas de variable naia dans indivi ??
#     eec_indivi = df.get_values(variables = indvar_eec, table = 'eec_indivi') #WARNING: Pas de variable naia dans indivi ??
#     indivi = erf_indivi.merge(eec_indivi, how='outer')

    indivi = load_temp(name="indivim", year=year) #TODO: USE THIS INSTEAD OF PREVIOUS LINES 
#    print list(indivi.columns)
    
# indivi$noidec <- as.numeric(substr(indivi$declar1,1,2))
    indivi['noidec'] = indivi['declar1'].str[0:2].astype('float16') # To be used later to set idfoy

# pac <- indivi[!is.na(indivi$persfip) & indivi$persfip == 'pac',]
# pac$key1 <- paste(pac$naia,pac$declar1)
# pac$key2 <- paste(pac$naia,pac$declar2)
# indivifip$key <- paste(indivifip$naia,indivifip$declar)
    
    pac = indivi[and_(indivi['persfip'] is not NaN, indivi['persfip']=='pac')]
    
    pac['naia'] = pac['naia'].astype('int32') # TODO: was float in pac fix upstream
    indivifip['naia'] = indivifip['naia'].astype('int32') 
    pac['key1'] = zip(pac['naia'], pac['declar1'].str[:29])
    pac['key2'] = zip(pac['naia'], pac['declar2'].str[:29])
    indivifip['key'] = zip(indivifip['naia'], indivifip['declaration'].str[:29])
    assert pac.naia.dtype == indivifip.naia.dtype, 'types %s , %s are different' %(pac.naia.dtype, indivifip.naia.dtype)
    
# fip <- indivifip[!indivifip$key %in% pac$key1,]
# fip <- fip[!fip$key %in% pac$key2,]
    
    fip = indivifip[not_(indivifip.key.isin(pac.key1.values))]
    fip = fip[not_(fip.key.isin(pac.key2.values))]
    
        
    print "    2.1 new fip created"

# We build a dataframe to link the pac to their type and noindiv
# table(duplicated(pac[,c("noindiv")])) 
    countInd = pac.noindiv.value_counts()
    
# pacInd1 <- merge(pac[,c("noindiv","key1","naia")],
#                 indivifip[,c("key","typ")], by.x="key1", by.y="key")
# pacInd2 <- merge(pac[,c("noindiv","key2","naia")],
#                 indivifip[,c("key","typ")], by.x="key2", by.y="key")

    tmp_pac1 = pac.loc[ :, ['noindiv', 'key1']]
    tmp_pac2 = pac.loc[ :, ['noindiv', 'key2']]
    tmp_indivifip = indivifip.loc[ :, ['key', 'type_pac', 'naia']]

    
    pac_ind1 = tmp_pac1.merge(tmp_indivifip, left_on=['key1'], right_on =['key'], how='inner')
    print 'longueur pacInd1' , len(pac_ind1)
    pac_ind2 = tmp_pac2.merge(tmp_indivifip, left_on='key2', right_on = 'key', how='inner')
    print 'longueur pacInd2', len(pac_ind2)

    print "pacInd1&2 créés"
    
# table(duplicated(pacInd1))
# table(duplicated(pacInd2))

    print pac_ind1.duplicated().sum()
    print pac_ind2.duplicated().sum()

# pacInd1 <-rename(pacInd1,c("key1" = "key"))
# pacInd2 <-rename(pacInd2,c("key2" = "key"))
# pacInd <- rbind(pacInd1,pacInd2)
# rm(pacInd1,pacInd2)

#     pacInd1.rename(columns={'key1':'key'}, inplace=True)
#     pacInd2.rename(columns={'key2':'key'}, inplace=True)
    del pac_ind1['key1'], pac_ind2['key2']
    print pac_ind1.columns
    print pac_ind2.columns

    if pac_ind1.index == []:
        if pac_ind2.index == []:
                print "Warning : no link between pac and noindiv for both pacInd1&2"
        else:
            print "Warning : pacInd1 is an empty data frame"
            pacInd = pac_ind2
    elif pac_ind2.index == []:
        print "Warning : pacInd2 is an empty data frame"
        pacInd = pac_ind1
    else:
        pacInd = concat([pac_ind2, pac_ind1]) 
    print len(pac_ind1), len(pac_ind2), len(pacInd)
    print pac_ind2.type_pac.isnull().sum()

    print pacInd.type_pac.value_counts()
    
    print '    2.2 : pacInd created'

# table(duplicated(pacInd[,c("noindiv","typ")]))
# table(duplicated(pacInd$noindiv))

    print 'doublons noindiv, type_pac', pacInd.duplicated(['noindiv', 'type_pac']).sum()
    print 'doublons noindiv seulement', pacInd.duplicated('noindiv').sum()
    print 'nb de NaN', pacInd.type_pac.isnull().sum()
    
    del pacInd["key"]
    pacIndiv = pacInd[not_(pacInd.duplicated('noindiv'))]
#     pacIndiv.reset_index(inplace=True)
    print pacIndiv.columns

    save_temp(pacIndiv, name="pacIndiv", year=year)
    
    print pacIndiv.type_pac.value_counts()
    gc.collect()
    
# # We keep the fip in the menage of their parents because it is used in to
# # build the famille. We should build an individual ident for the fip that are
# # older than 18 since they are not in their parents' menage according to the eec

# individec1 <- subset(indivi, (declar1 %in% fip$declar) & (persfip=="vous"))
# individec1 <- individec1[,c("declar1","noidec","ident","rga","ztsai","ztsao")]
# individec1 <- upData(individec1,rename=c(declar1="declar"))
# fip1       <- merge(fip,individec1)

    individec1 = indivi[and_(indivi.declar1.isin(fip.declaration.values), indivi['persfip']=="vous")]
    individec1 = individec1.loc[:, ["declar1","noidec","ident","rga","ztsai","ztsao"]]
    individec1 = individec1.rename(columns={'declar1':'declaration'})
    fip1 = fip.merge(individec1, on='declaration')
    print '    2.3 : fip1 created'

# # TODO: On ne s'occupe pas des declar2 pour l'instant
# # individec2 <- subset(indivi, (declar2 %in% fip$declar) & (persfip=="vous"))
# # individec2 <- individec2[,c("declar2","noidec","ident","rga","ztsai","ztsao")]
# # individec2 <- upData(individec2,rename=c(declar2="declar"))
# # fip2 <-merge(fip,individec2)

    individec2 = indivi[and_(indivi.declar2.isin(fip.declaration.values), indivi['persfip']=="vous")]
    individec2 = individec2.loc[:, ["declar2","noidec","ident","rga","ztsai","ztsao"]]
    individec2.rename(columns={'declar2':'declaration'}, inplace=True)
    print individec2.head()
    fip2 = fip.merge(individec2)
    print '    2.4 : fip2 created'


    fip1.duplicated().value_counts()
    fip2.duplicated().value_counts()
    
# #fip <- rbind(fip1,fip2)
# fip <- fip1
# table(fip$typ)
    
    fip = concat([fip1, fip2])
#     fip = fip1 #TODO: Pourquoi cette ligne ?
    fip.type_pac.value_counts()
 
    print fip.columns
    fip['persfip'] = 'pac'
    fip['year'] = year
    fip['year'] = fip['year'].astype('float') # BUG; pas de colonne année dans la DF
    fip['noi'] = 99
    fip['noicon'] = None
    fip['noindiv'] = fip['declaration'] 
    fip['noiper'] = None
    fip['noimer'] = None
    fip['declar1'] = fip['declaration'] #TODO declar ?
    fip['naim'] = 99
    fip['lien'] = None
    fip['quelfic'] = 'FIP'
    fip['acteu'] = None
    fip['agepf'] = fip['year'] - fip['naia'].astype('float')
    fip['lpr'] = where(fip['agepf'] <=20, 3, 4) # TODO pas très propre d'après Mahdi/Clément
    fip['stc'] = None
    fip['contra'] = None
    fip['titc'] = None
    fip['mrec'] = None
    fip['forter'] = None
    fip['rstg'] = None
    fip['retrai'] = None
    fip['cohab'] = None
    fip['sexe'] = None
    fip['persfip'] = "pac"
    fip['agepr'] = None
    fip['actrec'] = where(fip['agepf']<=15, 9, 5)
    
## TODO: probleme actrec des enfants fip entre 16 et 20 ans : on ne sait pas s'ils sont étudiants ou salariés */
## TODO problème avec les mois des enfants FIP : voir si on ne peut pas remonter à ces valeurs

# Reassigning noi for fip children if they are more than one per foyer fiscal 
# while ( any(duplicated( fip[,c("noi","ident")]) ) ) {
#   dup <- duplicated( fip[, c("noi","ident")])
#   tmp <- fip[dup,"noi"]
#   fip[dup, "noi"] <- (tmp-1)
# }
    #TODO: Le vecteur dup est-il correct
    fip["noi"] = fip["noi"].astype("int64")
    fip["ident"] = fip["ident"].astype("int64")
    
    fip_tmp = fip.loc[:, ['noi', 'ident']]

    while any(fip.duplicated(cols=['noi', 'ident'])):
        fip_tmp = fip.loc[:, ['noi', 'ident']]
        dup = fip_tmp.duplicated()
        tmp = fip.loc[dup, 'noi']
        print len(tmp)
        fip.loc[dup, 'noi'] = tmp.astype('int64') - 1

    fip['idfoy'] = 100*fip['ident'] + fip['noidec']
    fip['noindiv'] = 100*fip['ident'] + fip['noi']
    fip['type_pac'] = 0 ; fip['key'] = 0
    
    print fip.duplicated('noindiv').value_counts()
    save_temp(fip, name="fipDat", year=year)
    del fip, fip1, individec1, indivifip, indivi, pac
    print 'fip sauvegardé'


if __name__ == '__main__':
    create_fip()