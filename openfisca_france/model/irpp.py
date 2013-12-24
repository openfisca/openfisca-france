# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division
from numpy import ( maximum as max_, minimum as min_, logical_xor as xor_, 
                     logical_not as not_, round) 

from src.countries.france.model.data import QUIFOY

VOUS = QUIFOY['vous']
CONJ = QUIFOY['conj']
PAC1 = QUIFOY['pac1']
PAC2 = QUIFOY['pac2']
PAC3 = QUIFOY['pac3']
ALL = [x[1] for x in QUIFOY]
        
# zetrf = zeros(taille)
# jveuf = zeros(taille, dtype = bool)
# Reprise du crédit d'impôt en faveur des jeunes, des accomptes et des versements mensues de prime pour l'emploi
# reprise = zeros(taille) # TODO : reprise=J80
# Pcredit = P.credits_impots
# if hasattr(P.reductions_impots,'saldom'): Pcredit.saldom =  P.reductions_impots.saldom
# credits_impot = Credits(Pcredit, table)
# Réduction d'impôt
# reductions = Reductions(IPnet, P.reductions_impots)

#def mcirra():
#    # impôt sur le revenu
#    mcirra = -((IMP<=-8)*IMP)
#    mciria = max_(0,(IMP>=0)*IMP)
##        mciria = max_(0,(IMP>=0)*IMP - credimp_etranger - cont_rev_loc - ( f8to + f8tb + f8tc ))
#    
#    # Dans l'ERFS, les prelevement libératoire sur les montants non déclarés
#    # sont intégrés. Pas possible de le recalculer.
#    
#    # impot sur le revenu du foyer (hors prélèvement libératoire, revenus au quotient)
#    irpp   = -(mciria + ppetot - mcirra )
    

###############################################################################
## Initialisation de quelques variables utiles pour la suite
###############################################################################

def _nb_adult(marpac, celdiv, veuf):
    return 2*marpac + 1*(celdiv | veuf)

def _nb_pac(nbF, nbJ, nbR):
    return nbF + nbJ + nbR
        
def _marpac(statmarit, _option = {'statmarit': [VOUS]}):
    '''
    Marié (1) ou Pacsé (5)
    'foy'
    '''
    return (statmarit == 1) | (statmarit == 5)

def _celdiv(statmarit , _option = {'statmarit': [VOUS]}):
    '''
    Célibataire (2) ou divorcé (3)
    'foy'
    '''
    return (statmarit == 2) | (statmarit == 3)

def _veuf(statmarit , _option = {'statmarit': [VOUS]}):
    '''
    Veuf (4)
    'foy'
    '''
    return statmarit == 4

def _jveuf(statmarit , _option = {'statmarit': [VOUS]}):
    '''
    Jeune Veuf
    'foy'
    '''
    return statmarit == 6

###############################################################################
## Revenus catégoriels
###############################################################################

def _alloc(af, _P):
    '''
    Allocations familiales imposables
    '''
    P = _P.ir.autre
    return af*P.alloc_imp

def _rev_sal(sal, cho):
    '''
    Revenu imposé comme des salaires (salaires, mais aussi 3vj, 3vk)
    'ind'
    '''
    return sal + cho

def _sal_net(rev_sal, cho_ld, fra, _P):
    """
    Salaires après abattements
    'ind'
    """
    P = _P.ir.tspr.abatpro
    amin = P.min*not_(cho_ld) + P.min2*cho_ld
    abatfor = round(min_(max_(P.taux*rev_sal, amin),P.max))
    return (fra > abatfor)*(rev_sal - fra) \
         + (fra <= abatfor)*max_(0,rev_sal - abatfor)

def _rev_pen(alr, alr_decl, rst):
    """
    Revenu imposé comme des pensions (retraites, pensions alimentaires, etc.)
    'ind'
    """
    return alr*alr_decl + rst

def _pen_net(rev_pen, _P):
    """
    Pensions après abattements
    'ind'
    """
    P = _P.ir.tspr.abatpen
#    problème car les pensions sont majorées au niveau du foyer
#    d11 = ( AS + BS + CS + DS + ES + 
#            AO + BO + CO + DO + EO ) 
#    penv2 = (d11-f11> P.abatpen.max)*(penv + (d11-f11-P.abatpen.max)) + (d11-f11<= P.abatpen.max)*penv   
#    Plus d'abatement de 20% en 2006
    return max_(0, rev_pen - round(max_(P.taux*rev_pen , P.min))) 
#    return max_(0, rev_pen - min_(round(max_(P.taux*rev_pen , P.min)), P.max))  le max se met au niveau du foyer

def _indu_plaf_abat_pen(rev_pen, pen_net, _P, _option = {'rev_pen': ALL, 'pen_net': ALL}):
    """
    Plafonnement de l'abattement de 10% sur les pensions du foyer
    'foy' 
    """
    P = _P.ir.tspr.abatpen
    rev_pen_foy = 0
    for rev_pen_qui in rev_pen.itervalues():
        rev_pen_foy += rev_pen_qui

    pen_net_foy = 0
    for pen_net_qui in pen_net.itervalues():
        pen_net_foy += pen_net_qui
        
    abat = rev_pen_foy - pen_net_foy
    return abat - min_(abat, P.max)   

def _abat_sal_pen(sal_net, pen_net, _P):
    """
    Abattement de 20% sur les salaires
    'ind'
    """
    P = _P.ir.tspr.abatsalpen
    return min_(P.taux*max_(sal_net + pen_net, 0), P.max)

def _sal_pen_net(sal_net, pen_net, abat_sal_pen):
    """
    Salaires et pensions après abattement de 20% sur les salaires
    'ind'
    """
    return sal_net + pen_net - abat_sal_pen

def _rto(f1aw, f1bw, f1cw, f1dw):
    """
    Rentes viagères à titre onéreux (avant abattements)
    """
    return f1aw + f1bw + f1cw + f1dw

def _rto_net(f1aw, f1bw, f1cw, f1dw, _P):
    '''
    Rentes viagères après abattements
    '''
    P = _P.ir.tspr.abatviag
    return round(P.taux1*f1aw + P.taux2*f1bw + P.taux3*f1cw + P.taux4*f1dw )

def _tspr(sal_pen_net, rto_net):
    '''
    Traitemens salaires pensions et rentes individuelles
    'ind'
    '''
    return sal_pen_net + rto_net

def _rev_cat_tspr(tspr, indu_plaf_abat_pen, _option = {'tspr': ALL}):
    '''
    Traitemens salaires pensions et rentes
    'foy'
    '''
    #TODO: add just a sum option
    out = 0
    for qui in tspr.itervalues():
        out += qui

    return out + indu_plaf_abat_pen

def _deficit_rcm(f2aa, f2al, f2am, f2an):
    return f2aa + f2al + f2am + f2an

def _rev_cat_rvcm(marpac, deficit_rcm, f2ch, f2dc, f2ts, f2ca, f2fu, f2go, f2gr, f2tr, f2da, f2ee, _P):
    """
    REVENUS DES VALEURS ET CAPITAUX MOBILIERS 
    """
    P = _P.ir.rvcm
    if _P.datesim.year > 2004: f2gr = 0

    # Add f2da to f2dc and f2ee to f2tr when no PFL
    if _P.ir.autre.finpfl:
        f2dc_bis = f2dc + f2da
        f2tr_bis = f2tr + f2ee
    else:
        f2dc_bis = f2dc
        f2tr_bis = f2tr
    ## Calcul du revenu catégoriel
    #1.2 Revenus des valeurs et capitaux mobiliers
    b12 = min_(f2ch, P.abat_assvie*(1 + marpac))
    TOT1 = f2ch-b12
    # Part des frais s'imputant sur les revenus déclarés case DC
    den = ((f2dc_bis + f2ts)!=0)*(f2dc_bis + f2ts) + ((f2dc_bis + f2ts)==0)
    F1 =  f2ca/den*f2dc_bis
    
    # Revenus de capitaux mobiliers nets de frais, ouvrant droit à abattement
    # partie négative (à déduire des autres revenus nets de frais d'abattements
    g12a = - min_(f2dc_bis*P.abatmob_taux - F1,0)
    # partie positive
    g12b = max_(f2dc_bis*P.abatmob_taux - F1,0)
    
    rev = g12b + f2gr + f2fu*P.abatmob_taux

    # Abattements, limité au revenu
    h12 = P.abatmob*(1 + marpac)
    TOT2 = max_(0,rev - h12)
    i121= -min_(0,rev - h12)
    
    # Part des frais s'imputant sur les revenus déclarés ligne TS
    F2 = f2ca - F1
    TOT3 = (f2ts - F2) + f2go*P.majGO + f2tr_bis - g12a

    DEF = deficit_rcm

    return max_(TOT1 + TOT2 + TOT3 - DEF, 0)

def _rfr_rvcm(f2dc, f2fu, f2da, _P):
    '''
    Abattements sur rvcm à réintégrer dans le revenu fiscal de référence
    '''
    P = _P.ir.rvcm
    if _P.ir.autre.finpfl:
        f2dc_bis = f2dc + f2da
    else:
        f2dc_bis = f2dc
    ## TODO: manque le sous total i121 (dans la fonction _rev_cat_rvcm)
    i121 = 0
    return max_((1-P.abatmob_taux)*(f2dc_bis + f2fu) - i121, 0)

def _rev_cat_rfon(f4ba, f4bb, f4bc, f4bd, f4be, _P):
    """
    Revenus fonciers
    """    
    P = _P.ir.microfoncier
    ## Calcul du revenu catégoriel
    a13 = f4ba + f4be - P.taux*f4be*(f4be <= P.max)
    b13 = f4bb
    c13 = a13-b13
    d13 = f4bc
    e13 = c13- d13*(c13>=0)
    f13 = f4bd*(e13>=0)
    g13 = max_(0, e13- f13)
    out  = (c13>=0)*(g13 + e13*(e13<0)) - (c13<0)*d13
    return out

def _rev_cat_rpns(rpns_i, _option = {'rpns_i': ALL}):
    '''
    Traitemens salaires pensions et rentes
    'foy'
    '''
    out = None
    for qui in rpns_i.itervalues():
        if out is None:
            out = qui
        else:
            out += qui
    
    return out

def _rev_cat(rev_cat_tspr, rev_cat_rvcm, rev_cat_rfon, rev_cat_rpns):
    ''' Revenus Categoriels '''
#    AUTRE = TSPR + RVCM + RFON
    return rev_cat_tspr + rev_cat_rvcm + rev_cat_rfon + rev_cat_rpns

###############################################################################
## Déroulé du calcul de l'irpp
###############################################################################

def _deficit_ante(f6fa, f6fb, f6fc, f6fd, f6fe, f6fl):
    ''' Déficits antérieurs '''
    return f6fa + f6fb + f6fc + f6fd + f6fe + f6fl

def _rbg(alloc, rev_cat, deficit_ante, f6gh, _P):
    ''' Revenu brut global (Total 17) '''
    # sans les revenus au quotient
    return max_(0, alloc + rev_cat + f6gh - deficit_ante)

def _csg_deduc(rbg, f6de):
    ''' CSG déductible '''
    return min_(f6de, max_(rbg, 0))

def _rng(rbg, csg_deduc, charges_deduc):
    ''' Revenu net global (total 20) '''
    return max_(0, rbg - csg_deduc - charges_deduc)

def _rni(rng, abat_spe):
    return rng - abat_spe

def _ir_brut(nbptr, rni, _P):
    '''
    Impot sur le revenu avant non imposabilité et plafonnement du quotien
    'foy'
    '''
    bar = _P.ir.bareme
    bar.t_x()
#    bar._linear_taux_moy = True
    return nbptr*bar.calc(rni/nbptr) # TODO : partir d'ici, petite différence avec Matlab

def _ir_ss_qf(ir_brut, rni, nb_adult, _P):
    ''' Impôt sans quotient familial '''
    P = _P.ir
    I = ir_brut
    A = P.bareme.calc(rni/nb_adult)
    return nb_adult*A    
    

def _ir_plaf_qf(ir_brut, ir_ss_qf, nb_adult, nb_pac, nbptr, marpac, veuf, jveuf, celdiv, caseE, caseF, caseG, caseH, caseK, caseN, caseP, caseS, caseT, caseW, nbF, nbG, nbH, nbI, nbR, _P):
    ''' Impôt après plafonnement du quotient familial et réduction complémentaire '''

    A = ir_ss_qf
    I = ir_brut
    P = _P.ir
    
    aa0 = (nbptr-nb_adult)*2           #nombre de demi part excédant nbadult
    # on dirait que les impôts font une erreur sur aa1 (je suis obligé de
    # diviser par 2)
    aa1 = min_((nbptr-1)*2,2)/2  # deux première demi part excédants une part
    aa2 = max_((nbptr-2)*2,0)    # nombre de demi part restantes
    # celdiv parents isolés
    condition61 = celdiv & caseT
    B1 = P.plafond_qf.celib_enf*aa1 + P.plafond_qf.marpac*aa2
    # tous les autres
    B2 = P.plafond_qf.marpac*aa0                 #si autre
    # celdiv, veufs (non jveuf) vivants seuls et autres conditions
    # TODO: année en dur... pour caseH
    condition63 = (celdiv | (veuf & not_(jveuf))) & not_(caseN) & (nb_pac==0) & (caseK | caseE) & (caseH<1981)
    B3 = P.plafond_qf.celib

    B = B1*condition61 + \
        B2*(not_(condition61 | condition63)) + \
        B3*(condition63 & not_(condition61))
    C = max_(0,A-B)
    # Impôt après plafonnement
    IP0 = max_(I, C) 

    # 6.2 réduction d'impôt pratiquée sur l'impot après plafonnement et le cas particulier des DOM
    # pas de réduction complémentaire
    condition62a = (I>=C)
    # réduction complémentaire
    condition62b = (I<C)
    # celdiv veuf
    condition62caa0 = (celdiv | (veuf & not_(jveuf)))
    condition62caa1 = (nb_pac==0)&(caseP | caseG | caseF | caseW)
    condition62caa2 = caseP & ((nbF-nbG>0)|(nbH - nbI>0))
    condition62caa3 = not_(caseN) & (caseE | caseK )  & (caseH>=1981)
    condition62caa  = condition62caa0 & (condition62caa1 | condition62caa2 | condition62caa3)
    # marié pacs
    condition62cab = (marpac | jveuf) & caseS & not_(caseP | caseF)
    condition62ca =    (condition62caa | condition62cab)

    # plus de 590 euros si on a des plus de
    condition62cb = ((nbG+nbR+nbI)>0) | caseP | caseF
    D = P.plafond_qf.reduc_postplafond*(condition62ca + ~condition62ca*condition62cb*( 1*caseP + 1*caseF + nbG + nbR + nbI/2 ))

    E = max_(0,A-I-B)
    Fo = D*(D<=E) + E*(E<D)
    IP1 = IP0-Fo

    # TODO: 6.3 Cas particulier: Contribuables domiciliés dans les DOM.    
    # conditionGuadMarReu =
    # conditionGuyane=
    # conitionDOM = conditionGuadMarReu | conditionGuyane
    # postplafGuadMarReu = 5100
    # postplafGuyane = 6700
    # IP2 = IP1 - conditionGuadMarReu*min( postplafGuadMarReu,.3*IP1)  - conditionGuyane*min(postplafGuyane,.4*IP1)

    # Récapitulatif
    return condition62a*IP0 + condition62b*IP1 # IP2 si DOM

def _avantage_qf(ir_ss_qf, ir_plaf_qf):
    return ir_ss_qf - ir_plaf_qf


def _decote(ir_plaf_qf, _P):
    '''
    Décote
    '''
    P = _P.ir.decote
    return (ir_plaf_qf < P.seuil)*(P.seuil - ir_plaf_qf)*0.5

def _nat_imp(irpp):
    '''
    Renvoie True si le foyer est imposable, False sinon
    '''
    #def _nat_imp(rni, nbptr, _P):
    #P = _P.ir.non_imposable
    #seuil = P.seuil + (nbptr - 1)*P.supp
    return irpp > 0 

def _ip_net(ir_plaf_qf, decote):
    '''
    irpp après décote
    '''
    return max_(0, ir_plaf_qf - decote)

def _iaidrdi(ip_net, reductions):
    '''
    Impôt après imputation des réductions d'impôt
    '''
    return ip_net - reductions

def _cont_rev_loc(f4bl, _P):
    '''
    Contribution sur les revenus locatifs
    '''
    P = _P.ir.crl
    return round(P.taux *(f4bl >= P.seuil)*f4bl)

def _teicaa(f5qm, f5rm, _P):

    """
    Taxe exceptionelle sur l'indemnité compensatrice des agents d'assurance
    """
    bareme = _P.ir.teicaa
    return bareme.calc(f5qm) + bareme.calc(f5rm)

def _plus_values(f3vg, f3vh, f3vl, f3vm, f3vi, f3vf, f3vd, rpns_pvce, _P):
    """
    Taxation des plus value
    TODO: f3vt, 2013 f3Vg au barème
    """
    P = _P.ir.plus_values
        # revenus taxés à un taux proportionnel
    rdp = max_(0,f3vg - f3vh) + f3vl + rpns_pvce + f3vm + f3vi + f3vf
    out = (P.pvce*rpns_pvce +
           P.taux1*max_(0,f3vg - f3vh) +
           P.caprisque*f3vl +
           P.pea*f3vm +
           P.taux3*f3vi +
           P.taux4*f3vf )
    if _P.datesim.year >= 2008:
        # revenus taxés à un taux proportionnel
        rdp += f3vd
        out += P.taux1*f3vd
        
    return round(out)

def _iai(iaidrdi, plus_values, cont_rev_loc, teicaa):
    '''
    impôt avant imputation
    '''
    return iaidrdi + plus_values + cont_rev_loc + teicaa

def _cehr(rfr, nb_adult, _P):
    '''
    Contribution exceptionnelle sur les hauts revenus
    'foy'
    '''
    bar = _P.ir.cehr
    return bar.calc(rfr/nb_adult)*nb_adult

def _cesthra(sal, _P, _option = {'sal': ALL}):
    '''
    Contribution exceptionnelle de solidarité sur les très hauts revenus d'activité
    'foy'
    '''
    cesthra = 0
    bar = _P.ir.cesthra
    for rev in sal.itervalues():
        cesthra += bar.calc(rev)
    return cesthra


def _irpp(iai, credits_impot, cehr, cesthra):
    '''
    Montant avant seuil de recouvrement (hors ppe)
    '''
    return  -(iai - credits_impot + cehr + cesthra)

###############################################################################
## Autres totaux utiles pour la suite
###############################################################################

def _alv(f6gi, f6gj, f6el, f6em, f6gp, f6gu):
    '''
    Pensions alimentaires versées
    '''
    return - (f6gi + f6gj + f6el + f6em + f6gp + f6gu)

def _rfr(rni, alloc, f3va, f3vg, f3vi, rfr_cd, rfr_rvcm, rpns_exon, rpns_pvce, rev_cap_lib, f3vz):
    '''
    Revenu fiscal de référence
    '''
    return max_(0, rni - alloc) + rfr_cd + rfr_rvcm + rev_cap_lib + f3vi + rpns_exon + rpns_pvce + f3va + f3vg + f3vz
 
def _glo(f1tv, f1tw, f1tx, f3vf, f3vi, f3vj, f3vk): 
    # TODO: f1uv, f1uw, f1ux deletion to check
    '''
    Gains de levée d'option
    'foy'
    '''
    return f1tv + f1tw + f1tx  + f3vf + f3vi + f3vj + f3vk   # + f1uv + f1uw + f1ux                

def _rev_cap_bar(f2dc, f2gr, f2ch, f2ts, f2go, f2tr, f2fu, avf, f2da, f2ee, _P):
    """
    Revenus du capital imposés au barème
    """
#    if _P.datesim.year <= 2011:
#        return f2dc + f2gr + f2ch + f2ts + f2go + f2tr + f2fu - avf
#    elif _P.datesim.year > 2011:
#        return f2dc + f2gr + f2ch + f2ts + f2go + f2tr + f2fu - avf + (f2da + f2ee) 
    return f2dc + f2gr + f2ch + f2ts + f2go + f2tr + f2fu - avf + (f2da + f2ee)*(_P.ir.autre.finpfl)  # we add f2da an f2ee to allow for comparaison between year 

def _rev_cap_lib(f2da, f2dh, f2ee, _P):
    '''
    Revenu du capital imposé au prélèvement libératoire
    '''
    if _P.datesim.year <=2007: 
        out = f2dh + f2ee
    else:
        out = f2da + f2dh + f2ee
        
    return out*not_(_P.ir.autre.finpfl)

def _avf(f2ab):
    '''
    Avoir fiscal et crédits d'impôt (zavff)
    '''
    return f2ab
    
def _imp_lib(f2da, f2dh, f2ee, _P):
    '''
    Prelèvement libératoire sur les revenus du capital
    '''
    P = _P.ir.rvcm.prelevement_liberatoire
    if _P.datesim.year <=2007: 
        out = - (P.assvie*f2dh + P.autre*f2ee )
    else:
        out = - (P.action*f2da  + P.autre*f2ee)*not_(_P.ir.autre.finpfl) - P.assvie*f2dh
    return out

def _fon(f4ba, f4bb, f4bc, f4bd, f4be, _P):
    '''
    Revenus fonciers
    '''
    ## Calcul des totaux        
    P = _P.ir.microfoncier
    fon = f4ba - f4bb - f4bc + round(f4be*(1-P.taux))  
    return fon


def _rpns_pvce(frag_pvce, arag_pvce, nrag_pvce, mbic_pvce, abic_pvce, 
               nbic_pvce, macc_pvce, aacc_pvce, nacc_pvce, mbnc_pvce, 
               abnc_pvce, nbnc_pvce, mncn_pvce, cncn_pvce):
    ''' 
    Plus values de cession
    'ind'
    frag_pvce (f5hx, f5ix, f5jx)
    arag_pvce (f5he, f5ie, f5je)
    nrag_pvce (f5hk, f5lk, f5jk)
    mbic_pvce (f5kq, f5lq, f5mq)
    abic_pvce (f5ke, f5le, f5me)
    nbic_pvce (f5kk, f5ik, f5mk)
    macc_pvce (f5nq, f5oq, f5pq)
    aacc_pvce (f5ne, f5oe, f5pe)
    nacc_pvce (f5nk, f5ok, f5pk)
    mncn_pvce (f5kv, f5lv, f5mv)
    cncn_pvce (f5so, f5nt, f5ot)
    mbnc_pvce (f5hr, f5ir, f5jr)
    abnc_pvce (f5qd, f5rd, f5sd)
    nbnc_pvce (f5qj, f5rj, f5sj)
    '''

    return ( frag_pvce + arag_pvce + nrag_pvce + mbic_pvce + abic_pvce + 
             nbic_pvce + macc_pvce + aacc_pvce + nacc_pvce + mbnc_pvce + 
             abnc_pvce + nbnc_pvce + mncn_pvce + cncn_pvce )

def _rpns_exon(frag_exon, arag_exon, nrag_exon, mbic_exon, abic_exon, 
               nbic_exon, macc_exon, aacc_exon, nacc_exon, mbnc_exon, 
               abnc_exon, nbnc_exon ):
    ''' 
    Plus values de cession
    'ind'
    frag_exon (f5hn, f5in, f5jn)
    arag_exon (f5hb, f5ib, f5jb)
    nrag_exon (f5hh, f5ih, f5jh)
    mbic_exon (f5kn, f5ln, f5mn)
    abic_exon (f5kb, f5lb, f5mb)
    nbic_exon (f5kh, f5lh, f5mh)
    macc_exon (f5nn, f5on, f5pn)
    aacc_exon (f5nb, f5ob, f5pb)
    nacc_exon (f5nh, f5oh, f5ph)
    mbnc_exon (f5hp, f5ip, f5jp)
    abnc_exon (f5qb, f5rb, f5sb)
    nbnc_exon (f5qh, f5rh, f5sh)
    '''
    
    return (frag_exon + arag_exon + nrag_exon + mbic_exon + abic_exon + 
            nbic_exon + macc_exon + aacc_exon + nacc_exon + mbnc_exon + 
            abnc_exon + nbnc_exon )
    
def _rag(frag_exon, frag_impo, arag_exon, arag_impg, arag_defi, nrag_exon, nrag_impg, nrag_defi, nrag_ajag):
    '''
    Revenus agricoles
    'ind'
    frag_exon (f5hn, f5in, f5jn)
    frag_impo (f5ho, f5io, f5jo)    
    arag_exon (f5hb, f5ib, f5jb)
    arag_impg (f5hc, f5ic, f5jc)
    arag_defi (f5hf, f5if, f5jf)
    nrag_exon (f5hh, f5ih, f5jh)
    nrag_impg (f5hi, f5ii, f5ji)
    nrag_defi (f5hl, f5il, f5jl)
    nrag_ajag (f5hm, f5im, f5jm)
    '''    
    return (frag_exon + frag_impo + 
            arag_exon + arag_impg - arag_defi + 
            nrag_exon + nrag_impg - nrag_defi + 
            nrag_ajag)

def _ric(mbic_exon, mbic_impv, mbic_imps, abic_exon, nbic_exon, abic_impn, nbic_impn,
         abic_imps, nbic_imps, abic_defn, nbic_defn, abic_defs, nbic_defs, nbic_apch, _P):
    '''
    Bénéfices industriels et commerciaux
    'ind'
    mbic_exon (f5kn, f5ln, f5mn)
    abic_exon (f5kb, f5lb, f5mb)
    nbic_exon (f5kh, f5lh, f5mh)
    mbic_impv (f5ko, f5lo, f5mo)
    mbic_imps (f5kp, f5lp, f5mp)
    abic_impn (f5kc, f5lc, f5mc)
    abic_imps (f5kd, f5ld, f5md)
    nbic_impn (f5ki, f5li, f5mi)
    nbic_imps (f5kj, f5lj, f5mj)
    abic_defn (f5kf, f5lf, f5mf)
    abic_defs (f5kg, f5lg, f5mg)
    nbic_defn (f5kl, f5ll, f5ml)
    nbic_defs (f5km, f5lm, f5mm)
    nbic_apch (f5ks, f5ls, f5ms)
    '''
    
    P = _P.ir.rpns.microentreprise
        
    zbic =(  mbic_exon + mbic_impv + mbic_imps
           + abic_exon + nbic_exon 
           + abic_impn + nbic_impn 
           + abic_imps + nbic_imps 
           - abic_defn - nbic_defn 
           - abic_defs - nbic_defs 
           + nbic_apch)
    
    cond = (mbic_impv>0) & (mbic_imps==0)
    taux = P.vente.taux*cond + P.servi.taux*not_(cond)
            
    cbic = min_(mbic_impv + mbic_imps + mbic_exon, 
                max_(P.vente.min,round(mbic_impv*P.vente.taux + mbic_imps*P.servi.taux + mbic_exon*taux)))
    
    ric = zbic - cbic

    return ric

def _rac(macc_exon, macc_impv, macc_imps,
         aacc_exon, aacc_impn, aacc_imps, aacc_defn, aacc_defs,
         nacc_exon, nacc_impn, nacc_imps, nacc_defn, nacc_defs,
         mncn_impo, cncn_bene, cncn_defi, _P):
    '''
    Revenus accessoires individuels
    'ind'
    macc_exon (f5nn, f5on, f5pn)
    aacc_exon (f5nb, f5ob, f5pb)
    nacc_exon (f5nh, f5oh, f5ph)
    macc_impv (f5no, f5oo, f5po)
    macc_imps (f5np, f5op, f5pp)
    aacc_impn (f5nc, f5oc, f5pc)
    aacc_imps (f5nd, f5od, f5pd)
    aacc_defn (f5nf, f5of, f5pf)
    aacc_defs (f5ng, f5og, f5pg)
    nacc_impn (f5ni, f5oi, f5pi)
    nacc_imps (f5nj, f5oj, f5pj)
    nacc_defn (f5nl, f5ol, f5pl)
    nacc_defs (f5nm, f5om, f5pm)
    mncn_impo (f5ku, f5lu, f5mu)
    cncn_bene (f5sn, f5ns, f5os)
    cncn_defi (f5sp, f5nu, f5ou, f5sr)
    f5sv????
    '''
    P = _P.ir.rpns.microentreprise

    zacc = (  macc_exon + macc_impv + macc_imps 
            + aacc_exon + aacc_impn + aacc_imps - aacc_defn - aacc_defs 
            + nacc_exon + nacc_impn + nacc_imps - nacc_defn - nacc_defs 
            + mncn_impo + cncn_bene - cncn_defi)
    
    cond = (macc_impv >0) & (macc_imps ==0)
    taux = P.vente.taux*cond + P.servi.taux*not_(cond)
    
    cacc = min_(macc_impv + macc_imps + macc_exon + mncn_impo, 
                max_(P.vente.min,
                     round(macc_impv*P.vente.taux + macc_imps*P.servi.taux + macc_exon*taux + mncn_impo*P.specialbnc.taux )))
    
    rac = zacc - cacc
    
    return rac

def _rnc(mbnc_exon, mbnc_impo, abnc_exon, nbnc_exon, abnc_impo, nbnc_impo, abnc_defi, nbnc_defi, _P):
    '''
    Revenus non commerciaux individuels
    'ind'
    mbnc_exon (f5hp, f5ip, f5jp)
    abnc_exon (f5qb, f5rb, f5sb)
    nbnc_exon (f5qh, f5rh, f5sh)
    mbnc_impo (f5hq, f5iq, f5jq)
    abnc_impo (f5qc, f5rc, f5sc)
    abnc_defi (f5qe, f5re, f5se)
    nbnc_impo (f5qi, f5ri, f5si)
    nbnc_defi (f5qk, f5rk, f5sk)
    f5ql, f5qm????
    '''
    P = _P.ir.rpns.microentreprise.specialbnc

    zbnc = (  mbnc_exon + mbnc_impo 
            + abnc_exon + nbnc_exon 
            + abnc_impo + nbnc_impo 
            - abnc_defi - nbnc_defi )
        
    cbnc = min_(mbnc_exon + mbnc_impo, max_(P.min, round((mbnc_exon + mbnc_impo)*P.taux)))
    
    rnc = zbnc - cbnc
    return rnc


def _rpns(rag, ric, rac, rnc):
    '''
    Revenus des professions non salariées individuels
    'ind'
    '''
    return rag + ric + rac + rnc

def _rpns_pvct(frag_pvct, mbic_pvct, macc_pvct, mbnc_pvct, mncn_pvct):
    '''
    Plus values de court terme
    'ind'
    frag_pvct (f5hw, f5iw, f5jw)
    mbic_pvct (f5kx, f5lx, f5mx)
    macc_pvct (f5nx, f5ox, f5px)
    mbnc_pvct (f5hv, f5iv, f5jv)
    mncn_pvct (f5ky, f5ly, f5my)
    '''
    return frag_pvct + mbic_pvct + macc_pvct + mbnc_pvct + mncn_pvct

def _rpns_mvct(mbic_mvct, macc_mvct, mbnc_mvct, mncn_mvct):
    '''
    Moins values de court terme
    'ind'
    mbic_mvct (f5hu)
    macc_mvct (f5iu)
    mncn_mvct (f5ju)
    mbnc_mvct (f5kz)

    '''
    return mbic_mvct + macc_mvct + mbnc_mvct + mncn_mvct

def _rpns_mvlt(mbic_mvlt, macc_mvlt, mbnc_mvlt, mncn_mvlt):
    '''
    Moins values de long terme
    'ind'
    mbic_mvlt (f5kr, f5lr, f5mr)
    macc_mvlt (f5nr, f5or, f5pr)
    mncn_mvlt (f5kw, f5lw, f5mw)
    mbnc_mvlt (f5hs, f5is, f5js)
    '''
    return mbic_mvlt + macc_mvlt + mbnc_mvlt + mncn_mvlt
    
def _rpns_i(frag_impo, arag_impg, nrag_impg, arag_defi,  nrag_defi,
            mbic_impv, mbic_imps, 
            abic_impn, abic_imps, abic_defn, abic_defs,
            nbic_impn, nbic_imps, nbic_defn, nbic_defs,
            macc_impv, macc_imps,
            aacc_impn, aacc_imps, aacc_defn, aacc_defs,
            nacc_impn, nacc_imps, nacc_defn, nacc_defs,
            mbnc_impo,
            abnc_impo, abnc_defi,
            nbnc_impo, nbnc_defi,
            mncn_impo, cncn_bene, cncn_defi,
            rpns_pvct, rpns_mvct, rpns_mvlt, 
            f5sq, _P):
    '''
    Revenus des professions non salariées individuels
    '''
    P = _P.ir.rpns.microentreprise
    def abat_rnps(rev, P):
        return max_(0,rev - min_(rev, max_(P.taux*min_(P.max, rev), P.min)))
    
    #Jeunes agriculteurs montant de l'abattement de 50% ou 100% 
    # nrag_ajag = f5hm + f5im + f5jm 
    
#    # déficits agricole des années antérieurs (imputables uniquement
#    # sur des revenus agricoles)
#    rag_timp = frag_impo + frag_pvct + arag_impg + nrag_impg 
#    cond = (AUTRE <= P.def_agri_seuil)
#    def_agri = cond*(arag_defi + nrag_defi) + not_(cond)*min_(rag_timp, arag_defi + nrag_defi)
#    # TODO : check 2006 cf art 156 du CGI pour 2006
#    def_agri_ant    = min_(max_(0,rag_timp - def_agri), f5sq)

    def_agri = arag_defi + nrag_defi + f5sq

    ## B revenus industriels et commerciaux professionnels     
    # regime micro entreprise
    mbic_timp = abat_rnps(mbic_impv, P.vente) + abat_rnps(mbic_imps, P.servi)
    
    # Régime du bénéfice réel bénéficiant de l'abattement CGA
    abic_timp = abic_impn + abic_imps - (abic_defn + abic_defs)
    
    # Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
    nbic_timp = (nbic_impn + nbic_imps) - (nbic_defn + nbic_defs)
    
    # Abatemment artisant pécheur
    # nbic_apch = f5ks + f5ls + f5ms # TODO : à intégrer qqpart
            
    ## C revenus industriels et commerciaux non professionnels 
    # (revenus accesoires du foyers en nomenclature INSEE)

    #regime micro entreprise
    macc_timp = abat_rnps(macc_impv, P.vente) + abat_rnps(macc_imps, P.servi) 
    #Régime du bénéfice réel bénéficiant de l'abattement CGA
    aacc_timp = max_(0, (aacc_impn + aacc_imps) - (aacc_defn + aacc_defs))    
    #Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
    nacc_timp = max_(0, (nacc_impn + nacc_imps) - (nacc_defn + nacc_defs))
    
    ## E revenus non commerciaux non professionnels 
    #regime déclaratif special ou micro-bnc
    mncn_timp = abat_rnps(mncn_impo, P.specialbnc)
    
    # régime de la déclaration controlée 
    #total 11
    cncn_timp = max_(0,cncn_bene - cncn_defi) 
    # Abatement jeunes créateurs 
    
    ## D revenus non commerciaux professionnels
    #regime déclaratif special ou micro-bnc
    mbnc_timp = abat_rnps(mbnc_impo, P.specialbnc)
    
    #regime de la déclaration contrôlée bénéficiant de l'abattement association agréée
    abnc_timp = abnc_impo - abnc_defi
    
    #regime de la déclaration contrôlée ne bénéficiant pas de l'abattement association agréée
    nbnc_timp = nbnc_impo - nbnc_defi
    
    ## Totaux
    atimp = arag_impg + abic_timp +  aacc_timp + abnc_timp
    ntimp = nrag_impg + nbic_timp +  nacc_timp + nbnc_timp
    
    majo_cga = max_(0,_P.ir.rpns.cga_taux2*(ntimp + frag_impo)) # pour ne pas avoir à
                                            # majorer les déficits
    #total 6
    rev_NS = frag_impo - def_agri + atimp + ntimp + majo_cga 
    
    #revenu net après abatement
    # total 7
    rev_NS_mi = mbic_timp + macc_timp + mbnc_timp + mncn_timp - rpns_mvlt
        
    RPNS = rev_NS + rev_NS_mi + rpns_pvct - rpns_mvct + cncn_timp
    
    return RPNS

def _abat_spe(age, caseP, caseF, rng, nbN, _P, _option = {'age': [VOUS, CONJ]}):
    """
    Abattements spéciaux 
    """
#    - pour personnes âges ou invalides : âgé(e) de plus de 65 ans
#      ou invalide (titulaire d’une pension d’invalidité militaire ou d’accident 
#      du travail d’au moins 40 % ou titulaire de la carte d’invalidité), 
#      abattement de 2 172 € si rng du foyer fiscal inférieur à 13 370 € 
#                    1 086 € si rng  compris entre 13 370 € et 21 570 €. 
#      Abattement doublé si conjoint remplit également ces conditions 
#      d’âge ou d’invalidité. 
#    - pour enfants à charge ayant fondé un foyer distinct : Si  rattachement 
#      enfants mariés ou pacsés ou enfants  célibataires, veufs, divorcés, séparés, chargés de famille, 
#      abattement 5 495 € par personne ainsi rattachée. 
#      Si l’enfant de la personne rattachée est réputé à charge de 
#      l’un et l’autre de ses parents (garde alternée), cet abattement est divisé 
#      par deux soit 2 748€. Exemple : 10 990 € pour un jeune ménage et 8 243 €
#      pour un célibataire avec un jeune enfant en résidence alternée.

    ageV, ageC = age[VOUS], age[CONJ]
    invV, invC = caseP, caseF
    P = _P.ir.abattements_speciaux
    nb_elig_as = (1*(( (ageV>=65) | invV) & (ageV>0)) + 
               1*(( (ageC>=65) | invC) & (ageC>0)) )
    as_inv = nb_elig_as*P.inv_montant*((rng <= P.inv_max1) + ((rng > P.inv_max1)&(rng <= P.inv_max2))*0.5)

    as_enf = nbN*P.enf_montant 

    return min_(rng, as_inv + as_enf)

###############################################################################
## Calcul du nombre de parts
###############################################################################

def _nbptr(nb_pac, marpac, celdiv, veuf, jveuf, nbF, nbG, nbH, nbI, nbR, nbJ, caseP, caseW, caseG, caseE, caseK, caseN, caseF, caseS, caseL, caseT, _P):
    '''
    Nombre de parts du foyer
    'foy'
    note 1 enfants et résidence alternée (formulaire 2041 GV page 10)
    
    P.enf1 : nb part 2 premiers enfants
    P.enf2 : nb part enfants de rang 3 ou plus
    P.inv1 : nb part supp enfants invalides (I, G)
    P.inv2 : nb part supp adultes invalides (R)
    P.not31 : nb part supp note 3 : cases W ou G pour veuf, celib ou div
    P.not32 : nb part supp note 3 : personne seule ayant élevé des enfants
    P.not41 : nb part supp adultes invalides (vous et/ou conjoint) note 4
    P.not42 : nb part supp adultes anciens combattants (vous et/ou conjoint) note 4
    P.not6 : nb part supp note 6
    P.isol : demi-part parent isolé (T)
    P.edcd : enfant issu du mariage avec conjoint décédé;
    '''
    P = _P.ir.quotient_familial
    no_pac  = nb_pac == 0 # Aucune personne à charge en garde exclusive
    has_pac = not_(no_pac)
    no_alt  = nbH == 0 # Aucun enfant à charge en garde alternée
    has_alt = not_(no_alt)
    
    ## nombre de parts liées aux enfants à charge
    # que des enfants en résidence alternée
    enf1 = (no_pac & has_alt)*(P.enf1*min_(nbH,2)*0.5 + P.enf2*max_(nbH-2,0)*0.5)
    # pas que des enfants en résidence alternée
    enf2 = (has_pac & has_alt)*((nb_pac==1)*(P.enf1*min_(nbH,1)*0.5 + P.enf2*max_(nbH-1,0)*0.5) + (nb_pac>1)*(P.enf2*nbH*0.5))
    # pas d'enfant en résidence alternée    
    enf3 = P.enf1*min_(nb_pac,2) + P.enf2*max_((nb_pac-2),0)
    
    enf = enf1 + enf2 + enf3 
    ## note 2 : nombre de parts liées aux invalides (enfant + adulte)
    n2 = P.inv1*(nbG + nbI/2) + P.inv2*nbR 
    
    ## note 3 : Pas de personne à charge
    # - invalide 

    n31a = P.not31a*( no_pac & no_alt & caseP )
    # - ancien combatant 
    n31b = P.not31b*( no_pac & no_alt & ( caseW | caseG ) ) 
    n31 = max_(n31a,n31b)
    # - personne seule ayant élevé des enfants
    n32 = P.not32*( no_pac & no_alt &(( caseE | caseK) & not_(caseN)))
    n3 = max_(n31,n32)
    ## note 4 Invalidité de la personne ou du conjoint pour les mariés ou
    ## jeunes veuf(ve)s
    n4 = max_(P.not41*(1*caseP + 1*caseF), P.not42*(caseW | caseS))
    
    ## note 5
    #  - enfant du conjoint décédé
    n51 =  P.cdcd*(caseL & ((nbF + nbJ)>0))
    #  - enfant autre et parent isolé
    n52 =  P.isol*caseT*( ((no_pac & has_alt)*((nbH==1)*0.5 + (nbH>=2))) + 1*has_pac)
    n5 = max_(n51,n52)
    
    ## note 6 invalide avec personne à charge
    n6 = P.not6*(caseP & (has_pac | has_alt))
    
    ## note 7 Parent isolé
    n7 = P.isol*caseT*((no_pac & has_alt)*((nbH==1)*0.5 + (nbH>=2)) + 1*has_pac)
    
    ## Régime des mariés ou pacsés
    m = 2 + enf + n2 + n4
    
    ## veufs  hors jveuf
    v = 1 + enf + n2 + n3 + n5 + n6
    
    ## celib div
    c = 1 + enf + n2 + n3 + n6 + n7
    return (marpac | jveuf)*m + (veuf & not_(jveuf))*v + celdiv*c
    
###############################################################################
## Calcul de la prime pour l'emploi
###############################################################################

def _ppe_coef(jour_xyz):
    '''
    PPE: coefficient de conversion en cas de changement en cours d'année
    '''
    nb_jour = (jour_xyz==0) + jour_xyz
    return 360/nb_jour

def _ppe_elig(rfr, ppe_coef, marpac, veuf, celdiv, nbptr, _P):
    '''
    PPE: eligibilité à la ppe
    'foy'
    '''
    P = _P.ir.credits_impot.ppe
    seuil = (veuf|celdiv)*(P.eligi1 + 2*max_(nbptr-1,0)*P.eligi3) \
            + marpac*(P.eligi2 + 2*max_(nbptr-2,0)*P.eligi3)
    out = (rfr*ppe_coef) <= seuil
    return out

def _ppe_rev(sal, hsup, rpns, _P):
    '''
    base ressource de la ppe
    'ind'
    '''
    P = _P.ir.credits_impot.ppe
    # Revenu d'activité salarié
    rev_sa = sal + hsup # TODO: + TV + TW + TX + AQ + LZ + VJ
    # Revenu d'activité non salarié
    rev_ns = min_(0,rpns)/P.abatns + max_(0,rpns)*P.abatns
    return rev_sa + rev_ns

def _ppe_coef_tp(ppe_du_sa, ppe_du_ns, ppe_tp_sa, ppe_tp_ns, _P):
    '''
    PPE: coefficient de conversion temps partiel
    'ind'
    '''
    P = _P.ir.credits_impot.ppe
    frac_sa = ppe_du_sa/P.TP_nbh
    frac_ns = ppe_du_ns/P.TP_nbj
    tp = ppe_tp_sa | ppe_tp_ns |(frac_sa + frac_ns >= 1)
    return tp + not_(tp)*(frac_sa + frac_ns)
    
def _ppe_base(ppe_rev, ppe_coef_tp, ppe_coef, _option = {'ppe_coef':ALL} ):
    out = ppe_rev/(ppe_coef_tp + (ppe_coef_tp==0))*ppe_coef
    return out

def _ppe_elig_i(ppe_rev, ppe_coef_tp, _P):
    '''
    eligibilité individuelle à la ppe
    '''
    P = _P.ir.credits_impot.ppe
    return (ppe_rev >= P.seuil1)&(ppe_coef_tp!=0)

def _ppe_brute(ppe_elig, ppe_elig_i, ppe_rev, ppe_base, ppe_coef, ppe_coef_tp, nb_pac, marpac, celdiv, veuf, caseT, caseL, nbH, _P, _option = {'ppe_elig_i': ALL, 'ppe_base': ALL, 'ppe_rev': ALL, 'ppe_coef_tp': ALL}):
    '''
    Prime pour l'emploi (avant éventuel dispositif de cumul avec le RSA)
    'foy'
    '''
    P = _P.ir.credits_impot.ppe

    eliv, elic, eli1, eli2, eli3 = ppe_elig_i[VOUS], ppe_elig_i[CONJ], ppe_elig_i[PAC1], ppe_elig_i[PAC2], ppe_elig_i[PAC3], 
    basevi, baseci = ppe_rev[VOUS], ppe_rev[CONJ]
    basev, basec, base1, base2, base3  = ppe_base[VOUS], ppe_base[CONJ], ppe_base[PAC1], ppe_base[PAC2], ppe_base[PAC1]
    coef_tpv, coef_tpc, coef_tp1, coef_tp2, coef_tp3  = ppe_coef_tp[VOUS], ppe_coef_tp[CONJ], ppe_coef_tp[PAC1], ppe_coef_tp[PAC2], ppe_coef_tp[PAC1]
    
    nb_pac_ppe = max_(0, nb_pac - eli1 - eli2 -eli3 )
        
    ligne2 = marpac & xor_(basevi >= P.seuil1, baseci >= P.seuil1)
    ligne3 = (celdiv | veuf) & caseT & not_(veuf & caseT & caseL)
    ligne1 = not_(ligne2) & not_(ligne3)
    
    base_monact = ligne2*(eliv*basev + elic*basec)
    base_monacti = ligne2*(eliv*basevi + elic*baseci)

    def ppe_bar1(base):
        cond1 = ligne1 | ligne3
        cond2 = ligne2
        return 1/ppe_coef*((cond1 & (base <= P.seuil2))*(base)*P.taux1 +
                           (cond1 & (base> P.seuil2) & (base <= P.seuil3))*(P.seuil3 - base)*P.taux2 +
                           (cond2 & (base <= P.seuil2))*(base*P.taux1 ) +
                           (cond2 & (base >  P.seuil2) & (base <= P.seuil3))*((P.seuil3 - base)*P.taux2) +
                           (cond2 & (base >  P.seuil4) & (base <= P.seuil5))*(P.seuil5 - base)*P.taux3)

    def ppe_bar2(base):
        return 1/ppe_coef*((base <= P.seuil2)*(base)*P.taux1 +
                           ((base> P.seuil2) & (base <= P.seuil3))*(P.seuil3 - base1)*P.taux2 )

    # calcul des primes individuelles.
    ppev = eliv*ppe_bar1(basev)
    ppec = elic*ppe_bar1(basec)
    ppe1 = eli1*ppe_bar2(base1)
    ppe2 = eli2*ppe_bar2(base2)
    ppe3 = eli3*ppe_bar2(base3)
    
    ppe_monact_vous = (eliv & ligne2 & (basevi>=P.seuil1) & (basev <= P.seuil4))*P.monact
    ppe_monact_conj = (elic & ligne2 & (baseci>=P.seuil1) & (basec <= P.seuil4))*P.monact
    
    maj_pac = ppe_elig*(eliv|elic)*(
        (ligne1 & marpac & ((ppev+ppec)!=0) & (min_(basev,basec)<= P.seuil3))*P.pac*(nb_pac_ppe + nbH*0.5) +
        (ligne1 & (celdiv | veuf) & eliv & (basev<=P.seuil3))*P.pac*(nb_pac_ppe + nbH*0.5) +
        (ligne2 & (base_monacti >= P.seuil1) & (base_monact <= P.seuil3))*P.pac*(nb_pac_ppe + nbH*0.5) +
        (ligne2 & (base_monact > P.seuil3) & (base_monact <= P.seuil5))*P.pac*((nb_pac_ppe!=0) + 0.5*((nb_pac_ppe==0) & (nbH!=0))) +
        (ligne3 & (basevi >=P.seuil1) & (basev <= P.seuil3))*((min_(nb_pac_ppe,1)*2*P.pac + max_(nb_pac_ppe-1,0)*P.pac) + (nb_pac_ppe==0)*(min_(nbH,2)*P.pac + max_(nbH-2,0)*P.pac*0.5)) +
        (ligne3 & (basev  > P.seuil3) & (basev <= P.seuil5))*P.pac*((nb_pac_ppe!=0)*2 +((nb_pac_ppe==0) & (nbH!=0))))

    def coef(coef_tp):
        return (coef_tp <=0.5)*coef_tp*1.45 + (coef_tp > 0.5)*(0.55*coef_tp + 0.45)
    
    ppe_vous = ppe_elig*(ppev*coef(coef_tpv) + ppe_monact_vous)
    ppe_conj = ppe_elig*(ppec*coef(coef_tpc) + ppe_monact_conj)
    ppe_pac1 = ppe_elig*(ppe1*coef(coef_tp1))
    ppe_pac2 = ppe_elig*(ppe2*coef(coef_tp2))
    ppe_pac3 = ppe_elig*(ppe3*coef(coef_tp3))
    
    ppe_tot = ppe_vous + ppe_conj + ppe_pac1 + ppe_pac2 + ppe_pac3 +  maj_pac
    ppe_tot = (ppe_tot!=0)*max_(P.versmin, ppe_tot)
    return ppe_tot

def _ppe(ppe_brute, rsa_act_i, _option = {'rsa_act_i': [VOUS, CONJ]} ):
    """
    PPE effectivement versé
    """
#   On retranche le RSA activité de la PPE
#   Dans les agrégats officiels de la DGFP, c'est la PPE brute qu'il faut comparer
    ppe = max_(ppe_brute - rsa_act_i[VOUS] - rsa_act_i[CONJ],0)
    return ppe 
    
