# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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


import copy
import datetime
import logging

import numpy as np
from openfisca_core import simulations


log = logging.getLogger(__name__)


def adapt_to_survey(tax_benefit_system_class):
    # Add survey specific column
    from openfisca_france_data.model.input_variables.survey_variables import column_by_name as survey_column_by_name
    from openfisca_france_data.model.model import prestation_by_name as survey_prestation_by_name
    column_by_name = copy.deepcopy(tax_benefit_system_class.column_by_name)
    prestation_by_name = copy.deepcopy(tax_benefit_system_class.prestation_by_name)
    column_by_name.update(survey_column_by_name)
    prestation_by_name.update(survey_prestation_by_name)
    del column_by_name['birth']
    prestation_by_name['agem'].formula_constructor = None
    prestation_by_name['agem'].function = None
    prestation_by_name['age'].formula_constructor = None
    prestation_by_name['age'].function = None
    tax_benefit_system_subclass = type(
        'tax_benefit_system_subclass',
        (tax_benefit_system_class,),
        {
            'column_by_name': column_by_name,
            'prestation_by_name': prestation_by_name,
            }
        )
    return tax_benefit_system_subclass


class SurveyScenario(object):
    compact_legislation = None
    inflators = None
    input_data_frame = None
    simulation = None
    tax_benefit_system = None
    tax_benefit_system_class = None
    year = None
    weight_column_name_by_entity_symbol = dict()

    def init_from_data_frame(self, input_data_frame = None, tax_benefit_system_class = None, year = None):
        assert input_data_frame is not None
        self.input_data_frame = input_data_frame
        assert tax_benefit_system_class is not None
        self.tax_benefit_system_class = tax_benefit_system_class
        tax_benefit_system_subclass = adapt_to_survey(tax_benefit_system_class)
        self.tax_benefit_system = tax_benefit_system_subclass()
        assert year is not None
        self.year = year
        self.weight_column_name_by_entity_symbol['men'] = 'wprm'
        self.weight_column_name_by_entity_symbol['fam'] = 'weight_fam'
        self.weight_column_name_by_entity_symbol['foy'] = 'weight_foy'
        self.weight_column_name_by_entity_symbol['ind'] = 'weight_ind'
        return self

    def new_simulation(self, debug = False, debug_all = False, trace = False):
        input_data_frame = self.input_data_frame

        simulation = simulations.Simulation(
            compact_legislation = self.compact_legislation,
            date = datetime.date(self.year, 1, 1),
            debug = debug,
            debug_all = debug_all,
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
                input_data_frame = input_data_frame.drop(column_name, axis = 1)  # waiting for the new pandas version to hit Travis repo, inplace = True)  # TODO: effet de bords ?
        for column_name in input_data_frame:
            if column_by_name[column_name].formula_constructor is not None:
                log.info('Column "{}" in survey set to be calculated, dropped from input table'.format(column_name))
                input_data_frame = input_data_frame.drop(column_name, axis = 1)  # , inplace = True)  # TODO: effet de bords ?

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


def new_simulation_from_array_dict(compact_legislation = None, debug = False, debug_all = False, array_dict = None,
                                   tax_benefit_system = None, trace = False, year = None):
    simulation = simulations.Simulation(
        compact_legislation = compact_legislation,
        date = datetime.date(year, 1, 1),
        debug = debug,
        debug_all = debug_all,
        tax_benefit_system = tax_benefit_system,
        trace = trace,
        )

    assert len(set([len(x) for x in array_dict.itervalues() if len(x) != 1])) == 1, 'Arrays do not have the same size'

    global_count = len(array_dict.values()[0])
    provided_keys = array_dict.keys()

    for role_var in ['quifam', 'quifoy', 'quimen']:
        if role_var not in provided_keys:
            array_dict[role_var] = np.zeros(global_count, dtype = int)

    for id_var in ['idfam', 'idfoy', 'idmen', 'noi']:
        if id_var not in provided_keys:
            array_dict[id_var] = np.arange(global_count, dtype = int)

    column_by_name = tax_benefit_system.column_by_name
    for column_name, array in array_dict.iteritems():
        assert column_name in column_by_name, column_name

    entity_by_key_plural = simulation.entity_by_key_plural

    familles = entity_by_key_plural[u'familles']
    familles.count = familles.step_size = familles_step_size = (array_dict['quifam'] == 0).sum()
    foyers_fiscaux = entity_by_key_plural[u'foyers_fiscaux']
    foyers_fiscaux.count = foyers_fiscaux.step_size = foyers_fiscaux_step_size = (array_dict['quifoy'] == 0).sum()
    individus = entity_by_key_plural[u'individus']
    individus.count = individus.step_size = individus_step_size = global_count
    menages = entity_by_key_plural[u'menages']
    menages.count = menages.step_size = menages_step_size = (array_dict['quimen'] == 0).sum()

    assert 'idfam' in array_dict.keys()
    assert 'idfoy' in array_dict.keys()
    assert 'idmen' in array_dict.keys()
    assert 'noi' in array_dict.keys()
    assert 'quifam' in array_dict.keys()
    assert 'quifoy' in array_dict.keys()
    assert 'quimen' in array_dict.keys()

    familles.roles_count = array_dict['quifam'].max() + 1
    menages.roles_count = array_dict['quimen'].max() + 1
    foyers_fiscaux.roles_count = array_dict['quifoy'].max() + 1

    for column_name, column_array in array_dict.iteritems():
        holder = simulation.get_or_new_holder(column_name)
        entity = holder.entity
        if holder.entity.is_persons_entity:
            array = column_array
        else:
            array = column_array[array_dict['qui' + entity.symbol].values == 0]
        assert array.size == entity.count, 'Bad size for {}: {} instead of {}'.format(column_name, array.size,
            entity.count)
        holder.array = np.array(array, dtype = holder.column.dtype)

    return simulation

