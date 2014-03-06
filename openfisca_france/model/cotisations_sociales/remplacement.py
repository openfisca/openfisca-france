# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division

import logging

from numpy import logical_not as not_, maximum as max_, minimum as min_, ones

from openfisca_core.baremes import BaremeDict, scaleBaremes


log = logging.getLogger(__name__)

# Exonération de CSG et de CRDS sur les revenus du chômage
# et des préretraites si cela abaisse ces revenus sous le smic brut
# TODO: mettre un trigger pour l'éxonération
#       des revenus du chômage sous un smic

############################################################################
# # Allocations chômage
############################################################################


def _csg_rempl(rfr_n_2, nbpt_n_2, chobrut, rstbrut, _P):
    '''
    Taux retenu sur la CSG des revenus de remplacment:
    0 : Non renseigné/non pertinent
    1 : Exonéré  (sous plafond de ressource)
    2 : Taux réduit (irpp < seuil de non versement)
    3 : Taux plein
    '''
    # TODO: problème avec le rfr n-2
    P = _P.cotsoc.gen
    seuil_th = P.plaf_th_1 + P.plaf_th_supp * (max_(0, (nbpt_n_2 - 1) / 2))
    res = (0
           + max_((chobrut > 0) + (rstbrut > 0), 0)  # pertinence la personne est au chômage ou pensionnées
           + (rfr_n_2 >= seuil_th)  # la personne n'ont pas assez de  ressources
           + 1)  # la personne ne satisfait pas à la conditon de ressources mais son impot avant credit > seuil de non imposition
    return res


def exo_csg_chom(chobrut, csg_rempl, _P):
    '''
    Indicatrice d'exonération de la CSG sur les revenus du chômage sans exo
    '''
    chonet_sans_exo = (chobrut
                        + csgchod_sans_exo(chobrut, csg_rempl, _P)
                        + csgchoi_sans_exo(chobrut, csg_rempl, _P)
                        + crdscho_sans_exo(chobrut, csg_rempl, _P))
    nbh_travail = 151.67  # TODO: depuis 2001 mais avant ?
    cho_seuil_exo = _P.csg.chom.min_exo * nbh_travail * _P.cotsoc.gen.smic_h_b
    return (chonet_sans_exo <= 12 * cho_seuil_exo)  # annuel


def csgchod_sans_exo(chobrut, csg_rempl, _P):
    '''
    CSG déductible sur les allocations chômage sans exo
    '''
    plaf_ss = 12 * _P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', _P.csg.chom), plaf_ss)
    taux_plein = csg['plein']['deduc'].calc(chobrut)
    taux_reduit = csg['reduit']['deduc'].calc(chobrut)
    csgchod = (csg_rempl == 2) * taux_reduit + (csg_rempl == 3) * taux_plein
    return -csgchod


def csgchoi_sans_exo(chobrut, csg_rempl, _P):
    '''
    CSG imposable sur les allocations chômage sans exo
    '''
    plaf_ss = 12 * _P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', _P.csg.chom), plaf_ss)
    taux_plein = csg['plein']['impos'].calc(chobrut)
    taux_reduit = csg['reduit']['impos'].calc(chobrut)
    csgchoi = (csg_rempl == 2) * taux_reduit + (csg_rempl == 3) * taux_plein
    return -csgchoi


def crdscho_sans_exo(chobrut, csg_rempl, _P):
    '''
    CRDS sur les allocations chômage sans exo
    '''
    plaf_ss = 12 * _P.cotsoc.gen.plaf_ss
    crds = scaleBaremes(_P.crds.rst, plaf_ss)
    return -crds.calc(chobrut) * (2 <= csg_rempl)


def _csgchod(chobrut, csg_rempl, _P):
    '''
    CSG déductible sur les allocations chômage
    '''
    isexo = exo_csg_chom(chobrut, csg_rempl, _P)
    csgchod = csgchod_sans_exo(chobrut, csg_rempl, _P) * not_(isexo)
    return csgchod


def _csgchoi(chobrut, csg_rempl, _P):
    '''
    CSG imposable sur les allocations chômage
    '''
    isexo = exo_csg_chom(chobrut, csg_rempl, _P)
    csgchoi = csgchoi_sans_exo(chobrut, csg_rempl, _P) * not_(isexo)
    return csgchoi


def _crdscho(chobrut, csg_rempl, _P):
    '''
    CRDS sur les allocations chômage
    '''
    isexo = exo_csg_chom(chobrut, csg_rempl, _P)
    crdscho = crdscho_sans_exo(chobrut, csg_rempl, _P) * not_(isexo)
    return crdscho


def _cho(chobrut, csgchod, _P):
    '''
    Chômage imposable (recalculé)
    '''
    return chobrut + csgchod


def _chonet(cho, csgchoi, crdscho):
    '''
    Chômage net
    '''
    return cho + csgchoi + crdscho


############################################################################
# # Pensions
############################################################################

def _rstbrut(rsti, csg_rempl, _defaultP):
    '''
    Calcule les pensions de retraites brutes à partir des pensions imposables
    '''
    P = _defaultP.csg.retraite
    rst_plein = P.plein.deduc.inverse()
    # TODO: ajouter la non-déductible dans param
    rst_reduit = P.reduit.deduc.inverse()
    rstbrut = ((csg_rempl == 1) * rsti + (csg_rempl == 2) * rst_reduit.calc(rsti)
                + (csg_rempl == 3) * rst_plein.calc(rsti))
    log.info(csg_rempl)
    return rstbrut


def _csgrstd(rstbrut, csg_rempl, _P):
    '''
    CSG déductible sur les retraites
    '''
    plaf_ss = 12 * _P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', _P.csg.retraite), plaf_ss)
    taux_plein = csg['plein']['deduc'].calc(rstbrut)
    taux_reduit = csg['reduit']['deduc'].calc(rstbrut)
    csgrstd = (csg_rempl == 3) * taux_plein + (csg_rempl == 2) * taux_reduit
    return -csgrstd


def _csgrsti(rstbrut, csg_rempl, _P):
    '''
    CSG imposable sur les pensions de retraite
    '''
    plaf_ss = 12 * _P.cotsoc.gen.plaf_ss
    csg = scaleBaremes(BaremeDict('csg', _P.csg.retraite), plaf_ss)
    taux_plein = csg['plein']['impos'].calc(rstbrut)
    taux_reduit = csg['reduit']['impos'].calc(rstbrut)
    csgrsti = (csg_rempl == 3) * taux_plein + (csg_rempl == 2) * taux_reduit
    return -csgrsti


def _crdsrst(rstbrut, csg_rempl, _P):
    '''
    CRDS sur les pensions
    '''
    plaf_ss = 12 * _P.cotsoc.gen.plaf_ss
    crds = scaleBaremes(BaremeDict('crds', _P.crds.rst), plaf_ss)
    isexo = (csg_rempl == 1)
    return -crds['rst'].calc(rstbrut) * not_(isexo)


def _casa(rstbrut, csg_rempl, _P):
    """
    Contribution additionnelle de solidarité et d'autonomie
    """
    return (csg_rempl == 3) * _P.prelsoc.add_ret * rstbrut


def _rst(rstbrut, csgrstd):
    '''
    Calcule les pensions imposables
    '''
    return rstbrut + csgrstd


def _rstnet(rst, csgrsti, crdsrst, casa):
    '''
    Retraites nettes
    '''
    return rst + csgrsti + crdsrst + casa
