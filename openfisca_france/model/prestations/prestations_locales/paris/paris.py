# -*- coding: utf-8 -*-
from __future__ import division

from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select)

from ....base import *  # noqa analysis:ignore

class parisien(Variable):
    column = BoolCol
    entity_class = Familles
    label = u"Résidant à Paris au moins 3 ans dans les 5 dernières années"

class a_charge_fiscale(Variable):
    column = BoolCol(default = True)
    entity_class = Individus
    label = u"Enfant à charge fiscale du demandeur"

class enfant_place(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Enfant placé en structure spécialisée ou famille d'accueil"

class paris_base_ressources_i(Variable):
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
            aah = simulation.calculate('aah', period)

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
                revenus_stage_formation_pro + aah
                )

            return period, result

class paris_base_ressources(Variable):
    column = FloatCol
    label = u"Base de ressource pour Paris Logement Famille"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.this_month
        aspa = simulation.calculate('aspa', period)
        paris_base_ressources_i_holder = simulation.compute('paris_base_ressources_i', period)
        paris_base_ressources = self.sum_by_entity(paris_base_ressources_i_holder)
        result = paris_base_ressources + aspa

        return period, result

class paris_enfant_handicape(Variable):
    column = BoolCol
    label = u"Enfant handicapé au sens de la mairie de Paris"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month

        invalide = simulation.calculate('invalide', period)
        paris_enfant = simulation.calculate('paris_enfant', period)

        return period, paris_enfant * invalide

class paris_enfant(Variable):
    column = BoolCol
    label = u"Enfant pris en compte par la mairie de Paris pour PLF"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        est_enfant_dans_famille = simulation.calculate('est_enfant_dans_famille', period)
        enfant_place = simulation.calculate('enfant_place', period)
        a_charge_fiscale = simulation.calculate('a_charge_fiscale', period)

        return period, est_enfant_dans_famille * (1 - enfant_place) * a_charge_fiscale

class paris_enfant_garde_alternee(Variable):
    column = BoolCol
    label = u"Enfant en garde alternée pris en compte par la mairie de Paris pour PLF"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        alt = simulation.calculate('alt', period)
        paris_enfant = simulation.calculate('paris_enfant', period)

        return period, alt * paris_enfant

class paris_enfant_handicape_garde_alternee(Variable):
    column = BoolCol
    label = u"Enfant handicapé en garde alternée pris en compte par la mairie de Paris pour PLF"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.this_month
        alt = simulation.calculate('alt', period)
        paris_enfant_handicape = simulation.calculate('paris_enfant_handicape', period)

        return period, alt * paris_enfant_handicape

class personnes_agees(Variable):
    column = BoolCol
    label = u"Personne âgée"
    entity_class = Individus

    def function(self, simulation, period):
        age_min = simulation.legislation_at(period.start).paris.age_pers_agee
        age = simulation.calculate('age', period)
        aspa_elig = simulation.calculate('aspa_elig', period)
        personne_agee = (age >= age_min) + (aspa_elig)
        return period, personne_agee

class personnes_handicap_paris(Variable):
    column = BoolCol
    label = u"Personne qui possède l'AAH"
    entity_class = Individus

    def function(self, simulation, period):
        aah = simulation.calculate('aah', period)
        condition_aah = aah > 0
        return period, condition_aah

class paris_nb_enfants(Variable):
    column = FloatCol
    label = u"Nombre d'enfant dans la famille"
    entity_class = Familles

    def function(self, simulation, period):
        nb_enfants = simulation.compute('paris_enfant', period)
        paris_nb_enfants = self.sum_by_entity(nb_enfants)
        return period, paris_nb_enfants

class condition_taux_effort(Variable):
    column = BoolCol
    label = u"Taux d'effort"
    entity_class = Familles

    def function(self, simulation, period):
        taux_effort = simulation.legislation_at(period.start).paris.paris_logement.taux_effort
        loyer = simulation.calculate('loyer', period)

        ressources_mensuelles = simulation.calculate('paris_base_ressources', period)
        charges_forfaitaire_logement = simulation.calculate('charges_forfaitaire_logement', period)
        montant_aide_logement = simulation.calculate('aide_logement', period)
        calcul_taux_effort = (loyer + charges_forfaitaire_logement - montant_aide_logement) / ressources_mensuelles
        condition_loyer = calcul_taux_effort >= taux_effort
        return period, condition_loyer


class charges_forfaitaire_logement(Variable):
    column = FloatCol
    label = u"Charges Forfaitaire Logement (CAF)"
    entity_class = Familles

    def function(self, simulation, period):
        charges_forf_pers_isol = simulation.legislation_at(period.start).paris.charges_forf_pers_isol
        charges_forf_coloc = simulation.legislation_at(period.start).paris.charges_forf_coloc
        charges_forf_couple_ss_enf = simulation.legislation_at(period.start).paris.charges_forf_couple_ss_enf
        charges_forf_couple_enf = simulation.legislation_at(period.start).paris.charges_forf_couple_enf

        colocation_obj = simulation.compute('coloc', period)
        colocation = self.any_by_roles(colocation_obj)
        nb_enfants = simulation.calculate('paris_nb_enfants', period)
        couple = simulation.calculate('concub', period)
        personne_isol = (couple != 1) * (colocation != 1)
        personne_isol_coloc = (couple != 1) * colocation
        result = select([(personne_isol * (nb_enfants < 1)),
            (personne_isol_coloc * (nb_enfants < 1)), (couple * (nb_enfants < 1)),
            (couple * (nb_enfants >= 1)), (personne_isol * (nb_enfants >= 1))],
            [charges_forf_pers_isol, charges_forf_coloc, charges_forf_couple_ss_enf, charges_forf_couple_enf, 0])
        return period, result
