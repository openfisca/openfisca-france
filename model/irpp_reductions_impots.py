# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division
from numpy import minimum as min_, maximum as max_, zeros, logical_not as not_
from src.countries.france.model.data import QUIFOY 

VOUS = QUIFOY['vous']
CONJ = QUIFOY['conj']
PAC1 = QUIFOY['pac1']
ALL = []
for qui in QUIFOY:
    ALL.append(qui[1])

taille = 0

def _reductions(ip_net, donapd, dfppce, cotsyn, resimm, patnat, sofipe, saldom, intagr, 
               prcomp, spfcpi, mohist, sofica, cappme, repsoc, invfor, deffor, 
               daepad, rsceha, invlst, domlog, adhcga, creaen, ecpess, scelli, 
               locmeu, doment, domsoc, intemp, garext, assvie, invrev, intcon,
               ecodev, _P):
    '''
    Renvoie la liste des réductions d'impôt à intégrer en fonction de l'année
    '''
    if   _P.datesim.year == 2002:
        total = (donapd + dfppce + saldom + cotsyn + prcomp + spfcpi + cappme + intemp + 
                invfor + garext + daepad + rsceha + assvie + invrev + domlog + adhcga + 
                ecpess + doment)
    elif _P.datesim.year == 2003:
        total = (donapd + dfppce + saldom + cotsyn + prcomp + spfcpi + cappme + intemp + 
                repsoc + invfor + garext + daepad + rsceha + assvie + invrev + domlog + 
                adhcga + ecpess + doment)
    elif _P.datesim.year == 2004:
        total = (donapd + dfppce + saldom + cotsyn + prcomp + spfcpi + cappme + intcon + 
                repsoc + invfor + garext + daepad + rsceha + assvie + invlst + domlog + 
                adhcga + ecpess + doment)
    elif _P.datesim.year == 2005:
        total = (donapd + dfppce + cotsyn + saldom + intagr + prcomp + spfcpi + cappme + 
                intcon + repsoc + invfor + daepad + rsceha + invlst + domlog + adhcga + 
                ecpess + doment)
    elif _P.datesim.year == 2006:
        total = (donapd + dfppce + cotsyn + saldom + intagr + prcomp + spfcpi + sofica + 
                cappme + repsoc + invfor + deffor + daepad + rsceha + invlst + domlog + 
                adhcga + ecpess + doment)
    elif _P.datesim.year == 2007:
        total = (donapd + dfppce + cotsyn + saldom + intagr + prcomp + spfcpi + sofica + 
                cappme + repsoc + invfor + deffor + daepad + rsceha + invlst + domlog + 
                adhcga + creaen + ecpess + doment)
    elif _P.datesim.year == 2008:
        total = (donapd + dfppce + cotsyn + saldom + intagr + prcomp + spfcpi + mohist + 
                sofica + cappme + repsoc + invfor + deffor + daepad + rsceha + invlst + 
                domlog + adhcga + creaen + ecpess + doment)
    elif _P.datesim.year == 2009:
        total = (donapd + dfppce + cotsyn + resimm + sofipe + ecodev + saldom + intagr + 
                prcomp + spfcpi + mohist + sofica + cappme + repsoc + invfor + deffor + 
                daepad + rsceha + invlst + domlog + adhcga + creaen + ecpess + scelli + 
                locmeu + doment)
    elif _P.datesim.year == 2010:
        total = (donapd + dfppce + cotsyn + resimm + patnat + sofipe + saldom + intagr + 
                prcomp + spfcpi + mohist + sofica + cappme + repsoc + invfor + deffor + 
                daepad + rsceha + invlst + domlog + adhcga + creaen + ecpess + scelli + 
                locmeu + doment + domsoc) # TODO check (sees checked) and report in Niches.xls         
    elif _P.datesim.year == 2011:
        total = (donapd + dfppce + cotsyn + resimm + patnat + sofipe + saldom + intagr + 
                prcomp + spfcpi + mohist + sofica + cappme + repsoc + invfor + deffor + 
                daepad + rsceha + invlst + domlog + adhcga + creaen + ecpess + scelli + 
                locmeu + doment + domsoc)   # TODO Check because totally uncecked
        
    return min_(ip_net,total)    

def _donapd(f7ud, _P):
    '''
    Dons effectués à  des organises d'aide aux personnes en difficulté
    2002-
    '''
    P = _P.ir.reductions_impots.donapd

    return P.taux*min_(f7ud, P.max)

def _dfppce(rbg_int, f7uf, f7xs, f7xt, f7xu, f7xw, f7xy, _P):   
    '''
    Dons aux autres oeuvres et dons effectués pour le financement des partis
    politiques et des compagnes électorales
    2002-
    '''
    P = _P.ir.reductions_impots.dfppce
    base = f7uf
    if _P.datesim.year >= 2004: base += f7xs
    if _P.datesim.year >= 2005: base += f7xt
    if _P.datesim.year >= 2006: base += f7xu
    if _P.datesim.year >= 2007: base += f7xw
    if _P.datesim.year >= 2008: base += f7xy
    max1 = P.max*rbg_int
    return P.taux*min_(base, max1)
    # TODO: note de bas de page

def _cotsyn(f7ac, f7ae, f7ag, sal, cho, rst, _P, _option= {'sal':ALL, 'cho':ALL, 'rst':ALL}):
    '''
    Cotisations syndicales
    2002-
    '''
    P = _P.ir.reductions_impots.cotsyn
    tx = P.seuil
    
    salv, salc, salp = sal[VOUS], sal[CONJ], sal[PAC1]
    chov, choc, chop = cho[VOUS], cho[CONJ], cho[PAC1]
    rstv, rstc, rstp = rst[VOUS], rst[CONJ], rst[PAC1]
    maxv = (salv+chov+rstv)*tx
    maxc = (salc+choc+rstc)*tx
    maxp = (salp+chop+rstp)*tx
    
    return P.taux*(min_(f7ac,maxv)  + min_(f7ae,maxc) + min_(f7ag,maxp))

def _resimm(f7ra, f7rb, _P):
    '''
    Travaux de restauration immobilière (cases 7RA et 7RB)
    2009-
    '''
    P = _P.ir.reductions_impots.resimm
    max1 = P.max
    max2 = max_(max1 - f7rb, 0)
    return P.taux_rb*min_(f7rb, max1)+ P.taux_ra*min_(f7ra, max2)

def _patnat(f7ka, _P):
    '''
    Dépenses de protections du patrimoine naturel (case 7KA)
    2010-
    '''
    P = _P.ir.reductions_impots.patnat
    max1 = P.max
    return P.taux*min_(f7ka, max1)

def _sofipe(marpac, rbg_int, f7gs, _P):
    '''
    Souscription au capital d’une SOFIPECHE (case 7GS)
    2009-
    '''
    P = _P.ir.reductions_impots.sofipe
    max1 = min_(P.max*(marpac+1), P.base*rbg_int) # page3 ligne 18
    return P.taux*min_(f7gs, max1)

def _ecodev(f7uh, rbg_int, _P):
    '''
    Sommes versées sur un compte épargne codéveloppement (case 7UH)
    2009
    '''
    P = _P.ir.reductions_impots.ecodev
    return min_(f7uh, min_(P.base*rbg_int, P.max)) # page3 ligne 18

def _saldom(nb_pac2, f7db, f7df, f7dg, f7dl, f7dq, _P):
    '''
    Sommes versées pour l'emploi d'un salariés à  domicile
    2002-
    En 2006 : Le plafond des dépenses ouvrant droit à réduction d’impôt est de
    12 000 € majoré de 1 500 € par enfant mineur compté à charge (750 €
    si l’enfant est en résidence alternée), par enfant rattaché (que le rattachement
    prenne la forme d’une majoration du quotient familial ou d’un
    abattement), par membre du foyer fiscal âgé de plus de 65 ans ou par
    ascendant âgé de plus de 65 ans bénéficiant de l’APA lorsque vous supportez
    personnellement les frais au titre de l’emploi d’un salarié travaillant
    chez l’ascendant. Ce plafond ne peut excéder 15 000 €. Le plafond
    est de 20 000 € si un membre de votre foyer fiscal est titulaire de
    la carte d’invalidité d’au moins 80 % ou d’une pension d’invalidité de 3e
    catégorie ou si vous percevez un complément d’allocation d’éducation
    spéciale pour l’un de vos enfants à charge.
    '''
    P = _P.ir.reductions_impots.saldom
    
    isinvalid = f7dg
    
    if _P.datesim.year in (2002, 2003, 2004):
        max1 = P.max1*not_(isinvalid) + P.max3*isinvalid
    elif _P.datesim.year in (2005,2006):
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1
        maxDuMaxNonInv = P.max2
        maxNonInv = min_(maxBase + P.pac*nbpacmin, maxDuMaxNonInv)
        max1 = maxNonInv*not_(isinvalid) + P.max3*isinvalid
                 
    elif _P.datesim.year in (2007,2008):
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1
        maxDuMaxNonInv = P.max2
        maxNonInv = min_(maxBase + P.pac*nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv*not_(isinvalid) + P.max3*isinvalid
        max1 = maxEffectif - min_(f7db, maxEffectif)
            
    elif _P.datesim.year in (2009, 2010, 2011):  # TODO Check 2011
        annee1 = f7dq
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1*not_(annee1) + P.max1_1ereAnnee*annee1
        maxDuMaxNonInv = P.max2*not_(annee1) + P.max2_1ereAnnee*annee1
        maxNonInv = min_(maxBase + P.pac*nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv*not_(isinvalid) + P.max3*isinvalid
        max1 = maxEffectif - min_(f7db, maxEffectif)
                
    return P.taux*min_(f7df, max1)

def _intagr(f7um, marpac, _P):
    '''
    Intérêts pour paiement différé accordé aux agriculteurs
    2005-
    '''
    P = _P.ir.reductions_impots.intagr
    max1 = P.max*(1+marpac)
    return P.taux*min_(f7um, max1)

def _prcomp(f7wm, f7wn, f7wo, f7wp, _P):
    '''
    Prestations compensatoires
    2002-2010
    '''
    P = _P.ir.reductions_impots.prcomp
    div = (f7wo==0)*1 + f7wo # Pour éviter les divisions par zéro
    
    return ((f7wm == 0)*((f7wn==f7wo)*P.taux*min_(f7wn,P.seuil) +
                              (f7wn<f7wo)*(f7wo<=P.seuil)*P.taux*f7wn +
                              max_(0,(f7wn<f7wo)*(f7wo> P.seuil)*P.taux*P.seuil*f7wn/div) +
                              P.taux*f7wp ) +
            (f7wm != 0)*((f7wn==f7wm)*(f7wo<=P.seuil)*P.taux*f7wm + 
                              max_(0,(f7wn==f7wm)*(f7wo>=P.seuil)*P.taux*f7wm/div) + 
                              (f7wn>f7wm)*(f7wo<=P.seuil)*P.taux*f7wn  + 
                              max_(0,(f7wn>f7wm)*(f7wo>=P.seuil)*P.taux*f7wn/div)) +
             P.taux*f7wp)

def _spfcpi(marpac, f7gq, f7fq, f7fm, f7fl, _P):
    '''
    Souscription de parts de fonds communs de placement dans l'innovation, 
    de fonds d'investissement de proximité
    2002-
    '''
    P = _P.ir.reductions_impots.spfcpi
    max1 = P.max*(marpac+1)

    if _P.datesim.year <= 2002:
        return P.taux1*min_(f7gq, max1)
    elif _P.datesim.year <= 2006:
        return (P.taux1*min_(f7gq, max1) + 
                P.taux1*min_(f7fq, max1) )
    elif _P.datesim.year <= 2010:
        return (P.taux1*min_(f7gq, max1) + 
                P.taux1*min_(f7fq, max1) +
                P.taux2*min_(f7fm, max1) )

    elif _P.datesim.year <= 2011:
        return (P.taux1*min_(f7gq, max1) + 
                P.taux1*min_(f7fq, max1) +
                P.taux2*min_(f7fm, max1) +
                P.taux3*min_(f7fl, max1))


def _mohist(f7nz, _P):
    '''
    Travaux de conservation et de restauration d’objets classés monuments historiques (case NZ)
    2008-
    '''
    P = _P.ir.reductions_impots.mohist
    return P.taux*min_(f7nz, P.max)

def _sofica(f7gn, f7fn, rng, _P):
    '''
    Souscriptions au capital de SOFICA
    2006-
    '''
    P = _P.ir.reductions_impots.sofica
    
    max0 = min_(P.taux1*max_(rng,0), P.max)
    max1 = min_(0, max0 - f7gn)
    return P.taux2*min_(f7gn, max0) + P.taux3*min_(f7fn, max1)

def _cappme(marpac, f7cf, f7cl, f7cm, f7cn, f7cu, _P):
    '''
    Souscriptions au capital des PME
    2002-
    '''
    P = _P.ir.reductions_impots.cappme
    base = f7cf
    if _P.datesim.year >= 2003: base += f7cl
    if _P.datesim.year >= 2004: base += f7cm
    if _P.datesim.year >= 2005: base += f7cn
    seuil = P.seuil*(marpac + 1)

    if _P.datesim.year <= 2008:
        return P.taux*min_(base,seuil)
    elif _P.datesim.year <= 2010:
        seuil_tpe = P.seuil_tpe*(marpac + 1)
        return P.taux*(min_(base,seuil)+min_(f7cu, seuil_tpe))
    elif _P.datesim.year <= 2011:
        seuil_tpe = P.seuil_tpe*(marpac + 1)
        return P.taux*(min_(base,seuil)+min_(f7cu, seuil_tpe))  # TODO Modify and add f7cq
    

def _intemp(nb_pac, f7wg, _P):
    '''
    Intérêts d'emprunts
    2002-2003
    '''
    P = _P.ir.reductions_impots.intemp
    max1 = P.max + P.pac*nb_pac
    return P.taux*min_(f7wg, max1)

def _intcon(f7uh, _P):
    '''
    Intérêts des prêts à la consommation (case UH)
    2004-2005
    '''
    P = _P.ir.reductions_impots.intcon
    max1 = P.max
    return P.taux*min_(f7uh, max1)

def _repsoc(marpac, f7fh, _P):
    '''
    Intérèts d'emprunts pour reprises de société
    2003-
    '''
    P = _P.ir.reductions_impots.repsoc
    seuil = P.seuil*(marpac+1)
    return P.taux*min_(f7fh, seuil)
    
def _invfor(marpac, f7un, _P):
    '''
    Investissements forestiers
    '''
    P = _P.ir.reductions_impots.invfor
    if _P.datesim.year <= 2002:
        seuil = P.seuil*(marpac + 1)
        return P.taux*min_(f7un, seuil)
    elif _P.datesim.year <= 2008:
        return P.taux*f7un
    else:
        seuil = 0 # TODO vérifier la notice à partir de 2009
        return P.taux*min_(f7un, seuil) 

def _garext(f7ga, f7gb, f7gc, f7ge, f7gf, f7gg, _P):
    '''
    Frais de garde des enfants à l’extérieur du domicile (cases GA, GB, GC de la 2042)
    et GE, GF, GG
    2002-2005
    '''
    P = _P.ir.reductions_impots.garext
    max1 = P.max
    max2 = P.max/2
    
    if _P.datesim.year <= 2002:
        return P.taux*(min_(f7ga, max1) + 
                       min_(f7gb, max1) + 
                       min_(f7gc, max1) )
    elif _P.datesim.year <= 2005:
        return P.taux*(min_(f7ga, max1) + 
                       min_(f7gb, max1) + 
                       min_(f7gc, max1) + 
                       min_(f7ge, max2) + 
                       min_(f7gf, max2) + 
                       min_(f7gg, max2) )

def _deffor(f7uc, _P):
    '''
    Défense des forêts contre l'incendie
    2006-
    '''
    P = _P.ir.reductions_impots.deffor
    return P.taux*min_(f7uc, P.max)
    
def _daepad(f7cd, f7ce, _P):
    '''
    Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
    '''
    P = _P.ir.reductions_impots.daepad
    return P.taux*(min_(f7cd, P.max) + min_(f7ce, P.max))

def _rsceha(nb_pac2, nbR, f7gz, _P):
    '''
    Rentes de survie et contrats d'épargne handicap
    2002-
    '''
    P = _P.ir.reductions_impots.rsceha
    max1 = P.seuil1 + (nb_pac2 - nbR)*P.seuil2
    # TODO: verifier la formule précédente
    return P.taux*min_(f7gz, max1)

def _assvie(nb_pac, f7gw, f7gx, f7gy, _P):
    '''
    Assurance-vie (cases GW, GX et GY de la 2042)
    2002-2004
    '''
    P = _P.ir.reductions_impots.assvie
    max1 = P.max + nb_pac*P.pac
    return P.taux*min_(f7gw + f7gx + f7gy, max1)

def _invrev(marpac, f7gs, f7gt, f7xg, f7gu, f7gv, _P):
    '''
    Investissements locatifs dans les résidences de tourisme situées dans une zone de 
    revitalisation rurale (cases GS, GT, XG, GU et GV)
    2002-2003
    TODO 1/4 codé en dur
    '''
    P = _P.ir.reductions_impots.invrev
    return ( P.taux_gs*min_(f7gs, P.seuil_gs*(1+marpac))/4 +
             P.taux_gu*min_(f7gu, P.seuil_gu*(1+marpac))/4 +
             P.taux_xg*min_(f7xg, P.seuil_xg*(1+marpac))/4 +
             P.taux_gt*f7gt + P.taux_gt*f7gv )

def _invlst(marpac, f7xc, f7xd, f7xe, f7xf, f7xg, f7xh, f7xi, f7xj, f7xk, f7xl, f7xm, f7xn, f7xo, _P):
    '''
    Investissements locatifs dans le secteur de touristique
    2004-
    '''
    P = _P.ir.reductions_impots.invlst
    seuil1 = P.seuil1*(1+marpac)
    seuil2 = P.seuil2*(1+marpac)
    seuil3 = P.seuil3*(1+marpac)
 
    if _P.datesim.year == 2011:  # TODO formula and params !!
        return 0*f7xc
 
    
    if _P.datesim.year == 2004: xc = P.taux_xc*min_(f7xc,seuil1/4)
    else: xc = P.taux_xc*min_(f7xc, seuil1/6)
    xd = P.taux_xd*f7xd
    xe = P.taux_xe*min_(f7xe,seuil1/6)
    xf = P.taux_xf*f7xf
    xg = P.taux_xg*min_(f7xg,seuil2)
    xh = P.taux_xh*min_(f7xh, seuil3)
    xi = P.taux_xi*min_(f7xi, seuil1/4)
    xj = P.taux_xj*f7xj
    xk = P.taux_xk*f7xk
    xl = P.taux_xl*min_(f7xl, seuil1/6)
    xm = P.taux_xm*f7xm
    xn = P.taux_xn*min_(f7xn,seuil1/6)
    xo = P.taux_xo*f7xo
    
    return xc + xd + xe + xf + xg + xh + xi + xj + xk + xl + xm + xn + xo
    
def _domlog(f7ua, f7ub, f7uc, f7ui, f7uj, f7qb, f7qc, f7qd, f7ql, f7qt, f7qm, _P):
    '''
    Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
    2002-2009
    TODO: Plafonnement sur la notice
    '''
    if _P.datesim.year <=2007:
        P = _P.ir.reductions_impots.domlog
    if _P.datesim.year <= 2002:
        return P.taux1*f7uj + P.taux2*(f7uc + f7ub + f7uc) 
    elif _P.datesim.year <= 2004:
        return P.taux1*f7uj + P.taux2*(f7uc + f7ub + f7uc) + f7ui
    elif _P.datesim.year <= 2007:
        return P.taux1*f7uj + P.taux2*(f7uc + f7ub) + f7ui
    elif _P.datesim.year <= 2008:
        return f7ui
    elif _P.datesim.year <= 2009:
        return f7qb + f7qc + f7qd
    elif _P.datesim.year <= 2010:        
        return f7qb + f7qc + f7qd + f7ql + f7qt + f7qm
 
def _adhcga(f7ff, f7fg, _P):
    '''
    Frais de comptabilité et d'adhésion à un CGA ou AA
    2002-
    '''
    P = _P.ir.reductions_impots.adhcga

    return min_(f7ff, P.max*f7fg)

def _creaen(f7fy, f7gy, f7jy, f7hy, f7ky, f7iy, f7ly, f7my, _P):
    '''
    Aide aux créateurs et repreneurs d'entreprises
    TODO...
    '''
    P = _P.ir.reductions_impots.creaen
    if _P.datesim.year <= 2008:
        return (P.base*f7fy + P.hand*f7gy )
    elif _P.datesim.year == 2009:
        return (P.base*((f7jy + f7fy) + f7hy/2) +
                P.hand*((f7ky + f7gy) + f7iy/2) )
    elif _P.datesim.year >= 2010:
        return (P.base*((f7jy + f7fy) + (f7hy + f7ly)/2) +
                P.hand*((f7ky + f7gy) + (f7iy + f7my)/2) )

        
def _ecpess(f7ea, f7eb, f7ec, f7ed, f7ef, f7eg, _P):
    '''
    Réduction d'impôt au titre des enfants à charge poursuivant leurs études secondaires ou supérieures
    '''
    P = _P.ir.reductions_impots.ecpess
    return (P.col*(f7ea + f7eb/2) +
            P.lyc*(f7ec + f7ed/2) +
            P.sup*(f7ef + f7eg/2) )

def _scelli(f7hj, f7hk, f7hn, f7ho, f7hl, f7hm, f7hr, f7hs, f7la, _P):
    '''
    Investissements locatif neufs : Dispositif Scellier (cases 7HJ et 7HK)
    2009-2010
    '''
    # il est possible de cummuler différents dispositifs scelleir 
    # dans la limite d'un seul investissment par an
    P = _P.ir.reductions_impots.scelli
    # taux1 25%
    # taux2 40%
    if _P.datesim.year == 2009:
        return max_(P.taux1*min_(P.max,f7hj), P.taux2*min_(P.max,f7hk))/9
    elif _P.datesim.year == 2010:
        return ( max_(
            max_(P.taux1*min_(P.max,f7hj), P.taux2*min_(P.max,f7hk)),
            max_(P.taux1*min_(P.max,f7hn), P.taux2*min_(P.max,f7ho))   
                      )/9 +
            max_(P.taux1*min_(P.max,f7hl), P.taux2*min_(P.max,f7hm))/9 +
            max_(f7hr,f7hs) + f7la )

def _locmeu(f7ij, f7il, f7im, f7ik, f7is, _P):
    '''
    Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences (case 7IJ)
    2009-
    '''
    P = _P.ir.reductions_impots.locmeu
    return ( (max_(min_(P.max,f7ij), min_(P.max,f7il)) + min_(P.max,f7im))/9 + f7ik)*P.taux + f7is
    
def _doment(f7ur, f7oz, f7pz, f7qz, f7rz, f7sz):
    '''
    Investissements dans les DOM-TOM dans le cadre d'une entrepise.
    '''
    return  f7ur + f7oz + f7pz + f7qz + f7rz + f7sz

def _domsoc(f7qb, f7qc, f7ql, f7qt, f7qm, f7qd):
    '''
    Investissements outre-mer dans le logement social (déclaration n°2042 IOM)
    2010-
    TODO plafonnement à 15% f7qa / liens avec autres investissments ?
    '''
    return  f7qb + f7qc + f7ql + f7qt + f7qm + f7qd
