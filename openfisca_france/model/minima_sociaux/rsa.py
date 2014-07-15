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

from numpy import (floor, maximum as max_, logical_not as not_, logical_and as and_, logical_or as or_)
from openfisca_core.accessors import law

from ..input_variables.base import QUIFAM, QUIFOY
from ..pfam import nb_enf, age_en_mois_benjamin

CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
VOUS = QUIFOY['vous']
CONJ = QUIFOY['conj']


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


def _br_rmi_pf__2003(self, af_base, cf, asf, apje, ape, P = law.minim):
    """
    Prestations familiales inclues dans la base ressource RSA/RMI
    TO DO: Add mva (majoration vie autonome),
    """
    out = P.rmi.pfInBRrmi * (af_base + cf + asf + apje + ape)
    return self.cast_from_entity_to_role(out, entity = 'famille', role = CHEF)


def _br_rmi_pf_2004_(self, af_base, cf, asf, paje_base, paje_clca, paje_colca, P = law.minim):
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


def _rsa_socle(self, age_holder, activite_holder, nb_par, rmi_nbp, P = law.minim):
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
    activite = self.split_by_roles(activite_holder, roles = [CHEF, PART])

    eligib = ((age[CHEF] >= 25) * not_(activite[CHEF] == 2)) | ((age[PART] >= 25) * not_(activite[PART] == 2))
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


def _aefa__2008_(self, age_holder, smic55_holder, af_nbenf, nb_par, ass_holder, aer_holder, api, rsa, af = law.fam.af,
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

def _aefa_2008(self, age_holder, smic55_holder, af_nbenf, nb_par, ass_holder, aer_holder, api, rsa, af = law.fam.af,
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