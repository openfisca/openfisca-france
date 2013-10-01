# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)

from __future__ import division
from numpy import minimum as min_, maximum as max_

from src.countries.france.model.data import QUIFOY

VOUS = QUIFOY['vous']
CONJ = QUIFOY['conj']
PAC1 = QUIFOY['pac1']
PAC2 = QUIFOY['pac2']
PAC3 = QUIFOY['pac3']
ALL = [x[1] for x in QUIFOY]


def _rfr_cd(cd_acc75a, cd_doment, cd_eparet, cd_sofipe):
    return cd_acc75a + cd_doment + cd_eparet + cd_sofipe

def _cd1(cd_penali, cd_acc75a, cd_percap, cd_deddiv, cd_doment, cd_eparet, cd_grorep, _P):
    '''
    Renvoie la liste des charges déductibles à intégrer en fonction de l'année
    niches1 : niches avant le rbg_int
    niches2 : niches après le rbg_int
    niches3 : indices des niches à ajouter au revenu fiscal de référence
    '''
    if _P.datesim.year in (2002, 2003):
        niches1 = cd_penali + cd_acc75a + cd_percap + cd_deddiv + cd_doment
    elif _P.datesim.year in (2004,2005):
        niches1 = cd_penali + cd_acc75a + cd_percap + cd_deddiv + cd_doment + cd_eparet
    elif _P.datesim.year == 2006:
        niches1 = cd_penali + cd_acc75a + cd_percap + cd_deddiv + cd_eparet
    elif _P.datesim.year in (2007, 2008):
        niches1 = cd_penali + cd_acc75a + cd_deddiv + cd_eparet
    elif _P.datesim.year in (2009, 2010, 2011):
        niches1 = cd_penali + cd_acc75a + cd_deddiv + cd_eparet + cd_grorep
    else:
        niches1 = 0*cd_penali
    return niches1

def _cd2(cd_ecodev, cd_sofipe, cd_cinema, _P):
    '''
    Renvoie la liste des charges déductibles à intégrer en fonction de l'année
    niches1 : niches avant le rbg_int
    niches2 : niches après le rbg_int
    niches3 : indices des niches à ajouter au revenu fiscal de référence
    '''
    if _P.datesim.year in (2002, 2003, 2004, 2005):
        niches2 = cd_sofipe + cd_cinema
    elif _P.datesim.year == 2006:
        niches2 = cd_sofipe
    elif _P.datesim.year in (2007, 2008):
        niches2 = cd_ecodev
    return niches2

def _rbg_int(rbg, cd1):
    return max_(rbg - cd1, 0)

def _charges_deduc_reforme(charge_loyer):
    return charge_loyer

def _charge_loyer(loyer, nbptr, _P, _option = {'loyer': ALL}):
    
    from numpy import logical_not as not_
    plaf = _P.ir.autre.charge_loyer.plaf
    plaf_nbp = _P.ir.autre.charge_loyer.plaf_nbp
    plafond = plaf*(not_(plaf_nbp) + plaf*nbptr*plaf_nbp) 
    return 12*_P.ir.autre.charge_loyer.active*min_(sum(loyer.itervalues()), plafond)


def _charges_deduc(cd1, cd2, charges_deduc_reforme ):
    return cd1 + cd2 + charges_deduc_reforme


def _cd_penali(f6gi, f6gj, f6gp, f6el, f6em, f6gu, _P):
    '''
    Pensions alimentaires
    '''
    P = _P.ir.charges_deductibles.penalim
    max1 = P.max 
    if _P.datesim.year <= 2005:
        # TODO: si vous subvenez seul(e) à l'entretien d'un enfant marié ou 
        # pacsé ou chargé de famille, quel que soit le nmbre d'enfants du jeune 
        # foyer, la déduction est limitée à 2*max
        return (min_(f6gi ,max1) + 
                min_(f6gj, max1) + 
                f6gp)
    else:
        taux = P.taux
        return (min_(f6gi*(1 + taux), max1) + 
                min_(f6gj*(1 + taux), max1) + 
                min_(f6el, max1) + 
                min_(f6em, max1) + 
                f6gp*(1 + taux) + f6gu)

def _cd_acc75a(f6eu, f6ev, _P):
    '''
    Frais d’accueil sous votre toit d’une personne de plus de 75 ans
    '''
    P = _P.ir.charges_deductibles.acc75a
    amax = P.max*max_(1, f6ev)
    return min_(f6eu, amax)

def _cd_percap(f6cb, f6da, marpac, _P):
    '''
    Pertes en capital consécutives à la souscription au capital de sociétés 
    nouvelles ou de sociétés en difficulté (cases CB et DA de la déclaration 
    complémentaire)
    '''
    P = _P.ir.charges_deductibles
    if _P.datesim.year <= 2002:
        max_cb = P.percap.max_cb*(1 + marpac)
        return min_(f6cb, max_cb) 
    elif _P.datesim.year <= 2006:
        max_cb = P.percap.max_cb*(1 + marpac)
        max_da = P.percap.max_da*(1 + marpac)
        return min_(min_(f6cb, max_cb) + min_(f6da, max_da), max_da)

def _cd_deddiv(f6dd):
    '''
    Déductions diverses (case DD)
    '''
    return f6dd

def _cd_doment(f6eh, _P):
    '''
    Investissements DOM-TOM dans le cadre d’une entreprise (case EH de la 
    déclaration n° 2042 complémentaire)
    2002-2005
    '''
    return f6eh

def _cd_eparet(f6ps, f6rs, f6ss, f6pt, f6rt, f6st, f6pu, f6ru, f6su, _P):
    '''
    Épargne retraite - PERP, PRÉFON, COREM et CGOS
    2004-
    '''
    # TODO: En théorie, les plafonds de déductions (ps, pt, pu) sont calculés sur 
    # le formulaire 2041 GX
    return ((f6ps==0)*(f6rs + f6ss) + 
            (f6ps!=0)*min_(f6rs + f6ss, f6ps) +
            (f6pt==0)*(f6rt + f6st) + 
            (f6pt!=0)*min_(f6rt + f6st, f6pt) +
            (f6pu==0)*(f6ru + f6su) + 
            (f6pu!=0)*min_(f6ru + f6su, f6pu))

def _cd_sofipe(f6cc, rbg_int, marpac, _P):
    '''
    Souscriptions au capital des SOFIPÊCHE (case CC de la déclaration 
    complémentaire)
    2002-2006
    '''
    P = _P.ir.charges_deductibles
    max1 = min_(P.sofipe.taux*rbg_int, P.sofipe.max*(1+marpac))
    return min_(f6cc, max1)

def _cd_cinema(f6aa, rbg_int, _P):
    '''
    Souscriptions en faveur du cinéma ou de l’audiovisuel (case AA de la 
    déclaration n° 2042 complémentaire)
    2002-2005
    '''
    P = _P.ir.charges_deductibles
    max1 = min_(P.cinema.taux*rbg_int, P.cinema.max)
    return min_(f6aa, max1)

def _cd_ecodev(f6eh, rbg_int, _P):
    '''
    Versements sur un compte épargne codéveloppement (case EH de la déclaration 
    complémentaire)
    2007-2008
    '''
    P = _P.ir.charges_deductibles
    max1 = min_(P.ecodev.taux*rbg_int, P.ecodev.max)
    return min_(f6eh, max1)

def _cd_grorep(f6cb, f6hj, _P):
    '''
    Dépenses de grosses réparations des nus-propriétaires (case 6CB et 6HJ)
    2009- 
    '''
    P = _P.ir.charges_deductibles
    return min_(f6cb + f6hj, P.grorep.max)
