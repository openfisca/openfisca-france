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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from openfisca_core import columns, formulas, reforms
from numpy import vectorize, maximum as max_, logical_not as not_, logical_or as or_, absolute as abs_

from ..model.base import *

def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'aides_cd93',
        name = u'Aides du conseil départemental du 93',
        reference = tax_benefit_system,
        )

    Reform.input_variable(
        name = "perte_autonomie",
        column = BoolCol,
        entity_class = Individus,
        label = u"Personne en perte d'autonomie"
    )


    @Reform.formula
    class resident_93(SimpleFormulaColumn):
        column = BoolCol
        label = u"Résident en Seine-Saint-Denis"
        entity_class = Menages

        def function(self, simulation, period):
            depcom = simulation.calculate('depcom', period)

            def is_resident_93(code_insee):
                prefix = code_insee[0:2]
                result = (prefix == "93")
                return result

            is_resident_93_vec = vectorize(is_resident_93)

            result = is_resident_93_vec(depcom)

            return period, result


    @Reform.formula
    class adpa_elig(SimpleFormulaColumn):
        column = BoolCol
        label = u"Eligibilité à l'ADPA"
        entity_class = Individus

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('month')
            age = simulation.calculate('age', period)
            resident_93 = simulation.calculate('resident_93', period)
            perte_autonomie = simulation.calculate('perte_autonomie', period)
            print(perte_autonomie)

            result = (age > 60) * resident_93 * perte_autonomie

            return period, result


    @Reform.formula
    class base_ressources_adpa_i(SimpleFormulaColumn):
        column = FloatCol
        label = u"Base ressources ADPA pour un individu"
        entity_class = Individus

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('month')
            previous_year = period.start.period('year').offset(-1)
            two_years_ago = period.start.offset('first-of', 'year').period('year').offset(-2)
            salaire_imposable = simulation.calculate_add('salaire_imposable', two_years_ago)
            rst = simulation.calculate_add('rst', two_years_ago)
            cho = simulation.calculate_add('cho', two_years_ago)
            revenus_capital = simulation.calculate_add('revenus_capital', previous_year)
            revenus_locatifs = simulation.calculate_add('revenus_locatifs', previous_year)
            # Prélevements libératoire forfaitaire à prendre en compte sans abattement
            valeur_locative_immo_non_loue = simulation.calculate_add('valeur_locative_immo_non_loue', previous_year)
            valeur_locative_terrains_non_loue = simulation.calculate_add('valeur_locative_terrains_non_loue', previous_year)

            base_ressource_mensuelle = (
                salaire_imposable + rst + cho + revenus_locatifs +
                revenus_capital * 0.30 +
                valeur_locative_immo_non_loue * 0.5 +
                valeur_locative_terrains_non_loue * 0.8
            ) / 12

            return period, base_ressource_mensuelle


    @Reform.formula
    class base_ressources_adpa(SimpleFormulaColumn):
        column = FloatCol
        label = u"Base ressources ADPA pour une famille"
        entity_class = Familles

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('month')
            base_ressources_adpa_i = simulation.compute('base_ressources_adpa_i', period)
            base_ressources_adpa = self.sum_by_entity(base_ressources_adpa_i)

            return period, base_ressources_adpa


    @Reform.formula
    class adpa(SimpleFormulaColumn):
        column = FloatCol
        label = u"ADPA"
        entity_class = Familles

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('month')

            adpa_elig_holder = simulation.compute('adpa_elig', period)
            adpa_elig = self.any_by_roles(adpa_elig_holder)

            base_ressource_mensuelle = simulation.calculate('base_ressources_adpa', period)
            concub = simulation.calculate('concub', period)
            
            # On ne prend pas en compte le cas où le conjoint est placé.
            quotient_familial = 1 + 0.7 * concub
            base_ressource_mensuelle = base_ressource_mensuelle / quotient_familial

            # print("base_ressource_mensuelle")
            # print(base_ressource_mensuelle)

            majorationTiercePersonne = 1103.08
            seuil1 = 0.67 * majorationTiercePersonne
            seuil2 = 2.67 * majorationTiercePersonne


            # print((base_ressource_mensuelle < seuil1) * 0)
            # print((base_ressource_mensuelle >= seuil1) * (base_ressource_mensuelle <= seuil2) *
                     # 90 * (base_ressource_mensuelle - seuil1) / (2 * majorationTiercePersonne) )
            # print((base_ressource_mensuelle > seuil2) * 90)

            participation_usager = (
                (base_ressource_mensuelle < seuil1) * 0 +
                (base_ressource_mensuelle >= seuil1) * (base_ressource_mensuelle <= seuil2) *
                     90 * (base_ressource_mensuelle - seuil1) / (2 * majorationTiercePersonne) +
                (base_ressource_mensuelle > seuil2) * 90
            )

            participation_departement = 100 - participation_usager

            return period, participation_departement * adpa_elig

    reform = Reform()
    return reform
