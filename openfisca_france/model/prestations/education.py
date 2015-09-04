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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import zeros, logical_not as not_, logical_or as or_

from ..base import *  # noqa analysis:ignore


SCOLARITE_INCONNUE = 0
SCOLARITE_COLLEGE = 1
SCOLARITE_LYCEE = 2


@reference_formula
class bourse_college(SimpleFormulaColumn):
    column = FloatCol
    label = u"Montant mensuel de la bourse de collège"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        rfr = simulation.calculate('rfr', period.start.offset('first-of', 'year').period('year').offset(-2))
        age_holder = simulation.compute('age', period)
        scolarite_holder = simulation.compute('scolarite', period)
        P = simulation.legislation_at(period.start).bourses_education.bourse_college

        ages = self.split_by_roles(age_holder, roles = ENFS)
        nb_enfants = zeros(len(rfr))
        for age in ages.itervalues():
            nb_enfants += age >= 0

        plafond_taux_1 = P.plafond_taux_1 + P.plafond_taux_1 * nb_enfants * P.coeff_enfant_supplementaire
        plafond_taux_2 = P.plafond_taux_2 + P.plafond_taux_2 * nb_enfants * P.coeff_enfant_supplementaire
        plafond_taux_3 = P.plafond_taux_3 + P.plafond_taux_3 * nb_enfants * P.coeff_enfant_supplementaire

        eligible_taux_3 = rfr < plafond_taux_3
        eligible_taux_2 = not_(eligible_taux_3) * (rfr < plafond_taux_2)
        eligible_taux_1 = not_(or_(eligible_taux_2, eligible_taux_3)) * (rfr < plafond_taux_1)

        scolarites = self.split_by_roles(scolarite_holder, roles = ENFS)
        nb_enfants_college = zeros(len(rfr))
        for scolarite in scolarites.itervalues():
            nb_enfants_college += scolarite == SCOLARITE_COLLEGE

        montant = nb_enfants_college * (
            eligible_taux_3 * P.montant_taux_3 +
            eligible_taux_2 * P.montant_taux_2 +
            eligible_taux_1 * P.montant_taux_1
            )

        return period, montant / 12


@reference_formula
class bourse_lycee_points_de_charge(SimpleFormulaColumn):
    column = FloatCol
    label = u"Nombre de points de charge pour la bourse de lycée"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age_holder = simulation.compute('age', period)
        isol = simulation.calculate('isol', period)

        # compte le nombre d'enfants
        ages = self.split_by_roles(age_holder, roles = ENFS)
        nb_enfants = zeros(len(isol))
        for age in ages.itervalues():
            nb_enfants += age >= 0

        points_de_charge = 11 * (nb_enfants >= 1)
        points_de_charge += 1 * (nb_enfants >= 2) # 1 point de charge pour le 2ème enfant
        points_de_charge += 2 * (nb_enfants >= 3) + 2 * (nb_enfants >= 4) # 2 points de charge pour les 3ème et 4ème enfants
        points_de_charge += 3 * (nb_enfants >= 5) * (nb_enfants - 4) # 3 points de charge pour chaque enfant au-dessus de 4 enfants
        points_de_charge += 3 * isol # 3 points de charge en plus si parent isolé

        return period, points_de_charge


@reference_formula
class bourse_lycee_nombre_parts(SimpleFormulaColumn):
    column = FloatCol
    label = u"Nombre de parts pour le calcul du montant de la bourse de lycée"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        points_de_charge = simulation.calculate('bourse_lycee_points_de_charge', period)
        rfr = simulation.calculate('rfr', period.start.offset('first-of', 'year').period('year').offset(-2))
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

        nombre_parts = zeros(len(rfr))
        nombre_parts = ((rfr <= plafond_10_parts) * 10
            + (rfr > plafond_10_parts) * (rfr <= plafond_9_parts) * 9
            + (rfr > plafond_9_parts) * (rfr <= plafond_8_parts) * 8
            + (rfr > plafond_8_parts) * (rfr <= plafond_7_parts) * 7
            + (rfr > plafond_7_parts) * (rfr <= plafond_6_parts) * 6
            + (rfr > plafond_6_parts) * (rfr <= plafond_5_parts) * 5
            + (rfr > plafond_5_parts) * (rfr <= plafond_4_parts) * 4
            + (rfr > plafond_4_parts) * (rfr <= plafond_3_parts) * 3)

        return period, nombre_parts


@reference_formula
class bourse_lycee(SimpleFormulaColumn):
    column = FloatCol
    label = u"Montant mensuel de la bourse de lycée"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        nombre_parts = simulation.calculate('bourse_lycee_nombre_parts', period)
        scolarite_holder = simulation.compute('scolarite', period)
        valeur_part = simulation.legislation_at(period.start).bourses_education.bourse_lycee.valeur_part

        scolarites = self.split_by_roles(scolarite_holder, roles = ENFS)
        nb_enfants_lycee = zeros(len(nombre_parts))
        for scolarite in scolarites.itervalues():
            nb_enfants_lycee += scolarite == SCOLARITE_LYCEE

        montant = nombre_parts * valeur_part * nb_enfants_lycee

        return period, montant / 12


reference_input_variable(
    column = EnumCol(
        enum = Enum(
            [
                u"Inconnue",
                u"Collège",
                u"Lycée"
                ],
            ),
        default = 0
        ),
    entity_class = Individus,
    label = u"Scolarité de l'enfant : collège, lycée...",
    name = "scolarite",
    )


reference_input_variable(
    column = BoolCol,
    entity_class = Individus,
    label = u"Élève ou étudiant boursier",
    name = 'boursier',
    )
