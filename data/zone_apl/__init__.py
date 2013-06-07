# -*- coding:utf-8 -*-
#
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GPL (version 3 or later) license
# (see openfisca/__init__.py for details)


# TODO: THIS NEEDS CLEANING

# this directory contains:
#   - zone_apl_2006.csv : PSDC99, Pop_mun_2006, Zone, REG, POL99, TU99, TAU99
#   - zone_apl.csv : example of row : PARIS    Paris    75012    75056    1
#   - zone_apl_imputation_data : ,TU99,TAU99,REG,POL99,proba_zone1,proba_zone2,proba_zone3


# zone_apl_imputation_data_reader.py uses zone_apl_2006 to build zone_apl_imputation_data 

# code_apl in france.data is used by a widget codeAplReader was used to produce it. 
# Should be stored here