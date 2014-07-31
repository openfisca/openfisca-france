# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import division

from numpy import (maximum as max_, logical_not as not_)
from openfisca_core.accessors import law

from ..input_variables.base import QUIFAM, QUIFOY

CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
VOUS = QUIFOY['vous']
CONJ = QUIFOY['conj']


def _br_mv_i(self, sali, choi, rsti, alr, rto, rpns, rev_cap_bar_holder, rev_cap_lib_holder, rfon_ms, div_ms):
    '''
    Base ressource individuelle du minimum vieillesse et assimilés (ASPA)
    'ind'
    '''
    rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = VOUS)
    rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)

    out = (sali + choi + rsti + alr + rto + rpns +
           max_(0, rev_cap_bar) + max_(0, rev_cap_lib) + max_(0, rfon_ms) + max_(0, div_ms)
           # max_(0,etr) +
           )
    return out


def _br_mv(self, br_mv_i_holder):
    '''
    Base ressource du minimum vieillesse et assimilés (ASPA)
    'fam'

    Ressources prises en compte
    Tous les avantages de vieillesse et d'invalidité dont bénéficie l'intéressé sont pris en compte dans l'appréciation des ressources, de même que les revenus professionnels, les revenus des biens mobiliers et immobiliers et les biens dont il a fait donation dans les 10 années qui précèdent la demande d'Aspa.
    L'évaluation des ressources d'un couple est effectuée de la même manière, sans faire la distinction entre les biens propres ou les biens communs des conjoints, concubins ou partenaires liés par un Pacs.
    Ressources exclues
    Certaines ressources ne sont toutefois pas prises en compte dans l'estimation des ressources. Il s'agit notamment :
    de la valeur des locaux d'habitation occupés par le demandeur et les membres de sa famille vivant à son foyer lorsqu'il s'agit de sa résidence principale,
    des prestations familiales,
    de l'allocation de logement sociale,
    des majorations prévues par la législation, accordées aux personnes dont l'état de santé nécessite l'aide constante d'une tierce personne,
    de la retraite du combattant,
    des pensions attachées aux distinctions honorifiques,
    de l'aide apportée ou susceptible d'être apportée par les personnes tenues à l'obligation alimentaire.
    '''
    br_mv_i = self.split_by_roles(br_mv_i_holder, roles = [CHEF, PART])
    return br_mv_i[CHEF] + br_mv_i[PART]


#    Bloc ASPA/ASI
#    Allocation de solidarité aux personnes agées (ASPA)
#    et Allocation supplémentaire d'invalidité (ASI)

# ASPA crée le 1er janvier 2006
# TODO Allocation supplémentaire avant la loi de  2006 (entrée en vigueur au 1er janvier 2007)

# ASPA:
# Anciennes allocations du minimum vieillesse remplacées par l'ASPA
#
# Il s'agit de :
#    l'allocation aux vieux travailleurs salariés (AVTS),
#    l'allocation aux vieux travailleurs non salariés,
#    l'allocation aux mères de familles,
#    l'allocation spéciale de vieillesse,
#    l'allocation supplémentaire de vieillesse,
#    l'allocation de vieillesse agricole,
#    le secours viager,
#    la majoration versée pour porter le montant d'une pension de vieillesse au niveau de l'AVTS,
#    l'allocation viagère aux rapatriés âgés.

# ASI:
#        L'ASI peut être attribuée aux personnes atteintes d'une invalidité générale
#        réduisant au moins des deux tiers leur capacité de travail ou de gain.
#        Les personnes qui ont été reconnues atteintes d'une invalidité générale réduisant
#        au moins des deux tiers leur capacité de travail ou de gain pour l'attribution d'un
#        avantage d'invalidité au titre d'un régime de sécurité sociale résultant de
#        dispositions législatives ou réglementaires sont considérées comme invalides.

#        Le droit à l'ASI prend fin dès lors que le titulaire remplit la condition d'âge pour bénéficier de l'ASPA.
#        Le titulaire de l'ASI est présumé inapte au travail pour l'attribution de l'ASPA. (cf. par analogie circulaire n° 70 SS du 05/08/1957 - circulaire Cnav 28/85 du 26/02/1985 - Lettre Cnav du 15.04.1986)
#        Le droit à l'ASI prend donc fin au soixantième anniversaire du titulaire. En pratique, l'allocation est supprimée au premier
#        jour du mois civil suivant le 60ème anniversaire.

#        Plafond de ressources communs depuis le 1er janvier 2006
#        Changement au 1er janvier 2009 seulement pour les personnes seules !
#        P.aspa.plaf_couple = P.asi.plaf_couple mais P.aspa.plaf_seul = P.asi.plaf_seul

#    Minimum vieillesse - Allocation de solidarité aux personnes agées (ASPA)
# age minimum (CSS R815-2)
# base ressource R815-25:
#   - retraite, pensions et rentes,
#   - allocation spéciale (L814-1);
#   - allocation aux mères de famille (L813)
#   - majorations pour conjoint à charge des retraites
#   - pas de prise en compte des allocations logement, des prestations
#   familiales, de la rente viagère rapatriée...
# TODO: ajouter taux de la majoration pour 3 enfants 10% (D811-12) ?
#       P.aspa.maj_3enf = 0.10;

def _aspa_elig(age, inv, P = law.minim):
    '''
    Eligibitié individuelle à l'ASPA (Allocation de solidarité aux personnes agées)
    'ind'
    '''
    condition_age = (age >= P.aspa.age_min) | ((age >= P.aah.age_legal_retraite) & inv)
    return condition_age


def _asi_elig(aspa_elig, inv, activite):
    '''
    Éligibilité individuelle à l'ASI (Allocation supplémentaire d'invalidité)
    'ind'
    '''
    return inv & (activite >= 3) & not_(aspa_elig)


def _asi_aspa_nb_alloc(self, aspa_elig_holder, asi_elig_holder):
    '''
    Nombre d'allocataire à l'ASI
    '''
    asi_elig = self.split_by_roles(asi_elig_holder, roles = [CHEF, PART])
    aspa_elig = self.split_by_roles(aspa_elig_holder, roles = [CHEF, PART])

    return (1 * aspa_elig[CHEF] + 1 * aspa_elig[PART] + 1 * asi_elig[CHEF] + 1 * asi_elig[PART])

def _aspa_couple__2006(maries):
    '''
    Détermine si l'on a bien affaire à un couple au sens de l'ASPA
    '''
    return maries


def _aspa_couple_2007_(concub):
    '''
    Détermine si l'on a bien affaire à un couple au sens de l'ASPA
    '''
    return concub


def _aspa(self, asi_elig_holder, aspa_elig_holder, maries, concub, asi_aspa_nb_alloc, br_mv, P = law.minim):
    '''
    Calcule l'allocation de solidarité aux personnes âgées (ASPA)
    '''
    # TODO: Avant la réforme de 2007 n'était pas considéré comme un couple les individus en concubinage ou pacsés.
    # La base de ressources doit pouvoir être individualisée pour refletter ça.

    asi_elig = self.split_by_roles(asi_elig_holder, roles = [CHEF, PART])
    aspa_elig = self.split_by_roles(aspa_elig_holder, roles = [CHEF, PART])

    # Un seul éligible
    elig1 = ((asi_aspa_nb_alloc == 1) & (aspa_elig[CHEF] | aspa_elig[PART]))
    # Couple d'éligibles
    elig2 = (aspa_elig[CHEF] & aspa_elig[PART])
    # Un seul éligible et époux éligible ASI
    elig3 = ((asi_elig[CHEF] & aspa_elig[PART]) | (asi_elig[PART] & aspa_elig[CHEF])) * maries
    # Un seul éligible et conjoint non marié éligible ASI
    elig4 = ((asi_elig[CHEF] & aspa_elig[PART]) | (asi_elig[PART] & aspa_elig[CHEF])) * not_(maries)

    elig = elig1 | elig2 | elig3 | elig4

    montant_max = (elig1 * P.aspa.montant_seul
        + elig2 * P.aspa.montant_couple
        + elig3 * (P.asi.montant_couple / 2 + P.aspa.montant_couple / 2)
        + elig4 * (P.asi.montant_seul + P.aspa.montant_couple / 2))

    ressources = br_mv + montant_max

    plafond_ressources = (elig1 * (P.aspa.plaf_seul * not_(concub) + P.aspa.plaf_couple * concub)
        + (elig2 | elig3 | elig4) * P.aspa.plaf_couple)

    depassement = max_(ressources - plafond_ressources, 0)

    diff = ((elig1 | elig2) * (montant_max - depassement)
        + (elig3 | elig4) * (P.aspa.montant_couple / 2 - depassement / 2))

    montant_servi_aspa = max_(diff, 0) / 12

    print "montant_max: %.0f" % montant_max
    print "ressources: %.0f" % ressources
    print "plafond_ressources: %.0f" % plafond_ressources
    print "depassement: %.0f" % depassement
    print "diff: %.0f" % diff
    print "montant_servi_aspa: %.0f" % montant_servi_aspa

    # TODO: Faute de mieux, on verse l'aspa à la famille plutôt qu'aux individus
    # aspa[CHEF] = aspa_elig[CHEF]*montant_servi_aspa*(elig1 + elig2/2)
    # aspa[PART] = aspa_elig[PART]*montant_servi_aspa*(elig1 + elig2/2)
    return 12 * elig * montant_servi_aspa  # annualisé


def _asi(self, asi_elig_holder, aspa_elig_holder, maries, concub, asi_aspa_nb_alloc, br_mv, P = law.minim):
    '''
    Calcule l'allocation supplémentaire d'invalidité (ASI)
    '''
    asi_elig = self.split_by_roles(asi_elig_holder, roles = [CHEF, PART])
    aspa_elig = self.split_by_roles(aspa_elig_holder, roles = [CHEF, PART])

    # Un seul éligible
    elig1 = ((asi_aspa_nb_alloc == 1) & (asi_elig[CHEF] | asi_elig[PART]))
    # Couple d'éligibles mariés
    elig2 = (asi_elig[CHEF] & asi_elig[PART]) * maries
    # Couple d'éligibles non mariés
    elig3 = (asi_elig[CHEF] & asi_elig[PART]) * not_(maries)
    # Un seul éligible et époux éligible ASPA
    elig4 = ((asi_elig[CHEF] & aspa_elig[PART]) | (asi_elig[PART] & aspa_elig[CHEF])) * maries
    # Un seul éligible et conjoint non marié éligible ASPA
    elig5 = ((asi_elig[CHEF] & aspa_elig[PART]) | (asi_elig[PART] & aspa_elig[CHEF])) * not_(maries)

    elig = elig1 | elig2 | elig3 | elig4 | elig5

    montant_max = (elig1 * P.asi.montant_seul
        + elig2 * P.asi.montant_couple
        + elig3 * 2 * P.asi.montant_seul
        + elig4 * (P.asi.montant_couple / 2 + P.aspa.montant_couple / 2)
        + elig5 * (P.asi.montant_seul + P.aspa.montant_couple / 2))

    ressources = br_mv + montant_max

    plafond_ressources = (elig1 * (P.asi.plaf_seul * not_(concub) + P.asi.plaf_couple * concub)
        + elig2 * P.asi.plaf_couple
        + elig3 * P.asi.plaf_couple
        + elig4 * P.aspa.plaf_couple
        + elig5 * P.aspa.plaf_couple)

    depassement = max_(ressources - plafond_ressources, 0)

    diff = ((elig1 | elig2 | elig3) * (montant_max - depassement)
        + elig4 * (P.asi.montant_couple / 2 - depassement / 2)
        + elig5 * (P.asi.montant_seul - depassement / 2))

    montant_servi_asi = max_(diff, 0) / 12

    # TODO: Faute de mieux, on verse l'asi à la famille plutôt qu'aux individus
    # asi[CHEF] = asi_elig[CHEF]*montant_servi_asi*(elig1*1 + elig2/2 + elig3/2)
    # asi[PART] = asi_elig[PART]*montant_servi_asi*(elig1*1 + elig2/2 + elig3/2)
    return 12 * elig * montant_servi_asi  # annualisé
