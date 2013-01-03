# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)

from __future__ import division
from numpy import  floor, arange, array, where 
from src.countries.france.model.data import QUIMEN

ALL_MEN = [x[1] for x in QUIMEN]
PREF = QUIMEN['pref']
CREF = QUIMEN['cref']
ENFS = [QUIMEN['enf1'], QUIMEN['enf2'], QUIMEN['enf3'], QUIMEN['enf4'], QUIMEN['enf5'], QUIMEN['enf6'], QUIMEN['enf7'], QUIMEN['enf8'], QUIMEN['enf9'], ]

def _nbinde(agem, _option = {'agem' : ALL_MEN}):
    '''
    Number of household members
    'men'
    Values range between 1 and 6 for 6 members or more
    '''
    n1 = 0
    for ind in agem.iterkeys():
        n1 += 1*(floor(agem[ind]) >= 0) 
    
    n2 = where( n1 >=6, 6, n1)
    
    return n2


def _ageq(agem):
    '''
    Calcule la tranche d'âge quinquennal
    moins de 25 ans : 0
    25 à 29 ans     : 1
    30 à 34 ans     : 2
    35 à 39 ans     : 3
    40 à 44 ans     : 4
    45 à 49 ans     : 5
    50 à 54 ans     : 6
    55 à 59 ans     : 7
    60 à 64 ans     : 8
    65 à 69 ans     : 9
    70 à 74 ans     :10
    75 à 79 ans     :11
    80 ans et plus  :12
    'ind'
    '''
    age = floor(agem/12)
    tranche = array([ (age >= ag) for ag in arange(25,5,81) ]).sum(axis=0) 
    return tranche


def _nb_ageq0(agem, _option = {'agem': ALL_MEN}):
    '''
    Calcule le nombre d'individus dans chaque tranche d'âge quinquennal (voir ageq)
    'men'
    '''
    ag1 = 0
    nb  = 0
    for agm in agem.itervalues():   
        age = floor(agm/12) 
        nb   += (ag1 <= age) & (age <= (ag1+4))
    return nb

def _cohab(quimen, _option = {'quimen':[CREF]}):
    '''
    Indicatrice de vie en couple
    'men'
    '''
    return 1 * (quimen[CREF] == 1)

def _act_cpl(activite, cohab, _option = {'activite':[PREF, CREF]}):
    '''
    Nombre d'actifs parmi la personne de référence et son conjoint
    'men'
    '''
    return 1*(activite[PREF] <= 1) + 1*(activite[CREF] <= 1)*cohab

def _act_enf(activite, _option = {'activite': ENFS}):
    '''
    Nombre de membres actifs du ménage autre que la personne de référence ou son conjoint
    'men'
    '''
    res = 0
    for act in activite.itervalues():
        res += 1*(act <= 1) 
    return res
    
    
def _nb_act(act_cpl, act_enf):
    '''
    Nombre de membres actifs du ménage
    'men'
    '''
    return act_cpl + act_enf

def _cplx(typmen15):
#def _cplx(quifam, quimen, _option = {'quifam': ENFS, 'quimen': ENFS}):
    '''
    Indicatrice de ménage complexe
    'men'
    '''
    # ménage complexe si les personnes autres que la personne de référence ou son conjoint
    # ne sont pas enfants
    # TODO problème avec les ENFS qui n'existent pas: leur quifam = 0
    # On contourne en utilisant le fait que leur quimen = 0 également
#    res = 0
#    from itertools import izip
#    for quif, quim in izip(quifam.itervalues(), quimen.itervalues()):         
#        res += 1*(quif <= 1)*(quim != 0)
#    return (res > 0.5)
    # En fait on ne peut pas car on n'a les enfants qu'au sens des allocations familiales ...
    return (typmen15 > 12)
    
def _typmen15(typmen15, nbindebis, cohab, act_cpl, cplx, act_enf):
    '''
    Type de ménage en 15 modalités
    1 Personne seule active
    2 Personne seule inactive
    3 Familles monoparentales, parent actif
    4 Familles monoparentales, parent inactif et au moins un enfant actif
    5 Familles monoparentales, tous inactifs
    6 Couples sans enfant, 1 actif
    7 Couples sans enfant, 2 actifs
    8 Couples sans enfant, tous inactifs
    9 Couples avec enfant, 1 membre du couple actif
    10 Couples avec enfant, 2 membres du couple actif
    11 Couples avec enfant, couple inactif et au moins un enfant actif
    12 Couples avec enfant, tous inactifs
    13 Autres ménages, 1 actif
    14 Autres ménages, 2 actifs ou plus
    15 Autres ménages, tous inactifs
    'men'
    '''
    res = 0 + (cplx == 0 )*(
            1 * ( (nbindebis == 1) & (cohab == 0) & (act_cpl == 1)) + #  Personne seule active 
            2 * ( (nbindebis == 1) & (cohab == 0) & (act_cpl == 0)) + # Personne seule inactive
            3 * ( (nbindebis > 1)  & (cohab == 0) & (act_cpl == 1)) + # Familles monoparentales, parent actif
            4 * ( (nbindebis > 1)  & (cohab == 0) & (act_cpl == 0) & (act_enf >= 1) ) + # Familles monoparentales, parent inactif et au moins un enfant actif
            5 * ( (nbindebis > 1)  & (cohab == 0) & (act_cpl == 0) & (act_enf == 0) ) + # Familles monoparentales, tous inactifs
            6 * ( (nbindebis == 2) & (cohab == 1) & (act_cpl == 1) ) +   # Couples sans enfant, 1 actif
            7 * ( (nbindebis == 2) & (cohab == 1) & (act_cpl == 2) ) +   # Couples sans enfant, 2 actifs
            8 * ( (nbindebis == 2)  & (cohab == 1) & (act_cpl == 0) ) +   # Couples sans enfant, tous inactifs
            9 * ( (nbindebis > 2)  & (cohab == 1) & (act_cpl == 1) ) +   # Couples avec enfant, 1 membre du couple actif
            10 * ( (nbindebis > 2)  & (cohab == 1) & (act_cpl == 2) ) +  # Couples avec enfant, 2 membres du couple actif
            11 * ( (nbindebis > 2)  & (cohab == 1) & (act_cpl == 0) & (act_enf >= 1)) + # Couples avec enfant, couple inactif et au moins un enfant actif
            12 * ( (nbindebis > 2)  & (cohab == 1) & (act_cpl == 0) & (act_enf == 0))  # Couples avec enfant, tous inactifs
                           ) +  (cplx == 1 )*(
            13 * (  ( (act_cpl + act_enf) == 1) ) +      # Autres ménages, 1 actif
            14 * (  ( (act_cpl + act_enf) >  1) ) +     # Autres ménages, 2 actifs ou plus
            15 * (  ( (act_cpl + act_enf) == 0) )  )     # Autres ménages, tous inactifs
    
    ratio = (( (typmen15!=res)).sum())/((typmen15!=0).sum())
    # print ratio  2.7 % d'erreurs enfant non nés et erreur d'enfants  
    return res

