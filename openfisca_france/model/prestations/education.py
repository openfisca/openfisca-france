# -*- coding: utf-8 -*-

from __future__ import division

from numpy import logical_or as or_

from openfisca_france.model.base import *  # noqa analysis:ignore


class bourse_college_echelon(Variable):
    value_type = int
    label = u"Échelon de la bourse de collège attribuée"
    entity = Famille
    definition_period = MONTH

    def formula_2016_07_01(famille, period, parameters):
        """
        Références législatives :
        Arrêté du 22 mars 2016 fixant les plafonds de ressources...
        https://www.legifrance.gouv.fr/eli/arrete/2016/3/22/MENE1606428A/jo
        """

        rfr = famille.demandeur.foyer_fiscal("rfr", period.n_2)
        age_i = famille.members("age", period)
        nb_enfants = famille.sum(age_i >= 0, role=Famille.ENFANT)
        P = parameters(period).bourses_education.bourse_college.apres_2016

        # Les plafonds sont estimés en multiples du SMIC au 1er juillet de l'année n_2
        juillet_n_2 = period.n_2.first_month.offset(6, MONTH)
        smic_juillet_n_2 = parameters(juillet_n_2).cotsoc.gen.smic_h_b

        P_e3 = P.echelon_3
        plafonds_echelon_3_en_pourcent_smic = select(
            [nb_enfants <= i for i in range(1, 8)],
            [
                P_e3.plafond_1e,
                P_e3.plafond_2e,
                P_e3.plafond_3e,
                P_e3.plafond_4e,
                P_e3.plafond_5e,
                P_e3.plafond_6e,
                P_e3.plafond_7e,
            ],
            P_e3.plafond_8e,
        )
        P_e2 = P.echelon_2
        plafonds_echelon_2_en_pourcent_smic = select(
            [nb_enfants <= i for i in range(1, 8)],
            [
                P_e2.plafond_1e,
                P_e2.plafond_2e,
                P_e2.plafond_3e,
                P_e2.plafond_4e,
                P_e2.plafond_5e,
                P_e2.plafond_6e,
                P_e2.plafond_7e,
            ],
            P_e2.plafond_8e,
        )
        P_e1 = P.echelon_1
        plafonds_echelon_1_en_pourcent_smic = select(
            [nb_enfants <= i for i in range(1, 8)],
            [
                P_e1.plafond_1e,
                P_e1.plafond_2e,
                P_e1.plafond_3e,
                P_e1.plafond_4e,
                P_e1.plafond_5e,
                P_e1.plafond_6e,
                P_e1.plafond_7e,
            ],
            P_e1.plafond_8e,
        )

        plafonds_echelon_3 = round_(
            plafonds_echelon_3_en_pourcent_smic * smic_juillet_n_2
        )
        plafonds_echelon_2 = round_(
            plafonds_echelon_2_en_pourcent_smic * smic_juillet_n_2
        )
        plafonds_echelon_1 = round_(
            plafonds_echelon_1_en_pourcent_smic * smic_juillet_n_2
        )

        return apply_thresholds(
            rfr,
            thresholds=[plafonds_echelon_3, plafonds_echelon_2, plafonds_echelon_1],
            choices=[3, 2, 1],
        )

    def formula(famille, period, parameters):
        rfr = famille.demandeur.foyer_fiscal("rfr", period.n_2)
        age_i = famille.members("age", period)
        nb_enfants = famille.sum(age_i >= 0, role=Famille.ENFANT)

        P = parameters(period).bourses_education.bourse_college.avant_2016

        coefficient_famille = 1 + nb_enfants * P.coeff_enfant_supplementaire

        return apply_thresholds(
            rfr,
            thresholds=[
                # plafond_taux_3 est le plus bas
                round_(P.plafond_taux_3 * coefficient_famille),
                round_(P.plafond_taux_2 * coefficient_famille),
                round_(P.plafond_taux_1 * coefficient_famille),
            ],
            choices=[3, 2, 1],
        )


class bourse_college(Variable):
    value_type = float
    label = u"Montant annuel de la bourse de collège"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(famille, period, parameters):
        """
        Références législatives :
            Article D531-7 du code de l'éducation
            https://www.legifrance.gouv.fr/affichCode.do?idSectionTA=LEGISCTA000020743197&cidTexte=LEGITEXT000006071191&dateTexte=20160610
        """
        P = parameters(period).bourses_education.bourse_college

        # On prends en compte la BMAF du premier janvier de l'année de la rentrée scolaire
        bmaf_1er_janvier = parameters(
            period.this_year.first_month
        ).prestations.prestations_familiales.af.bmaf

        scolarite_i = famille.members("scolarite", period)
        nb_enfants_college = famille.sum(
            scolarite_i == TypesScolarite.college, role=Famille.ENFANT
        )

        echelon = famille("bourse_college_echelon", period)

        montant_par_enfant_en_pourcent_bmaf = select(
            [echelon == 3, echelon == 2, echelon == 1],
            [P.montant_taux_3, P.montant_taux_2, P.montant_taux_1],
        )

        # Arrondi au multiple de 3 le plus proche, car 3 trimestres
        montant_par_enfant = (
            round_(montant_par_enfant_en_pourcent_bmaf * bmaf_1er_janvier / 3) * 3
        )

        return nb_enfants_college * montant_par_enfant


class bourse_lycee_points_de_charge(Variable):
    value_type = float
    label = u"Nombre de points de charge pour la bourse de lycée"
    entity = Famille
    definition_period = MONTH
    end = "2016-07-01"

    def formula(famille, period, parameters):
        isole = not_(famille("en_couple", period))
        age_i = famille.members("age", period)
        nb_enfants = famille.sum(age_i >= 0, role=Famille.ENFANT)

        points_de_charge = (
            11 * (nb_enfants >= 1)
            + 1 * (nb_enfants >= 2)
            + 2 * (nb_enfants >= 3)  # 1 point de charge pour le 2ème enfant
            + 2 * (nb_enfants >= 4)
            + 3  # 2 points de charge pour les 3ème et 4ème enfants
            * (nb_enfants >= 5)
            * (nb_enfants - 4)
            + 3  # 3 points de charge pour chaque enfant au-dessus de 4 enfants
            * isole  # 3 points de charge en plus si parent isolé
        )

        return points_de_charge


class bourse_lycee_nombre_parts(Variable):
    value_type = float
    label = u"Nombre de parts pour le calcul du montant de la bourse de lycée"
    entity = Famille
    definition_period = MONTH
    end = "2016-07-01"

    def formula(famille, period, parameters):
        points_de_charge = famille("bourse_lycee_points_de_charge", period)
        rfr = famille.demandeur.foyer_fiscal("rfr", period.n_2)
        plafonds_reference = parameters(
            period
        ).bourses_education.bourse_lycee.avant_2016.plafonds_reference
        increments_par_point_de_charge = parameters(
            period
        ).bourses_education.bourse_lycee.avant_2016.increments_par_point_de_charge

        choices = [10, 9, 8, 7, 6, 5, 4, 3]
        nombre_parts = apply_thresholds(
            rfr,
            thresholds=[
                round_(
                    plafonds_reference["{}_parts".format(index)]
                    + (
                        (points_de_charge - 9)
                        * increments_par_point_de_charge["{}_parts".format(index)]
                    )
                )
                for index in choices
            ],
            choices=choices,
        )

        return nombre_parts


class bourse_lycee_echelon(Variable):
    value_type = int
    label = u"Échelon de la bourse de collège attribuée"
    entity = Famille
    definition_period = MONTH

    def formula(famille, period, parameters):
        """
        Références législatives :
        Arrêté du 22 mars 2016 fixant les modalités de détermination des plafonds de ressources ouvrant droit...
        https://www.legifrance.gouv.fr/eli/arrete/2016/3/22/MENE1606432A/jo
        """

        rfr = famille.demandeur.foyer_fiscal("rfr", period.n_2)
        age_i = famille.members("age", period)
        nb_enfants = famille.sum(age_i >= 0, role=Famille.ENFANT)
        P = parameters(period).bourses_education.bourse_lycee.apres_2016

        # Les plafonds sont estimés en multiples du SMIC au 1er juillet de l'année n_2
        juillet_n_2 = period.n_2.first_month.offset(6, MONTH)
        smic_juillet_n_2 = parameters(juillet_n_2).cotsoc.gen.smic_h_b

        P_e6 = P.echelon_6
        plafonds_echelon_6_en_pourcent_smic = select(
            [nb_enfants <= i for i in range(1, 8)],
            [
                P_e6.plafond_1e,
                P_e6.plafond_2e,
                P_e6.plafond_3e,
                P_e6.plafond_4e,
                P_e6.plafond_5e,
                P_e6.plafond_6e,
                P_e6.plafond_7e,
            ],
            P_e6.plafond_8e,
        )
        P_e5 = P.echelon_5
        plafonds_echelon_5_en_pourcent_smic = select(
            [nb_enfants <= i for i in range(1, 8)],
            [
                P_e5.plafond_1e,
                P_e5.plafond_2e,
                P_e5.plafond_3e,
                P_e5.plafond_4e,
                P_e5.plafond_5e,
                P_e5.plafond_6e,
                P_e5.plafond_7e,
            ],
            P_e5.plafond_8e,
        )
        P_e4 = P.echelon_4
        plafonds_echelon_4_en_pourcent_smic = select(
            [nb_enfants <= i for i in range(1, 8)],
            [
                P_e4.plafond_1e,
                P_e4.plafond_2e,
                P_e4.plafond_3e,
                P_e4.plafond_4e,
                P_e4.plafond_5e,
                P_e4.plafond_6e,
                P_e4.plafond_7e,
            ],
            P_e4.plafond_8e,
        )
        P_e3 = P.echelon_3
        plafonds_echelon_3_en_pourcent_smic = select(
            [nb_enfants <= i for i in range(1, 8)],
            [
                P_e3.plafond_1e,
                P_e3.plafond_2e,
                P_e3.plafond_3e,
                P_e3.plafond_4e,
                P_e3.plafond_5e,
                P_e3.plafond_6e,
                P_e3.plafond_7e,
            ],
            P_e3.plafond_8e,
        )
        P_e2 = P.echelon_2
        plafonds_echelon_2_en_pourcent_smic = select(
            [nb_enfants <= i for i in range(1, 8)],
            [
                P_e2.plafond_1e,
                P_e2.plafond_2e,
                P_e2.plafond_3e,
                P_e2.plafond_4e,
                P_e2.plafond_5e,
                P_e2.plafond_6e,
                P_e2.plafond_7e,
            ],
            P_e2.plafond_8e,
        )
        P_e1 = P.echelon_1
        plafonds_echelon_1_en_pourcent_smic = select(
            [nb_enfants <= i for i in range(1, 8)],
            [
                P_e1.plafond_1e,
                P_e1.plafond_2e,
                P_e1.plafond_3e,
                P_e1.plafond_4e,
                P_e1.plafond_5e,
                P_e1.plafond_6e,
                P_e1.plafond_7e,
            ],
            P_e1.plafond_8e,
        )

        plafonds_echelon_6 = round_(
            plafonds_echelon_6_en_pourcent_smic * smic_juillet_n_2
        )
        plafonds_echelon_5 = round_(
            plafonds_echelon_5_en_pourcent_smic * smic_juillet_n_2
        )
        plafonds_echelon_4 = round_(
            plafonds_echelon_4_en_pourcent_smic * smic_juillet_n_2
        )
        plafonds_echelon_3 = round_(
            plafonds_echelon_3_en_pourcent_smic * smic_juillet_n_2
        )
        plafonds_echelon_2 = round_(
            plafonds_echelon_2_en_pourcent_smic * smic_juillet_n_2
        )
        plafonds_echelon_1 = round_(
            plafonds_echelon_1_en_pourcent_smic * smic_juillet_n_2
        )

        return apply_thresholds(
            rfr,
            thresholds=[
                plafonds_echelon_6,
                plafonds_echelon_5,
                plafonds_echelon_4,
                plafonds_echelon_3,
                plafonds_echelon_2,
                plafonds_echelon_1,
            ],
            choices=[6, 5, 4, 3, 2, 1],
        )


class bourse_lycee(Variable):
    value_type = float
    label = u"Montant annuel de la bourse de lycée"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2016_07_01(famille, period, parameters):
        """
        Références legislatives :
            Article Article D531-29 du code de l'éducation
            https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006071191&idArticle=LEGIARTI000020663350&dateTexte=&categorieLien=cid
        """
        P = parameters(period).bourses_education.bourse_lycee.apres_2016

        # On prends en compte la BMAF du premier janvier de l'année de la rentrée scolaire
        bmaf_1er_janvier = parameters(
            period.this_year.first_month
        ).prestations.prestations_familiales.af.bmaf

        scolarite_i = famille.members("scolarite", period)
        nb_enfants_lycee = famille.sum(
            scolarite_i == TypesScolarite.lycee, role=Famille.ENFANT
        )

        echelon = famille("bourse_lycee_echelon", period)

        montant_par_enfant_en_pourcent_bmaf = select(
            [
                echelon == 6,
                echelon == 5,
                echelon == 4,
                echelon == 3,
                echelon == 2,
                echelon == 1,
            ],
            [
                P.echelon_6.montant,
                P.echelon_5.montant,
                P.echelon_4.montant,
                P.echelon_3.montant,
                P.echelon_2.montant,
                P.echelon_1.montant,
            ],
        )

        # Arrondi au multiple de 3 le plus proche, car 3 trimestres
        montant_par_enfant = (
            round_(montant_par_enfant_en_pourcent_bmaf * bmaf_1er_janvier / 3) * 3
        )

        return nb_enfants_lycee * montant_par_enfant

    def formula(famille, period, parameters):
        nombre_parts = famille("bourse_lycee_nombre_parts", period)
        valeur_part = parameters(
            period
        ).bourses_education.bourse_lycee.avant_2016.valeur_part

        scolarite_i = famille.members("scolarite", period)
        nb_enfants_lycee = famille.sum(
            scolarite_i == TypesScolarite.lycee, role=Famille.ENFANT
        )

        montant = nombre_parts * valeur_part * nb_enfants_lycee

        return montant


class TypesScolarite(Enum):
    __order__ = (
        "inconnue college lycee"
    )  # Needed to preserve the enum order in Python 2
    inconnue = u"Inconnue"
    college = u"Collège"
    lycee = u"Lycée"


class scolarite(Variable):
    value_type = Enum
    possible_values = TypesScolarite
    default_value = TypesScolarite.inconnue
    entity = Individu
    label = u"Scolarité de l'enfant : collège, lycée..."
    definition_period = MONTH
