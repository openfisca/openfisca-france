# -*- coding: utf-8 -*-


# TODO switch to to average tax rates


"""Impôt Landais, Piketty, Saez"""


from __future__ import division

from openfisca_core.reforms import Reform
from openfisca_france.model.base import *

class assiette_csg(Variable):
    column = FloatCol
    entity = Individu
    label = u"Assiette de la CSG"
    definition_period = YEAR

    def formula(self, simulation, period):
        salaire_de_base = simulation.calculate_add('salaire_de_base', period)
        chomage_brut = simulation.calculate_add('chomage_brut', period)
        retraite_brute = simulation.calculate_add('retraite_brute', period)
        rev_cap_bar_holder = simulation.compute_add('rev_cap_bar', period)
        rev_cap_lib_holder = simulation.compute_add('rev_cap_lib', period)
        rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = QUIFOY['vous'])
        rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = QUIFOY['vous'])
        return salaire_de_base + chomage_brut + retraite_brute + rev_cap_bar + rev_cap_lib

class impot_revenu_lps(Variable):
    column = FloatCol
    entity = Individu
    label = u"Impôt individuel sur l'ensemble de l'assiette de la csg, comme proposé par Landais, Piketty et Saez"
    definition_period = YEAR

    def formula(self, simulation, period):
        janvier = period.first_month

        nbF_holder = simulation.compute('nbF', period)
        nbF = self.cast_from_entity_to_role(nbF_holder, role = QUIFOY['vous'])
        nbH_holder = simulation.compute('nbH', period)
        nbH = self.cast_from_entity_to_role(nbH_holder, role = QUIFOY['vous'])
        nbEnf = (nbF + nbH / 2)
        lps = simulation.legislation_at(period.start).landais_piketty_saez
        ae = nbEnf * lps.abatt_enfant
        re = nbEnf * lps.reduc_enfant
        ce = nbEnf * lps.credit_enfant
        statut_marital = simulation.calculate('statut_marital', period = janvier)
        couple = (statut_marital == 1) | (statut_marital == 5)
        ac = couple * lps.abatt_conj
        rc = couple * lps.reduc_conj
        assiette_csg = simulation.calculate('assiette_csg', period)
        return -max_(0, lps.bareme.calc(max_(assiette_csg - ae - ac, 0)) - re - rc) + ce


class revenu_disponible(Variable):
    column = FloatCol
    entity = Menage
    label = u"Revenu disponible du ménage"
    url = u"http://fr.wikipedia.org/wiki/Revenu_disponible"
    definition_period = YEAR

    def formula(self, simulation, period):
        impot_revenu_lps_holder = simulation.compute('impot_revenu_lps', period)
        impot_revenu_lps = self.sum_by_entity(impot_revenu_lps_holder)
        pen_holder = simulation.compute('pensions', period)
        pen = self.sum_by_entity(pen_holder)
        prestations_sociales_holder = simulation.compute('prestations_sociales', period)
        prestations_sociales = self.cast_from_entity_to_role(prestations_sociales_holder, role = QUIFAM['chef'])
        prestations_sociales = self.sum_by_entity(prestations_sociales)
        revenus_du_capital_holder = simulation.compute('revenus_du_capital', period)
        revenus_du_capital = self.sum_by_entity(revenus_du_capital_holder)
        revenus_du_travail_holder = simulation.compute('revenus_du_travail', period)
        revenus_du_travail = self.sum_by_entity(revenus_du_travail_holder)
        return revenus_du_travail + pen + revenus_du_capital + impot_revenu_lps + prestations_sociales


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": u"Impôt à base large proposé par Landais, Piketty et Saez",
        "children": {
            "bareme": {
                "@type": "Scale",
                "unit": "currency",
                "description": u"Barème de l'impôt",
                "rates_kind": "average",
                "brackets": [
                    {
                        "rate": [
                            {'start': u'2015-01-01', },
                            {'start': u'2000-01-01', 'value': .02},
                            ],
                        "threshold": [
                            {'start': u'2015-01-01', },
                            {'start': u'2000-01-01', 'value': 1100},
                            ],
                        },
                    {
                        "rate": [
                            {'start': u'2015-01-01', },
                            {'start': u'2000-01-01', 'value': .1},
                            ],
                        "threshold": [
                            {'start': u'2015-01-01', },
                            {'start': u'2000-01-01', 'value': 2200},
                            ],
                        },
                    {
                        "rate": [
                            {'start': u'2015-01-01', },
                            {'start': u'2000-01-01', 'value': .13},
                            ],
                        "threshold": [
                            {'start': u'2015-01-01', },
                            {'start': u'2000-01-01', 'value': 5000},
                            ],
                        },
                    {
                        "rate": [
                            {'start': u'2015-01-01', },
                            {'start': u'2000-01-01', 'value': .25},
                            ],
                        "threshold": [
                            {'start': u'2015-01-01', },
                            {'start': u'2000-01-01', 'value': 10000},
                            ],
                        },
                    {
                        "rate": [
                            {'start': u'2015-01-01', },
                            {'start': u'2000-01-01', 'value': .5},
                            ],
                        "threshold": [
                            {'start': u'2015-01-01', },
                            {'start': u'2000-01-01', 'value': 40000},
                            ],
                        },
                    {
                        "rate": [
                            {'start': u'2015-01-01', },
                            {'start': u'2000-01-01', 'value': .6},
                            ],
                        "threshold": [
                            {'start': u'2015-01-01', },
                            {'start': u'2000-01-01', 'value': 100000},
                            ],
                        },
                    ],
                },
            "imposition": {
                "@type": "Parameter",
                "description": u"Indicatrice d'imposition",
                "format": "boolean",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2000-01-01', 'value': True},
                    ],
                },
            "credit_enfant": {
                "@type": "Parameter",
                "description": u"Crédit d'impôt forfaitaire par enfant",
                "format": "integer",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2000-01-01', 'value': 0},
                    ],
                },
            "reduc_enfant": {
                "@type": "Parameter",
                "description": u"Réduction d'impôt forfaitaire par enfant",
                "format": "integer",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2000-01-01', 'value': 0},
                    ],
                },
            "abatt_enfant": {
                "@type": "Parameter",
                "description": u"Abattement forfaitaire sur le revenu par enfant",
                "format": "integer",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2000-01-01', 'value': 0},
                    ],
                },
            "reduc_conj": {
                "@type": "Parameter",
                "description": u"Réduction d'impôt forfaitaire si conjoint",
                "format": "integer",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2000-01-01', 'value': 0},
                    ],
                },
            "abatt_conj": {
                "@type": "Parameter",
                "description": u"Abattement forfaitaire sur le revenu si conjoint",
                "format": "integer",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2000-01-01', 'value': 0},
                    ],
                },
            },
        }
    reference_legislation_json_copy['children']['landais_piketty_saez'] = reform_legislation_subtree
    return reference_legislation_json_copy


class landais_piketty_saez(Reform):
    name = u'Landais Piketty Saez'

    def apply(self):
        for variable in [assiette_csg, impot_revenu_lps, revenu_disponible]:
            self.update_variable(variable)
        self.modify_legislation_json(modifier_function = modify_legislation_json)
