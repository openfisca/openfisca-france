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


import numpy as np
from openfisca_core import formulas


class FormulaMixin(object):
    def cast_from_entity_to_all_roles(self, array, default = 0, entity = None):
        holder = self.holder
        target_entity = holder.entity
        simulation = target_entity.simulation
        individus = simulation.entities['individus']
        assert entity in simulation.entity_by_key_singular, u"Unknown entity: {}".format(entity).encode('utf-8')
        entity = simulation.entity_by_key_singular[entity]
        assert isinstance(array, np.ndarray), u"Expected a numpy array. Got: {}".format(array).encode('utf-8')
        assert array.size == entity.count, u"Expected an array of size {}. Got: {}".format(entity.count, array.size)
        target_array = np.empty(individus.count, dtype = array.dtype)
        target_array.fill(default)
        entity_index_array = individus.holder_by_name['id' + entity.symbol].array
        for role in range(entity.roles_count):
            boolean_filter = individus.holder_by_name['qui' + entity.symbol].array == role
            try:
                target_array[entity_index_array[boolean_filter]] = array
            except:
                log.error(u'An error occurred while transforming array for role {}[{}] in function {}'.format(
                    entity.key_singular, role, holder.column.name))
                raise
        return target_array

    def cast_from_entity_to_role(self, array, default = 0, entity = None, role = None):
        holder = self.holder
        target_entity = holder.entity
        simulation = target_entity.simulation
        individus = simulation.entities['individus']
        assert entity in simulation.entity_by_key_singular, u"Unknown entity: {}".format(entity).encode('utf-8')
        entity = simulation.entity_by_key_singular[entity]
        assert isinstance(array, np.ndarray), u"Expected a numpy array. Got: {}".format(array).encode('utf-8')
        assert array.size == entity.count, u"Expected an array of size {}. Got: {}".format(entity.count, array.size)
        target_array = np.empty(individus.count, dtype = array.dtype)
        target_array.fill(default)
        entity_index_array = individus.holder_by_name['id' + entity.symbol].array
        assert role is not None
        boolean_filter = individus.holder_by_name['qui' + entity.symbol].array == role
        try:
            target_array[entity_index_array[boolean_filter]] = array
        except:
            log.error(u'An error occurred while transforming array for role {}[{}] in function {}'.format(
                entity.key_singular, role, holder.column.name))
            raise
        return target_array

    def sum_by_entity(self, array, entity = None):
        holder = self.holder
        target_entity = holder.entity
        simulation = target_entity.simulation
        individus = simulation.entities['individus']
        assert entity in simulation.entity_by_key_singular, u"Unknown entity: {}".format(entity).encode('utf-8')
        entity = simulation.entity_by_key_singular[entity]
        assert isinstance(array, np.ndarray), u"Expected a numpy array. Got: {}".format(array).encode('utf-8')
        assert array.size == individus.count, u"Expected an array of size {}. Got: {}".format(individus.count,
            array.size)
        target_array = np.zeros(entity.count, dtype = array.dtype)
        entity_index_array = individus.holder_by_name['id' + entity.symbol].array
        for role in range(entity.roles_count):
            # TODO Mettre les filtres en cache dans la simulation
            boolean_filter = individus.holder_by_name['qui' + entity.symbol].array == role
            target_array[entity_index_array[boolean_filter]] += array[boolean_filter]
        return target_array

    or_by_entity = sum_by_entity


class Formula(FormulaMixin, formulas.AbstractFormula):
    pass


class SimpleFormula(FormulaMixin, formulas.AbstractSimpleFormula):
    pass
