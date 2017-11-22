# -*- coding: utf-8 -*-

from __future__ import division

import os

from openfisca_france.model.base import *

from .. import entities
from ..model.prelevements_obligatoires.impot_revenu import ir


dir_path = os.path.join(os.path.dirname(__file__), 'parameters')


def modify_parameters(parameters):
    file_path = os.path.join(dir_path, 'cesthra_invalidite.yaml')
    reform_parameters_subtree = load_parameter_file(name='cesthra', file_path=file_path)
    parameters.add_child('cesthra', reform_parameters_subtree)
    return parameters


class cesthra(Variable):
    value_type = float
    entity = entities.FoyerFiscal
    label = u"Contribution exceptionnelle de solidarité sur les très hauts revenus d'activité"
    definition_period = YEAR
    # PLF 2013 (rejeté) : 'taxe à 75%'

    def formula(self, simulation, period):
        salaire_imposable_holder = simulation.calculate_add("salaire_imposable", period)
        law_cesthra = simulation.parameters_at(period.start).cesthra
        salaire_imposable = self.split_by_roles(salaire_imposable_holder)

        cesthra = 0
        for rev in salaire_imposable.itervalues():
            cesthra += max_(rev - law_cesthra.seuil, 0) * law_cesthra.taux
        return cesthra


class irpp(Variable):
    label = u"Impôt sur le revenu des personnes physiques (réformée pour intégrer la cesthra)"
    definition_period = YEAR

    def formula(self, simulation, period):
        '''
        Montant après seuil de recouvrement (hors ppe)
        '''
        iai = simulation.calculate('iai', period)
        credits_impot = simulation.calculate('credits_impot', period)
        cehr = simulation.calculate('cehr', period)
        cesthra = simulation.calculate('cesthra', period = period)
        P = simulation.parameters_at(period.start).impot_revenu.recouvrement

        pre_result = iai - credits_impot + cehr + cesthra
        return ((iai > P.seuil) *
            ((pre_result < P.min) * (pre_result > 0) * iai * 0 +
            ((pre_result <= 0) + (pre_result >= P.min)) * (- pre_result)) +
            (iai <= P.seuil) * ((pre_result < 0) * (-pre_result) +
            (pre_result >= 0) * 0 * iai))


class cesthra_invalidee(Reform):
    name = u"Contribution execptionnelle sur les très hauts revenus d'activité (invalidée par le CC)"

    def apply(self):
        self.add_variable(cesthra)
        self.update_variable(irpp)
        self.modify_parameters(modifier_function = modify_parameters)
