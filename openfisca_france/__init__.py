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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os

COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENCY = u"€"
ENTITIES_INDEX = ['men', 'fam', 'foy']
REVENUES_CATEGORIES = {
    'brut': ['salbrut', 'chobrut', 'rstbrut', 'alr', 'alv', 'rev_cap_brut', 'fon'],
    'imposable': ['sal', 'cho', 'rst', 'alr', 'alv', 'rev_cap_brut', 'fon', 'cotsoc_cap'],
    'net': ['salnet', 'chonet', 'rstnet', 'alr', 'alv', 'rev_cap_net', 'fon'],
    'superbrut': ['salsuperbrut', 'chobrut', 'rstbrut', 'alr', 'alv', 'rev_cap_brut', 'fon'],
    }


def init_country(drop_survey_only_variables = False, qt = False, simulate_f6de = False, start_from = 'imposable'):
    """Create a country-specific TaxBenefitSystem."""
    from openfisca_core.columns import FloatCol
    from openfisca_core import taxbenefitsystems as core_taxbenefitsystems
    if qt:
        from openfisca_qt import widgets as qt_widgets

    from . import decompositions, entities, scenarios  # utils
    from .model.cotisations_sociales.preprocessing import preprocess_legislation_parameters
    from .model.input_variables import column_by_name
    from .model.datatrees import columns_name_tree_by_entity
    from .model.model import prestation_by_name
    if qt:
        from .widgets.Composition import CompositionWidget

    assert start_from in ['brut', 'imposable']  # TODO: net
    column_by_name = column_by_name.copy()

    if start_from in ['brut', 'net']:
        drop_survey_only_variables = True

    if start_from == 'brut':
        variables_bruts = ['salbrut', 'chobrut', 'rstbrut']
        variables_imposables = ['sali', 'choi', 'rsti']
        column_by_name.update(
            (variable, prestation_by_name.pop(variable).to_column())
            for variable in variables_bruts + ['type_sal', 'primes']
            )
        for variable in variables_imposables:
            del column_by_name[variable]
    elif start_from == 'net':
        raise NotImplementedError

    if drop_survey_only_variables:
        survey_only_variables = [
            name
            for name, column in column_by_name.iteritems()
            if column.survey_only
            ]
        for variable in survey_only_variables:
            del column_by_name[variable]

#        survey_only_variables = [
#            name
#            for name, prestation in prestation_by_name.iteritems()
#            if prestation.survey_only
#            ]
#        for variable in survey_only_variables:
#            del prestation_by_name[variable]

        needed_columns = ['type_sal', 'primes']
        for variable in needed_columns:
            if variable not in column_by_name:
                column_by_name[variable] = prestation_by_name.pop(variable).to_column()

    if simulate_f6de:
        del column_by_name['f6de']
        csg_deduc_patrimoine_simulated = prestation_by_name.pop('csg_deduc_patrimoine_simulated')
        prestation_by_name['csg_deduc_patrimoine'] = FloatCol(
            csg_deduc_patrimoine_simulated._func,
            entity = csg_deduc_patrimoine_simulated.entity,
            label = csg_deduc_patrimoine_simulated.label,
            start = csg_deduc_patrimoine_simulated.start,
            end = csg_deduc_patrimoine_simulated.end,
            val_type = csg_deduc_patrimoine_simulated.val_type,
            freq = csg_deduc_patrimoine_simulated.freq,
            survey_only = False,
            )
    else:
        prestation_by_name.pop('csg_deduc_patrimoine_simulated', None)

    if qt:
        qt_widgets.CompositionWidget = CompositionWidget

    class TaxBenefitSystem(core_taxbenefitsystems.AbstractTaxBenefitSystem):
        """French tax benefit system"""
        check_consistency = None  # staticmethod(utils.check_consistency)
        CURRENCY = CURRENCY
        DATA_SOURCES_DIR = os.path.join(COUNTRY_DIR, 'data', 'sources')
        DECOMP_DIR = os.path.dirname(os.path.abspath(decompositions.__file__))
        DEFAULT_DECOMP_FILE = decompositions.DEFAULT_DECOMP_FILE
        entities = [
            'familles',
            'foyers_fiscaux',
            'individus',
            'menages',
            ]
        ENTITIES_INDEX = ENTITIES_INDEX
        # entity_class_by_key_plural = entity_class_by_key_plural  # Done below to avoid "name is not defined" exception
        # column_by_name = column_by_name  # Done below to avoid "name is not defined" exception
        # columns_name_tree_by_entity = columns_name_tree_by_entity  # Done below to avoid "name is not defined" exception
        PARAM_FILE = os.path.join(COUNTRY_DIR, 'param', 'param.xml')
        # preprocess_legislation_parameters = preprocess_legislation_parameters  # Done below to avoid "name is not defined" exception
        # prestation_by_name = prestation_by_name  # Done below to avoid "name is not defined" exception
        REFORMS_DIR = os.path.join(COUNTRY_DIR, 'reformes')
        REV_TYP = None  # utils.REV_TYP  # Not defined for France
        REVENUES_CATEGORIES = REVENUES_CATEGORIES
        Scenario = scenarios.Scenario

    TaxBenefitSystem.column_by_name = column_by_name
    TaxBenefitSystem.columns_name_tree_by_entity = columns_name_tree_by_entity
    TaxBenefitSystem.entity_class_by_key_plural = dict(
        (entity_class.key_plural, entity_class)
        for entity_class in entities.entity_class_by_symbol.itervalues()
        )
    TaxBenefitSystem.preprocess_legislation_parameters = staticmethod(preprocess_legislation_parameters)

    TaxBenefitSystem.prestation_by_name = prestation_by_name
    return TaxBenefitSystem
