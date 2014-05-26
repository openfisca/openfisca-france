# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)

from __future__ import division

from numpy import (zeros, maximum as max_, minimum as min_, logical_not as not_)
from openfisca_core.accessors import law

from .input_variables.base import QUIFAM, QUIFOY


CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
VOUS = QUIFOY['vous']


def _acs_montant(self, age_holder, P = law.cmu):
    '''
    Calcule le montant de l'ACS en cas d'éligibilité
    '''
    ages_couple = self.split_by_roles(age_holder, roles = [CHEF, PART])
    ages_pac = self.split_by_roles(age_holder, roles = ENFS)
    return ((nb_par_age(ages_couple, 0, 15) + nb_par_age(ages_pac, 0, 15)) * P.acs_moins_16_ans +
       (nb_par_age(ages_couple, 16, 49) + nb_par_age(ages_pac, 16, 25)) * P.acs_16_49_ans +
       nb_par_age(ages_couple, 50, 59) * P.acs_50_59_ans +
       nb_par_age(ages_couple, 60, 200) * P.acs_plus_60_ans)


def _cmu_forfait_logement_base(cmu_nbp_foyer, P = law.cmu.forfait_logement, law_rsa = law.minim.rmi):
    '''
    Calcule le forfait logement applicable en cas de propriété ou d'occupation à titre gratuit
    '''
    return forfait_logement(cmu_nbp_foyer, P, law_rsa)


def _cmu_forfait_logement_al(cmu_nbp_foyer, P = law.cmu.forfait_logement_al, law_rsa = law.minim.rmi):
    '''
    Calcule le forfait logement applicable en cas d'aide au logement
    '''
    return forfait_logement(cmu_nbp_foyer, P, law_rsa)


def _cmu_nbp_foyer(nb_par, cmu_nb_pac):
    '''
    Calcule le nombre de personnes dans le foyer CMU
    '''
    return nb_par + cmu_nb_pac


def _cmu_c_plafond(cmu_nbp_foyer, P = law.cmu):
    '''
    Calcule le plafond de ressources pour la CMU complémentaire
    TODO: Rajouter la majoration pour les DOM
    '''
    return (P.plafond_base * (1 +
        (cmu_nbp_foyer >= 2) * P.coeff_p2 +
        min_(2, cmu_nbp_foyer - 2) * P.coeff_p3_p4 +
        max_(0, cmu_nbp_foyer - 4) * P.coeff_p5_plus
    ))


def _acs_plafond(cmu_c_plafond, P = law.cmu):
    '''
    Calcule le plafond de ressources pour l'ACS
    '''
    return cmu_c_plafond * P.majoration_plafond_acs


def _cmu_br_i(activite, sali, choi, rsti, alr, P = law.cmu):
    '''
    Calcule la base de ressource d'un individu pour la CMU
    '''
    return sali * (1 - (activite == 1) * P.abattement_chomage) + choi + rsti + alr


def _cmu_br(self, so_holder, apl_holder, als_holder, alf_holder, cmu_forfait_logement_base, cmu_forfait_logement_al, age_holder, cmu_br_i_holder, P = law.cmu):
    '''
    Calcule la base de ressources du foyer CMU
    '''
    so = self.cast_from_entity_to_roles(so_holder)
    so = self.filter_role(so, role = CHEF)
    apl = self.cast_from_entity_to_roles(apl_holder)
    apl = self.filter_role(apl, role = CHEF)
    als = self.cast_from_entity_to_roles(als_holder)
    als = self.filter_role(als, role = CHEF)
    alf = self.cast_from_entity_to_roles(alf_holder)
    alf = self.filter_role(alf, role = CHEF)

    cmu_br_i_par = self.split_by_roles(cmu_br_i_holder, roles = [CHEF, PART])
    cmu_br_i_pac = self.split_by_roles(cmu_br_i_holder, roles = ENFS)
    age_pac = self.split_by_roles(cmu_br_i_holder, roles = ENFS)

    res = (cmu_br_i_par[CHEF] + cmu_br_i_par[PART] +
        ((so == 2) + (so == 6)) * cmu_forfait_logement_base +
        ((alf + alf + als) > 0) * cmu_forfait_logement_al)

    for key, age in age_pac.iteritems():
        res += (0 <= age) * (age <= P.age_limite_pac) * cmu_br_i_pac[key]
    return res


def _cmu_nb_pac(self, age_holder, P = law.cmu):
    '''
    Calcule de nombre d'enfants / personnes à charge à comptabiliser dans la famille CMU
    '''
    ages = self.split_by_roles(age_holder, roles = ENFS)
    return nb_par_age(ages, 0, P.age_limite_pac)


def _cmu_c(cmu_c_plafond, cmu_br):
    '''
    Détermine si le foyer a droit à la CMU complémentaire
    '''
    return cmu_br <= cmu_c_plafond


def _acs(cmu_c, acs_plafond, cmu_br, acs_montant):
    '''
    Calcule le montant de l'ACS auquel le foyer a droit
    '''
    return not_(cmu_c) * (cmu_br <= acs_plafond) * acs_montant


############################################################################
# Helper functions
############################################################################
def nb_par_age(ages, min, max):
    '''
    Calcule le nombre d'individus ayant un âge compris entre min et max
    '''
    res = None
    for key, age in ages.iteritems():
        if res is None: res = zeros(len(age))
        res += (min <= age) & (age <= max)
    return res


def rsa_socle_base(nbp, P):
    '''
    Calcule le RSA socle du foyer pour nombre de personnes donné
    '''
    return P.rmi * (1 + P.txp2 * (nbp >= 2) + P.txp3 * (nbp >= 3) + P.txps * max_(0, nbp - 3))

def forfait_logement(nbp_foyer, P, law_rsa):
    '''
    Calcule le forfait logement en fonction du nombre de personnes dans le "foyer CMU" et d'un jeu de taux
    '''
    return (12 * rsa_socle_base(nbp_foyer, law_rsa) *
        ((nbp_foyer == 1) * P.taux_1p + (nbp_foyer == 2) * P.taux_2p + (nbp_foyer > 2) * P.taux_3p_plus))
