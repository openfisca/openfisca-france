# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013 OpenFisca Team
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


AGGREGATES_DEFAULT_VARS = [
    'cotsoc_noncontrib', 'csg', 'crds',
    'irpp', 'ppe','ppe_brute',
    'af', 'af_base', 'af_majo','af_forf', 'cf',
    'paje_base', 'paje_nais', 'paje_clca', 'paje_clmg',
    'ars', 'aeeh', 'asf', 'aspa',
    'aah', 'caah',
    'rsa', 'rsa_act', 'aefa', 'api', 'majo_rsa', 'psa',
    'logt', 'alf', 'als', 'apl',
    ]
    #ajouter csgd pour le calcul des agrégats erfs
    #ajouter rmi pour le calcul des agrégats erfs
COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENCY = u"€"
DATA_DIR = os.path.join(COUNTRY_DIR, 'data')
DEBUG_COTSOC = True
ENTITIES_INDEX = ['men', 'fam', 'foy']
FILTERING_VARS = ["champm"]
REVENUES_CATEGORIES = {
    'brut': ['salbrut', 'chobrut', 'rstbrut', 'alr', 'alv', 'rev_cap_brut', 'fon'],
    'imposable': ['sal', 'cho', 'rst', 'alr', 'alv', 'rev_cap_brut', 'fon', 'cotsoc_cap'],
    'net': ['salnet', 'chonet', 'rstnet', 'alr', 'alv', 'rev_cap_net', 'fon'],
    'superbrut': ['salsuperbrut', 'chobrut', 'rstbrut', 'alr', 'alv', 'rev_cap_brut', 'fon'],
    }
WEIGHT = "wprm"
WEIGHT_INI = "wprm_init"
X_AXES_PROPERTIES = {
    'alr': {
        'name': 'alr',
        'typ_tot': {
            'pen': "Pensions",
            },
        'typ_tot_default': 'pen',
        },
    'choi': {
        'name': 'cho',
        'typ_tot': {
            'cho': u"Chômage",
            'chobrut': u"Chômage brut",
            'chonet': u"Chômage net",
            },
        'typ_tot_default': 'cho',
        },
    'rsti': {
        'name': 'rst',
        'typ_tot': {
            'rst': u"Retraite",
            'rstbrut': u"Retraite brut",
            'rstnet': u"Retraite net",
            },
        'typ_tot_default': 'rst',
        },
    'sali': {
        'name': 'sal',
        'typ_tot': {
            'sal':'Salaire imposable',
            'salbrut': 'Salaire brut',
            'salnet': 'Salaire net',
            'salsuperbrut': 'Salaire super brut',
            },
        'typ_tot_default': 'sal',
        },
    'f2da': {
        'name': 'divpfl',
        'typ_tot': {
            'rev_cap_brut': u"Revenus des capitaux",
            'rev_cap_net': u"Revenus des capitaux nets",
            },
        'typ_tot_default': 'rev_cap_brut',
        },
    'f2dc': {
        'name': 'divb',
        'typ_tot': {
            'rev_cap_brut': "Revenus des capitaux",
            'rev_cap_net': "Revenus des capitaux nets",
            },
        'typ_tot_default': 'rev_cap_brut',
        },
    'f2ee': {
        'name': 'intpfl',
        'typ_tot': {
            'rev_cap_brut': "Revenus des capitaux",
            'rev_cap_net': "Revenus des capitaux nets",
            },
        'typ_tot_default': 'rev_cap_brut',
        },
    'f2tr': {
        'name': 'intb',
        'typ_tot': {
            'rev_cap_brut': "Revenus des capitaux",
            'rev_cap_net': "Revenus des capitaux nets",
            },
        'typ_tot_default': 'rev_cap_brut',
        },
    'f4ba': {
        'name': 'f4ba',
        'typ_tot': {
            'fon': "Revenus fonciers",
            },
        'typ_tot_default': 'fon',
        },
    'f6gu': {
        'name': 'f6gu',
        'typ_tot': {
            'pen': "Pensions",
            },
        'typ_tot_default': 'pen',
        },
    }


def init_country(qt = False):
    """Add country-specific content to OpenFisca-Core package."""
    from openfisca_core import model as core_model
    from openfisca_core import simulations as core_simulations
    from openfisca_core import taxbenefitsystems as core_taxbenefitsystems
    from openfisca_core.xaxes import XAxis
    if qt:
        from openfisca_qt import widgets as qt_widgets

    from . import decompositions, scenarios, utils
    from .model.data import InputDescription
    from .model.model import OutputDescription
    if qt:
        from .widgets.Composition import CompositionWidget

    core_taxbenefitsystems.preproc_inputs = utils.preproc_inputs

    core_model.AGGREGATES_DEFAULT_VARS = AGGREGATES_DEFAULT_VARS
    core_model.CURRENCY = CURRENCY
    core_model.DATA_DIR = DATA_DIR
    core_model.DATA_SOURCES_DIR = os.path.join(COUNTRY_DIR, 'data', 'sources')
    core_model.DECOMP_DIR = os.path.dirname(os.path.abspath(decompositions.__file__))
    core_model.DEFAULT_DECOMP_FILE = decompositions.DEFAULT_DECOMP_FILE
    core_model.ENTITIES_INDEX = ENTITIES_INDEX
    core_model.FILTERING_VARS = FILTERING_VARS
    core_model.InputDescription = InputDescription
    core_model.OutputDescription = OutputDescription
    core_model.PARAM_FILE = os.path.join(COUNTRY_DIR, 'param', 'param.xml')
    core_model.REFORMS_DIR = os.path.join(COUNTRY_DIR, 'reformes')
    core_model.REV_TYP = None  # utils.REV_TYP  # Not defined for France
    core_model.REVENUES_CATEGORIES = REVENUES_CATEGORIES
    core_model.Scenario = scenarios.Scenario
    core_model.WEIGHT = WEIGHT
    core_model.WEIGHT_INI = WEIGHT_INI
    core_model.x_axes = dict(
        (col_name, XAxis(col_name = col_name, label = InputDescription.column_by_name[col_name].label, **properties))
        for col_name, properties in X_AXES_PROPERTIES.iteritems()
        )

    core_simulations.check_consistency = utils.check_consistency

    if qt:
        qt_widgets.CompositionWidget = CompositionWidget
#        qt_widgets.ScenarioWidget = ScenarioWidget
