# -*- coding: utf-8 -*-

from __future__ import division


from numpy import maximum as max_, minimum as min_, round as round_


from openfisca_core import formulas, periods, reforms
from ..model.base import *  # analysis.ignore
from ..model.prelevements_obligatoires.impot_revenu import ir, reductions_impot


# Réforme de l'amendement Ayrault-Muet

def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'ayrault_muet',
        name = u'Amendement Ayrault-Muet au PLF2016',
        reference = tax_benefit_system,
        )

    @Reform.formula
    class reduction_csg(formulas.DatedFormulaColumn):
        column = FloatCol
        entity_class = FoyersFiscaux
        label = u"Réduction dégressive de CSG"

        @dated_function(start = date(2015, 1, 1))
        def function_2015__(self, simulation, period):
            period = period.start.offset('first-of', 'year').period('year')
            smic_proratise = simulation.calculate_add('smic_proratise', period)
            assiette_csg_abattue = simulation.calculate_add('assiette_csg_abattue', period)

            seuil = 1.34
            coefficient_correctif = .9
            taux_csg = (
                simulation.legislation_at(period.start).csg.activite.imposable.taux +
                simulation.legislation_at(period.start).csg.activite.deductible.taux
                )
            tx_max = coefficient_correctif * taux_csg
            print tx_max
            ratio_smic_salaire = smic_proratise / (assiette_csg_abattue + 1e-16)
            # règle d'arrondi: 4 décimales au dix-millième le plus proche
            taux_allegement_csg = tx_max * min_(1, max_(seuil - 1 / ratio_smic_salaire, 0) / (seuil - 1))
            # Montant de l'allegment
            print 1 / ratio_smic_salaire
            print taux_allegement_csg
            return period, taux_allegement_csg * assiette_csg_abattue

    reform = Reform()
    # reform.modify_legislation_json(modifier_function = counterfactual_modify_legislation_json)
    return reform


def ayrault_muet_modify_legislation_json(reference_legislation_json_copy):
    # TODO: inflater les paramètres de la décote le barème de l'IR
    inflation = .001
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "PLF 2016 sur revenus 2015",
        "children": {
            "decote_seuil_celib": {
                "@type": "Parameter",
                "description": "Seuil de la décôte pour un célibataire",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': round(1135 * (1 + inflation))}],
                },
            "decote_seuil_couple": {
                "@type": "Parameter",
                "description": "Seuil de la décôte pour un couple",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': round(1870 * (1 + inflation))}],
                },
            },
        }
    reference_legislation_json_copy['children']['ayrault_muet'] = reform_legislation_subtree
    return reference_legislation_json_copy
