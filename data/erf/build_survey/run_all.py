# -*- coding:utf-8 -*-
# Created on 10 juin 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul, Jérôme Santoul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)
# # # OpenFisca

from src import SRC_PATH
from src.countries.france.data.erf.build_survey.utilitaries import control
import os

def run_all():
    
    pre_proc = __import__('01pre_proc')
    fip = __import__('03_fip')
    famille = __import__('04_famille')
    foyer = __import__('05_foyer')
    rebuild = __import__('06_rebuild')
    invalides = __import__('07_invalides')
    final = __import__('08_final')
    
    pre_proc.create_indivim()
    pre_proc.create_enfnn()
    fip.create_fip()
    famille.famille()
    foyer.sif()
    foyer.foyer_all()
    rebuild.create_totals()
    rebuild.create_final()
    invalides.invalide()
    final.final()

if __name__ == '__main__':
    run_all()