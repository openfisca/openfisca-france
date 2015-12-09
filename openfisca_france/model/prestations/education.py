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

        plafond_taux_1 = round_(P.plafond_taux_1 + P.plafond_taux_1 * nb_enfants * P.coeff_enfant_supplementaire)
        plafond_taux_2 = round_(P.plafond_taux_2 + P.plafond_taux_2 * nb_enfants * P.coeff_enfant_supplementaire)
        plafond_taux_3 = round_(P.plafond_taux_3 + P.plafond_taux_3 * nb_enfants * P.coeff_enfant_supplementaire)

        eligible_taux_3 = rfr <= plafond_taux_3
        eligible_taux_2 = not_(eligible_taux_3) * (rfr <= plafond_taux_2)
        eligible_taux_1 = not_(or_(eligible_taux_2, eligible_taux_3)) * (rfr <= plafond_taux_1)

        scolarites = self.split_by_roles(scolarite_holder, roles = ENFS)

        nb_enfants_college = sum(
            scolarite == SCOLARITE_COLLEGE for scolarite in scolarites.itervalues()
        )

        montant = nb_enfants_college * (
            eligible_taux_3 * P.montant_taux_3 +
            eligible_taux_2 * P.montant_taux_2 +
            eligible_taux_1 * P.montant_taux_1
            )

        return period, montant / 12


class bourse_lycee_points_de_charge(Variable):
    column = FloatCol
    label = u"Nombre de points de charge pour la bourse de lycée"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        age_holder = simulation.compute('age', period)
        isol = simulation.calculate('isol', period)

        # compte le nombre d'enfants
        ages = self.split_by_roles(age_holder, roles = ENFS)
        nb_enfants = sum(
            age >= 0 for age in ages.itervalues()
        )

        points_de_charge = 11 * (nb_enfants >= 1)
        points_de_charge += 1 * (nb_enfants >= 2) # 1 point de charge pour le 2ème enfant
        points_de_charge += 2 * (nb_enfants >= 3) + 2 * (nb_enfants >= 4) # 2 points de charge pour les 3ème et 4ème enfants
        points_de_charge += 3 * (nb_enfants >= 5) * (nb_enfants - 4) # 3 points de charge pour chaque enfant au-dessus de 4 enfants
        points_de_charge += 3 * isol # 3 points de charge en plus si parent isolé

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

        plafond_10_parts = round(plafonds_reference['10_parts'] + ((points_de_charge - 9) * increments_par_point_de_charge['10_parts']))
        plafond_9_parts = round(plafonds_reference['9_parts'] + ((points_de_charge - 9) * increments_par_point_de_charge['9_parts']))
        plafond_8_parts = round(plafonds_reference['8_parts'] + ((points_de_charge - 9) * increments_par_point_de_charge['8_parts']))
        plafond_7_parts = round(plafonds_reference['7_parts'] + ((points_de_charge - 9) * increments_par_point_de_charge['7_parts']))
        plafond_6_parts = round(plafonds_reference['6_parts'] + ((points_de_charge - 9) * increments_par_point_de_charge['6_parts']))
        plafond_5_parts = round(plafonds_reference['5_parts'] + ((points_de_charge - 9) * increments_par_point_de_charge['5_parts']))
        plafond_4_parts = round(plafonds_reference['4_parts'] + ((points_de_charge - 9) * increments_par_point_de_charge['4_parts']))
        plafond_3_parts = round(plafonds_reference['3_parts'] + ((points_de_charge - 9) * increments_par_point_de_charge['3_parts']))

        nombre_parts = (
            (rfr <= plafond_10_parts) * 10 +
            (rfr > plafond_10_parts) * (rfr <= plafond_9_parts) * 9 +
            (rfr > plafond_9_parts) * (rfr <= plafond_8_parts) * 8 +
            (rfr > plafond_8_parts) * (rfr <= plafond_7_parts) * 7 +
            (rfr > plafond_7_parts) * (rfr <= plafond_6_parts) * 6 +
            (rfr > plafond_6_parts) * (rfr <= plafond_5_parts) * 5 +
            (rfr > plafond_5_parts) * (rfr <= plafond_4_parts) * 4 +
            (rfr > plafond_4_parts) * (rfr <= plafond_3_parts) * 3
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
