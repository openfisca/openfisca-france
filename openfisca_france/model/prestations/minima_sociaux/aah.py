# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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

from ...base import *  # noqa analysis:ignore


@reference_formula
class br_aah(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base ressources de l'allocation adulte handicapé"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        annee_fiscale_n_2 = period.start.offset('first-of', 'year').period('year').offset(-2)

# inactifs ou travailleurs en ESAT :
        br_pf_n_2 = simulation.calculate_add('br_pf', period)
        asi_n_2 = simulation.calculate_add('asi', annee_fiscale_n_2)
        aspa_n_2 = simulation.calculate_add('aspa', annee_fiscale_n_2)
# TODO: travailleurs en milieu protégé : les ressources celles des trois derniers mois.
# toujours la même base ressources ? http://www.guide-familial.fr/actualite-149654--nouvelle-etape-dans-la-reforme-de-l-aah--la-prise-en-compte-trimestrielle-des-ressources.html

        return period, br_pf_n_2 + asi_n_2 + aspa_n_2

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
    Age minimum : Le demandeur ne doit plus avoir l'âge de bénéficier de l'allocation d'éducation de l'enfant
    handicapé, c'est-à-dire qu'il doit être âgé :
    - de plus de vingt ans,
    - ou de plus de seize ans, s'il ne remplit plus les conditions pour ouvrir droit aux allocations familiales.
    Pour les montants http://www.handipole.org/spip.php?article666

    Âge max_
    Le versement de l'AAH prend fin à partir de l'âge minimum légal de départ à la retraite en cas d'incapacité
    de 50 % à 79 %. À cet âge, le bénéficiaire bascule dans le régime de retraite pour inaptitude.
    En cas d'incapacité d'au moins 80 %, une AAH différentielle (c'est-à-dire une allocation mensuelle réduite)
    peut être versée au-delà de l'âge minimum légal de départ à la retraite en complément d'une retraite inférieure
    au minimum vieillesse.

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


@reference_formula
class aah_eligible(SimpleFormulaColumn):
    column = BoolCol
    label = u"Eligibilité à  l'Allocation adulte handicapé"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        law = simulation.legislation_at(period.start)

        invalide = simulation.calculate('invalide', period)
        age = simulation.calculate('age', period)
        smic55 = simulation.calculate('smic55', period)

        eligible_aah = (
            ((invalide) & (age <= law.minim.aah.age_legal_retraite)) &
            ((age >= law.fam.aeeh.age) | ((age >= 16) & (smic55)))
            )

        return period, eligible_aah
    # TODO: dated_function : avant 2008, il fallait ne pas avoir travaillé pendant les 12 mois précédant la demande.


@reference_formula
class nb_eligib_aah(SimpleFormulaColumn):
    column = FloatCol
    label = "Nombre d'allocataires de l'AAH dans la famille"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        br_aah = simulation.calculate('br_aah', period)
        aah_eligible_holder = simulation.calculate('aah_eligible', period)

        aah_eligible = self.split_by_roles(aah_eligible_holder)

        nb_eligib_aah = 0.0 * br_aah
        for eligible in aah_eligible.values():
            nb_eligib_aah = nb_eligib_aah + eligible

        return period, nb_eligib_aah


@reference_formula
class aah_famille(SimpleFormulaColumn):
    column = FloatCol
    label = u"Allocation adulte handicapé (Familles) mensualisée"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        law = simulation.legislation_at(period.start)

        br_aah = simulation.calculate('br_aah', period)
        concub = simulation.calculate('concub', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        nb_eligib_aah = simulation.calculate('nb_eligib_aah', period)

        plaf_ress_aah = 12 * law.minim.aah.montant * (1 + concub + law.minim.aah.tx_plaf_supp * af_nbenf)

        return period, nb_eligib_aah * max_(plaf_ress_aah - br_aah, 0) / 12


@reference_formula
class aah(SimpleFormulaColumn):
    column = FloatCol
    label = u"Allocation adulte handicapé (Individus) mensualisée"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        aah_eligible = simulation.calculate('aah_eligible', period)

        aah_famille_holder = simulation.compute('aah_famille', period)
        aah_famille = self.cast_from_entity_to_role(aah_famille_holder, role = VOUS)

        nb_eligib_aah_holder = simulation.compute('nb_eligib_aah', period)
        nb_eligib_aah = self.cast_from_entity_to_role(nb_eligib_aah_holder, role = VOUS)

        if aah_eligible == 'False':
            return period, 0 * aah_famille
        else:
            return period, aah_famille / nb_eligib_aah


class caah(SimpleFormulaColumn):
    column = FloatCol
    label = u"Complément d'allocation adulte handicapé (mensualisé)"
    entity_class = Individus
    '''
    Complément d'allocation adulte handicapé : complément de ressources ou majoration vie autonome.

    Complément de ressources

    Pour bénéficier du complément de ressources, l’intéressé doit remplir les conditions
    suivantes :
    - percevoir l’allocation aux adultes handicapés à taux normal ou en
       complément d’une pension d’invalidité, d’une pension de vieillesse ou
       d’une rente accident du travail ;
    - avoir un taux d’incapacité égal ou supérieur à 80 % ;
    - avoir une capacité de travail, appréciée par la commission des droits et
       de l’autonomie (CDAPH) inférieure à 5 % du fait du handicap ;
    - ne pas avoir perçu de revenu à caractère professionnel depuis un an à la date
       du dépôt de la demande de complément ;
    - disposer d’un logement indépendant.
    A noter : une personne hébergée par un particulier à son domicile n’est pas
    considérée disposer d’un logement indépendant, sauf s’il s’agit de son conjoint,
    de son concubin ou de la personne avec laquelle elle est liée par un pacte civil
    de solidarité.

    Le complément de ressources est destiné aux personnes handicapées dans l’incapacité de
    travailler. Il est égal à la différence entre la garantie de ressources pour les personnes
    handicapées (GRPH) et l’AAH.

    Majoration pour la vie autonome

    La majoration pour la vie autonome est destinée à permettre aux personnes, en capacité de travailler et
    au chômage en raison de leur handicap, de pourvoir faire face à leur dépense de logement.

    Conditions d'attribution
    La majoration pour la vie autonome est versée automatiquement aux personnes qui remplissent les conditions
    suivantes :
    - percevoir l'AAH à taux normal ou en complément d'un avantage vieillesse ou d'invalidité ou d'une rente
    accident du travail,
    - avoir un taux d'incapacité au moins égal à 80 %,
    - disposer d'un logement indépendant,
    - bénéficier d'une aide au logement (aide personnelle au logement, ou allocation de logement sociale ou
    familiale), comme titulaire du droit, ou comme conjoint, concubin ou partenaire lié par
    un Pacs au titulaire du droit,
    - ne pas percevoir de revenu d'activité à caractère professionnel propre.

    Choix entre la majoration ou la garantie de ressources
    La majoration pour la vie autonome n'est pas cumulable avec la garantie de ressources pour les personnes
    handicapées.
    La personne qui remplit les conditions d'octroi de ces deux avantages doit choisir de bénéficier de l'un ou de
    l'autre.
    '''

    @dated_function(start=date(2005, 7, 1))
    def function(self, simulation period):
        period = period.start.offset('first-of', 'month').period('month')
        law = simulation.legislation_at(period.start)

        law.minim.caah.grph = simulation.calculate(law.minim.caah.cpltx, period)
        law.minim.aah.montant = simulation.calculate(law.minim.aah.montant, period)

        aah = simulation.calculate(aah, period)
        asi = simulation.calculate(asi, period)

        elig_cpl = ((aah > 0) | (asi > 0))  # TODO: & logement indépendant & inactif 12 derniers mois
                                            # & capa de travail < 5% & taux d'invalidité >= 80%
        compl_ress = elig_cpl * max_(law.minim.caah.grph - law.minim.aah.montant / 12, 0)

        elig_mva = (al > 0) * ((aah > 0) | (asi > 0))  # TODO: & logement indépendant & pas de revenus professionnels
                                                       # propres & capa de travail < 5% & taux d'invalidité >= 80%
        mva = 0  # TODO: rentrer mva dans paramètres. mva (mensuelle) = 104,77 en 2015, était de 101,80 en 2006, et de 119,72 en 2007

        return period, max_(compl_ress, mva)

    @dated_function(stop=date(2005, 6, 30))
    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        law = simulation.legislation_at(period.start)

        law.minim.caah.cpltx = simulation.calculate(law.minim.caah.cpltx, period)
        law.minim.aah.montant = simulation.calculate(law.minim.aah.montant, period)

        aah = simulation.calculate(aah, period)
        asi = simulation.calculate(asi, period)

        elig_ancien_caah = ((aah > 0) | (asi > 0)) * (al > 0)  # TODO: & invalidité >= 80%  & logement indépendant
        ancien_caah = law.minim.caah.cpltx * law.minim.aah.montant * elig_ancien_caah
            # En fait le taux cpltx perdure jusqu'en 2008

        return period, ancien_caah
