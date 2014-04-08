# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division

import cPickle

from numpy import ceil, floor, fromiter, int16, logical_not as not_, maximum as max_, minimum as min_, round
from openfisca_core.accessors import law
import pkg_resources

from .. import data as data_resources
from .input_variables.base import QUIFAM, QUIMEN, QUIFOY
from .pfam import nb_enf


CHEF = QUIFAM['chef']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
PART = QUIFAM['part']
VOUS = QUIFOY['vous']


zone_apl_by_code_postal = None


def _al_pac(self, age_holder, smic55_holder, nbR_holder, af = law.fam.af, cf = law.fam.cf,
        D_enfch = law.al.autres.D_enfch):
    '''
    Nombre de personne à charge au sens des allocations logement

    site de la CAF en 2011:

    # Enfant à charge
    Vous assurez financièrement l'entretien et asez la responsabilité
    affective et éducative d'un enfant, que vous ayez ou non un lien de
    parenté avec lui. Il est reconnu à votre charge pour le versement
    des aides au logement jusqu'au mois précédent ses 21 ans.
    Attention, s'il travaille, il doit gagner moins de 836,55 € par mois.

    # Parents âgés ou infirmes
    Sont à votre charge s'ils vivent avec vous et si leurs revenus 2009
    ne dépassent pas 10 386,59 € :
    * vos parents ou grand-parents âgés de plus de 65 ans ou d'au moins
    60 ans, inaptes au travail, anciens déportés,
    * vos proches parents infirmes âgés de 22 ans ou plus (parents,
    grand-parents, enfants, petits enfants, frères, soeurs, oncles,
    tantes, neveux, nièces).
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

    # P_AL.D_enfch est une dummy qui vaut 1 si les enfants sont comptés à
    # charge (cas actuel) et zéro sinon.
    nbR = self.cast_from_entity_to_role(nbR_holder, role = VOUS)
    al_nbinv = self.sum_by_entity(nbR)

    age1 = af.age1
    age2 = cf.age2
    al_nbenf = nb_enf(age, smic55, age1, age2)
    al_pac = D_enfch * (al_nbenf + al_nbinv)  #  TODO: manque invalides
    # TODO: il faudrait probablement définir les AL pour un ménage et non
    # pour une famille
    return al_pac


def _br_al(self, etu_holder, boursier_holder, br_pf_i_holder, rev_coll_holder, biact, Pr = law.al.ressources):
    '''
    Base ressource des allocations logement
    '''
    # On ne considère que les revenus des 2 conjoints et les revenus non
    # individualisables
    #   0 - non étudiant
    #   1 - étudiant non boursier
    #   2 - éutidant boursier
    # revCatvous et self.conj : somme des revenus catégoriel après abatement
    # revColl : autres revenus du ménage non individualisable
    # ALabat : abatement prix en compte pour le calcul de la base ressources
    # des allocattions logement
    # plancher de ressources pour les etudiants
    boursier = self.split_by_roles(boursier_holder, roles = [CHEF, PART])
    br_pf_i = self.split_by_roles(br_pf_i_holder, roles = [CHEF, PART])
    etu = self.split_by_roles(etu_holder, roles = [CHEF, PART])
    rev_coll = self.sum_by_entity(rev_coll_holder)

    etuC = (etu[CHEF]) & (not_(etu[PART]))
    etuP = not_(etu[CHEF]) & (etu[PART])
    etuCP = (etu[CHEF]) & (etu[PART])
    # Boursiers
    # TODO: distinguer boursier foyer/boursier locatif
    etuCB = etu[CHEF] & boursier[CHEF]
    etuPB = etu[PART] & boursier[PART]
    # self.etu = (self.etu[CHEF]>=1)|(self.etuP>=1)

    revCatVous = max_(br_pf_i[CHEF], etuC * (Pr.dar_4 - (etuCB) * Pr.dar_5))
    revCatConj = max_(br_pf_i[PART], etuP * (Pr.dar_4 - (etuPB) * Pr.dar_5))
    revCatVsCj = not_(etuCP) * (revCatVous + revCatConj) + \
                    etuCP * max_(br_pf_i[CHEF] + br_pf_i[PART], Pr.dar_4 - (etuCB | etuPB) * Pr.dar_5 + Pr.dar_7)

    # TODO: ajouter les paramètres pour les étudiants en foyer (boursier et non boursier), les inclure dans le calcul
    # somme des revenus catégoriels après abatement
    revCat = revCatVsCj + rev_coll

    # TODO: charges déductibles : pension alimentaires et abatements spéciaux
    revNet = revCat

    # On ne considère pas l'abattement sur les ressources de certaines
    # personnes (enfant, ascendants ou grands infirmes).

    # abattement forfaitaire double activité
    abatDoubleAct = biact * Pr.dar_1

    # TODO: neutralisation des ressources
    # ...

    # TODO: abbattement sur les ressources
    # ...

    # TODO: évaluation forfaitaire des ressources (première demande)

    # TODO :double résidence pour raisons professionnelles

    # Base ressource des aides au logement (arrondies aux 100 euros supérieurs)

    br_al = ceil(max_(revNet - abatDoubleAct, 0) / 100) * 100

    return br_al


def _al(self, concub, br_al, so, loyer, coloc_holder, isol, al_pac, zone_apl, nat_imp_holder, al = law.al,
        charge_loyer = law.ir.autre.charge_loyer, fam = law.fam):
    '''
    Formule des aides aux logements en secteur locatif
    Attention, cette fonction calcule l'aide mensuelle
    '''
    coloc = self.any_by_roles(coloc_holder)
    nat_imp = self.cast_from_entity_to_roles(nat_imp_holder)
    nat_imp = self.any_by_roles(nat_imp)

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

    loca = (3 <= so) & (5 >= so)
    acce = so == 1
    rmi = al.rmi
    bmaf = fam.af.bmaf_n_2

    # # aides au logement pour les locataires
    # loyer mensuel;
    L1 = loyer
    # loyer plafond;
    lp_taux = (not_(coloc)) * 1 + coloc * al.loyers_plafond.colocation

    z1 = al.loyers_plafond.zone1
    z2 = al.loyers_plafond.zone2
    z3 = al.loyers_plafond.zone3

    Lz1 = ((isol) * (al_pac == 0) * z1.L1 + (concub) * (al_pac == 0) * z1.L2 + (al_pac > 0) * z1.L3 + (al_pac > 1) * (al_pac - 1) * z1.L4) * lp_taux
    Lz2 = ((isol) * (al_pac == 0) * z2.L1 + (concub) * (al_pac == 0) * z2.L2 + (al_pac > 0) * z2.L3 + (al_pac > 1) * (al_pac - 1) * z2.L4) * lp_taux
    Lz3 = ((isol) * (al_pac == 0) * z3.L1 + (concub) * (al_pac == 0) * z3.L2 + (al_pac > 0) * z3.L3 + (al_pac > 1) * (al_pac - 1) * z3.L4) * lp_taux

    L2 = Lz1 * (zone_apl == 1) + Lz2 * (zone_apl == 2) + Lz3 * (zone_apl == 3)
    # loyer retenu
    L = min_(L1, L2)

    # forfait de charges
    P_fc = al.forfait_charges
    C = not_(coloc) * (P_fc.fc1 + al_pac * P_fc.fc2) + \
          (coloc) * ((isol * 0.5 + concub) * P_fc.fc1 + al_pac * P_fc.fc2)

    # dépense éligible
    E = L + C

    # ressources prises en compte
    R = br_al

    # Plafond RO
    R1 = al.R1.taux1 * rmi * (isol) * (al_pac == 0) + \
         al.R1.taux2 * rmi * (concub) * (al_pac == 0) + \
         al.R1.taux3 * rmi * (al_pac == 1) + \
         al.R1.taux4 * rmi * (al_pac >= 2) + \
         al.R1.taux5 * rmi * (al_pac > 2) * (al_pac - 2)

    R2 = al.R2.taux4 * bmaf * (al_pac >= 2) + \
         al.R2.taux5 * bmaf * (al_pac > 2) * (al_pac - 2)

    Ro = round(12 * (R1 - R2) * (1 - al.autres.abat_sal));

    Rp = max_(0, R - Ro);

    # Participation personnelle
    Po = max_(al.pp.taux * E, al.pp.min);

    # Taux de famille
    TF = al.TF.taux1 * (isol) * (al_pac == 0) + \
         al.TF.taux2 * (concub) * (al_pac == 0) + \
         al.TF.taux3 * (al_pac == 1) + \
         al.TF.taux4 * (al_pac == 2) + \
         al.TF.taux5 * (al_pac == 3) + \
         al.TF.taux6 * (al_pac >= 4) + \
         al.TF.taux7 * (al_pac > 4) * (al_pac - 4)

    # Loyer de référence
    L_Ref = z2.L1 * (isol) * (al_pac == 0) + \
            z2.L2 * (concub) * (al_pac == 0) + \
            z2.L3 * (al_pac >= 1) + \
            z2.L4 * (al_pac > 1) * (al_pac - 1)

    RL = L / L_Ref

    # TODO: paramètres en dur ??
    TL = max_(max_(0, al.TL.taux2 * (RL - 0.45)), al.TL.taux3 * (RL - 0.75) + al.TL.taux2 * (0.75 - 0.45))

    Tp = TF + TL

    PP = Po + Tp * Rp
    al_loc = max_(0, E - PP) * loca
    al_loc = al_loc * (al_loc >= al.autres.nv_seuil)

    # # TODO: APL pour les accédants à la propriété
    al_acc = 0 * acce
    # # APL (tous)

    if charge_loyer.active:
        al = 12 * (al_loc + al_acc) * not_(nat_imp)
    else:
        al = 12 * (al_loc + al_acc)

    return al

def _alf(al, al_pac, so):
    '''
    Allocation logement familiale
    '''
    alf = (al_pac >= 1) * (so != 3) * al  # TODO: également pour les jeunes ménages et femems enceints
    return alf


def _als_nonet(self, al, al_pac, etu_holder, so):
    '''
    Allocation logement sociale (non étudiante)
    '''
    etu = self.split_by_roles(etu_holder, roles = [CHEF, PART])

    als = (al_pac == 0) * (so != 3) * not_(etu[CHEF] | etu[PART]) * al
    return als


def _alset(self, al, al_pac, etu_holder, so):
    '''
    Allocation logement sociale étudiante
    '''
    etu = self.split_by_roles(etu_holder, roles = [CHEF, PART])

    alset = (al_pac == 0) * (so != 3) * (etu[CHEF] | etu[PART]) * al
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
    # TODO:
    return al * (so == 3)


def _crds_lgtm(al, crds = law.fam.af.crds):
    '''
    CRDS des allocations logement
    '''
    return -al * crds


def _zone_apl(code_postal):
    """Retrouve la zone d'allocation personnelle au logement de la commune."""
    global zone_apl_by_code_postal
    if zone_apl_by_code_postal is None:
        with pkg_resources.resource_stream(data_resources.__name__, 'code_apl') as code_apl_file:
            zone_apl_by_code_postal = dict(
                (int(code_postal_str), int(zone))
                for code_postal_str, (name, zone) in cPickle.load(code_apl_file).iteritems()
                )
    return fromiter(
        (
            zone_apl_by_code_postal.get(code_postal_cell, 2)
            for code_postal_cell in code_postal
            ),
        dtype = int16,
        )
