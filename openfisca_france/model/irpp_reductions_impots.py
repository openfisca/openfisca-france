# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division

import logging

from numpy import minimum as min_, maximum as max_, logical_not as not_
from openfisca_core.accessors import law

from .input_variables.base import QUIFOY


log = logging.getLogger(__name__)
VOUS = QUIFOY['vous']
CONJ = QUIFOY['conj']
PAC1 = QUIFOY['pac1']


def _reductions_2002(ip_net, donapd, dfppce, saldom, cotsyn, prcomp, spfcpi, cappme, intemp,
                invfor, garext, daepad, rsceha, assvie, invrev, domlog, adhcga, ecpess, doment):
    '''
    Renvoie la somme des réductions d'impôt à intégrer pour l'année 2002
    '''
    total_reductions = (donapd + dfppce + saldom + cotsyn + prcomp + spfcpi + cappme + intemp +
                invfor + garext + daepad + rsceha + assvie + invrev + domlog + adhcga + ecpess + doment)
    return min_(ip_net, total_reductions)


def _reductions_2003_2004(ip_net, donapd, dfppce, saldom, cotsyn, prcomp, spfcpi, cappme, intemp,
                repsoc, invfor, garext, daepad, rsceha, assvie, invrev, domlog, adhcga, ecpess, doment):
    '''
    Renvoie la somme des réductions d'impôt à intégrer pour l'année 2003 et 2004
    '''
    total_reductions = (donapd + dfppce + saldom + cotsyn + prcomp + spfcpi + cappme + intemp +
                repsoc + invfor + garext + daepad + rsceha + assvie + invrev + domlog + adhcga + ecpess + doment)
    return min_(ip_net, total_reductions)


def _reductions_2005(ip_net, donapd, dfppce, cotsyn, saldom, intagr, prcomp, spfcpi, cappme,
                intcon, repsoc, invfor, daepad, rsceha, invlst, domlog, adhcga, ecpess, doment):
    '''
    Renvoie la somme des réductions d'impôt à intégrer pour l'année 2005
    '''
    total_reductions = (donapd + dfppce + cotsyn + saldom + intagr + prcomp + spfcpi + cappme +
                intcon + repsoc + invfor + daepad + rsceha + invlst + domlog + adhcga + ecpess + doment)
    return min_(ip_net, total_reductions)


def _reductions_2006(ip_net, donapd, dfppce, cotsyn, saldom, intagr, prcomp, spfcpi, sofica,
                cappme, repsoc, invfor, deffor, daepad, rsceha, invlst, domlog,
                adhcga, ecpess, doment):
    '''
    Renvoie la somme des réductions d'impôt à intégrer pour l'année 2006
    '''
    total_reductions = (donapd + dfppce + cotsyn + saldom + intagr + prcomp + spfcpi + sofica +
                cappme + repsoc + invfor + deffor + daepad + rsceha + invlst + domlog +
                adhcga + ecpess + doment)
    return min_(ip_net, total_reductions)


def _reductions_2007(ip_net, donapd, dfppce, cotsyn, saldom, intagr, prcomp, spfcpi, sofica,
                cappme, repsoc, invfor, deffor, daepad, rsceha, invlst, domlog,
                adhcga, creaen, ecpess, doment):
    '''
    Renvoie la somme des réductions d'impôt à intégrer pour l'année 2007
    '''
    total_reductions = (donapd + dfppce + cotsyn + saldom + intagr + prcomp + spfcpi + sofica +
                cappme + repsoc + invfor + deffor + daepad + rsceha + invlst + domlog +
                adhcga + creaen + ecpess + doment)

    return min_(ip_net, total_reductions)


def _reductions_2008(ip_net, donapd, dfppce, cotsyn, saldom, intagr, prcomp, spfcpi, mohist,
                sofica, cappme, repsoc, invfor, deffor, daepad, rsceha, invlst,
                domlog, adhcga, creaen, ecpess, doment):
    '''
    Renvoie la somme des réductions d'impôt à intégrer pour l'année 2008
    '''
    total_reductions = (donapd + dfppce + cotsyn + saldom + intagr + prcomp + spfcpi + mohist +
                sofica + cappme + repsoc + invfor + deffor + daepad + rsceha + invlst +
                domlog + adhcga + creaen + ecpess + doment)
    return min_(ip_net, total_reductions)


def _reductions_2009(ip_net, donapd, dfppce, cotsyn, resimm, sofipe, ecodev, saldom, intagr,
                prcomp, spfcpi, mohist, sofica, cappme, repsoc, invfor, deffor,
                daepad, rsceha, invlst, domlog, adhcga, creaen, ecpess, scelli,
                locmeu, doment):
    '''
    Renvoie la somme des réductions d'impôt à intégrer pour l'année 2009
    '''
    total_reductions = (donapd + dfppce + cotsyn + resimm + sofipe + ecodev + saldom + intagr +
                prcomp + spfcpi + mohist + sofica + cappme + repsoc + invfor + deffor +
                daepad + rsceha + invlst + domlog + adhcga + creaen + ecpess + scelli +
                locmeu + doment)
    return min_(ip_net, total_reductions)


def _reductions_2010(ip_net, donapd, dfppce, cotsyn, resimm, patnat, sofipe, saldom, intagr,
                prcomp, spfcpi, mohist, sofica, cappme, repsoc, invfor, deffor,
                daepad, rsceha, invlst, domlog, adhcga, creaen, ecpess, scelli,
                locmeu, doment, domsoc):  # TODO: check (sees checked) and report in Niches.xls
    '''
    Renvoie la somme des réductions d'impôt à intégrer pour l'année 2010
    '''
    total_reductions = (donapd + dfppce + cotsyn + resimm + patnat + sofipe + saldom + intagr +
                prcomp + spfcpi + mohist + sofica + cappme + repsoc + invfor + deffor +
                daepad + rsceha + invlst + domlog + adhcga + creaen + ecpess + scelli +
                locmeu + doment + domsoc)  # TODO: check (sees checked) and report in Niches.xls
    return min_(ip_net, total_reductions)


def _reductions_2011(ip_net):
    '''
    Renvoie la somme des réductions d'impôt à intégrer pour l'année 2011
    '''
    total_reductions = ip_net * 0
    return min_(ip_net, total_reductions)


def _reductions_2012(ip_net, donapd, dfppce, cotsyn, resimm, patnat):
    '''
    Renvoie la somme des réductions d'impôt à intégrer pour l'année 2012 TODO: complete
    '''
    total_reductions = ip_net * 0
    return min_(ip_net, total_reductions)


def _reductions_2013(ip_net, donapd, dfppce, cotsyn, resimm, patnat,
                     ecpess, garext, saldom, daepad, rsceha, prcomp, repsoc, intagr,
                     cappme, spfcpi, sofica, adhcga, creaen, deffor, invfor, invlst, scelli,
                     locmeu):
    '''
    Renvoie la somme des réductions d'impôt à intégrer pour l'année 2013
    '''
    total_reductions = (donapd + dfppce + cotsyn + resimm + patnat +
                     ecpess + garext + saldom + daepad + rsceha + prcomp + repsoc + intagr +
                     cappme + spfcpi + sofica + adhcga + creaen + deffor + invfor + invlst + scelli +
                     locmeu)
    return min_(ip_net, total_reductions)
    # TODO: mécénat d'entreprise 7US voir  mecena dans crédits d'impôt
    # TODO Biens culturels       7UO voir  accult dans crédits d'impôt

def _donapd_2002_2010(f7ud, P = law.ir.reductions_impots.donapd):
    '''
    Dons effectués à  des organises d'aide aux personnes en difficulté (2002-2010)
    '''
    return P.taux * min_(f7ud, P.max)

def _donapd_2011_2013(f7ud, f7va, P = law.ir.reductions_impots.donapd):
    '''
    Dons effectués à  des organises d'aide aux personnes en difficulté (2011-2013)
    '''
    return P.taux * min_(f7ud + f7va, P.max)


def _dfppce_2002_2010(rbg_int, f7uf, f7xs, f7xt, f7xu, f7xw, f7xy, _P, P = law.ir.reductions_impots.dfppce):
    '''
    Dons aux autres oeuvres et dons effectués pour le financement des partis
    politiques et des campagnes électorales (2002-2010)
    '''
    base = f7uf
    if _P.datesim.year >= 2004: base += f7xs
    if _P.datesim.year >= 2005: base += f7xt
    if _P.datesim.year >= 2006: base += f7xu
    if _P.datesim.year >= 2007: base += f7xw
    if _P.datesim.year >= 2008: base += f7xy
    max1 = P.max * rbg_int
    return P.taux * min_(base, max1)
    # TODO: note de bas de page
    # TODO: plafonnement pour parti politiques depuis 2012 P.ir.reductions_impots.dfppce.max_niv


def _dfppce_2011_2013(rbg_int, f7uf, f7xs, f7xt, f7xu, f7xw, f7xy, f7vc, P = law.ir.reductions_impots.dfppce):
    '''
    Dons aux autres oeuvres et dons effectués pour le financement des partis
    politiques et des campagnes électorales (2011-2013)
    '''
    base = f7uf + f7vc + f7xs + f7xt + f7xu + f7xw + f7xy
    max1 = P.max * rbg_int
    return P.taux * min_(base, max1)
    # TODO: note de bas de page
    # TODO: plafonnement pour parti politiques depuis 2012 P.ir.reductions_impots.dfppce.max_niv
    #       Introduire plus de détails dans la déclaration pour séparer les dons aux partis poitiques
    #       et aux candidats des autres dons


def _cotsyn(self, f7ac_holder, sal_holder, cho_holder, rst_holder, P = law.ir.reductions_impots.cotsyn):
        # TODO: change f7ac and use split_by_roles
    '''
    Cotisations syndicales (2002-2013)
    '''
    f7ac = self.filter_role(f7ac_holder, role = VOUS)
    f7ae = self.filter_role(f7ac_holder, role = CONJ)
    f7ag = self.filter_role(f7ac_holder, role = PAC1)

    cho = self.split_by_roles(cho_holder)
    rst = self.split_by_roles(rst_holder)
    sal = self.split_by_roles(sal_holder)

    tx = P.seuil

    salv, salc, salp = sal[VOUS], sal[CONJ], sal[PAC1]
    chov, choc, chop = cho[VOUS], cho[CONJ], cho[PAC1]
    rstv, rstc, rstp = rst[VOUS], rst[CONJ], rst[PAC1]
    maxv = (salv + chov + rstv) * tx
    maxc = (salc + choc + rstc) * tx
    maxp = (salp + chop + rstp) * tx

    return P.taux * (min_(f7ac, maxv) + min_(f7ae, maxc) + min_(f7ag, maxp))


def _resimm(f7ra, f7rb, P = law.ir.reductions_impots.resimm):
    '''
    Travaux de restauration immobilière (cases 7RA et 7RB)
    2009-
    '''
    # TODO: add f7rc, f7rd, f7re, f7rf, f7sx, f7sy ... param inserted DONE
    max1 = P.max
    max2 = max_(max1 - f7rb, 0)
    return P.taux_rb * min_(f7rb, max1) + P.taux_ra * min_(f7ra, max2)


def _patnat(f7ka, P = law.ir.reductions_impots.patnat):
    '''
    Dépenses de protections du patrimoine naturel (case 7KA)
    2010-
    '''
    # TODO: add fka, f7kb, f7kc, f7kd ...
    max1 = P.max
    return P.taux * min_(f7ka, max1)

def _sofipe(marpac, rbg_int, f7gs, _P, P = law.ir.reductions_impots.sofipe):
    """
    Souscription au capital d’une SOFIPECHE (case 7GS)
    2009-2011
    """
    if _P.datesim.year >= 2011:
        return rbg_int * 0
    max1 = min_(P.max * (marpac + 1), P.base * rbg_int)  # page3 ligne 18
    return P.taux * min_(f7gs, max1)

def _ecodev(f7uh, rbg_int, P = law.ir.reductions_impots.ecodev):
    '''
    Sommes versées sur un compte épargne codéveloppement (case 7UH)
    2009
    '''
    return min_(f7uh, min_(P.base * rbg_int, P.max))  # page3 ligne 18

def _saldom(nb_pac2, f7db, f7df, f7dg, f7dl, f7dq, _P, P = law.ir.reductions_impots.saldom):
    '''
    Sommes versées pour l'emploi d'un salariés à  domicile
    2002-
    '''
    isinvalid = f7dg

    if _P.datesim.year in (2002, 2003, 2004):
        max1 = P.max1 * not_(isinvalid) + P.max3 * isinvalid
    elif _P.datesim.year in (2005, 2006):
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1
        maxDuMaxNonInv = P.max2
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        max1 = maxNonInv * not_(isinvalid) + P.max3 * isinvalid
    elif _P.datesim.year in (2007, 2008):
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1
        maxDuMaxNonInv = P.max2
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid
        max1 = maxEffectif - min_(f7db, maxEffectif)
    elif 2009 <= _P.datesim.year <= 2013:  
        annee1 = f7dq
        nbpacmin = nb_pac2 + f7dl
        maxBase = P.max1 * not_(annee1) + P.max1_1ereAnnee * annee1
        maxDuMaxNonInv = P.max2 * not_(annee1) + P.max2_1ereAnnee * annee1
        maxNonInv = min_(maxBase + P.pac * nbpacmin, maxDuMaxNonInv)
        maxEffectif = maxNonInv * not_(isinvalid) + P.max3 * isinvalid
        max1 = maxEffectif - min_(f7db, maxEffectif)
    else:
        return f7df * 0
    return P.taux * min_(f7df, max1)


def _intagr(f7um, marpac, P = law.ir.reductions_impots.intagr):
    '''
    Intérêts pour paiement différé accordé aux agriculteurs
    2005-
    '''
    max1 = P.max * (1 + marpac)
    return P.taux * min_(f7um, max1)


def _prcomp(f7wm, f7wn, f7wo, f7wp, P = law.ir.reductions_impots.prcomp):
    '''
    Prestations compensatoires
    2002-
    '''
    div = (f7wo == 0) * 1 + f7wo  # Pour éviter les divisions par zéro

    return ((f7wm == 0) * ((f7wn == f7wo) * P.taux * min_(f7wn, P.seuil) +
                              (f7wn < f7wo) * (f7wo <= P.seuil) * P.taux * f7wn +
                              max_(0, (f7wn < f7wo) * (f7wo > P.seuil) * P.taux * P.seuil * f7wn / div) +
                              P.taux * f7wp) +
            (f7wm != 0) * ((f7wn == f7wm) * (f7wo <= P.seuil) * P.taux * f7wm +
                              max_(0, (f7wn == f7wm) * (f7wo >= P.seuil) * P.taux * f7wm / div) +
                              (f7wn > f7wm) * (f7wo <= P.seuil) * P.taux * f7wn +
                              max_(0, (f7wn > f7wm) * (f7wo >= P.seuil) * P.taux * f7wn / div)) +
             P.taux * f7wp)


def _spfcpi(marpac, f7gq, f7fq, f7fm, f7fl, _P, P = law.ir.reductions_impots.spfcpi):
    '''
    Souscription de parts de fonds communs de placement dans l'innovation,
    de fonds d'investissement de proximité
    2002-
    '''
    max1 = P.max * (marpac + 1)

    if _P.datesim.year <= 2002:
        return P.taux1 * min_(f7gq, max1)
    elif _P.datesim.year <= 2006:
        return (P.taux1 * min_(f7gq, max1) +
                P.taux1 * min_(f7fq, max1))
    elif _P.datesim.year <= 2010:
        return (P.taux1 * min_(f7gq, max1) +
                P.taux1 * min_(f7fq, max1) +
                P.taux2 * min_(f7fm, max1))

    elif _P.datesim.year <= 2013:
        return (P.taux1 * min_(f7gq, max1) +
                P.taux1 * min_(f7fq, max1) +
                P.taux2 * min_(f7fm, max1) +
                P.taux3 * min_(f7fl, max1))
    else:
        return f7gq * 0


def _mohist(f7nz, P = law.ir.reductions_impots.mohist):
    '''
    Travaux de conservation et de restauration d’objets classés monuments historiques (case NZ)
    2008-
    '''
    return P.taux * min_(f7nz, P.max)


def _sofica(f7gn, f7fn, rng, P = law.ir.reductions_impots.sofica):
    '''
    Souscriptions au capital de SOFICA
    2006-
    '''
    max0 = min_(P.taux1 * max_(rng, 0), P.max)
    max1 = min_(0, max0 - f7gn)
    return P.taux2 * min_(f7gn, max0) + P.taux3 * min_(f7fn, max1)


def _cappme(marpac, f7cf, f7cl, f7cm, f7cn, f7cu, _P, P = law.ir.reductions_impots.cappme):
    '''
    Souscriptions au capital des PME
    2002-
    '''
    base = f7cf
    if _P.datesim.year >= 2003: base += f7cl
    if _P.datesim.year >= 2004: base += f7cm
    if _P.datesim.year >= 2005: base += f7cn
    seuil = P.seuil * (marpac + 1)

    if _P.datesim.year <= 2008:
        return P.taux * min_(base, seuil)
    elif _P.datesim.year <= 2010:
        seuil_tpe = P.seuil_tpe * (marpac + 1)
        return P.taux * (min_(base, seuil) + min_(f7cu, seuil_tpe))
    elif _P.datesim.year <= 2011:
        seuil_tpe = P.seuil_tpe * (marpac + 1)
        return P.taux * (min_(base, seuil) + min_(f7cu, seuil_tpe))  # TODO: Modify and add f7cq, check taux
    else:
        return f7cu * 0


def _intemp(nb_pac, f7wg, P = law.ir.reductions_impots.intemp):
    '''
    Intérêts d'emprunts
    2002-2003
    '''
    max1 = P.max + P.pac * nb_pac
    return P.taux * min_(f7wg, max1)


def _intcon(f7uh, P = law.ir.reductions_impots.intcon):
    '''
    Intérêts des prêts à la consommation (case UH)
    2004-2005
    '''
    max1 = P.max
    return P.taux * min_(f7uh, max1)


def _repsoc(marpac, f7fh, P = law.ir.reductions_impots.repsoc):
    '''
    Intérèts d'emprunts pour reprises de société
    2003-
    '''
    seuil = P.seuil * (marpac + 1)
    return P.taux * min_(f7fh, seuil)


def _invfor(marpac, f7un, _P, P = law.ir.reductions_impots.invfor):
    '''
    Investissements forestiers
    '''
    # TODO: 7UN, 7UP, 7UQ, 7UT, 7UU et 7TE
    if _P.datesim.year <= 2002:
        seuil = P.seuil * (marpac + 1)
        return P.taux * min_(f7un, seuil)
    elif _P.datesim.year <= 2008:
        return P.taux * f7un
    else:
        seuil = 0  # TODO vérifier la notice à partir de 2009
        return P.taux * min_(f7un, seuil)


def _garext(f7ga, f7gb, f7gc, f7ge, f7gf, f7gg, P = law.ir.reductions_impots.garext):
    '''
    Frais de garde des enfants à l’extérieur du domicile (cases GA, GB, GC de la 2042)
    et GE, GF, GG
    2002-2005
    '''
    max1 = P.max
    max2 = P.max / 2

    if _P.datesim.year <= 2002:
        return P.taux * (min_(f7ga, max1) +
                       min_(f7gb, max1) +
                       min_(f7gc, max1))
    elif _P.datesim.year <= 2005:
        return P.taux * (min_(f7ga, max1) +
                       min_(f7gb, max1) +
                       min_(f7gc, max1) +
                       min_(f7ge, max2) +
                       min_(f7gf, max2) +
                       min_(f7gg, max2))


def _deffor(f7uc, P = law.ir.reductions_impots.deffor):
    '''
    Défense des forêts contre l'incendie
    2006-
    '''
    return P.taux * min_(f7uc, P.max)


def _daepad(f7cd, f7ce, P = law.ir.reductions_impots.daepad):
    '''
    Dépenses d'accueil dans un établissement pour personnes âgées dépendantes
    ?-
    '''
    return P.taux * (min_(f7cd, P.max) + min_(f7ce, P.max))


def _rsceha(nb_pac2, nbR, f7gz, P = law.ir.reductions_impots.rsceha):
    '''
    Rentes de survie et contrats d'épargne handicap
    2002-
    '''
    max1 = P.seuil1 + (nb_pac2 - nbR) * P.seuil2
    # TODO: verifier la formule précédente
    return P.taux * min_(f7gz, max1)


def _assvie(nb_pac, f7gw, f7gx, f7gy, P = law.ir.reductions_impots.assvie):
    '''
    Assurance-vie (cases GW, GX et GY de la 2042)
    2002-2004
    '''
    max1 = P.max + nb_pac * P.pac
    return P.taux * min_(f7gw + f7gx + f7gy, max1)


def _invrev(marpac, f7gs, f7gt, f7xg, f7gu, f7gv, P = law.ir.reductions_impots.invrev):
    '''
    Investissements locatifs dans les résidences de tourisme situées dans une zone de
    revitalisation rurale (cases GS, GT, XG, GU et GV)
    2002-2003
    TODO 1/4 codé en dur
    '''
    return (P.taux_gs * min_(f7gs, P.seuil_gs * (1 + marpac)) / 4 +
             P.taux_gu * min_(f7gu, P.seuil_gu * (1 + marpac)) / 4 +
             P.taux_xg * min_(f7xg, P.seuil_xg * (1 + marpac)) / 4 +
             P.taux_gt * f7gt + P.taux_gt * f7gv)


def _invlst(marpac, f7xc, f7xd, f7xe, f7xf, f7xg, f7xh, f7xi, f7xj, f7xk, f7xl, f7xm, f7xn, f7xo, _P,
        P = law.ir.reductions_impots.invlst):
    '''
    Investissements locatifs dans le secteur touristique
    2004-
    '''
    seuil1 = P.seuil1 * (1 + marpac)
    seuil2 = P.seuil2 * (1 + marpac)
    seuil3 = P.seuil3 * (1 + marpac)

    if _P.datesim.year == 2011:  # TODO formula and params !!
        return 0 * f7xc

    if _P.datesim.year == 2004: xc = P.taux_xc * min_(f7xc, seuil1 / 4)
    else: xc = P.taux_xc * min_(f7xc, seuil1 / 6)
    xd = P.taux_xd * f7xd
    xe = P.taux_xe * min_(f7xe, seuil1 / 6)
    xf = P.taux_xf * f7xf
    xg = P.taux_xg * min_(f7xg, seuil2)
    xh = P.taux_xh * min_(f7xh, seuil3)
    xi = P.taux_xi * min_(f7xi, seuil1 / 4)
    xj = P.taux_xj * f7xj
    xk = P.taux_xk * f7xk
    xl = P.taux_xl * min_(f7xl, seuil1 / 6)
    xm = P.taux_xm * f7xm
    xn = P.taux_xn * min_(f7xn, seuil1 / 6)
    xo = P.taux_xo * f7xo

    return xc + xd + xe + xf + xg + xh + xi + xj + xk + xl + xm + xn + xo


def _domlog(f7ua, f7ub, f7uc, f7ui, f7uj, f7qb, f7qc, f7qd, f7ql, f7qt, f7qm, _P, P = law.ir.reductions_impots.domlog):
    '''
    Investissements OUTRE-MER dans le secteur du logement et autres secteurs d’activité
    2002-2009
    TODO: Plafonnement sur la notice
    '''
    if _P.datesim.year <= 2002:
        return P.taux1 * f7uj + P.taux2 * (f7uc + f7ub + f7uc)
    elif _P.datesim.year <= 2004:
        return P.taux1 * f7uj + P.taux2 * (f7uc + f7ub + f7uc) + f7ui
    elif _P.datesim.year <= 2007:
        return P.taux1 * f7uj + P.taux2 * (f7uc + f7ub) + f7ui
    elif _P.datesim.year <= 2008:
        return f7ui
    elif _P.datesim.year <= 2009:
        return f7qb + f7qc + f7qd
    elif _P.datesim.year <= 2010:
        return f7qb + f7qc + f7qd + f7ql + f7qt + f7qm


def _adhcga(f7ff, f7fg, P = law.ir.reductions_impots.adhcga):
    '''
    Frais de comptabilité et d'adhésion à un CGA ou AA
    2002-
    '''
    return min_(f7ff, P.max * f7fg)


def _creaen(f7fy, f7gy, f7jy, f7hy, f7ky, f7iy, f7ly, f7my, _P, P = law.ir.reductions_impots.creaen):
    '''
    Aide aux créateurs et repreneurs d'entreprises
    ?-
    '''
    if _P.datesim.year <= 2008:
        return (P.base * f7fy + P.hand * f7gy)
    elif _P.datesim.year == 2009:
        return (P.base * ((f7jy + f7fy) + f7hy / 2) +
                P.hand * ((f7ky + f7gy) + f7iy / 2))
    elif _P.datesim.year >= 2010:
        return (P.base * ((f7jy + f7fy) + (f7hy + f7ly) / 2) +
                P.hand * ((f7ky + f7gy) + (f7iy + f7my) / 2))
    elif _P.datesim.year >= 2012:
        return (P.base * (f7ly / 2) +
                P.hand * (f7my / 2))


def _ecpess(f7ea, f7eb, f7ec, f7ed, f7ef, f7eg, P = law.ir.reductions_impots.ecpess):
    '''
    Réduction d'impôt au titre des enfants à charge poursuivant leurs études secondaires ou supérieures
    '''
    return (P.col * (f7ea + f7eb / 2) +
            P.lyc * (f7ec + f7ed / 2) +
            P.sup * (f7ef + f7eg / 2))


def _scelli(f7hj, f7hk, f7hn, f7ho, f7hl, f7hm, f7hr, f7hs, f7la, _P, P = law.ir.reductions_impots.scelli):
    '''
    Investissements locatif neufs : Dispositif Scellier (cases 7HJ et 7HK)
    2009-2010
    '''
    # TODO: à compléter
    # il est possible de cummuler différents dispositifs scelleir
    # dans la limite d'un seul investissment par an
    # taux1 25%
    # taux2 40%
    if _P.datesim.year == 2009:
        return max_(P.taux1 * min_(P.max, f7hj), P.taux2 * min_(P.max, f7hk)) / 9
    elif _P.datesim.year == 2010:
        return (max_(
            max_(P.taux1 * min_(P.max, f7hj), P.taux2 * min_(P.max, f7hk)),
            max_(P.taux1 * min_(P.max, f7hn), P.taux2 * min_(P.max, f7ho))
                      ) / 9 +
            max_(P.taux1 * min_(P.max, f7hl), P.taux2 * min_(P.max, f7hm)) / 9 +
            max_(f7hr, f7hs) + f7la)


def _locmeu(f7ij, f7il, f7im, f7ik, f7is, P = law.ir.reductions_impots.locmeu):
    '''
    Investissement en vue de la location meublée non professionnelle dans certains établissements ou résidences (case 7IJ)
    2009-
    '''
    return ((max_(min_(P.max, f7ij), min_(P.max, f7il)) + min_(P.max, f7im)) / 9 + f7ik) * P.taux + f7is


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
