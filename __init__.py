# -*- coding: utf-8 -*-

# This file is part of OpenFisca
# Copyright © 2012 Mahdi Ben Jelloul, Clément Schaff 
# Licensed under the terms of the GPL License v3 or later version
# (see src/__init__.py for details)

## France 

# Some variables needed bu the test case

ENTITIES_INDEX = ['men', 'fam', 'foy']


WEIGHT = "wprm"
WEIGHT_INI = "wprm_init"

CURRENCY = u"€"

REVENUES_CATEGORIES = {'superbrut' : ['salsuperbrut', 'chobrut', 'rstbrut', 'alr', 'alv',
                       'rev_cap_brut', 'fon'],
       'brut': ['salbrut', 'chobrut', 'rstbrut', 'alr', 'alv',
                 'rev_cap_brut', 'fon'],
       'imposable' : ['sal', 'cho', 'rst', 'alr', 'alv', 'rev_cap_brut', 'fon', 'cotsoc_cap'],
       'net'      : ['salnet', 'chonet', 'rstnet', 'alr', 'alv', 'rev_cap_net', 'fon',
                      ]}        
#        alim = data['alr'].vals + data['alv'].vals
#        penbrut = data['chobrut'].vals + data['rstbrut'].vals + alim
#        penimp  = data['cho'].vals + data['rst'].vals + alim
#        pennet  = data['chonet'].vals + data['rstnet'].vals + alim
#        capbrut = data['rev_cap_bar'].vals + data['rev_cap_lib'].vals + data['fon'].vals
#        capnet = capbrut + data['cotsoc_bar'].vals + data['cotsoc_lib'].vals

#        if   typrev == 'superbrut': 
#            out = data['salsuperbrut'].vals + penbrut + capbrut
#        elif typrev == 'brut':      
#            out = data['salbrut'].vals + penbrut + capbrut
#        elif typrev == 'imposable':
#            out = data['sali'].vals + penimp + capnet
#        elif typrev == 'net':       
#            out = data['salnet'].vals + pennet + capnet
