# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division
from src.countries.france.model.data import CAT
from numpy import maximum as max_, minimum as min_, logical_not as not_, zeros, ones
from src.core.utils_old import  scaleBaremes, combineBaremes, BaremeDict


                
# TODO: CHECK la csg déductible en 2006 est case GH
# TODO:  la revenus soumis aux csg déductible et imposable sont en CG et BH en 2010 

#        # Heures supplémentaires exonérées
#        if not self.bareme.ir.autre.hsup_exo:
#            self.sal += self.hsup
#            self.hsup = 0*self.hsup
                        
# Exonération de CSG et de CRDS sur les revenus du chômage 
# et des préretraites si cela abaisse ces revenus sous le smic brut        
# TODO: mettre un trigger pour l'éxonération des revenus du chômage sous un smic

# TODO: RAFP assiette + prime
# TODO: pension assiette = salaire hors prime
# autres salaires + primes


# TODO: contribution patronale de prévoyance complémentaire
# Formation professionnelle (entreprise de 10 à moins de 20 salariés) salaire total 1,05%
# Formation professionnelle (entreprise de moins de 10 salariés)      salaire total 0,55%
# Taxe sur les salaries (pour ceux non-assujettis à la TVA)           salaire total 4,25% 
# TODO: accident du travail ?
    
#temp = 0
#if hasattr(P, "prelsoc"):
#    for val in P.prelsoc.__dict__.itervalues(): temp += val
#    P.prelsoc.total = temp         
#else : 
#    P.__dict__.update({"prelsoc": {"total": 0} })
#
#a = {'sal':sal, 'pat':pat, 'csg':csg, 'crds':crds, 'exo_fillon': P.cotsoc.exo_fillon, 'lps': P.lps, 'ir': P.ir, 'prelsoc': P.prelsoc}
#return Dicts2Object(**a)

def _mhsup(hsup):
    """
    Heures supplémentaires comptèes négativement
    """
    return -hsup

############################################################################
## Revenus du capital
############################################################################

# revenus du capital soumis au barème
def _csg_cap_bar(rev_cap_bar, _P):
    '''
    Calcule la CSG sur les revenus du captial soumis au barème
    '''
    return - rev_cap_bar*_P.csg.capital.glob

def _crds_cap_bar(rev_cap_bar, _P):
    '''
    Calcule la CRDS sur les revenus du capital soumis au barème
    '''
    return - rev_cap_bar*_P.crds.capital

def _prelsoc_cap_bar(rev_cap_bar, _P):
    '''
    Calcule le prélèvement social sur les revenus du capital soumis au barème
    '''
    P = _P.prelsoc
    if _P.datesim.year < 2006:
        total = P.base 
    elif _P.datesim.year < 2009:    
        total = P.base + P.add
    else:    
        total = P.base + P.add + P.rsa
    return - rev_cap_bar*total

# revenus du capital soumis au prélèvement libératoire
def _csg_cap_lib(rev_cap_lib, _P):
    '''
    Calcule la CSG sur les revenus du capital soumis au prélèvement libératoire
    '''
    return - rev_cap_lib*_P.csg.capital.glob

def _crds_cap_lib(rev_cap_lib, _P):
    '''
    Calcule la CRDS sur les revenus du capital soumis au prélèvement libératoire
    '''
    return - rev_cap_lib*_P.crds.capital

def _prelsoc_cap_lib(rev_cap_lib, _P):
    '''
    Calcule le prélèvement social sur les revenus du capital soumis au prélèvement libératoire
    '''
    P = _P.prelsoc
    if _P.datesim.year < 2006:
        total = P.base 
    elif _P.datesim.year < 2009:    
        total = P.base + P.add
    else:    
        total = P.base + P.add + P.rsa
    return - rev_cap_lib*total


# TODO: non_imposabilité pour les revenus au barème
#        verse = (-csgcap_bar - crdscap_bar - prelsoccap_bar) > bareme.csg.capital.nonimp
##        verse=1
#        # CSG sur les revenus du patrimoine non imposés au barême (contributions sociales déjà prélevées)
#                
#        table.setIndiv('csgcap_bar', csgcap_bar*verse)
#        table.setIndiv('prelsoccap_bar', prelsoccap_bar*verse)
#        table.setIndiv('crdscap_bar', crdscap_bar*verse)


############################################################################
## Salaires
############################################################################

def _salbrut(sali, hsup, type_sal, _defaultP):
    '''
    Calcule le salaire brut à partir du salaire net
    '''
    plaf_ss = 12*_defaultP.cotsoc.gen.plaf_ss

    sal = scaleBaremes(BaremeDict('sal', _defaultP.cotsoc.sal), plaf_ss)
    csg = scaleBaremes(BaremeDict('csg', _defaultP.csg), plaf_ss)
    
    sal['noncadre'].update(sal['commun'])
    sal['cadre'].update(sal['commun'])


    noncadre = combineBaremes(sal['noncadre'])
    cadre    = combineBaremes(sal['cadre'])
    fonc     = combineBaremes(sal['fonc'])

    # On ajoute la CSG deductible
    noncadre.addBareme(csg['act']['deduc'])
    cadre.addBareme(csg['act']['deduc'])
    fonc.addBareme(csg['act']['deduc'])
    
    nca = noncadre.inverse()
    cad = cadre.inverse()
    fon = fonc.inverse()

    brut_nca = nca.calc(sali)
    brut_cad = cad.calc(sali)
    brut_fon = fon.calc(sali)

    salbrut = (brut_nca*(type_sal == CAT['noncadre']) + 
               brut_cad*(type_sal == CAT['cadre']) + 
               brut_fon*(type_sal == CAT['etat_t']) )
    
    return salbrut + hsup


def _type_sal(titc, statut, chpub, cadre, _P):
    '''
    Defines the type_sal of the individual
    0 noncadre
    1 cadre
    2 etat_t   : agent titualire de l'Etat
    3 colloc_t : agent titualire des collectivités locales
    4 contract : agent contractuel de l'Etat ou des collectivités locales
    
    '''
    
    cadre    = (statut ==8)*(chpub>3)*cadre 
    noncadre = (statut ==8)*(chpub>3)*not_(cadre)    

    
    etat_stag = (chpub==1)*(titc == 1)
    etat_tit  = (chpub==1)*(titc == 2)
    etat_cont = (chpub==1)*(titc == 3)

    colloc_stag = (chpub==2)*(titc == 1)
    colloc_tit  = (chpub==2)*(titc == 2)
    colloc_cont = (chpub==2)*(titc == 3)


    hosp_stag = (chpub==2)*(titc == 1)
    hosp_tit  = (chpub==2)*(titc == 2)
    hosp_cont = (chpub==2)*(titc == 3)

    contract = (colloc_cont + hosp_cont + etat_cont) > 1
    
    colloc_tit2 = (colloc_tit + hosp_tit ) > 1
    
    return 1*cadre + 2*etat_tit + 3*colloc_tit2 + 4*contract 



def build_pat(_P):
    '''
    Builds pat from P.cotsoc.pat
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    
    pat = scaleBaremes(BaremeDict('pat', _P.cotsoc.pat), plaf_ss)

    pat['noncadre'].update(pat['commun'])
    pat['cadre'].update(pat['commun'])
    
    pat['fonc']['contract'].update(pat['commun'])

    for var in ["maladie", "apprentissage", "apprentissage2", "vieillesseplaf", "vieillessedeplaf", "formprof", "chomfg", "construction","assedic"]:
        del pat['commun'][var]
        
    for var in ["apprentissage", "apprentissage2", "formprof", "chomfg", "construction","assedic"]:
        del pat['fonc']['contract'][var]

    pat['fonc']['etat'].update(pat['commun'])
    pat['fonc']['colloc'].update(pat['commun'])
    
    
    del pat['commun']

    pat['etat_t'] = pat['fonc']['etat']
    pat['colloc_t'] = pat['fonc']['colloc']

    pat['contract'] =  pat['fonc']['contract']
    
    del pat['fonc']['etat']
    del pat['fonc']['colloc']
    

# TODO manque transport

    return pat


def _cotpat_contrib(salbrut, hsup, type_sal, _P):
    '''
    Cotisation sociales patronales contributives
    '''
    pat = build_pat(_P)
    cotpat = zeros(len(salbrut))
    for categ in CAT:
        iscat = (type_sal == categ[1])
        for bar in pat[categ[0]].itervalues():
            is_contrib = (bar.option == "contrib")
            temp = - (iscat*bar.calc(salbrut))*is_contrib
            cotpat += temp
    return cotpat

def _cotpat_noncontrib(salbrut, hsup, type_sal, _P):
    '''
    Cotisation sociales patronales non contributives
    '''
    pat = build_pat(_P)
    cotpat = zeros(len(salbrut))
    for categ in CAT:
        iscat = (type_sal == categ[1])
        for bar in pat[categ[0]].itervalues(): 
            is_noncontrib = (bar.option == "noncontrib")
            temp = - (iscat*bar.calc(salbrut))*is_noncontrib
            cotpat += temp
    return cotpat


def _cotpat(cotpat_contrib, cotpat_noncontrib):
    '''
    Cotisations sociales patronales
    '''
    return cotpat_contrib + cotpat_noncontrib


def build_sal(_P):
    '''
    Builds sal from P.cotsoc.pat
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    
    sal = scaleBaremes(BaremeDict('sal', _P.cotsoc.sal), plaf_ss)
    sal['noncadre'].update(sal['commun'])
    sal['cadre'].update(sal['commun'])
    sal['etat_t'] = sal['fonc']['etat']
    sal['colloc_t'] = sal['fonc']['colloc']
    sal['contract']   = sal['fonc']['contract']

    sal['contract'].update(sal['commun'])
    del sal['contract']['arrco']
    del sal['contract']['assedic'] 
    sal['contract']['solidarite'] = sal['fonc']['commun']['solidarite']

    del sal['fonc']['etat']
    del sal['fonc']['colloc']
    del sal['fonc']['contract']
    del sal['commun']

#    print 'sal etat'
#    print sal['etat_t'].keys()
#    
#    print 'sal colloc'
#    print sal['colloc_t'].keys()
    
#    print 'sal contract'
#    print sal['contract'].keys()
    
    
    return sal


def seuil_fds(_P):
    '''
    Calcul du seuil mensuel d'assujetissement à la contribution au fond de solidarité 
    '''
    from math import  floor
    ind_maj_ref = _P.cotsoc.sal.fonc.commun.ind_maj_ref
    pt_ind = _P.cotsoc.sal.fonc.commun.pt_ind
    seuil_mensuel = floor(100*(pt_ind*ind_maj_ref)/12)
    return seuil_mensuel


def _cotsal_contrib(salbrut, hsup, type_sal, _P):
    '''
    Cotisations sociales salariales contributives
    '''
    sal = build_sal(_P)
    cotsal = zeros(len(salbrut))
    for categ in CAT:
        iscat = (type_sal == categ[1])
        for bar in sal[categ[0]].itervalues():
            is_contrib = (bar.option == "contrib")
            temp = - (iscat*bar.calc(salbrut-hsup))*is_contrib
            cotsal += temp
    return cotsal

def _cotsal_noncontrib(salbrut, hsup, type_sal, _P):
    '''
    Cotisations sociales salariales non-contributives
    '''
    sal = build_sal(_P)    
    cotsal = zeros(len(salbrut))
    seuil_assuj_fds = seuil_fds(_P)
    for categ in CAT:
        iscat = (type_sal == categ[1])
        for bar in sal[categ[0]].itervalues():
            is_noncontrib = (bar.option == "noncontrib")
            is_exempt_fds = (categ[0] in ['etat_t', 'colloc_t'])*(bar._name == 'solidarite')*( (salbrut-hsup) <= seuil_assuj_fds)   #TODO: check assiette voir IPP
            
            temp = - (iscat*bar.calc(salbrut-hsup))*is_noncontrib*not_(is_exempt_fds)
            cotsal += temp
    return cotsal

def _cotsal(cotsal_contrib, cotsal_noncontrib):
    '''
    Cotisations sociales salariales
    '''
    return cotsal_contrib + cotsal_noncontrib


def _csgsald(salbrut, hsup, _P):
    '''
    CSG deductible sur les salaires
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(_P.csg.act.deduc, plaf_ss)

    return - csg.calc(salbrut - hsup) 

def _csgsali(salbrut, hsup, _P):
    '''
    CSG imposable sur les salaires
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(_P.csg.act.impos, plaf_ss)
    return  - csg.calc(salbrut - hsup)

def _crdssal(salbrut, hsup, _P):
    '''
    CRDS sur les salaires
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    crds = scaleBaremes(_P.crds.act, plaf_ss)
    return - crds.calc(salbrut - hsup)

def _sal_h_b(salbrut):
    '''
    Salaire horaire brut
    '''
    nbh_travaillees = 151.67*12
    return salbrut/nbh_travaillees


def _alleg_fillon(salbrut, sal_h_b, type_sal, _P):
    '''
    Allègement de charges patronales sur les bas et moyens salaires
    dit allègement Fillon  
    '''
    
    P = _P.cotsoc

    taux_fillon = taux_exo_fillon(sal_h_b, P)
    alleg_fillon = taux_fillon*salbrut*(type_sal == CAT['noncadre'])
    return alleg_fillon

def _sal(salbrut, csgsald, cotsal, hsup):
    '''
    Calcul du salaire imposable
    '''
    return salbrut + csgsald + cotsal - hsup

def _salsuperbrut(salbrut, cotpat, alleg_fillon):
    return salbrut - cotpat - alleg_fillon
############################################################################
## Allocations chômage
############################################################################

def exo_csg_chom(choi, _P):
    '''
    Indicatrice d'exonération de la CSG sur les revenus du chômage
    '''
    # TODO: on néglige la csg imposable ...
    nbh_travail = 151.67 # depuis 2001
    cho_seuil_exo = _P.csg.chom.min_exo*nbh_travail*_P.cotsoc.gen.smic_h_b
    return (choi <= 12*cho_seuil_exo) # annuel
    

def _csg_rempl(rfr_n_2, nbpt_n_2, choi, rsti, _P):
    '''
    Taux retenu sur la CSG des revenus de remplacment:
    0 : Non renseigné/non pertinent
    1 : Exonéré
    2 : Taux réduit
    3 : Taux plein
    '''
    # TODO: problème avec le rfr n-2
    P = _P.cotsoc.gen
    seuil_th = P.plaf_th_1 + P.plaf_th_supp*(max_(0, (nbpt_n_2-1)/2))
    res =  (0 + 
            max_((choi>0) + (rsti>0), 0) +
            (rfr_n_2 >= seuil_th) +
            1  ) # conditon sur impot avant credit > seuil de non imposition 
    
    return 3*ones(len(res))

def _chobrut(choi, csg_rempl, _defaultP):
    '''
    Calcule les allocations chômage brute à partir des allocations nettes
    '''
    # TODO: ajouter la crds ?
    P = _defaultP.csg.chom
    chom_plein = P.plein.deduc.inverse()
    chom_reduit = P.reduit.deduc.inverse()
    chobrut = (csg_rempl==1)*choi + (csg_rempl==2)*chom_reduit.calc(choi) + (csg_rempl==3)*chom_plein.calc(choi) 
    isexo = exo_csg_chom(choi, _defaultP)
    chobrut = not_(isexo)*chobrut + (isexo)*choi
 
    return chobrut

def _csgchod(chobrut, choi, csg_rempl, _P):
    '''
    CSG déductible sur les allocations chômage
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', _P.csg.chom), plaf_ss)
    taux_plein = csg['plein']['deduc'].calc(chobrut)
    taux_reduit = csg['reduit']['deduc'].calc(chobrut)
    csgchod = (csg_rempl==2)*taux_reduit + (csg_rempl==3)*taux_plein
    isexo = exo_csg_chom(choi, _P)
    return - not_(isexo)*csgchod  

def _csgchoi(chobrut, choi, csg_rempl, _P):
    '''
    CSG imposable sur les allocations chômage
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', _P.csg.chom), plaf_ss)
    taux_plein = csg['plein']['impos'].calc(chobrut)
    taux_reduit = csg['reduit']['impos'].calc(chobrut)
    csgchoi = (csg_rempl==2)*taux_reduit + (csg_rempl==3)*taux_plein
    isexo = exo_csg_chom(choi, _P)
    return - not_(isexo)*csgchoi

def _crdscho(chobrut, choi, _P):
    '''
    CRDS sur les allocations chômage
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    crds = scaleBaremes(_P.crds.act, plaf_ss)
    return - crds.calc(chobrut)

def _cho(chobrut, csgchod, choi, _P):
    '''
    
    '''
    isexo = exo_csg_chom(choi, _P)
    return chobrut + not_(isexo)*csgchod


############################################################################
## Pensions
############################################################################
def _rstbrut(rsti, csg_rempl, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions nettes
    '''
    P = _defaultP.csg.retraite
    rst_plein = P.plein.deduc.inverse()  # TODO:     rajouter la non  déductible dans param
    rst_reduit = P.reduit.deduc.inverse()  #
    rstbrut = (csg_rempl==2)*rst_reduit.calc(rsti) + (csg_rempl==3)*rst_plein.calc(rsti)    
    return rstbrut

def _csgrstd(rstbrut, csg_rempl, _P):
    '''
    CSG déductible sur les allocations chômage
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', _P.csg.retraite), plaf_ss)
    taux_plein = csg['plein']['deduc'].calc(rstbrut)
    taux_reduit = csg['reduit']['deduc'].calc(rstbrut)
    csgrstd = (csg_rempl==3)*taux_plein + (csg_rempl==2)*taux_reduit
    return - csgrstd

def _csgrsti(rstbrut, csg_rempl, _P):
    '''
    CSG imposable sur les allocations chômage
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', _P.csg.retraite), plaf_ss)
    taux_plein = csg['plein']['impos'].calc(rstbrut)
    taux_reduit = csg['reduit']['impos'].calc(rstbrut)    
    csgrsti = (csg_rempl==3)*taux_plein + (csg_rempl==2)*taux_reduit
    return - csgrsti

def _crdsrst(rstbrut, _P):
    '''
    CRDS sur les pensions
    '''
    plaf_ss = 12*_P.cotsoc.gen.plaf_ss
    crds = scaleBaremes(BaremeDict('crds', _P.crds.rst), plaf_ss)
    return - crds['rst'].calc(rstbrut)

def _rst(rstbrut, csgrstd):
    '''
    Calcule les pensions nettes
    '''
    return rstbrut + csgrstd

############################################################################
## Impôt Landais, Piketty, Saez
############################################################################

def _base_csg(salbrut, chobrut, rstbrut, rev_cap_bar, rev_cap_lib):
    '''
    Assiette de la csg
    '''
    return salbrut + chobrut + rstbrut + rev_cap_bar + rev_cap_lib

def _ir_lps(base_csg, nbF, nbH, statmarit, _P):
    '''
    Impôt individuel sur l'ensemble de l'assiette de la csg, comme proposé par
    Landais, Piketty, Saez (2011)
    '''
    P = _P.lps
    nbEnf = (nbF + nbH/2)
    ae = nbEnf*P.abatt_enfant
    re = nbEnf*P.reduc_enfant
    ce = nbEnf*P.credit_enfant

    couple = (statmarit == 1) | (statmarit == 5)
    ac = couple*P.abatt_conj
    rc = couple*P.reduc_conj

    return - max_(0, P.bareme.calc(max_(base_csg - ae - ac, 0) )-re-rc) + ce


############################################################################
## Helper functions
############################################################################

def taux_exo_fillon(sal_h_b, P):
    '''
    Exonération Fillon
    http://www.securite-sociale.fr/comprendre/dossiers/exocotisations/exoenvigueur/fillon.htm
    '''
    # TODO Ainsi, à compter du 1er juillet 2007, le taux d’exonération des employeurs de 19 salariés au plus
    # passera pour une rémunération horaire égale au SMIC de 26 % à 28,1 %.
    
    # TODO la divison par zéro engendre un warning
    # Le montant maximum de l’allègement dépend de l’effectif de l’entreprise. 
    # Le montant est calculé chaque année civile, pour chaque salarié ; 
    # il est égal au produit de la totalité de la rémunération annuelle telle que visée à l’article L. 242-1 du code de la Sécurité sociale par un coefficient. 
    # Ce montant est majoré de 10 % pour les entreprises de travail temporaire au titre des salariés temporaires pour lesquels elle est tenue à l’obligation 
    # d’indemnisation compensatrice de congés payés.
    smic_h_b = P.gen.smic_h_b
    seuil = P.exo_fillon.seuil
    tx_max = P.exo_fillon.tx_max
    if seuil <= 1:
        return 0 
    return tx_max*min_(1,max_(seuil*smic_h_b/(sal_h_b + 1e-10)-1,0)/(seuil-1))

