# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division

from numpy import logical_not as not_, maximum as max_, minimum as min_

from .input_variables.base import QUIMEN, QUIFOY


PREF = QUIMEN['pref']
VOUS = QUIFOY['vous']


def _exonere_taxe_habitation(self, zthabm, aah, aspa, asi, age_holder, isf_tot_holder, rfr_holder, statmarit_holder, nbptr_holder, _P):
    '''
    Taxe d'habitation
    'men'

    Eligibilité:
    - âgé de plus de 60 ans, non soumis à l'impôt de solidarité sur la fortune (ISF) en n-1
    - veuf quel que soit votre âge et non soumis à l'impôt de solidarité sur la fortune (ISF) n-1
    - titulaire de l'allocation de solidarité aux personnes âgées (Aspa)  ou de l'allocation supplémentaire d'invalidité (Asi),
    bénéficiaire de l'allocation aux adultes handicapés (AAH),
    atteint d'une infirmité ou d'une invalidité vous empêchant de subvenir à vos besoins par votre travail.
    '''
    isf_tot = self.cast_from_entity_to_role(isf_tot_holder, role = VOUS)
    isf_tot = self.sum_by_entity(isf_tot)
    rfr = self.cast_from_entity_to_role(rfr_holder, role = VOUS)
    rfr = self.sum_by_entity(rfr)
    nbptr = self.cast_from_entity_to_role(nbptr_holder, role = VOUS)
    nbptr = self.sum_by_entity(nbptr)
    age = self.filter_role(age_holder, role = PREF)
    statmarit = self.filter_role(statmarit_holder, role = PREF)

    P = _P.cotsoc.gen
    concern = ((age >= 60) + (statmarit == 4)) * (isf_tot <= 0) + (aspa > 0) + (asi > 0)
    seuil_th = P.plaf_th_1 + P.plaf_th_supp * (max_(0, (nbptr - 1) / 2))
    elig = concern * (rfr < seuil_th) + (asi > 0) + (aspa > 0)
    return not_(elig)


def _tax_hab(self, zthabm, exonere_taxe_habitation, nbF, nbJ, rfr_n_1):
    # Documentation voir http://www2.impots.gouv.fr/documentation/2013/idl/files/assets/common/downloads/publication.pdf
    # Variables TODO: à inclure dans la fonction
    valeur_locative_brute = 0
    valeur_locative_moyenne = 0  # déped de la collectivité)

    # Paramètres: à inclure dans param.xml
    taux_minimal_2_premiers = .1  # minimun depusi 2011
    majoration_2_premiers = 0
    taux_minimal_3_et_plus = .15
    majoration_3_et_plus = 0

    abattement_general_base_forfaitaire = 0  # si non nul le taux suivant est nul
    taux_abattement_general_base = .1  # entre 1% et 15% depuis 2011

    taux_special_modeste = 0
    seuil_elig_special_modeste = 1.3  # 130 % de la valeur locative moyenne
    seuil_elig_special_modeste_add = .1  # 10% par personne à charge en garde exclusive et 5% en garde altennée

    taux_special_invalide = .1  # 10% si l'abattement est voté est en vigueur

    taux_imposition = .10  # TODO: taux d'imposition voté par les colloc

    # abattements pour l'habitation principale

    #   abattements obligatoires pour charges de famille

    # * les enfants du contribuable, de son conjoint ou les enfants recueillis qui sont pris en compte pour le
    # calcul de l’impôt sur le revenu (2). Ne sont pas concernés ceux pour lesquels le redevable déduit de ses
    # revenus imposables une pension alimentaire ;
    pac_enf = nbF + nbJ  # TODO: inclure ceux du conjoint non présent sur la feuille d'impôt ? gestion des gardes alternées

    # * les ascendants du contribuable et ceux de son conjoint remplissant les 3 conditions suivantes :
    # – être âgés de plus de 70 ans ou infirmes (c’est-à-dire ne pouvant subvenir par leur travail aux nécessités
    # de l’existence),
    # – résider avec lui,
    # – et disposer d’un revenu fiscal de référence pour l’année précédente n’excédant pas la limite prévue à
    # l’article 1417-I du CGI (voir page 94).

    pac_asc = 0  # TODO

    taux_2_premiers = taux_minimal_2_premiers + majoration_2_premiers
    taux_3_et_plus = taux_minimal_3_et_plus + majoration_3_et_plus

    abattement_obligatoire = (min_(pac_enf + pac_asc, 2) * taux_2_premiers
       + max_(pac_enf + pac_asc - 2, 0) * taux_3_et_plus) * valeur_locative_moyenne

    #   abattements facultatifs à la base :
    #     abattement faculattif général

    abattement_general = abattement_general_base_forfaitaire + taux_abattement_general_base * valeur_locative_moyenne

    #     abattement facultatif dit spécial en faveur des personnes dont le « revenu fiscal de référence » n’excède pas certaines limites

    # Il est institué à l’initiative des communes et EPCI à fiscalité propre ; il est indépendant de l’abattement géné-
    # ral à la base avec lequel il peut se cumuler. Il ne s’applique pas dans les départements d’outre-mer.
    # Son taux peut être fixé, selon la décision des communes et EPCI à fiscalité propre qui en décident
    # l’application, à une valeur entière comprise entre 1 et 15 % de la valeur locative moyenne des habitations
    # (pour rappel, jusqu’en 2011, les taux pouvaient être fixés à 5 %, 10 % ou 15 %)
    #
    # Pour bénéficier de cet abattement, les contribuables doivent remplir deux conditions :

    abattement_special_modeste = (valeur_locative_brute <= ((seuil_elig_special_modeste + seuil_elig_special_modeste_add * (pac_enf + pac_asc)) * valeur_locative_moyenne)
 #       ) * (rfr_n_1 <= 100  # TODO
        ) * taux_special_modeste * valeur_locative_moyenne

    #     abattement facultatif en faveur des personnes handicapées ou invalides.
    abattement_special_invalide = 0 * taux_special_invalide  # Tous les habitants doivent êtres invalides

    base_nette = valeur_locative_brute - (
        abattement_obligatoire + abattement_general + abattement_special_modeste + abattement_special_invalide)

    cotisation_brute = base_nette * taux_imposition

    # Frais de gestion
    #     FRAIS DE GESTION DE LA
    # FISCALITÉ DIRECTE LOCALE (art. 1641 du CGI)
    # En contrepartie des frais de confection des
    # rôles et de dégrèvement qu’il prend à sa
    # charge, l’État perçoit une somme égale à :
    # - 3 %
    # (1) des cotisations perçues au profit
    # des communes et EPCI à fiscalité propre,
    # ramenée à 1 % pour les locaux meublés
    # affectés à l’habitation principale ;
    # - 8 % (2) des cotisations perçues au profit
    # des syndicats de communes ;
    # - 9 % (2) des cotisations perçues au profit
    # des établissements publics bénéficiaires de
    # taxes spéciales d’équipement (TSE).
    # (1) Dont frais de dégrèvement et de non-valeurs : 2 %.
    # (2) Dont frais de dégrèvement et de non-valeurs : 3,6 %.
    frais_gestion = 0

    # Prélèvement pour base élevée et sur les résidences secondaires
    prelevement_residence_secondaire = 0  # TODO


    return -zthabm * 0
