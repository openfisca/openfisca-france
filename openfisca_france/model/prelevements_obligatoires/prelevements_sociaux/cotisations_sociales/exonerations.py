# -*- coding: utf-8 -*-

from __future__ import division


from numpy import datetime64, maximum as max_, minimum as min_, round as round_, timedelta64

from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.base import apply_bareme_for_relevant_type_sal

class jei_date_demande(Variable):
    column = DateCol(default = date(2099, 12, 31))
    entity_class = Individus
    label = u"Date de demande (et d'octroi) du statut de jeune entreprise innovante (JEI)"


class exoneration_cotisations_employeur_geographiques(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Exonérations de cotisations employeur dépendant d'une zone géographique"
    url = "https://www.apce.com/pid815/aides-au-recrutement.html?espace=1&tp=1"

    def function(self, simulation, period):
        exoneration_cotisations_employeur_zfu = simulation.calculate_add('exoneration_cotisations_employeur_zfu',
            period)
        exoneration_cotisations_employeur_zrd = simulation.calculate_add('exoneration_cotisations_employeur_zrd',
            period)
        exoneration_cotisations_employeur_zrr = simulation.calculate_add('exoneration_cotisations_employeur_zrr',
            period)

        exonerations_geographiques = (exoneration_cotisations_employeur_zfu + exoneration_cotisations_employeur_zrd +
            exoneration_cotisations_employeur_zrr)

        return period, exonerations_geographiques


class exoneration_cotisations_employeur_jei(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Exonrérations de cotisations employeur pour une jeune entreprise innovante"
    url = "http://www.apce.com/pid1653/jeune-entreprise-innovante.html?pid=1653&pagination=2"

    def function(self, simulation, period):
        period = period.this_month
        assiette_allegement = simulation.calculate('assiette_allegement', period)
        jei_date_demande = simulation.calculate('jei_date_demande', period)
        jeune_entreprise_innovante = simulation.calculate('jeune_entreprise_innovante', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        smic_proratise = simulation.calculate('smic_proratise', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)

        bareme_by_type_sal_name = simulation.legislation_at(period.start).cotsoc.cotisations_employeur
        bareme_names = ['vieillesse_deplafonnee', 'vieillesse_plafonnee', 'maladie', 'famille']

        exoneration = smic_proratise * 0.0
        for bareme_name in bareme_names:
            exoneration += apply_bareme_for_relevant_type_sal(
                bareme_by_type_sal_name = bareme_by_type_sal_name,
                bareme_name = bareme_name,
                categorie_salarie = categorie_salarie,
                base = min_(assiette_allegement, 4.5 * smic_proratise),
                plafond_securite_sociale = plafond_securite_sociale,
                round_base_decimals = 2,
                )

        exoneration_relative_year_passed = exoneration_relative_year(period, jei_date_demande)
        rate_by_year_passed = {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: 1,
            6: 1,
            7: 1,
            }  # TODO: move to legislation parameters file
        for year_passed, rate in rate_by_year_passed.iteritems():
            condition_on_year_passed = exoneration_relative_year_passed == timedelta64(year_passed, 'Y')
            if condition_on_year_passed.any():
                exoneration[condition_on_year_passed] = rate * exoneration

        return period, - exoneration * jeune_entreprise_innovante


class exoneration_cotisations_employeur_zfu(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Exonrérations de cotisations employeur pour l'embauche en zone franche urbaine (ZFU)"
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
# Dans les entreprises de 5 salariés et plus, les cotisations employeur bénéficient d'un abattement sur la base
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
        period = period.this_month
        assiette_allegement = simulation.calculate('assiette_allegement', period)
        contrat_de_travail_duree = simulation.calculate('contrat_de_travail_duree', period)  # 0: CDI, 1:CDD
        contrat_de_travail_debut = simulation.calculate('contrat_de_travail_debut', period)
        contrat_de_travail_fin = simulation.calculate('contrat_de_travail_fin', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        entreprise_chiffre_affaire = simulation.calculate('entreprise_chiffre_affaire', period)
        entreprise_bilan = simulation.calculate('entreprise_bilan', period)
        taux_versement_transport = simulation.calculate('taux_versement_transport', period)

        # TODO: move to legislation parameters file
        entreprise_eligible = (entreprise_chiffre_affaire <= 1e7) | (entreprise_bilan <= 1e7)

        smic_proratise = simulation.calculate('smic_proratise', period)
        zone_franche_urbaine = simulation.calculate('zone_franche_urbaine', period)

        duree_cdd_eligible = (contrat_de_travail_fin > contrat_de_travail_debut + timedelta64(365, 'D'))
        # TODO: move to legislation parameters file
        contrat_de_travail_eligible = (contrat_de_travail_debut <= datetime64("2014-12-31")) * (
            (contrat_de_travail_duree == 0) + (
                (contrat_de_travail_duree == 1) * (duree_cdd_eligible)
                )
            )
        # TODO: move to legislation parameters file

        eligible = (
            contrat_de_travail_eligible *
            (effectif_entreprise <= 50) *
            zone_franche_urbaine *
            entreprise_eligible
            )
        bareme_by_name = simulation.legislation_at(period.start).cotsoc.cotisations_employeur['prive_non_cadre']
        taux_max = (
            bareme_by_name['vieillesse_deplafonnee'].rates[0] +
            bareme_by_name['vieillesse_plafonnee'].rates[0] +
            bareme_by_name['maladie'].rates[0] +
            bareme_by_name['famille'].rates[0] +
            bareme_by_name['fnal1'].rates[0] +
            bareme_by_name['fnal2'].rates[0] * (effectif_entreprise >= 20) +
            taux_versement_transport
            )
        # TODO: move to legislation parameters file : voir http://www.urssaf.fr/images/ref_lc2009-077.pdf
        seuil_max = 2
        seuil_min = 1.4

        taux_exoneration = compute_taux_exoneration(assiette_allegement, smic_proratise, taux_max, seuil_max, seuil_min)
        exoneration_relative_year_passed = exoneration_relative_year(period, contrat_de_travail_debut)
        large_rate_by_year_passed = {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: .60,
            6: .40,
            7: .20,
            }  # TODO: move to legislation parameters file
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
            }  # TODO: move to legislation parameters file
        large_taux_exoneration = eligible * 0.0
        small_taux_exoneration = eligible * 0.0
        for year_passed, rate in large_rate_by_year_passed.iteritems():
            condition_on_year_passed = exoneration_relative_year_passed == timedelta64(year_passed, 'Y')
            if condition_on_year_passed.any():
                large_taux_exoneration[condition_on_year_passed] = rate * taux_exoneration

        for year_passed, rate in small_rate_by_year_passed.iteritems():
            if condition_on_year_passed.any():
                small_taux_exoneration[condition_on_year_passed] = rate * taux_exoneration

        exoneration_cotisations_zfu = eligible * assiette_allegement * (
            small_taux_exoneration * (effectif_entreprise <= 5) +
            large_taux_exoneration * (effectif_entreprise > 5)
            )
        return period, exoneration_cotisations_zfu
        # TODO: propager dans le temps


class exoneration_cotisations_employeur_zrd(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Exonrérations de cotisations employeur pour l'embauche en zone de restructuration de la Défense (ZRD)"
    url = "http://www.apce.com/pid11668/exoneration-dans-les-zrd.html?espace=1&tp=1"

    def function(self, simulation, period):
        period = period.this_month
        assiette_allegement = simulation.calculate('assiette_allegement', period)
        entreprise_creation = simulation.calculate('entreprise_creation', period)
        smic_proratise = simulation.calculate('smic_proratise', period)
        zone_restructuration_defense = simulation.calculate('zone_restructuration_defense', period)

        eligible = zone_restructuration_defense
        taux_max = .281  # TODO: move to legislation parameters file
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
            }  # TODO: move to legislation parameters file
        ratio = eligible * 0.0
        for year_passed, rate in rate_by_year_passed.iteritems():
            condition_on_year_passed = exoneration_relative_year_passed == timedelta64(year_passed, 'Y')
            if condition_on_year_passed.any():
                ratio[condition_on_year_passed] = rate

        exoneration_cotisations_zrd = ratio * taux_exoneration * assiette_allegement * eligible

        return period, exoneration_cotisations_zrd


class exoneration_cotisations_employeur_zrr(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Exonrérations de cotisations employeur pour l'embauche en zone de revitalisation rurale (ZRR)"
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
        period = period.this_month
        assiette_allegement = simulation.calculate('assiette_allegement', period)
        contrat_de_travail_duree = simulation.calculate('contrat_de_travail_duree', period)  # 0: CDI, 1:CDD
        contrat_de_travail_debut = simulation.calculate('contrat_de_travail_debut', period)
        contrat_de_travail_fin = simulation.calculate('contrat_de_travail_fin', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        smic_proratise = simulation.calculate('smic_proratise', period)
        zone_revitalisation_rurale = simulation.calculate('zone_revitalisation_rurale', period)

        duree_cdd_eligible = contrat_de_travail_fin > contrat_de_travail_debut + timedelta64(365, 'D')
        # TODO: move to legislation parameters file
        contrat_de_travail_eligible = (
            contrat_de_travail_duree == 0) + (
            (contrat_de_travail_duree == 1) * (duree_cdd_eligible)
            )

        duree_validite = (
            datetime64(period.start) + timedelta64(1, 'D') - contrat_de_travail_debut
            ).astype('timedelta64[Y]') < timedelta64(1, 'Y')

        eligible = (
            contrat_de_travail_eligible *
            (effectif_entreprise <= 50) *
            zone_revitalisation_rurale *
            duree_validite
            )
        taux_max = .281 if period.start.year < 2015 else .2655  # TODO: move to legislation parameters file
        seuil_max = 2.4
        seuil_min = 1.5
        taux_exoneration = compute_taux_exoneration(assiette_allegement, smic_proratise, taux_max, seuil_max, seuil_min)
        exoneration_cotisations_zrr = taux_exoneration * assiette_allegement * eligible

        return period, exoneration_cotisations_zrr


# Aides à la création
class exoneration_is_creation_zrr(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Exonrérations fiscales pour création d'une entreprise en zone de revitalisation rurale (ZRR)"
    url = 'http://www.apce.com/pid11690/exonerations-d-impots-zrr.html?espace=1&tp=1'

    def function(self, simulation, period):
        period = period.this_year
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        entreprise_benefice = simulation.calculate('entreprise_benefice', period)
        # TODO: MODIFIER avec création d'entreprise
        contrat_de_travail_duree = simulation.calculate('contrat_de_travail_duree', period)  # 0: CDI, 1:CDD

        contrat_de_travail_debut = simulation.calculate('contrat_de_travail_debut', period)
        contrat_de_travail_fin = simulation.calculate('contrat_de_travail_fin', period)
        duree_eligible = contrat_de_travail_fin > contrat_de_travail_debut + timedelta64(365, 'D')
        # TODO: move to legislation parameters file
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
        exoneration_relative_year_passed = exoneration_relative_year(period, contrat_de_travail_debut)
        rate_by_year_passed = {
            0: 1,
            1: 1,
            2: 1,
            3: 1,
            4: 1,
            5: .75,
            6: .50,
            7: .25,
            }  # TODO: move to legislation parameters file
        taux_exoneraion = eligible * 0.0
        for year_passed, rate in rate_by_year_passed.iteritems():
            condition_on_year_passed = exoneration_relative_year_passed == timedelta64(year_passed, 'Y')
            taux_exoneraion[condition_on_year_passed] = rate

        return period, taux_exoneraion * entreprise_benefice
        # TODO: mettre sur toutes les années


# # class bassin_emploi_redynamiser(Variable):
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

class jeune_entreprise_innovante(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"L'entreprise est une jeune entreprise innovante"

    def function(self, simulation, period):
        # Toute entreprise existante au 1er janvier 2004 ou créée entre le 1er janvier 2004 et le 31 décembre 2016 à
        # condition de remplir les conditions suivantes :
        #
        # avoir moins de 8 ans d'existence au moment de la demande
        #
        # être réellement nouvelle, c'est-à-dire ne pas avoir été créée dans le cadre d'une concentration,
        # d'une restructuration, d'une extension d'activité préexistante ou d'une reprise
        #
        # employer moins de 250 personnes au cours de l'exercice au titre duquel elle demande à bénéficier de ce statut
        #
        # réaliser un chiffre d'affaires inférieur à 50 M€  et disposer d'un total de bilan inférieur à 43 M€
        #
        # être indépendante, c'est-à-dire que son capital doit être détenu pour 50 % au minimum par :
        #
        # - des personnes physiques
        #
        # - une ou plusieurs autres JEI dont 50 % du capital au moins est détenu par des personnes physiques
        #
        # - des associations ou fondations reconnues d'utilité publique à caractère scientifique
        #
        # - des établissements de recherche et d'enseignement et leurs filiales
        #
        # - des structures d'investissement sous réserve qu'il n'y ait pas de lien de dépendance telles que des :
        #   -  fonds communs de placement dans l'innovation (FCPI)
        #   -  sociétés de capital-risque
        #   -  fonds d'investissement de proximité (FIP)
        #   -  sociétés de développement régional (SDR)
        #   -  sociétés financières d'innovation (SFI)
        #   -  sociétés unipersonnelles d'investissements à risques (SUIR).
        #
        # réaliser des dépenses de R§D représentant au moins 15 % des charges fiscalement déductibles au titre du même
        # exercice.
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        entreprise_bilan = simulation.calculate('entreprise_bilan', period)
        entreprise_chiffre_affaire = simulation.calculate('entreprise_chiffre_affaire', period)
        entreprise_creation = simulation.calculate('entreprise_creation', period)
        # entreprise_depenses_rd =  simulation.calculate('entreprise_depenses_rd', period)
        jei_date_demande = simulation.calculate('jei_date_demande', period)
        # TODO: move to legislation parameters file
        # entreprise_depenses_rd > .15 TODO
        independance = True
        jeune_entreprise_innovante = (
            independance *
            (effectif_entreprise < 250) *
            (entreprise_creation <= datetime64("2016-12-31")) *
            (
                (jei_date_demande + timedelta64(1, 'D') - entreprise_creation).astype('timedelta64[Y]') <
                timedelta64(8, 'Y')
                ) *
            (entreprise_chiffre_affaire < 50e6) *
            (entreprise_bilan < 43e6)
            )
        return period, jeune_entreprise_innovante


class bassin_emploi_redynamiser(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"L'entreprise est située danns un bassin d'emploi à redynamiser (BER)"
    # La liste des bassins d'emploi à redynamiser a été fixée par le décret n°2007-228 du 20 février 2007.
    # Actuellement, deux régions sont concernées : Champagne-Ardenne (zone d'emploi de la Vallée de la Meuse)
    # et Midi-Pyrénées (zone d'emploi de Lavelanet).

    def function(self, simulation, period):
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)

        return period, (effectif_entreprise >= 1) * False


class zone_restructuration_defense(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"L'entreprise est située dans une zone de restructuration de la Défense (ZRD)"

    def function(self, simulation, period):
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        return period, (effectif_entreprise >= 1) * False


class zone_franche_urbaine(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"L'entreprise est située danns une zone franche urbaine (ZFU)"

    def function(self, simulation, period):
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        return period, (effectif_entreprise >= 1) * False


class zone_revitalisation_rurale(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"L'entreprise est située dans une zone de revitalisation rurale (ZRR)"

    def function(self, simulation, period):
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        return period, (effectif_entreprise >= 1) * False


# Helpers

def compute_taux_exoneration(assiette_allegement, smic_proratise, taux_max, seuil_max, seuil_min = 1):
    ratio_smic_salaire = smic_proratise / (assiette_allegement + 1e-16)
    # règle d'arrondi: 4 décimales au dix-millième le plus proche ( # TODO: reprise de l'allègement Fillon unchecked)
    return round_(
        taux_max * min_(1, max_(seuil_max * seuil_min * ratio_smic_salaire - seuil_min, 0) / (seuil_max - seuil_min)),
        4,
        )


def exoneration_relative_year(period, other_date):
    return (datetime64(period.start) + timedelta64(1, 'D') - other_date).astype('timedelta64[Y]')
