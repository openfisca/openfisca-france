# -*- coding:utf-8 -*-
# Created on 10 juin 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul, Jérôme Santoul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)
# # # OpenFisca

from src.countries.france.data.erf.build_survey.utilitaries import control

def run_all(year=2006):
    
    pre_proc = __import__('01pre_proc')
    imput_loyer = __import__('02_imput_loyer')
    fip = __import__('03_fip')
    famille = __import__('04_famille')
    foyer = __import__('05_foyer')
    rebuild = __import__('06_rebuild')
    invalides = __import__('07_invalides')
    final = __import__('08_final')
    
    pre_proc.create_indivim(year=year)
    pre_proc.create_enfnn(year=year)
#     imput_loyer.create_imput_loyer(year=year)
    fip.create_fip(year=year)
    famille.famille(year=year)
    foyer.sif(year=year)
    foyer.foyer_all(year=year)
    rebuild.create_totals(year=year)
    rebuild.create_final(year=year)
#     invalides.invalide(year=year)
#     final.final(year=year)

if __name__ == '__main__':
    run_all(year = 2006)
