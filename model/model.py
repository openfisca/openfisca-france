# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from datetime import date
from src.lib.utils import Enum
from src.lib.description import ModelDescription
from src.lib.columns import Prestation, BoolPresta, IntPresta, EnumPresta
import src.countries.france.model.cotsoc as cs
import src.countries.france.model.irpp as ir
import src.countries.france.model.irpp_charges_deductibles as cd
import src.countries.france.model.irpp_reductions_impots as ri
import src.countries.france.model.irpp_credits_impots as ci
import src.countries.france.model.irpp_plus_values_immo as immo
import src.countries.france.model.isf as isf
import src.countries.france.model.pfam as pf
import src.countries.france.model.mini as ms
import src.countries.france.model.lgtm as lg
import src.countries.france.model.common as cm
import src.countries.france.model.calage as cl
import src.countries.france.model.th as th

from src.lib.columns import IntCol, EnumCol
from src.countries.france.model.data import QUIFOY, QUIFAM, QUIMEN



def _noi(noi):
    return noi
def _men(idmen, _option = {'idmen': [0]}):
    return idmen
def _fam(idfam, _option = {'idfam': [0]}):
    return idfam
def _foy(idfoy, _option = {'idfoy': [0]}):
    return idfoy
def _quimen(quimen):
    return quimen
def _quifam(quifam):
    return quifam
def _quifoy(quifoy):
    return quifoy
def _wprm(wprm):
    return wprm

class OutputDescription(ModelDescription):

    ############################################################
    # Reproduction des identifiants 
    ############################################################    
#TODO: find a way of having only 'ind' if num_table == 1

    noi_ind = Prestation(_noi)
    idmen_ind = Prestation(_men)
    idmen_foy = EnumPresta(_men,"foy")
    idmen_men = EnumPresta(_men,"men")
    idmen_fam = EnumPresta(_men,"fam")
    idfam_ind = Prestation(_fam)
    idfam_foy = EnumPresta(_fam,"foy")
    idfam_men = EnumPresta(_fam,"men")
    idfam_fam = EnumPresta(_fam,"fam")
    idfoy_ind = Prestation(_foy)
    idfoy_foy = EnumPresta(_foy,"foy")
    idfoy_men = EnumPresta(_foy,"men")
    idfoy_fam = EnumPresta(_foy,"fam")
    
    quimen_ind = EnumPresta(_quimen)
    quifam_ind = EnumPresta(_quifam)
    quifoy_ind = EnumPresta(_quifoy)    
    
    ############################################################
    # Reproduction des pondérations
    ############################################################       
    wprm_ind = Prestation(_wprm,"ind")
    wprm_fam = Prestation(_wprm,"fam")
    wprm_foy = Prestation(_wprm,"foy")    
    
    mhsup = Prestation(cs._mhsup)
    alv   = Prestation(ir._alv)
    ############################################################
    # Cotisations sociales
    ############################################################
    
    # Salaires
    type_sal = EnumPresta(cs._type_sal)
    salbrut = Prestation(cs._salbrut)
    sal_h_b = Prestation(cs._sal_h_b)
    
    cotpat_contrib = Prestation(cs._cotpat_contrib)
    cotpat_noncontrib = Prestation(cs._cotpat_noncontrib)
    cotpat  = Prestation(cs._cotpat)
    
    alleg_fillon = Prestation(cs._alleg_fillon)

    cotsal_contrib = Prestation(cs._cotsal_contrib)
    cotsal_noncontrib = Prestation(cs._cotsal_noncontrib)
    cotsal  = Prestation(cs._cotsal)

    csgsald = Prestation(cs._csgsald)
    csgsali = Prestation(cs._csgsali)
    crdssal = Prestation(cs._crdssal)
    sal = Prestation(cs._sal)    
    salsuperbrut = Prestation(cs._salsuperbrut)
    
    # Chômage
    chobrut = Prestation(cs._chobrut)
    csgchod = Prestation(cs._csgchod)
    csgchoi = Prestation(cs._csgchoi)
    crdscho = Prestation(cs._crdscho)
    cho = Prestation(cs._cho)

    # Pension
    rstbrut = Prestation(cs._rstbrut)
    csgrstd = Prestation(cs._csgrstd)
    csgrsti = Prestation(cs._csgrsti)
    crdsrst = Prestation(cs._crdsrst)
    rst = Prestation(cs._rst)
    
    # Revenus du capital soumis au prélèvement libératoire
    csg_cap_lib = Prestation(cs._csg_cap_lib, label=u"CSG sur les revenus du capital soumis au prélèvement libératoire")
    crds_cap_lib = Prestation(cs._crds_cap_lib, label=u"CRDS sur les revenus du capital soumis au prélèvement libératoire")
    prelsoc_cap_lib = Prestation(cs._prelsoc_cap_lib, label=u"Prélèvements sociaux sur les revenus du capital soumis au prélèvement libératoire")

    # Revenus du capital soumis au barème
    csg_cap_bar = Prestation(cs._csg_cap_bar, label=u"CSG sur les revenus du capital soumis au barème")
    crds_cap_bar = Prestation(cs._crds_cap_bar, label=u"CRDS sur les revenus du capital soumis au barème")
    prelsoc_cap_bar = Prestation(cs._prelsoc_cap_bar, label=u"Prélèvements sociaux sur les revenus du capital soumis au barème")

    # Revenus fonciers (sur les foyers)
    csg_fon = Prestation(cs._csg_fon, "foy", label=u"CSG sur les revenus fonciers")
    crds_fon = Prestation(cs._crds_fon, "foy", label=u"CRDS sur les revenus fonciers")
    prelsoc_fon = Prestation(cs._prelsoc_fon, "foy", label=u"Prélèvements sociaux sur les revenus fonciers")
    
    # Plus values de cessions de valeurs mobilières
    csg_pv_mo = Prestation(cs._csg_pv_mo, "foy", label=u"CSG sur les plus-values de cession de valeurs mobilières")
    crds_pv_mo = Prestation(cs._crds_pv_mo, "foy", label=u"CRDS sur les plus-values de cession de valeurs mobilières")
    prelsoc_pv_mo = Prestation(cs._prelsoc_pv_mo, "foy", label=u"Prélèvements sociaux sur les plus-values de cession de valeurs mobilières")
        
    # Plus-values immobilières
    csg_pv_immo = Prestation(cs._csg_pv_immo, "foy", label=u"CSG sur les plus-values immobilières")
    crds_pv_immo = Prestation(cs._crds_pv_immo, "foy", label=u"CRDS sur les plus-values immobilières")
    prelsoc_pv_immo = Prestation(cs._prelsoc_pv_immo, "foy", label=u"Prélèvements sociaux sur les plus-values immobilières")

    base_csg = Prestation(cs._base_csg)    
    ir_lps = Prestation(cs._ir_lps, start=date(2010, 1, 1))

    ############################################################
    # Impôt sur le revenu
    ############################################################

    marpac = BoolPresta(ir._marpac, entity = 'foy')
    celdiv = BoolPresta(ir._celdiv, entity = 'foy')
    veuf = BoolPresta(ir._veuf, entity = 'foy')
    jveuf = BoolPresta(ir._jveuf, entity = 'foy')
    nbptr = Prestation(ir._nbptr, entity = 'foy', label = u"Nombre de parts")
    rbg = Prestation(ir._rbg, entity = 'foy', label = u"Revenu brut global")

    # charges déductibles
    cd_penali = Prestation(cd._cd_penali, entity = 'foy')
    cd_acc75a = Prestation(cd._cd_acc75a, entity = 'foy')
    cd_percap = Prestation(cd._cd_percap, entity = 'foy', start=date(2002,1,1), end=date(2006,12,31))
    cd_deddiv = Prestation(cd._cd_deddiv, entity = 'foy')
    cd_doment = Prestation(cd._cd_doment, entity = 'foy', start=date(2002,1,1), end=date(2005,12,31))
    cd_eparet = Prestation(cd._cd_eparet, entity = 'foy', start=date(2004,1,1))
    cd_sofipe = Prestation(cd._cd_sofipe, entity = 'foy', start=date(2002,1,1), end=date(2006,12,31))
    cd_cinema = Prestation(cd._cd_cinema, entity = 'foy', start=date(2002,1,1), end=date(2005,12,31))
    cd_ecodev = Prestation(cd._cd_ecodev, entity = 'foy', start=date(2007,1,1), end=date(2008,12,31))
    cd_grorep = Prestation(cd._cd_grorep, entity = 'foy', start=date(2009,1,1))
    
    rbg_int = Prestation(cd._rbg_int, entity = 'foy', label = u"Revenu brut global intermédiaire")
    cd1     = Prestation(cd._cd1, entity = 'foy', label = u"Charges déductibles non plafonnées")
    cd2     = Prestation(cd._cd2, entity = 'foy', label = u"Charges déductibles plafonnées", start=date(2002,1,1), end=date(2008,12,31))    
    charges_deduc = Prestation(cd._charges_deduc, entity = 'foy', label = u"Charges déductibles")
    
    rfr_cd  = Prestation(cd._rfr_cd, entity = 'foy', label = u"Charges déductibles entrant dans le revenus fiscal de référence")  # TODO  

    rng = Prestation(ir._rng, entity = 'foy', label = u"Revenu net global")
    rni = Prestation(ir._rni, entity = 'foy', label = u"Revenu net imposable")
    
    abat_spe = Prestation(ir._abat_spe, entity = 'foy', label = u"Abattements spéciaux")
    alloc    = Prestation(ir._alloc, entity = 'foy', label = u"Allocation familiale pour l'ir")
    deficit_ante = Prestation(ir._deficit_ante, entity = 'foy', label = u"Déficit global antérieur")

    rev_sal = Prestation(ir._rev_sal)
    sal_net = Prestation(ir._sal_net)
    rev_pen = Prestation(ir._rev_pen)
    pen_net = Prestation(ir._pen_net)
    indu_plaf_abat_pen = Prestation(ir._indu_plaf_abat_pen, entity = 'foy')
    abat_sal_pen = Prestation(ir._abat_sal_pen, start=date(2002,1,1), end = date(2005,12,31))
    sal_pen_net = Prestation(ir._sal_pen_net)
    rto     = Prestation(ir._rto, label = u'Rentes viagères (rentes à titre onéreux)')
    rto_net = Prestation(ir._rto_net, label = u'Rentes viagères après abattements')
    tspr    = Prestation(ir._tspr)

    rev_cat_tspr = Prestation(ir._rev_cat_tspr, entity = 'foy', label = u"Revenu catégoriel - Salaires, pensions et rentes")
    rev_cat_rvcm = Prestation(ir._rev_cat_rvcm, entity = 'foy', label = u'Revenu catégoriel - Capitaux')
    rev_cat_rpns = Prestation(ir._rev_cat_rpns, entity = 'foy', label = u'Revenu catégoriel - Rpns')
    rev_cat_rfon = Prestation(ir._rev_cat_rfon, entity = 'foy', label = u'Revenu catégoriel - Foncier')

    rev_cat = Prestation(ir._rev_cat, entity = 'foy', label = u"Revenus catégoriels")

    deficit_rcm = Prestation(ir._deficit_rcm, entity = 'foy', label = u'Deficit capitaux mobiliers')
    csg_deduc = Prestation(ir._csg_deduc, entity = 'foy', label = u'Csg déductible')
    
    plus_values = Prestation(ir._plus_values, entity = 'foy')
    ir_brut     = Prestation(ir._ir_brut, entity = 'foy')
    nb_pac      = Prestation(ir._nb_pac, entity = 'foy')
    nb_adult    = Prestation(ir._nb_adult, entity = 'foy')
    ir_ss_qf    = Prestation(ir._ir_ss_qf, entity = 'foy')
    ir_plaf_qf  = Prestation(ir._ir_plaf_qf, entity = 'foy')
    avantage_qf = Prestation(ir._avantage_qf, entity = 'foy')
    nat_imp     = Prestation(ir._nat_imp, entity = 'foy')
    decote      = Prestation(ir._decote, entity = 'foy')
    
    # réductions d'impots
    donapd   = Prestation(ri._donapd, entity = 'foy')
    dfppce   = Prestation(ri._dfppce, entity = 'foy')
    cotsyn   = Prestation(ri._cotsyn, entity = 'foy')
    resimm   = Prestation(ri._resimm, entity = 'foy', start=date(2009,1,1))
    patnat   = Prestation(ri._patnat, entity = 'foy', start=date(2010,1,1))
    sofipe   = Prestation(ri._sofipe, entity = 'foy', start=date(2009,1,1))
    saldom   = Prestation(ri._saldom, entity = 'foy', start=date(2007,1,1))
    intagr   = Prestation(ri._intagr, entity = 'foy', start=date(2005,1,1))
    prcomp   = Prestation(ri._prcomp, entity = 'foy')
    spfcpi   = Prestation(ri._spfcpi, entity = 'foy')
    mohist   = Prestation(ri._mohist, entity = 'foy', start=date(2008,1,1))
    sofica   = Prestation(ri._sofica, entity = 'foy', start=date(2006,1,1))
    cappme   = Prestation(ri._cappme, entity = 'foy')
    repsoc   = Prestation(ri._repsoc, entity = 'foy', start=date(2003,1,1))
    invfor   = Prestation(ri._invfor, entity = 'foy')
    deffor   = Prestation(ri._deffor, entity = 'foy', start=date(2006,1,1))
    daepad   = Prestation(ri._daepad, entity = 'foy')
    rsceha   = Prestation(ri._rsceha, entity = 'foy')
    invlst   = Prestation(ri._invlst, entity = 'foy', start=date(2004,1,1))
    domlog   = Prestation(ri._domlog, entity = 'foy', start=date(2002,1,1), end=date(2009,12,31))
    adhcga   = Prestation(ri._adhcga, entity = 'foy')
    creaen   = Prestation(ri._creaen, entity = 'foy', start=date(2006,1,1))
    ecpess   = Prestation(ri._ecpess, entity = 'foy')
    scelli   = Prestation(ri._scelli, entity = 'foy', start=date(2009,1,1), end=date(2010,12,31))
    locmeu   = Prestation(ri._locmeu, entity = 'foy', start=date(2009,1,1), end=date(2010,12,31))
    doment   = Prestation(ri._doment, entity = 'foy')
    domsoc   = Prestation(ri._domsoc, entity = 'foy')
    intemp   = Prestation(ri._intemp, entity = 'foy', start=date(2002,1,1), end=date(2003,12,31))
    garext   = Prestation(ri._garext, entity = 'foy', start=date(2002,1,1), end=date(2005,12,31))
    assvie   = Prestation(ri._assvie, entity = 'foy', start=date(2002,1,1), end=date(2004,12,31))
    invrev   = Prestation(ri._invrev, entity = 'foy', start=date(2002,1,1), end=date(2003,12,31))
    intcon   = Prestation(ri._intcon, entity = 'foy', start=date(2004,1,1), end=date(2005,12,31))
    ecodev   = Prestation(ri._ecodev, entity = 'foy', start=date(2009,1,1), end=date(2009,12,31))
    
    nb_pac2  = Prestation(ci._nb_pac2, entity = 'foy')
    
    ip_net      = Prestation(ir._ip_net, entity = 'foy')
    reductions  = Prestation(ri._reductions, entity = 'foy')
    iaidrdi     = Prestation(ir._iaidrdi, entity = 'foy')
    teicaa      = Prestation(ir._teicaa, entity = 'foy')
    cont_rev_loc = Prestation(ir._cont_rev_loc, entity = 'foy', start=date(2001,1,1))
    iai = Prestation(ir._iai, entity = 'foy')
    cehr = Prestation(ir._cehr, entity = 'foy')
    cesthra =  Prestation(ir._cesthra, entity = 'foy')
    imp_lib = Prestation(ir._imp_lib, entity = 'foy')
    
    
    # Prime pour l'emploi
    ppe_coef    = Prestation(ir._ppe_coef, entity = 'foy')
    ppe_base    = Prestation(ir._ppe_base)
    ppe_coef_tp = Prestation(ir._ppe_coef_tp)
    ppe_elig    = BoolPresta(ir._ppe_elig, entity = 'foy')
    ppe_elig_i  = BoolPresta(ir._ppe_elig_i)
    ppe_rev     = Prestation(ir._ppe_rev)
    ppe_brute   = Prestation(ir._ppe_brute, entity = 'foy', label="Prime pour l'emploi brute")
    ppe  = Prestation(ir._ppe,'foy', label="Prime pour l'emploi")
    
    # Autres crédits d'impôts
    creimp = Prestation(ci._creimp, entity = 'foy')
    accult = Prestation(ci._accult, entity = 'foy')
    percvm = Prestation(ci._percvm, entity = 'foy', start=date(2010,1,1))
    direpa = Prestation(ci._direpa, entity = 'foy')
    mecena = Prestation(ci._mecena, entity = 'foy', start=date(2003,1,1))
    prlire = Prestation(ci._prlire, entity = 'foy')
    aidper = Prestation(ci._aidper, entity = 'foy')
    quaenv = Prestation(ci._quaenv, entity = 'foy', start=date(2005,1,1))
    drbail = Prestation(ci._drbail, entity = 'foy')
    ci_garext = Prestation(ci._ci_garext, entity = 'foy', start=date(2005,1,1))
    preetu = Prestation(ci._preetu, entity = 'foy', start=date(2005,1,1))
    saldom2 = Prestation(ci._saldom2, entity = 'foy', start=date(2007,1,1))
    inthab = Prestation(ci._inthab, entity = 'foy', start=date(2007,1,1))
    assloy = Prestation(ci._assloy, entity = 'foy', start=date(2005,1,1))
    autent = Prestation(ci._autent, entity = 'foy', start=date(2009,1,1))
    acqgpl = Prestation(ci._acqgpl, entity = 'foy', start=date(2002,1,1), end=date(2007,12,31))
    divide = Prestation(ci._divide, entity = 'foy', start=date(2005,1,1), end=date(2009,12,31))
    aidmob = Prestation(ci._aidmob, entity = 'foy', start=date(2005,1,1), end=date(2008,12,31))
    
    jeunes = Prestation(ci._jeunes, entity = 'foy', start=date(2005,1,1), end=date(2008,12,31))
    
    credits_impot = Prestation(ci._credits_impot, entity = 'foy')
    
    irpp = Prestation(ir._irpp, entity = 'foy', label=u"Impôt sur le revenu des personnes physiques")

    rfr = Prestation(ir._rfr, entity = 'foy')
    rfr_rvcm = Prestation(ir._rfr_rvcm, entity = 'foy')

#    alv = Prestation(ir._alv)
    glo = Prestation(ir._glo, entity = 'foy')
    rag  = Prestation(ir._rag)
    ric  = Prestation(ir._ric)
    rac  = Prestation(ir._rac)
    rnc  = Prestation(ir._rnc)
    rpns = Prestation(ir._rpns)
    fon  = Prestation(ir._fon, entity = 'foy')
        
    rpns_mvct = Prestation(ir._rpns_mvct)
    rpns_pvct = Prestation(ir._rpns_pvct)
    rpns_mvlt = Prestation(ir._rpns_mvlt)
    rpns_pvce = Prestation(ir._rpns_pvce)
    rpns_exon = Prestation(ir._rpns_exon)
    rpns_i    = Prestation(ir._rpns_i)
    
    rev_cap_bar = Prestation(ir._rev_cap_bar, entity = 'foy')
    rev_cap_lib = Prestation(ir._rev_cap_lib, entity = 'foy')
    avf = Prestation(ir._avf, entity = 'foy')
    
    ###########################################################
    # Impôt sur le revenu afférent à la plus-value immobilière
    ###########################################################
    
    ir_pv_immo = Prestation(immo._ir_pv_immo, entity = 'foy', label = "Impôt sur le revenu afférent à la plus-value immobilière")
    
    ############################################################
    # Impôt de solidarité sur la fortune
    ############################################################
    isf_imm_bati = Prestation(isf._isf_imm_bati, entity = 'foy')
    isf_imm_non_bati = Prestation(isf._isf_imm_non_bati, entity = 'foy')
    isf_actions_sal = Prestation(isf._isf_actions_sal, entity = 'foy', start = date(2006,1,1))
    isf_droits_sociaux = Prestation(isf._isf_droits_sociaux, entity = 'foy')
    ass_isf = Prestation(isf._ass_isf, entity = 'foy')

    isf_iai = Prestation(isf._isf_iai, entity = 'foy')
    tot_impot= Prestation(isf._tot_impot, entity = 'foy')
    isf_avant_plaf = Prestation(isf._isf_avant_plaf, entity = 'foy')
    isf_reduc_pac = Prestation(isf._isf_reduc_pac, entity = 'foy')
    isf_inv_pme = Prestation(isf._isf_inv_pme, entity = 'foy', start = date(2008,1,1))
    isf_org_int_gen= Prestation(isf._isf_org_int_gen, entity = 'foy')
    revetproduits= Prestation(isf._revetproduits, entity = 'foy')
    isf_apres_plaf= Prestation(isf._isf_apres_plaf, entity = 'foy')
    isf_tot = Prestation(isf._isf_tot, entity = 'foy')
    
    
#############################################################################
#                            Bouclier Fiscal                              ###
#############################################################################
    rvcm_plus_abat = Prestation(isf._rvcm_plus_abat, entity = 'foy')
    maj_cga_i = Prestation(isf._maj_cga_i)
    maj_cga = Prestation(isf._maj_cga, entity = 'foy')
    
    bouclier_rev = Prestation( isf._bouclier_rev, entity = 'foy')
    bouclier_imp_gen = Prestation(isf._bouclier_imp_gen, entity = 'foy')
    restitutions = Prestation(isf._restitutions, entity = 'foy')
    bouclier_sumimp = Prestation(isf._bouclier_sumimp, entity = 'foy')
    bouclier_fiscal = Prestation(isf._bouclier_fiscal, entity = 'foy', start = date(2006,1,1))
    

    
    # inclure aussi les dates si nécessaire start=date(2007,1,1)
    
    ############################################################
    # Prestations familiales
    ############################################################
    
    etu      = BoolPresta(pf._etu, label = u"Indicatrice individuelle étudiant")
    biact    = BoolPresta(pf._biact, entity = 'fam', label = u"Indicatrice de biactivité")
    concub   = BoolPresta(pf._concub, entity = 'fam', label = u"Indicatrice de vie en couple") 
    maries   = BoolPresta(pf._maries, entity = 'fam') 
    nb_par   = Prestation(pf._nb_par, entity = 'fam', label = u"Nombre de parents")
    smic55   = BoolPresta(pf._smic55, label = u"Indicatrice individuelle d'un salaire supérieur à 55% du smic")
    isol     = BoolPresta(pf._isol, entity = 'fam')

    div      = Prestation(pf._div)
    rev_coll = Prestation(pf._rev_coll)
    br_pf_i  = Prestation(pf._br_pf_i, label ='Base ressource individuele des prestations familiales')
    br_pf    = Prestation(pf._br_pf, entity = 'fam', label ='Base ressource des prestations familiales')
    
    af_nbenf = Prestation(pf._af_nbenf, entity = 'fam', label = u"Nombre d'enfant au sens des AF")
    af_base  = Prestation(pf._af_base, entity = 'fam', label ='Allocations familiales - Base')
    af_majo  = Prestation(pf._af_majo, entity = 'fam', label ='Allocations familiales - Majoration pour age')
    af_forf  = Prestation(pf._af_forf, entity = 'fam', label ='Allocations familiales - Forfait 20 ans', start = date(2003,7,1))
    af       = Prestation(pf._af, entity = 'fam', label = u"Allocations familiales")
    
    cf_temp  = Prestation(pf._cf, entity = 'fam', label = u"Complément familial avant d'éventuels cumuls")
    asf_elig = BoolPresta(pf._asf_elig)
    asf      = Prestation(pf._asf, entity = 'fam', label = u"Allocation de soutien familial")

    ars      = Prestation(pf._ars, entity = 'fam', label = u"Allocation de rentrée scolaire")

    
    paje_base_temp = Prestation(pf._paje_base, entity = 'fam', label = u"Allocation de base de la PAJE sans tenir compte d'éventuels cumuls", start=date(2004,1,1))
    paje_base      = Prestation(pf._paje_cumul, entity = 'fam', label = u"Allocation de base de la PAJE", start=date(2004,1,1))

    paje_nais      = Prestation(pf._paje_nais, entity = 'fam', label = u"Allocation de naissance de la PAJE", start=date(2004,1,1))
    paje_clca      = Prestation(pf._paje_clca, entity = 'fam', label = u"PAJE - Complément de libre choix d'activité", start=date(2004,1,1))
    paje_clca_taux_plein   = BoolPresta(pf._paje_clca_taux_plein, entity = 'fam', label = u"Indicatrice Clca taux plein", start=date(2004,1,1))
    paje_clca_taux_partiel = BoolPresta(pf._paje_clca_taux_partiel, entity = 'fam', label = u"Indicatrice Clca taux partiel", start=date(2004,1,1))
    paje_colca     = Prestation(pf._paje_colca, entity = 'fam', label = u"PAJE - Complément optionnel de libre choix d'activité", start=date(2004,1,1))
    paje_clmg      = Prestation(pf._paje_clmg, entity = 'fam', label = u"PAJE - Complément de libre choix du mode de garde", start=date(2004,1,1))
    paje           = Prestation(pf._paje, entity = 'fam', label = u"PAJE - Ensemble des prestations", start=date(2004,1,1))


    cf             = Prestation(pf._cf_cumul, entity = 'fam', label = u"Complément familial")    
    aeeh           = Prestation(pf._aeeh, entity = 'fam', label = u"Allocation d'éducation de l'enfant handicapé")

    ape_temp       = Prestation(pf._ape, entity = 'fam', label = u"Allocation parentale d'éducation", end=date(2004, 1,1))
    apje_temp      = Prestation(pf._apje, entity = 'fam', label = u"Allocation pour le jeune enfant", end=date(2004, 1,1)) 
    ape            = Prestation(pf._ape_cumul, entity = 'fam', label = u"Allocation parentale d'éducation", end=date(2004, 1,1))
    apje           = Prestation(pf._apje_cumul, entity = 'fam', label = u"Allocation pour le jeune enfant", end=date(2004, 1,1)) 
    
    crds_pfam      = Prestation(pf._crds_pfam, entity = 'fam', label = u"CRDS (prestations familiales)")
    
    # En fait en vigueur pour les enfants nés avant 2004 ...        
    # TODO Gestion du cumul apje ape
    ############################################################
    # Allocations logement
    ############################################################

    br_al  = Prestation(lg._br_al, entity = 'fam', label = u"Base ressource des allocations logement")
    al_pac = Prestation(lg._al_pac, entity = 'fam', label = u"Nombre de personnes à charge au sens des allocations logement")  
    al     = Prestation(lg._al, entity = 'fam', label = u"Allocation logement (indifferrenciée)")
    alf    = Prestation(lg._alf, entity = 'fam', label = u"Allocation logement familiale")
    als    = Prestation(lg._als, entity = 'fam', label = u"Allocation logement sociale")
    als_nonet    = Prestation(lg._als_nonet, entity = 'fam', label = u"Allocation logement sociale (non étudiant)")
    alset  = Prestation(lg._alset, entity = 'fam', label = u"Allocation logement sociale étudiante")
    apl    = Prestation(lg._apl, entity = 'fam', label = u"Aide personalisée au logement")
    crds_lgtm =Prestation(lg._crds_lgtm, entity = 'fam', label = u"CRDS (allocation logement)")
 
    
    ############################################################
    # RSA/RMI
    ############################################################

    div_ms  = Prestation(ms._div_ms)
    rfon_ms = Prestation(ms._rfon_ms)

    ra_rsa  = Prestation(ms._ra_rsa, label = u"Revenus d'activité du Rsa")
    br_rmi_i = Prestation(ms._br_rmi_i)
    br_rmi_ms = Prestation(ms._br_rmi_ms)
    br_rmi_pf = Prestation(ms._br_rmi_pf)
    br_rmi  = Prestation(ms._br_rmi, entity = 'fam', label = u"Base ressources du Rmi/Rsa")
    
    rmi_nbp = Prestation(ms._rmi_nbp, entity = 'fam', label = u"Nombre de personne à charge au sens du Rmi/Rsa")
    forf_log  = Prestation(ms._forf_log, entity = 'fam')
    rsa_socle = Prestation(ms._rsa_socle, entity = 'fam', label = u"RSA socle")
    rmi  = Prestation(ms._rmi, entity = 'fam', label = u"Revenu de solidarité active - socle")
    rsa  = Prestation(ms._rsa, entity = 'fam', label = u"Revenu de solidarité active")
    majo_rsa = Prestation(ms._majo_rsa, entity = 'fam', label = u"Majoration pour parent isolé du Revenu de solidarité active socle", start = date(2009, 7, 1))
    rsa_act = Prestation(ms._rsa_act, entity = 'fam', label = u"Revenu de solidarité active - activité", start = date(2009, 7, 1))
    rsa_act_i = Prestation(ms._rsa_act_i)
    psa = Prestation(ms._psa, entity = 'fam', label = u"Prime de solidarité active", start = date(2009, 1, 1), end=date(2009, 12,31))
    api  = Prestation(ms._api, entity = 'fam', end = date(2009, 7, 1), label = u"Allocation de parent isolé" )
    crds_mini = Prestation(ms._crds_mini, entity = 'fam', start = date(2009, 7, 1))
    aefa = Prestation(ms._aefa, entity = 'fam', label = u"Allocation exceptionelle de fin d'année")

    ############################################################
    # ASPA/ASI, Minimum vieillesse
    ############################################################

    br_mv_i = Prestation(ms._br_mv_i, label = u"Base ressources du minimum vieillesse/ASPA")
    br_mv   = Prestation(ms._br_mv, entity = 'fam', label = u"Base ressources du minimum vieillesse/ASPA")
    
    asi_aspa_nb_alloc = Prestation(ms._asi_aspa_nb_alloc, entity = 'fam')
    asi_aspa_elig = BoolPresta(ms._asi_aspa_elig, entity = 'fam')
    asi_elig = BoolPresta(ms._asi_elig, label = u"Indicatrice individuelle d'éligibilité à l'allocation supplémentaire d'invalidité")
    asi_coexist_aspa = Prestation(ms._asi_coexist_aspa, entity = 'fam', label = u"Allocation supplémentaire d'invalidité quand un adulte de la famille perçoit l'ASPA")
    asi_pure         = Prestation(ms._asi_pure, entity = 'fam', label = u"Allocation supplémentaire d'invalidité quand aucun adulte de la famille ne perçoit l'ASPA") 
    asi     = Prestation(ms._asi, entity = 'fam', label = u"Allocation supplémentaire d'invalidité", start=date(2007, 1, 1))
    # En 2007, Transformation du MV et de L'ASI en ASPA et ASI. La prestation ASPA calcule bien l'ancien MV
    # mais TODO manque l'ancienne ASI
    
    aspa_elig = BoolPresta(ms._aspa_elig, label = u"Indicatrice individuelle d'éligibilité à l'allocation de solidarité aux personnes agées")
    aspa_coexist_asi  = Prestation(ms._aspa_coexist_asi, entity = 'fam', label = u"Allocation de solidarité aux personnes agées quand un adulte de la famille perçoit l'ASI")
    aspa_pure         = Prestation(ms._aspa_pure, entity = 'fam', label = u"Allocation de solidarité aux personnes agées quand aucun adulte de la famille ne perçoit l'ASI") 
    aspa              = Prestation(ms._aspa, entity = 'fam', label = u"Allocation de solidarité aux personnes agées")
    
    ############################################################
    # Allocation adulte handicapé
    ############################################################

    br_aah  = Prestation(ms._br_aah, entity = 'fam', label = u"Base ressources de l'allocation adulte handicapé")
    aah     = Prestation(ms._aah, entity = 'fam', label = u"Allocation adulte handicapé")
    caah    = Prestation(ms._caah, entity = 'fam', label = u"Complément de l'allocation adulte handicapé")

    ############################################################
    # Taxe d'habitation
    ############################################################
    
    tax_hab       = Prestation(th._tax_hab, entity = 'men', label = u"Taxe d'habitation")

    ############################################################
    # Unité de consommation du ménage
    ############################################################
    uc = Prestation(cm._uc, entity = 'men', label = u"Unités de consommation")

    ############################################################
    # Catégories
    ############################################################
    
    typ_men = IntPresta(cm._typ_men, entity = 'men', label = u"Type de ménage")
    nb_ageq0 = IntPresta(cl._nb_ageq0, entity = 'men', label = u"Effectifs des tranches d'âge quiquennal")
    nbinde = EnumPresta(cl._nbinde, label = u"Nombre d'individus dans le ménage",
                          entity = 'men', 
                          enum = Enum([u"Une personne",
                                       u"Deux personnes",
                                       u"Trois personnes",
                                       u"Quatre personnes",
                                       u"Cinq personnes",
                                       u"Six personnes et plus"], start=1))
    
    cplx = BoolPresta(cl._cplx, entity = 'men', label = u"Indicatrice de ménage complexe")
    
    act_cpl = IntPresta(cl._act_cpl, entity = 'men', label = u"Nombre d'actifs parmi la personne de référence du méange et son conjoint")
    cohab   = BoolPresta(cl._cohab, entity = 'men', label = u"Vie en couple")
    act_enf = IntPresta(cl._act_enf, entity = 'men', label = u"Nombre d'enfants actifs")

    typmen15 = EnumPresta(cl._typmen15, label = u"Type de ménage",
                          entity = 'men',
                          enum = Enum([u"Personne seule active",
                                       u"Personne seule inactive",
                                       u"Familles monoparentales, parent actif",
                                       u"Familles monoparentales, parent inactif et au moins un enfant actif",
                                        u"Familles monoparentales, tous inactifs",
                                        u"Couples sans enfant, 1 actif",
                                        u"Couples sans enfant, 2 actifs",
                                        u"Couples sans enfant, tous inactifs",
                                        u"Couples avec enfant, 1 membre du couple actif",
                                        u"Couples avec enfant, 2 membres du couple actif",
                                        u"Couples avec enfant, couple inactif et au moins un enfant actif",
                                        u"Couples avec enfant, tous inactifs",
                                        u"Autres ménages, 1 actif",
                                        u"Autres ménages, 2 actifs ou plus",
                                        u"Autres ménages, tous inactifs"],start=1))

    decile = EnumPresta(cm._decile, entity = 'men',
                        label = u"Décile de niveau de vie disponible",
                        enum = Enum([u"Hors champ"
                                     u"1er décile",
                                     u"2nd décile",
                                     u"3e décile",
                                     u"4e décile",
                                     u"5e décile",
                                     u"6e décile",
                                     u"7e décile",
                                     u"8e décile",
                                     u"9e décile",
                                     u"10e décile"]))
     
    decile_net = EnumPresta(cm._decile_net, entity = 'men',
                        label = u"Décile de niveau de vie net",
                        enum = Enum([u"Hors champ"
                                     u"1er décile",
                                     u"2nd décile",
                                     u"3e décile",
                                     u"4e décile",
                                     u"5e décile",
                                     u"6e décile",
                                     u"7e décile",
                                     u"8e décile",
                                     u"9e décile",
                                     u"10e décile"]))
     
     
    pauvre40 = EnumPresta(cm._pauvre40, entity = 'men',
                        label = u"Pauvreté monétaire au seuil de 40%",
                        enum = Enum([u"Ménage au dessus du seuil de pauvreté à 40%",
                                     u"Ménage en dessous du seuil de pauvreté à 40%"]))
     
     
    pauvre50 = EnumPresta(cm._pauvre50, entity = 'men',
                        label = u"Pauvreté monétaire au seuil de 50%",
                        enum = Enum([u"Ménage au dessus du seuil de pauvreté à 50%",
                                     u"Ménage en dessous du seuil de pauvreté à 50%"]))
 
    pauvre60 = EnumPresta(cm._pauvre60, entity = 'men',
                        label = u"Pauvreté monétaire au seuil de 60%",
                        enum = Enum([u"Ménage au dessus du seuil de pauvreté à 50%",
                                     u"Ménage en dessous du seuil de pauvreté à 50%"]))



    ############################################################
    # Totaux
    ############################################################

    revdisp_i = Prestation(cm._revdisp_i, label = u"Revenu disponible individuel")
    revdisp = Prestation(cm._revdisp, entity = 'men', label = u"Revenu disponible du ménage")
    nivvie = Prestation(cm._nivvie, entity = 'men', label = u"Niveau de vie du ménage")
        
    revnet_i = Prestation(cm._revnet_i, label = u"Revenu net individuel")
    revnet   = Prestation(cm._revnet, entity = 'men', label = u"Revenu net du ménage")
    nivvie_net = Prestation(cm._nivvie_net, entity = 'men', label = u"Niveau de vie net du ménage")

    revini_i = Prestation(cm._revini_i, label = u"Revenu initial individuel")
    revini   = Prestation(cm._revini, entity = 'men', label = u"Revenu initial du ménage")
    nivvie_ini = Prestation(cm._nivvie_ini, entity = 'men', label = u"Niveau de vie initial du ménage")

    rev_trav = Prestation(cm._rev_trav)    
    pen = Prestation(cm._pen)
    chonet = Prestation(cm._chonet)
    rstnet = Prestation(cm._rstnet)
    cotsoc_bar = Prestation(cm._cotsoc_bar)
    cotsoc_lib = Prestation(cm._cotsoc_lib)
    rev_cap = Prestation(cm._rev_cap)
    psoc = Prestation(cm._psoc)
    pfam = Prestation(cm._pfam, label=u"Prestations familiales")
    mini = Prestation(cm._mini)
    logt = Prestation(cm._logt, label=u"Allocation logement")
    impo = Prestation(cm._impo, label=u"Impôt sur le revenu")
    crds = Prestation(cm._crds, label=u"Contribution au remboursement de la dette sociale")
    csg  = Prestation(cm._csg, label=u"Contribution sociale généralisée")
    cotsoc_noncontrib = Prestation(cm._cotsoc_noncontrib, label=u"Cotisations sociales non contributives")