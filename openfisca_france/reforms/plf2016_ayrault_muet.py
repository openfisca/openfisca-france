# -*- coding: utf-8 -*-

from __future__ import division


from numpy import maximum as max_, minimum as min_, logical_not as not_


from openfisca_core import periods
from openfisca_core.reforms import Reform, update_legislation
from ..model.base import *


# Réforme de l'amendement Ayrault-Muet

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
    reference_legislation_json_copy['children']['impot_revenu']['children']['credits_impot']['children']['ppe']['children'].update(
        reform_legislation_subtree)
    return reference_legislation_json_copy


class variator(Variable):
    column = FloatCol(default = 1)
    entity = FoyerFiscal
    label = u'Multiplicateur du seuil de régularisation'


class reduction_csg(DatedVariable):
    column = FloatCol
    entity = Individu
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


class reduction_csg_foyer_fiscal(Variable):
    entity = FoyerFiscal
    label = u"Réduction dégressive de CSG des memebres du foyer fiscal"
    column = FloatCol

    def function(self, simulation, period):
        reduction_csg = simulation.calculate('reduction_csg', period)
        return period, simulation.foyer_fiscal.sum(reduction_csg)


class reduction_csg_nette(DatedVariable):
    column = FloatCol
    entity = Individu
    label = u"Réduction dégressive de CSG"

    @dated_function(start = date(2015, 1, 1))
    def function_2015__(individu, period):
        period = period.this_year
        reduction_csg = individu('reduction_csg', period)
        ppe_elig_bis = individu.foyer_fiscal('ppe_elig_bis', period)
        return period, reduction_csg * ppe_elig_bis


class ppe_elig_bis(Variable):
    column = BoolCol(default = False)
    entity = FoyerFiscal
    label = u"ppe_elig_bis"

    def function(self, simulation, period):
        '''
        PPE: eligibilité à la ppe, condition sur le revenu fiscal de référence
        'foy'
        '''
        period = period.start.offset('first-of', 'year').period('year')
        rfr = simulation.calculate('rfr', period)
        ppe_coef = simulation.calculate('ppe_coef', period)
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        veuf = simulation.calculate('veuf', period)
        celibataire_ou_divorce = simulation.calculate('celibataire_ou_divorce', period)
        nbptr = simulation.calculate('nbptr', period)
        variator = simulation.calculate('variator', period)
        ppe = simulation.legislation_at(period.start).impot_revenu.credits_impot.ppe
        seuil = (veuf | celibataire_ou_divorce) * (ppe.eligi1 + 2 * max_(nbptr - 1, 0) * ppe.eligi3) \
            + maries_ou_pacses * (ppe.eligi2 + 2 * max_(nbptr - 2, 0) * ppe.eligi3)
        return period, (rfr * ppe_coef) <= (seuil * variator)


class regularisation_reduction_csg(DatedVariable):
    column = FloatCol
    entity = FoyerFiscal
    label = u"Régularisation complète réduction dégressive de CSG"

    @dated_function(start = date(2015, 1, 1))
    def function_2015__(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        reduction_csg = simulation.calculate('reduction_csg_foyer_fiscal', period)
        ppe_elig_bis = simulation.calculate('ppe_elig_bis', period)
        return period, not_(ppe_elig_bis) * (reduction_csg > 1)


class ayrault_muet(Reform):
    name = u'Amendement Ayrault-Muet au PLF2016'
    key = 'ayrault_muet'

    def apply(self):
        for variable in [
            reduction_csg,
            regularisation_reduction_csg,
            reduction_csg_foyer_fiscal,
            reduction_csg_nette,
            ppe_elig_bis,
            variator,
            ]:
            self.update_variable(variable)
        self.modify_legislation_json(modifier_function = ayrault_muet_modify_legislation_json)
