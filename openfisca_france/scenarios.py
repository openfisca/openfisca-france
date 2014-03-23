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


import collections
import datetime
import itertools
import json
import logging
import os
import time
import urllib2
import uuid

import numpy as np
from openfisca_core import legislations, simulations

from . import conv, entities


log = logging.getLogger(__name__)
N_ = lambda message: message


class Scenario(object):
    axes = None
    compact_legislation = None
    tax_benefit_system = None
    test_case = None
    year = None

    def init_single_entity(self, axes = None, enfants = None, famille = None, foyer_fiscal = None, menage = None,
            parent1 = None, parent2 = None, year = None):
        if enfants is None:
            enfants = []
        assert parent1 is not None
        famille = famille.copy() if famille is not None else {}
        foyer_fiscal = foyer_fiscal.copy() if foyer_fiscal is not None else {}
        individus = []
        menage = menage.copy() if menage is not None else {}
        for index, individu in enumerate([parent1, parent2] + (enfants or [])):
            if individu is None:
                continue
            id = individu.get('id')
            if id is None:
                individu = individu.copy()
                individu['id'] = id = 'ind{}'.format(index)
            individus.append(individu)
            if index <= 1 :
                famille.setdefault('parents', []).append(id)
                foyer_fiscal.setdefault('declarants', []).append(id)
                if index == 0:
                    menage['personne_de_reference'] = id
                else:
                    menage['conjoint'] = id
            else:
                famille.setdefault('enfants', []).append(id)
                foyer_fiscal.setdefault('personnes_a_charge', []).append(id)
                menage.setdefault('enfants', []).append(id)
        conv.check(self.make_json_or_python_to_attributes())(dict(
            axes = axes,
            test_case = dict(
                familles = [famille],
                foyers_fiscaux = [foyer_fiscal],
                individus = individus,
                menages = [menage],
                ),
            year = year,
            ))
        return self

    def json_or_python_to_test_case(self, value, state = None):
        if value is None:
            return value, None
        if state is None:
            state = conv.default_state

        column_by_name = self.tax_benefit_system.column_by_name

        # First validation and conversion step
        test_case, error = conv.pipe(
            conv.test_isinstance(dict),
            conv.struct(
                dict(
                    familles = conv.pipe(
                        conv.condition(
                            conv.test_isinstance(list),
                            conv.pipe(
                                conv.uniform_sequence(
                                    conv.test_isinstance(dict),
                                    drop_none_items = True,
                                    ),
                                conv.function(lambda values: collections.OrderedDict(
                                    (value.pop('id', index), value)
                                    for index, value in enumerate(values)
                                    )),
                                ),
                            ),
                        conv.test_isinstance(dict),
                        conv.uniform_mapping(
                            conv.pipe(
                                conv.test_isinstance((basestring, int)),
                                conv.not_none,
                                ),
                            conv.pipe(
                                conv.test_isinstance(dict),
                                conv.struct(
                                    dict(itertools.chain(
                                        dict(
                                            enfants = conv.pipe(
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items = True,
                                                    ),
                                                conv.default([]),
                                                ),
                                            parents = conv.pipe(
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items = True,
                                                    ),
                                                conv.empty_to_none,
                                                conv.not_none,
                                                conv.test(lambda parents: len(parents) <= 2,
                                                    error = N_(u'A "famille" must have at most 2 "parents"'))
                                                ),
                                            ).iteritems(),
                                        (
                                            (column.name, column.json_to_python)
                                            for column in column_by_name.itervalues()
                                            if column.entity == 'fam'
                                            ),
                                        )),
                                    drop_none_values = True,
                                    ),
                                ),
                            drop_none_values = True,
                            ),
                        conv.empty_to_none,
                        conv.not_none,
                        ),
                    foyers_fiscaux = conv.pipe(
                        conv.condition(
                            conv.test_isinstance(list),
                            conv.pipe(
                                conv.uniform_sequence(
                                    conv.test_isinstance(dict),
                                    drop_none_items = True,
                                    ),
                                conv.function(lambda values: collections.OrderedDict(
                                    (value.pop('id', index), value)
                                    for index, value in enumerate(values)
                                    )),
                                ),
                            ),
                        conv.test_isinstance(dict),
                        conv.uniform_mapping(
                            conv.pipe(
                                conv.test_isinstance((basestring, int)),
                                conv.not_none,
                                ),
                            conv.pipe(
                                conv.test_isinstance(dict),
                                conv.struct(
                                    dict(itertools.chain(
                                        dict(
                                            declarants = conv.pipe(
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items = True,
                                                    ),
                                                conv.empty_to_none,
                                                conv.not_none,
                                                conv.test(lambda declarants: len(declarants) <= 2,
                                                    error = N_(u'A "foyer_fiscal" must have at most 2 "declarants"'
                                                    ))
                                                ),
                                            personnes_a_charge = conv.pipe(
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items = True,
                                                    ),
                                                conv.default([]),
                                                ),
                                            ).iteritems(),
                                        (
                                            (column.name, column.json_to_python)
                                            for column in column_by_name.itervalues()
                                            if column.entity == 'foy'
                                            ),
                                        )),
                                    drop_none_values = True,
                                    ),
                                ),
                            drop_none_values = True,
                            ),
                        conv.empty_to_none,
                        conv.not_none,
                        ),
                    individus = conv.pipe(
                        conv.condition(
                            conv.test_isinstance(list),
                            conv.pipe(
                                conv.uniform_sequence(
                                    conv.test_isinstance(dict),
                                    drop_none_items = True,
                                    ),
                                conv.function(lambda values: collections.OrderedDict(
                                    (value.pop('id', index), value)
                                    for index, value in enumerate(values)
                                    )),
                                ),
                            ),
                        conv.test_isinstance(dict),
                        conv.uniform_mapping(
                            conv.pipe(
                                conv.test_isinstance((basestring, int)),
                                conv.not_none,
                                ),
                            conv.pipe(
                                conv.test_isinstance(dict),
                                conv.struct(
                                    dict(
                                        (column.name, column.json_to_python)
                                        for column in column_by_name.itervalues()
                                        if column.entity == 'ind' and column.name not in (
                                            'idfam', 'idfoy', 'idmen', 'quifam', 'quifoy', 'quimen')
                                        ),
                                    drop_none_values = True,
                                    ),
                                ),
                            drop_none_values = True,
                            ),
                        conv.empty_to_none,
                        conv.not_none,
                        ),
                    menages = conv.pipe(
                        conv.condition(
                            conv.test_isinstance(list),
                            conv.pipe(
                                conv.uniform_sequence(
                                    conv.test_isinstance(dict),
                                    drop_none_items = True,
                                    ),
                                conv.function(lambda values: collections.OrderedDict(
                                    (value.pop('id', index), value)
                                    for index, value in enumerate(values)
                                    )),
                                ),
                            ),
                        conv.test_isinstance(dict),
                        conv.uniform_mapping(
                            conv.pipe(
                                conv.test_isinstance((basestring, int)),
                                conv.not_none,
                                ),
                            conv.pipe(
                                conv.test_isinstance(dict),
                                conv.struct(
                                    dict(itertools.chain(
                                        dict(
                                            autres = conv.pipe(
                                                # personnes ayant un lien autre avec la personne de référence
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items = True,
                                                    ),
                                                conv.default([]),
                                                ),
                                            conjoint = conv.test_isinstance((basestring, int)),
                                                # conjoint de la personne de référence
                                            enfants = conv.pipe(
                                                # enfants de la personne de référence ou de son conjoint
                                                conv.test_isinstance(list),
                                                conv.uniform_sequence(
                                                    conv.test_isinstance((basestring, int)),
                                                    drop_none_items = True,
                                                    ),
                                                conv.default([]),
                                                ),
                                            personne_de_reference = conv.pipe(
                                                conv.test_isinstance((basestring, int)),
                                                conv.not_none,
                                                ),
                                            ).iteritems(),
                                        (
                                            (column.name, column.json_to_python)
                                            for column in column_by_name.itervalues()
                                            if column.entity == 'men'
                                            ),
                                        )),
                                    drop_none_values = True,
                                    ),
                                ),
                            drop_none_values = True,
                            ),
                        conv.empty_to_none,
                        conv.not_none,
                        ),
                    ),
                ),
            )(value, state = state)
        if error is not None:
            return test_case, error

        # Second validation step
        familles_individus_id = set(test_case['individus'].iterkeys())
        foyers_fiscaux_individus_id = set(test_case['individus'].iterkeys())
        menages_individus_id = set(test_case['individus'].iterkeys())
        test_case, error = conv.struct(
            dict(
                familles = conv.uniform_mapping(
                    conv.noop,
                    conv.struct(
                        dict(
                            enfants = conv.uniform_sequence(conv.test_in_pop(familles_individus_id)),
                            parents = conv.uniform_sequence(conv.test_in_pop(familles_individus_id)),
                            ),
                        default = conv.noop,
                        ),
                    ),
                foyers_fiscaux = conv.uniform_mapping(
                    conv.noop,
                    conv.struct(
                        dict(
                            declarants = conv.uniform_sequence(conv.test_in_pop(foyers_fiscaux_individus_id)),
                            personnes_a_charge = conv.uniform_sequence(conv.test_in_pop(foyers_fiscaux_individus_id)),
                            ),
                        default = conv.noop,
                        ),
                    ),
                menages = conv.uniform_mapping(
                    conv.noop,
                    conv.struct(
                        dict(
                            autres = conv.uniform_sequence(conv.test_in_pop(menages_individus_id)),
                            conjoint = conv.test_in_pop(menages_individus_id),
                            enfants = conv.uniform_sequence(conv.test_in_pop(menages_individus_id)),
                            personne_de_reference = conv.test_in_pop(menages_individus_id),
                            ),
                        default = conv.noop,
                        ),
                    ),
                ),
            default = conv.noop,
            )(test_case, state = state)

        remaining_individus_id = familles_individus_id.union(foyers_fiscaux_individus_id, menages_individus_id)
        if remaining_individus_id:
            if error is None:
                error = {}
            for individu_id in remaining_individus_id:
                error.setdefault('individus', {})[individu_id] = state._(u"Individual is missing from {}").format(
                    u' & '.join(
                        word
                        for word in [
                            u'familles' if individu_id not in familles_individus_id else None,
                            u'foyers_fiscaux' if individu_id not in foyers_fiscaux_individus_id else None,
                            u'menages' if individu_id not in menages_individus_id else None,
                            ]
                        if word is not None
                        ))

        return test_case, error

    def make_json_or_python_to_attributes(self, cache_dir = None):
        column_by_name = self.tax_benefit_system.column_by_name

        def json_or_python_to_attributes(value, state = None):
            if value is None:
                return value, None
            if state is None:
                state = conv.default_state

            # First validation and conversion step
            data, error = conv.pipe(
                conv.test_isinstance(dict),
                conv.struct(
                    dict(
                        axes = conv.pipe(
                            conv.test_isinstance(list),
                            conv.uniform_sequence(
                                conv.pipe(
                                    conv.test_isinstance(dict),
                                    conv.struct(
                                        dict(
                                            count = conv.pipe(
                                                conv.test_isinstance(int),
                                                conv.test_greater_or_equal(1),
                                                conv.not_none,
                                                ),
                                            index = conv.pipe(
                                                conv.test_isinstance(int),
                                                conv.test_greater_or_equal(0),
                                                conv.default(0),
                                                ),
                                            max = conv.pipe(
                                                conv.test_isinstance((float, int)),
                                                conv.not_none,
                                                ),
                                            min = conv.pipe(
                                                conv.test_isinstance((float, int)),
                                                conv.not_none,
                                                ),
                                            name = conv.pipe(
                                                conv.test_isinstance(basestring),
                                                conv.test_in(column_by_name),
                                                conv.test(lambda column_name: column_by_name[column_name].dtype in (
                                                    np.float32, np.int16, np.int32),
                                                    error = N_(u'Invalid type for axe: integer or float expected')),
                                                conv.not_none,
                                                ),
                                            ),
                                        ),
                                    ),
                                drop_none_items = True,
                                ),
                            conv.empty_to_none,
                            ),
                        legislation_url = conv.pipe(
                            conv.test_isinstance(basestring),
                            conv.make_input_to_url(error_if_fragment = True, full = True, schemes = ('http', 'https')),
                            ),
                        test_case = conv.pipe(
                            self.json_or_python_to_test_case,
                            conv.not_none,
                            ),
                        year = conv.pipe(
                            conv.test_isinstance(int),
                            conv.test_greater_or_equal(1900), # TODO: Check that year is valid in params.
                            conv.not_none,
                            ),
                        ),
                    ),
                )(value, state = state)
            if error is not None:
                return data, error

            errors = {}

            if data['axes'] is not None:
                for axis_index, axis in enumerate(data['axes']):
                    if axis['min'] >= axis['max']:
                        errors.setdefault('axes', {}).setdefault(axis_index, {})['max'] = state._(
                            u"Max value must be greater than min value")
                    column = column_by_name[axis['name']]
                    entity_class = entities.entity_class_by_symbol[column.entity]
                    if axis['index'] >= len(data['test_case'][entity_class.key_plural]):
                        errors.setdefault('axes', {}).setdefault(axis_index, {})['index'] = state._(
                            u"Index must be lower than {}").format(len(data['test_case'][entity_class.key_plural]))

            famille_by_id = data['test_case']['familles']
            parents_id = set(
                parent_id
                for famille in data['test_case']['familles'].itervalues()
                for parent_id in famille['parents']
                )
            individu_by_id = data['test_case']['individus']
            data, errors = conv.struct(
                dict(
                     test_case = conv.struct(
                        dict(
                            foyers_fiscaux = conv.uniform_mapping(
                                conv.noop,
                                conv.struct(
                                    dict(
                                        declarants = conv.uniform_sequence(conv.pipe(
                                            conv.test(lambda individu_id:
                                                individu_by_id[individu_id].get('birth') is None
                                                or data['year'] - individu_by_id[individu_id]['birth'].year >= 18,
                                                error = u"Un déclarant d'un foyer fiscal doit être agé d'au moins 18"
                                                    u" ans",
                                                ),
                                            conv.test(lambda individu_id:
                                                individu_by_id[individu_id].get('age') is None
                                                or individu_by_id[individu_id]['age'] >= 18,
                                                error = u"Un déclarant d'un foyer fiscal doit être agé d'au moins 18"
                                                    u" ans",
                                                ),
                                            conv.test(lambda individu_id:
                                                individu_by_id[individu_id].get('agem') is None
                                                or individu_by_id[individu_id]['agem'] >= 18 * 12,
                                                error = u"Un déclarant d'un foyer fiscal doit être agé d'au moins 18"
                                                    u" ans",
                                                ),
                                            conv.test(lambda individu_id: individu_id in parents_id,
                                                error = u"Un déclarant ou un conjoint sur la feuille d'impôt, doit être"
                                                    u"un parent dans sa famille",
                                                ),
                                            )),
                                        personnes_a_charge = conv.uniform_sequence(conv.pipe(
                                            conv.test(lambda individu_id: individu_by_id[individu_id].get('inv', False)
                                                or individu_by_id[individu_id].get('birth') is None
                                                or data['year'] - individu_by_id[individu_id]['birth'].year <= 25,
                                                error = u"Une personne à charge d'un foyer fiscal doit avoir moins de"
                                                    u" 25 ans ou être invalide",
                                                ),
                                            conv.test(lambda individu_id: individu_by_id[individu_id].get('inv', False)
                                                or individu_by_id[individu_id].get('age') is None
                                                or individu_by_id[individu_id]['age'] <= 25,
                                                error = u"Une personne à charge d'un foyer fiscal doit avoir moins de"
                                                    u" 25 ans ou être invalide",
                                                ),
                                            conv.test(lambda individu_id: individu_by_id[individu_id].get('inv', False)
                                                or individu_by_id[individu_id].get('agem') is None
                                                or individu_by_id[individu_id]['agem'] <= 25 * 12,
                                                error = u"Une personne à charge d'un foyer fiscal doit avoir moins de"
                                                    u" 25 ans ou être invalide",
                                                ),
                                            )),
                                        ),
                                    default = conv.noop,
                                    ),
                                ),
                            individus = conv.uniform_mapping(
                                conv.noop,
                                conv.struct(
                                    dict(
                                        birth = conv.test(lambda birth: data['year'] - birth.year >= 0,
                                            error = u"L'individu doit être né au plus tard l'année de la simulation",
                                            ),
                                        ),
                                    default = conv.noop,
                                    drop_none_values = 'missing',
                                    ),
                                ),
                            ),
                        default = conv.noop,
                        ),
                    ),
                default = conv.noop,
                )(data, state = state)

            if errors:
                return data, errors

            if data['legislation_url'] is None:
                compact_legislation = None
            else:
                legislation_json = None
                if cache_dir is not None:
                    legislation_uuid_hex = uuid.uuid5(uuid.NAMESPACE_URL, data['legislation_url'].encode('utf-8')).hex
                    legislation_dir = os.path.join(cache_dir, 'legislations', legislation_uuid_hex[:2])
                    legislation_filename = '{}.json'.format(legislation_uuid_hex[2:])
                    legislation_file_path = os.path.join(legislation_dir, legislation_filename)
                    if os.path.exists(legislation_file_path) \
                            and os.path.getmtime(legislation_file_path) > time.time() - 900: # 15 minutes
                        with open(legislation_file_path) as legislation_file:
                            try:
                                legislation_json = json.load(legislation_file,
                                    object_pairs_hook = collections.OrderedDict)
                            except ValueError:
                                log.exception('Error while reading legislation JSON file: {}'.format(
                                    legislation_file_path))
                if legislation_json is None:
                    request = urllib2.Request(data['legislation_url'], headers = {
                        'User-Agent': 'OpenFisca-Web-API',
                        })
                    try:
                        response = urllib2.urlopen(request)
                    except urllib2.HTTPError:
                        return data, dict(legislation_url = state._(u'HTTP Error while retrieving legislation JSON'))
                    except urllib2.URLError:
                        return data, dict(legislation_url = state._(u'Error while retrieving legislation JSON'))
                    legislation_json, error = conv.pipe(
                        conv.make_input_to_json(object_pairs_hook = collections.OrderedDict),
                        legislations.validate_any_legislation_json,
                        conv.not_none,
                        )(response.read(), state = state)
                    if error is not None:
                        return data, dict(legislation_url = error)
                    if cache_dir is not None:
                        if not os.path.exists(legislation_dir):
                            os.makedirs(legislation_dir)
                        with open(legislation_file_path, 'w') as legislation_file:
                            legislation_file.write(unicode(json.dumps(legislation_json, encoding = 'utf-8',
                                ensure_ascii = False, indent = 2)).encode('utf-8'))
                datesim = datetime.date(data['year'], 1, 1)
                if legislation_json.get('datesim') is None:
                    dated_legislation_json = legislations.generate_dated_legislation_json(legislation_json, datesim)
                else:
                    dated_legislation_json = legislation_json
                    legislation_json = None
                compact_legislation = legislations.compact_dated_node_json(dated_legislation_json)
                if self.tax_benefit_system.preprocess_legislation_parameters is not None:
                    self.tax_benefit_system.preprocess_legislation_parameters(compact_legislation)

            self.axes = data['axes']
            self.compact_legislation = compact_legislation
            self.test_case = data['test_case']
            self.year = data['year']
            return self, None

        return json_or_python_to_attributes

    @classmethod
    def make_json_to_instance(cls, cache_dir = None, tax_benefit_system = None):
        def json_to_instance(value, state = None):
            if value is None:
                return None, None
            self = cls()
            self.tax_benefit_system = tax_benefit_system
            return self.make_json_or_python_to_attributes(cache_dir = cache_dir)(value = value,
                state = state or conv.default_state)

        return json_to_instance

    def new_simulation(self, debug = False):
        simulation = simulations.Simulation(
            compact_legislation = self.compact_legislation,
            date = datetime.date(self.year, 1, 1),
            debug = debug,
            tax_benefit_system = self.tax_benefit_system,
            )

        column_by_name = self.tax_benefit_system.column_by_name
        entity_by_key_plural = simulation.entity_by_key_plural
        steps_count = 1
        if self.axes is not None:
            for axis in self.axes:
                steps_count *= axis['count']
        simulation.steps_count = steps_count
        test_case = self.test_case

        familles = entity_by_key_plural[u'familles']
        familles.step_size = familles_step_size = len(test_case[u'familles'])
        familles.count = steps_count * familles_step_size
        foyers_fiscaux = entity_by_key_plural[u'foyers_fiscaux']
        foyers_fiscaux.step_size = foyers_fiscaux_step_size = len(test_case[u'foyers_fiscaux'])
        foyers_fiscaux.count = steps_count * foyers_fiscaux_step_size
        individus = entity_by_key_plural[u'individus']
        individus.step_size = individus_step_size = len(test_case[u'individus'])
        individus.count = steps_count * individus_step_size
        menages = entity_by_key_plural[u'menages']
        menages.step_size = menages_step_size = len(test_case[u'menages'])
        menages.count = steps_count * menages_step_size

        individu_index_by_id = dict(
            (individu_id, individu_index)
            for individu_index, individu_id in enumerate(test_case[u'individus'].iterkeys())
            )
#        individus.new_holder('id').array = np.array(
#            [
#                individu_id + (u'-{}'.format(step_index) if step_index > 0 else u'')
#                for step_index in range(steps_count)
#                for individu_index, individu_id in enumerate(test_case[u'individus'].iterkeys())
#                ],
#            dtype = object)
        #
        individus.new_holder('idfam').array = idfam_array = np.empty(steps_count * individus_step_size,
            dtype = column_by_name['idfam'].dtype)  # famille_index
        individus.new_holder('quifam').array = quifam_array = np.empty(steps_count * individus_step_size,
            dtype = column_by_name['quifam'].dtype)  # famille_role
        familles_roles_count = 0
        for famille_index, famille in enumerate(test_case[u'familles'].itervalues()):
            parents_id = famille.pop(u'parents')
            enfants_id = famille.pop(u'enfants')
            for step_index in range(steps_count):
                individu_index = individu_index_by_id[parents_id[0]]
                idfam_array[step_index * individus_step_size + individu_index] = step_index * familles_step_size + famille_index
                quifam_array[step_index * individus_step_size + individu_index] = 0  # chef
                famille_roles_count = 1
                if len(parents_id) > 1:
                    individu_index = individu_index_by_id[parents_id[1]]
                    idfam_array[step_index * individus_step_size + individu_index] \
                        = step_index * familles_step_size + famille_index
                    quifam_array[step_index * individus_step_size + individu_index] = 1  # part
                    famille_roles_count += 1
                for enfant_index, enfant_id in enumerate(enfants_id):
                    individu_index = individu_index_by_id[enfant_id]
                    idfam_array[step_index * individus_step_size + individu_index] \
                        = step_index * familles_step_size + famille_index
                    quifam_array[step_index * individus_step_size + individu_index] = 2 + enfant_index  # enf
                    famille_roles_count += 1
                if famille_roles_count > familles_roles_count:
                    familles_roles_count = famille_roles_count
        familles.roles_count = familles_roles_count
        #
        individus.new_holder('idfoy').array = idfoy_array = np.empty(steps_count * individus_step_size,
            dtype = column_by_name['idfoy'].dtype)  # foyer_fiscal_index
        individus.new_holder('quifoy').array = quifoy_array = np.empty(steps_count * individus_step_size,
            dtype = column_by_name['quifoy'].dtype)  # foyer_fiscal_role
        foyers_fiscaux_roles_count = 0
        for foyer_fiscal_index, foyer_fiscal in enumerate(test_case[u'foyers_fiscaux'].itervalues()):
            declarants_id = foyer_fiscal.pop(u'declarants')
            personnes_a_charge_id = foyer_fiscal.pop(u'personnes_a_charge')
            for step_index in range(steps_count):
                individu_index = individu_index_by_id[declarants_id[0]]
                idfoy_array[step_index * individus_step_size + individu_index] \
                    = step_index * foyers_fiscaux_step_size + foyer_fiscal_index
                quifoy_array[step_index * individus_step_size + individu_index] = 0  # vous
                foyer_fiscal_roles_count = 1
                if len(declarants_id) > 1:
                    individu_index = individu_index_by_id[declarants_id[1]]
                    idfoy_array[step_index * individus_step_size + individu_index] \
                        = step_index * foyers_fiscaux_step_size + foyer_fiscal_index
                    quifoy_array[step_index * individus_step_size + individu_index] = 1  # conj
                    foyer_fiscal_roles_count += 1
                for personne_a_charge_index, personne_a_charge_id in enumerate(personnes_a_charge_id):
                    individu_index = individu_index_by_id[personne_a_charge_id]
                    idfoy_array[step_index * individus_step_size + individu_index] \
                        = step_index * foyers_fiscaux_step_size + foyer_fiscal_index
                    quifoy_array[step_index * individus_step_size + individu_index] = 2 + personne_a_charge_index  # pac
                    foyer_fiscal_roles_count += 1
                if foyer_fiscal_roles_count > foyers_fiscaux_roles_count:
                    foyers_fiscaux_roles_count = foyer_fiscal_roles_count
        foyers_fiscaux.roles_count = foyers_fiscaux_roles_count
        #
        individus.new_holder('idmen').array = idmen_array = np.empty(steps_count * individus_step_size,
            dtype = column_by_name['idmen'].dtype)  # menage_index
        individus.new_holder('quimen').array = quimen_array = np.empty(steps_count * individus_step_size,
            dtype = column_by_name['quimen'].dtype)  # menage_role
        menages_roles_count = 0
        for menage_index, menage in enumerate(test_case[u'menages'].itervalues()):
            personne_de_reference_id = menage.pop(u'personne_de_reference')
            conjoint_id = menage.pop(u'conjoint')
            enfants_id = menage.pop(u'enfants')
            autres_id = menage.pop(u'autres')
            for step_index in range(steps_count):
                individu_index = individu_index_by_id[personne_de_reference_id]
                idmen_array[step_index * individus_step_size + individu_index] = step_index * menages_step_size + menage_index
                quimen_array[step_index * individus_step_size + individu_index] = 0  # pref
                menage_roles_count = 1
                if conjoint_id is not None:
                    individu_index = individu_index_by_id[conjoint_id]
                    idmen_array[step_index * individus_step_size + individu_index] \
                        = step_index * menages_step_size + menage_index
                    quimen_array[step_index * individus_step_size + individu_index] = 1  # cref
                    menage_roles_count += 1
                for enfant_index, enfant_id in enumerate(itertools.chain(enfants_id, autres_id)):
                    individu_index = individu_index_by_id[enfant_id]
                    idmen_array[step_index * individus_step_size + individu_index] \
                        = step_index * menages_step_size + menage_index
                    quimen_array[step_index * individus_step_size + individu_index] = 2 + enfant_index  # enf
                    menage_roles_count += 1
                if menage_roles_count > menages_roles_count:
                    menages_roles_count = menage_roles_count
        menages.roles_count = menages_roles_count
        #
        individus.new_holder('noi').array = np.arange(steps_count * individus_step_size,
            dtype = column_by_name['noi'].dtype)
#        individus.new_holder('prenom').array = np.array(
#            [individu['prenom'] for individu in test_case[u'individus'].itervalues()],
#            dtype = object)
        used_columns_name = set(
            key
            for individu in test_case[u'individus'].itervalues()
            for key, value in individu.iteritems()
            if value is not None
            )
        for column_name, column in column_by_name.iteritems():
            if column.entity == 'ind' and column_name in used_columns_name \
                    and column_name not in ('idfam', 'idfoy', 'idmen', 'quifam', 'quifoy', 'quimen'):
                cells_iter = (
                    cell if cell is not None else column.default
                    for cell in (
                        individu.get(column_name)
                        for step_index in range(steps_count)
                        for individu in test_case[u'individus'].itervalues()
                        )
                    )
                individus.new_holder(column_name).array = np.fromiter(cells_iter, dtype = column.dtype) \
                    if column.dtype is not object else np.array(list(cells_iter), dtype = column.dtype)

#        familles.new_holder('id').array = np.array(test_case[u'familles'].keys(), dtype = object)
        used_columns_name = set(
            key
            for famille in test_case[u'familles'].itervalues()
            for key, value in famille.iteritems()
            if value is not None
            )
        for column_name, column in column_by_name.iteritems():
            if column.entity == 'fam' and column_name in used_columns_name:
                cells_iter = (
                    cell if cell is not None else column.default
                    for cell in (
                        famille.get(column_name)
                        for step_index in range(steps_count)
                        for famille in test_case[u'familles'].itervalues()
                        )
                    )
                familles.new_holder(column_name).array = np.fromiter(cells_iter, dtype = column.dtype) \
                    if column.dtype is not object else np.array(list(cells_iter), dtype = column.dtype)

#        foyers_fiscaux.new_holder('id').array = np.array(test_case[u'foyers_fiscaux'].keys(), dtype = object)
        used_columns_name = set(
            key
            for foyer_fiscal in test_case[u'foyers_fiscaux'].itervalues()
            for key, value in foyer_fiscal.iteritems()
            if value is not None
            )
        for column_name, column in column_by_name.iteritems():
            if column.entity == 'foy' and column_name in used_columns_name:
                cells_iter = (
                    cell if cell is not None else column.default
                    for cell in (
                       foyer_fiscal.get(column_name)
                        for step_index in range(steps_count)
                        for foyer_fiscal in test_case[u'foyers_fiscaux'].itervalues()
                        )
                    )
                foyers_fiscaux.new_holder(column_name).array = np.fromiter(cells_iter, dtype = column.dtype) \
                    if column.dtype is not object else np.array(list(cells_iter), dtype = column.dtype)

#        menages.new_holder('id').array = np.array(test_case[u'menages'].keys(), dtype = object)
        used_columns_name = set(
            key
            for menage in test_case[u'menages'].itervalues()
            for key, value in menage.iteritems()
            if value is not None
            )
        for column_name, column in column_by_name.iteritems():
            if column.entity == 'men' and column_name in used_columns_name:
                cells_iter = (
                    cell if cell is not None else column.default
                    for cell in (
                        menage.get(column_name)
                        for step_index in range(steps_count)
                        for menage in test_case[u'menages'].itervalues()
                        )
                    )
                menages.new_holder(column_name).array = np.fromiter(cells_iter, dtype = column.dtype) \
                    if column.dtype is not object else np.array(list(cells_iter), dtype = column.dtype)

        if self.axes is not None:
            if len(self.axes) == 1:
                axis = self.axes[0]
                entity = simulation.entity_by_column_name[axis['name']]
                holder = simulation.get_or_new_holder(axis['name'])
                if holder.array is None:
                    column = entity.column_by_name[axis['name']]
                    holder.array = np.empty(entity.count, dtype = column.dtype)
                    holder.array.fill(column.default)
                holder.array[axis['index']:: entity.step_size] = np.linspace(axis['min'], axis['max'], axis['count'])
            else:
                axes_linspaces = [
                    np.linspace(axis['min'], axis['max'], axis['count'])
                    for axis in self.axes
                    ]
                axes_meshes = np.meshgrid(*axes_linspaces)
                for axis, mesh in zip(self.axes, axes_meshes):
                    entity = simulation.entity_by_column_name[axis['name']]
                    holder = simulation.get_or_new_holder(axis['name'])
                    if holder.array is None:
                        column = entity.column_by_name[axis['name']]
                        holder.array = np.empty(entity.count, dtype = column.dtype)
                        holder.array.fill(column.default)
                    holder.array[axis['index']:: entity.step_size] = mesh.reshape(steps_count)

        return simulation

    def suggest(self):
        test_case = self.test_case
        suggestions = dict()
        for individu_id, individu in test_case['individus'].iteritems():
            if individu.get('age') is None and individu.get('agem') is None and individu.get('birth') is None:
                # Add missing birth date to person (a parent is 40 years old and a child is 10 years old.
                is_parent = any(individu_id in famille['parents'] for famille in test_case['familles'].itervalues())
                birth_year = self.year - 40 if is_parent else self.year - 10
                birth = datetime.date(birth_year, 1, 1)
                individu['birth'] = birth
                suggestions.setdefault('test_case', {}).setdefault('individus', {}).setdefault(individu_id, {})[
                    'birth'] = birth.isoformat()
            if individu.get('activite') is None:
                if self.year - individu['birth'].year < 16:
                    suggestions.setdefault('test_case', {}).setdefault('individus', {}).setdefault(individu_id, {})[
                        'activite'] = individu['activite'] = 2  # Étudiant, élève
        return suggestions or None

#    def __init__(self):
#        super(Scenario, self).__init__()

#        self.indiv = {}
#        # indiv est un dict de dict. La clé est le noi de l'individu
#        # Exemple :
#        # 0: {'quifoy': 'vous', 'noi': 0, 'quifam': 'parent 1', 'noipref': 0, 'noidec': 0,
#        # 'birth': date(1980, 1, 1), 'quimen': 'pref', 'noichef': 0}
#        self.declar = {}
#        # declar est un dict de dict. La clé est le noidec.
#        self.famille = {}

#        # menage est un dict de dict la clé est la pref
#        self.menage = {0:{'loyer':500, 'so':4, 'code_postal':69001, 'zone_apl':2, 'zthabm' :0}}

#        # on ajoute un individu, déclarant et chef de famille
#        self.addIndiv(0, datetime(1975, 1, 1).date(), 'vous', 'chef')

#        self.nmen = None
#        self.x_axis = None
#        self.maxrev = None
#        self.same_rev_couple = None
#        self.year = None

#    def check_consistency(self):
#        '''
#Vérifie que le ménage entré est valide
#'''
#        for noi, vals in self.indiv.iteritems():
#            age = self.year - vals['birth'].year
#            if age < 0:
#                return u"L'année de naissance doit être antérieure à celle de la simulation (voir Fichier->Paramètres pour régler la date de la simulation"
#            if vals['quifoy'] in ('vous', 'conj'):
#                if age < 18: return u'Le déclarant et son éventuel conjoint doivent avoir plus de 18 ans'
#            else:
#                if age > 25 and (vals['inv'] == 0): return u'Les personnes à charges doivent avoir moins de 25 ans si elles ne sont pas invalides'
#            if vals['quifoy'] == 'conj' and not vals['quifam'] == 'part':
#                return u"Un conjoint sur la déclaration d'impôt doit être le partenaire dans la famille"
#        return ''
