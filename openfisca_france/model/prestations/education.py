# -*- coding: utf-8 -*-

from __future__ import division

from numpy import logical_not as not_, logical_or as or_, round as round_

from ..base import *  # noqa analysis:ignore


SCOLARITE_INCONNUE = 0
SCOLARITE_COLLEGE = 1
SCOLARITE_LYCEE = 2


class bourse_college(Variable):
    column = FloatCol
    label = u"Montant mensuel de la bourse de collège"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        rfr = simulation.calculate('rfr', period.n_2)
        age_holder = simulation.compute('age', period)
        scolarite_holder = simulation.compute('scolarite', period)
        P = simulation.legislation_at(period.start).bourses_education.bourse_college

        ages = self.split_by_roles(age_holder, roles = ENFS)
        nb_enfants = sum(
            age >= 0 for age in ages.itervalues()
        )

        scolarites = self.split_by_roles(scolarite_holder, roles = ENFS)

        nb_enfants_college = sum(
            scolarite == SCOLARITE_COLLEGE for scolarite in scolarites.itervalues()
        )

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

        return period, montant / 12


class bourse_lycee_points_de_charge(Variable):
    column = FloatCol
    label = u"Nombre de points de charge pour la bourse de lycée"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        age_holder = simulation.compute('age', period)
        isole = not_(simulation.calculate('en_couple', period))

        # compte le nombre d'enfants
        ages = self.split_by_roles(age_holder, roles = ENFS)
        nb_enfants = sum(
            age >= 0 for age in ages.itervalues()
        )

        points_de_charge = 11 * (nb_enfants >= 1)
        points_de_charge += 1 * (nb_enfants >= 2) # 1 point de charge pour le 2ème enfant
        points_de_charge += 2 * (nb_enfants >= 3) + 2 * (nb_enfants >= 4) # 2 points de charge pour les 3ème et 4ème enfants
        points_de_charge += 3 * (nb_enfants >= 5) * (nb_enfants - 4) # 3 points de charge pour chaque enfant au-dessus de 4 enfants
        points_de_charge += 3 * isole # 3 points de charge en plus si parent isolé

        return period, points_de_charge


class bourse_lycee_nombre_parts(Variable):
    column = FloatCol
    label = u"Nombre de parts pour le calcul du montant de la bourse de lycée"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        points_de_charge = simulation.calculate('bourse_lycee_points_de_charge', period)
        rfr = simulation.calculate('rfr', period.n_2)
        plafonds_reference = simulation.legislation_at(period.start).bourses_education.bourse_lycee.plafonds_reference
        increments_par_point_de_charge = simulation.legislation_at(period.start).bourses_education.bourse_lycee.increments_par_point_de_charge

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

        return period, nombre_parts


class bourse_lycee(Variable):
    column = FloatCol
    label = u"Montant mensuel de la bourse de lycée"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        nombre_parts = simulation.calculate('bourse_lycee_nombre_parts', period)
        scolarite_holder = simulation.compute('scolarite', period)
        valeur_part = simulation.legislation_at(period.start).bourses_education.bourse_lycee.valeur_part

        scolarites = self.split_by_roles(scolarite_holder, roles = ENFS)

        nb_enfants_lycee = sum(
            scolarite == SCOLARITE_LYCEE for scolarite in scolarites.itervalues()
        )

        montant = nombre_parts * valeur_part * nb_enfants_lycee

        return period, montant / 12


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
    entity_class = Individus
    label = u"Scolarité de l'enfant : collège, lycée..."

class boursier(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Élève ou étudiant boursier"
