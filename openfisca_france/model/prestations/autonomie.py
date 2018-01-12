# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_france.model.base import *  # noqa analysis:ignore


class base_ressources_apa(Variable):
    value_type = float
    label = u"Ressources considérées dans le calcul de l'APA"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        period = period.first_month
        revenu_fiscal_de_reference = individu.foyer_fiscal('rfr', period.n_2) / 12
        aide_logement_montant = individu.famille('aide_logement_montant', period)
        valeur_locative_immo_non_loue = individu('valeur_locative_immo_non_loue', period)
        valeur_locative_terrains_non_loue = individu('valeur_locative_terrains_non_loue', period)

        return revenu_fiscal_de_reference - (
            valeur_locative_immo_non_loue + valeur_locative_terrains_non_loue + aide_logement_montant
            )


class apa_domicile_participation(Variable):
    value_type = float
    label = u"Participation du bénéficiaire de l'APA à domicile en euros"
    entity = Individu
    definition_period = MONTH


    def formula_2002(individu, period, parameters):
        # Les départements doivent appliquer la nouvelle formule
        # entre le 1er mars 2016 et le 28 février 2017
        base_ressources_apa = individu('base_ressources_apa', period)
        en_couple = individu.famille('en_couple', period)
        parameters = parameters(period.start).autonomie
        seuil_inf = parameters.apa_domicile.seuil_de_revenu_en_part_du_mtp.seuil_inferieur
        seuil_sup = parameters.apa_domicile.seuil_de_revenu_en_part_du_mtp.seuil_superieur
        majoration_tierce_personne = parameters.mtp.mtp
        taux_min_participation = parameters.apa_domicile.taux_de_participation_minimum
        taux_max_participation = parameters.apa_domicile.taux_de_participation_maximum
        proratisation_couple = (
            1 +
            en_couple * (parameters.apa_domicile.divison_des_ressources_du_menage_pour_les_couples - 1)
            )
        dependance_plan_aide_domicile_accepte = individu('dependance_plan_aide_domicile_accepte', period)
        base_ressources_apa_domicile = base_ressources_apa / proratisation_couple

        condition_ressources_domicile = [
            base_ressources_apa_domicile <= (seuil_inf * majoration_tierce_personne),
            (seuil_inf * majoration_tierce_personne) < base_ressources_apa_domicile <= (seuil_sup * majoration_tierce_personne),
            base_ressources_apa_domicile > (seuil_sup * majoration_tierce_personne),
            ]
        taux_participation = [
            taux_min_participation,
            (base_ressources_apa_domicile - seuil_inf * majoration_tierce_personne) / ((seuil_sup - seuil_inf) * majoration_tierce_personne) * taux_max_participation,
            taux_max_participation,
            ]
        return select(condition_ressources_domicile, taux_participation) * dependance_plan_aide_domicile_accepte


    def formula_2016_03_01(individu, period, parameters):
        # Les départements doivent appliquer la nouvelle formule
        # entre le 1er mars 2016 et le 28 février 2017
        base_ressources_apa = individu('base_ressources_apa', period)
        en_couple = individu.famille('en_couple', period)
        dependance_plan_aide_domicile_accepte = individu('dependance_plan_aide_domicile_accepte', period)
        parameters = parameters(period.start).autonomie
        majoration_tierce_personne = parameters.mtp.mtp
        proratisation_couple = (
            1 +
            en_couple * (parameters.apa_domicile.divison_des_ressources_du_menage_pour_les_couples - 1)
            )
        base_ressources_apa_domicile = base_ressources_apa / proratisation_couple


        premier_seuil = 0.317 * majoration_tierce_personne
        second_seuil = 0.498 * majoration_tierce_personne
        condlist = [
            dependance_plan_aide_domicile_accepte <= premier_seuil,
            premier_seuil <= dependance_plan_aide_domicile_accepte <= second_seuil,
            dependance_plan_aide_domicile_accepte >= second_seuil,
            ]
        choicelist_1 = [
            dependance_plan_aide_domicile_accepte,
            premier_seuil,
            premier_seuil,
            ]
        choicelist_2 = [
            0,
            dependance_plan_aide_domicile_accepte - premier_seuil,
            second_seuil,
            ]
        choicelist_3 = [
            0,
            0,
            dependance_plan_aide_domicile_accepte - (premier_seuil + second_seuil)
            ]
        A_1 = select(condlist, choicelist_1)
        A_2 = select(condlist, choicelist_2)
        A_3 = select(condlist, choicelist_3)

        apa_domicile_participation = min_(0.9 * dependance_plan_aide_domicile_accepte,
            0.9 *
            max_(0, base_ressources_apa_domicile - 0.725 * majoration_tierce_personne) / (1.945 * majoration_tierce_personne) *
            (
                A_1 +
                A_2 * (
                    (1 - 0.4) * base_ressources_apa_domicile / (1.945 * majoration_tierce_personne) +
                    (0.4 * 2.67 * majoration_tierce_personne - 0.725 * majoration_tierce_personne) / (1.945 * majoration_tierce_personne)
                    ) +
                A_3 * (
                    (1 - 0.2) * base_ressources_apa_domicile / (1.945 * majoration_tierce_personne) +
                    (0.2 * 2.67 * majoration_tierce_personne - 0.725 * majoration_tierce_personne) / (1.945 * majoration_tierce_personne)
                    )
                )
            )

        return apa_domicile_participation


class apa_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = u"Allocation personalisée d'autonomie - Éligibilité"
    definition_period = MONTH

    def formula(individu, period, parameters):
        period = period.start.offset('first-of', 'month').period('month')
        parameters = parameters(period.start).autonomie
        age = individu('age', period)
        apa_age_min = parameters.age_ouverture_des_droits.age_d_ouverture_des_droits

        gir = individu('gir', period)
        eligibilite_gir = (
            (gir == TypesGir.gir_1) +
            (gir == TypesGir.gir_2) +
            (gir == TypesGir.gir_3) +
            (gir == TypesGir.gir_4)
            )

        return (age >= apa_age_min) * eligibilite_gir


class apa_domicile_taux_participation(Variable):
    value_type = float
    label = u"Taux de participation du bénéficiaire à l'APA à domicile"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        dependance_plan_aide_domicile_accepte = individu('dependance_plan_aide_domicile_accepte', period)
        apa_domicile_participation = individu('apa_domicile_participation', period)

        return (apa_domicile >= 0) * apa_domicile_participation / dependance_plan_aide_domicile_accepte


class apa_domicile(Variable):
    value_type = float
    label = u"Allocation personalisée d'autonomie"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        period = period.start.offset('first-of', 'month').period('month')
        parameters = parameters(period.start).autonomie
        apa_eligibilite = individu('apa_eligibilite', period)
        seuil_non_versement = parameters.seuil_de_versement_de_l_apa.seuil_versement.seuil_de_versement_de_l_apa
        dependance_plan_aide_domicile_accepte = individu('dependance_plan_aide_domicile_accepte', period)

        apa_domicile_participation = individu('apa_domicile_participation', period)

        apa = dependance_plan_aide_domicile_accepte - apa_domicile_participation
        return apa * (apa >= seuil_non_versement) * apa_eligibilite


class apa_etablissement(Variable):
    value_type = float
    label = u"Allocation personalisée d'autonomie en institution"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        period = period.start.offset('first-of', 'month').period('month')
        parameters = parameters(period.start).autonomie
        seuil_non_versement = parameters.seuil_de_versement_de_l_apa.seuil_versement.seuil_de_versement_de_l_apa

        en_couple = individu.famille('en_couple', period)
        apa_eligibilite = individu('apa_eligibilite', period)
        gir = individu('gir', period)
        base_ressources_apa = individu('base_ressources_apa', period)
        proratisation_couple_etablissement = (
            1 +
            en_couple * (parameters.apa_institution.divison_des_ressources_du_menage_pour_les_couples - 1)
            )
        base_ressources_apa_etablissement = base_ressources_apa / proratisation_couple_etablissement
        dependance_tarif_etablissement_gir_5_6 = individu('dependance_tarif_etablissement_gir_5_6', period)
        dependance_tarif_etablissement_gir_dependant = individu('dependance_tarif_etablissement_gir_dependant', period)
        seuil_inf_inst = parameters.apa_institution.seuil_de_revenu_en_part_du_mtp.seuil_inferieur
        seuil_sup_inst = parameters.apa_institution.seuil_de_revenu_en_part_du_mtp.seuil_superieur
        majoration_tierce_personne = parameters.mtp.mtp

        conditions_ressources = [
            base_ressources_apa_etablissement <= seuil_inf_inst * majoration_tierce_personne,
            seuil_inf_inst * majoration_tierce_personne < base_ressources_apa_etablissement <= seuil_sup_inst * majoration_tierce_personne,
            base_ressources_apa > seuil_sup_inst * majoration_tierce_personne
            ]
        participations = [
            dependance_tarif_etablissement_gir_5_6,
            (
                dependance_tarif_etablissement_gir_5_6 +
                (dependance_tarif_etablissement_gir_dependant - dependance_tarif_etablissement_gir_5_6) * (
                    (base_ressources_apa - seuil_inf_inst * majoration_tierce_personne) /
                    ((seuil_sup_inst - seuil_inf_inst) * majoration_tierce_personne) * 0.80
                    )
                ),
            dependance_tarif_etablissement_gir_5_6 + (
                dependance_tarif_etablissement_gir_dependant - dependance_tarif_etablissement_gir_5_6) * 0.80
            ]
        participation_beneficiaire = select(conditions_ressources, participations)
        taux_reste_a_vivre = parameters.apa_institution.taux_reste_a_vivre
        participation_beneficiaire = min_(
            participation_beneficiaire,
            max_(base_ressources_apa_etablissement * (1 - taux_reste_a_vivre), 0)
            )
        apa = dependance_tarif_etablissement_gir_dependant - participation_beneficiaire

        eligibilite_etablissement = (
            (dependance_tarif_etablissement_gir_5_6 > 0) * (dependance_tarif_etablissement_gir_dependant > 0)
            )  # permet de sélectionner les individus vivant en établissement éligible.

        return apa * (apa >= seuil_non_versement) * eligibilite_etablissement * apa_eligibilite


class TypesGir(Enum):
    __order__ = 'gir_1 gir_2 gir_3 gir_4 gir_5 gir_6'  # Needed to preserve the enum order in Python 2
    non_defini = u"Non défini"
    gir_1 = u"Gir 1"
    gir_2 = u"Gir 2"
    gir_3 = u"Gir 3"
    gir_4 = u"Gir 4"
    gir_5 = u"Gir 5"
    gir_6 = u"Gir 6"


class gir(Variable):
    value_type = Enum
    possible_values = TypesGir
    default_value = TypesGir.non_defini
    entity = Individu
    label = u"Groupe iso-ressources de l'individu"
    definition_period = MONTH


class dependance_plan_aide_domicile(Variable):
    value_type = float
    entity = Individu
    label = u"Coût du plan d'aide à domicile pour une personne dépendante"
    definition_period = MONTH


class dependance_tarif_etablissement_gir_5_6(Variable):
    value_type = float
    entity = Individu
    label = u"Tarif dépendance de l'établissement pour les GIR 5 et 6"
    definition_period = MONTH


class dependance_tarif_etablissement_gir_dependant(Variable):
    value_type = float
    entity = Individu
    label = u"Tarif dépendance de l'établissement pour le GIR de la personne dépendante"
    definition_period = MONTH


class apa_urgence_domicile(Variable):
    value_type = float
    label = u"Allocation personalisée d'autonomie d'urgence à domicile"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        period = period.first_month
        parameters = parameters(period.start).autonomie
        majoration_tierce_personne = autonomie.mtp.mtp
        plafond_gir1 = parameters.apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_1
        part_urgence_domicile = parameters.apa_domicile.apa_d_urgence.part_du_plafond_de_l_apa_a_domicile
        return part_urgence_domicile * plafond_gir1 * majoration_tierce_personne


class apa_urgence_institution(Variable):
    value_type = float
    label = u"Allocation personalisée d'autonomie en institution"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period, parameters):
        period = period.start.offset('first-of', 'month').period('month')
        dependance_tarif_etablissement_gir_1_2 = individu('dependance_tarif_etablissement_gir_5_6', period)
        part_urgence_institution = parameters.apa_institution.apa_d_urgence.part_du_tarif_dependance_gir_1_2_de_l_etablissement_d_accueil
        apa_urgence_institution = part_urgence_institution * dependance_tarif_etablissement_gir_1_2
        return apa_urgence_institution


class dependance_plan_aide_domicile_accepte(Variable):
    value_type = float
    label = u"Coût du plan d'aide plafonné pris en compte pour la détermination de l'APA"
    entity = Individu
    definition_period = MONTH
    reference = [
        # Code de l'action sociale et des familles - Article R232-10-1
        'https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=4D213136F764CDAC77B33F705B4DE178.tplgfr41s_1?idArticle=LEGIARTI000032133764&cidTexte=LEGITEXT000006074069&dateTexte=20170929&categorieLien=id&oldAction=&nbResultRech='
    ]

    def formula(individu, period, parameters):
        gir = individu('gir', period)
        dependance_plan_aide_domicile = individu('dependance_plan_aide_domicile', period)
        parameters_autonomie = parameters(period.start).autonomie

        plafond_gir1 = parameters_autonomie.apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_1
        plafond_gir2 = parameters_autonomie.apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_2
        plafond_gir3 = parameters_autonomie.apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_3
        plafond_gir4 = parameters_autonomie.apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_4
        majoration_tierce_personne = parameters_autonomie.mtp.mtp

        condition_plafond_par_gir = [
            gir == TypesGir.gir_1,
            gir == TypesGir.gir_2,
            gir == TypesGir.gir_3,
            gir == TypesGir.gir_4,
            ]
        valeur_plafond_par_gir = [
            plafond_gir1 * majoration_tierce_personne,
            plafond_gir2 * majoration_tierce_personne,
            plafond_gir3 * majoration_tierce_personne,
            plafond_gir4 * majoration_tierce_personne,
            ]
        plafond_par_gir = select(condition_plafond_par_gir, valeur_plafond_par_gir)
        return min_(plafond_par_gir, dependance_plan_aide_domicile)
