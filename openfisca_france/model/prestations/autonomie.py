# -*- coding: utf-8 -*-


from __future__ import division

import numpy as np
from numpy import maximum as max_, minimum as min_, select

from openfisca_france.model.base import *  # noqa analysis:ignore


# TODO: fill the parameters file. May be should use the majoration pour tierce personne as parameter

seuil_non_versement = 28.83
taux_reste_a_vivre = 0.10


class base_ressources_apa(Variable):
    column = FloatCol
    label = u"Ressources considérées dans le calcul de l'APA"
    entity = Individu

    def function(individu, period):
        period = period.this_month
        revenu_fiscal_de_reference = individu.foyer_fiscal('rfr', period.n_2) / 12
        aide_logement_montant = individu.famille('aide_logement_montant', period)
        valeur_locative_immo_non_loue = individu('valeur_locative_immo_non_loue', period)
        valeur_locative_terrains_non_loue = individu('valeur_locative_terrains_non_loue', period)

        base_ressources_apa = revenu_fiscal_de_reference - (
            valeur_locative_immo_non_loue + valeur_locative_terrains_non_loue + aide_logement_montant
            )
        return period, base_ressources_apa


class apa_domicile_participation(DatedVariable):
    column = FloatCol
    label = u"Participation du bénéficiaire de l'APA à domicile"
    entity = Individu

    @dated_function(start = date(2002, 1, 1), stop = date(2016, 2, 29))
    def function_2002_20160229(individu, period, legislation):
        # Les départements doivent appliquer la nouvelle formule
        # entre le 1er mars 2016 et le 28 février 2017
        base_ressources_apa = individu('base_ressources_apa', period)
        dependance_plan_aide_domicile = individu('dependance_plan_aide_domicile', period)
        en_couple = individu.famille('en_couple', period)
        gir = individu('gir', period)
        legislation = legislation(period.start).autonomie
        seuil_inf = legislation.apa_domicile.seuil_de_revenu_en_part_du_mtp.seuil_inferieur
        seuil_sup = legislation.apa_domicile.seuil_de_revenu_en_part_du_mtp.seuil_superieur
        majoration_tierce_personne = legislation.mtp.mtp
        taux_min_participation = legislation.apa_domicile.taux_de_participation_minimum
        taux_max_participation = legislation.apa_domicile.taux_de_participation_maximum
        proratisation_couple = (
            1 +
            en_couple * (legislation.apa_domicile.divison_des_ressources_du_menage_pour_les_couples - 1)
            )
        dependance_plan_aide_domicile_accepte = compute_dependance_plan_aide_domicile_accepte(
            legislation_autonomie = legislation,
            gir = gir,
            dependance_plan_aide_domicile = dependance_plan_aide_domicile
            )
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
        apa_domicile_participation = select(condition_ressources_domicile, taux_participation) * dependance_plan_aide_domicile_accepte
        return period, apa_domicile_participation

    @dated_function(start = date(2016, 3, 1))
    def function_20160301(individu, period, legislation):
        # Les départements doivent appliquer la nouvelle formule
        # entre le 1er mars 2016 et le 28 février 2017
        base_ressources_apa = individu('base_ressources_apa', period)
        en_couple = individu.famille('en_couple', period)
        dependance_plan_aide_domicile = individu('dependance_plan_aide_domicile', period)
        dependance_plan_aide_domicile_accepte = compute_dependance_plan_aide_domicile_accepte(
            legislation_autonomie = legislation,
            gir = gir,
            dependance_plan_aide_domicile = dependance_plan_aide_domicile
            )
        legislation = legislation(period.start).autonomie
        majoration_tierce_personne = legislation.mtp.mtp
        proratisation_couple = (
            1 +
            en_couple * (legislation.apa_domicile.divison_des_ressources_du_menage_pour_les_couples - 1)
            )
        base_ressources_apa_domicile = base_ressources_apa / proratisation_couple
        # TODO: use a marignal tax scale
        condlist = [
            dependance_plan_aide_domicile_accepte <= (0.317 * majoration_tierce_personne),
            (0.317 * majoration_tierce_personne) <= dependance_plan_aide_domicile_accepte <= (0.498 * majoration_tierce_personne),
            dependance_plan_aide_domicile_accepte >= (0.498 * majoration_tierce_personne),
            ]
        choicelist_1 = [
            dependance_plan_aide_domicile_accepte,
            0.317 * majoration_tierce_personne,
            0.317 * majoration_tierce_personne,
            ]
        choicelist_2 = [
            0,
            dependance_plan_aide_domicile_accepte - 0.317 * majoration_tierce_personne,
            0.498 * majoration_tierce_personne,
            ]
        choicelist_3 = [
            0,
            0,
            dependance_plan_aide_domicile_accepte - 0.815 * majoration_tierce_personne
            ]
        A_1 = select(condlist, choicelist_1)
        A_2 = select(condlist, choicelist_2)
        A_3 = select(condlist, choicelist_3)

        apa_domicile_participation = (
            0.9 *
            (base_ressources_apa_domicile - 0.725 * majoration_tierce_personne) / (1.945 * majoration_tierce_personne) *
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

        return period, apa_domicile_participation


class apa_domicile(Variable):
    column = FloatCol
    label = u"Allocation personalisée d'autonomie"
    entity = Individu

    def function(individu, period, legislation):
        period = period.start.offset('first-of', 'month').period('month')
        legislation = legislation(period.start).autonomie
        age = individu('age', period)
        apa_age_min = legislation.age_ouverture_des_droits.age_d_ouverture_des_droits
        dependance_plan_aide_domicile = individu('dependance_plan_aide_domicile', period)
        gir = individu('gir', period)
        dependance_plan_aide_domicile_accepte = compute_dependance_plan_aide_domicile_accepte(
            legislation_autonomie = legislation,
            gir = gir,
            dependance_plan_aide_domicile = dependance_plan_aide_domicile
            )

        apa_domicile_participation = individu('apa_domicile_participation', period)

        apa = dependance_plan_aide_domicile_accepte - apa_domicile_participation
        return period, apa * (apa >= seuil_non_versement) * (age >= apa_age_min)


class apa_etablissement(Variable):
    column = FloatCol
    label = u"Allocation personalisée d'autonomie en institution"
    entity = Individu

    def function(individu, period, legislation):
        period = period.start.offset('first-of', 'month').period('month')
        legislation = legislation(period.start).autonomie
        en_couple = individu.famille('en_couple', period)
        age = individu('age', period)
        apa_age_min = legislation.age_ouverture_des_droits.age_d_ouverture_des_droits
        gir = individu('gir', period)
        base_ressources_apa = individu('base_ressources_apa', period)
        proratisation_couple_etablissement = (
            1 +
            en_couple * (legislation.apa_institution.divison_des_ressources_du_menage_pour_les_couples - 1)
            )
        base_ressources_apa_etablissement = base_ressources_apa / proratisation_couple_etablissement
        dependance_tarif_etablissement_gir_5_6 = individu('dependance_tarif_etablissement_gir_5_6', period)
        dependance_tarif_etablissement_gir_dependant = individu('dependance_tarif_etablissement_gir_dependant', period)
        seuil_inf_inst = legislation.apa_institution.seuil_de_revenu_en_part_du_mtp.seuil_inferieur
        seuil_sup_inst = legislation.apa_institution.seuil_de_revenu_en_part_du_mtp.seuil_superieur
        majoration_tierce_personne = legislation.mtp.mtp

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
        participation_beneficiaire = min_(
            participation_beneficiaire,
            max_(base_ressources_apa_etablissement * (1 - taux_reste_a_vivre), 0)
            )
        apa = dependance_tarif_etablissement_gir_dependant - participation_beneficiaire

        eligibilite_etablissement = (
            (dependance_tarif_etablissement_gir_5_6 > 0) * (dependance_tarif_etablissement_gir_dependant > 0)
            )  # permet de sélectionner les individus vivant en établissement éligible.
        eligibilite_gir = (0 < gir) & (gir <= 4)
        return period, (
            apa * (apa >= seuil_non_versement) * eligibilite_etablissement * (age >= apa_age_min) * eligibilite_gir
            )


class gir(Variable):
    column = EnumCol(
        enum = Enum(
            [
                u"Non défini",
                u"Gir 1",
                u"Gir 2",
                u"Gir 3",
                u"Gir 4",
                u"Gir 5",
                u"Gir 6",
                ],
            ),
        default = 0,
        )
    entity = Individu
    label = u"Groupe iso-ressources de l'individu"


class dependance_plan_aide_domicile(Variable):
    column = FloatCol
    entity = Individu
    label = u"Plan d'aide à domicile pour une personne dépendate"


class dependance_tarif_etablissement_gir_5_6(Variable):
    column = FloatCol
    entity = Individu
    label = u"Tarif dépendance de l'établissement pour les GIR 5 et 6"


class dependance_tarif_etablissement_gir_dependant(Variable):
    column = FloatCol
    entity = Individu
    label = u"Tarif dépendance de l'établissement pour le GIR de la personne dépendante"


class apa_urgence_domicile(Variable):
    column = FloatCol
    label = u"Allocation personalisée d'autonomie en institution"
    entity = Individu

    def function(individu, period, legislation):
        period = period.this_month
        legislation = legislation(period.start).autonomie
        majoration_tierce_personne = autonomie.mtp.mtp
        plafond_gir1 = legislation.apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_1
        part_urgence_domicile = legislation.apa_domicile.apa_d_urgence.part_du_plafond_de_l_apa_a_domicile
        apa_urgence_domicile = part_urgence_domicile * plafond_gir1 * majoration_tierce_personne

        return period, apa_urgence_domicile


class apa_urgence_institution(Variable):
    column = FloatCol
    label = u"Allocation personalisée d'autonomie en institution"
    entity = Individu

    def function(individu, period, legislation):
        period = period.start.offset('first-of', 'month').period('month')
        dependance_tarif_etablissement_gir_1_2 = individu('dependance_tarif_etablissement_gir_5_6', period)
        part_urgence_institution = legislation.apa_institution.apa_d_urgence.part_du_tarif_dependance_gir_1_2_de_l_etablissement_d_accueil
        apa_urgence_institution = part_urgence_institution * dependance_tarif_etablissement_gir_1_2
        return period, apa_urgence_institution


# Helpers

def compute_dependance_plan_aide_domicile_accepte(legislation_autonomie = None, gir = None,
            dependance_plan_aide_domicile = None):
        assert isinstance(gir, np.ndarray)
        assert isinstance(dependance_plan_aide_domicile, np.ndarray)
        plafond_gir1 = legislation_autonomie.apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_1
        plafond_gir2 = legislation_autonomie.apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_2
        plafond_gir3 = legislation_autonomie.apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_3
        plafond_gir4 = legislation_autonomie.apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_4
        majoration_tierce_personne = legislation_autonomie.mtp.mtp

        condition_plafond_par_gir = [
            gir == 1,
            gir == 2,
            gir == 3,
            gir == 4,
            ]
        valeur_plafond_par_gir = [
            plafond_gir1 * majoration_tierce_personne,
            plafond_gir2 * majoration_tierce_personne,
            plafond_gir3 * majoration_tierce_personne,
            plafond_gir4 * majoration_tierce_personne,
            ]
        plafond_par_gir = select(condition_plafond_par_gir, valeur_plafond_par_gir)
        return min_(plafond_par_gir, dependance_plan_aide_domicile)