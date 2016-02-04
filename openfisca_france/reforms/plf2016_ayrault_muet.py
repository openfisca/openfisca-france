# -*- coding: utf-8 -*-

from __future__ import division


from numpy import maximum as max_, minimum as min_, logical_not as not_


from openfisca_core import formulas, reforms
from ..model.base import *  # analysis.ignore
from ..model.prelevements_obligatoires.impot_revenu import ir


# Réforme de l'amendement Ayrault-Muet

def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'ayrault_muet',
        name = u'Amendement Ayrault-Muet au PLF2016',
        reference = tax_benefit_system,
        )

    class variator(Reform.Variable):
        column = FloatCol(default = 1)
        entity_class = FoyersFiscaux
        label = u'Multiplicateur du seuil de régularisation'

    class reduction_csg(Reform.DatedVariable):
        column = FloatCol
        entity_class = Individus
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
            ratio_smic_salaire = smic_proratise / (assiette_csg_abattue + 1e-16)
            # règle d'arrondi: 4 décimales au dix-millième le plus proche
            taux_allegement_csg = tx_max * min_(1, max_(seuil - 1 / ratio_smic_salaire, 0) / (seuil - 1))
            # Montant de l'allegment

            return period, taux_allegement_csg * assiette_csg_abattue

    class reduction_csg_foyer_fiscal(Reform.PersonToEntityColumn):
        entity_class = FoyersFiscaux
        label = u"Réduction dégressive de CSG des memebres du foyer fiscal"
        operation = 'add'
        variable = reduction_csg

    class reduction_csg_nette(Reform.DatedVariable):
        column = FloatCol
        entity_class = Individus
        label = u"Réduction dégressive de CSG"

        @dated_function(start = date(2015, 1, 1))
        def function_2015__(self, simulation, period):
            period = period.start.offset('first-of', 'year').period('year')
            reduction_csg = simulation.calculate('reduction_csg', period)
            ppe_elig_bis_individu = simulation.calculate('ppe_elig_bis_individu', period)
            return period, reduction_csg * ppe_elig_bis_individu

    class ppe_elig_bis(Reform.Variable):
        column = BoolCol(default = False)
        entity_class = FoyersFiscaux
        label = u"ppe_elig_bis"

        def function(self, simulation, period):
            '''
            PPE: eligibilité à la ppe, condition sur le revenu fiscal de référence
            'foy'
            '''
            period = period.start.offset('first-of', 'year').period('year')
            rfr = simulation.calculate('rfr', period)
            ppe_coef = simulation.calculate('ppe_coef', period)
            marpac = simulation.calculate('marpac', period)
            veuf = simulation.calculate('veuf', period)
            celdiv = simulation.calculate('celdiv', period)
            nbptr = simulation.calculate('nbptr', period)
            variator = simulation.calculate('variator', period)
            ppe = simulation.legislation_at(period.start).ir.credits_impot.ppe
            seuil = (veuf | celdiv) * (ppe.eligi1 + 2 * max_(nbptr - 1, 0) * ppe.eligi3) \
                + marpac * (ppe.eligi2 + 2 * max_(nbptr - 2, 0) * ppe.eligi3)
            return period, (rfr * ppe_coef) <= (seuil * variator)

    class ppe_elig_bis_individu(Reform.EntityToPersonColumn):
        entity_class = Individus
        variable = ppe_elig_bis

    class regularisation_reduction_csg(Reform.DatedVariable):
        column = FloatCol
        entity_class = FoyersFiscaux
        label = u"Régularisation complète réduction dégressive de CSG"

        @dated_function(start = date(2015, 1, 1))
        def function_2015__(self, simulation, period):
            period = period.start.offset('first-of', 'year').period('year')
            reduction_csg = simulation.calculate('reduction_csg_foyer_fiscal', period)
            ppe_elig_bis = simulation.calculate('ppe_elig_bis', period)
            return period, not_(ppe_elig_bis) * (reduction_csg > 1)

    reform = Reform()
    reform.modify_legislation_json(modifier_function = ayrault_muet_modify_legislation_json)
    return reform


def ayrault_muet_modify_legislation_json(reference_legislation_json_copy):
    # TODO: inflater les paramètres de la décote le barème de l'IR
    inflator = 1
    for inflation in [2.8, 0.1, 1.5, 2.1, 2, 0.9, 0.5, 0.1]:
        inflator = inflator * (1 + inflation / 100)
    del inflation

    reform_legislation_subtree = {
        "elig1": {
            "@type": "Parameter",
            "format": "integer",
            "unit": "currency",
            "values": [{'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': round(16251 * inflator)}],
            },
        "elig2": {
            "@type": "Parameter",
            "format": "integer",
            "unit": "currency",
            "values": [{'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': round(32498 * inflator)}],
            },
        "elig3": {
            "@type": "Parameter",
            "format": "integer",
            "unit": "currency",
            "values": [{'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': round(4490 * inflator)}],
            },
        }
    reference_legislation_json_copy['children']['ir']['children']['credits_impot']['children']['ppe']['children'].update(
        reform_legislation_subtree)
    return reference_legislation_json_copy
