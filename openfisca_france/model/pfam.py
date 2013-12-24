# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)

from __future__ import division
from numpy import (round, floor, zeros, maximum as max_, minimum as min_,
                   logical_not as not_)
from src.countries.france.model.data import QUIFAM


CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]

def _nb_par(quifam, _option={'quifam':[PART]}):
    '''
    Nombre d'adultes (parents) dans la famille
    'fam'
    '''
    return 1 + 1 * (quifam == 1) 
    
def _maries(statmarit , _option = {'statmarit': [CHEF]}):
    '''
    couple = 1 si couple marié sinon 0 TODO faire un choix avec couple ? 
    '''
    return statmarit == 1

def _concub(nb_par):
    '''
    concub = 1 si vie en couple TODO pas très heureux  
    '''
    # TODO: concub n'est pas égal à 1 pour les conjoints
    return nb_par == 2

def _isol(nb_par):
    '''
    Parent (s'il y a lieu) isolé  
    '''
    return nb_par == 1

def _etu(activite):
    '''
    Indicatrice individuelle etudiant
    ''' 
    return activite == 2

def _smic55(salbrut, _P):
    '''
    Indicatrice individuelle d'un salaire supérieur à 55% du smic
    'ind'
    '''
    nbh_travaillees = 151.67 * 12
    smic_annuel_brut = _P.cotsoc.gen.smic_h_b * nbh_travaillees
    return salbrut >= _P.fam.af.seuil_rev_taux * smic_annuel_brut

def _br_pf_i(tspr, hsup, rpns):
    '''
    Base ressource individuelle des prestations familiales
    'ind'
    '''
    return tspr + hsup + rpns

def _biact(br_pf_i, _P, _option={'br_pf_i': [CHEF, PART]}):
    '''
    Indicatrice de biactivité des adultes de la famille
    '''
    seuil_rev = 12 * _P.fam.af.bmaf_n_2
    biact = (br_pf_i[CHEF] >= seuil_rev) & (br_pf_i[PART] >= seuil_rev)
    return biact

def _div(rpns_pvce, rpns_pvct, rpns_mvct, rpns_mvlt, f3vc, f3ve, f3vg, f3vh, f3vl, f3vm):
    return f3vc + f3ve + f3vg - f3vh + f3vl + f3vm + rpns_pvce + rpns_pvct - rpns_mvct - rpns_mvlt

def _rev_coll(rto_net, rev_cap_lib, rev_cap_bar, div, abat_spe, glo, fon, alv, f7ga, f7gb, f7gc):
    '''
    revenus collectif
    '''
    # TODO: ajouter les revenus de l'étranger etr*0.9
    # alv is negative since it is paid by the declaree
    return rto_net + rev_cap_lib + rev_cap_bar + fon + glo + alv - f7ga - f7gb - f7gc - abat_spe
    
def _br_pf(br_pf_i, rev_coll, _option={'br_pf_i': [CHEF, PART], 'rev_coll': [CHEF, PART]}):
    '''
    Base ressource des prestations familiales de la famille
    'fam'
    '''
    br_pf = br_pf_i[CHEF] + br_pf_i[PART] + rev_coll[CHEF] + rev_coll[PART]
    return br_pf
    
#def _af_nbenf(agem, smic55, _P, _option={'agem': ENFS, 'smic55': ENFS}, _freq={'agem':'month'}):    
def _af_nbenf(agem, smic55, _P, _option={'agem': ENFS, 'smic55': ENFS}):
    P = _P.fam.af
    for key, val in agem.iteritems():
        agem[key] = val//12
        
    af_nbenf = nb_enf(agem, smic55, P.age1, P.age2)
    return af_nbenf

############################################################################
# Allocations familiales
############################################################################
    
def _af_base(af_nbenf, _P):
    '''
    Allocations familiales - allocation de base
    'fam'
    '''
    P = _P.fam
    bmaf = P.af.bmaf
    # prestations familiales (brutes de crds)
    af_1enf = round(bmaf * P.af.taux.enf1, 2)
    af_2enf = round(bmaf * P.af.taux.enf2, 2)
    af_enf_supp = round(bmaf * P.af.taux.enf3, 2)
    af_base = (af_nbenf >= 1)*af_1enf + (af_nbenf >= 2)*af_2enf + max_(af_nbenf - 2, 0)*af_enf_supp
    return 12*af_base  # annualisé
    
def _af_majo(age, smic55, af_nbenf, _P, _option={'age': ENFS, 'smic55': ENFS}):
    '''
    Allocations familiales - majoration pour âge
    'fam'
    '''
    # TODO: Date d'entrée en vigueur de la nouvelle majoration
    # enfants nés après le "1997-04-30"       
    bmaf = _P.fam.af.bmaf    
    P_af = _P.fam.af
    P = _P.fam.af.maj_age
    af_maj1 = round(bmaf * P.taux1, 2)
    af_maj2 = round(bmaf * P.taux2, 2)

    ageaine = age_aine(age, smic55, P_af.age1, P_af.age2)

    def age_sf_aine(age, ag1, ag2, ageaine):
        dum = (ag1 <= ageaine) & (ageaine <= ag2)
        return nb_enf(age, smic55, ag1, ag2) - dum * 1


    nbenf_maj1 = ( (af_nbenf == 2)*age_sf_aine(age, P.age1, P.age2 - 1, ageaine)
                   + nb_enf(age, smic55, P.age1, P.age2 - 1)*(af_nbenf >= 3)  )
    nbenf_maj2 = ( (af_nbenf == 2)*age_sf_aine(age, P.age2, P_af.age2, ageaine) 
                   + nb_enf(age, smic55, P.age2, P_af.age2)*(af_nbenf >= 3)  )
        
    af_majo = nbenf_maj1 * af_maj1 + nbenf_maj2 * af_maj2
    
    return 12*af_majo # annualisé

def _af_forf(age, af_nbenf, smic55, _P, _option={'age': ENFS, 'smic55': ENFS}):
    '''
    Allocations familiales - forfait
    'fam'
    '''
    P = _P.fam
    bmaf = _P.fam.af.bmaf    
    nbenf_forf = nb_enf(age, smic55, P.af.age3, P.af.age3)
    af_forfait = round(bmaf * P.af.taux.forfait, 2)
    return 12 * ((af_nbenf >= 2) * nbenf_forf) * af_forfait # annualisé

#def _af(af_base, af_majo, af_forf, _freq = {"af_base" : "year"}):
def _af(af_base, af_majo, af_forf):
    '''
    Allocations familiales - total des allocations
    'fam'
    '''
    return af_base + af_majo + af_forf

############################################################################
# Complément familial
############################################################################

def _cf(age, br_pf, isol, biact, smic55, _P, _option={'age': ENFS, 'smic55': ENFS}):
    """
    Complément familial
    Vous avez au moins 3 enfants à charge tous âgés de plus de 3 ans. 
    Vos ressources ne dépassent pas certaines limites. 
    Vous avez peut-être droit au Complément Familial à partir du mois 
    suivant les 3 ans du 3ème, 4ème, etc. enfant.
    
    # TODO: 
    # En théorie, il faut comparer les revenus de l'année n-2 à la bmaf de
    # l'année n-2 pour déterminer l'éligibilité avec le cf_seuil. Il faudrait
    # pouvoir déflater les revenus de l'année courante pour en tenir compte. 
    """
    P = _P.fam
    bmaf = P.af.bmaf
    bmaf2 = P.af.bmaf_n_2
    cf_nbenf = nb_enf(age, smic55, P.cf.age1, P.cf.age2)
            
    cf_base_n_2 = P.cf.tx * bmaf2
    cf_base = P.cf.tx * bmaf
    
    cf_plaf_tx = 1 + P.cf.plaf_tx1 * min_(cf_nbenf, 2) + P.cf.plaf_tx2 * max_(cf_nbenf - 2, 0)
    cf_majo = isol | biact
    cf_plaf = P.cf.plaf * cf_plaf_tx + P.cf.plaf_maj * cf_majo
    cf_plaf2 = cf_plaf + 12 * cf_base_n_2
    
    cf = (cf_nbenf >= 3) * ((br_pf <= cf_plaf) * cf_base + 
                             (br_pf > cf_plaf) * max_(cf_plaf2 - br_pf, 0) / 12.0)
    return 12 * cf

def _asf_elig(caseT, caseL, _option={'caseT': [CHEF, PART], 'caseL': [CHEF, PART]}):
    return caseT | caseL

def _asf(age, rst, isol, asf_elig, smic55, alr, _P, 
         _option={'rst': [CHEF, PART], 'age': ENFS, 'smic55': ENFS, 'alr': [CHEF, PART] + ENFS}):
    '''
    Allocation de soutien familial
    '''
    # TODO: what is rst doing here ?
    
    # L’ASF permet d’aider le conjoint survivant ou le parent isolé ayant la garde 
    # d’un enfant et les familles ayant à la charge effective et permanente un enfant 
    # orphelin.
    # Vous avez au moins un enfant à votre charge. Vous êtes son père ou sa mère et vous vivez seul(e),
    # ou vous avez recueilli cet enfant et vous vivez seul ou en couple.
    
#    http://www.caf.fr/aides-et-services/s-informer-sur-les-aides/solidarite-et-insertion/l-allocation-de-soutien-familial-asf
    # TODO: Ajouter orphelin recueilli, soustraction à l'obligation d'entretien (et date de celle-ci),
    # action devant le TGI pour complêter l'éligibilité               

    # TODO: la valeur est annualisé mais l'ASF peut ne pas être versée toute l'année   
    P = _P.fam
    asf_nbenf = nb_enf(age, smic55, P.af.age1, P.af.age2)
    asf_nbenfa = asf_nbenf

    asf_brut = round(isol * asf_elig * max_(0, asf_nbenfa * 12 * P.af.bmaf * P.asf.taux1), 2)
    
    res = None
    for alr in alr.itervalues():
        if res is None: res = zeros(len(alr))
        res += alr
    no_alr = not_(res > 0)
    return asf_brut*no_alr

def _ars(age, smic55, br_pf, _P, _option={'age': ENFS, 'smic55': ENFS}):
    '''
    Allocation de rentrée scolaire
    '''
    # TODO: convention sur la mensualisation
    # On tient compte du fait qu'en cas de léger dépassement du plafond, une allocation dégressive 
    # (appelée allocation différentielle), calculée en fonction des revenus, peut être versée. 
    
    P = _P.fam
    bmaf = P.af.bmaf
    # On doit prendre l'âge en septembre
    enf_05 = nb_enf(age, smic55, P.ars.agep - 1, P.ars.agep - 1)  # 6 ans avant le 31 décembre
    #enf_05 = 0
    # Un enfant scolarisé qui n'a pas encore atteint l'âge de 6 ans 
    # avant le 1er février 2012 peut donner droit à l'ARS à condition qu'il 
    # soit inscrit à l'école primaire. Il faudra alors présenter un 
    # certificat de scolarité. 
    enf_primaire = enf_05 + nb_enf(age, smic55, P.ars.agep, P.ars.agec - 1)
    enf_college = nb_enf(age, smic55, P.ars.agec, P.ars.agel - 1)
    enf_lycee = nb_enf(age, smic55, P.ars.agel, P.ars.ages)
    
    arsnbenf = enf_primaire + enf_college + enf_lycee
    
    ars_plaf_res = P.ars.plaf * (1 + arsnbenf * P.ars.plaf_enf_supp)
    arsbase = bmaf * (P.ars.tx0610 * enf_primaire + 
                     P.ars.tx1114 * enf_college + 
                     P.ars.tx1518 * enf_lycee)
    # Forme de l'ARS  en fonction des enfants a*n - (rev-plaf)/n                                             
    ars = max_(0, (ars_plaf_res + arsbase * arsnbenf - max_(br_pf, ars_plaf_res)) / max_(1, arsnbenf))
    return ars * (ars >= P.ars.seuil_nv)

############################################################################
# Prestation d'accueil du jeune enfant
############################################################################

def _paje(paje_base, paje_nais, paje_clca, paje_clmg, paje_colca):
    '''
    Prestation d'accueil du jeune enfant
    '''
    return paje_base + paje_nais + paje_clca + paje_clmg + paje_colca

def _paje_base(age, br_pf, isol, biact, smic55, _P, _option={'age': ENFS, 'smic55': ENFS}):
    ''' 
    Prestation d'acceuil du jeune enfant - allocation de base
    '''
    # TODO cumul des paje si et seulement si naissance multiples
    
    # TODO : théorie, il faut comparer les revenus de l'année n-2 à la bmaf de
    # l'année n-2 pour déterminer l'éligibilité avec le cf_seuil. Il faudrait
    # pouvoir déflater les revenus de l'année courante pour en tenir compte.
    
    P = _P.fam
    bmaf = P.af.bmaf
    bmaf2 = P.af.bmaf_n_2

    base = round(P.paje.base.taux * bmaf, 2)
    base2 = round(P.paje.base.taux * bmaf2, 2)

    # L'allocation de base est versée jusqu'au dernier jour du mois civil précédant 
    # celui au cours duquel l'enfant atteint l'âge de 3 ans.
    
    nbenf = nb_enf(age, smic55, 0, P.paje.base.age - 1)
    
    plaf_tx = (nbenf > 0) + P.paje.base.plaf_tx1 * min_(nbenf, 2) + P.paje.base.plaf_tx2 * max_(nbenf - 2, 0)
    majo = isol | biact
    plaf = P.paje.base.plaf * plaf_tx + (plaf_tx > 0) * P.paje.base.plaf_maj * majo
    plaf2 = plaf + 12 * base2     # TODO vérifier l'aspect différentielle de la PAJE et le plaf2 de la paje
             
    paje_base = (nbenf > 0) * ((br_pf < plaf) * base + 
                           (br_pf >= plaf) * max_(plaf2 - br_pf, 0) / 12) 
    
    # non cumulabe avec la CF, voir Paje_CumulCf
    return 12 * paje_base # annualisé

def _paje_nais(agem, age, af_nbenf, br_pf, isol, biact, _P, _option={'age': ENFS, 'agem': ENFS}):
    '''
    Prestation d'accueil du jeune enfant - Allocation de naissance
    '''
    P = _P.fam   
    bmaf = P.af.bmaf
    nais_prime = round(100 * P.paje.nais.prime_tx * bmaf) / 100
    # Versée au 7e mois de grossesse dans l'année
    # donc les enfants concernés sont les enfants qui ont -2 mois  
    nbnais = 0
    for age_m in agem.itervalues():
# nbnais += (age_m == -2) cas mensuel
        nbnais += (age_m >= -2) * (age_m < 10) 
          
    # Et on compte le nombre d'enfants AF présents  pour le seul mois de la prime
    nbaf = af_nbenf
    nbenf = nbaf + nbnais   # On ajoute l'enfant à  naître;
    
    paje_plaf = P.paje.base.plaf
            
    plaf_tx = 1 + P.paje.base.plaf_tx1 * min_(nbenf, 2) + P.paje.base.plaf_tx2 * max_(nbenf - 2., 0)
    majo = isol | biact
    nais_plaf = paje_plaf * plaf_tx + majo
    elig = (br_pf <= nais_plaf) * (nbnais != 0)
    nais_brut = nais_prime * elig * (nbnais)
    return nais_brut  
    
def _paje_clca(agem, af_nbenf, paje_base, inactif, partiel1, partiel2, _P, _option={'agem': ENFS}):
    """
    Prestation d'accueil du jeune enfant - Complément de libre choix d'activité
    'fam'
    
    Parameters:
    -----------
    
    age :  âge en mois
    af_nbenf : nombre d'enfants aus sens des allocations familiales
    paje_base : allocation de base de la PAJE
    inactif : indicatrice d'inactivité
    partiel1 : Salarié: Temps de travail ne dépassant pas 50 % de la durée du travail fixée dans l'entreprise pour les salariés
               VRP ou non salarié travaillant à temps partiel: Temps de travail ne dépassant pas 76 heures par mois 
                  et un revenu professionnel mensuel inférieur ou égal à (smic_8.27*169*85 %) 
    partiel2 :  Salarié: Temps de travail compris entre 50 et 80 % de la durée du travail fixée dans l'entreprise.
                VRP ou non salarié travaillant à temps partiel: Temps de travail compris entre 77 et 122 heures par mois et un revenu professionnel mensuel ne dépassant pas
                                                                (smic_8.27*169*136 %)
    """
    
    # http://www.caf.fr/wps/portal/particuliers/catalogue/metropole/paje
    paje = paje_base >= 0
    P = _P.fam
    # durée de versement :   
    # Pour un seul enfant à charge, le CLCA est versé pendant une période de 6 mois (P.paje.clca.duree1)
    # à partir de la naissance ou de la cessation des IJ maternité et paternité. 
    # A partir du 2ème enfant, il est versé jusqu’au mois précédant le 3ème anniversaire 
    # de l’enfant.
    
    # Calcul de l'année et mois de naisage_in_months( du cadet 
    # TODO: ajuster en fonction de la cessation des IJ etc
    age_m_benjamin = age_en_mois_benjamin(agem)
    condition1 = (af_nbenf == 1) * (age_m_benjamin >= 0) * (age_m_benjamin < P.paje.clca.duree1)
    age_benjamin = floor(age_m_benjamin / 12)
    condition2 = (age_benjamin <= (P.paje.base.age - 1))            
    condition = (af_nbenf >= 2) * condition2 + condition1
    paje_clca = (condition * P.af.bmaf) * (
                (not_(paje)) * (inactif * P.paje.clca.sansab_tx_inactif + 
                            partiel1 * P.paje.clca.sansab_tx_partiel1 + 
                            partiel2 * P.paje.clca.sansab_tx_partiel2) + 
                (paje) * (inactif * P.paje.clca.avecab_tx_inactif + 
                            partiel1 * P.paje.clca.avecab_tx_partiel1 + 
                            partiel2 * P.paje.clca.avecab_tx_partiel2))
    return 12 * paje_clca  # annualisé
    
def _paje_clca_taux_plein(paje_clca, inactif):
    return (paje_clca > 0) * inactif

def _paje_clca_taux_partiel(paje_clca, partiel1):
    return (paje_clca > 0) * partiel1
            
    # TODO gérer les cumuls avec autres revenus et colca voir site caf

def _paje_clmg(aah, age, smic55, etu, sal, hsup, concub, af_nbenf, br_pf, empl_dir, ass_mat, gar_dom, paje_clca_taux_partiel, paje_clca_taux_plein, _P, _option={'age': ENFS, 'smic55': ENFS, 'etu': [CHEF, PART], 'sal': [CHEF, PART], 'hsup': [CHEF, PART] }):
    '''
    Prestation d accueil du jeune enfant - Complément de libre choix du mode de garde
    '''
    
#        Les conditions
#
#Vous devez :
#
#    avoir un enfant de moins de 6 ans né, adopté ou recueilli en vue d'adoption à partir du 1er janvier 2004
#    employer une assistante maternelle agréée ou une garde à domicile.
#    avoir une activité professionnelle min_
#        si vous êtes salarié cette activité doit vous procurer un revenu min_ de :
#            si vous vivez seul : une fois la BMAF
#            si vous vivez en couple  soit 2 fois la BMAF
#        si vous êtes non salarié, vous devez être à jour de vos cotisations sociales d'assurance vieillesse
#
#Vous n'avez pas besoin de justifier d'une activité min_ si vous êtes :
#
#    bénéficiaire de l'allocation aux adultes handicapés (Aah)
#    au chômage et bénéficiaire de l'allocation d'insertion ou de l'allocation de solidarité spécifique
#    bénéficiaire du Revenu de solidarité active (Rsa), sous certaines conditions de ressources étudiées par votre Caf, et inscrit dans une démarche d'insertion
#    étudiant (si vous vivez en couple, vous devez être tous les deux étudiants).
#
#Autres conditions à remplir : Assistante maternelle agréée     Garde à domicile
#Son salaire brut ne doit pas dépasser par jour de garde et par enfant 5 fois le montant du Smic horaire brut, soit au max_ 45,00 €.     Vous ne devez pas bénéficier de l'exonération des cotisations sociales dues pour la personne employée.
#
# 
       
    P = _P.fam
   
    # condition de revenu minimal

    cond_age_enf = (nb_enf(age, smic55, P.paje.clmg.age1, P.paje.clmg.age2 - 1) > 0)
    cond_sal = (sal[CHEF] + sal[PART] + hsup[CHEF] + hsup[PART] > 12 * P.af.bmaf_n_2 * (1 + concub))
# TODO    cond_rpns    = 
    cond_act = cond_sal   # | cond_rpns
    
    cond_nonact = (aah > 0) | (etu[CHEF] & etu[PART]) # | (ass>0)  
#  TODO RSA insertion, alloc insertion, ass   
    elig = cond_age_enf & (cond_act | cond_nonact) 
    nbenf = af_nbenf
    seuil1 = P.paje.clmg.seuil11 * (nbenf == 1) + P.paje.clmg.seuil12 * (nbenf >= 2) + max_(nbenf - 2, 0) * P.paje.clmg.seuil1sup
    seuil2 = P.paje.clmg.seuil21 * (nbenf == 1) + P.paje.clmg.seuil22 * (nbenf >= 2) + max_(nbenf - 2, 0) * P.paje.clmg.seuil2sup

#        Si vous bénéficiez du Clca taux partiel (= vous travaillez entre 50 et 80% de la durée du travail fixée dans l'entreprise), 
#        vous cumulez intégralement le Clca et le Cmg. 
#        Si vous bénéficiez du Clca taux partiel (= vous travaillez à 50% ou moins de la durée 
#        du travail fixée dans l'entreprise), le montant des plafonds Cmg est divisé par 2.
    seuil1 = seuil1 * (1 - .5 * paje_clca_taux_partiel)
    seuil2 = seuil2 * (1 - .5 * paje_clca_taux_partiel)
    
    clmg = P.af.bmaf * ((nb_enf(age, smic55, 0, P.paje.clmg.age1 - 1) > 0) + 
                           0.5 * (nb_enf(age, smic55, P.paje.clmg.age1, P.paje.clmg.age2 - 1) > 0) 
                           ) * (
        empl_dir * (
            (br_pf < seuil1) * P.paje.clmg.empl_dir1 + 
            ((br_pf >= seuil1) & (br_pf < seuil2)) * P.paje.clmg.empl_dir2 + 
            (br_pf >= seuil2) * P.paje.clmg.empl_dir3) + 
        ass_mat * (
            (br_pf < seuil1) * P.paje.clmg.ass_mat1 + 
            ((br_pf >= seuil1) & (br_pf < seuil2)) * P.paje.clmg.ass_mat2 + 
            (br_pf >= seuil2) * P.paje.clmg.ass_mat3) + 
        gar_dom * (
            (br_pf < seuil1) * P.paje.clmg.domi1 + 
            ((br_pf >= seuil1) & (br_pf < seuil2)) * P.paje.clmg.domi2 + 
            (br_pf >= seuil2) * P.paje.clmg.domi3))        
    # TODO: connecter avec le crédit d'impôt
#        Si vous bénéficiez du Clca taux plein (= vous ne travaillez plus ou interrompez votre activité professionnelle), 
#        vous ne pouvez pas bénéficier du Cmg.         
    paje_clmg = elig * not_(paje_clca_taux_plein) * clmg
    # TODO vérfiez les règles de cumul        
    return 12 * paje_clmg  # annualisé
    
def _paje_colca(af_nbenf, agem, opt_colca, paje_base, _P, _option={'agem': ENFS}):    
    '''
    Prestation d'accueil du jeune enfant - Complément optionnel de libre choix du mode de garde
    '''
    P = _P.fam
    age_m_benjamin = age_en_mois_benjamin(agem)
    condition = (age_m_benjamin < 12 * P.paje.colca.age) * (age_m_benjamin >= 0)   
    nbenf = af_nbenf
    paje = (paje_base > 0)  
    paje_colca = opt_colca * condition * (nbenf >= 3) * P.af.bmaf * (
        (paje) * P.paje.colca.avecab + not_(paje) * P.paje.colca.sansab)
    return 12 * paje_colca  # annualisé

    #TODO: cumul avec clca self.colca_tot_m 

def _paje_cumul(paje_base_temp, cf_temp):
    '''
    L'allocation de base de la paje n'est pas cumulable avec le complément familial
    '''
    # On regarde ce qui est le plus intéressant pour la famille, chaque mois
    paje_base = (paje_base_temp >= cf_temp) * paje_base_temp
    return round(paje_base, 2)
    
def _cf_cumul(paje_base_temp, apje_temp, ape_temp, cf_temp):
    '''
    L'allocation de base de la paje n'est pas cumulable avec le complément familial
    '''
    cf_brut = (paje_base_temp < cf_temp) * (apje_temp <= cf_temp) * (ape_temp <= cf_temp) *cf_temp
    return round(cf_brut, 2)

############################################################################
# Enfant handicapé
############################################################################
    
def _aeeh(age, inv, isol, categ_inv, _P, _option={'categ_inv': ENFS, 'inv': ENFS, 'age': ENFS}):
    '''
    Allocation d'éducation de l'enfant handicapé (Allocation d'éducation spécialisée avant le 1er janvier 2006)
    '''
#        
#        Ce montant peut être majoré par un complément accordé par la Cdaph qui prend en compte :
#        le coût du handicap de l'enfant,
#        la cessation ou la réduction d'activité professionnelle daspa_elig[CHEF]un ou l'autre des deux parents,
#        l'embauche d'une tierce personne rémunérée.
#
#        Une majoration est versée au parent isolé bénéficiaire d'un complément d'Aeeh lorsqu'il cesse ou réduit son activité professionnelle ou lorsqu'il embauche une tierce personne rémunérée.
    P = _P.fam
    isole = isol
    
    aeeh = 0
    for enfant in age.iterkeys():
        enfhand = inv[enfant] * (age[enfant] < P.aeeh.age) / 12
        categ = categ_inv[enfant] 
        if _P.datesim.year <= 2002:
            aeeh += 0 * enfhand    # TODO
        else:
            aeeh += enfhand * (P.af.bmaf * (P.aeeh.base + 
                              P.aeeh.cpl1 * (categ == 1) + 
                              (categ == 2) * (P.aeeh.cpl2 + P.aeeh.maj2 * isole) + 
                              (categ == 3) * (P.aeeh.cpl3 + P.aeeh.maj3 * isole) + 
                              (categ == 4) * (P.aeeh.cpl4 + P.aeeh.maj4 * isole) + 
                              (categ == 5) * (P.aeeh.cpl5 + P.aeeh.maj5 * isole) + 
                              (categ == 6) * (P.aeeh.maj6 * isole)) + 
                              (categ == 6) * P.aeeh.cpl6)

# L'attribution de l'AEEH de base et de ses compléments éventuels ne fait pas obstacle au 
# versement des prestations familiales.
# L'allocation de présence parentale peut être cumulée avec l'AEEH de base, mais pas avec son 
# complément ni avec la majoration de parent isolé.
# Tous les éléments de la prestattion de compensation du handicap (PCH) sont également ouverts 
# aux bénéficiaires de l'AEEH de base, sous certaines conditions, mais ce cumul est exclusif du 
# complément de l'AEEH. Les parents d'enfants handicapés doivent donc choisir entre le versement 
# du complément d'AEEH et la PCH.   
            
    # Ces allocations ne sont pas soumis à la CRDS
    return 12 * aeeh  # annualisé

def _ape(age, smic55, inactif, partiel1, partiel2, _P, _option={'age': ENFS, 'smic55': ENFS}):
    ''' 
    Allocation parentale d'éducation
    'fam'
    L’allocation parentale d’éducation s’adresse aux parents qui souhaitent arrêter ou 
    réduire leur activité pour s’occuper de leurs jeunes enfants, à condition que ceux-ci 
    soient nés avant le 01/01/2004. En effet, pour les enfants nés depuis cette date, 
    dans le cadre de la Prestation d’Accueil du Jeune Enfant, les parents peuvent bénéficier 
    du « complément de libre choix d’activité. »
    '''
    # Les personnes en couple peuvent toutes deux bénéficier de l’APE à taux plein, mais pas en même temps. En revanche, ils peuvent cumuler deux taux partiels, à condition que leur total ne dépasse pas le montant du taux plein.
        
        
    # TODO cumul,  adoption, triplés, 
    #    Cumul d'allocations : Cette allocation n'est pas cumulable pour un même ménage avec
    #- une autre APE (sauf à taux partiel),
    #- ou l'allocation pour jeune enfant (APJE) versée à partir de la naissance,
    #- ou le complément familial,
    #- ou l'allocation d’adulte handicapé (AAH).
    #Enfin, il est à noter que cette allocation n’est pas cumulable avec :
    #- une pension d’invalidité ou une retraite ;
    #- des indemnités journalières de maladie, de maternité ou d’accident du travail ;
    #- des allocations chômage. Il est tout de même possible de demander aux ASSEDIC la suspension de ces dernières pour percevoir l’APE.
    
    # L'allocation parentale d'éducation n'est pas soumise 
    # à condition de ressources, sauf l’APE à taux partiel pour les professions non salariées
    P = _P.fam
    elig = (nb_enf(age, smic55, 0, P.ape.age - 1) >= 1) & (nb_enf(age, smic55, 0, P.af.age2) >= 2)   
    # Inactif
    # Temps partiel 1
    # Salarié: 
    # Temps de travail ne dépassant pas 50 % de la durée du travail fixée dans l'entreprise
    # VRP ou non salarié travaillant à temps partiel:
    # Temps de travail ne dépassant pas 76 heures par mois et un revenu professionnel mensuel inférieur ou égal à (smic_8.27*169*85 %)
    #partiel1 = zeros((12,self.taille))
    
    # Temps partiel 2
    # Salarié:
    # Salarié: Temps de travail compris entre 50 et 80 % de la durée du travail fixée dans l'entreprise.
    # Temps de travail compris entre 77 et 122 heures par mois et un revenu professionnel mensuel ne dépassant pas
    #  (smic_8.27*169*136 %)
    ape = elig * (inactif * P.ape.tx_inactif + partiel1 * P.ape.tx_50 + partiel2 * P.ape.tx_80)
    # Cummul APE APJE CF    
    return 12 * ape  # annualisé
     
def _apje(br_pf, age, smic55, isol, biact, _P, _option={'age': ENFS, 'smic55': ENFS}):
    '''
    Allocation pour jeune enfant
    '''
    # TODO: APJE courte voir doc ERF 2006
    P = _P.fam
    nbenf = nb_enf(age, smic55, 0, P.apje.age - 1)
    bmaf = P.af.bmaf
    bmaf_n_2 = P.af.bmaf_n_2 
    base = round(P.apje.taux * bmaf, 2)
    base2 = round(P.apje.taux * bmaf_n_2, 2)

    plaf_tx = (nbenf > 0) + P.apje.plaf_tx1 * min_(nbenf, 2) + P.apje.plaf_tx2 * max_(nbenf - 2, 0)
    majo = isol | biact
    plaf = P.apje.plaf * plaf_tx + P.apje.plaf_maj * majo
    plaf2 = plaf + 12 * base2    

    apje = (nbenf >= 1) * ((br_pf <= plaf) * base 
                            + (br_pf > plaf) * max_(plaf2 - br_pf, 0) / 12.0)

    # Pour bénéficier de cette allocation, il faut que tous les enfants du foyer soient nés, adoptés, ou recueillis en vue d’une adoption avant le 1er janvier 2004, et qu’au moins l’un d’entre eux ait moins de 3 ans.
    # Cette allocation est verséE du 5ème mois de grossesse jusqu’au mois précédant le 3ème anniversaire de l’enfant.
     
    # Non cumul APE APJE CF  
    #  - L’allocation parentale d’éducation (APE), sauf pour les femmes enceintes. 
    #    L’APJE est alors versée du 5ème mois de grossesse jusqu’à la naissance de l’enfant.
    #  - Le CF
    return 12*apje  # annualisé

def _ape_cumul(apje_temp, ape_temp, cf_temp):
    '''
    L'allocation de base de la paje n'est pas cumulable avec le complément familial
    '''
    ape = (apje_temp < ape_temp) * (cf_temp < ape_temp) * ape_temp
    return round(ape, 2)

def _apje_cumul(apje_temp, ape_temp, cf_temp):
    '''
    L'APJE n'est pas cumulable avec le complément familial et l'APE
    '''
    apje = (cf_temp < apje_temp) * (ape_temp < apje_temp) * apje_temp
    return round(apje, 2)

        
## TODO rajouter la prime à la naissance et à l'adoption br_mv paje check ancienne version

def _aged(age, smic55, br_pf, ape_taux_partiel, dep_trim, _P, _option={'age': ENFS, 'smic55': ENFS}):
    '''
    Allocation garde d'enfant à domicile
    '''
    # TODO: trimestrialiser 
    # les deux conjoints actif et revenu min requis, jusqu'aux 6 ans de l'enfant né avant le 01/01/2004, emploi d'une garde A DOMICILE
    # cette allocation consiste en une prise en charge partielle des charges sociales inhérentes à l'emploi d'une personne à domicile.
    # Si vous avez au moins un enfant  de moins de 3 ans gardé au domicile, 2 cas :
    # Revenus 2005 > 37 241  € : la CAF prend en charge 50% des charges sociales (plafonné à 1 106 € par trimestre),
    # Revenus 2005 < 37 341  € : la CAF prend en charge 75% des charges sociales (plafonné à 1 659 € par trimestre).
    # Si vous avez un enfant de plus de 3 ans gardé au domicile (1 seul cas, sans condition de ressources) :
    # la CAF prend en charge 50% des charges sociales (plafonné à 553 € par trimestre)


    P = _P.fam    
    nbenf = nb_enf(age, smic55, 0, P.aged.age1 - 1)
    nbenf2 = nb_enf(age, smic55, 0, P.aged.age2 - 1)
    elig1 = (nbenf > 0) 
    elig2 = not_(elig1) * (nbenf2 > 0) * ape_taux_partiel
    depenses = 4 * dep_trim # gérer les dépenses trimestrielles        
    aged3 = elig1 * (max_(P.aged.remb_plaf1 - P.aged.remb_taux1 * depenses, 0) * (br_pf > P.aged.revenus_plaf) 
       + (br_pf <= P.aged.revenus_plaf) * max_(P.aged.remb_taux2 * depenses - P.aged.remb_plaf1, 0))
    aged6 = elig2 * max_(P.aged.remb_taux2 * depenses - P.aged.remb_plaf2, 0)
    return 12 * (aged3 + aged6) # annualisé 


def _afeama(age, smic55, ape, af_nbenf, br_pf, _P, _option={'age': ENFS, 'smic55': ENFS}):
    '''
    Aide à la famille pour l'emploi d'une assistante maternelle agréée
    '''
    # TODO http://web.archive.org/web/20080205163300/http://www.caf.fr/wps/portal/particuliers/catalogue/metropole/afeama
    # Les seuils sont de 80 et 110 % de l'ARS
    # Vérifier que c'est la même chose pour le clmg
    P = _P.fam
    
    elig = not_(ape) # assistante maternelle agréee
    # Vous devez:
    #    faire garder votre enfant de moins de 6 ans par une assistante maternelle agréée dont vous êtes l'employeur
    #    déclarer son embauche à l'Urssaf
    #    lui verser un salaire ne dépassant pas par jour de garde et par enfant 5 fois le montant horaire du Smic, soit au max_ 42,20 €
    #
    #Si vous cessez de travailler et bénéficiez de l'allocation parentale d'éducation, vous ne recevrez plus l'Afeama.
    #Vos enfants doivent être nés avant le 1er janvier 2004.

    # TODO calcul des cotisations urssaf
    # 
    nbenf_afeama = nb_enf(age, smic55, P.af.age1, P.afeama.age - 1)
    nbenf = elig * af_nbenf * (nbenf_afeama > 0)

    nb_par_ars = (nbenf == 1 + max_(nbenf - 1, 0) * (1 + P.ars.plaf_enf_supp))
    seuil1 = (P.afeama.mult_seuil1 * P.ars.plaf) * nb_par_ars 
    seuil2 = (P.afeama.mult_seuil2 * P.ars.plaf) * nb_par_ars
        
    afeama = nbenf_afeama * P.af.bmaf * (
            (br_pf < seuil1) * P.afeama.taux_mini + 
            ((br_pf >= seuil1) & (br_pf < seuil2)) * P.afeama.taux_median + 
            (br_pf >= seuil2) * P.afeama.taux_maxi)
    return 12 * afeama # annualisé

    # L'AFEAMA comporte 2 volets complémentaires: l'AFEAMA proprement dit qui consiste à prendre en charge les cotisations sociales sur les salaires, d'une part, 
    # et une allocation complémentaire versée aux parents, la majoration AFEAMA, d'autre part. 
    # Le système de majoration AFEAMA a été modifié au 1er janvier 2001 : 
    # Jusqu'en décembre 2000, son montant ne dépendait que de l'âge de l'enfant. 
    # Depuis janvier 2001, il dépend également de la catégorie de revenus des parents employeurs (fonction de leur base ressources et du nombre d'enfants qu'ils ont à charge).
    # Parallélement, son plafonnement a été ramené de 100 % à 85 % du salaire net versé à l'assistante maternelle (sauf si ces 85 % sont inférieurs au montant de la majoration la moins élevée, compte tenu de l'âge de l'enfant). 
    # La catégorie de revenus des parents employeurs est déterminée par la CAF en fonction de la base ressources du ménage. 
    # Le tableau suivant récapitule les montants pris en compte depuis le 1er juillet 2007 pour la détermination du montant maximal de la majoration AFEAMA selon les catégories de revenus :
    # Base ressources du ménage
    #                 1 enfant                      2 enfants             par enfant suppémentaire
    # revenus    inférieurs à 17 593 €             inférieurs à 21 653 €          4060 €
    #            inférieurs à 24 190 €             inférieurs à 29 773 €          5583 €
    #            supérieurs à 24 190 €             supérieurs à 29 773 €          5583 €
    # Montant base ressources 2006, au 1er juillet 2007

def _crds_pfam(af, cf, asf, ars, paje, ape, apje, _P):
    '''
    Renvoie la CRDS des prestations familiales
    '''
    return -(af + cf + asf + ars + paje + ape + apje)*_P.fam.af.crds

############################################################################
# Helper functions
############################################################################

def nb_enf(ages, smic55, ag1, ag2):
    """
    Renvoie le nombre d'enfant au sens des allocations familiales dont l'âge est compris entre ag1 et ag2
    """
#        Les allocations sont dues à compter du mois civil qui suit la naissance 
#        ag1==0 ou suivant les anniversaires ag1>0.  
#        Un enfant est reconnu à charge pour le versement des prestations 
#        jusqu'au mois précédant son age limite supérieur (ag2 + 1) mais 
#        le versement à lieu en début de mois suivant
    res = None
    for key, age in ages.iteritems():
        if res is None: res = zeros(len(age))  
        res += ((ag1 <= age) & (age <= ag2)) * not_(smic55[key])
    return res

def age_aine(ages, smic55, ag1, ag2):
    '''
    renvoi un vecteur avec l'âge de l'ainé (au sens des allocations 
    familiales) de chaque famille
    '''
    ageaine = -9999
    for key, age in ages.iteritems():
        ispacaf = ((ag1 <= age) & (age <= ag2)) * not_(smic55[key])
        isaine = ispacaf & (age > ageaine)
        ageaine = isaine * age + not_(isaine) * ageaine
    return ageaine

def age_en_mois_benjamin(agems):
    '''
    renvoi un vecteur (une entree pour chaque famille) avec l'age du benjamin.  # TODO check agem > 0
    '''
    agem_benjamin = 12 * 9999
    for agem in agems.itervalues():
        isbenjamin = (agem < agem_benjamin)
        agem_benjamin = isbenjamin * agem + not_(isbenjamin) * agem_benjamin
    return agem_benjamin

