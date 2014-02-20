# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division

from numpy import arange, floor, logical_not as not_
from openfisca_core.statshelpers import mark_weighted_percentiles

from .data import QUIFAM, QUIMEN


CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]

ALL = [x[1] for x in QUIMEN]

def _uc(agem, _option = {'agem': ALL}):
    '''
    Calcule le nombre d'unités de consommation du ménage avec l'échelle de l'insee
    'men'
    '''
    uc_adt = 0.5
    uc_enf = 0.3
    uc = 0.5
    for agm in agem.itervalues():
        age = floor(agm / 12)
        adt = (15 <= age) & (age <= 150)
        enf = (0 <= age) & (age <= 14)
        uc += adt * uc_adt + enf * uc_enf
    return uc

def _typ_men(isol, af_nbenf):
    '''
    type de menage
    'men'
    TODO: prendre les enfants du ménages et non ceux de la famille
    '''
    _0_kid = af_nbenf == 0
    _1_kid = af_nbenf == 1
    _2_kid = af_nbenf == 2
    _3_kid = af_nbenf >= 3

    return (0 * (isol & _0_kid) +  # Célibataire
            1 * (not_(isol) & _0_kid) +  # Couple sans enfants
            2 * (not_(isol) & _1_kid) +  # Couple un enfant
            3 * (not_(isol) & _2_kid) +  # Couple deux enfants
            4 * (not_(isol) & _3_kid) +  # Couple trois enfants et plus
            5 * (isol & _1_kid) +  # Famille monoparentale un enfant
            6 * (isol & _2_kid) +  # Famille monoparentale deux enfants
            7 * (isol & _3_kid))  # Famille monoparentale trois enfants et plus


def _revdisp_i(rev_trav, pen, rev_cap, ir_lps, psoc, ppe, impo):
    '''
    Revenu disponible
    'ind'
    '''
    return rev_trav + pen + rev_cap + ir_lps + psoc + ppe + impo

def _revdisp(revdisp_i, _option = {'revdisp_i': ALL}):
    '''
    Revenu disponible - ménage
    'men'
    '''
    r = 0
    for rev in revdisp_i.itervalues():
        r += rev
    return r

def _nivvie(revdisp, uc):
    '''
    Niveau de vie du ménage
    'men'
    '''
    return revdisp / uc

def _revnet_i(rev_trav, pen, rev_cap):
    '''
    Revenu net individuel
    'ind'
    '''
    return rev_trav + pen + rev_cap

def _revnet(revnet_i, _option = {'revnet_i': ALL}):
    '''
    Revenu net du ménage
    'ind'
    '''
    r = 0
    for rev in revnet_i.itervalues():
        r += rev
    return r

def _nivvie_net(revnet, uc):
    '''
    Niveau de vie net du ménage
    'men'
    '''
    return revnet / uc


def _revini_i(rev_trav, pen, rev_cap, cotpat_contrib, cotsal_contrib):
    '''
    Revenu initial individuel
    'ind'
    '''
    return rev_trav + pen + rev_cap - cotpat_contrib - cotsal_contrib

def _revini(revini_i, _option = {'revini_i': ALL}):
    '''
    Revenu initial du ménage
    'ind'
    '''
    r = 0
    for rev in revini_i.itervalues():
        r += rev
    return r

def _nivvie_ini(revini, uc):
    '''
    Niveau de vie initial du ménage
    'men'
    '''
    return revini / uc

def _revprim_i(rev_trav, cho, rev_cap, cotpat, cotsal):
    '''
    Revenu primaire individuel
    Ensemble des revenus d'activités superbruts avant tout prélèvement
    Il est égale à la valeur ajoutée produite par les résidents
    'ind'
    '''
    return rev_trav + rev_cap - cotpat - cotsal - cho

def _revprim(revprim_i, _option = {'revprim_i': ALL}):
    '''
    Revenu net du ménage
    'ind'
    '''
    r = 0
    for rev in revprim_i.itervalues():
        r += rev
    return r

def _rev_trav(rev_sal, rag, ric, rnc):
    '''
    Revenu du travail
    '''
    return rev_sal + rag + ric + rnc

def _pen(chonet, rstnet, alr, alv, rto):
    '''
    Pensions
    '''
    return chonet + rstnet + alr + alv + rto

def _cotsoc_bar(csg_cap_bar, prelsoc_cap_bar, crds_cap_bar):
    '''
    Cotisations sociales sur les revenus du capital imposés au barème
    '''
    return csg_cap_bar + prelsoc_cap_bar + crds_cap_bar

def _cotsoc_lib(csg_cap_lib, prelsoc_cap_lib, crds_cap_lib):
    '''
    Cotisations sociales sur les revenus du capital soumis au prélèvement libératoire
    '''
    return csg_cap_lib + prelsoc_cap_lib + crds_cap_lib

def _rev_cap(fon, rev_cap_bar, cotsoc_bar, rev_cap_lib, cotsoc_lib, imp_lib, rac):
    '''
    Revenus du patrimoine
    '''
    return fon + rev_cap_bar + cotsoc_bar + rev_cap_lib + cotsoc_lib + imp_lib + rac


def _psoc(pfam, mini, logt):
    '''
    Prestations sociales
    '''
    return pfam + mini + logt

def _pfam(af, cf, ars, aeeh, paje, asf, crds_pfam):
    '''
    Prestations familiales
    '''
    return af + cf + ars + aeeh + paje + asf + crds_pfam

def _mini(aspa, aah, caah, asi, rsa, aefa, api, ass, psa, majo_rsa):
    '''
    Minima sociaux
    '''
    return aspa + aah + caah + asi + rsa + aefa + api + ass + psa + majo_rsa

def _logt(apl, als, alf, crds_lgtm):
    '''
    Prestations logement
    '''
    return apl + als + alf + crds_lgtm

def _impo(irpp, tax_hab):
    '''
    Impôts directs
    '''
    return irpp + tax_hab

def _crds(crdssal, crdsrst, crdscho, crds_fon, crds_cap_bar, crds_cap_lib, crds_pfam, crds_lgtm, crds_mini, crds_pv_mo, crds_pv_immo):
    '''
    Contribution au remboursement de la dette sociale
    '''
    return (crdssal + crdsrst + crdscho +
            crds_fon + crds_cap_bar + crds_cap_lib + crds_pv_mo + crds_pv_immo +
            crds_pfam + crds_lgtm + crds_mini)

def _csg(csgsali, csgsald, csgchoi, csgchod, csgrsti, csgrstd, csg_fon, csg_cap_lib, csg_cap_bar, csg_pv_mo, csg_pv_immo):
    """
    Contribution sociale généralisée
    """
    return (csgsali + csgsald + csgchoi + csgchod + csgrsti + csgrstd +
            csg_fon + csg_cap_lib + csg_pv_mo + csg_pv_immo + csg_cap_bar)


def _cotsoc_noncontrib(cotpat_noncontrib, cotsal_noncontrib):
    '''
    Cotisations sociales non contributives (hors prelsoc_cap_lib, prelsoc_cap_bar)
    '''
    return cotpat_noncontrib + cotsal_noncontrib

def _prelsoc_cap(prelsoc_fon, prelsoc_cap_lib, prelsoc_cap_bar, prelsoc_pv_mo, prelsoc_pv_immo):
    """
    Prélèvements sociaux sur les revenus du capital
    """
    return prelsoc_fon + prelsoc_cap_lib + prelsoc_cap_bar + prelsoc_pv_mo + prelsoc_pv_immo

def _check_csk(prelsoc_cap_bar, prelsoc_pv_mo, prelsoc_fon):
    return prelsoc_cap_bar + prelsoc_pv_mo + prelsoc_fon

def _check_csg(csg_cap_bar, csg_pv_mo, csg_fon):
    return csg_cap_bar + csg_pv_mo + csg_fon

def _check_crds(crds_cap_bar, crds_pv_mo, crds_fon):
    return crds_cap_bar + crds_pv_mo + crds_fon

def _decile(nivvie, champm, wprm):
    '''
    Décile de niveau de vie disponible
    'men'
    '''
    labels = arange(1, 11)
    method = 2
    decile, values = mark_weighted_percentiles(nivvie, labels, wprm * champm, method, return_quantiles = True)
#    print values
#    print len(values)
#    print (nivvie*champm).min()
#    print (nivvie*champm).max()
#    print decile.min()
#    print decile.max()
#    print (nivvie*(decile==1)*champm*wprm).sum()/( ((decile==1)*champm*wprm).sum() )
    del values
    return decile * champm


def _decile_net(nivvie_net, champm, wprm):
    '''
    Décile de niveau de vie net
    'men'
    '''
    labels = arange(1, 11)
    method = 2
    decile, values = mark_weighted_percentiles(nivvie_net, labels, wprm * champm, method, return_quantiles = True)
    return decile * champm


def _pauvre40(nivvie, champm, wprm):
    '''
    Indicatrice de pauvreté à 50% du niveau de vie median
    'men'
    '''
    labels = arange(1, 3)
    method = 2
    percentile, values = mark_weighted_percentiles(nivvie, labels, wprm * champm, method, return_quantiles = True)
    threshold = .4 * values[1]
    return (nivvie <= threshold) * champm


def _pauvre50(nivvie, champm, wprm):
    '''
    Indicatrice de pauvreté à 50% du niveau de vie median
    'men'
    '''
    labels = arange(1, 3)
    method = 2
    percentile, values = mark_weighted_percentiles(nivvie, labels, wprm * champm, method, return_quantiles = True)
    threshold = .5 * values[1]
    return (nivvie <= threshold) * champm

def _pauvre60(nivvie, champm, wprm):
    '''
    Indicatrice de pauvreté à 60% du niveau de vie median
    'men'
    '''
    labels = arange(1, 3)
    method = 2
    percentile, values = mark_weighted_percentiles(nivvie, labels, wprm * champm, method, return_quantiles = True)
    threshold = .6 * values[1]
    return (nivvie <= threshold) * champm

