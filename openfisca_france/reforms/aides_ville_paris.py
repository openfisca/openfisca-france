# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import columns, reforms
from numpy import absolute as abs_, minimum as min_, maximum as max_

from .. import entities


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'aides_ville_paris',
        name = u'Aides de la ville de Paris',
        reference = tax_benefit_system,
        )

    class parisien(Reform.Variable):
        column = columns.BoolCol
        entity_class = entities.Menages
        label = u"Résidant à Paris au moins 3 ans dans les 5 dernières années"

    class a_charge_fiscale(Reform.Variable):
        column = columns.BoolCol
        entity_class = entities.Individus
        label = u"Enfant à charge fiscale du demandeur"

    class enfant_place(Reform.Variable):
        column = columns.BoolCol
        entity_class = entities.Individus
        label = u"Enfant placé en structure spécialisée ou famille d'accueil"

    class paris_logement_familles_elig(Reform.Variable):
        column = columns.BoolCol
        label = u"Eligibilité à Paris-Logement-Familles"
        entity_class = entities.Familles

        def function(self, simulation, period):
            parisien = simulation.calculate('parisien', period)
            statut_occupation_logement = simulation.calculate('statut_occupation_logement', period)
            charge_logement = (
                (statut_occupation_logement == 1) +
                (statut_occupation_logement == 2) +
                (statut_occupation_logement == 3) +
                (statut_occupation_logement == 4) +
                (statut_occupation_logement == 5) +
                (statut_occupation_logement == 7)
                )

            result = parisien * charge_logement

            return period, result

    class paris_logement_familles_br_i(Reform.Variable):
        column = columns.FloatCol
        label = u"Base de ressources individuelle pour Paris Logement Famille"
        entity_class = entities.Individus

        def function(self, simulation, period):
            period = period.this_month
            last_year = period.last_year
            salaire_net = simulation.calculate('salaire_net', period)
            chomage_net = simulation.calculate('chomage_net', period)
            retraite_nette = simulation.calculate('retraite_nette', period)
            pensions_alimentaires_percues = simulation.calculate('pensions_alimentaires_percues', period)
            pensions_alimentaires_versees_individu = simulation.calculate(
                'pensions_alimentaires_versees_individu', period)
            rsa_base_ressources_patrimoine_i = simulation.calculate_add('rsa_base_ressources_patrimoine_individu', period)
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
                salaire_net + indemnites_chomage_partiel + indemnites_stage + chomage_net + retraite_nette +
                pensions_alimentaires_percues - abs_(pensions_alimentaires_versees_individu) +
                rsa_base_ressources_patrimoine_i + allocation_securisation_professionnelle +
                indemnites_journalieres_imposables + prestation_compensatoire +
                pensions_invalidite + bourse_recherche + gains_exceptionnels + revenus_tns() +
                revenus_stage_formation_pro
                )

            return period, result

    class paris_logement_familles_br(Reform.Variable):
        column = columns.FloatCol
        label = u"Base de ressource pour Paris Logement Famille"
        entity_class = entities.Familles

        def function(self, simulation, period):
            period = period.this_month
            paris_logement_familles_br_i_holder = simulation.compute('paris_logement_familles_br_i', period)
            paris_logement_familles_br = self.sum_by_entity(paris_logement_familles_br_i_holder)
            result = paris_logement_familles_br

            return period, result

    class plf_enfant_handicape(Reform.Variable):
        column = columns.BoolCol
        label = u"Enfant handicapé au sens de la mairie de Paris"
        entity_class = entities.Individus

        def function(self, simulation, period):
            period = period.this_month

            handicap = simulation.calculate('handicap', period)
            plf_enfant = simulation.calculate('plf_enfant', period)

            return period, plf_enfant * handicap

    class plf_enfant(Reform.Variable):
        column = columns.BoolCol
        label = u"Enfant pris en compte par la mairie de Paris pour PLF"
        entity_class = entities.Individus

        def function(self, simulation, period):
            period = period.this_month
            est_enfant_dans_famille = simulation.calculate('est_enfant_dans_famille', period)
            enfant_place = simulation.calculate('enfant_place', period)
            a_charge_fiscale = simulation.calculate('a_charge_fiscale', period)

            return period, est_enfant_dans_famille * (1 - enfant_place) * a_charge_fiscale

    class plf_enfant_garde_alternee(Reform.Variable):
        column = columns.BoolCol
        label = u"Enfant en garde alternée pris en compte par la mairie de Paris pour PLF"
        entity_class = entities.Individus

        def function(self, simulation, period):
            period = period.this_month
            garde_alternee = simulation.calculate('garde_alternee', period)
            plf_enfant = simulation.calculate('plf_enfant', period)

            return period, garde_alternee * plf_enfant

    class plf_enfant_handicape_garde_alternee(Reform.Variable):
        column = columns.BoolCol
        label = u"Enfant handicapé en garde alternée pris en compte par la mairie de Paris pour PLF"
        entity_class = entities.Individus

        def function(self, simulation, period):
            period = period.this_month
            garde_alternee = simulation.calculate('garde_alternee', period)
            plf_enfant_handicape = simulation.calculate('plf_enfant_handicape', period)

            return period, garde_alternee * plf_enfant_handicape

    class plf_handicap(Reform.Variable):
        column = columns.FloatCol
        entity_class = entities.Familles
        label = u"Allocation Paris-Logement-Familles en cas d'enfant handicapé"

        def function(self, simulation, period):
            period = period.this_month
            plf_enfant_handicape = simulation.compute('plf_enfant_handicape', period)
            plf_enfant_handicape_garde_alternee = simulation.compute('plf_enfant_handicape_garde_alternee', period)
            br = simulation.calculate('paris_logement_familles_br', period)

            nb_enf_handicape = self.sum_by_entity(plf_enfant_handicape)
            nb_enf_handicape_garde_alternee = self.sum_by_entity(plf_enfant_handicape_garde_alternee)

            P = simulation.legislation_at(period.start).aides_locales.paris.paris_logement_familles
            plafond = P.plafond_haut_3enf
            montant = P.montant_haut_3enf

            plf_handicap = (nb_enf_handicape > 0) * (br <= plafond) * montant

            # Si tous les enfants handicapés sont en garde alternée
            garde_alternee = nb_enf_handicape - nb_enf_handicape_garde_alternee == 0
            deduction_garde_alternee = garde_alternee * 0.5 * plf_handicap

            plf_handicap = plf_handicap - deduction_garde_alternee

            return period, plf_handicap

    class paris_logement_familles(Reform.Variable):
        column = columns.FloatCol
        label = u"Allocation Paris Logement Familles"
        entity_class = entities.Familles
        url = "http://www.paris.fr/pratique/toutes-les-aides-et-allocations/aides-sociales/paris-logement-familles-prestation-ville-de-paris/rub_9737_stand_88805_port_24193"  # noqa

        def function(self, simulation, period):
            period = period.this_month
            elig = simulation.calculate('paris_logement_familles_elig', period)
            br = simulation.calculate('paris_logement_familles_br', period)
            plf_enfant = simulation.compute('plf_enfant', period)
            nbenf = self.sum_by_entity(plf_enfant)
            plf_enfant_garde_alternee = simulation.compute('plf_enfant_garde_alternee', period)
            nbenf_garde_alternee = self.sum_by_entity(plf_enfant_garde_alternee)
            plf_handicap = simulation.calculate('plf_handicap', period)
            loyer = simulation.calculate('loyer', period) + simulation.calculate('charges_locatives', period)
            P = simulation.legislation_at(period.start).aides_locales.paris.paris_logement_familles

            ressources_sous_plaf_bas = (br <= P.plafond_bas_3enf)
            ressources_sous_plaf_haut = (br <= P.plafond_haut_3enf) * (br > P.plafond_bas_3enf)
            montant_base_3enfs = (nbenf >= 3) * (
                ressources_sous_plaf_bas * P.montant_haut_3enf +
                ressources_sous_plaf_haut * P.montant_bas_3enf
                )
            montant_enf_sup = (
                ressources_sous_plaf_bas * P.montant_haut_enf_sup +
                ressources_sous_plaf_haut * P.montant_bas_enf_sup
                )
            montant_3enfs = montant_base_3enfs + montant_enf_sup * max_(nbenf - 3, 0)
            montant_2enfs = (nbenf == 2) * (br <= P.plafond_2enf) * P.montant_2enf

            plf = montant_2enfs + montant_3enfs

            deduction_garde_alternee = (nbenf_garde_alternee > 0) * (
                (nbenf - nbenf_garde_alternee < 3) * 0.5 * plf +
                (nbenf - nbenf_garde_alternee >= 3) * nbenf_garde_alternee * 0.5 * montant_enf_sup
                )

            plf = plf - deduction_garde_alternee

            plf = max_(plf, plf_handicap)
            plf = elig * plf
            plf = min_(plf, loyer)

            return period, plf

    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "Aides locales",
        "children": {
            "paris": {
                "@type": "Node",
                "description": "Aides de la ville de Paris",
                "children": {
                    "paris_logement_familles": {
                        "@type": "Node",
                        "description": "Paris Logement Famille",
                        "children": {
                            "plafond_haut_3enf": {
                                "@type": "Parameter",
                                "description": "Plafond haut de PLF pour les familles à 3 enfants, aussi plafond de PLF avec enfant handicapé",  # noqa
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2016-12-31', 'value': 5000}],
                                },
                            "plafond_bas_3enf": {
                                "@type": "Parameter",
                                "description": "Plafond bas de PLF pour les familles à 3 enfants",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2016-12-31', 'value': 3000}],
                                },
                            "plafond_2enf": {
                                "@type": "Parameter",
                                "description": "Plafond de PLF pour les familles à deux enfants.",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2016-12-31', 'value': 2000}],
                                },
                            "montant_haut_3enf": {
                                "@type": "Parameter",
                                "description": "Montant haut PLF pour famille à 3 enfants",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2016-12-31', 'value': 128}],
                            },
                            "montant_bas_3enf": {
                                "@type": "Parameter",
                                "description": "Montant bas PLF pour famille à 3 enfants.",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2016-12-31', 'value': 84}],
                                },
                            "montant_2enf": {
                                "@type": "Parameter",
                                "description": "Montant PLF pour les familles à deux enfants.",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2016-12-31', 'value': 116}],
                                },
                            "montant_haut_enf_sup": {
                                "@type": "Parameter",
                                "description": "Montant haut sup par enfant",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2016-12-31', 'value': 41}],
                                },
                            "montant_bas_enf_sup": {
                                "@type": "Parameter",
                                "description": "Montant bas sup par enfant.",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2016-12-31', 'value': 21}],
                                },
                            }
                        }
                    }
                },
            },
        }
    reference_legislation_json_copy['children']['aides_locales'] = reform_legislation_subtree
    return reference_legislation_json_copy
