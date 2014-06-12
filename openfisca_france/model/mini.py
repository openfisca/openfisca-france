# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


from __future__ import division

from numpy import (floor, maximum as max_, where,
                   logical_not as not_, logical_and as and_,
                   logical_or as or_)
from openfisca_core.accessors import law

from .input_variables.base import QUIFAM, QUIFOY
from .pfam import nb_enf, age_en_mois_benjamin


CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
VOUS = QUIFOY['vous']
CONJ = QUIFOY['conj']


############################################################################
# ASPA /  Minimum vieillesse
############################################################################
def _br_mv_i(self, salbrut, chobrut, rstbrut, alr, rto, rpns, rev_cap_bar_holder, rev_cap_lib_holder, rfon_ms, div_ms):
    '''
    Base ressource individuelle du minimlum vieillesse et assimilés (ASPA)
    'ind'
    '''
    rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = VOUS)
    rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)

    out = (salbrut + chobrut + rstbrut + alr + rto + rpns +
           max_(0, rev_cap_bar) + max_(0, rev_cap_lib) + max_(0, rfon_ms) + max_(0, div_ms)
           # max_(0,etr) +
           )
    return out

def _br_mv(self, br_mv_i_holder):
    '''
    Base ressource du minimlum vieillesse et assimilés (ASPA)
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

    br_mv = br_mv_i[CHEF] + br_mv_i[PART]
    return br_mv


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

def _aspa_elig(age, inv, activite, P = law.minim):
    '''
    Eligibitié individuelle à l'ASPA (Allocation de solidarité aux personnes agées)
    'ind'
    '''
    condition_age = (age >= P.aspa.age_min) | ((age >= P.aah.age_legal_retraite) & inv)
    condition_activite = (activite == 3)
    return condition_age & condition_activite


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
    Calcule l'ASPA lorsqu'il y a un ou deux bénéficiaire de l'ASPA et aucun bénéficiaire de l'ASI
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

    montant_max = elig1 * P.aspa.montant_seul
    + elig2 * P.aspa.montant_couple
    + elig3 * P.asi.montant_couple / 2 + P.aspa.montant_couple / 2
    + elig4 * P.asi.montant_seul + P.aspa.montant_couple / 2

    ressources = br_mv + montant_max

    plafond_ressources = elig1 * (P.aspa.plaf_seul * not_(concub) + P.aspa.plaf_couple * concub)
        + (elig2 | elig3 | elig4) * P.aspa.plaf_couple

    depassement = ressources - plafond_ressources

    diff = (elig1 | elig2) * montant_max - depassement
        + (elig3 | elig4) * P.aspa.montant_couple / 2 - depassement / 2

    montant_servi_aspa = max_(diff, 0) / 12

    # TODO: Faute de mieux, on verse l'aspa à la famille plutôt qu'aux individus
    # aspa[CHEF] = aspa_elig[CHEF]*montant_servi_aspa*(elig1 + elig2/2)
    # aspa[PART] = aspa_elig[PART]*montant_servi_aspa*(elig1 + elig2/2)
    return 12 * elig * (aspa_elig[CHEF] + aspa_elig[PART]) * montant_servi_aspa * ((elig1 | elig3 | elig4) + elig2 / 2)  # annualisé


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

    montant_max = elig1 * P.asi.montant_seul
        + elig2 * P.asi.montant_couple
        + elig3 * 2 * P.asi.montant_seul
        + elig4 * P.asi.montant_couple / 2 + P.aspa.montant_couple / 2
        + elig5 * P.asi.montant_seul + P.aspa.montant_couple / 2

    ressources = br_mv + montant_max

    plafond_ressources = elig1 * (P.asi.plaf_seul * not_(concub) + P.asi.plaf_couple * concub)
        + elig2 * P.asi.plaf_couple
        + elig3 * P.asi.plaf_couple
        + elig4 * P.aspa.plaf_couple
        + elig5 * P.aspa.plaf_couple

    depassement = ressources - plafond_ressources

    diff = (elig1 | elig2 | elig3) * montant_max - depassement
        + elig4 * P.asi.montant_couple / 2 - depassement / 2
        + elig5 * P.asi.montant_seul - depassement / 2

    montant_servi_asi = max_(diff, 0) / 12

    # TODO: Faute de mieux, on verse l'asi à la famille plutôt qu'aux individus
    # asi[CHEF] = asi_elig[CHEF]*montant_servi_asi*(elig1*1 + elig2/2 + elig3/2)
    # asi[PART] = asi_elig[PART]*montant_servi_asi*(elig1*1 + elig2/2 + elig3/2)
    return 12 * elig * (asi_elig[CHEF] + asi_elig[PART]) * montant_servi_asi * ((elig1 | elig4 | elig5) + (elig2 | elig3) / 2)  # annualisé


############################################################################
# RSA / RMI
############################################################################


def _div_ms(self, f3vc_holder, f3ve_holder, f3vg_holder, f3vl_holder, f3vm_holder):
    f3vc = self.cast_from_entity_to_role(f3vc_holder, role = VOUS)
    f3ve = self.cast_from_entity_to_role(f3ve_holder, role = VOUS)
    f3vg = self.cast_from_entity_to_role(f3vg_holder, role = VOUS)
    f3vl = self.cast_from_entity_to_role(f3vl_holder, role = VOUS)
    f3vm = self.cast_from_entity_to_role(f3vm_holder, role = VOUS)

    return f3vc + f3ve + f3vg + f3vl + f3vm


def _rfon_ms(self, f4ba_holder, f4be_holder):
    '''
    Revenus fonciers pour la base ressource du rmi/rsa
    'ind'
    '''
    f4ba = self.cast_from_entity_to_role(f4ba_holder, role = VOUS)
    f4be = self.cast_from_entity_to_role(f4be_holder, role = VOUS)

    return f4ba + f4be


def _ra_rsa(sal, hsup, rpns, etr):
    '''
    Revenus d'activité au sens du Rsa
    'ind'
    '''
    return sal + hsup + rpns + etr


def _br_rmi_pf__2003(self, af_base, cf, asf, apje, ape, _P, P = law.minim):
    """
    Prestations familiales inclues dans la base ressource RSA/RMI
    TO DO: Add mva (majoration vie autonome),
    """
    out = P.rmi.pfInBRrmi * (af_base + cf + asf + apje + ape)
    return self.cast_from_entity_to_role(out, entity = 'famille', role = CHEF)


def _br_rmi_pf_2004_(self, af_base, cf, asf, paje_base, paje_clca, paje_colca, _P, P = law.minim):
    """
    Prestations familiales inclues dans la base ressource RSA/RMI
    TO DO: Add mva (majoration vie autonome),
    """

    out = P.rmi.pfInBRrmi * (af_base + cf + asf + paje_base + paje_clca + paje_colca)

    return self.cast_from_entity_to_role(out, entity = 'famille', role = CHEF)


def _br_rmi_ms(self, aspa, asi, aah, caah):
    """
    Minima sociaux inclus dans la base ressource RSA/RMI
    'ind'
    """
    return self.cast_from_entity_to_role(aspa + asi + aah + caah,
        entity = 'famille', role = CHEF)


def _br_rmi_i(self, ra_rsa, cho, rst, alr, rto, rev_cap_bar_holder, rev_cap_lib_holder, rfon_ms, div_ms):
    '''
    Base ressource individuelle du RSA/RMI
    'ind'
    '''
    rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = VOUS)
    rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)

    return ra_rsa + cho + rst + alr + rto + rev_cap_bar + rev_cap_lib + rfon_ms + div_ms


def _br_rmi(self, br_rmi_pf_holder, br_rmi_ms_holder, br_rmi_i_holder):
    """
    Base ressources du Rmi ou du Rsa

    Sont pris en compte:
    1 L’ensemble des revenus tirés d’une activité salariée ou non salariée ;
    2 Les revenus tirés de stages de formation professionnelle ;
    3 Les revenus tirés de stages réalisés en application de l’article 9 de
      la loi no  2006-396 du 31 mars 2006 pour l’égalité des chances ;
    4 L’aide légale ou conventionnelle aux salariés en chômage partiel ;
    5 Les indemnités perçues à l’occasion des congés légaux de maternité, de paternité ou d’adoption ;
    6 Les indemnités journalières de sécurité sociale, de base et complémentaires, perçues en cas d’incapacité
      physique médicalement constatée de continuer ou de reprendre le travail, d’accident du travail ou de maladie
      professionnelle pendant une durée qui ne peut excéder trois mois à compter de l’arrêt de travail

    On ne tient pas compte:
    1 De la prime à la naissance ou à l’adoption mentionnée à l’article L. 531-2 du code de la sécurité
      sociale ;
    2 De l’allocation de base mentionnée à l’article L. 531-3 du code de la sécurité sociale due pour le mois
      au cours duquel intervient la naissance ou, dans les situations visées à l’article L. 262-9 du présent code,
      jusqu’au dernier jour du mois civil au cours duquel l’enfant atteint l’âge de trois mois ;
    3 De la majoration pour âge des allocations familiales mentionnée à l’article L. 521-3 du code de la
      sécurité sociale ainsi que de l’allocation forfaitaire instituée par le second alinéa de l’article L. 521-1 du même
      code ;
    4 De l’allocation de rentrée scolaire mentionnée à l’article L. 543-1 du code de la sécurité sociale ;
    5 Du complément de libre choix du mode de garde mentionné aux articles L. 531-5 à L. 531-9 du code de
      la sécurité sociale ;16 avril 2009 JOURNAL OFFICIEL DE LA RÉPUBLIQUE
      FRANÇAISE Texte 3 sur 110.
    6 De l’allocation d’éducation de l’enfant handicapé et de ses compléments mentionnés à l’article L. 541-1
      du code de la sécurité sociale, de la majoration spécifique pour personne isolée mentionnée à l’article L. 541-4
      du même code ainsi que de la prestation de compensation du handicap lorsqu’elle est perçue en application de
      l’article 94 de la loi no 2007-1786 du 19 décembre 2007 de financement de la sécurité sociale pour 2008 ;
    7 De l’allocation journalière de présence parentale mentionnée à l’article L. 544-1 du code de la sécurité sociale ;
    8 Des primes de déménagement prévues par les articles L. 542-8 du code de la sécurité sociale et L. 351-5
      du code de la construction et de l’habitation ;
    9 De la prestation de compensation mentionnée à l’article L. 245-1 ou de l’allocation compensatrice
      prévue au chapitre V du titre IV du livre II du code de l’action sociale et des familles dans sa rédaction antérieure
      à la loi no 2005-102 du 11 février 2005 pour l’égalité des droits et des chances, la participation et la
      citoyenneté des personnes handicapées, lorsque l’une ou l’autre sert à rémunérer un tiers ne faisant pas partie
      du foyer du bénéficiaire du revenu de solidarité active ;
    10 Des prestations en nature dues au titre des assurances maladie, maternité, accidents du travail et
       maladies professionnelles ou au titre de l’aide médicale de l’Etat ;
    11 De l’allocation de remplacement pour maternité prévue par les articles L. 613-19-1 et L. 722-8-1 du
       code de la sécurité sociale et L. 732-10 du code rural ;
    12 De l’indemnité en capital attribuée à la victime d’un accident du travail prévue à l’article L. 434-1 du
       code de la sécurité sociale ;
    13 De la prime de rééducation et du prêt d’honneur mentionnés à l’article R. 432-10 du code de la sécurité
       sociale ;
    14 Des aides et secours financiers dont le montant ou la périodicité n’ont pas de caractère régulier ainsi
       que des aides et secours affectés à des dépenses concourant à l’insertion du bénéficiaire et de sa famille,
       notamment dans les domaines du logement, des transports, de l’éducation et de la formation ;
    15 De la prime de retour à l’emploi et de l’aide personnalisée de retour à l’emploi mentionnées
       respectivement aux articles L. 5133-1 et L. 5133-8 du code du travail ainsi que de l’allocation mentionnée à
       l’article L. 5131-6 du même code ;
    16 Des bourses d’études ainsi que de l’allocation pour la diversité dans la fonction publique ;
    17 Des frais funéraires mentionnés à l’article L. 435-1 du code de la sécurité sociale ;
    18 Du capital décès servi par un régime de sécurité sociale ;
    19 De l’allocation du fonds de solidarité en faveur des anciens combattants d’Afrique du Nord prévue à
       l’article 125 de la loi no 91-1322 de finances pour 1992 ;
    20 De l’aide spécifique en faveur des conjoints survivants de nationalité française des membres des
       formations supplétives et assimilés, mentionnée aux premier et troisième alinéas de l’article 10 de la loi
       no 94-488 du 11 juin 1994 relative aux rapatriés, anciens membres des formations supplétives et assimilés ou
       victimes de la captivité en Algérie ;
    21 De l’allocation de reconnaissance instituée par l’article 47 de la loi no 99-1173 de finances rectificative pour 1999 ;
    22 Des mesures de réparation mentionnées à l’article 2 du décret no 2000-657 du 13 juillet 2000 instituant
       une mesure de réparation pour les orphelins dont les parents ont été victimes de persécutions antisémites ;
    23 Des mesures de réparation mentionnées à l’article 2 du décret no 2004-751 du 27 juillet 2004 instituant
       une aide financière en reconnaissance des souffrances endurées par les orphelins dont les parents ont été
       victimes d’actes de barbarie durant la Deuxième Guerre mondiale
    """
    br_rmi_i = self.split_by_roles(br_rmi_i_holder, roles = [CHEF, PART])
    br_rmi_ms = self.split_by_roles(br_rmi_ms_holder, roles = [CHEF, PART])
    br_rmi_pf = self.split_by_roles(br_rmi_pf_holder, roles = [CHEF, PART])
    br_rmi = (br_rmi_i[CHEF] + br_rmi_pf[CHEF] + br_rmi_ms[CHEF] +
              br_rmi_i[PART] + br_rmi_pf[PART] + br_rmi_ms[PART])
    return br_rmi


def _rmi_nbp(self, age_holder, smic55_holder, nb_par , P = law.minim.rmi):
    '''
    Nombre de personne à charge au sens du Rmi ou du Rsa
    'fam'
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

    # TODO: file a issue to check if D_enfch in rsa should be removed
    return nb_par + nb_enf(age, smic55, 0, P.age_pac - 1)  # TODO: check limite d'âge in legislation


def _forf_log(rmi_nbp, P = law.minim):
    '''
    Forfait logement intervenant dans le calcul du Rmi ou du Rsa
    'fam'
    '''
    # calcul du forfait logement annuel si le ménage touche des allocations logements
    # mais également pour les propriétaires en tant qu'avantage en nature et les hébergés également
    # donc on le donne à tout le monde

    # loca = (3 <= so)&(5 >= so)
    FL = P.rmi.forfait_logement
    tx_fl = ((rmi_nbp == 1) * FL.taux1 +
             (rmi_nbp == 2) * FL.taux2 +
             (rmi_nbp >= 3) * FL.taux3)
    return 12 * (tx_fl * P.rmi.rmi)


def _rsa_socle(self, age_holder, nb_par, rmi_nbp, P = law.minim):
    '''
    Rsa socle / Rmi
    'fam'

    RSA socle TODO: mécanisme similaire à l'API: Pour les personnes ayant la charge
    d’au moins un enfant né ou à naître et se retrouvant en situation d’isolement,
    le montant forfaitaire est majoré pendant 12 mois, continus ou non, dans la
    limite de 18 mois à compter de la date du fait générateur de l’isolement. Le
    cas échéant, la durée de majoration est prolongée jusqu’à ce que le plus jeune
    enfant atteigne trois ans.
    '''
    age = self.split_by_roles(age_holder, roles = [CHEF, PART])

    eligib = (age[CHEF] >= 25) | (age[PART] >= 25)
    tx_rmi = (1 + (rmi_nbp >= 2) * P.rmi.txp2
                 + (rmi_nbp >= 3) * P.rmi.txp3
                 + (rmi_nbp >= 4) * ((nb_par == 1) * P.rmi.txps + (nb_par != 1) * P.rmi.txp3)
                 + max_(rmi_nbp - 4, 0) * P.rmi.txps)
    return 12 * P.rmi.rmi * tx_rmi * eligib


def _rmi(rsa_socle, forf_log, br_rmi):
    '''
    Cacule le montant du RMI/ Revenu de solidarité active - socle
    'fam'
    '''
    rmi = max_(0, rsa_socle - forf_log - br_rmi)
    return rmi


def _rsa(self, rsa_socle, ra_rsa_holder, forf_log, br_rmi, P = law.minim.rmi):
    '''
    Cacule le montant du RSA
    'fam'
    '''
    ra_rsa = self.split_by_roles(ra_rsa_holder, roles = [CHEF, PART])
    RSA = max_(0, rsa_socle + P.pente * (ra_rsa[CHEF] + ra_rsa[PART]) - forf_log - br_rmi)
    rsa = RSA * (RSA >= 12 * P.rsa_nv)
    return rsa


def _majo_rsa(self, rsa_socle, agem_holder, age_holder, smic55_holder, isol, forf_log, br_rmi, af_majo, rsa,
        fam = law.fam, rmi = law.minim.rmi):
    '''
    Cacule le montant du RSA majoré pour parent isolé
    'fam'
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    agem = self.split_by_roles(agem_holder, roles = ENFS)
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

    rsa_socle = rmi.rmi

#    Majoration du RSA socle, mécanisme similaire à l'API: Pour les personnes ayant la charge
#    d’au moins un enfant né ou à naître et se retrouvant en situation d’isolement,
#    le montant forfaitaire est majoré pendant 12 mois, continus ou non, dans la
#    limite de 18 mois à compter de la date du fait générateur de l’isolement. Le
#    cas échéant, la durée de majoration est prolongée jusqu’à ce que le plus jeune
#    enfant atteigne trois ans.

#    Majoration pour isolement
#    Si vous êtes parent isolé, c’est-à-dire célibataire, divorcé(e), séparé(e) ou veuf(ve) avec des enfants à charge ou enceinte, le montant forfaitaire garanti est majoré.
#    Ce montant forfaitaire majoré est accordé à partir du mois au cours duquel survient l'un des événements suivants :
#    - déclaration de grossesse,
#    - naissance d'un enfant,
#    - prise en charge d'un enfant,
#    - séparation, veuvage,
#    - dépôt de la demande si l’événement est antérieur.
#
#    Le montant forfaitaire majoré peut être accordé pendant 12 mois, continus ou discontinus, au cours d’une période de 18 mois suivant l’événement.
#    Si votre plus jeune enfant à charge a moins de 3 ans, le montant forfaitaire majoré vous est accordé jusqu'à ses 3 ans.

    benjamin = age_en_mois_benjamin(agem)
    enceinte = (benjamin < 0) * (benjamin > -6)
    # TODO: quel mois mettre ?
    # TODO: pas complètement exact
    # L'allocataire perçoit la majoration :
    # jusqu'à ce que le plus jeune enfant ait 3 ans,
    # ou pendant 12 mois consécutifs si les enfants sont âgés de plus de 3 ans
    #    et s'il a présenté sa demande dans les 6 mois à partir du moment où il
    #    assure seul la charge de l'enfant.
    # TODO: API courte gens pour les gens qui ont divorcés dans l'année
    # Le droit à l'allocation est réétudié tous les 3 mois.
    # # Calcul de l'année et mois de naissance du benjamin

    condition = (floor(benjamin / 12) <= rmi.majo_rsa.age - 1)
    eligib = isol * ((enceinte != 0) | (nb_enf(age, smic55, 0, rmi.majo_rsa.age - 1) > 0)) * condition;

    # moins de 20 ans avant inclusion dans rsa
    # moins de 25 ans après inclusion dans rsa
    majo1 = eligib * rsa_socle * (rmi.majo_rsa.pac0
        + rmi.majo_rsa.pac_enf_sup * nb_enf(age, smic55, fam.af.age1, rmi.majo_rsa.age_pac - 1))
    rsa = (rmi.majo_rsa.age_pac >= 25)  # dummy passage au rsa majoré
    br_api = br_rmi + af_majo * not_(rsa)
    # On pourrait mensualiser RMI, BRrmi et forfait logement
    majo_rsa = max_(0, majo1 - forf_log / 12 - br_api / 12 - rsa / 12)
    # L'API est exonérée de CRDS
    return 12 * majo_rsa  # annualisé
    # TODO API: temps partiel qui modifie la base ressource
    # Cumul
    # Cumul avec un revenu
    # Si l'allocataire reprend une activité ou suit une formation professionnelle rémunérée, les revenus sont cumulables intégralement au cours des 3 premiers mois de reprise d'activité.
    # Du 4e au 12e mois qui suit, le montant de l'allocation varie en fonction de la durée de l'activité ou de la formation.
    # Durée d'activité de 78 heures ou plus par mois ou activité non salariée
    # Lorsque la durée d'activité est de 78 heures minimum par mois, le montant de l'API perçu par l'allocataire est diminué de la totalité du salaire. Tous les revenus d'activité sont pris en compte pour le calcul de l'API, sauf si l'allocataire perçoit des revenus issus d'un contrat insertion-revenu minimum d'activité (CIRMA) ou d'un contrat d'avenir (CAV).
    # L'allocataire peut bénéficier, sous certaines conditions :
    # • de la prime de retour à l'emploi si son activité est d'une durée d'au moins 4 mois consécutifs, sauf s'il effectue un stage de formation professionnelle,
    # • de la prime forfaitaire pendant 9 mois, sauf s'il exerce une activité salariée dans le cadre d'un CIRMA ou d'un CAV.
    # Durée d'activité de moins de 78 heures par mois
    # Lorsque la durée d'activité est inférieure à 78 heures par mois, le montant de l'API perçu par l'allocataire est diminué de la moitié du salaire.
    # Si l'allocataire exerce une activité dans le cadre d'un CIRMA ou d'un CAV, ses revenus d'activité ne sont pas pris en compte pour le calcul de son API.


def _psa(self, api, rsa, activite_holder, af_nbenf, al, P = law.minim.rmi):
    '''
    Prime de solidarité active (exceptionnelle, 200€ versés une fois en avril 2009)

    Versement en avril 2009 d’une prime de solidarité active (Psa) aux familles modestes qui ont bénéficié en janvier,
    février ou mars 2009 du Rmi, de l’Api (du Rsa expérimental, du Cav ou du Rma pour les ex-bénéficiaires du Rmi ou de l’Api),
    de la prime forfaitaire mensuelle au titre du Rmi ou de l’Api
    ou enfin d’une aide au logement (à condition d’exercer une activité professionnelle et d’être âgé de plus de 25 ans
    ou d’avoir au moins un enfant à charge).
    La Psa, prime exceptionnelle, s’élève à 200 euros par foyer bénéficiaire.
    '''
    activite = self.split_by_roles(activite_holder, roles = [CHEF, PART])

    dummy_api = api > 0
    dummy_rmi = rsa > 0
    dummy_al = and_(al > 0, or_(af_nbenf > 0, or_(activite[CHEF] == 0, activite[PART] == 0)))

    condition = (dummy_api + dummy_rmi + dummy_al > 0)
    psa = condition * P.psa

    return psa


def _rsa_act(rsa, rmi):
    '''
    Calcule le montant du RSA activité
    Note: le partage en moitié est un point de législation, pas un choix arbitraire
    '''
    res = max_(rsa - rmi, 0)
    return res


def _rsa_act_i(self, rsa_act_holder, concub_holder, maries_holder, quifam, idfam):
    '''
    Calcule le montant du RSA activité.

    Note: le partage en moitié est un point de législation, pas un choix arbitraire.
    '''
    concub = self.cast_from_entity_to_roles(concub_holder)
    maries = self.cast_from_entity_to_roles(maries_holder)
    rsa_act = self.cast_from_entity_to_roles(rsa_act_holder)

    conj = or_(concub, maries)
    rsa_act_i = 0 * quifam
    chef_filter = quifam == 0
    rsa_act_i[chef_filter] = rsa_act[chef_filter] / (1 + conj[chef_filter])
    partenaire_filter = quifam == 1
    rsa_act_i[partenaire_filter] = rsa_act[partenaire_filter] * conj[partenaire_filter] / 2
    return rsa_act_i


def _crds_mini(rsa_act, P = law.fam.af.crds):
    """
    CRDS sur les minima sociaux
    """
    return -P * rsa_act


def _api(self, agem_holder, age_holder, smic55_holder, isol, forf_log, br_rmi, af_majo, rsa, af = law.fam.af,
        api = law.minim.api):
    """
    Allocation de parent isolé
    """
    age = self.split_by_roles(age_holder, roles = ENFS)
    agem = self.split_by_roles(agem_holder, roles = ENFS)
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

    # TODO:
    #    Majoration pour isolement
    #    Si vous êtes parent isolé, c’est-à-dire célibataire, divorcé(e), séparé(e) ou veuf(ve) avec des enfants à charge ou enceinte, le montant forfaitaire garanti est majoré.
    #    Ce montant forfaitaire majoré est accordé à partir du mois au cours duquel survient l'un des événements suivants :
    #    - déclaration de grossesse,
    #    - naissance d'un enfant,
    #    - prise en charge d'un enfant,
    #    - séparation, veuvage,
    #    - dépôt de la demande si l’événement est antérieur.
    #
    #    Le montant forfaitaire majoré peut être accordé pendant 12 mois, continus ou discontinus, au cours d’une période de 18 mois suivant l’événement.
    #    Si votre plus jeune enfant à charge a moins de 3 ans, le montant forfaitaire majoré vous est accordé jusqu'à ses 3 ans.
    benjamin = age_en_mois_benjamin(agem)
    enceinte = (benjamin < 0) * (benjamin > -6)
    # TODO: quel mois mettre ?
    # TODO: pas complètement exact
    # L'allocataire perçoit l'API :
    # jusqu'à ce que le plus jeune enfant ait 3 ans,
    # ou pendant 12 mois consécutifs si les enfants sont âgés de plus de 3 ans
    #    et s'il a présenté sa demande dans les 6 mois à partir du moment où il
    #    assure seul la charge de l'enfant.
    # TODO: API courte gens pour les gens qui ont divorcés dans l'année
    # Le droit à l'allocation est réétudié tous les 3 mois.
    # # Calcul de l'année et mois de naissance du benjamin

    condition = (floor(benjamin / 12) <= api.age - 1)
    eligib = isol * ((enceinte != 0) | (nb_enf(age, smic55, 0, api.age - 1) > 0)) * condition;

    # moins de 20 ans avant inclusion dans rsa
    # moins de 25 ans après inclusion dans rsa
    api1 = eligib * af.bmaf * (api.base + api.enf_sup * nb_enf(age, smic55, af.age1, api.age_pac - 1))
    rsa = (api.age_pac >= 25)  # dummy passage au rsa majoré
    br_api = br_rmi + af_majo * not_(rsa)
    # On pourrait mensualiser RMI, BRrmi et forfait logement
    api = max_(0, api1 - forf_log / 12 - br_api / 12 - rsa / 12)
    # L'API est exonérée de CRDS
    return 12 * api  # annualisé
    # TODO API: temps partiel qui modifie la base ressource
    # Cumul
    # Cumul avec un revenu
    # Si l'allocataire reprend une activité ou suit une formation professionnelle rémunérée, les revenus sont cumulables intégralement au cours des 3 premiers mois de reprise d'activité.
    # Du 4e au 12e mois qui suit, le montant de l'allocation varie en fonction de la durée de l'activité ou de la formation.
    # Durée d'activité de 78 heures ou plus par mois ou activité non salariée
    # Lorsque la durée d'activité est de 78 heures minimum par mois, le montant de l'API perçu par l'allocataire est diminué de la totalité du salaire. Tous les revenus d'activité sont pris en compte pour le calcul de l'API, sauf si l'allocataire perçoit des revenus issus d'un contrat insertion-revenu minimum d'activité (CIRMA) ou d'un contrat d'avenir (CAV).
    # L'allocataire peut bénéficier, sous certaines conditions :
    # • de la prime de retour à l'emploi si son activité est d'une durée d'au moins 4 mois consécutifs, sauf s'il effectue un stage de formation professionnelle,
    # • de la prime forfaitaire pendant 9 mois, sauf s'il exerce une activité salariée dans le cadre d'un CIRMA ou d'un CAV.
    # Durée d'activité de moins de 78 heures par mois
    # Lorsque la durée d'activité est inférieure à 78 heures par mois, le montant de l'API perçu par l'allocataire est diminué de la moitié du salaire.
    # Si l'allocataire exerce une activité dans le cadre d'un CIRMA ou d'un CAV, ses revenus d'activité ne sont pas pris en compte pour le calcul de son API.


def _aefa__2008_(self, age_holder, smic55_holder, af_nbenf, nb_par, ass_holder, aer_holder, api, rsa, _P, af = law.fam.af,
        P = law.minim.aefa):
    '''
    Aide exceptionelle de fin d'année (prime de Noël)

    Insituée en 1998
    Apparaît sous le nom de complément de rmi dans les ERF

    Le montant de l’aide mentionnée à l’article 1er versée aux bénéficiaires de l’allocation de solidarité
    spécifique à taux majoré servie aux allocataires âgés de cinquante-cinq ans ou plus justifiant de vingt années
    d’activité salariée, aux allocataires âgés de cinquante-sept ans et demi ou plus justifiant de dix années d’activité
    salariée ainsi qu’aux allocataires justifiant d’au moins 160 trimestres validés dans les régimes d’assurance
    vieillesse ou de périodes reconnues équivalentes est égal à


    Pour bénéficier de la Prime de Noël 2011, vous devez être éligible pour le compte du mois de novembre 2011 ou au plus de décembre 2011, soit d’une allocation de solidarité spécifique (ASS), de la prime forfaitaire mensuelle de reprise d'activité, de l'allocation équivalent retraite (allocataire AER), du revenu de solidarité active (Bénéficiaires RSA), de l'allocation de parent isolé (API), du revenu minimum d'insertion (RMI), de l’Allocation pour la Création ou la Reprise d'Entreprise (ACCRE-ASS) ou encore allocation chômage.
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    aer = self.sum_by_entity(aer_holder)
    ass = self.sum_by_entity(ass_holder)
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

    dummy_ass = ass > 0
    dummy_aer = aer > 0
    dummy_api = api > 0
    dummy_rmi = rsa > 0

    maj = 0  # TODO

    condition = (dummy_ass + dummy_aer + dummy_api + dummy_rmi > 0)

    if hasattr(af, "age3"): nbPAC = nb_enf(age, smic55, af.age1, af.age3)
    else: nbPAC = af_nbenf
    # TODO check nombre de PAC pour une famille
    aefa = condition * P.mon_seul * (1 + (nb_par == 2) * P.tx_2p
              + nbPAC * P.tx_supp * (nb_par <= 2)
              + nbPAC * P.tx_3pac * max_(nbPAC - 2, 0))

    aefa_maj = P.mon_seul * maj
    aefa = max_(aefa_maj, aefa)
    return aefa

def _aefa_2008(self, age_holder, smic55_holder, af_nbenf, nb_par, ass_holder, aer_holder, api, rsa, _P, af = law.fam.af,
        P = law.minim.aefa):
    '''
    Aide exceptionelle de fin d'année (prime de Noël)

    Insituée en 1998
    Apparaît sous le nom de complément de rmi dans les ERF

    Le montant de l’aide mentionnée à l’article 1er versée aux bénéficiaires de l’allocation de solidarité
    spécifique à taux majoré servie aux allocataires âgés de cinquante-cinq ans ou plus justifiant de vingt années
    d’activité salariée, aux allocataires âgés de cinquante-sept ans et demi ou plus justifiant de dix années d’activité
    salariée ainsi qu’aux allocataires justifiant d’au moins 160 trimestres validés dans les régimes d’assurance
    vieillesse ou de périodes reconnues équivalentes est égal à


    Pour bénéficier de la Prime de Noël 2011, vous devez être éligible pour le compte du mois de novembre 2011 ou au plus de décembre 2011, soit d’une allocation de solidarité spécifique (ASS), de la prime forfaitaire mensuelle de reprise d'activité, de l'allocation équivalent retraite (allocataire AER), du revenu de solidarité active (Bénéficiaires RSA), de l'allocation de parent isolé (API), du revenu minimum d'insertion (RMI), de l’Allocation pour la Création ou la Reprise d'Entreprise (ACCRE-ASS) ou encore allocation chômage.
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    aer = self.sum_by_entity(aer_holder)
    ass = self.sum_by_entity(ass_holder)
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

    dummy_ass = ass > 0
    dummy_aer = aer > 0
    dummy_api = api > 0
    dummy_rmi = rsa > 0

    maj = 0  # TODO

    condition = (dummy_ass + dummy_aer + dummy_api + dummy_rmi > 0)

    if hasattr(af, "age3"): nbPAC = nb_enf(age, smic55, af.age1, af.age3)
    else: nbPAC = af_nbenf
    # TODO check nombre de PAC pour une famille
    aefa = condition * P.mon_seul * (1 + (nb_par == 2) * P.tx_2p
              + nbPAC * P.tx_supp * (nb_par <= 2)
              + nbPAC * P.tx_3pac * max_(nbPAC - 2, 0))

    aefa += condition * P.forf2008

    aefa_maj = P.mon_seul * maj
    aefa = max_(aefa_maj, aefa)
    return aefa


def _br_aah(br_pf, asi, aspa):
    '''
    Base ressources de l'allocation adulte handicapé
    'fam'
    '''
    br_aah = br_pf + asi + aspa
    return br_aah


def _aah(self, br_pf_i_holder, br_aah, inv_holder, age_holder, smic55_holder, concub, af_nbenf, aah = law.minim.aah,
        aeeh = law.fam.aeeh):
    '''
    Allocation adulte handicapé

    Conditions liées au handicap
    La personne doit être atteinte d’un taux d’incapacité permanente :
    - d’au moins 80 %,
    - ou compris entre 50 et 79 %. Dans ce cas, elle doit remplir deux conditions
    supplémentaires : être dans l’impossibilité de se procurer un emploi compte
    tenu de son handicap et ne pas avoir travaillé depuis au moins 1 an
    Condition de résidence
    L'AAH peut être versée aux personnes résidant en France métropolitaine ou
     dans les départements d'outre-mer ou à Saint-Pierre et Miquelon de façon permanente.
     Les personnes de nationalité étrangère doivent être en possession d'un titre de séjour
     régulier ou être titulaire d'un récépissé de renouvellement de titre de séjour.
    Condition d'âge
    Age minimum : Le demandeur ne doit plus avoir l'âge de bénéficier de l'allocation d'éducation de l'enfant handicapé, c'est-à-dire qu'il doit être âgé :
    - de plus de vingt ans,
    - ou de plus de seize ans, s'il ne remplit plus les conditions pour ouvrir droit aux allocations familiales.
    Pour les montants http://www.handipole.org/spip.php?article666

    Âge max_
    Le versement de l'AAH prend fin à partir de l'âge minimum légal de départ à la retraite en cas d'incapacité
    de 50 % à 79 %. À cet âge, le bénéficiaire bascule dans le régime de retraite pour inaptitude.
    En cas d'incapacité d'au moins 80 %, une AAH différentielle (c'est-à-dire une allocation mensuelle réduite)
    peut être versée au-delà de l'âge minimum légal de départ à la retraite en complément d'une retraite inférieure au minimum vieillesse.

    N'entrent pas en compte dans les ressources :
    L'allocation compensatrice tierce personne, les allocations familiales,
    l'allocation de logement, la retraite du combattant, les rentes viagères
    constituées en faveur d'une personne handicapée ou dans la limite d'un
    montant fixé à l'article D.821-6 du code de la sécurité sociale (1 830 €/an),
    lorsqu'elles ont été constituées par une personne handicapée pour elle-même.
    Le RMI (article R 531-10 du code de la sécurité sociale).
    A partir du 1er juillet 2007, votre Caf, pour le calcul de votre Aah,
    continue à prendre en compte les ressources de votre foyer diminuées de 20%.
    Notez, dans certaines situations, la Caf évalue forfaitairement vos
    ressources à partir de votre revenu mensuel.
    '''
    age = self.split_by_roles(age_holder, roles = [CHEF, PART])
    br_pf_i = self.split_by_roles(br_pf_i_holder, roles = [CHEF, PART])
    inv = self.split_by_roles(inv_holder, roles = [CHEF, PART])
    smic55 = self.split_by_roles(smic55_holder, roles = [CHEF, PART])

#    TODO éligibilité AAH, notamment avoir le % d'incapacité ?

    eligC = (((inv[CHEF]) & (age[CHEF] <= aah.age_legal_retraite)) &
              ((age[CHEF] >= aeeh.age) | ((age[CHEF] >= 16) & (smic55[CHEF]))))

    eligP = (((inv[PART]) & (age[PART] <= aah.age_legal_retraite)) &
              ((age[PART] >= aeeh.age) | ((age[PART] >= 16) & (smic55[PART]))))

    plaf_aah = 12 * aah.montant * (1 + concub + aah.tx_plaf_supp * af_nbenf)
    eligib = (eligC | eligP)
    # l'aah est exonérée de crds

#        Cumul d'allocation
# L'AAH peut être cumulée :
#
# - avec le complément d'AAH (à titre transitoire pour les derniers bénéficiaires,
#  ce complément étant remplacé par la majoration pour la vie autonome depuis
#  le 1er juillet 2005) ;
# - avec la majoration pour la vie autonome ;
# - avec le complément de ressources (dans le cadre de la garantie de ressources).
#
# L'AAH n'est pas cumulable avec la perception d'un avantage de vieillesse,
# d'invalidité, ou d'accident du travail si cet avantage est d'un montant au
# moins égal à ladite allocation.
    return eligib * max_(plaf_aah - br_aah, 0)  # annualisé


def _caah__2005(aah, asi, _P, P = law.minim):
    '''
    Complément d'allocation adulte handicapé
    '''
# Pour bénéficier du complément de ressources, l’intéressé doit remplir les conditions
# suivantes :
# - percevoir l’allocation aux adultes handicapés à taux normal ou en
#    complément d’une pension d’invalidité, d’une pension de vieillesse ou
#    d’une rente accident du travail ;
# - avoir un taux d’incapacité égal ou supérieur à 80 % ;
# - avoir une capacité de travail, appréciée par la commission des droits et
#    de l’autonomie (CDAPH) inférieure à 5 % du fait du handicap ;
# - ne pas avoir perçu de revenu à caractère professionnel depuis un an à la date
#    du dépôt de la demande de complément ;
# - disposer d’un logement indépendant.
# A noter : une personne hébergée par un particulier à son domicile n’est pas
# considérée disposer d’un logement indépendant, sauf s’il s’agit de son conjoint,
# de son concubin ou de la personne avec laquelle elle est liée par un pacte civil
# de solidarité.

#       Complément de ressources Le complément de ressources est
#       destiné aux personnes handicapées dans l’incapacité de
#       travailler Il est égal à la différence entre la garantie de
#       ressources pour les personnes handicapées (GRPH) et l’AAH

    elig_cpl = ((aah > 0) | (asi > 0))  # TODO: éligibilité logement indépendant
    compl = P.caah.cpltx * P.aah.montant * elig_cpl
        # En fait perdure jusqu'en 2008


    # Majoration pour la vie autonome
    # La majoration pour la vie autonome est destinée à permettre aux personnes, en capacité de travailler et au chômage
    # en raison de leur handicap, de pourvoir faire face à leur dépense de logement.

#        Conditions d'attribution
# La majoration pour la vie autonome est versée automatiquement aux personnes qui remplissent les conditions suivantes :
# - percevoir l'AAH à taux normal ou en complément d'un avantage vieillesse ou d'invalidité ou d'une rente accident du travail,
# - avoir un taux d'incapacité au moins égal à 80 %,
# - disposer d'un logement indépendant,
# - bénéficier d'une aide au logement (aide personnelle au logement, ou allocation de logement sociale ou familiale), comme titulaire du droit, ou comme conjoint, concubin ou partenaire lié par un Pacs au titulaire du droit,
# - ne pas percevoir de revenu d'activité à caractère professionnel propre.
# Choix entre la majoration ou la garantie de ressources
# La majoration pour la vie autonome n'est pas cumulable avec la garantie de ressources pour les personnes handicapées.
# La personne qui remplit les conditions d'octroi de ces deux avantages doit choisir de bénéficier de l'un ou de l'autre.
    mva = 0
    caah = max_(compl, mva)
    return 12 * caah  # annualisé

def _caah_2006_(aah, asi, br_aah, al, _P, P = law.minim):
    '''
    Complément d'allocation adulte handicapé
    '''
# Pour bénéficier du complément de ressources, l’intéressé doit remplir les conditions
# suivantes :
# - percevoir l’allocation aux adultes handicapés à taux normal ou en
#    complément d’une pension d’invalidité, d’une pension de vieillesse ou
#    d’une rente accident du travail ;
# - avoir un taux d’incapacité égal ou supérieur à 80 % ;
# - avoir une capacité de travail, appréciée par la commission des droits et
#    de l’autonomie (CDAPH) inférieure à 5 % du fait du handicap ;
# - ne pas avoir perçu de revenu à caractère professionnel depuis un an à la date
#    du dépôt de la demande de complément ;
# - disposer d’un logement indépendant.
# A noter : une personne hébergée par un particulier à son domicile n’est pas
# considérée disposer d’un logement indépendant, sauf s’il s’agit de son conjoint,
# de son concubin ou de la personne avec laquelle elle est liée par un pacte civil
# de solidarité.

#       Complément de ressources Le complément de ressources est
#       destiné aux personnes handicapées dans l’incapacité de
#       travailler Il est égal à la différence entre la garantie de
#       ressources pour les personnes handicapées (GRPH) et l’AAH

    elig_cpl = ((aah > 0) | (asi > 0))  # TODO: éligibilité logement indépendant
    compl = elig_cpl * max_(P.caah.grph - (aah + br_aah) / 12, 0)

        # En fait perdure jusqu'en 2008


    # Majoration pour la vie autonome
    # La majoration pour la vie autonome est destinée à permettre aux personnes, en capacité de travailler et au chômage
    # en raison de leur handicap, de pourvoir faire face à leur dépense de logement.

#        Conditions d'attribution
# La majoration pour la vie autonome est versée automatiquement aux personnes qui remplissent les conditions suivantes :
# - percevoir l'AAH à taux normal ou en complément d'un avantage vieillesse ou d'invalidité ou d'une rente accident du travail,
# - avoir un taux d'incapacité au moins égal à 80 %,
# - disposer d'un logement indépendant,
# - bénéficier d'une aide au logement (aide personnelle au logement, ou allocation de logement sociale ou familiale), comme titulaire du droit, ou comme conjoint, concubin ou partenaire lié par un Pacs au titulaire du droit,
# - ne pas percevoir de revenu d'activité à caractère professionnel propre.
# Choix entre la majoration ou la garantie de ressources
# La majoration pour la vie autonome n'est pas cumulable avec la garantie de ressources pour les personnes handicapées.
# La personne qui remplit les conditions d'octroi de ces deux avantages doit choisir de bénéficier de l'un ou de l'autre.
    elig_mva = (al > 0) * ((aah > 0) | (asi > 0))  # TODO: complêter éligibilité
    mva = P.caah.mva * elig_mva * 0
    caah = max_(compl, mva)
    return 12 * caah  # annualisé

def _ass(self, br_pf, cho_holder, concub, ass = law.chomage.ass):
    '''
    Allocation de solidarité spécifique

    L’Allocation de Solidarité Spécifique (ASS) est une allocation versée aux
    personnes ayant épuisé leurs droits à bénéficier de l'assurance chômage.

    Le prétendant doit avoir épuisé ses droits à l’assurance chômage.
    Il doit être inscrit comme demandeur d’emploi et justifier de recherches actives.
    Il doit être apte à travailler.
    Il doit justifier de 5 ans d’activité salariée au cours des 10 ans précédant le chômage.
    À partir de 60 ans, il doit répondre à des conditions particulières.
     TODO majo ass et base ressource

    Les ressources prises en compte pour apprécier ces plafonds, comprennent l'allocation de solidarité elle-même ainsi que les autres ressources de l'intéressé, et de son conjoint, partenaire pacsé ou concubin, soumises à impôt sur le revenu.
    Ne sont pas prises en compte, pour déterminer le droit à ASS :
      l'allocation d'assurance chômage précédemment perçue,
      les prestations familiales,
      l'allocation de logement,
      la majoration de l'ASS,
      la prime forfaitaire mensuelle de retour à l'emploi,
      la pension alimentaire ou la prestation compensatoire due par l'intéressé.


    Conditions de versement de l'ASS majorée
        Pour les allocataires admis au bénéfice de l'ASS majorée ( avant le 1er janvier 2004) , le montant de l'ASS majorée est fixé à 22,07 € par jour.
        Pour mémoire, jusqu'au 31 décembre 2003, pouvaient bénéficier de l'ASS majorée, les allocataires :
        âgés de 55 ans ou plus et justifiant d'au moins 20 ans d'activité salariée,
        ou âgés de 57 ans et demi ou plus et justifiant de 10 ans d'activité salariée,
        ou justifiant d'au moins 160 trimestres de cotisation retraite.
    '''
    cho = self.split_by_roles(cho_holder, roles = [CHEF, PART])

    P = _P
    majo = 0
    cond_act_prec_suff = False
    elig_ass = (cho[CHEF] | cho[PART]) & cond_act_prec_suff
    plaf = ass.plaf_seul * not_(concub) + ass.plaf_coup * concub
    montant_mensuel = 30 * (ass.montant_plein * not_(majo) + majo * ass.montant_maj)
    revenus = br_pf + 12 * montant_mensuel  # TODO check base ressources
    ass = elig_ass * (montant_mensuel * (revenus <= plaf)
              + (revenus > plaf) * max_(plaf + montant_mensuel - revenus, 0))

    return 12 * ass  # annualisé


# TODO surle rsa hors rmi et api ?    def crds_mini():

