# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select)

from ....base import *  # noqa analysis:ignore

class parisien(Variable):
    column = BoolCol
    entity_class = Familles
    label = u"Résidant à Paris au moins 3 ans dans les 5 dernières années"

class a_charge_fiscale(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant à charge fiscale du demandeur"

class enfant_place(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant placé en structure spécialisée ou famille d'accueil"

class paris_logement_familles_br_i(Variable):
        column = FloatCol
        label = u"Base de ressources individuelle pour Paris Logement Famille"
        entity_class = Individus

        def function(self, simulation, period):
            period = period.this_month
            last_year = period.last_year
            salaire_net = simulation.calculate('salaire_net', period)
            chonet = simulation.calculate('chonet', period)
            rstnet = simulation.calculate('rstnet', period)
            pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', period)
            pensions_alimentaires_versees_individu = simulation.calculate(
                'pensions_alimentaires_versees_individu', period)
            rsa_base_ressources_patrimoine_i = simulation.calculate_add('rsa_base_ressources_patrimoine_i', period)
            indemnites_journalieres_imposables = simulation.calculate('indemnites_journalieres_imposables', period)
            indemnites_stage = simulation.calculate('indemnites_stage', period)
            revenus_stage_formation_pro = simulation.calculate('revenus_stage_formation_pro', period)
            allocation_securisation_professionnelle = simulation.calculate(
                'allocation_securisation_professionnelle', period)
            prestation_compensatoire = simulation.calculate('prestation_compensatoire', period)
            pensions_invalidite = simulation.calculate('pensions_invalidite', period)
            indemnites_chomage_partiel = simulation.calculate('indemnites_chomage_partiel', period)
            bourse_recherche = simulation.calculate('bourse_recherche', period)
            gains_exceptionnels = simulation.calculate('gains_exceptionnels', period)

            def revenus_tns():
                revenus_auto_entrepreneur = simulation.calculate_add('tns_auto_entrepreneur_benefice', period)

                # Les revenus TNS hors AE sont estimés en se basant sur le revenu N-1
                tns_micro_entreprise_benefice = simulation.calculate('tns_micro_entreprise_benefice', last_year) / 12
                tns_benefice_exploitant_agricole = simulation.calculate('tns_benefice_exploitant_agricole', last_year) / 12
                tns_autres_revenus = simulation.calculate('tns_autres_revenus', last_year) / 12

                return revenus_auto_entrepreneur + tns_micro_entreprise_benefice + tns_benefice_exploitant_agricole + tns_autres_revenus

            result = (
                salaire_net + indemnites_chomage_partiel + indemnites_stage + chonet + rstnet +
                pensions_alimentaires_percues - abs_(pensions_alimentaires_versees_individu) +
                rsa_base_ressources_patrimoine_i + allocation_securisation_professionnelle +
                indemnites_journalieres_imposables + prestation_compensatoire +
                pensions_invalidite + bourse_recherche + gains_exceptionnels + revenus_tns() +
                revenus_stage_formation_pro
                )

            return period, result

class paris_logement_familles_br(Variable):
    column = FloatCol
    label = u"Base de ressource pour Paris Logement Famille"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        paris_logement_familles_br_i_holder = simulation.compute('paris_logement_familles_br_i', period)
        paris_logement_familles_br = self.sum_by_entity(paris_logement_familles_br_i_holder)
        result = paris_logement_familles_br

        return period, result

class plf_enfant_handicape(Variable):
    column = BoolCol
    label = u"Enfant handicapé au sens de la mairie de Paris"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month

        invalide = simulation.calculate('invalide', period)
        plf_enfant = simulation.calculate('plf_enfant', period)

        return period, plf_enfant * invalide

class plf_enfant(Variable):
    column = BoolCol
    label = u"Enfant pris en compte par la mairie de Paris pour PLF"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        est_enfant_dans_famille = simulation.calculate('est_enfant_dans_famille', period)
        enfant_place = simulation.calculate('enfant_place', period)
        a_charge_fiscale = simulation.calculate('a_charge_fiscale', period)

        return period, est_enfant_dans_famille * (1 - enfant_place) * a_charge_fiscale

class plf_enfant_garde_alternee(Variable):
    column = BoolCol
    label = u"Enfant en garde alternée pris en compte par la mairie de Paris pour PLF"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        alt = simulation.calculate('alt', period)
        plf_enfant = simulation.calculate('plf_enfant', period)

        return period, alt * plf_enfant

class plf_enfant_handicape_garde_alternee(Variable):
    column = BoolCol
    label = u"Enfant handicapé en garde alternée pris en compte par la mairie de Paris pour PLF"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        alt = simulation.calculate('alt', period)
        plf_enfant_handicape = simulation.calculate('plf_enfant_handicape', period)

        return period, alt * plf_enfant_handicape
