# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division

import logging

from ..input_variables.base import QUIFOY


log = logging.getLogger(__name__)
VOUS = QUIFOY['vous']


# TODO: CHECK la csg déductible en 2006 est case GH
# TODO:  la revenus soumis aux csg déductible et imposable sont
#        en CG et BH en 2010

# temp = 0
# if hasattr(P, "prelsoc"):
#    for val in P.prelsoc.__dict__.itervalues(): temp += val
#    P.prelsoc.total = temp
# else :
#    P.__dict__.update({"prelsoc": {"total": 0} })
#
# a = {'sal':sal, 'pat':pat, 'csg':csg, 'crds':crds,
#      'exo_fillon': P.cotsoc.exo_fillon, 'lps': P.lps,
#      'ir': P.ir, 'prelsoc': P.prelsoc}
# return Dicts2Object(**a)


def _mhsup(hsup):
    """
    Heures supplémentaires comptées négativement
    """
    return -hsup

############################################################################
# # Revenus du capital
############################################################################


# revenus du capital soumis au barème
def _csg_cap_bar(self, rev_cap_bar, _P):
    '''
    Calcule la CSG sur les revenus du captial soumis au barème
    '''
    return self.cast_from_entity_to_role(-rev_cap_bar * _P.csg.capital.glob,
        entity = 'foyer_fiscal', role = VOUS)


def _crds_cap_bar(self, rev_cap_bar, _P):
    '''
    Calcule la CRDS sur les revenus du capital soumis au barème
    '''
    return self.cast_from_entity_to_role(-rev_cap_bar * _P.crds.capital,
        entity = 'foyer_fiscal', role = VOUS)


def _prelsoc_cap_bar__2005(self, rev_cap_bar, _P):
    '''
    Calcule le prélèvement social sur les revenus du capital soumis au barème
    '''
    P = _P.prelsoc    
    total = P.base_pat
    return self.cast_from_entity_to_role(-rev_cap_bar * total,
        entity = 'foyer_fiscal', role = VOUS)

def _prelsoc_cap_bar_2006_2008(self, rev_cap_bar, _P):
    '''
    Calcule le prélèvement social sur les revenus du capital soumis au barème
    '''
    P = _P.prelsoc
    total = P.base_pat + P.add_pat
    return self.cast_from_entity_to_role(-rev_cap_bar * total,
        entity = 'foyer_fiscal', role = VOUS)

def _prelsoc_cap_bar_2009_(self, rev_cap_bar, _P):
    '''
    Calcule le prélèvement social sur les revenus du capital soumis au barème
    '''
    P = _P.prelsoc    
    total = P.base_pat + P.add_pat + P.rsa
    return self.cast_from_entity_to_role(-rev_cap_bar * total,
        entity = 'foyer_fiscal', role = VOUS)
# plus-values de valeurs mobilières


def _csg_pv_mo(f3vg, _P):
    """
    Calcule la CSG sur les plus-values de cession mobilière
    """
    return -f3vg * _P.csg.capital.glob


def _crds_pv_mo(f3vg, _P):
    """
    Calcule la CRDS sur les plus-values de cession mobilière
    """
    return -f3vg * _P.crds.capital


def _prelsoc_pv_mo__2005(f3vg, _P):
    """
    Calcule le prélèvement social sur les plus-values
    de cession de valeurs mobilières
    """
    P = _P.prelsoc    
    total = P.base_pat
    return -f3vg * total

def _prelsoc_pv_mo_2006_2008(f3vg, _P):
    """
    Calcule le prélèvement social sur les plus-values
    de cession de valeurs mobilières
    """
    P = _P.prelsoc
    total = P.base_pat + P.add_pat
    return -f3vg * total

def _prelsoc_pv_mo_2009_(f3vg, _P):
    """
    Calcule le prélèvement social sur les plus-values
    de cession de valeurs mobilières
    """
    P = _P.prelsoc
    total = P.base_pat + P.add_pat + P.rsa
    return -f3vg * total


# plus-values immobilières

def _csg_pv_immo(f3vz, _P):
    """
    Calcule la CSG sur les plus-values de cession immobilière
    """
    return -f3vz * _P.csg.capital.glob


def _crds_pv_immo(f3vz, _P):
    """
    Calcule la CRDS sur les plus-values de cession immobilière
    """
    return -f3vz * _P.crds.capital


def _prelsoc_pv_immo__2005(f3vz, _P):
    """
    Calcule le prélèvement social sur les plus-values de cession immobilière
    """
    P = _P.prelsoc
    total = P.base_pat
    
    return -f3vz * total

def _prelsoc_pv_immo_2006_2008(f3vz, _P):
    """
    Calcule le prélèvement social sur les plus-values de cession immobilière
    """
    P = _P.prelsoc
    total = P.base_pat + P.add_pat
    
    return -f3vz * total

def _prelsoc_pv_immo_2009_(f3vz, _P):
    """
    Calcule le prélèvement social sur les plus-values de cession immobilière
    """
    P = _P.prelsoc
    total = P.base_pat + P.add_pat + P.rsa
    return -f3vz * total

# revenus fonciers
def _csg_fon(rev_cat_rfon, _P):
    '''
    Calcule la CSG sur les revenus fonciers
    Attention : assiette csg = asiette irpp valable 2006-2014 mais pourrait changer 
    '''
    return -rev_cat_rfon * _P.csg.capital.glob

def _crds_fon(rev_cat_rfon, _P):
    '''
    Calcule la CRDS sur les revenus fonciers
    Attention : assiette csg = asiette irpp valable 2006-2014 mais pourrait changer 
    '''
    return -rev_cat_rfon * _P.crds.capital


def _prelsoc_fon__2005(rev_cat_rfon, _P):
    '''
    Calcule le prélèvement social sur les revenus fonciers
    Attention : assiette csg = asiette irpp valable 2006-2014 mais pourrait changer 
    '''
    P = _P.prelsoc
    total = P.base_pat
    
    return -rev_cat_rfon * total

def _prelsoc_fon_2006_2008(rev_cat_rfon, _P):
    '''
    Calcule le prélèvement social sur les revenus fonciers
    Attention : assiette csg = asiette irpp valable 2006-2014 mais pourrait changer 
    '''
    P = _P.prelsoc
    total = P.base_pat + P.add_pat

    return -rev_cat_rfon * total

def _prelsoc_fon_2009_(rev_cat_rfon, _P):
    '''
    Calcule le prélèvement social sur les revenus fonciers
    Attention : assiette csg = asiette irpp valable 2006-2014 mais pourrait changer 
    '''
    P = _P.prelsoc
    total = P.base_pat + P.add_pat + P.rsa
    return -rev_cat_rfon * total

# revenus du capital soumis au prélèvement libératoire
def _csg_cap_lib(self, rev_cap_lib, _P):
    '''
    Calcule la CSG sur les revenus du capital soumis au prélèvement libératoire
    '''
    return self.cast_from_entity_to_role(-rev_cap_lib * _P.csg.capital.glob,
        entity = 'foyer_fiscal', role = VOUS)


def _crds_cap_lib(self, rev_cap_lib, _P):
    '''
    Calcule la CRDS sur les revenus du capital
    soumis au prélèvement libératoire
    '''
    return self.cast_from_entity_to_role(-rev_cap_lib * _P.crds.capital,
        entity = 'foyer_fiscal', role = VOUS)


def _prelsoc_cap_lib(self, rev_cap_lib, _P):
    '''
    Calcule le prélèvement social sur les revenus du capital
    soumis au prélèvement libératoire
    '''
    P = _P.prelsoc
    if _P.datesim.year < 2006:
        total = P.base_pat
    elif _P.datesim.year < 2009:
        total = P.base_pat + P.add_pat
    else:
        total = P.base_pat + P.add_pat + P.rsa
    return self.cast_from_entity_to_role(-rev_cap_lib * total,
        entity = 'foyer_fiscal', role = VOUS)


# TODO: non_imposabilité pour les revenus au barème
#        verse = (-csgcap_bar - crdscap_bar - prelsoccap_bar) > bareme.csg.capital.nonimp
# #        verse=1
#        # CSG sur les revenus du patrimoine non imposés au barême (contributions sociales déjà prélevées)
#
#        table.setIndiv('csgcap_bar', csgcap_bar*verse)
#        table.setIndiv('prelsoccap_bar', prelsoccap_bar*verse)
#        table.setIndiv('crdscap_bar', crdscap_bar*verse)

