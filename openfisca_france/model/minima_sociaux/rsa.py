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

from ..base import QUIFAM, QUIFOY
from ..pfam import nb_enf, age_en_mois_benjamin

CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
VOUS = QUIFOY['vous']
CONJ = QUIFOY['conj']


def _enceinte_fam(self, agem_holder, enceinte_holder):
    agem_enf = self.split_by_roles(agem_holder, roles = ENFS)
    enceinte = self.split_by_roles(enceinte_holder, roles = [CHEF, PART])

    benjamin = age_en_mois_benjamin(agem_enf)
    enceinte_compat = and_(benjamin < 0, benjamin > -6)
    return or_(or_(enceinte_compat, enceinte[CHEF]), enceinte[PART])


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


def _rsa_forfait_asf(asf_elig, asf_nbenf, bmaf = law.fam.af.bmaf, forfait_asf = law.minim.rmi.forfait_asf):
    '''
    Allocation de soutien familial forfaitisée pour le RSA
    '''

    # TODO: la valeur est annualisé mais l'ASF peut ne pas être versée toute l'année
    return asf_elig * max_(0, asf_nbenf * 12 * bmaf * forfait_asf.taux1)


def _br_rmi_pf__2003(self, af_base, cf, asf, apje, ape, P = law.minim):
    """
    Prestations familiales inclues dans la base ressource RSA/RMI
    TODO: Add mva (majoration vie autonome),
    """
    out = P.rmi.pfInBRrmi * (af_base + cf + asf + apje + ape)
    return self.cast_from_entity_to_role(out, entity = 'famille', role = CHEF)


def _br_rmi_pf_2004_2014(self, af_base, cf, asf, paje_base, paje_clca, paje_colca, P = law.minim):
    """
    Prestations familiales inclues dans la base ressource RSA/RMI
    TODO: Add mva (majoration vie autonome),
    """

    out = P.rmi.pfInBRrmi * (af_base + cf + asf + paje_base + paje_clca + paje_colca)

    return self.cast_from_entity_to_role(out, entity = 'famille', role = CHEF)


def _br_rmi_pf_2014_(self, af_base, cf, rsa_forfait_asf, paje_base, paje_clca, paje_colca, P = law.minim):
    """
    Prestations familiales inclues dans la base ressource RSA/RMI
    TODO: Add mva (majoration vie autonome),
    """

    out = P.rmi.pfInBRrmi * (af_base + cf + rsa_forfait_asf + paje_base + paje_clca + paje_colca)

    return self.cast_from_entity_to_role(out, entity = 'famille', role = CHEF)


def _br_rmi_ms(self, aspa, asi, aah, caah):
    """
    Minima sociaux inclus dans la base ressource RSA/RMI
    'ind'
    """
    return self.cast_from_entity_to_role(
        aspa + asi,
        entity = 'famille',
        role = CHEF,
        ) + aah + caah


def _br_rmi_i(self, ass_holder, ra_rsa, cho, rst, alr, rto, rev_cap_bar_holder, rev_cap_lib_holder, rfon_ms, div_ms):
    '''
    Base ressource individuelle du RSA/RMI
    'ind'
    '''
    rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = VOUS)
    rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = VOUS)
    ass = self.cast_from_entity_to_roles(ass_holder)

    return ass + ra_rsa + cho + rst + alr + rto + rev_cap_bar + rev_cap_lib + rfon_ms + div_ms


def _br_rmi(self, br_rmi_pf_holder, br_rmi_ms_holder, br_rmi_i_holder, rsa_base_ressources_patrimoine_i_holder):
    """
    Base ressources du Rmi ou du Rsa
    """
    br_rmi_i = self.split_by_roles(br_rmi_i_holder, roles = [CHEF, PART])
    br_rmi_ms = self.split_by_roles(br_rmi_ms_holder, roles = [CHEF, PART])
    br_rmi_pf = self.split_by_roles(br_rmi_pf_holder, roles = [CHEF, PART])
    rsa_base_ressources_patrimoine_i = self.split_by_roles(rsa_base_ressources_patrimoine_i_holder, roles = [CHEF, PART])
    br_rmi = (br_rmi_i[CHEF] + br_rmi_pf[CHEF] + br_rmi_ms[CHEF] + rsa_base_ressources_patrimoine_i[CHEF] +
              br_rmi_i[PART] + br_rmi_pf[PART] + br_rmi_ms[PART] + rsa_base_ressources_patrimoine_i[PART])
    return br_rmi


def _rsa_base_ressources_patrimoine_i(interets_epargne_sur_livrets, epargne_non_remuneree, revenus_capital, valeur_locative_immo_non_loue, valeur_locative_terrains_non_loue, revenus_locatifs, rsa = law.minim.rmi):
    '''
    Base de ressources des revenus du patrimoine
    'ind'
    '''

    return (
        interets_epargne_sur_livrets +
        epargne_non_remuneree * rsa.patrimoine.taux_interet_forfaitaire_epargne_non_remunere +
        revenus_capital +
        valeur_locative_immo_non_loue * rsa.patrimoine.abattement_valeur_locative_immo_non_loue +
        valeur_locative_terrains_non_loue * rsa.patrimoine.abattement_valeur_locative_terrains_non_loue +
        revenus_locatifs
        )


def _rmi_nbp(self, age_holder, smic55_holder, nb_par , P = law.minim.rmi):
    '''
    Nombre de personne à charge au sens du Rmi ou du Rsa
    'fam'
    '''
    age = self.split_by_roles(age_holder, roles = ENFS)
    smic55 = self.split_by_roles(smic55_holder, roles = ENFS)

    # TODO: file a issue to check if D_enfch in rsa should be removed
    return nb_par + nb_enf(age, smic55, 0, P.age_pac - 1)  # TODO: check limite d'âge in legislation


def _rsa_forfait_logement(rmi_nbp, P = law.minim):
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


def _crds_mini(rsa_act, P = law.fam.af.crds):
    """
    CRDS sur les minima sociaux
    """
    return -P * rsa_act


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


def _rsa_socle(self, age_holder, smic55_holder, activite_holder, nb_par, rmi = law.minim.rmi):
    '''
    Rsa socle / Rmi
    'fam'
    '''
    age_parents = self.split_by_roles(age_holder, roles = [CHEF, PART])
    activite_parents = self.split_by_roles(activite_holder, roles = [CHEF, PART])
    age_enf = self.split_by_roles(age_holder, roles = ENFS)
    smic55_enf = self.split_by_roles(smic55_holder, roles = ENFS)

    nbp = nb_par + nb_enf(age_enf, smic55_enf, 0, rmi.age_pac)

    eligib = (
        (age_parents[CHEF] >= rmi.age_pac)
        *
        not_(activite_parents[CHEF] == 2)
        ) | (
            (age_parents[PART] >= rmi.age_pac) * not_(activite_parents[PART] == 2)
            )

    taux = (1 + (nbp >= 2) * rmi.txp2
                 + (nbp >= 3) * rmi.txp3
                 + (nbp >= 4) * ((nb_par == 1) * rmi.txps + (nb_par != 1) * rmi.txp3)
                 + max_(nbp - 4, 0) * rmi.txps)

    return eligib * rmi.rmi * taux * 12


def _rsa_socle_majore(self, enceinte_fam, age_holder, smic55_holder, nb_par, isol, rmi = law.minim.rmi):
    '''
    Cacule le montant du RSA majoré pour isolement
    'fam'
    '''
    age_enf = self.split_by_roles(age_holder, roles = ENFS)
    smic55_enf = self.split_by_roles(smic55_holder, roles = ENFS)

    nbenf = nb_enf(age_enf, smic55_enf, 0, rmi.age_pac)

    eligib = isol * (enceinte_fam | (nbenf > 0))

    taux = rmi.majo_rsa.pac0 + rmi.majo_rsa.pac_enf_sup * nbenf

    return eligib * rmi.rmi * taux * 12


def _rmi(rsa_socle, rsa_forfait_logement, br_rmi):
    '''
    Cacule le montant du RMI/ Revenu de solidarité active - socle
    'fam'
    '''
    rmi = max_(0, rsa_socle - rsa_forfait_logement - br_rmi)
    return rmi


def _rsa(self, rsa_socle, rsa_socle_majore, ra_rsa_holder, rsa_forfait_logement, br_rmi, P = law.minim.rmi):
    '''
    Cacule le montant du RSA
    'fam'
    '''
    ra_rsa = self.split_by_roles(ra_rsa_holder, roles = [CHEF, PART])

    # rsa_socle applicable - forfait logement - base ressources + bonification RSA activité
    base = max_(rsa_socle, rsa_socle_majore) - rsa_forfait_logement - br_rmi + P.pente * (ra_rsa[CHEF] + ra_rsa[PART])
    base_normalise = max_(base, 0)

    # Seuil de versement *annualisé*
    return base_normalise * (base_normalise >= P.rsa_nv * 12)


def _api(self, agem_holder, age_holder, smic55_holder, isol, rsa_forfait_logement, br_rmi, af_majo, rsa, af = law.fam.af,
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
    api = max_(0, api1 - rsa_forfait_logement / 12 - br_api / 12 - rsa / 12)
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


def _aefa__2008_(self, age_holder, smic55_holder, af_nbenf, nb_par, ass, aer_holder, api, rsa, af = law.fam.af,
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


def _aefa_2008(self, age_holder, smic55_holder, af_nbenf, nb_par, ass, aer_holder, api, rsa, af = law.fam.af,
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
