# -*- coding: utf-8 -*-

# This file is part of OpenFisca
# Copyright © 2012 Mahdi Ben Jelloul, Clément Schaff 
# Licensed under the terms of the GPL License v3 or later version
# (see src/__init__.py for details)

import os
from src import SRC_PATH

## France 

# Model parameters
ENTITIES_INDEX = ['men', 'fam', 'foy']


# Data
WEIGHT = "wprm"
WEIGHT_INI = "wprm_init"


DATA_SOURCES_DIR = os.path.join(SRC_PATH,"countries","france","data","sources")


# Some variables needed by the test case plugins

CURRENCY = u"€"

REVENUES_CATEGORIES = {'superbrut' : ['salsuperbrut', 'chobrut', 'rstbrut', 'alr', 'alv',
                       'rev_cap_brut', 'fon'],
       'brut': ['salbrut', 'chobrut', 'rstbrut', 'alr', 'alv',
                 'rev_cap_brut', 'fon'],
       'imposable' : ['sal', 'cho', 'rst', 'alr', 'alv', 'rev_cap_brut', 'fon', 'cotsoc_cap'],
       'net'      : ['salnet', 'chonet', 'rstnet', 'alr', 'alv', 'rev_cap_net', 'fon',
                      ]}        


# Some variables used by other plugins

AGGREGATES_DEFAULT_VARS = ['cotsoc_noncontrib', 'csg', 'crds',
            'irpp', 'ppe',
            'af', 'af_base', 'af_majo','af_forf', 'cf',
            'paje_base', 'paje_nais', 'paje_colca', 'paje_clmg',
            'ars', 'aeeh', 'asf', 'aspa',
            'aah', 'caah', 
            'rsa', 'rsa_act', 'aefa', 'api',
            'logt', 'alf', 'als', 'apl']