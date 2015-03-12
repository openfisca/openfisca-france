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


from numpy import datetime64, timedelta64


from ..base import *  # noqa analysis:ignore


@reference_formula
class remuneration_apprenti(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Rémunération de l'apprenti"
    url = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"

    # Aux jeunes de 16 à 25 ans (exceptionnellement 15 ans, s'ils ont effectué la scolarité du premier cycle de
    # l'enseignement secondaire, ou, s'ils suivent une "formation apprentissage junior").
    #
    # Depuis le 30 juillet 2011, il est possible pour un jeune mineur ayant 15 ans au cours de l'année civile, de
    # souscrire un contrat d'apprentissage s'il justifie avoir accompli la scolarité du premier cycle de l'enseignement
    # secondaire, ou avoir suivi une formation dans le cadre du dispositif d'initiation aux métiers en
    # alternance (DIMA).

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age = simulation.calculate('age', period)
        apprentissage_contrat_debut = simulation.calculate('apprentissage_contrat_debut', period)
        smic = simulation.legislation_at(period.start).cotsoc.gen.smic_h_b * 52 * 35 / 12

        anciennete_contrat = (
            datetime64(period.start) + timedelta64(1, 'D') - apprentissage_contrat_debut
            ).astype('timedelta64[Y]')
        salaire_en_smic = [  # TODO: move to parameters
            dict(
                part_de_smic = {
                    1: .25,
                    2: .41,
                    3: .53,
                    },
                age_min = 15,
                age_max = 18,
                ),
            dict(
                part_de_smic = {
                    1: .37,
                    2: .49,
                    3: .61,
                    },
                age_min = 18,
                age_max = 21,
                ),
            dict(
                part_de_smic = {
                    1: .53,
                    2: .65,
                    3: .78,
                    },
                age_min = 21,
                age_max = 99
                )
            ]

        output = age * 0.0
        for age_interval in salaire_en_smic:
            age_condition = age_interval["age_min"] <= age <= age_interval["age_max"]

            output[age_condition] = sum([
                (anciennete_contrat[age_condition] == anciennete) * part_de_smic
                for anciennete, part_de_smic in age_interval['part_de_smic'].iteritems()
                ])
        return period, output * smic


@reference_formula
class exoneration_cotisations_patronales_apprenti(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Exonération de cotisations patronales pour l'emploi d'un apprenti"
    url = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"
    # Artisans et employeurs de moins de 11 salariés
    #
    # - exonération totale (part patronale et salariale) des charges sociales,
    # - sauf : cotisation sociale patronale d'accidents du travail et des maladies professionnelles, cotisation
    #   supplémentaire accidents du travail et cotisation supplémentaire de retraite complémentaire (c'est-à-dire
    #   dépassant le taux minimum obligatoire).
    #
    # Autres entreprises
    #
    # - exonération totale (part patronale et salariale) des cotisations de sécurité sociale
    #   (maladie-veuvage-vieillesse) et d'allocations familiales,
    # - exonération des autres cotisations sociales salariales,
    # - restent donc dues par l'employeur : les cotisations supplémentaires d'accidents du travail, la part patronale
    #   des cotisations d'accidents du travail et de maladies professionnelles, de retraite complémentaire, d'assurance
    #   chômage et d'AGFF, le versement transport ainsi que les cotisations Fnal.
    # Précision : le décompte de l'effectif des entreprises non artisanales s'apprécie au 31 décembre précédant la date
    # de conclusion du contrat d'apprentissage.
    #

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        bareme_by_name = simulation.legislation_at(period.start).cotsoc.cotisations_employeur['prive_non_cadre']
        taux_max = (
            bareme_by_name['vieillessedeplaf'].rates[0] +
            bareme_by_name['vieillesseplaf'].rates[0] +
            bareme_by_name['maladie'].rates[0] +
            bareme_by_name['famille'].rates[0]
            )
        #TODO
        return period, - taux_max * remuneration_apprenti


@reference_formula
class exoneration_cotisations_salariales_apprenti(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Exonération de cotisations salariales pour l'emploi d'un apprenti"
    url = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"

    def function(self, simulation, period):
        cotisations_salariales = simulation.calculate('cotisations_salariales', period)
        return period, - cotisations_salariales


@reference_formula
class prime_apprentissage(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Prime d'apprentissage pour les entreprise employant un apprenti"
    url = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"

    def function(self, simulation, period):
        pass
    # L'employeur peut également recevoir de la région dans laquelle est situé l'établissement du lieu de travail,
    # une prime d'apprentissage.
    #
    # Les conditions d'attribution de cette aide sont fixées par chaque région (ou pour la Corse, par la collectivité
    # territoriale de Corse) après avis du comité de coordination régional de l'emploi et de la formation
    # professionnelle en tenant compte notamment de l'ensemble de l'effort de l'employeur dans le domaine de
    # l'apprentissage, de la durée de la formation et des objectifs de développement de la formation professionnelle
    # des jeunes sur le territoire de la région (ou de la collectivité territoriale de Corse).
    #
    # Son montant est au minimum de 1 000 euros par année de cycle de formation.
    # nouveau. Depuis le 1er janvier 2014 , cette aide n'est versée qu'aux entreprises de moins de 11 salariés.
    #
    # Son versement est subordonné à la condition que l'embauche de l'apprenti soit confirmée à l'issue des deux
    # premiers mois de l'apprentissage.
    #
    # Son versement cesse lorsque l'apprenti n'est plus salarié dans l'entreprise ou l'établissement qui l'a embauché.


@reference_formula
class credit_impot_emploi_apprenti(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u" Crédit d'impôt pour l'emploi d'apprentis"
    url = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"

    def function(self, simulation, period):
        pass
    # Cet avantage fiscal est réservé aux entreprises imposées selon un régime d'imposition du réel.
    # Précision : les entreprises exonérées d'impôt sur les bénéfices au titre des entreprises nouvelles, d'une
    # implantation en zone franche urbaine, du statut de jeune entreprise innovante ou d'une implantation en Corse
    # peuvent également en bénéficier.
    #
    # Le crédit d'impôt est égal au nombre moyen d'apprentis dont le contrat de travail a atteint une durée d'au moins
    # 1 mois au cours de l'année civile multiplié par :
    # - 1 600 €,
    # - ou 2 200 € si l'apprenti est reconnu travailleur handicapé et qu'il bénéficie d'un accompagnement personnalisé,
    # ou si l'apprenti est employé par une entreprise portant le label "Entreprise du patrimoine vivant", ou s'il est
    # recruté dans le cadre d'une "formation apprentissage junior".
    #
    # L'avantage fiscal est plafonné au montant des dépenses de personnel afférentes aux apprentis minoré des
    # subventions perçues en contrepartie de leur embauche.
