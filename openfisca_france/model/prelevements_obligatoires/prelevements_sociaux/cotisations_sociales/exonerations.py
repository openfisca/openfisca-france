# -*- coding: utf-8 -*-


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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division


from numpy import datetime64, maximum as max_, minimum as min_, round as round_, timedelta64

from ....base import *  # noqa analysis:ignore


@reference_formula
class exoneration_cotisations_patronales_geographiques(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Exonérations de cotisations patronales dépendant d'une zone géographique"
    url = "https://www.apce.com/pid815/aides-au-recrutement.html?espace=1&tp=1"

    def function(self, simulation, period):
        exonerations_geographiques = [
            'exoneration_cotisations_employeur_zfu',
            'exoneration_cotisations_employeur_zrd',
            'exoneration_cotisations_employeur_zrr',
            ]
        exonerations_montant = 0
        for exoneration in exonerations_geographiques:
            exonerations_montant = exonerations_montant + simulation.calculate_add(exoneration, period)

        return period, exonerations_montant


@reference_formula
class exoneration_cotisations_employeur_zfu(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Exonrérations de cotisations patronales pour l'embauche en zone franche urbaine (ZFU)"
    url = "http://www.apce.com/pid553/exoneration-dans-les-zfu.html?espace=1&tp=1&pagination=2"

# TODO
# Ce dispositif d'exonération sociale est fermé depuis le 1er janvier 2015 mais reste applicable aux entreprises qui
# en bénéficiaient avant cette date.
# - ne pas être détenues à plus de 25 % par des entreprises employant plus de 250 salariés et dont le chiffre d'affaires
#   ou dont le bilan excède 50 M€ ou 43 M€,
# - disposer des éléments d'exploitation ou des stocks nécessaires à l'activité des salariés,
# - être à jour de ses cotisations sociales ou avoir souscrit à un engagement d'apurement progressif de ses dettes.
#
# Secteurs d'activité concernés
#
# L'exonération est applicable, quel que soit le secteur d'activité.
# Toutefois, les entreprises exerçant une activité principale dans les secteurs de la construction automobile,
# construction navale, fabrication de fibres textiles artificielles ou synthétiques, sidérurgie ou des transports
# routiers de marchandises, ne pourront pas bénéficier de cette exonération.

# Embauche de résidents (clause d'embauche locale)
# Pour les entreprises qui se créent ou s'implantent dans une ZFU à compter du 1er janvier 2012,  le bénéfice de
# l'exonération des cotisations sociales est subordonnée lors de toute nouvelle embauche à la condition que la moitié
# de salariés embauchés ou employés résident en ZFU ou en zone urbaine sensible.
#
# Le respect de la condition d'embauche locale est apprécié à la date d'effet de la nouvelle embauche dès la deuxième
# embauche.
#
# Précision : les salariés employés sont ceux déjà présents dans l'entreprise à la date de la nouvelle embauche, les
# salariés embauchés sont ceux recrutés depuis la date de création ou d'implantation de l'entreprise en ZFU.
#
# Est considéré comme résident le salarié habitant soit dans la ZFU d'implantation, soit dans l'une des ZUS de l'unité
# urbaine où se trouve la ZFU. Le maire peut, à la demande de l'employeur, fournir des éléments d'informations relatifs
# à la qualité de résident dans la zone afin de déterminer si la proportion exigée est respectée.
#
# Si la proportion n'est pas respectée à la date d'effet de l'embauche, l'employeur dispose d'un délai de 3 mois pour
# régulariser la situation. A défaut, le bénéfice de l'exonération est suspendu du 1er jour du mois suivant
# l'expiration du délai de 3 mois, jusqu'au 1er jour du mois suivant la date où la condition est de nouveau remplie.
#
# Le salarié résident doit être titulaire d'un contrat à durée indéterminée ou d'un contrat à durée déterminée d'au
# moins 12 mois, conclu pour une durée minimale de 16 heures par semaine.
# 5 ans +
# Dans les entreprises de 5 salariés et plus, les cotisations patronales bénéficient d'un abattement sur la base
# imposable pendant 3 ans de :
# - 60 % la première année,
# - 40 % la seconde année,
# - 20 % la troisième année.
#
# Dans les entreprises de moins de 5 salariés, un abattement est appliqué sur 9 ans de la manière suivante :
# - 60 % les 5 premières années,
# - 40 % les 2 années suivantes,
# - 20 % les deux dernières années.
#
# Le cumul de l'ensemble des aides publiques de minimis (allégements fiscaux, sociaux et aides des collectivités
# territoriales) ne peut dépasser le plafond des aides de minimis, fixé à 200 000 euros sur une période glissante de 36
# mois (100 000 euros pour les entreprises de transport routier).

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        assiette_allegement = simulation.calculate('assiette_allegement', period)
        contrat_de_travail_duree = simulation.calculate('contrat_de_travail_duree', period)  # 0: CDI, 1:CDD
        contrat_de_travail_arrivee = simulation.calculate('contrat_de_travail_arrivee', period)
        contrat_de_travail_depart = simulation.calculate('contrat_de_travail_depart', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        entreprise_chiffre_affaire = simulation.calculate('entreprise_chiffre_affaire', period)
        entreprise_bilan = simulation.calculate('entreprise_bilan', period)
        smic_proratise = simulation.calculate('smic_proratise', period)
        taux_versement_transport = simulation.calculate('taux_versement_transport', period)

        entreprise_eligible = (entreprise_chiffre_affaire <= 1e7) | (entreprise_bilan <= 1e7) # TODO: param

        smic_proratise = simulation.calculate('smic_proratise', period)
        zone_franche_urbaine = simulation.calculate('zone_franche_urbaine', period)

        duree_cdd_eligible = (contrat_de_travail_depart > contrat_de_travail_arrivee + timedelta64(365, 'D'))
        # TODO parameter
        contrat_de_travail_eligible = (contrat_de_travail_arrivee < datetime64("2014-12-31")) * (
            (contrat_de_travail_duree == 0) + (
                (contrat_de_travail_duree == 1) * (duree_cdd_eligible)
                )
            )
        # TODO parameter

        eligible = (
            contrat_de_travail_eligible *
            (effectif_entreprise <= 50) *
            zone_franche_urbaine *
            entreprise_eligible
            )

        bareme_by_name = simulation.legislation_at(period.start).cotsoc.cotisations_employeur['prive_non_cadre']
        taux_max = (
            bareme_by_name['vieillessedeplaf'].rates[0] +
            bareme_by_name['vieillesseplaf'].rates[0] +
            bareme_by_name['maladie'].rates[0] +
            bareme_by_name['famille'].rates[0] +
            bareme_by_name['fnal1'].rates[0] +
            bareme_by_name['fnal2'].rates[0] * (effectif_entreprise >= 20) +
            taux_versement_transport
            )
        # TODO: parameters voir http://www.urssaf.fr/images/ref_lc2009-077.pdf
        seuil_max = 2
        seuil_min = 1.4

        taux_exoneration = compute_taux_exoneration(assiette_allegement, smic_proratise, taux_max, seuil_max, seuil_min)
        exoneration_relative_year_passed = exoneration_relative_year(period, contrat_de_travail_arrivee)
        large_rate_by_year_passed = {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: .60,
            6: .40,
            7: .20,
            }  # TODO: insert in parameter
        small_rate_by_year_passed = {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: .60,
            6: .60,
            7: .60,
            8: .60,
            9: .60,
            10: .40,
            11: .40,
            12: .20,
            13: .20,
            }  # TODO: insert in parameter
        large_taux_exoneration = eligible * 0.0
        small_taux_exoneration = eligible * 0.0
        for year_passed, rate in large_rate_by_year_passed.iteritems():
            if (exoneration_relative_year_passed == year_passed).any():
                large_taux_exoneration[exoneration_relative_year_passed == year_passed] = rate * taux_exoneration

        for year_passed, rate in small_rate_by_year_passed.iteritems():
            if (exoneration_relative_year_passed == year_passed).any():
                small_taux_exoneration[exoneration_relative_year_passed == year_passed] = rate * taux_exoneration

        exoneration_cotisations_zfu = eligible * assiette_allegement * (
            small_taux_exoneration * (effectif_entreprise <= 5) +
            large_taux_exoneration * (effectif_entreprise > 5)
            )
        return period, exoneration_cotisations_zfu
        # TODO: propager dans le temps


@reference_formula
class exoneration_cotisations_employeur_zrd(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Exonrérations de cotisations patronales pour l'embauche en zone de revitalisation rurale (ZRR)"
    url = "http://www.apce.com/pid11668/exoneration-dans-les-zrd.html?espace=1&tp=1"

    # http://www.urssaf.fr/images/ref_LCIRC-2012-0000001.pdf
    # Les entreprises et groupements d'employeurs exerçant une activité industrielle, commerciale, artisanale, agricole
    # ou libérale et cotisant au régime d'assurance chômage.
    # Les entreprises concernées, y compris chacune de celles appartenant à un groupement d'employeurs, doivent avoir
    # au moins un établissement situé en zone de revitalisation rurale.
    #
    # A noter : les associations à but non lucratif sont exclues du dispositif. Par contre, quelle que soit leur forme
    # juridique, les entreprises d'insertion ou d'intérim d'insertion peuvent en bénéficier. Les régies de quartier
    # peuvent en bénéficier lorsque leur activité est susceptible d'entraîner l'assujettissement à la TVA à l'impôt sur
    # les sociétés ainsi qu'à la contribution économique territoriale qu'elles en soient effectivement redevables
    # ou non.
    #
    # L'employeur ne doit avoir procédé à aucun licenciement économique durant les 12 mois précédant l'embauche.

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        assiette_allegement = simulation.calculate('assiette_allegement', period)
        entreprise_creation = simulation.calculate('entreprise_creation', period)
        smic_proratise = simulation.calculate('smic_proratise', period)
        zone_restructuration_defense = simulation.calculate('zone_restructuration_defense', period)

        eligible = zone_restructuration_defense
        taux_max = .281  # TODO: parameters
        seuil_max = 2.4
        seuil_min = 1.4
        taux_exoneration = compute_taux_exoneration(assiette_allegement, smic_proratise, taux_max, seuil_max, seuil_min)

        exoneration_relative_year_passed = exoneration_relative_year(period, entreprise_creation)
        rate_by_year_passed = {
            0: 1,
            1: 1,
            2: 1,
            3: 2 / 3,
            4: 1 / 3,
            }  # TODO: insert in parameter
        ratio = eligible * 0.0
        for year_passed, rate in rate_by_year_passed.iteritems():
            if (exoneration_relative_year_passed == year_passed).any():
                ratio[exoneration_relative_year_passed == year_passed] = rate

        exoneration_cotisations_zrd = ratio * taux_exoneration * assiette_allegement * eligible

        return period, exoneration_cotisations_zrd


@reference_formula
class exoneration_cotisations_employeur_zrr(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Exonrérations de cotisations patronales pour l'embauche en zone de revitalisation rurale (ZRR)"
    url = "http://www.apce.com/pid538/embauches-en-zru-et-zrr.html?espace=1&tp=1"

    # Les entreprises et groupements d'employeurs exerçant une activité industrielle, commerciale, artisanale, agricole
    # ou libérale et cotisant au régime d'assurance chômage.
    # Les entreprises concernées, y compris chacune de celles appartenant à un groupement d'employeurs, doivent avoir
    # au moins un établissement situé en zone de revitalisation rurale.
    #
    # A noter : les associations à but non lucratif sont exclues du dispositif. Par contre, quelle que soit leur forme
    # juridique, les entreprises d'insertion ou d'intérim d'insertion peuvent en bénéficier. Les régies de quartier
    # peuvent en bénéficier lorsque leur activité est susceptible d'entraîner l'assujettissement à la TVA à l'impôt sur
    # les sociétés ainsi qu'à la contribution économique territoriale qu'elles en soient effectivement redevables
    # ou non.
    #
    # L'employeur ne doit avoir procédé à aucun licenciement économique durant les 12 mois précédant l'embauche.

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        assiette_allegement = simulation.calculate('assiette_allegement', period)
        contrat_de_travail_duree = simulation.calculate('contrat_de_travail_duree', period)  # 0: CDI, 1:CDD
        contrat_de_travail_arrivee = simulation.calculate('contrat_de_travail_arrivee', period)
        contrat_de_travail_depart = simulation.calculate('contrat_de_travail_depart', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        smic_proratise = simulation.calculate('smic_proratise', period)
        zone_revitalisation_rurale = simulation.calculate('zone_revitalisation_rurale', period)

        duree_cdd_eligible = contrat_de_travail_depart > contrat_de_travail_arrivee + timedelta64(365, 'D')
        # TODO parameter
        contrat_de_travail_eligible = (
            contrat_de_travail_duree == 0) + (
            (contrat_de_travail_duree == 1) * (duree_cdd_eligible)
            )

        duree_validite = (
            datetime64(period.start) + timedelta64(1, 'D') - contrat_de_travail_arrivee).astype('timedelta64[Y]') < 1

        eligible = (
            contrat_de_travail_eligible *
            (effectif_entreprise <= 50) *
            zone_revitalisation_rurale *
            duree_validite
            )
        taux_max = .281 # TODO: parameters
        seuil_max = 2.4
        seuil_min = 1.5
        taux_exoneration = compute_taux_exoneration(assiette_allegement, smic_proratise, taux_max, seuil_max, seuil_min)
        exoneration_cotisations_zrr = taux_exoneration * assiette_allegement * eligible

        return period, exoneration_cotisations_zrr


# Aides à la création
@reference_formula
class exoneration_is_creation_zrr(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Exonrérations fiscales pour création d'une entreprise en zone de revitalisation rurale (ZRR)"
    url = 'http://www.apce.com/pid11690/exonerations-d-impots-zrr.html?espace=1&tp=1'

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        entreprise_benefice = simulation.calculate('entreprise_benefice', period)
        # TODO: MODIFIER avec création d'entreprise
        contrat_de_travail_duree = simulation.calculate('contrat_de_travail_duree', period)  # 0: CDI, 1:CDD

        contrat_de_travail_arrivee = simulation.calculate('contrat_de_travail_arrivee', period)
        contrat_de_travail_depart = simulation.calculate('contrat_de_travail_depart', period)
        duree_eligible = contrat_de_travail_depart > contrat_de_travail_arrivee + timedelta64(365, 'D')
        # TODO parameter
        contrat_de_travail_eligible = (
            contrat_de_travail_duree == 0) + (
            (contrat_de_travail_duree == 1) * (duree_eligible)
            )
        zone_revitalisation_rurale = simulation.calculate('zone_revitalisation_rurale', period)
        eligible = (
            contrat_de_travail_eligible *
            (effectif_entreprise <= 50) *
            zone_revitalisation_rurale
            )
        exoneration_relative_year_passed = exoneration_relative_year(period, contrat_de_travail_arrivee)
        rate_by_year_passed = {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: .75,
            6: .50,
            7: .25,
            }  # TODO: insert in parameter
        taux_exoneraion = eligible * 0.0
        for year_passed, rate in rate_by_year_passed.iteritems():
            taux_exoneraion[exoneration_relative_year_passed == year_passed] = rate

        return period, taux_exoneraion * entreprise_benefice
        # TODO: mettre sur toutes les années


# @reference_formula
# class bassin_emploi_redynamiser(SimpleFormulaColumn):
#     column = BoolCol
#     entity_class = Individus
#     label = u"L'entreprise est située danns un bassin d'emploi à redynamiser(BER)"
#     # La liste des bassins d'emploi à redynamiser a été fixée par le décret n°2007-228 du 20 février 2007.
#     # Actuellement, deux régions sont concernées : Champagne-Ardenne (zone d'emploi de la Vallée de la Meuse)
#     # et Midi-Pyrénées (zone d'emploi de Lavelanet).
#
#     def function(self, simulation, period):
#         effectif_entreprise = simulation.calculate('effectif_entreprise', period)
#         return period, (effectif_entreprise >= 1) * False


@reference_formula
class zone_restructuration_defense(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"L'entreprise est située dans une zone de restructuration de la Défense (ZRD))"

    def function(self, simulation, period):
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        return period, (effectif_entreprise >= 1) * False


@reference_formula
class zone_franche_urbaine(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"L'entreprise est située danns une zone franche urbaine (ZFU)"

    def function(self, simulation, period):
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        return period, (effectif_entreprise >= 1) * False


@reference_formula
class zone_revitalisation_rurale(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Individus
    label = u"L'entreprise est située dans une zone de revitalisation rurale (ZRR)"

    def function(self, simulation, period):
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        return period, (effectif_entreprise >= 1) * False


# Helpers

def compute_taux_exoneration(assiette_allegement, smic_proratise, taux_max, seuil_max, seuil_min = 1):
    ratio_smic_salaire = smic_proratise / (assiette_allegement + 1e-16)
    # règle d'arrondi: 4 décimales au dix-millième le plus proche (TODO: reprise de l'allègement Fillon unchecked)
    return round_(
        taux_max * min_(1, max_(seuil_max * seuil_min * ratio_smic_salaire - seuil_min, 0) / (seuil_max - seuil_min)),
        4,
        )


def exoneration_relative_year(period, other_date):
    return (datetime64(period.start) + timedelta64(1, 'D') - other_date).astype('timedelta64[Y]')
