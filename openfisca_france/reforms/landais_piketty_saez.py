# -*- coding: utf-8 -*-


# TODO switch to to average tax rates


"""Impôt Landais, Piketty, Saez"""


from __future__ import division

from numpy import maximum as max_
from openfisca_core import columns, reforms
from openfisca_france import entities
from openfisca_france.model.base import QUIFAM, QUIFOY


def build_reform(base_tax_benefit_system):
    Reform = reforms.make_reform(
        reference = base_tax_benefit_system,
        key = 'landais_piketty_saez',
        name = u'Landais Piketty Saez',
        )

    class assiette_csg(Reform.Variable):
        column = columns.FloatCol
        entity_class = entities.Individus
        label = u"Assiette de la CSG"

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('year')
            salaire_de_base = simulation.calculate('salaire_de_base', period)
            chomage_brut = simulation.calculate('chomage_brut', period)
            retraite_brute = simulation.calculate('retraite_brute', period)
            rev_cap_bar_holder = simulation.compute_add('rev_cap_bar', period)
            rev_cap_lib_holder = simulation.compute_add('rev_cap_lib', period)
            rev_cap_bar = self.cast_from_entity_to_role(rev_cap_bar_holder, role = QUIFOY['vous'])
            rev_cap_lib = self.cast_from_entity_to_role(rev_cap_lib_holder, role = QUIFOY['vous'])
            return period, salaire_de_base + chomage_brut + retraite_brute + rev_cap_bar + rev_cap_lib

    class impot_revenu_lps(Reform.Variable):
        column = columns.FloatCol
        entity_class = entities.Individus
        label = u"Impôt individuel sur l'ensemble de l'assiette de la csg, comme proposé par Landais, Piketty et Saez"

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('year')
            nbF_holder = simulation.compute('nbF')
            nbF = self.cast_from_entity_to_role(nbF_holder, role = QUIFOY['vous'])
            nbH_holder = simulation.compute('nbH')
            nbH = self.cast_from_entity_to_role(nbH_holder, role = QUIFOY['vous'])
            nbEnf = (nbF + nbH / 2)
            lps = simulation.legislation_at(period.start).landais_piketty_saez
            ae = nbEnf * lps.abatt_enfant
            re = nbEnf * lps.reduc_enfant
            ce = nbEnf * lps.credit_enfant
            statut_marital = simulation.calculate('statut_marital')
            couple = (statut_marital == 1) | (statut_marital == 5)
            ac = couple * lps.abatt_conj
            rc = couple * lps.reduc_conj
            assiette_csg = simulation.calculate('assiette_csg')
            return period, -max_(0, lps.bareme.calc(max_(assiette_csg - ae - ac, 0)) - re - rc) + ce

    class revenu_disponible(Reform.Variable):
        column = columns.FloatCol(default = 0)
        entity_class = entities.Menages
        label = u"Revenu disponible du ménage"
        url = u"http://fr.wikipedia.org/wiki/Revenu_disponible"

        def function(self, simulation, period):
            period = period.start.offset('first-of', 'month').period('year')
            impot_revenu_lps_holder = simulation.compute('impot_revenu_lps')
            impot_revenu_lps = self.sum_by_entity(impot_revenu_lps_holder)
            pen_holder = simulation.compute('pen')
            pen = self.sum_by_entity(pen_holder)
            psoc_holder = simulation.compute('psoc')
            psoc = self.cast_from_entity_to_role(psoc_holder, role = QUIFAM['chef'])
            psoc = self.sum_by_entity(psoc)
            rev_cap_holder = simulation.compute('rev_cap')
            rev_cap = self.sum_by_entity(rev_cap_holder)
            rev_trav_holder = simulation.compute('rev_trav')
            rev_trav = self.sum_by_entity(rev_trav_holder)
            return rev_trav + pen + rev_cap + impot_revenu_lps + psoc

    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform


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
                        "rate": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .02}],
                        "threshold": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 1100}],
                        },
                    {
                        "rate": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .1}],
                        "threshold": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 2200}],
                        },
                    {
                        "rate": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .13}],
                        "threshold": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 5000}],
                        },
                    {
                        "rate": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .25}],
                        "threshold": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 10000}],
                        },
                    {
                        "rate": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .5}],
                        "threshold": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 40000}],
                        },
                    {
                        "rate": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': .6}],
                        "threshold": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 100000}],
                        },
                    ],
                },
            "imposition": {
                "@type": "Parameter",
                "description": u"Indicatrice d'imposition",
                "format": "boolean",
                "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': True}],
                },
            "credit_enfant": {
                "@type": "Parameter",
                "description": u"Crédit d'impôt forfaitaire par enfant",
                "format": "integer",
                "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 0}],
                },
            "reduc_enfant": {
                "@type": "Parameter",
                "description": u"Réduction d'impôt forfaitaire par enfant",
                "format": "integer",
                "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 0}],
                },
            "abatt_enfant": {
                "@type": "Parameter",
                "description": u"Abattement forfaitaire sur le revenu par enfant",
                "format": "integer",
                "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 0}],
                },
            "reduc_conj": {
                "@type": "Parameter",
                "description": u"Réduction d'impôt forfaitaire si conjoint",
                "format": "integer",
                "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 0}],
                },
            "abatt_conj": {
                "@type": "Parameter",
                "description": u"Abattement forfaitaire sur le revenu si conjoint",
                "format": "integer",
                "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 0}],
                },
            },
        }
    reference_legislation_json_copy['children']['landais_piketty_saez'] = reform_legislation_subtree
    return reference_legislation_json_copy
