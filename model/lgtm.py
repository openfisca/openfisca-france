# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)

from __future__ import division
from numpy import (round, ceil, floor, maximum as max_, minimum as min_, 
                   logical_not as not_)
from src.countries.france.model.data import QUIFAM, QUIMEN
from src.countries.france.model.pfam import nb_enf

CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]

ALL = [x[1] for x in QUIMEN]

def _al_pac(age, smic55, nbR, _P, _option = {'age': ENFS, 'smic55': ENFS}):
    '''
    Nombre de personne à charge au sens des allocations logement
    '''
    P = _P
    # site de la CAF en 2011: 
    ## Enfant à charge
    # Vous assurez financièrement l'entretien et asez la responsabilité 
    # affective et éducative d'un enfant, que vous ayez ou non un lien de 
    # parenté avec lui. Il est reconnu à votre charge pour le versement 
    # des aides au logement jusqu'au mois précédent ses 21 ans.
    # Attention, s'il travaille, il doit gagner moins de 836,55 € par mois.
    ## Parents âgés ou infirmes
    # Sont à votre charge s'ils vivent avec vous et si leurs revenus 2009 
    # ne dépassent pas 10 386,59 € :
    #   * vos parents ou grand-parents âgés de plus de 65 ans ou d'au moins
    #     60 ans, inaptes au travail, anciens déportés,
    #   * vos proches parents infirmes âgés de 22 ans ou plus (parents, 
    #     grand-parents, enfants, petits enfants, frères, soeurs, oncles, 
    #     tantes, neveux, nièces).
    # P_AL.D_enfch est une dummy qui vaut 1 si les enfants sont comptés à
    # charge (cas actuel) et zéro sinon.
    al_nbinv = nbR
    age1 = P.fam.af.age1
    age2 = P.fam.cf.age2
    al_nbenf = nb_enf(age, smic55, age1, age2)
    al_pac = P.al.autres.D_enfch*(al_nbenf + al_nbinv) #  TODO: manque invalides
    # TODO: il faudrait probablement définir les AL pour un ménage et non 
    # pour une famille
    return al_pac
        
def _br_al(etu, boursier, br_pf_i, rev_coll, biact, _P ,_option = {'boursier': [CHEF, PART], 'etu': [CHEF, PART], 'br_pf_i': [CHEF, PART]}):
    '''
    Base ressource des allocations logement
    '''
    # On ne considère que les revenus des 2 conjoints et les revenus non
    # individualisable
    #   0 - non étudiant
    #   1 - étudiant non boursier
    #   2 - éutidant boursier
    # revCatvous et self.conj : somme des revenus catégoriel après abatement
    # revColl autres revenus du ménage non individualisable
    # ALabat abatement prix en compte pour le calcul de la base ressources
    # des allocattions logement
    # plancher de ressources pour les etudiants
    P = _P
    Pr = P.al.ressources
    
    etuC = (etu[CHEF]) & (not_(etu[PART]))
    etuP = not_(etu[CHEF]) & (etu[PART])
    etuCP = (etu[CHEF]) & (etu[PART])
    # Boursiers
    etuCB = etu[CHEF]&boursier[CHEF]
    etuPB = etu[PART]&boursier[PART]
    # self.etu = (self.etu[CHEF]>=1)|(self.etuP>=1)
    
    revCatVous = max_(br_pf_i[CHEF],etuC*(Pr.dar_4-(etuCB)*Pr.dar_5))
    revCatConj = max_(br_pf_i[PART],etuP*(Pr.dar_4-(etuPB)*Pr.dar_5))
    revCatVsCj = not_(etuCP)*(revCatVous + revCatConj) + \
                    etuCP*max_(br_pf_i[CHEF] + br_pf_i[PART], Pr.dar_4 -(etuCB|etuPB)*Pr.dar_5 + Pr.dar_7)
    
    # somme des revenus catégoriels après abatement
    revCat = revCatVsCj + rev_coll
    # TODO: charges déductibles : pension alimentaires et abatements spéciaux
    revNet = revCat
    
    # On ne considère pas l'abattement sur les ressources de certaines
    # personnes (enfant, ascendants ou grands infirmes).
    
    # abattement forfaitaire double activité
    abatDoubleAct = biact*Pr.dar_1 
    
    # neutralisation des ressources
    # ...
    
    # abbattement sur les ressources
    # ...
    
    # évaluation forfaitaire des ressources (première demande)
    
    # double résidence pour raisons professionnelles
    
    # Base ressource des aides au logement (arrondies aux 100 euros supérieurs)
    
    br_al = ceil(max_(revNet - abatDoubleAct,0)/100)*100

    return br_al

def _al(concub, br_al, so, loyer, coloc, isol, al_pac, zone_apl, nat_imp, _P, _option = {'nat_imp': ALL}):
    '''
    Formule des aides aux logements en secteur locatif
    Attention, cette fonction calcul l'aide mensuelle
    '''
    P = _P
    # ne prend pas en compte les chambres ni les logements-foyers.
    # variables nécéssaires dans FA
    # isol : ménage isolé
    # concub: ménage en couple (rq : concub = ~isol.
    # al_pac : nb de personne à charge du ménage prise en compte pour les AL
    # zone_apl
    # loyer
    # br_al : base ressource des al après abattement.
    # coloc (1 si colocation, 0 sinon)
    # so : statut d'occupation du logement
    #   SO==1 : Accédant à la propriété
    #   SO==2 : Propriétaire (non accédant) du logement.
    #   SO==3 : Locataire d'un logement HLM
    #   SO==4 : Locataire ou sous-locataire d'un logement loué vie non-HLM
    #   SO==5 : Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel.
    #   sO==6 : Logé gratuitement par des parents, des amis ou l'employeur
        
    loca = (3 <= so)&(5 >= so)
    acce = so==1
    rmi = P.al.rmi
    bmaf = P.fam.af.bmaf_n_2
        
    ## aides au logement pour les locataires
    # loyer mensuel;
    L1 = loyer
    # loyer plafond;
    lp_taux = (not_(coloc))*1 + coloc*P.al.loyers_plafond.colocation
    
    z1 = P.al.loyers_plafond.zone1
    z2 = P.al.loyers_plafond.zone2
    z3 = P.al.loyers_plafond.zone3
    
    Lz1 = ((isol)*(al_pac==0)*z1.L1 + (concub)*(al_pac==0)*z1.L2 + (al_pac>0)*z1.L3 + (al_pac>1)*(al_pac-1)*z1.L4)*lp_taux
    Lz2 = ((isol)*(al_pac==0)*z2.L1 + (concub)*(al_pac==0)*z2.L2 + (al_pac>0)*z2.L3 + (al_pac>1)*(al_pac-1)*z2.L4)*lp_taux
    Lz3 = ((isol)*(al_pac==0)*z3.L1 + (concub)*(al_pac==0)*z3.L2 + (al_pac>0)*z3.L3 + (al_pac>1)*(al_pac-1)*z3.L4)*lp_taux
    
    L2 = Lz1*(zone_apl==1) + Lz2*(zone_apl==2) + Lz3*(zone_apl==3)
    # loyer retenu
    L = min_(L1,L2)

    # forfait de charges
    P_fc = P.al.forfait_charges
    C = not_(coloc)*(P_fc.fc1 + al_pac*P_fc.fc2) + \
          ( coloc)*((isol*0.5 + concub)*P_fc.fc1 + al_pac*P_fc.fc2)
    
    # dépense éligible
    E = L + C
    
    # ressources prises en compte 
    R = br_al
    
    # Plafond RO    
    R1 = P.al.R1.taux1*rmi*(isol)*(al_pac==0) + \
         P.al.R1.taux2*rmi*(concub)*(al_pac==0) + \
         P.al.R1.taux3*rmi*(al_pac==1) + \
         P.al.R1.taux4*rmi*(al_pac>=2) + \
         P.al.R1.taux5*rmi*(al_pac>2)*(al_pac-2)
    
    R2 = P.al.R2.taux4*bmaf*(al_pac>=2) + \
         P.al.R2.taux5*bmaf*(al_pac>2)*(al_pac-2)
    
    Ro = round(12*(R1-R2)*(1-P.al.autres.abat_sal));
    
    Rp = max_(0, R - Ro );
    
    # Participation personnelle
    Po = max_(P.al.pp.taux*E, P.al.pp.min);
    
    # Taux de famille    
    TF = P.al.TF.taux1*(isol)*(al_pac==0) + \
         P.al.TF.taux2*(concub)*(al_pac==0) + \
         P.al.TF.taux3*(al_pac==1) + \
         P.al.TF.taux4*(al_pac==2) + \
         P.al.TF.taux5*(al_pac==3) + \
         P.al.TF.taux6*(al_pac>=4) + \
         P.al.TF.taux7*(al_pac>4)*(al_pac-4)
    
    # Loyer de référence
    L_Ref = z2.L1*(isol)*(al_pac==0) + \
            z2.L2*(concub)*(al_pac==0) + \
            z2.L3*(al_pac>=1) + \
            z2.L4*(al_pac>1)*(al_pac-1)

    RL = L / L_Ref

    # TODO: paramètres en dur ??
    TL = max_(max_(0,P.al.TL.taux2*(RL-0.45)),P.al.TL.taux3*(RL-0.75)+P.al.TL.taux2*(0.75-0.45))
    
    Tp= TF + TL
    
    PP = Po + Tp*Rp
    al_loc = max_(0,E - PP)*loca
    al_loc = al_loc*(al_loc>=P.al.autres.nv_seuil)

    ## APL pour les accédants à la propriété
    al_acc = 0*acce
    ## APL (tous)
    
    if _P.ir.autre.charge_loyer.active:
        al = 12*(al_loc + al_acc)*not_( sum(nat_imp.itervalues()) >= 1)
    else:
        al = 12*(al_loc + al_acc)
    
    return al

def _alf(al, al_pac, so):
    '''
    Allocation logement familiale
    '''    
    alf   = (al_pac>=1)*(so != 3)*al    # TODO: également pour les jeunes ménages et femems enceints
    return alf
     
def _als_nonet(al, al_pac, etu, so, _option = {'etu': [CHEF, PART]}):
    '''
    Allocation logement sociale (non étudiante)
    '''    
    als   = (al_pac==0)*(so != 3)*not_(etu[CHEF]|etu[PART])*al
    return als
          
     
def _alset(al, al_pac, etu, so, _option = {'etu': [CHEF, PART]}):
    '''
    Allocation logement sociale étudiante
    '''    
    alset = (al_pac==0)*(so != 3)*(etu[CHEF] | etu[PART])*al
    return alset

def _als(als_nonet, alset):
    '''
    Allocation logement sociale
    '''
    return als_nonet + alset


def _apl(al, so):
    '''
    Aide personalisée au logement (réservée aux logements conventionné, surtout des HLM, 
    et financé par le fonds national de l'habitation)
    '''
    #TODO: 
    return al*(so == 3)

def _crds_lgtm(al, _P):
    '''
    CRDS des allocations logement
    '''
    return -al*_P.fam.af.crds

def _uc(agem, _option = {'agem': ALL}):
    '''
    Calcule le nombre d'unités de consommation du ménage avec l'échelle de l'insee
    'men'
    '''
    uc_adt = 0.5
    uc_enf = 0.3
    uc = 0.5
    for agm in agem.itervalues():
        age = floor(agm/12)
        adt = (15 <= age) & (age <= 150)
        enf = (0  <= age) & (age <= 14)
        uc += adt*uc_adt + enf*uc_enf
    return uc
