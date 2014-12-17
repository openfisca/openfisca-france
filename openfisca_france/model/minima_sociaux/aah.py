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

from numpy import (maximum as max_)

from ..base import *  # noqa


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


def _caah__2005(aah, asi, P = law.minim):
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

def _caah_2006_(aah, asi, br_aah, al, P = law.minim):
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
