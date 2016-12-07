# -*- coding: utf-8 -*-

from __future__ import division

from numpy import maximum as max_
from openfisca_core import columns
from openfisca_core.reforms import Reform
from openfisca_core.variables import Variable

from .. import entities
from ..model.prelevements_obligatoires.impot_revenu import ir


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "Contribution execptionnelle sur les très hauts revenus d'activité",
        "children": {
            "seuil": {
                "@type": "Parameter",
                "description": "Seuil",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2012-01-01', 'stop': u'2013-12-31', 'value': 1000000}],
                },
            "taux": {
                "@type": "Parameter",
                "description": "Taux",
                "format": "rate",
                "unit": "currency",
                "values": [{'start': u'2012-01-01', 'stop': u'2013-12-31', 'value': .75}],
                },
            },
        }
    reference_legislation_json_copy['children']['cesthra'] = reform_legislation_subtree
    return reference_legislation_json_copy


class cesthra(Variable):
    column = columns.FloatCol
    entity = entities.FoyerFiscal
    label = u"Contribution exceptionnelle de solidarité sur les très hauts revenus d'activité"
    # PLF 2013 (rejeté) : 'taxe à 75%'

    def function(self, simulation, period):
        period = period.this_year
        salaire_imposable_holder = simulation.calculate("salaire_imposable", period)
        law_cesthra = simulation.legislation_at(period.start).cesthra
        salaire_imposable = self.split_by_roles(salaire_imposable_holder)

        cesthra = 0
        for rev in salaire_imposable.itervalues():
            cesthra += max_(rev - law_cesthra.seuil, 0) * law_cesthra.taux
        return period, cesthra


class irpp(Variable):
    label = u"Impôt sur le revenu des personnes physiques (réformée pour intégrer la cesthra)"

    def function(self, simulation, period):
        '''
        Montant après seuil de recouvrement (hors ppe)
        '''
        period = period.this_year
        iai = simulation.calculate('iai', period)
        credits_impot = simulation.calculate('credits_impot', period)
        cehr = simulation.calculate('cehr', period)
        cesthra = simulation.calculate('cesthra', period = period)
        P = simulation.legislation_at(period.start).impot_revenu.recouvrement

        pre_result = iai - credits_impot + cehr + cesthra
        return period, ((iai > P.seuil) *
            ((pre_result < P.min) * (pre_result > 0) * iai * 0 +
            ((pre_result <= 0) + (pre_result >= P.min)) * (- pre_result)) +
            (iai <= P.seuil) * ((pre_result < 0) * (-pre_result) +
            (pre_result >= 0) * 0 * iai))


class cesthra_invalidee(Reform):
    name = u"Contribution execptionnelle sur les très hauts revenus d'activité (invalidée par le CC)"

    def apply(self):
        self.add_variable(cesthra)
        self.update_variable(irpp)
        self.modify_legislation_json(modifier_function = modify_legislation_json)
