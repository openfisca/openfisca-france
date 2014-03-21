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

from . import entities


def new_simulation_from_survey_data_frame(compact_legislation = None, debug = False, survey = None, tax_benefit_system = None, year = None):
    simulation = simulations.Simulation(
        compact_legislation = compact_legislation,
        date = datetime.date(year, 5, 1),
        debug = debug,
        tax_benefit_system = tax_benefit_system,
        )

    column_by_name = tax_benefit_system.column_by_name
    for column_name, series in survey.iteritems():
        assert column_name in column_by_name, column_name
    entity_by_key_plural = simulation.entity_by_key_plural

    familles = entity_by_key_plural[u'familles']
    familles.count = familles.step_size = familles_step_size = (survey.quifam == 0).sum()
    foyers_fiscaux = entity_by_key_plural[u'foyers_fiscaux']
    foyers_fiscaux.count = foyers_fiscaux.step_size = foyers_fiscaux_step_size = (survey.quifoy == 0).sum()
    individus = entity_by_key_plural[u'individus']
    individus.count = individus.step_size = individus_step_size = len(survey)
    menages = entity_by_key_plural[u'menages']
    menages.count = menages.step_size = menages_step_size = (survey.quimen == 0).sum()

    assert 'age' in survey.columns
    assert 'agem' in survey.columns
    assert 'idfam' in survey.columns
    assert 'idfoy' in survey.columns
    assert 'idmen' in survey.columns
    assert 'noi' in survey.columns
    assert 'quifam' in survey.columns
    assert 'quifoy' in survey.columns
    assert 'quimen' in survey.columns

    familles.roles_count = survey['quifam'].max() + 1
    menages.roles_count = survey['quimen'].max() + 1
    foyers_fiscaux.roles_count = survey['quifoy'].max() + 1

    for column_name, column_series in survey.iteritems():
        holder = simulation.new_holder(column_name)
        entity = holder.entity
        if holder.entity.is_persons_entity:
            array = column_series.values
        else:
            array = column_series.values[survey['qui' + entity.symbol].values == 0]
        assert array.size == entity.count, 'Bad size for {}: {} instead of {}'.format(column_name, array.size,
            entity.count)
        holder.array = np.array(array, dtype = holder.column._dtype)

    return simulation

