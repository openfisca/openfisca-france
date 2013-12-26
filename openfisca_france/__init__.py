# -*- coding: utf-8 -*-

# This file is part of OpenFisca
# Copyright © 2012 Mahdi Ben Jelloul, Clément Schaff 
# Licensed under the terms of the GPL License v3 or later version
# (see src/__init__.py for details)

import os


## Debugging parameters

DEBUG_COTSOC = True

# Model parameters
ENTITIES_INDEX = ['men', 'fam', 'foy']

# Data
FILTERING_VARS = ["champm"]

DATA_SOURCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data","sources")

WEIGHT = "wprm"
WEIGHT_INI = "wprm_init"

# Some variables needed by the test case plugins

CURRENCY = u"€"



# Some variables needed by the test case graph widget

REVENUES_CATEGORIES = {'superbrut' : ['salsuperbrut', 'chobrut', 'rstbrut', 'alr', 'alv',
                       'rev_cap_brut', 'fon'],
       'brut': ['salbrut', 'chobrut', 'rstbrut', 'alr', 'alv',
                 'rev_cap_brut', 'fon'],
       'imposable' : ['sal', 'cho', 'rst', 'alr', 'alv', 'rev_cap_brut', 'fon', 'cotsoc_cap'],
       'net'      : ['salnet', 'chonet', 'rstnet', 'alr', 'alv', 'rev_cap_net', 'fon',
                      ]}        


XAXIS_PROPERTIES = { 'sali': {
                              'name' : 'sal',
                              'typ_tot' : {'salsuperbrut' : 'Salaire super brut',
                                           'salbrut': 'Salaire brut',
                                           'sal':  'Salaire imposable',
                                           'salnet': 'Salaire net'},
                              'typ_tot_default' : 'sal'},
                    'choi': {
                             'name' : 'cho',
                             'col_name' : 'choi', 
                             'typ_tot' : {'chobrut': u"Chômage brut",
                                          'cho':     u"Chômage",
                                          'chonet':  u"Chômage net"},
                             'typ_tot_default' : 'cho' },
                    'rsti': {
                             'name' : 'rst',
                             'col_name' : 'rsti', 
                             'typ_tot' : {'rstbrut': u"Retraite brut",
                                          'rst':     u"Retraite",
                                          'rstnet':  u"Retraite net"},
                             'typ_tot_default' : 'rst'},
                    'f2da': {
                             'name': 'divpfl',
                             'col_name' : 'f2da', 
                             'typ_tot' : {'rev_cap_brut': u"Revenus des capitaux", 
                                          'rev_cap_net': u"Revenus des capitaux nets"},
                             'typ_tot_default' : 'rev_cap_brut'},
                    'f2ee': {
                             'name' : 'intpfl',
                             'col_name' : 'f2ee', 
                             'typ_tot' : {'rev_cap_brut': "Revenus des capitaux", 
                                          'rev_cap_net': "Revenus des capitaux nets"},
                             'typ_tot_default' : 'rev_cap_brut'},
                    'f2dc': {
                             'name' : 'divb',
                             'col_name' : 'f2dc',
                             'typ_tot' : {'rev_cap_brut': "Revenus des capitaux", 
                                          'rev_cap_net': "Revenus des capitaux nets"},
                             'typ_tot_default' : 'rev_cap_brut'},
                    'f2tr': {
                             'name' : 'intb',
                             'col_name' : 'f2tr', 
                             'typ_tot' : {'rev_cap_brut': "Revenus des capitaux", 
                                          'rev_cap_net': "Revenus des capitaux nets"},
                             'typ_tot_default' : 'rev_cap_brut'},
                    'alr' : {
                             'name' : 'alr',
                             'col_name' : 'alr',
                             'typ_tot' : {'pen': "Pensions"},
                             'typ_tot_default' : 'pen'},
                    'f6gu' : {
                             'name' : 'f6gu',
                             'col_name' : 'f6gu',
                             'typ_tot' : {'pen': "Pensions"},
                             'typ_tot_default' : 'pen'},
                    'f4ba' : {
                             'name' : 'f4ba',
                             'col_name' : 'f4ba',
                             'typ_tot' : {'fon': "Revenus fonciers"},
                             'typ_tot_default' : 'fon'},
                    
                    }


# Some variables used by other plugins

AGGREGATES_DEFAULT_VARS = ['cotsoc_noncontrib', 'csg', 'crds',
            'irpp', 'ppe','ppe_brute',
            'af', 'af_base', 'af_majo','af_forf', 'cf',
            'paje_base', 'paje_nais', 'paje_clca', 'paje_clmg',
            'ars', 'aeeh', 'asf', 'aspa',
            'aah', 'caah', 
            'rsa', 'rsa_act', 'aefa', 'api', 'majo_rsa', 'psa',
            'logt', 'alf', 'als', 'apl']
#ajouter csgd pour le calcul des agrégats erfs
#ajouter rmi pour le calcul des agrégats erfs


def init_country(qt = False):
    """Add country-specific content to OpenFisca-Core package."""
    from openfisca_core import model as core_model
    from openfisca_core import datatables as core_datatables
    from openfisca_core import simulations as core_simulations
    if qt:
        from openfisca_qt import widgets as qt_widgets

    from . import decompositions, utils
    from .model.data import InputDescription
    from .model.model import OutputDescription
    if qt:
        from .widgets.Composition import CompositionWidget

    country_dir = os.path.dirname(os.path.abspath(__file__))

    core_datatables.preproc_inputs = utils.preproc_inputs

    core_model.AGGREGATES_DEFAULT_VARS = AGGREGATES_DEFAULT_VARS
    core_model.CURRENCY = CURRENCY
    core_model.DATA_DIR = os.path.join(country_dir, 'data')
    core_model.DATA_SOURCES_DIR = os.path.join(country_dir, 'data', 'sources')
    core_model.DECOMP_DIR = os.path.dirname(os.path.abspath(decompositions.__file__))
    core_model.DEFAULT_DECOMP_FILE = decompositions.DEFAULT_DECOMP_FILE
    core_model.ENTITIES_INDEX = ENTITIES_INDEX
    core_model.FILTERING_VARS = FILTERING_VARS
    core_model.InputDescription = InputDescription
    core_model.OutputDescription = OutputDescription
    core_model.PARAM_FILE = os.path.join(country_dir, 'param', 'param.xml')
    core_model.REFORMS_DIR = os.path.join(country_dir, 'reformes')
    core_model.REV_TYP = None  # utils.REV_TYP  # Not defined for France
    core_model.REVENUES_CATEGORIES = REVENUES_CATEGORIES
    core_model.Scenario = utils.Scenario
    core_model.WEIGHT = WEIGHT
    core_model.WEIGHT_INI = WEIGHT_INI
    core_model.XAXIS_PROPERTIES = XAXIS_PROPERTIES

    core_simulations.check_consistency = utils.check_consistency

    if qt:
        qt_widgets.CompositionWidget = CompositionWidget
#        qt_widgets.ScenarioWidget = ScenarioWidget

