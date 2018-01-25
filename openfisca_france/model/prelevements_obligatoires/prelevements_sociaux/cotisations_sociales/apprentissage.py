# -*- coding: utf-8 -*-

from __future__ import division

from numpy import datetime64, timedelta64


from openfisca_france.model.base import *  # noqa analysis:ignore


class apprenti(Variable):
    value_type = bool
    entity = Individu
    label = u"L'individu est apprenti"
    reference = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"
    definition_period = MONTH

    def formula(individu, period, parameters):
        age = individu('age', period)
        age_condition = (16 <= age) * (age < 25)
        apprentissage_contrat_debut = individu('apprentissage_contrat_debut', period)
        duree_contrat = (
            datetime64(period.start) + timedelta64(1, 'D') - apprentissage_contrat_debut
            ).astype('timedelta64[Y]')
        anciennete_contrat = (duree_contrat < timedelta64(3, 'Y'))

        return age_condition * anciennete_contrat


class remuneration_apprenti(Variable):
    value_type = float
    entity = Individu
    label = u"Rémunération de l'apprenti"
    reference = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"
    definition_period = MONTH

    # Aux jeunes de 16 à 25 ans (exceptionnellement 15 ans, s'ils ont effectué la scolarité du premier cycle de
    # l'enseignement secondaire, ou, s'ils suivent une "formation apprentissage junior").
    #
    # Depuis le 30 juillet 2011, il est possible pour un jeune mineur ayant 15 ans au cours de l'année civile, de
    # souscrire un contrat d'apprentissage s'il justifie avoir accompli la scolarité du premier cycle de l'enseignement
    # secondaire, ou avoir suivi une formation dans le cadre du dispositif d'initiation aux métiers en
    # alternance (DIMA).

    def formula(individu, period, parameters):
        age = individu('age', period)
        apprentissage_contrat_debut = individu('apprentissage_contrat_debut', period)
        smic = parameters(period).cotsoc.gen.smic_h_b * 52 * 35 / 12
        anciennete_contrat = (
            datetime64(period.start) + timedelta64(1, 'D') - apprentissage_contrat_debut
            ).astype('timedelta64[Y]')
        apprenti = individu('apprenti', period)
        salaire_en_smic = [  # TODO: move to parameters
            dict(
                part_de_smic_by_anciennete = {
                    1: .25,
                    2: .41,
                    3: .53,
                    },
                age_min = 15,
                age_max = 18,
                ),
            dict(
                part_de_smic_by_anciennete = {
                    1: .37,
                    2: .49,
                    3: .61,
                    },
                age_min = 18,
                age_max = 21,
                ),
            dict(
                part_de_smic_by_anciennete = {
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
            age_condition = (age_interval["age_min"] <= age) * (age < age_interval["age_max"])
            output[age_condition] = sum([
                (anciennete_contrat[age_condition] == timedelta64(anciennete, 'Y')) * part_de_smic
                for anciennete, part_de_smic in age_interval['part_de_smic_by_anciennete'].iteritems()
                ])
        return output * smic * apprenti


class exoneration_cotisations_employeur_apprenti(Variable):
    value_type = float
    entity = Individu
    label = u"Exonération de cotisations employeur pour l'emploi d'un apprenti"
    reference = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"
    definition_period = MONTH
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

    def formula(individu, period, parameters):
        accident_du_travail = individu('accident_du_travail', period)
        apprenti = individu('apprenti', period)
        cotisations_employeur = individu('cotisations_employeur', period)
        effectif_entreprise = individu('effectif_entreprise', period)
        famille = individu('famille', period)
        mmid_employeur = individu('mmid_employeur', period)
        vieillesse_deplafonnee_employeur = individu('vieillesse_deplafonnee_employeur', period)
        vieillesse_plafonnee_employeur = individu('vieillesse_plafonnee_employeur', period)

        cotisations_non_exonerees = accident_du_travail
        exoneration_moins_11 = cotisations_non_exonerees - cotisations_employeur

        cotisations_exonerees = (famille + mmid_employeur + vieillesse_plafonnee_employeur +
            vieillesse_deplafonnee_employeur)
        exoneration_plus_11 = -cotisations_exonerees

        return (
            exoneration_plus_11 * (effectif_entreprise >= 11) +
            exoneration_moins_11 * (effectif_entreprise < 11)
            ) * apprenti


class exoneration_cotisations_salariales_apprenti(Variable):
    value_type = float
    entity = Individu
    label = u"Exonération de cotisations salariales pour l'emploi d'un apprenti"
    reference = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"
    definition_period = MONTH

    def formula(individu, period, parameters):
        apprenti = individu('apprenti', period)
        cotisations_salariales_contributives = individu('cotisations_salariales_contributives', period)
        cotisations_salariales_non_contributives = individu(
            'cotisations_salariales_non_contributives', period)
        return - (cotisations_salariales_contributives + cotisations_salariales_non_contributives) * apprenti


class prime_apprentissage(Variable):
    value_type = float
    entity = Individu
    label = u"Prime d'apprentissage pour les entreprise employant un apprenti"
    reference = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"
    definition_period = YEAR
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

    def formula(individu, period, parameters):
        apprenti = individu('apprenti', period)
        return 1000 * apprenti

# # class credit_impot_emploi_apprenti(Variable):
#     value_type = float
#     entity = Individu
#     label = u" Crédit d'impôt pour l'emploi d'apprentis"
#     reference = "http://www.apce.com/pid927/contrat-d-apprentissage.html?espace=1&tp=1&pagination=2"
#
#     def formula(individu, period, parameters):
#         pass
#     # Cet avantage fiscal est réservé aux entreprises imposées selon un régime d'imposition du réel.
#     # Précision : les entreprises exonérées d'impôt sur les bénéfices au titre des entreprises nouvelles, d'une
#     # implantation en zone franche urbaine, du statut de jeune entreprise innovante ou d'une implantation en Corse
#     # peuvent également en bénéficier.
#     #
#     # Le crédit d'impôt est égal au nombre moyen d'apprentis dont le contrat de travail a atteint une durée d'au moins
#     # 1 mois au cours de l'année civile multiplié par :
#     # - 1 600 €,
#     # - ou 2 200€ si l'apprenti est reconnu travailleur handicapé et qu'il bénéficie d'un accompagnement personnalisé,
#     # ou si l'apprenti est employé par une entreprise portant le label "Entreprise du patrimoine vivant", ou s'il est
#     # recruté dans le cadre d'une "formation apprentissage junior".
#     #
#     # L'avantage fiscal est plafonné au montant des dépenses de personnel afférentes aux apprentis minoré des
#     # subventions perçues en contrepartie de leur embauche.


# # class credit_impot_emploi_apprenti(Variable):
#     value_type = float
#     entity = Individu
#     label = u"Déduction de la créance "bonus alternant"
# Les entreprises de plus de 250 salariés, tous établissements confondus, redevables de la taxe d'apprentissage,
# qui emploient plus de 4 % de jeunes en apprentissage (5 % pour la taxe payable en 2016 au titre de 2015), dans la
# limite de 6 % d'alternants, peuvent bénéficier d'une créance à déduire du hors quota de la taxe d'apprentissage (TA).
# Les entreprises concernées doivent calculer elles-mêmes le montant de la créance à déduire de leur TA.
# Son montant est calculé selon la formule suivante : pourcentage d'alternants ouvrant droit à l'aide x effectif annuel
# moyen de l'entreprise au 31 décembre de l'année précédente x un montant forfaitaire de 400 € par alternant.
# Par exemple, une entreprise de 300 salariés employant 6 % de salariés en alternance, ce qui porte le nombre
# d'alternants ouvrant droit à l'aide à 2 % (6 % - 4 %), peut bénéficier d'une prime de : 2 % x 300 x 400 = 2 400 €.
