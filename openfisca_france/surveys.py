# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


# import copy
import logging

import numpy as np
from openfisca_core import periods, simulations


log = logging.getLogger(__name__)


class SurveyScenario(object):
    inflators = None
    input_data_frame = None
    legislation_json = None
    simulation = None
    tax_benefit_system = None
    tax_benefit_system_class = None
    year = None
    weight_column_name_by_entity_symbol = dict()

    def init_from_data_frame(self, input_data_frame = None, tax_benefit_system = None, year = None):
        assert input_data_frame is not None
        self.input_data_frame = input_data_frame
        assert tax_benefit_system is not None
        self.tax_benefit_system = tax_benefit_system
        survey_tax_benefit_system = adapt_to_survey(tax_benefit_system)
        self.tax_benefit_system = survey_tax_benefit_system
        assert year is not None
        self.year = year
        self.weight_column_name_by_entity_symbol['men'] = 'wprm'
        self.weight_column_name_by_entity_symbol['fam'] = 'weight_fam'
        self.weight_column_name_by_entity_symbol['foy'] = 'weight_foy'
        self.weight_column_name_by_entity_symbol['ind'] = 'weight_ind'
        return self

    def new_simulation(self, debug = False, debug_all = False, trace = False):
        input_data_frame = self.input_data_frame
        # TODO: Pass year to this method, not init_from_data_frame
        simulation = simulations.Simulation(
            debug = debug,
            debug_all = debug_all,
            period = periods.period(self.year),
            tax_benefit_system = self.tax_benefit_system,
            trace = trace,
            )

        symbols_other_than_ind = [entity.symbol for entity in simulation.entity_by_key_singular.values()]
        symbols_other_than_ind.remove('ind')
        id_variables = ["id{}".format(symbol) for symbol in symbols_other_than_ind]
        role_variables = ["qui{}".format(symbol) for symbol in symbols_other_than_ind]
        for id_variable in id_variables + role_variables:
            assert id_variable in self.input_data_frame.columns

        column_by_name = self.tax_benefit_system.column_by_name
        for column_name in input_data_frame:
            if column_name not in column_by_name:
                log.info('Unknown column "{}" in survey, dropped from input table'.format(column_name))
                # waiting for the new pandas version to hit Travis repo
                input_data_frame = input_data_frame.drop(column_name, axis = 1)
                # , inplace = True)  # TODO: effet de bords ?
        for column_name in input_data_frame:
            if column_by_name[column_name].formula_class is not None:
                log.info('Column "{}" in survey set to be calculated, dropped from input table'.format(column_name))
                input_data_frame = input_data_frame.drop(column_name, axis = 1)
                # , inplace = True)  # TODO: effet de bords ?

        for entity in simulation.entity_by_key_singular.values():
            if entity.is_persons_entity:
                entity.count = entity.step_size = len(input_data_frame)
            else:
                entity.count = entity.step_size = (input_data_frame["qui{}".format(entity.symbol)] == 0).sum()
                entity.roles_count = input_data_frame["qui{}".format(entity.symbol)].max() + 1
#       TODO: Create a validation/conversion step
#       TODO: introduce an assert when loading in place of astype
        for column_name, column_series in input_data_frame.iteritems():
            holder = simulation.get_or_new_holder(column_name)
            entity = holder.entity
            if entity.is_persons_entity:
                array = column_series.values.astype(holder.column.dtype)
            else:
                array = column_series.values[input_data_frame['qui' + entity.symbol].values == 0].astype(
                    holder.column.dtype)
            assert array.size == entity.count, 'Bad size for {}: {} instead of {}'.format(
                column_name,
                array.size,
                entity.count)
            holder.array = np.array(array, dtype = holder.column.dtype)

        self.simulation = simulation
        return simulation

    def inflate(self, inflators = None):
        if inflators is not None:
            self.inflators = inflators
        assert self.inflators is not None
        assert self.simulation is not None
        simulation = self.simulation
        tax_benefit_system = self.tax_benefit_system
        for column_name, inflator in inflators:
            assert column_name in tax_benefit_system.column_by_name
            holder = simulation.get_or_new_holder(column_name)
            holder.array = inflator * holder.array


def adapt_to_survey(tax_benefit_system):

    survey_entity_class_by_key_plural = tax_benefit_system.entity_class_by_key_plural.copy()

    individus_class = survey_entity_class_by_key_plural['individus']
    familles_class = survey_entity_class_by_key_plural['familles']
    foyers_class = survey_entity_class_by_key_plural['foyers_fiscaux']
    menages_class = survey_entity_class_by_key_plural['menages']

    survey_individus_column_by_name = individus_class.column_by_name.copy()
    survey_familles_column_by_name = familles_class.column_by_name.copy()
    survey_foyers_column_by_name = foyers_class.column_by_name.copy()
    survey_menages_column_by_name = menages_class.column_by_name.copy()

    del survey_individus_column_by_name['birth']
    survey_individus_column_by_name['age_en_mois'].formula_class = None
    survey_individus_column_by_name['age'].formula_class = None

    class SurveyIndividus(individus_class):
        column_by_name = survey_individus_column_by_name

    class SurveyFamilles(familles_class):
        column_by_name = survey_familles_column_by_name

    class SurveyFoyers(foyers_class):
        column_by_name = survey_foyers_column_by_name

    class SurveyMenages(menages_class):
        column_by_name = survey_menages_column_by_name

    survey_entity_class_by_key_plural['individus'] = SurveyIndividus
    survey_entity_class_by_key_plural['familles'] = SurveyFamilles
    survey_entity_class_by_key_plural['foyers_fiscaux'] = SurveyFoyers
    survey_entity_class_by_key_plural['menages'] = SurveyMenages

    from openfisca_france_data.model.input_variables.survey_variables import add_survey_columns_to_entities
    add_survey_columns_to_entities(survey_entity_class_by_key_plural)

    from openfisca_france_data.model.model import add_survey_formulas_to_entities
    add_survey_formulas_to_entities(survey_entity_class_by_key_plural)

    from openfisca_core import reforms
    survey_tax_benefit_system = reforms.make_reform(
        # entity_class_by_key_plural = survey_entity_class_by_key_plural,
        name = u'openfisca-france-survey',
        # new_formulas = (),
        reference = tax_benefit_system,
        )
    return survey_tax_benefit_system


def new_simulation_from_array_dict(array_dict = None, debug = False, debug_all = False, legislation_json = None,
        tax_benefit_system = None, trace = False, year = None):
    simulation = simulations.Simulation(
        debug = debug,
        debug_all = debug_all,
        legislation_json = legislation_json,
        period = periods.period(year),
        tax_benefit_system = tax_benefit_system,
        trace = trace,
        )

    assert len(set(len(x) for x in array_dict.itervalues() if len(x) != 1)) == 1, 'Arrays do not have the same size'
    global_count = len(array_dict.values()[0])

    for role_var in ['quifam', 'quifoy', 'quimen']:
        if role_var not in array_dict:
            array_dict[role_var] = np.zeros(global_count, dtype = int)

    for id_var in ['idfam', 'idfoy', 'idmen']:
        if id_var not in array_dict:
            array_dict[id_var] = np.arange(global_count, dtype = int)

    column_by_name = tax_benefit_system.column_by_name
    for column_name, array in array_dict.iteritems():
        assert column_name in column_by_name, column_name

    entity_by_key_plural = simulation.entity_by_key_plural

    familles = entity_by_key_plural[u'familles']
    familles.count = familles.step_size = (array_dict['quifam'] == 0).sum()
    foyers_fiscaux = entity_by_key_plural[u'foyers_fiscaux']
    foyers_fiscaux.count = foyers_fiscaux.step_size = (array_dict['quifoy'] == 0).sum()
    individus = entity_by_key_plural[u'individus']
    individus.count = individus.step_size = global_count
    menages = entity_by_key_plural[u'menages']
    menages.count = menages.step_size = (array_dict['quimen'] == 0).sum()

    assert 'idfam' in array_dict.keys()
    assert 'idfoy' in array_dict.keys()
    assert 'idmen' in array_dict.keys()
    assert 'quifam' in array_dict.keys()
    assert 'quifoy' in array_dict.keys()
    assert 'quimen' in array_dict.keys()

    familles.roles_count = array_dict['quifam'].max() + 1
    menages.roles_count = array_dict['quimen'].max() + 1
    foyers_fiscaux.roles_count = array_dict['quifoy'].max() + 1

    for column_name, column_array in array_dict.iteritems():
        holder = simulation.get_or_new_holder(column_name)
        entity = holder.entity
        if entity.is_persons_entity:
            array = column_array
        else:
            array = column_array[array_dict['qui' + entity.symbol].values == 0]
        assert array.size == entity.count, 'Bad size for {}: {} instead of {}'.format(
            column_name,
            array.size,
            entity.count
            )
        holder.array = np.array(array, dtype = holder.column.dtype)

    return simulation
