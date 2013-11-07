# -*- coding:utf-8 -*-
# Created on 10 juin 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul, Jérôme Santoul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)
# # # OpenFisca

from src.countries.france.data.erf.build_survey import (step_01_pre_proc as pre_proc,
                                                       step_02_imput_loyer as imput_loyer, 
                                                       step_03_fip as fip, 
                                                       step_04_famille as famille,
                                                       step_05_foyer as foyer,
                                                       step_06_rebuild as rebuild,
                                                       step_07_invalides as invalides,
                                                       step_08_final as final)

def run_all(year=2006, filename="test", check=False):
      
#     pre_proc.create_indivim(year=year)
#     pre_proc.create_enfnn(year=year)
#     imput_loyer.create_imput_loyer(year=year)
#     fip.create_fip(year=year)
#     famille.famille(year=year)
#     foyer.sif(year=year)
#     foyer.foyer_all(year=year)
#     rebuild.create_totals(year=year)
#     rebuild.create_final(year=year)
#     invalides.invalide(year=year)
    final.final(year=year, check=check)

if __name__ == '__main__':
    run_all(year = 2006, check=False)
    import pdb
    pdb.set_trace()
