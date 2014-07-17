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

from .input_variables.base import QUIFAM, QUIFOY


CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
VOUS = QUIFOY['vous']


def _nb_par(self, quifam_holder):
    '''
    Nombre d'adultes (parents) dans la famille
    'fam'
    '''
    quifam = self.filter_role(quifam_holder, role = PART)

    return 1 + 1 * (quifam == 1)


def _maries(self, statmarit_holder):
    '''
    couple = 1 si couple marié sinon 0 TODO faire un choix avec couple ?
    '''
    statmarit = self.filter_role(statmarit_holder, role = CHEF)

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


def _biact(self, br_pf_i_holder, _P):
    '''
    Indicatrice de biactivité des adultes de la famille
    '''
    br_pf_i = self.split_by_roles(br_pf_i_holder, roles = [CHEF, PART])

    seuil_rev = 12 * _P.fam.af.bmaf_n_2
    biact = (br_pf_i[CHEF] >= seuil_rev) & (br_pf_i[PART] >= seuil_rev)
    return biact


def _div(self, rpns_pvce, rpns_pvct, rpns_mvct, rpns_mvlt, f3vc_holder, f3ve_holder, f3vg_holder, f3vh_holder,
        f3vl_holder, f3vm_holder):
    f3vc = self.cast_from_entity_to_role(f3vc_holder, role = VOUS)
    f3ve = self.cast_from_entity_to_role(f3ve_holder, role = VOUS)
    f3vg = self.cast_from_entity_to_role(f3vg_holder, role = VOUS)
    f3vh = self.cast_from_entity_to_role(f3vh_holder, role = VOUS)
    f3vl = self.cast_from_entity_to_role(f3vl_holder, role = VOUS)
    f3vm = self.cast_from_entity_to_role(f3vm_holder, role = VOUS)

    return f3vc + f3ve + f3vg - f3vh + f3vl + f3vm + rpns_pvce + rpns_pvct - rpns_mvct - rpns_mvlt

def _rev_coll(self, rto_net, rev_cap_lib_holder, rev_cat_rvcm_holder, div, abat_spe_holder, glo, fon_holder, alv,
        f7ga_holder, f7gb_holder, f7gc_holder, rev_cat_pv_holder):
    '''
    Revenus collectifs
    '''
    # TODO: ajouter les revenus de l'étranger etr*0.9
    # alv is negative since it is paid by the declaree
    rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)
    rev_cat_rvcm = self.cast_from_entity_to_role(rev_cat_rvcm_holder, role = VOUS)
    abat_spe = self.cast_from_entity_to_role(abat_spe_holder, role = VOUS)
    fon = self.cast_from_entity_to_role(fon_holder, role = VOUS)
    f7ga = self.cast_from_entity_to_role(f7ga_holder, role = VOUS)
    f7gb = self.cast_from_entity_to_role(f7gb_holder, role = VOUS)
    f7gc = self.cast_from_entity_to_role(f7gc_holder, role = VOUS)
    rev_cat_pv = self.cast_from_entity_to_role(rev_cat_pv_holder, role = VOUS)

    return rto_net + rev_cap_lib + rev_cat_rvcm + fon + glo + alv - f7ga - f7gb - f7gc - abat_spe + rev_cat_pv


def _br_pf(self, br_pf_i_holder, rev_coll_holder):
    '''
    Base ressource des prestations familiales de la famille
    'fam'
    '''
    br_pf_i = self.split_by_roles(br_pf_i_holder, roles = [CHEF, PART])
    rev_coll = self.split_by_roles(rev_coll_holder, roles = [CHEF, PART])

    br_pf = br_pf_i[CHEF] + br_pf_i[PART] + rev_coll[CHEF] + rev_coll[PART]
    return br_pf


############################################################################
# Complément familial
############################################################################


def _cf(self, age_holder, br_pf, isol, biact, smic55_holder, _P):
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
    age = self.split_by_roles(age_holder, roles = ENFS)
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

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

def _asf_elig(self, caseT_holder, caseL_holder):
    '''
    Eligibilté à l'allocation de soutien familial (ASF)
    '''
    caseT = self.cast_from_entity_to_role(caseT_holder, role = VOUS)
    caseT = self.any_by_roles(caseT)
    caseL = self.cast_from_entity_to_role(caseL_holder, role = VOUS)
    caseL = self.any_by_roles(caseL)
    return caseT | caseL


def _asf(self, age_holder, isol, asf_elig, smic55_holder, alr_holder, _P):
    '''
    Allocation de soutien familial

    L’ASF permet d’aider le conjoint survivant ou le parent isolé ayant la garde
    d’un enfant et les familles ayant à la charge effective et permanente un enfant
    orphelin.
    Vous avez au moins un enfant à votre charge. Vous êtes son père ou sa mère et vous vivez seul(e),
    ou vous avez recueilli cet enfant et vous vivez seul ou en couple.

    http://www.caf.fr/aides-et-services/s-informer-sur-les-aides/solidarite-et-insertion/l-allocation-de-soutien-familial-asf
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    alr = self.sum_by_entity(alr_holder)
    # TODO: what is rst doing here?
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

    # TODO: Ajouter orphelin recueilli, soustraction à l'obligation d'entretien (et date de celle-ci),
    # action devant le TGI pour complêter l'éligibilité

    # TODO: la valeur est annualisé mais l'ASF peut ne pas être versée toute l'année
    P = _P.fam
    asf_nbenf = nb_enf(age, smic55, P.af.age1, P.af.age2)
    asf_nbenfa = asf_nbenf

    asf_brut = isol * asf_elig * max_(0, asf_nbenfa * 12 * P.af.bmaf * P.asf.taux1)

    no_alr = not_(alr > 0)
    return asf_brut * no_alr


def _ars(self, age_holder, af_nbenf, smic55_holder, br_pf, _P):
    '''
    Allocation de rentrée scolaire brute de CRDS
    '''
    # TODO: convention sur la mensualisation
    # On tient compte du fait qu'en cas de léger dépassement du plafond, une allocation dégressive
    # (appelée allocation différentielle), calculée en fonction des revenus, peut être versée.
    age = self.split_by_roles(age_holder, roles = ENFS)
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

    P = _P.fam
    bmaf = P.af.bmaf
    # On doit prendre l'âge en septembre
    enf_05 = nb_enf(age, smic55, P.ars.agep - 1, P.ars.agep - 1)  # 5 ans et 6 ans avant le 31 décembre
    # enf_05 = 0
    # Un enfant scolarisé qui n'a pas encore atteint l'âge de 6 ans
    # avant le 1er février 2012 peut donner droit à l'ARS à condition qu'il
    # soit inscrit à l'école primaire. Il faudra alors présenter un
    # certificat de scolarité.
    enf_primaire = enf_05 + nb_enf(age, smic55, P.ars.agep, P.ars.agec - 1)
    enf_college = nb_enf(age, smic55, P.ars.agec, P.ars.agel - 1)
    enf_lycee = nb_enf(age, smic55, P.ars.agel, P.ars.ages)

    arsnbenf = enf_primaire + enf_college + enf_lycee

    # Plafond en fonction du nb d'enfants A CHARGE (Cf. article R543)
    ars_plaf_res = P.ars.plaf * (1 + af_nbenf * P.ars.plaf_enf_supp)
    arsbase = bmaf * (P.ars.tx0610 * enf_primaire +
                     P.ars.tx1114 * enf_college +
                     P.ars.tx1518 * enf_lycee)
    # Forme de l'ARS  en fonction des enfants a*n - (rev-plaf)/n
    # ars_diff = (ars_plaf_res + arsbase - br_pf) / arsnbenf
    ars = (arsnbenf > 0) * max_(0, arsbase - max_(0, (br_pf - ars_plaf_res) / max_(1, arsnbenf)))
    # Calcul net de crds : ars_net = (P.ars.enf0610 * enf_primaire + P.ars.enf1114 * enf_college + P.ars.enf1518 * enf_lycee)

    return ars * (ars >= P.ars.seuil_nv)


def _cf_cumul(paje_base_temp, apje_temp, ape_temp, cf_temp):
    '''
    L'allocation de base de la paje n'est pas cumulable avec le complément familial
    '''
    cf_brut = (paje_base_temp < cf_temp) * (apje_temp <= cf_temp) * (ape_temp <= cf_temp) * cf_temp
    return round(cf_brut, 2)


############################################################################
# Enfant handicapé
############################################################################


def _aeeh_2003_(self, age_holder, inv_holder, isol, categ_inv_holder, _P):
    '''
    Allocation d'éducation de l'enfant handicapé (Allocation d'éducation spécialisée avant le 1er janvier 2006)

    Ce montant peut être majoré par un complément accordé par la Cdaph qui prend en compte :
    le coût du handicap de l'enfant,
    la cessation ou la réduction d'activité professionnelle d'un ou l'autre des deux parents,
    l'embauche d'une tierce personne rémunérée.

    Une majoration est versée au parent isolé bénéficiaire d'un complément d'Aeeh lorsqu'il cesse ou réduit son activité
    professionnelle ou lorsqu'il embauche une tierce personne rémunérée.
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    categ_inv = self.split_by_roles(categ_inv_holder, roles = ENFS)
    inv = self.split_by_roles(inv_holder, roles = ENFS)

    P = _P.fam
    isole = isol

    aeeh = 0
    for enfant in age.iterkeys():
        enfhand = inv[enfant] * (age[enfant] < P.aeeh.age) / 12
        categ = categ_inv[enfant]
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

def _aeeh__2002(self, age_holder, inv_holder, isol, categ_inv_holder, _P):
    '''
    Allocation d'éducation de l'enfant handicapé (Allocation d'éducation spécialisée avant le 1er janvier 2006)

    Ce montant peut être majoré par un complément accordé par la Cdaph qui prend en compte :
    le coût du handicap de l'enfant,
    la cessation ou la réduction d'activité professionnelle d'un ou l'autre des deux parents,
    l'embauche d'une tierce personne rémunérée.

    Une majoration est versée au parent isolé bénéficiaire d'un complément d'Aeeh lorsqu'il cesse ou réduit son activité
    professionnelle ou lorsqu'il embauche une tierce personne rémunérée.
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    categ_inv = self.split_by_roles(categ_inv_holder, roles = ENFS)
    inv = self.split_by_roles(inv_holder, roles = ENFS)

    P = _P.fam
    isole = isol

    aeeh = 0
    for enfant in age.iterkeys():
        enfhand = inv[enfant] * (age[enfant] < P.aeeh.age) / 12
        categ = categ_inv[enfant]
        aeeh += 0 * enfhand  # TODO:

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


def _crds_pfam(af, cf, asf, ars, paje, ape, apje, _P):
    '''
    Renvoie la CRDS des prestations familiales
    '''
    return -(af + cf + asf + ars + paje + ape + apje) * _P.fam.af.crds


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
        isbenjamin = (agem < agem_benjamin) & (agem != -9999)
        agem_benjamin = isbenjamin * agem + not_(isbenjamin) * agem_benjamin
    return agem_benjamin
