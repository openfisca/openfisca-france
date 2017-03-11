# -*- coding: utf-8 -*-

from __future__ import division

from numpy import logical_not as not_, logical_or as or_, round as round_

from openfisca_france.model.base import *  # noqa analysis:ignore


SCOLARITE_INCONNUE = 0
SCOLARITE_COLLEGE = 1
SCOLARITE_LYCEE = 2


class bourse_college(Variable):
    column = FloatCol
    label = u"Montant annuel de la bourse de collège"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def function(famille, period, legislation):
        rfr = famille.demandeur.foyer_fiscal('rfr', period.n_2)
        P = legislation(period).bourses_education.bourse_college

        age_i = famille.members('age', period)
        nb_enfants = famille.sum(age_i >= 0, role = Famille.ENFANT)

        scolarite_i = famille.members('scolarite', period)
        nb_enfants_college = famille.sum(scolarite_i == SCOLARITE_COLLEGE, role = Famille.ENFANT)

        montant_par_enfant = apply_thresholds(
            rfr,
            thresholds = [
                # plafond_taux_3 est le plus bas
                round_(P.plafond_taux_3 + P.plafond_taux_3 * nb_enfants * P.coeff_enfant_supplementaire),
                round_(P.plafond_taux_2 + P.plafond_taux_2 * nb_enfants * P.coeff_enfant_supplementaire),
                round_(P.plafond_taux_1 + P.plafond_taux_1 * nb_enfants * P.coeff_enfant_supplementaire),
                ],
            choices = [P.montant_taux_3, P.montant_taux_2, P.montant_taux_1]
            )

        montant = nb_enfants_college * montant_par_enfant

        return montant


class bourse_lycee_points_de_charge(Variable):
    column = FloatCol
    label = u"Nombre de points de charge pour la bourse de lycée"
    entity = Famille
    definition_period = MONTH

    def function(famille, period, legislation):
        isole = not_(famille('en_couple', period))
        age_i = famille.members('age', period)
        nb_enfants = famille.sum(age_i >= 0, role = Famille.ENFANT)

        points_de_charge = 11 * (nb_enfants >= 1)
        points_de_charge += 1 * (nb_enfants >= 2) # 1 point de charge pour le 2ème enfant
        points_de_charge += 2 * (nb_enfants >= 3) + 2 * (nb_enfants >= 4) # 2 points de charge pour les 3ème et 4ème enfants
        points_de_charge += 3 * (nb_enfants >= 5) * (nb_enfants - 4) # 3 points de charge pour chaque enfant au-dessus de 4 enfants
        points_de_charge += 3 * isole # 3 points de charge en plus si parent isolé

        return points_de_charge


class bourse_lycee_nombre_parts(Variable):
    column = FloatCol
    label = u"Nombre de parts pour le calcul du montant de la bourse de lycée"
    entity = Famille
    definition_period = MONTH

    def function(famille, period, legislation):
        points_de_charge = famille('bourse_lycee_points_de_charge', period)
        rfr = famille.demandeur.foyer_fiscal('rfr', period.n_2)
        plafonds_reference = legislation(period).bourses_education.bourse_lycee.plafonds_reference
        increments_par_point_de_charge = legislation(period).bourses_education.bourse_lycee.increments_par_point_de_charge

        choices = [10, 9, 8, 7, 6, 5, 4, 3]
        nombre_parts = apply_thresholds(
            rfr,
            thresholds = [
                round(
                    plafonds_reference['{}_parts'.format(index)] +
                    ((points_de_charge - 9) * increments_par_point_de_charge['{}_parts'.format(index)])
                    )
                for index in choices
                ],
            choices = choices,
            )

        return nombre_parts


class bourse_lycee(Variable):
    column = FloatCol
    label = u"Montant annuel de la bourse de lycée"
    entity = Famille
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def function(famille, period, legislation):
        nombre_parts = famille('bourse_lycee_nombre_parts', period)
        valeur_part = legislation(period).bourses_education.bourse_lycee.valeur_part

        scolarite_i = famille.members('scolarite', period)
        nb_enfants_lycee = famille.sum(scolarite_i == SCOLARITE_LYCEE, role = Famille.ENFANT)

        montant = nombre_parts * valeur_part * nb_enfants_lycee

        return montant


class scolarite(Variable):
    column = EnumCol(
        enum = Enum(
            [
                u"Inconnue",
                u"Collège",
                u"Lycée"
                ],
            ),
        default = 0
        )
    entity = Individu
    label = u"Scolarité de l'enfant : collège, lycée..."
    definition_period = MONTH
