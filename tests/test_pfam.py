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



''' test avec 2 enfants 
'''


af_2enf = {2006: 1412.64, 2007 : 1436.64, 2008: 1451.04, 2009: 1494.48}

def test_af2():
    country = 'france'
    for yr in range(2006,2010):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, 
                        nmen = 2, maxrev = 100000, xaxis = 'sali')
        # Adding a husband/wife on the same tax sheet (foyer)
        simulation.scenario.addIndiv(1, datetime(1975,1,1).date(), 'conj', 'part') 
        simulation.scenario.addIndiv(2, datetime(1975,2,2).date(), 'conj', 'part') 
        simulation.set_param()
        # Adding children on the same tax sheet (foyer)
        simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
        simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
        df = simulation.get_results_dataframe(index_by_code=True)
#        print df.loc["af"][0]
#        print af_2enf[yr]
#        print type(df.loc["af"][0])
#        print type(af_2enf[yr])
#        print abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3
        assert abs(df.loc["af"][0] - af_2enf[yr]) < 1e-3 
    #   montant AF annuel brut de CRDS

   
   
''' test avec 3 enfants 
'''

def test_af063():
    yr = 2006
    country = 'france'

    simulation = ScenarioSimulation()
    simulation.set_config(year = yr, country = country, 
                    nmen = 2, maxrev = 100000, xaxis = 'sali')
    # Adding a husband/wife on the same tax sheet (foyer)
    simulation.scenario.addIndiv(1, datetime(1975,1,1).date(), 'conj', 'part') 
    simulation.scenario.addIndiv(2, datetime(1975,2,2).date(), 'conj', 'part') 
    simulation.set_param()
    # Adding children on the same tax sheet (foyer)
    simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
    simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
    df = simulation.get_results_dataframe(index_by_code=True)
    print simulation.P.fam.af.bmaf
    assert df.loc["af"][0] == 3222.60 
#   montant AF annuel brut de CRDS

def test_af073():
    yr = 2007
    country = 'france'

    simulation = ScenarioSimulation()
    simulation.set_config(year = yr, country = country, 
                    nmen = 2, maxrev = 100000, xaxis = 'sali')
    # Adding a husband/wife on the same tax sheet (foyer)
    simulation.scenario.addIndiv(1, datetime(1975,1,1).date(), 'conj', 'part') 
    simulation.scenario.addIndiv(2, datetime(1975,2,2).date(), 'conj', 'part') 
    simulation.set_param()
    # Adding children on the same tax sheet (foyer)
    simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
    simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
    df = simulation.get_results_dataframe(index_by_code=True)
    print simulation.P.fam.af.bmaf
    assert df.loc["af"][0] == 3277.32
#   montant AF annuel brut de CRDS


def test_af083():
    yr = 2008
    country = 'france'

    simulation = ScenarioSimulation()
    simulation.set_config(year = yr, country = country, 
                    nmen = 2, maxrev = 100000, xaxis = 'sali')
    # Adding a husband/wife on the same tax sheet (foyer)
    simulation.scenario.addIndiv(1, datetime(1975,1,1).date(), 'conj', 'part') 
    simulation.scenario.addIndiv(2, datetime(1975,2,2).date(), 'conj', 'part') 
    simulation.set_param()
    # Adding children on the same tax sheet (foyer)
    simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
    simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
    df = simulation.get_results_dataframe(index_by_code=True)
    print simulation.P.fam.af.bmaf
    assert df.loc["af"][0] == 3310.08 
#   montant AF annuel brut de CRDS


def test_af093():
    yr = 2009
    country = 'france'

    simulation = ScenarioSimulation()
    simulation.set_config(year = yr, country = country, 
                    nmen = 2, maxrev = 100000, xaxis = 'sali')
    # Adding a husband/wife on the same tax sheet (foyer)
    simulation.scenario.addIndiv(1, datetime(1975,1,1).date(), 'conj', 'part') 
    simulation.scenario.addIndiv(2, datetime(1975,2,2).date(), 'conj', 'part') 
    simulation.set_param()
    # Adding children on the same tax sheet (foyer)
    simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
    simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
    df = simulation.get_results_dataframe(index_by_code=True)
    print simulation.P.fam.af.bmaf
    assert df.loc["af"][0] == 3409.44 
#   montant AF annuel brut de CRDS
    
   
''' test avec 5 enfants 
'''

def test_af065():
    yr = 2006
    country = 'france'

    simulation = ScenarioSimulation()
    simulation.set_config(year = yr, country = country, 
                    nmen = 2, maxrev = 100000, xaxis = 'sali')
    # Adding a husband/wife on the same tax sheet (foyer)
    simulation.scenario.addIndiv(1, datetime(1975,1,1).date(), 'conj', 'part') 
    simulation.scenario.addIndiv(2, datetime(1975,2,2).date(), 'conj', 'part') 
    simulation.set_param()
    # Adding children on the same tax sheet (foyer)
    simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
    simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
    df = simulation.get_results_dataframe(index_by_code=True)
    print simulation.P.fam.af.bmaf
    assert df.loc["af"][0] == 6842.40 
#   montant AF annuel brut de CRDS

def test_af075():
    yr = 2007
    country = 'france'

    simulation = ScenarioSimulation()
    simulation.set_config(year = yr, country = country, 
                    nmen = 2, maxrev = 100000, xaxis = 'sali')
    # Adding a husband/wife on the same tax sheet (foyer)
    simulation.scenario.addIndiv(1, datetime(1975,1,1).date(), 'conj', 'part') 
    simulation.scenario.addIndiv(2, datetime(1975,2,2).date(), 'conj', 'part') 
    simulation.set_param()
    # Adding children on the same tax sheet (foyer)
    simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
    simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
    df = simulation.get_results_dataframe(index_by_code=True)
    print simulation.P.fam.af.bmaf
    assert df.loc["af"][0] == 6958.68 
#   montant AF annuel brut de CRDS


def test_af085():
    yr = 2008
    country = 'france'

    simulation = ScenarioSimulation()
    simulation.set_config(year = yr, country = country, 
                    nmen = 2, maxrev = 100000, xaxis = 'sali')
    # Adding a husband/wife on the same tax sheet (foyer)
    simulation.scenario.addIndiv(1, datetime(1975,1,1).date(), 'conj', 'part') 
    simulation.scenario.addIndiv(2, datetime(1975,2,2).date(), 'conj', 'part') 
    simulation.set_param()
    # Adding children on the same tax sheet (foyer)
    simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
    simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
    df = simulation.get_results_dataframe(index_by_code=True)
    print simulation.P.fam.af.bmaf
    assert df.loc["af"][0] == 7028.16 
#   montant AF annuel brut de CRDS


def test_af095():
    yr = 2009
    country = 'france'

    simulation = ScenarioSimulation()
    simulation.set_config(year = yr, country = country, 
                    nmen = 2, maxrev = 100000, xaxis = 'sali')
    # Adding a husband/wife on the same tax sheet (foyer)
    simulation.scenario.addIndiv(1, datetime(1975,1,1).date(), 'conj', 'part') 
    simulation.scenario.addIndiv(2, datetime(1975,2,2).date(), 'conj', 'part') 
    simulation.set_param()
    # Adding children on the same tax sheet (foyer)
    simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
    simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
    df = simulation.get_results_dataframe(index_by_code=True)
    print simulation.P.fam.af.bmaf
    assert df.loc["af"][0] == 7239.12 
#   montant AF annuel brut de CRDS
    
    
 
if __name__ == '__main__':

    test_af2()
    nose.core.runmodule(argv=[__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)

