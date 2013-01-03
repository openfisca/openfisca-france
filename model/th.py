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

from src.countries.france.model.data import QUIMEN

CHEF = QUIMEN['pref']
PART = QUIMEN['cref']
ENFS = [QUIMEN['enf1'], QUIMEN['enf2'], QUIMEN['enf3'], QUIMEN['enf4'], QUIMEN['enf5'], QUIMEN['enf6'], QUIMEN['enf7'], QUIMEN['enf8'], QUIMEN['enf9'], ]

ALL = [x[1] for x in QUIMEN]
        

def _tax_hab(zthabm, aah, aspa, asi, age, isf_tot, rfr, statmarit, nbptr, _P):
    '''
    Taxe d'habitation
    'men'
    '''
    P = _P.cotsoc.gen
    # Eligibilité:
    # - âgé de plus de 60 ans, non soumis à l'impôt de solidarité sur la fortune (ISF) en n-1
    # - veuf quel que soit votre âge et non soumis à l'impôt de solidarité sur la fortune (ISF) n-1
    # - titulaire de l'allocation de solidarité aux personnes âgées (Aspa)  ou de l'allocation supplémentaire d'invalidité (Asi),  
    # bénéficiaire de l'allocation aux adultes handicapés (AAH),  
    # atteint d'une infirmité ou d'une invalidité vous empêchant de subvenir à vos besoins par votre travail.
    concern = ((age >= 60) + (statmarit == 4))*(isf_tot  <= 0)  + (aspa > 0) + (asi > 0)
    
    seuil_th = P.plaf_th_1 + P.plaf_th_supp*(max_(0, (nbptr-1)/2))
    
    elig = concern*(rfr < seuil_th) + (asi > 0)  + (aspa > 0)
    
    return -zthabm*(elig)