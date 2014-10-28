# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)

from __future__ import division

from numpy import (zeros, maximum as max_, minimum as min_, logical_not as not_, logical_or as or_)
from numpy.core.defchararray import startswith

from openfisca_core.accessors import law
from openfisca_core.columns import BoolCol, FloatCol
from openfisca_core.formulas import SimpleFormulaColumn

from .base import QUIFAM, QUIFOY, reference_formula
from ..entities import Familles, Individus


CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
VOUS = QUIFOY['vous']


def _acs_montant__2009(self, age_holder):
    '''
    Calcule le montant de l'ACS en cas d'éligibilité (jusqu'au 31 juillet 2009)
    '''
    # TODO
    ages = self.filter_role(age_holder, role = CHEF)
    return 0*ages


def _acs_montant_2009_(self, age_holder, P = law.cmu):
    '''
    Calcule le montant de l'ACS en cas d'éligibilité (à compter du 1 août 2009)
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


def _cmu_eligible_majoration_dom(self, depcom_holder):
    depcom = self.cast_from_entity_to_roles(depcom_holder)
    depcom = self.filter_role(depcom, role = CHEF)

    return startswith(depcom, '971') | startswith(depcom, '972') | startswith(depcom, '973') | startswith(depcom, '974')


def _cmu_c_plafond(self, cmu_eligible_majoration_dom, cmu_nbp_foyer, P = law.cmu):
    '''
    Calcule le plafond de ressources pour la CMU complémentaire
    TODO: Rajouter la majoration pour les DOM
    '''
    return (P.plafond_base *
        (1 + cmu_eligible_majoration_dom * P.majoration_dom) *
        (1 + (cmu_nbp_foyer >= 2) * P.coeff_p2 +
            max_(0, min_(2, cmu_nbp_foyer - 2)) * P.coeff_p3_p4 +
            max_(0, cmu_nbp_foyer - 4) * P.coeff_p5_plus))


def _acs_plafond(cmu_c_plafond, P = law.cmu):
    '''
    Calcule le plafond de ressources pour l'ACS
    '''
    return cmu_c_plafond * (1 + P.majoration_plafond_acs)


@reference_formula
class cmu_br_i(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressources de l'individu prise en compte pour l'éligibilité à la CMU-C / ACS"
    entity_class = Individus
    period_unit = 'year'

    def function(self, activite, salnet, chonet, rstnet, alr, rsa_base_ressources_patrimoine_i, aah, indemnites_journalieres_maternite,
                 indemnites_journalieres_maladie, indemnites_journalieres_maladie_professionnelle, indemnites_journalieres_accident_travail,
                 indemnites_stage, revenus_stage_formation_pro, allocation_securisation_professionnelle, prime_forfaitaire_mensuelle_reprise_activite,
                 dedommagement_victime_amiante, prestation_compensatoire, retraite_combattant, pensions_invalidite,
                 indemnites_chomage_partiel, bourse_enseignement_sup, bourse_recherche, gains_exceptionnels, P = law.cmu):
        return ((salnet + revenus_stage_formation_pro + indemnites_chomage_partiel) * (1 - (activite == 1) * P.abattement_chomage) +
            indemnites_stage + aah + chonet + rstnet + alr + rsa_base_ressources_patrimoine_i + allocation_securisation_professionnelle +
            indemnites_journalieres_maternite + indemnites_journalieres_accident_travail + indemnites_journalieres_maladie + indemnites_journalieres_maladie_professionnelle +
            prime_forfaitaire_mensuelle_reprise_activite + dedommagement_victime_amiante + prestation_compensatoire +
            retraite_combattant + pensions_invalidite + bourse_enseignement_sup + bourse_recherche + gains_exceptionnels)

    def get_variable_period(self, output_period, variable_name):
        if variable_name == 'activite':
            return output_period
        else:
            return output_period.offset(-1)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class cmu_br(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base de ressources prise en compte pour l'éligibilité à la CMU-C / ACS"
    entity_class = Familles
    period_unit = 'year'

    def function(self, so_holder, apl_holder, als_holder, alf_holder, cmu_forfait_logement_base, cmu_forfait_logement_al, age_holder, cmu_br_i_holder, P = law.cmu):
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
            ((alf + apl + als) > 0) * cmu_forfait_logement_al)

        for key, age in age_pac.iteritems():
            res += (0 <= age) * (age <= P.age_limite_pac) * cmu_br_i_pac[key]
        return res

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


def _cmu_nb_pac(self, age_holder, P = law.cmu):
    '''
    Calcule de nombre d'enfants / personnes à charge à comptabiliser dans la famille CMU
    '''
    ages = self.split_by_roles(age_holder, roles = ENFS)
    return nb_par_age(ages, 0, P.age_limite_pac)


@reference_formula
class cmu_c(SimpleFormulaColumn):
    '''
    Détermine si le foyer a droit à la CMU complémentaire
    '''
    column = BoolCol
    label = u"Éligibilité à la CMU-C"
    entity_class = Familles
    period_unit = 'year'

    def function(self, cmu_c_plafond, cmu_br, period):
        return cmu_br <= cmu_c_plafond

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


@reference_formula
class acs(SimpleFormulaColumn):
    '''
    Calcule le montant de l'ACS auquel le foyer a droit
    '''
    column = FloatCol
    label = u"Éligibilité à l'ACS"
    entity_class = Familles
    period_unit = 'year'

    def function(self, cmu_c, cmu_br, acs_plafond, acs_montant):
        return not_(cmu_c) * (cmu_br <= acs_plafond) * acs_montant

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('year')


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
