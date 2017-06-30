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

    def formula(individu, period, legislation):
        salaire_de_base = individu('salaire_de_base', period, options = [ADD])
        chomage_brut = individu('chomage_brut', period, options = [ADD])
        retraite_brute = individu('retraite_brute', period, options = [ADD])
        rev_cap_bar = individu.foyer_fiscal('rev_cap_bar', period, options = [ADD]) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        rev_cap_lib = individu.foyer_fiscal('rev_cap_lib', period, options = [ADD]) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        return salaire_de_base + chomage_brut + retraite_brute + rev_cap_bar + rev_cap_lib


class impot_revenu_lps(Variable):
    column = FloatCol
    entity = Individu
    label = u"Impôt individuel sur l'ensemble de l'assiette de la csg, comme proposé par Landais, Piketty et Saez"
    definition_period = YEAR

    def formula(individu, period, legislation):
        janvier = period.first_month

        nbF = individu.foyer_fiscal('nbF', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        nbH = individu.foyer_fiscal('nbH', period) * individu.has_role(FoyerFiscal.DECLARANT_PRINCIPAL)
        nbEnf = (nbF + nbH / 2)
        lps = legislation(period).landais_piketty_saez
        ae = nbEnf * lps.abatt_enfant
        re = nbEnf * lps.reduc_enfant
        ce = nbEnf * lps.credit_enfant
        statut_marital = individu('statut_marital', period = janvier)
        couple = (statut_marital == 1) | (statut_marital == 5)
        ac = couple * lps.abatt_conj
        rc = couple * lps.reduc_conj
        assiette_csg = individu('assiette_csg', period)
        return -max_(0, lps.bareme.calc(max_(assiette_csg - ae - ac, 0)) - re - rc) + ce


class revenu_disponible(Variable):
    column = FloatCol
    entity = Menage
    label = u"Revenu disponible du ménage"
    reference = u"http://fr.wikipedia.org/wiki/Revenu_disponible"
    definition_period = YEAR

    def formula(menage, period, legislation):
        impot_revenu_lps_i = menage.members('impot_revenu_lps', period)
        impot_revenu_lps = menage.sum(impot_revenu_lps_i)
        pen_i = menage.members('pensions', period)
        pen = menage.sum(pen_i)
        prestations_sociales_i = menage.members.famille('prestations_sociales', period) * individu.has_role(Famille.DEMANDEUR)
        prestations_sociales = menage.sum(prestations_sociales)
        revenus_du_capital_i = menage.members('revenus_du_capital', period)
        revenus_du_capital = menage.sum(revenus_du_capital_i)
        revenus_du_travail_i = menage.members('revenus_du_travail', period)
        revenus_du_travail = menage.sum(revenus_du_travail_i)

        return revenus_du_travail + pen + revenus_du_capital + impot_revenu_lps + prestations_sociales


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "type": "node",
        "description": u"Impôt à base large proposé par Landais, Piketty et Saez",
        "children": {
            "bareme": {
                "type": "scale",
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
                "type": "parameter",
                "description": u"Indicatrice d'imposition",
                "format": "boolean",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2000-01-01', 'value': True},
                    ],
                },
            "credit_enfant": {
                "type": "parameter",
                "description": u"Crédit d'impôt forfaitaire par enfant",
                "format": "integer",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2000-01-01', 'value': 0},
                    ],
                },
            "reduc_enfant": {
                "type": "parameter",
                "description": u"Réduction d'impôt forfaitaire par enfant",
                "format": "integer",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2000-01-01', 'value': 0},
                    ],
                },
            "abatt_enfant": {
                "type": "parameter",
                "description": u"Abattement forfaitaire sur le revenu par enfant",
                "format": "integer",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2000-01-01', 'value': 0},
                    ],
                },
            "reduc_conj": {
                "type": "parameter",
                "description": u"Réduction d'impôt forfaitaire si conjoint",
                "format": "integer",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2000-01-01', 'value': 0},
                    ],
                },
            "abatt_conj": {
                "type": "parameter",
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
