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
    
    class paris_logement_familles_elig(Reform.Variable):
        column = columns.BoolCol
        label = u"Eligibilité à Paris-Logement-Familles"
        entity_class = entities.Familles

        def function(self, simulation, period):
            parisien = simulation.calculate('parisien', period)
            statut_occupation = simulation.calculate('statut_occupation', period)
            charge_logement = (
                (statut_occupation == 1) +
                (statut_occupation == 2) +
                (statut_occupation == 3) +
                (statut_occupation == 4) +
                (statut_occupation == 5) +
                (statut_occupation == 7)
                )

            result = parisien * charge_logement

            return period, result


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
            garde_alternee = (nb_enf_handicape - nb_enf_handicape_garde_alternee) == 0
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
                                "values": [{'start': u'2014-01-01', 'stop': u'2015-12-31', 'value': 5000}],
                                },
                            "plafond_bas_3enf": {
                                "@type": "Parameter",
                                "description": "Plafond bas de PLF pour les familles à 3 enfants",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2015-12-31', 'value': 3000}],
                                },
                            "plafond_2enf": {
                                "@type": "Parameter",
                                "description": "Plafond de PLF pour les familles à deux enfants.",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2015-12-31', 'value': 2000}],
                                },
                            "montant_haut_3enf": {
                                "@type": "Parameter",
                                "description": "Montant haut PLF pour famille à 3 enfants",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2015-12-31', 'value': 128}],
                            },
                            "montant_bas_3enf": {
                                "@type": "Parameter",
                                "description": "Montant bas PLF pour famille à 3 enfants.",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2015-12-31', 'value': 84}],
                                },
                            "montant_2enf": {
                                "@type": "Parameter",
                                "description": "Montant PLF pour les familles à deux enfants.",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2015-12-31', 'value': 116}],
                                },
                            "montant_haut_enf_sup": {
                                "@type": "Parameter",
                                "description": "Montant haut sup par enfant",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2015-12-31', 'value': 41}],
                                },
                            "montant_bas_enf_sup": {
                                "@type": "Parameter",
                                "description": "Montant bas sup par enfant.",
                                "unit": "currency",
                                "format": "float",
                                "values": [{'start': u'2014-01-01', 'stop': u'2015-12-31', 'value': 21}],
                                },
                            }
                        }
                    }
                },
            },
        }
    reference_legislation_json_copy['children']['aides_locales'] = reform_legislation_subtree
    return reference_legislation_json_copy
