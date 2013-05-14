# -*- coding:utf-8 -*-
# Created on 14 mai 2013
# This file is part of OpenFisca.
# OpenFisca is a socio-fiscal microsimulation software
# Copyright ©2013 Clément Schaff, Mahdi Ben Jelloul
# Licensed under the terms of the GVPLv3 or later license
# (see openfisca/__init__.py for details)

import nose
from src.lib.simulation import ScenarioSimulation
from datetime import datetime

def test_af():
    yr = 2009
    country = 'france'

    simulation = ScenarioSimulation()
    simulation.set_config(year = yr, country = country, 
                    nmen = 2, maxrev = 100000, xaxis = 'sali')
    # Adding a husband/wife on the same tax sheet (foyer)
    simulation.scenario.addIndiv(1, datetime(1975,1,1).date(), 'conj', 'part') 
    simulation.set_param()
    # Adding children on the same tax sheet (foyer)
    simulation.scenario.addIndiv(2, datetime(2000,1,1).date(), 'pac', 'enf')
    simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')    
    df = simulation.get_results_dataframe(index_by_code=True)
    print simulation.P.fam.af.bmaf
    assert df.loc["af"][0] == 1494.48

if __name__ == '__main__':

#    test_1()
    nose.core.runmodule(argv=[__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)

