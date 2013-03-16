# -*- coding:utf-8 -*-
# Created on 27 févr. 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright © 2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)

from src.countries.france.data.sources.config import DATA_DIR
from src.countries.france.data.sources.utils import cvs2hdf5
import os


def get_csv_file_name(year):
    
    os.path.dirname(DATA_DIR)
    R_DIR = os.path.join(os.path.dirname(DATA_DIR),'R','openfisca', str(year))
    yr = str(year)[2:]
    fname = os.path.join(R_DIR,"final"+ yr + ".csv")
    return fname

def build_survey_psl():
    year = 2006
    h5_name = '../survey_psl.h5'    
    dfname = 'survey_' + str(year)
    os.path.dirname(DATA_DIR)
    PSL_DIR = os.path.join(os.path.dirname(DATA_DIR),'PSL')
    csv_name = os.path.join(PSL_DIR,"psl_"+ str(year) + ".csv")
    print("Using " + csv_name + " to build " + h5_name)
    csv2hdf5(csv_name, h5_name, dfname)


def build_survey(year, option='frame'):
    h5_name = '../survey.h5'
    dfname = 'survey_' + str(year)
    csv_name = get_csv_file_name(year)
    print("Using " + csv_name + " to build " + h5_name)
    csv2hdf5(csv_name, h5_name, dfname, option=option)

def build_all_surveys( option = 'frame'):
    h5_name = '../survey.h5'    
    try:
        os.remove(h5_name)
    except:
        pass
    for year in range(2006,2010):
        build_survey(year, option=option)
        



if __name__ == '__main__':

    build_all_surveys()