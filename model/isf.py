# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Sarah Dijols, Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division
from numpy import ( maximum as max_, minimum as min_) 
from src.countries.france.model.data import QUIFOY
ALL = [x[1] for x in QUIFOY]


# 1 ACTIF BRUT

def _isf_imm_bati(b1ab, b1ac, _P):
    '''
    Immeubles bâtis
    '''
    P= _P.isf.res_princ
    return (1-P.taux)*b1ab + b1ac

def _isf_imm_non_bati(b1bc, b1be, b1bh, b1bk, _P):
    '''
    Immeubles non bâtis
    '''
    P= _P.isf.nonbat
    # forêts
    b1bd = b1bc*P.taux_f
    # bien ruraux loués à long terme
    b1bf = min_(b1be, P.seuil)*P.taux_r1 
    b1bg = max_(b1be-P.seuil,0)*P.taux_r2 
    # part de groupements forestiers- agricoles fonciers
    b1bi = min_(b1bh, P.seuil)*P.taux_r1 
    b1bj = max_(b1bh-P.seuil,0)*P.taux_r2
    
    return b1bd + b1bf + b1bg + b1bi + b1bj + b1bk
  

## droits sociaux- valeurs mobilières- liquidités- autres meubles ##

def _isf_actions_sal(b1cl, _P): ## non présent en 2005##
    '''
    Parts ou actions détenues par les salariés et mandataires sociaux
    '''
    P = _P.isf.droits_soc
    return  b1cl*P.taux1  

def _isf_droits_sociaux(isf_actions_sal, b1cb, b1cd, b1ce, b1cf, b1cg, _P):
    P = _P.isf.droits_soc
    # parts ou actions de sociétés avec engagement de 6 ans conservation minimum
    b1cc = b1cb*P.taux2 

    return isf_actions_sal + b1cc + b1cd + b1ce + b1cf + b1cg

def _ass_isf(isf_imm_bati, isf_imm_non_bati, isf_droits_sociaux, b1cg, b2gh, _P):
    total = isf_imm_bati + isf_imm_non_bati + isf_droits_sociaux
    P=_P.isf.forf_mob
    forf_mob = (b1cg != 0)*b1cg + (b1cg==0)*total*P.taux 
    actif_brut = total + forf_mob
    return actif_brut - b2gh 
    
## calcul de l'impôt par application du barème ##

def _isf_iai(ass_isf, _P):
    bar = _P.isf.bareme
    bar.t_x()
    return bar.calc(ass_isf)

def _isf_reduc_pac(nb_pac, nbH, _P):
    '''
    Réductions pour personnes à charges
    '''
    P= _P.isf.reduc_pac
   
    return P.reduc_1*nb_pac + P.reduc_2*nbH  


def _isf_inv_pme(b2mt, b2ne, b2mv, b2nf, b2mx, b2na, _P):
    '''
    Réductions pour investissements dans les PME
    à partir de 2008!
    '''
    
    P= _P.isf.pme
    inv_dir_soc = b2mt*P.taux2 + b2ne*P.taux1
    holdings = b2mv*P.taux2+ b2nf*P.taux1
    fip = b2mx*P.taux1
    fcpi= b2na*P.taux1
    return holdings + fip + fcpi + inv_dir_soc

    
def _isf_org_int_gen(b2nc, _P):
    P = _P.isf.pme
    return b2nc*P.taux2

def _isf_avant_plaf(isf_iai, isf_inv_pme, isf_org_int_gen, isf_reduc_pac, _P ) :
    '''
    Montant de l'impôt avant plafonnement
    '''
    borne_max = _P.isf.pme.max
    return max_(0, isf_iai - min_(isf_inv_pme + isf_org_int_gen, borne_max) - isf_reduc_pac)

  
## calcul du plafonnement ##
  
def _tot_impot(irpp, isf_avant_plaf ):
    return -irpp + isf_avant_plaf
# irpp n'est pas suffisant : ajouter ir soumis à taux propor + impôt acquitté à l'étranger
# + prélèvement libé de l'année passée + montant de la csg TODO


def _revetproduits(sal_net, pen_net, rto_net, rfr_rvcm, fon, ric, rag, rpns_exon, rpns_pvct, rev_cap_lib, imp_lib, _P) :   # TODO: ric? benef indu et comm 
    pt = max_(sal_net + pen_net + rto_net + rfr_rvcm + ric + rag + rpns_exon + rpns_pvct + rev_cap_lib + imp_lib, 0)
    # rev_cap et imp_lib pour produits soumis à prel libératoire- check TODO
    ## def rev_exon et rev_etranger dans data? ##
    P= _P.isf.plafonnement
    return pt*P.taux

def _isf_apres_plaf(tot_impot, revetproduits, isf_avant_plaf, _P): 
    """
    Impôt sur la fortune après plafonnement
    """
    ## si ISF avant plafonnement n'excède pas seuil 1= la limitation du plafonnement ne joue pas ##
    ## si entre les deux seuils; l'allègement est limité au 1er seuil ##
    ## si ISF avant plafonnement est supérieur au 2nd seuil, l'allègement qui résulte du plafonnement est limité à 50% de l'ISF ##
    plafonnement = max_(tot_impot- revetproduits, 0)
    P = _P.isf.plaf
    limitationplaf = (
                      (isf_avant_plaf<= P.seuil1)*plafonnement + 
                      (P.seuil1 <= isf_avant_plaf)*(isf_avant_plaf <= P.seuil2)*min_(plafonnement, P.seuil1) + 
                      (isf_avant_plaf >= P.seuil2)*min_(isf_avant_plaf*P.taux, plafonnement))  
    return (isf_avant_plaf - limitationplaf)


def _isf_tot(b4rs, isf_avant_plaf, isf_apres_plaf, irpp):
    ## rs est le montant des impôts acquittés hors de France ## 
    return min_( -((isf_apres_plaf - b4rs)*((-irpp)>0) + (isf_avant_plaf-b4rs)*((-irpp)<=0)), 0)



## BOUCLIER FISCAL ##

## calcul de l'ensemble des revenus du contribuable ##

# TODO: à reintégrer dans irpp
def _rvcm_plus_abat(rev_cat_rvcm, rfr_rvcm):
    '''
    Revenu catégoriel avec abattement de 40% réintégré.
    '''
    return rev_cat_rvcm + rfr_rvcm

# TODO: à reintégrer dans irpp (et vérifier au passage que frag_impo est dans la majo_cga
def _maj_cga_i(frag_impo, nrag_impg, 
            nbic_impn, nbic_imps, nbic_defn, nbic_defs,
            nacc_impn, nacc_imps, nacc_defn, nacc_defs,
            nbnc_impo, nbnc_defi, _P):
    '''
    Majoration pour non adhésion à un centre de gestion agréé
    'ind'
    '''
    
    ## B revenus industriels et commerciaux professionnels     
    nbic_timp = (nbic_impn + nbic_imps) - (nbic_defn + nbic_defs)
    
    ## C revenus industriels et commerciaux non professionnels 
    # (revenus accesoires du foyers en nomenclature INSEE)
    nacc_timp = max_(0, (nacc_impn + nacc_imps) - (nacc_defn + nacc_defs))
    
    #regime de la déclaration contrôlée ne bénéficiant pas de l'abattement association agréée
    nbnc_timp = nbnc_impo - nbnc_defi
    
    ## Totaux
    ntimp = nrag_impg + nbic_timp +  nacc_timp + nbnc_timp
    
    maj_cga = max_(0,_P.ir.rpns.cga_taux2*(ntimp + frag_impo))
    return maj_cga

def _maj_cga(maj_cga_i, _option = {'maj_cga_i': ALL}):
    '''
    Traitemens salaires pensions et rentes
    'foy'
    '''
    out = None
    for qui in maj_cga_i.itervalues():
        if out is None:
            out = qui
        else:
            out += qui
    
    return out


def _bouclier_rev(rbg, maj_cga, csg_deduc, rvcm_plus_abat, rev_cap_lib, rev_exo, rev_or, cd_penali, cd_eparet):
    ''' 
    Total des revenus sur l'année 'n' net de charges
    '''
    # TODO: réintégrer les déficits antérieur
    # TODO: intégrer les revenus soumis au prélèvement libératoire
    null = 0*rbg
    
    deficit_ante = null
    
    ## Revenus
    frac_rvcm_rfr = 0.7*rvcm_plus_abat
    ## revenus distribués? 
    ## A majorer de l'abatt de 40% - montant brut en cas de PFL
    ## pour le calcul de droit à restitution : prendre 0.7*montant_brut_rev_dist_soumis_au_barème
    rev_bar = rbg - maj_cga - csg_deduc - deficit_ante

## TODO: AJOUTER : indemnités de fonction percus par les élus- revenus soumis à régimes spéciaux

    # Revenu soumis à l'impôt sur le revenu forfaitaire
    rev_lib = rev_cap_lib 
    ## AJOUTER plus-values immo et moins values? 
    
    ##Revenus exonérés d'IR réalisés en France et à l'étranger##
#    rev_exo = primes_pel + primes_cel + rente_pea + int_livrets + plus_values_per
    rev_exo = null
    
    ## proposer à l'utilisateur des taux de réference- PER, PEA, PEL,...TODO
    ## sommes investis- calculer les plus_values annuelles et prendre en compte pour rev_exo?
    # revenus soumis à la taxe forfaitaire sur les métaux précieux : rev_or 
  
    revenus = rev_bar + rev_lib + rev_exo + rev_or
    
    ## CHARGES 
    # Pension alimentaires
    # Cotisations ou primes versées au titre de l'épargne retraite
   
    charges = cd_penali + cd_eparet
    
    return revenus - charges
    
def _bouclier_imp_gen (irpp, tax_hab, tax_fonc, isf_tot, cotsoc_lib, cotsoc_bar, csgsald, csgsali, crdssal, csgchoi, csgchod, csgrstd, csgrsti, imp_lib): ## ajouter CSG- CRDS
    ## ajouter Prelèvements sources/ libé 
    ## ajouter crds rstd
    ## impôt sur les plus-values immo et cession de fonds de commerce
    imp1= cotsoc_lib + cotsoc_bar + csgsald + csgchod + crdssal + csgrstd  + imp_lib
    ''' 
    Impôts payés en l'année 'n' au titre des revenus réalisés sur l'année 'n' 
    '''
    imp2= irpp + isf_tot + tax_hab + tax_fonc  + csgsali + csgchoi + csgrsti
    '''
    Impôts payés en l'année 'n' au titre des revenus réalisés en 'n-1'
    '''
    return imp1+ imp2



def _restitutions(ppe, restit_imp ):
    '''
    Restitutions d'impôt sur le revenu et degrèvements percus en l'année 'n'
    '''
    return ppe + restit_imp

def _bouclier_sumimp(bouclier_imp_gen, restitutions):
    '''
    Somme totale des impôts moins restitutions et degrèvements 
    '''
    return - bouclier_imp_gen +restitutions 
    
def _bouclier_fiscal(bouclier_sumimp, bouclier_rev, _P):
    P = _P.bouclier_fiscal
    return max_(0, bouclier_sumimp - (bouclier_rev*P.taux))
    
