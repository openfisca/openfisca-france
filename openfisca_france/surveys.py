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


import datetime

import numpy as np
from openfisca_core import simulations


def new_simulation_from_survey_data_frame(compact_legislation = None, debug = False, debug_all = False, survey = None,
        tax_benefit_system = None, year = None):
    assert 'idfam' in survey.columns
    assert 'idfoy' in survey.columns
    assert 'idmen' in survey.columns
    assert 'noi' in survey.columns
    assert 'quifam' in survey.columns
    assert 'quifoy' in survey.columns
    assert 'quimen' in survey.columns

    column_by_name = tax_benefit_system.column_by_name
    for column_name in survey:
        assert column_name in column_by_name, 'Unknown column "{}" in survey'.format(column_name)

    simulation = simulations.Simulation(
        compact_legislation = compact_legislation,
        date = datetime.date(year, 5, 1),
        debug = debug,
        debug_all = debug_all,
        tax_benefit_system = tax_benefit_system,
        )
    entity_by_key_plural = simulation.entity_by_key_plural

    familles = entity_by_key_plural[u'familles']
    familles.count = familles.step_size = familles_step_size = (survey.quifam == 0).sum()
    familles.roles_count = survey['quifam'].max() + 1
    foyers_fiscaux = entity_by_key_plural[u'foyers_fiscaux']
    foyers_fiscaux.count = foyers_fiscaux.step_size = foyers_fiscaux_step_size = (survey.quifoy == 0).sum()
    foyers_fiscaux.roles_count = survey['quifoy'].max() + 1
    individus = entity_by_key_plural[u'individus']
    individus.count = individus.step_size = individus_step_size = len(survey)
    menages = entity_by_key_plural[u'menages']
    menages.count = menages.step_size = menages_step_size = (survey.quimen == 0).sum()
    menages.roles_count = survey['quimen'].max() + 1

    for column_name, column_series in survey.iteritems():
        holder = simulation.get_or_new_holder(column_name)
        entity = holder.entity
        if holder.entity.is_persons_entity:
            array = column_series.values
        else:
            array = column_series.values[survey['qui' + entity.symbol].values == 0]
        assert array.size == entity.count, 'Bad size for {}: {} instead of {}'.format(column_name, array.size,
            entity.count)
        holder.array = np.array(array, dtype = holder.column.dtype)

    return simulation


def new_simulation_from_array_dict(compact_legislation = None, debug = False, debug_all = False, array_dict = None,
        tax_benefit_system = None, year = None):
    simulation = simulations.Simulation(
        compact_legislation = compact_legislation,
        date = datetime.date(year, 1, 1),
        debug = debug,
        debug_all = debug_all,
        tax_benefit_system = tax_benefit_system,
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

