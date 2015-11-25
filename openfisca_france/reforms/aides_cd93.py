# -*- coding: utf-8 -*-

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
            period = period.this_month
            depcom = simulation.calculate('depcom', period)

            def is_resident_93(code_insee):
                prefix = code_insee[0:2]
                result = (prefix == "93")
                return result

            is_resident_93_vec = vectorize(is_resident_93)

            result = is_resident_93_vec(depcom)

            return period, result


    @Reform.formula
    class adpa_eligibilite(SimpleFormulaColumn):
        column = BoolCol
        label = u"Eligibilité à l'ADPA"
        entity_class = Individus

        def function(self, simulation, period):
            period = period.this_month
            age = simulation.calculate('age', period)
            resident_93 = simulation.calculate('resident_93', period)
            perte_autonomie = simulation.calculate('perte_autonomie', period)

            result = (age > 60) * resident_93 * perte_autonomie

            return period, result


    @Reform.formula
    class adpa_base_ressources_i(SimpleFormulaColumn):
        column = FloatCol
        label = u"Base ressources ADPA pour un individu"
        entity_class = Individus

        def function(self, simulation, period):
            period = period.this_month
            previous_year = period.start.period('year').offset(-1)
            salaire_imposable = simulation.calculate_add('salaire_imposable', period.n_2)
            rst = simulation.calculate_add('rst', period.n_2)
            cho = simulation.calculate_add('cho', period.n_2)
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
    class adpa_base_ressources(SimpleFormulaColumn):
        column = FloatCol
        label = u"Base ressources ADPA pour une famille"
        entity_class = Familles

        def function(self, simulation, period):
            period = period.this_month
            adpa_base_ressources_i = simulation.compute('adpa_base_ressources_i', period)
            adpa_base_ressources = self.sum_by_entity(adpa_base_ressources_i)

            return period, adpa_base_ressources


    @Reform.formula
    class adpa(SimpleFormulaColumn):
        column = FloatCol
        label = u"ADPA"
        entity_class = Familles

        def function(self, simulation, period):
            period = period.this_month

            adpa_eligibilite_holder = simulation.compute('adpa_eligibilite', period)
            adpa_eligibilite = self.any_by_roles(adpa_eligibilite_holder)
            base_ressource_mensuelle = simulation.calculate('adpa_base_ressources', period)
            concub = simulation.calculate('concub', period)
            
            # On ne prend pas en compte le cas où le conjoint est placé.
            quotient_familial = 1 + 0.7 * concub
            base_ressource_mensuelle = base_ressource_mensuelle / quotient_familial

            majorationTiercePersonne = 1103.08
            seuil1 = 0.67 * majorationTiercePersonne
            seuil2 = 2.67 * majorationTiercePersonne

            participation_usager = (
                (base_ressource_mensuelle < seuil1) * 0 +
                (base_ressource_mensuelle >= seuil1) * (base_ressource_mensuelle <= seuil2) *
                     90 * (base_ressource_mensuelle - seuil1) / (2 * majorationTiercePersonne) +
                (base_ressource_mensuelle > seuil2) * 90
            )

            participation_departement = 100 - participation_usager

            return period, participation_departement * adpa_eligibilite

    reform = Reform()
    return reform
