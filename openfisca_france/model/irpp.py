# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division

import logging

from numpy import (datetime64, int16, logical_and as and_, logical_not as not_, logical_or as or_, logical_xor as xor_,
    maximum as max_, minimum as min_, round)
from openfisca_core.accessors import law

from .input_variables.base import QUIFOY


CONJ = QUIFOY['conj']
log = logging.getLogger(__name__)
PAC1 = QUIFOY['pac1']
PAC2 = QUIFOY['pac2']
PAC3 = QUIFOY['pac3']
VOUS = QUIFOY['vous']


# zetrf = zeros(taille)
# jveuf = zeros(taille, dtype = bool)
# Reprise du crédit d'impôt en faveur des jeunes, des accomptes et des versements mensues de prime pour l'emploi
# reprise = zeros(taille) # TODO : reprise=J80
# Pcredit = P.credits_impots
# if hasattr(P.reductions_impots,'saldom'): Pcredit.saldom =  P.reductions_impots.saldom
# credits_impot = Credits(Pcredit, table)
# Réduction d'impôt
# reductions = Reductions(IPnet, P.reductions_impots)

# def mcirra():
#    # impôt sur le revenu
#    mcirra = -((IMP<=-8)*IMP)
#    mciria = max_(0,(IMP>=0)*IMP)
# #        mciria = max_(0,(IMP>=0)*IMP - credimp_etranger - cont_rev_loc - ( f8to + f8tb + f8tc ))
#
#    # Dans l'ERFS, les prelevement libératoire sur les montants non déclarés
#    # sont intégrés. Pas possible de le recalculer.
#
#    # impot sur le revenu du foyer (hors prélèvement libératoire, revenus au quotient)
#    irpp   = -(mciria + ppetot - mcirra )


###############################################################################
# # Initialisation de quelques variables utiles pour la suite
###############################################################################


def _age_from_agem(agem):
    return agem // 12


def _age_from_birth(birth, _P):
    return (datetime64(_P.datesim) - birth).astype('timedelta64[Y]')


def _agem_from_age(age):
    return age * 12


def _agem_from_birth(birth, _P):
    return (datetime64(_P.datesim) - birth).astype('timedelta64[M]')


def _nb_adult(marpac, celdiv, veuf):
    return 2 * marpac + 1 * (celdiv | veuf)


def _nb_pac(nbF, nbJ, nbR):
    return nbF + nbJ + nbR


def _nbF(self, age, alt, inv, quifoy):
    enfant_a_charge = and_(quifoy >= 2, or_(age < 18, inv), not_(alt))
    return self.sum_by_entity(enfant_a_charge.astype(int16))


def _nbG(self, alt, inv, quifoy):
    enfant_a_charge_invalide = and_(quifoy >= 2, inv, not_(alt))
    return self.sum_by_entity(enfant_a_charge_invalide.astype(int16))


def _nbH(self, age, alt, inv, quifoy):
    enfant_a_charge_garde_alternee = and_(quifoy >= 2, or_(age < 18, inv), alt)
    return self.sum_by_entity(enfant_a_charge_garde_alternee.astype(int16))


def _nbI(self, alt, inv, quifoy):
    enfant_a_charge_garde_alternee_invalide = and_(quifoy >= 2, inv, alt)
    return self.sum_by_entity(enfant_a_charge_garde_alternee_invalide.astype(int16))


def _nbJ(self, age, inv, quifoy):
    majeur_celibataire_sans_enfant = and_(quifoy >= 2, age >= 18, not_(inv))
    return self.sum_by_entity(majeur_celibataire_sans_enfant.astype(int16))


def _marpac(self, statmarit_holder):
    '''
    Marié (1) ou Pacsé (5)
    'foy'
    '''
    statmarit = self.filter_role(statmarit_holder, role = VOUS)

    return (statmarit == 1) | (statmarit == 5)


def _celdiv(self, statmarit_holder):
    '''
    Célibataire (2) ou divorcé (3)
    'foy'
    '''
    statmarit = self.filter_role(statmarit_holder, role = VOUS)

    return (statmarit == 2) | (statmarit == 3)


def _veuf(self, statmarit_holder):
    '''
    Veuf (4)
    'foy'
    '''
    statmarit = self.filter_role(statmarit_holder, role = VOUS)

    return statmarit == 4


def _jveuf(self, statmarit_holder):
    '''
    Jeune Veuf
    'foy'
    '''
    statmarit = self.filter_role(statmarit_holder, role = VOUS)

    return statmarit == 6


###############################################################################
# # Revenus catégoriels
###############################################################################


def _alloc(self, af_holder, alloc_imp = law.ir.autre.alloc_imp):
    '''
    Allocations familiales imposables
    '''
    # TODO: remove frome here it is a reforme
    af = self.cast_from_entity_to_role(af_holder, role = VOUS)
    af = self.sum_by_entity(af)
    return af * alloc_imp


def _rev_sal(sal, cho):
    '''  
    Revenu imposé comme des salaires (salaires, mais aussi 3vj, 3vk)
    'ind'
    '''
    return sal + cho

def _salcho_imp(rev_sal, cho_ld, fra, abatpro = law.ir.tspr.abatpro):
    """
    Salaires après abattements
    'ind'
    """
    amin = abatpro.min * not_(cho_ld) + abatpro.min2 * cho_ld
    abatfor = round(min_(max_(abatpro.taux * rev_sal, amin), abatpro.max))
    return (fra > abatfor) * (rev_sal - fra) + (fra <= abatfor) * max_(0, rev_sal - abatfor)

def _rev_pen(alr, alr_decl, rst):
    """
    Revenu imposé comme des pensions (retraites, pensions alimentaires, etc.)
    'ind'
    """
    return alr * alr_decl + rst

def _pen_net(rev_pen, abatpen = law.ir.tspr.abatpen):
    """
    Pensions après abattements
    'ind'
    """
#    TODO: problème car les pensions sont majorées au niveau du foyer
#    d11 = ( AS + BS + CS + DS + ES +
#            AO + BO + CO + DO + EO )
#    penv2 = (d11-f11> abatpen.max)*(penv + (d11-f11-abatpen.max)) + (d11-f11<= abatpen.max)*penv
#    Plus d'abatement de 20% en 2006
    return max_(0, rev_pen - round(max_(abatpen.taux * rev_pen , abatpen.min)))
#    return max_(0, rev_pen - min_(round(max_(abatpen.taux*rev_pen , abatpen.min)), abatpen.max))  le max se met au niveau du foyer

def _indu_plaf_abat_pen(self, rev_pen_holder, pen_net_holder, abatpen = law.ir.tspr.abatpen):
    """
    Plafonnement de l'abattement de 10% sur les pensions du foyer
    'foy'
    """
    pen_net = self.sum_by_entity(pen_net_holder)
    rev_pen = self.sum_by_entity(rev_pen_holder)

    abat = rev_pen - pen_net
    return abat - min_(abat, abatpen.max)

def _abat_sal_pen(salcho_imp, pen_net, abatsalpen = law.ir.tspr.abatsalpen):
    """
    Abattement de 20% sur les salaires
    'ind'
    """
    return min_(abatsalpen.taux * max_(salcho_imp + pen_net, 0), abatsalpen.max)

def _sal_pen_net(salcho_imp, pen_net, abat_sal_pen):
    """
    Salaires et pensions après abattement de 20% sur les salaires
    'ind'
    """
    return salcho_imp + pen_net - abat_sal_pen

def _rto(self, f1aw, f1bw, f1cw, f1dw):
    """
    Rentes viagères à titre onéreux (avant abattements)
    """
    return self.cast_from_entity_to_role(f1aw + f1bw + f1cw + f1dw,
        entity = 'foyer_fiscal', role = VOUS)

def _rto_net(self, f1aw, f1bw, f1cw, f1dw, abatviag = law.ir.tspr.abatviag):
    '''
    Rentes viagères après abattements
    '''
    return self.cast_from_entity_to_role(
        round(abatviag.taux1 * f1aw + abatviag.taux2 * f1bw + abatviag.taux3 * f1cw + abatviag.taux4 * f1dw),
        entity = 'foyer_fiscal',
        role = VOUS,
        )

def _tspr(sal_pen_net, rto_net):
    '''
    Traitemens salaires pensions et rentes individuelles
    'ind'
    '''
    return sal_pen_net + rto_net


def _rev_cat_pv(f3vg, f3vh):
    return f3vg - f3vh


def _rev_cat_tspr(self, tspr_holder, indu_plaf_abat_pen):
    '''
    Traitemens salaires pensions et rentes
    'foy'
    '''
    tspr = self.sum_by_entity(tspr_holder)

    return tspr + indu_plaf_abat_pen


def _deficit_rcm(_P, f2aa, f2al, f2am, f2an, f2aq, f2ar):  # TODO: check this, f2as): and correct in data.py
    year = _P.datesim.year
    return (f2aa * (year == 2009)
        + f2al * (year == 2009 | year == 2010)
        + f2am * (year == 2009 | year == 2010 | year == 2011)
        + f2an * (year == 2010 | year == 2011 | year == 2012)
        + f2aq * (year == 2011 | year == 2012 | year == 2013)
        + f2ar * (year == 2012 | year == 2013 | year == 2014))
        # TODO: check this f2as * (year == 2013 | year == 2014 | year == 2015)


def _rev_cat_rvcm(marpac, deficit_rcm, f2ch, f2dc, f2ts, f2ca, f2fu, f2go, f2gr, f2tr, f2da, f2ee, _P,
        finpfl = law.ir.autre.finpfl, rvcm = law.ir.rvcm):
    """
    REVENUS DES VALEURS ET CAPITAUX MOBILIERS
    """
    if _P.datesim.year > 2004:
        f2gr = 0

    # Add f2da to f2dc and f2ee to f2tr when no PFL
    if finpfl:
        f2dc_bis = f2dc + f2da
        f2tr_bis = f2tr + f2ee
    else:
        f2dc_bis = f2dc
        f2tr_bis = f2tr
    # # Calcul du revenu catégoriel
    # 1.2 Revenus des valeurs et capitaux mobiliers
    b12 = min_(f2ch, rvcm.abat_assvie * (1 + marpac))
    TOT1 = f2ch - b12
    # Part des frais s'imputant sur les revenus déclarés case DC
    den = ((f2dc_bis + f2ts) != 0) * (f2dc_bis + f2ts) + ((f2dc_bis + f2ts) == 0)
    F1 = f2ca / den * f2dc_bis
    # Revenus de capitaux mobiliers nets de frais, ouvrant droit à abattement
    # partie négative (à déduire des autres revenus nets de frais d'abattements
    g12a = -min_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
    # partie positive
    g12b = max_(f2dc_bis * (1 - rvcm.abatmob_taux) - F1, 0)
    rev = g12b + f2gr + f2fu * (1 - rvcm.abatmob_taux)

    # Abattements, limité au revenu
    h12 = rvcm.abatmob * (1 + marpac)
    TOT2 = max_(0, rev - h12)
    # i121= -min_(0,rev - h12)

    # Part des frais s'imputant sur les revenus déclarés ligne TS
    F2 = f2ca - F1
    TOT3 = (f2ts - F2) + f2go * rvcm.majGO + f2tr_bis - g12a

    DEF = deficit_rcm
    return max_(TOT1 + TOT2 + TOT3 - DEF, 0)



def _rfr_rvcm(f2dc, f2fu, f2da, finpfl = law.ir.autre.finpfl, rvcm = law.ir.rvcm):
    '''
    Abattements sur rvcm à réintégrer dans le revenu fiscal de référence
    '''
    if finpfl:
        f2dc_bis = f2dc + f2da
    else:
        f2dc_bis = f2dc
    # # TODO: manque le sous total i121 (dans la fonction _rev_cat_rvcm)
    i121 = 0
    return max_((rvcm.abatmob_taux) * (f2dc_bis + f2fu) - i121, 0)


def _rev_cat_rfon(f4ba, f4bb, f4bc, f4bd, f4be, microfoncier = law.ir.microfoncier):
    """
    Revenus fonciers
    TODO: add assert in validator
    """
    # # Calcul du revenu catégoriel
    if ((f4be != 0) & ((f4ba != 0) | (f4bb != 0) | (f4bc != 0))).any():
        log.error(("Problème de déclarations des revenus : incompatibilité de la déclaration des revenus fonciers (f4ba, f4bb, f4bc) et microfonciers (f4be)"))

    a13 = f4ba + f4be - microfoncier.taux * f4be * (f4be <= microfoncier.max)
    b13 = f4bb
    c13 = a13 - b13
    d13 = f4bc
    e13 = c13 - d13 * (c13 >= 0)
    f13 = f4bd * (e13 >= 0)
    g13 = max_(0, e13 - f13)
    rev_cat_rfon = (c13 >= 0) * (g13 + e13 * (e13 < 0)) - (c13 < 0) * d13
    return rev_cat_rfon


def _rev_cat_rpns(self, rpns_i_holder):
    '''
    Traitemens salaires pensions et rentes
    'foy'
    '''
    return self.sum_by_entity(rpns_i_holder)


def _rev_cat(rev_cat_tspr, rev_cat_rvcm, rev_cat_rfon, rev_cat_rpns, rev_cat_pv):
    '''
    Revenus Categoriels
    '''
    return rev_cat_tspr + rev_cat_rvcm + rev_cat_rfon + rev_cat_rpns + rev_cat_pv

###############################################################################
# # Déroulé du calcul de l'irpp
###############################################################################


def _deficit_ante(f6fa, f6fb, f6fc, f6fd, f6fe, f6fl):
    '''
    Déficits antérieurs
    '''
    return f6fa + f6fb + f6fc + f6fd + f6fe + f6fl


def _rbg(alloc, rev_cat, deficit_ante, f6gh):
    '''Revenu brut global
    '''
    # (Total 17)
    # sans les revenus au quotient
    return max_(0, alloc + rev_cat + f6gh - deficit_ante)


def _csg_deduc_patrimoine(f6de):
    '''
    CSG déductible sur les revenus du patrimoine
    http://bofip.impots.gouv.fr/bofip/887-PGP
    '''
    return max_(f6de, 0)


def _csg_deduc_patrimoine_simulated(rev_cat_rfon, rev_cap_bar, rto, taux = law.csg.capital.deduc):
    '''
    Cette fonction simule le montant mentionné dans la case f6de de la déclaration 2042
    http://bofip.impots.gouv.fr/bofip/887-PGP
    '''
    patrimoine_deduc = rev_cat_rfon + rev_cap_bar + rto
    return taux * patrimoine_deduc

def _csg_deduc(rbg, csg_deduc_patrimoine):  # f6de
    ''' CSG déductible '''
    # min_(f6de, max_(rbg, 0))
    return min_(csg_deduc_patrimoine, max_(rbg, 0))

def _rng(rbg, csg_deduc, charges_deduc):
    ''' Revenu net global (total 20) '''
    return max_(0, rbg - csg_deduc - charges_deduc)

def _rni(rng, abat_spe):
    return rng - abat_spe


def _ir_brut(nbptr, rni, bareme = law.ir.bareme):
    '''
    Impot sur le revenu avant non imposabilité et plafonnement du quotient
    'foy'
    '''
    bareme.t_x()
#    bar._linear_taux_moy = True
    return nbptr * bareme.calc(rni / nbptr)  # TODO: partir d'ici, petite différence avec Matlab REMOVE


def _ir_ss_qf(ir_brut, rni, nb_adult, bareme = law.ir.bareme):
    '''
    Impôt sans quotient familial
    '''
    A = bareme.calc(rni / nb_adult)
    return nb_adult * A


def _ir_plaf_qf(ir_brut, ir_ss_qf, nb_adult, nb_pac, nbptr, marpac, veuf, jveuf, celdiv, caseE, caseF, caseG, caseH,
        caseK, caseN, caseP, caseS, caseT, caseW, nbF, nbG, nbH, nbI, nbR, plafond_qf = law.ir.plafond_qf):
    ''' 
    Impôt après plafonnement du quotient familial et réduction complémentaire
    '''
    A = ir_ss_qf
    I = ir_brut

    aa0 = (nbptr - nb_adult) * 2  # nombre de demi part excédant nbadult
    # on dirait que les impôts font une erreur sur aa1 (je suis obligé de
    # diviser par 2)
    aa1 = min_((nbptr - 1) * 2, 2) / 2  # deux première demi part excédants une part
    aa2 = max_((nbptr - 2) * 2, 0)  # nombre de demi part restantes
    # celdiv parents isolés
    condition61 = celdiv & caseT
    B1 = plafond_qf.celib_enf * aa1 + plafond_qf.marpac * aa2
    # tous les autres
    B2 = plafond_qf.marpac * aa0  # si autre
    # celdiv, veufs (non jveuf) vivants seuls et autres conditions
    # TODO: année en dur... pour caseH
    condition63 = (celdiv | (veuf & not_(jveuf))) & not_(caseN) & (nb_pac == 0) & (caseK | caseE) & (caseH < 1981)
    B3 = plafond_qf.celib

    B = B1 * condition61 + \
        B2 * (not_(condition61 | condition63)) + \
        B3 * (condition63 & not_(condition61))
    C = max_(0, A - B)
    # Impôt après plafonnement
    IP0 = max_(I, C)

    # 6.2 réduction d'impôt pratiquée sur l'impot après plafonnement et le cas particulier des DOM
    # pas de réduction complémentaire
    condition62a = (I >= C)
    # réduction complémentaire
    condition62b = (I < C)
    # celdiv veuf
    condition62caa0 = (celdiv | (veuf & not_(jveuf)))
    condition62caa1 = (nb_pac == 0) & (caseP | caseG | caseF | caseW)
    condition62caa2 = caseP & ((nbF - nbG > 0) | (nbH - nbI > 0))
    condition62caa3 = not_(caseN) & (caseE | caseK) & (caseH >= 1981)
    condition62caa = condition62caa0 & (condition62caa1 | condition62caa2 | condition62caa3)
    # marié pacs
    condition62cab = (marpac | jveuf) & caseS & not_(caseP | caseF)
    condition62ca = (condition62caa | condition62cab)

    # plus de 590 euros si on a des plus de
    condition62cb = ((nbG + nbR + nbI) > 0) | caseP | caseF
    D = plafond_qf.reduc_postplafond * (condition62ca + ~condition62ca * condition62cb * (
        1 * caseP + 1 * caseF + nbG + nbR + nbI / 2))

    E = max_(0, A - I - B)
    Fo = D * (D <= E) + E * (E < D)
    IP1 = IP0 - Fo

    # TODO: 6.3 Cas particulier: Contribuables domiciliés dans les DOM.
    # conditionGuadMarReu =
    # conditionGuyane=
    # conitionDOM = conditionGuadMarReu | conditionGuyane
    # postplafGuadMarReu = 5100
    # postplafGuyane = 6700
    # IP2 = IP1 - conditionGuadMarReu*min( postplafGuadMarReu,.3*IP1)  - conditionGuyane*min(postplafGuyane,.4*IP1)

    # Récapitulatif

    return condition62a * IP0 + condition62b * IP1  # IP2 si DOM


def _avantage_qf(ir_ss_qf, ir_plaf_qf):
    return ir_ss_qf - ir_plaf_qf


def _decote(ir_plaf_qf, decote = law.ir.decote):
    '''
    Décote
    '''
    return (ir_plaf_qf < decote.seuil) * (decote.seuil - ir_plaf_qf) * 0.5


def _nat_imp(irpp):
    '''
    Renvoie True si le foyer est imposable, False sinon
    '''
    # def _nat_imp(rni, nbptr, non_imposable = law.ir.non_imposable):
    # seuil = non_imposable.seuil + (nbptr - 1)*non_imposable.supp
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


def _cont_rev_loc(f4bl, crl = law.ir.crl):
    '''
    Contribution sur les revenus locatifs
    '''
    return round(crl.taux * (f4bl >= crl.seuil) * f4bl)


def _teicaa(self, f5qm_holder, bareme = law.ir.teicaa):  # f5rm

    """
    Taxe exceptionelle sur l'indemnité compensatrice des agents d'assurance
    """
    f5qm = self.filter_role(f5qm_holder, role = VOUS)
    f5rm = self.filter_role(f5qm_holder, role = CONJ)

    return bareme.calc(f5qm) + bareme.calc(f5rm)


def _micro_social_vente(self, ebic_impv_holder):
    '''
    Assiette régime microsociale pour les ventes
    '''
    return self.sum_by_entity(ebic_impv_holder)
    # P = _P.ir.rpns.microentreprise
    # assert (ebic_impv <= P.vente.max)


def _micro_social_service(self, ebic_imps_holder):
    '''
    Assiette régime microsociale pour les prestations et services
    '''
    return self.sum_by_entity(ebic_imps_holder)
    # P = _P.ir.rpns.microentreprise
    # assert (ebic_imps <= P.servi.max)


def _micro_social_proflib(self, ebnc_impo_holder):
    '''
    Assiette régime microsociale pour les professions libérales
    '''
    # TODO: distinction RSI/CIPAV (pour les cotisations sociales)
    return self.sum_by_entity(ebnc_impo_holder)
    # P = _P.ir.rpns.microentreprise
    # assert (ebnc_impo <= P.specialbnc.max)


def _micro_social(assiette_service, assiette_proflib, assiette_vente, _P, microsocial = law.ir.rpns.microsocial):
    if _P.datesim.year >= 2009:
        return assiette_service * microsocial.servi + assiette_vente * microsocial.vente + assiette_proflib \
            * microsocial.bnc
    else:
        return 0 * assiette_service


def _plus_values(self, f3vg, f3vh, f3vl, f3vm, f3vi_holder, f3vf_holder, f3vd_holder, f3sa, rpns_pvce_holder, _P,
        plus_values = law.ir.plus_values):  # f3sd is in f3vd holder
    """
    Taxation des plus value
    TODO: f3vt, 2013 f3Vg au barème / tout refaire
    """

    rpns_pvce = self.sum_by_entity(rpns_pvce_holder)
    f3vd = self.filter_role(f3vd_holder, role = VOUS)
    f3sd = self.filter_role(f3vd_holder, role = CONJ)
    f3vi = self.filter_role(f3vi_holder, role = VOUS)
    f3si = self.filter_role(f3vi_holder, role = CONJ)
    f3vf = self.filter_role(f3vf_holder, role = VOUS)
    f3sf = self.filter_role(f3vf_holder, role = CONJ)
    #  TODO: remove this todo use sum for all fields after checking
        # revenus taxés à un taux proportionnel
    rdp = max_(0, f3vg - f3vh) + f3vl + rpns_pvce + f3vm + f3vi + f3vf
    out = (plus_values.pvce * rpns_pvce +
           plus_values.taux1 * max_(0, f3vg - f3vh) +
           plus_values.caprisque * f3vl +
           plus_values.pea * f3vm +
           plus_values.taux3 * f3vi +
           plus_values.taux4 * f3vf)
    if _P.datesim.year >= 2008:
        # revenus taxés à un taux proportionnel
        rdp += f3vd
        out += plus_values.taux1 * f3vd
    if _P.datesim.year == 2012:
#        out = plus_values.taux2 * f3vd + plus_values.taux3 * f3vi + plus_values.taux4 * f3vf + plus_values.taux1 * max_(
#            0, f3vg - f3vh)
        out = (plus_values.taux2 * (f3vd + f3sd) + plus_values.taux3 * (f3vi + f3si) +
            plus_values.taux4 * (f3vf + f3sf) + plus_values.taux1 * max_(0, f3vg - f3vh) + plus_values.pvce * f3sa)
            # TODO: chek this rpns missing ?
    if _P.datesim.year > 2012:
        out = f3vg * 0  # TODO: completely undone

    return round(out)

def _iai(iaidrdi, plus_values, cont_rev_loc, teicaa):
    '''
    impôt avant imputation de l'irpp
    '''
    return iaidrdi + plus_values + cont_rev_loc + teicaa


def _cehr(rfr, nb_adult, bareme = law.ir.cehr):
    '''
    Contribution exceptionnelle sur les hauts revenus
    'foy'
    '''
    return bareme.calc(rfr / nb_adult) * nb_adult

def _cesthra(self, sal_holder, bareme = law.ir.cesthra):
    '''
    Contribution exceptionnelle de solidarité sur les très hauts revenus d'activité
    'foy'
    PLF 2013 (rejeté) : 'taxe à 75%'
    '''
    sal = self.split_by_roles(sal_holder)

    cesthra = 0
    for rev in sal.itervalues():
        cesthra += bareme.calc(rev)
    return cesthra


def _irpp(iai, credits_impot, cehr, microsocial):
    '''
    Montant avant seuil de recouvrement (hors ppe)
    '''
    # log.error(("\n iai: %s, \n - credits_impot: %s \n + cehr : %s \n + cesthra: %s \n + microsocial : %s \n " % (iai, -credits_impot, cehr, cesthra , microsocial)))
    return -(iai - credits_impot + cehr + microsocial)


###############################################################################
# # Autres totaux utiles pour la suite
###############################################################################

def _alv(self, f6gi, f6gj, f6el, f6em, f6gp, f6gu):
    '''
    Pensions alimentaires versées
    '''
    return self.cast_from_entity_to_role(-(f6gi + f6gj + f6el + f6em + f6gp + f6gu),
        entity = 'foyer_fiscal', role = VOUS)

def _rfr(self, rni, alloc, f3va_holder, f3vi_holder, rfr_cd, rfr_rvcm, rpns_exon_holder, rpns_pvce_holder, rev_cap_lib, f3vz):
    '''
    Revenu fiscal de référence
    f3vg -> rev_cat_pv -> ... -> rni
    '''

    f3va = self.sum_by_entity(f3va_holder)
    f3vi = self.sum_by_entity(f3vi_holder)

    rpns_exon = self.sum_by_entity(rpns_exon_holder)
    rpns_pvce = self.sum_by_entity(rpns_pvce_holder)

    return max_(0, rni - alloc) + rfr_cd + rfr_rvcm + rev_cap_lib + f3vi + rpns_exon + rpns_pvce + f3va + f3vz


def _glo(self, f1tv, f1tw, f1tx, f3vf, f3vi, f3vj):
    # f1tv contient f1uv
    # f1tw contient f1uw
    # f1tx contient f1ux
    # f3vf contient f3sf
    # f3vi contient f3si
    # f3vj contient f3vk voir data.py TODO: rename
    '''
    Gains de levée d'option
    '''
    return f1tv + f1tw + f1tx + f3vf + f3vi + f3vj


def _rev_cap_bar(f2dc, f2gr, f2ch, f2ts, f2go, f2tr, f2fu, avf, f2da, f2ee, finpfl = law.ir.autre.finpfl,
        majGO = law.ir.rvcm.majGO):
    """
    Revenus du capital imposés au barème
    """
#    if _P.datesim.year <= 2011:
#        return f2dc + f2gr + f2ch + f2ts + f2go + f2tr + f2fu - avf
#    elif _P.datesim.year > 2011:
#        return f2dc + f2gr + f2ch + f2ts + f2go + f2tr + f2fu - avf + (f2da + f2ee)
    return f2dc + f2gr + f2ch + f2ts + f2go * majGO + f2tr + f2fu - avf + (f2da + f2ee) * finpfl
        # We add f2da an f2ee to allow for comparaison between years


def _rev_cap_lib(f2da, f2dh, f2ee, _P, finpfl = law.ir.autre.finpfl):
    '''
    Revenu du capital imposé au prélèvement libératoire
    '''
    if _P.datesim.year <= 2007:
        out = f2dh + f2ee
    else:
        out = f2da + f2dh + f2ee
    return out * not_(finpfl)


def _avf(f2ab):
    '''
    Avoir fiscal et crédits d'impôt (zavff)
    '''
    return f2ab


def _imp_lib(f2da, f2dh, f2ee, _P, finpfl = law.ir.autre.finpfl,
        prelevement_liberatoire = law.ir.rvcm.prelevement_liberatoire):
    '''
    Prelèvement libératoire sur les revenus du capital
    '''
    if _P.datesim.year <= 2007:
        out = -(prelevement_liberatoire.assvie * f2dh + prelevement_liberatoire.autre * f2ee)
    else:
        out = -(prelevement_liberatoire.action * f2da + prelevement_liberatoire.autre * f2ee) * not_(finpfl) \
            - prelevement_liberatoire.assvie * f2dh
    return out


def _fon(f4ba, f4bb, f4bc, f4bd, f4be, microfoncier = law.ir.microfoncier):
    '''
    Revenus fonciers
    '''
    return f4ba - f4bb - f4bc + round(f4be * (1 - microfoncier.taux))


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

    return (frag_pvce + arag_pvce + nrag_pvce + mbic_pvce + abic_pvce +
             nbic_pvce + macc_pvce + aacc_pvce + nacc_pvce + mbnc_pvce +
             abnc_pvce + nbnc_pvce + mncn_pvce + cncn_pvce)

def _rpns_exon(frag_exon, arag_exon, nrag_exon, mbic_exon, abic_exon,
               nbic_exon, macc_exon, aacc_exon, nacc_exon, mbnc_exon,
               abnc_exon, nbnc_exon):
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
            abnc_exon + nbnc_exon)

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
        abic_imps, nbic_imps, abic_defn, nbic_defn, abic_defs, nbic_defs, nbic_apch,
        microentreprise = law.ir.rpns.microentreprise):
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
    zbic = (mbic_exon + mbic_impv + mbic_imps
        + abic_exon + nbic_exon
        + abic_impn + nbic_impn
        + abic_imps + nbic_imps
        - abic_defn - nbic_defn
        - abic_defs - nbic_defs
        + nbic_apch)

    cond = (mbic_impv > 0) & (mbic_imps == 0)
    taux = microentreprise.vente.taux * cond + microentreprise.servi.taux * not_(cond)

    cbic = min_(mbic_impv + mbic_imps + mbic_exon, max_(microentreprise.vente.min,
        round(mbic_impv * microentreprise.vente.taux + mbic_imps * microentreprise.servi.taux + mbic_exon * taux)))

    return zbic - cbic


def _rac(macc_exon, macc_impv, macc_imps,
         aacc_exon, aacc_impn, aacc_imps, aacc_defn, aacc_defs,
         nacc_exon, nacc_impn, nacc_imps, nacc_defn, nacc_defs,
         mncn_impo, cncn_bene, cncn_defi, microentreprise = law.ir.rpns.microentreprise):
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
    zacc = (macc_exon + macc_impv + macc_imps
            + aacc_exon + aacc_impn + aacc_imps - aacc_defn - aacc_defs
            + nacc_exon + nacc_impn + nacc_imps - nacc_defn - nacc_defs
            + mncn_impo + cncn_bene - cncn_defi)

    cond = (macc_impv > 0) & (macc_imps == 0)
    taux = microentreprise.vente.taux * cond + microentreprise.servi.taux * not_(cond)

    cacc = min_(macc_impv + macc_imps + macc_exon + mncn_impo, max_(microentreprise.vente.min, round(
        macc_impv * microentreprise.vente.taux
        + macc_imps * microentreprise.servi.taux + macc_exon * taux
        + mncn_impo * microentreprise.specialbnc.taux)))

    return zacc - cacc


def _rnc(mbnc_exon, mbnc_impo, abnc_exon, nbnc_exon, abnc_impo, nbnc_impo, abnc_defi, nbnc_defi,
        specialbnc = law.ir.rpns.microentreprise.specialbnc):
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
    zbnc = (mbnc_exon + mbnc_impo
            + abnc_exon + nbnc_exon
            + abnc_impo + nbnc_impo
            - abnc_defi - nbnc_defi)

    cbnc = min_(mbnc_exon + mbnc_impo, max_(specialbnc.min, round((mbnc_exon + mbnc_impo) * specialbnc.taux)))

    return zbnc - cbnc


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

def _rpns_mvct(self, mbic_mvct, macc_mvct, mbnc_mvct, mncn_mvct):
    '''
    Moins values de court terme
    'ind'
    mbic_mvct (f5hu)
    macc_mvct (f5iu)
    mncn_mvct (f5ju)
    mbnc_mvct (f5kz)

    '''
    return self.cast_from_entity_to_role(mbic_mvct + macc_mvct + mbnc_mvct + mncn_mvct,
        entity = 'foyer_fiscal', role = VOUS)

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

def _rpns_i(frag_impo, arag_impg, nrag_impg, arag_defi, nrag_defi,
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
        f5sq,
        cga_taux2 = law.ir.rpns.cga_taux2, microentreprise = law.ir.rpns.microentreprise):
    '''
    Revenus des professions non salariées individuels
    '''
    def abat_rnps(rev, P):
        return max_(0, rev - min_(rev, max_(P.taux * min_(P.max, rev), P.min)))

    # Jeunes agriculteurs montant de l'abattement de 50% ou 100%
    # nrag_ajag = f5hm + f5im + f5jm

#    # déficits agricole des années antérieurs (imputables uniquement
#    # sur des revenus agricoles)
#    rag_timp = frag_impo + frag_pvct + arag_impg + nrag_impg
#    cond = (AUTRE <= microentreprise.def_agri_seuil)
#    def_agri = cond*(arag_defi + nrag_defi) + not_(cond)*min_(rag_timp, arag_defi + nrag_defi)
#    # TODO : check 2006 cf art 156 du CGI pour 2006
#    def_agri_ant    = min_(max_(0,rag_timp - def_agri), f5sq)

    def_agri = arag_defi + nrag_defi + f5sq

    # # B revenus industriels et commerciaux professionnels
    # regime micro entreprise
    mbic_timp = abat_rnps(mbic_impv, microentreprise.vente) + abat_rnps(mbic_imps, microentreprise.servi)

    # Régime du bénéfice réel bénéficiant de l'abattement CGA
    abic_timp = abic_impn + abic_imps - (abic_defn + abic_defs)

    # Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
    nbic_timp = (nbic_impn + nbic_imps) - (nbic_defn + nbic_defs)

    # Abatemment artisant pécheur
    # nbic_apch = f5ks + f5ls + f5ms # TODO : à intégrer qqpart

    # # C revenus industriels et commerciaux non professionnels
    # (revenus accesoires du foyers en nomenclature INSEE)

    # regime micro entreprise
    macc_timp = abat_rnps(macc_impv, microentreprise.vente) + abat_rnps(macc_imps, microentreprise.servi)
    # Régime du bénéfice réel bénéficiant de l'abattement CGA
    aacc_timp = max_(0, (aacc_impn + aacc_imps) - (aacc_defn + aacc_defs))
    # Régime du bénéfice réel ne bénéficiant pas de l'abattement CGA
    nacc_timp = max_(0, (nacc_impn + nacc_imps) - (nacc_defn + nacc_defs))

    # # E revenus non commerciaux non professionnels
    # regime déclaratif special ou micro-bnc
    mncn_timp = abat_rnps(mncn_impo, microentreprise.specialbnc)

    # régime de la déclaration controlée
    # total 11
    cncn_timp = max_(0, cncn_bene - cncn_defi)
    # Abatement jeunes créateurs

    # # D revenus non commerciaux professionnels
    # regime déclaratif special ou micro-bnc
    mbnc_timp = abat_rnps(mbnc_impo, microentreprise.specialbnc)

    # regime de la déclaration contrôlée bénéficiant de l'abattement association agréée
    abnc_timp = abnc_impo - abnc_defi

    # regime de la déclaration contrôlée ne bénéficiant pas de l'abattement association agréée
    nbnc_timp = nbnc_impo - nbnc_defi

    # # Totaux
    atimp = arag_impg + abic_timp + aacc_timp + abnc_timp
    ntimp = nrag_impg + nbic_timp + nacc_timp + nbnc_timp

    majo_cga = max_(0, cga_taux2 * (ntimp + frag_impo))  # Pour ne pas avoir à majorer les déficits
    # total 6
    rev_NS = frag_impo - def_agri + atimp + ntimp + majo_cga

    # revenu net après abatement
    # total 7
    rev_NS_mi = mbic_timp + macc_timp + mbnc_timp + mncn_timp - rpns_mvlt

    RPNS = rev_NS + rev_NS_mi + rpns_pvct - rpns_mvct + cncn_timp

    return RPNS


def _abat_spe(self, age_holder, caseP, caseF, rng, nbN, abattements_speciaux = law.ir.abattements_speciaux):
    """
    Abattements spéciaux

    - pour personnes âges ou invalides : âgé(e) de plus de 65 ans
      ou invalide (titulaire d’une pension d’invalidité militaire ou d’accident
      du travail d’au moins 40 % ou titulaire de la carte d’invalidité),
      abattement de 2 172 € si rng du foyer fiscal inférieur à 13 370 €
                    1 086 € si rng  compris entre 13 370 € et 21 570 €.
      Abattement doublé si conjoint remplit également ces conditions
      d’âge ou d’invalidité.
    - pour enfants à charge ayant fondé un foyer distinct : Si  rattachement
      enfants mariés ou pacsés ou enfants  célibataires, veufs, divorcés, séparés, chargés de famille,
      abattement 5 495 € par personne ainsi rattachée.
      Si l’enfant de la personne rattachée est réputé à charge de
      l’un et l’autre de ses parents (garde alternée), cet abattement est divisé
      par deux soit 2 748€. Exemple : 10 990 € pour un jeune ménage et 8 243 €
      pour un célibataire avec un jeune enfant en résidence alternée.
    """
    age = self.split_by_roles(age_holder, roles = [VOUS, CONJ])

    ageV, ageC = age[VOUS], age[CONJ]
    invV, invC = caseP, caseF
    nb_elig_as = (1 * (((ageV >= 65) | invV) & (ageV > 0)) +
               1 * (((ageC >= 65) | invC) & (ageC > 0)))
    as_inv = (nb_elig_as * abattements_speciaux.inv_montant * ((rng <= abattements_speciaux.inv_max1)
        + ((rng > abattements_speciaux.inv_max1) & (rng <= abattements_speciaux.inv_max2)) * 0.5))

    as_enf = nbN * abattements_speciaux.enf_montant

    return min_(rng, as_inv + as_enf)


###############################################################################
# # Calcul du nombre de parts
###############################################################################


def _nbptr(nb_pac, marpac, celdiv, veuf, jveuf, nbF, nbG, nbH, nbI, nbR, nbJ, caseP, caseW, caseG, caseE, caseK, caseN,
        caseF, caseS, caseL, caseT, quotient_familial = law.ir.quotient_familial):
    '''
    Nombre de parts du foyer
    'foy'
    note 1 enfants et résidence alternée (formulaire 2041 GV page 10)

    quotient_familial.conj : nb part associées au conjoint d'un couple marié ou pacsé
    quotient_familial.enf1 : nb part 2 premiers enfants
    quotient_familial.enf2 : nb part enfants de rang 3 ou plus
    quotient_familial.inv1 : nb part supp enfants invalides (I, G)
    quotient_familial.inv2 : nb part supp adultes invalides (R)
    quotient_familial.not31 : nb part supp note 3 : cases W ou G pour veuf, celib ou div
    quotient_familial.not32 : nb part supp note 3 : personne seule ayant élevé des enfants
    quotient_familial.not41 : nb part supp adultes invalides (vous et/ou conjoint) note 4
    quotient_familial.not42 : nb part supp adultes anciens combattants (vous et/ou conjoint) note 4
    quotient_familial.not6 : nb part supp note 6
    quotient_familial.isol : demi-part parent isolé (T)
    quotient_familial.edcd : enfant issu du mariage avec conjoint décédé;
    '''
    no_pac = nb_pac == 0  # Aucune personne à charge en garde exclusive
    has_pac = not_(no_pac)
    no_alt = nbH == 0  # Aucun enfant à charge en garde alternée
    has_alt = not_(no_alt)

    # # nombre de parts liées aux enfants à charge
    # que des enfants en résidence alternée
    enf1 = (no_pac & has_alt) * (quotient_familial.enf1 * min_(nbH, 2) * 0.5
        + quotient_familial.enf2 * max_(nbH - 2, 0) * 0.5)
    # pas que des enfants en résidence alternée
    enf2 = (has_pac & has_alt) * ((nb_pac == 1) * (quotient_familial.enf1 * min_(nbH, 1) * 0.5
        + quotient_familial.enf2 * max_(nbH - 1, 0) * 0.5) + (nb_pac > 1) * (quotient_familial.enf2 * nbH * 0.5))
    # pas d'enfant en résidence alternée
    enf3 = quotient_familial.enf1 * min_(nb_pac, 2) + quotient_familial.enf2 * max_((nb_pac - 2), 0)

    enf = enf1 + enf2 + enf3
    # # note 2 : nombre de parts liées aux invalides (enfant + adulte)
    n2 = quotient_familial.inv1 * (nbG + nbI / 2) + quotient_familial.inv2 * nbR

    # # note 3 : Pas de personne à charge
    # - invalide

    n31a = quotient_familial.not31a * (no_pac & no_alt & caseP)
    # - ancien combatant
    n31b = quotient_familial.not31b * (no_pac & no_alt & (caseW | caseG))
    n31 = max_(n31a, n31b)
    # - personne seule ayant élevé des enfants
    n32 = quotient_familial.not32 * (no_pac & no_alt & ((caseE | caseK) & not_(caseN)))
    n3 = max_(n31, n32)
    # # note 4 Invalidité de la personne ou du conjoint pour les mariés ou
    # # jeunes veuf(ve)s
    n4 = max_(quotient_familial.not41 * (1 * caseP + 1 * caseF), quotient_familial.not42 * (caseW | caseS))

    # # note 5
    #  - enfant du conjoint décédé
    n51 = quotient_familial.cdcd * (caseL & ((nbF + nbJ) > 0))
    #  - enfant autre et parent isolé
    n52 = quotient_familial.isol * caseT * (((no_pac & has_alt) * ((nbH == 1) * 0.5 + (nbH >= 2))) + 1 * has_pac)
    n5 = max_(n51, n52)

    # # note 6 invalide avec personne à charge
    n6 = quotient_familial.not6 * (caseP & (has_pac | has_alt))

    # # note 7 Parent isolé
    n7 = quotient_familial.isol * caseT * ((no_pac & has_alt) * ((nbH == 1) * 0.5 + (nbH >= 2)) + 1 * has_pac)

    # # Régime des mariés ou pacsés
    m = 1 + quotient_familial.conj + enf + n2 + n4

    # # veufs  hors jveuf
    v = 1 + enf + n2 + n3 + n5 + n6

    # # celib div
    c = 1 + enf + n2 + n3 + n6 + n7

    return (marpac | jveuf) * m + (veuf & not_(jveuf)) * v + celdiv * c


###############################################################################
# # Calcul de la prime pour l'emploi
###############################################################################


def _ppe_coef(jour_xyz):
    '''
    PPE: coefficient de conversion en cas de changement en cours d'année
    '''
    nb_jour = (jour_xyz == 0) + jour_xyz
    return 360 / nb_jour


def _ppe_elig(rfr, ppe_coef, ppe_rev, marpac, veuf, celdiv, nbptr, ppe = law.ir.credits_impot.ppe):
    '''
    PPE: eligibilité à la ppe, condition sur le revenu fiscal de référence
    'foy'
    CF ligne 1: http://bofip.impots.gouv.fr/bofip/3913-PGP.html
    '''
    seuil = (veuf | celdiv) * (ppe.eligi1 + 2 * max_(nbptr - 1, 0) * ppe.eligi3) \
            + marpac * (ppe.eligi2 + 2 * max_(nbptr - 2, 0) * ppe.eligi3)
    return (rfr * ppe_coef) <= seuil


def _ppe_rev(sal, hsup, rpns, ppe = law.ir.credits_impot.ppe):
    '''
    base ressource de la ppe
    'ind'
    '''
    # Revenu d'activité salarié
    rev_sa = sal + hsup  # TODO: + TV + TW + TX + AQ + LZ + VJ
    # Revenu d'activité non salarié
    rev_ns = min_(0, rpns) / ppe.abatns + max_(0, rpns) * ppe.abatns
    return rev_sa + rev_ns


def _ppe_coef_tp(ppe_du_sa, ppe_du_ns, ppe_tp_sa, ppe_tp_ns, ppe = law.ir.credits_impot.ppe):
    '''
    PPE: coefficient de conversion temps partiel
    'ind'
    '''
    frac_sa = ppe_du_sa / ppe.TP_nbh
    frac_ns = ppe_du_ns / ppe.TP_nbj
    tp = ppe_tp_sa | ppe_tp_ns | (frac_sa + frac_ns >= 1)
    return tp + not_(tp) * (frac_sa + frac_ns)


def _ppe_base(self, ppe_rev, ppe_coef_tp, ppe_coef_holder):
    ppe_coef = self.cast_from_entity_to_roles(ppe_coef_holder)

    return ppe_rev / (ppe_coef_tp + (ppe_coef_tp == 0)) * ppe_coef


def _ppe_elig_i(ppe_rev, ppe_coef_tp, ppe = law.ir.credits_impot.ppe):
    '''
    Eligibilité individuelle à la ppe 
    Attention : condition de plafonnement introduite dans ppe brute
    'ind'
    '''
    return (ppe_rev >= ppe.seuil1) & (ppe_coef_tp != 0)


def _ppe_brute(self, ppe_elig, ppe_elig_i_holder, ppe_rev_holder, ppe_base_holder, ppe_coef, ppe_coef_tp_holder, nb_pac,
        marpac, celdiv, veuf, caseT, caseL, nbH, ppe = law.ir.credits_impot.ppe):
    '''
    Prime pour l'emploi (avant éventuel dispositif de cumul avec le RSA)
    'foy'
    Cf. http://travail-emploi.gouv.fr/informations-pratiques,89/fiches-pratiques,91/remuneration,113/la-prime-pour-l-emploi-ppe,1034.html
    '''
    ppe_base = self.split_by_roles(ppe_base_holder)
    ppe_coef_tp = self.split_by_roles(ppe_coef_tp_holder)
    ppe_elig_i = self.split_by_roles(ppe_elig_i_holder)
    ppe_rev = self.split_by_roles(ppe_rev_holder)

    eliv, elic, eli1, eli2, eli3 = ppe_elig_i[VOUS], ppe_elig_i[CONJ], ppe_elig_i[PAC1], ppe_elig_i[PAC2], ppe_elig_i[PAC3],
    basevi, baseci = ppe_rev[VOUS], ppe_rev[CONJ]
    basev, basec, base1, base2, base3 = ppe_base[VOUS], ppe_base[CONJ], ppe_base[PAC1], ppe_base[PAC2], ppe_base[PAC1]
    coef_tpv, coef_tpc, coef_tp1, coef_tp2, coef_tp3 = ppe_coef_tp[VOUS], ppe_coef_tp[CONJ], ppe_coef_tp[PAC1], ppe_coef_tp[PAC2], ppe_coef_tp[PAC1]

    nb_pac_ppe = max_(0, nb_pac - eli1 - eli2 - eli3)

    ligne2 = marpac & xor_(basevi >= ppe.seuil1, baseci >= ppe.seuil1)
    ligne3 = (celdiv | veuf) & caseT & not_(veuf & caseT & caseL)
    ligne1 = not_(ligne2) & not_(ligne3)

    base_monact = ligne2 * (eliv * basev + elic * basec)
    base_monacti = ligne2 * (eliv * basevi + elic * baseci)

    def ppe_bar1(base):
#        cond1 = ligne1 | ligne3
#        cond2 = ligne2
#        return 1 / ppe_coef * ((cond1 & (base <= ppe.seuil2)) * (base) * ppe.taux1 +
#                           (cond1 & (base > ppe.seuil2) & (base <= ppe.seuil3)) * (ppe.seuil3 - base) * ppe.taux2 +
#                           (cond2 & (base <= ppe.seuil2)) * (base * ppe.taux1) +
#                           (cond2 & (base > ppe.seuil2) & (base <= ppe.seuil3)) * ((ppe.seuil3 - base) * ppe.taux2) +
#                           (cond2 & (base > ppe.seuil4) & (base <= ppe.seuil5)) * (ppe.seuil5 - base) * ppe.taux3)
        return (1 / ppe_coef) * (((base <= ppe.seuil2)) * (base) * ppe.taux1
            + ((base > ppe.seuil2) & (base <= ppe.seuil3)) * (ppe.seuil3 - base) * ppe.taux2
            + ligne2 * ((base > ppe.seuil4) & (base <= ppe.seuil5)) * (ppe.seuil5 - base) * ppe.taux3)


    def ppe_bar2(base):
        return (1 / ppe_coef) * ((base <= ppe.seuil2) * (base) * ppe.taux1
            + ((base > ppe.seuil2) & (base <= ppe.seuil3)) * (ppe.seuil3 - base1) * ppe.taux2)

    # calcul des primes individuelles.

    ppev = eliv * ppe_bar1(basev)
    ppec = elic * ppe_bar1(basec)
    ppe1 = eli1 * ppe_bar2(base1)
    ppe2 = eli2 * ppe_bar2(base2)
    ppe3 = eli3 * ppe_bar2(base3)

    # Primes de monoactivité
    ppe_monact_vous = (eliv & ligne2 & (basevi >= ppe.seuil1) & (basev <= ppe.seuil4)) * ppe.monact
    ppe_monact_conj = (elic & ligne2 & (baseci >= ppe.seuil1) & (basec <= ppe.seuil4)) * ppe.monact

    # Primes pour enfants à charge
    maj_pac = ppe_elig * (eliv | elic) * (
        (ligne1 & marpac & ((ppev + ppec) != 0) & (min_(basev, basec) <= ppe.seuil3)) * ppe.pac
            * (nb_pac_ppe + nbH * 0.5)
        + (ligne1 & (celdiv | veuf) & eliv & (basev <= ppe.seuil3)) * ppe.pac * (nb_pac_ppe + nbH * 0.5)
        + (ligne2 & (base_monacti >= ppe.seuil1) & (base_monact <= ppe.seuil3)) * ppe.pac * (nb_pac_ppe + nbH * 0.5)
        + (ligne2 & (base_monact > ppe.seuil3) & (base_monact <= ppe.seuil5)) * ppe.pac
            * ((nb_pac_ppe != 0) + 0.5 * ((nb_pac_ppe == 0) & (nbH != 0)))
        + (ligne3 & (basevi >= ppe.seuil1) & (basev <= ppe.seuil3)) * (
            (min_(nb_pac_ppe, 1) * 2 * ppe.pac + max_(nb_pac_ppe - 1, 0) * ppe.pac)
            + (nb_pac_ppe == 0) * (min_(nbH, 2) * ppe.pac + max_(nbH - 2, 0) * ppe.pac * 0.5))
        + (ligne3 & (basev > ppe.seuil3) & (basev <= ppe.seuil5)) * ppe.pac
            * ((nb_pac_ppe != 0) * 2 + ((nb_pac_ppe == 0) & (nbH != 0))))

    def coef(coef_tp):
        return (coef_tp <= 0.5) * coef_tp * 1.45 + (coef_tp > 0.5) * (0.55 * coef_tp + 0.45)

    ppe_vous = ppe_elig * (ppev * coef(coef_tpv) + ppe_monact_vous)
    ppe_conj = ppe_elig * (ppec * coef(coef_tpc) + ppe_monact_conj)
    ppe_pac1 = ppe_elig * (ppe1 * coef(coef_tp1))
    ppe_pac2 = ppe_elig * (ppe2 * coef(coef_tp2))
    ppe_pac3 = ppe_elig * (ppe3 * coef(coef_tp3))

    ppe_tot = ppe_vous + ppe_conj + ppe_pac1 + ppe_pac2 + ppe_pac3 + maj_pac

    ppe_tot = (ppe_tot != 0) * max_(ppe.versmin, ppe_tot)
    # from pandas import DataFrame
    # decompo = {0: ppev, 1 :ppe_vous, 2: ppec,3: ppe_conj, 4: maj_pac, 5 : ppe_monact_vous, 6: ppe_monact_conj, 8: basev, 81 : basevi, 9: basec, 91 : baseci, 10:ppe_tot}
    # ppe DataFrame(decompo).to_string()

    return ppe_tot


def _ppe(self, ppe_brute, rsa_act_i_holder):
    """
    PPE effectivement versée
    'foy'
    """
    rsa_act_i = self.split_by_roles(rsa_act_i_holder, roles = [VOUS, CONJ])

#   On retranche le RSA activité de la PPE
#   Dans les agrégats officiels de la DGFP, c'est la PPE brute qu'il faut comparer
    ppe = max_(ppe_brute - rsa_act_i[VOUS] - rsa_act_i[CONJ], 0)
    return ppe
