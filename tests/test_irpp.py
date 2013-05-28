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




''' test pour un célibataire ayant un revenu salarial (1AJ) de 20 000 € '''


irpp = {2010: -1181, 2011 : -1181}

def test_irpp_20000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)

        simulation.set_param()
        test_case = simulation.scenario  
        test_case.indiv[0].update({"sali":20000})

#pour les cases non individualisables
#       test_case.declar[0].update({"f2tr":20000})   

        
        # Adding children on the same tax sheet (foyer)
#        simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
#        simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
        df = simulation.get_results_dataframe(index_by_code=True)

#        print test_case
#        print df.to_string()
#        print test_case.indiv[0]
#        print test_case.declar[0]
#        print irpp[yr]
#        print abs(df.loc["irpp"][0] - irpp[yr]) < 1e-3
#        print  df.loc["irpp"][0]
#        print  irpp[yr]      
        assert abs(df.loc["irpp"][0] - irpp[yr]) < 1 
#       montant de l'irpp


''' test pour un célibataire ayant un revenu salarial (1AJ) de 50 000 € '''


irpp1 = {2010: -7934, 2011 : -7934}

def test_irpp_50000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)

        simulation.set_param()
        test_case = simulation.scenario  
        test_case.indiv[0].update({"sali":50000})

#pour les cases non individualisables
#       test_case.declar[0].update({"f2tr":20000})   

        
        # Adding children on the same tax sheet (foyer)
#        simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
#        simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
        df = simulation.get_results_dataframe(index_by_code=True)


#        print test_case
#        print df.to_string()
#        print test_case.indiv[0]
#        print test_case.declar[0]
#        print irpp[yr]
#        print abs(df.loc["irpp"][0] - irpp[yr]) < 1e-3
#        print  df.loc["irpp"][0]
#        print  irpp[yr]      
        assert abs(df.loc["irpp"][0] - irpp1[yr]) < 1 
#       montant de l'irpp

''' test pour un célibataire ayant un revenu salarial (1AJ) de 150 000 € '''


irpp2 = {2010: -42338, 2011 : -42338}

def test_irpp_150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)

        simulation.set_param()
        test_case = simulation.scenario  
        test_case.indiv[0].update({"sali":150000})

#pour les cases non individualisables
#       test_case.declar[0].update({"f2tr":20000})   

        
        # Adding children on the same tax sheet (foyer)
#        simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
#        simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
        df = simulation.get_results_dataframe(index_by_code=True)
#        print test_case
#        print df.to_string()
 #       print test_case.indiv[0]
#        print test_case.declar[0]
#        print irpp[yr]
#        print abs(df.loc["irpp"][0] - irpp[yr]) < 1e-3
#        print  df.loc["irpp"][0]
#        print  irpp[yr]      
        assert abs(df.loc["irpp"][0] - irpp2[yr]) < 1 
#       montant de l'irpp





''' test pour un retraité célibataire ayant une pension (1AS) de 20 000 € '''


irppr = {2010: -1181, 2011 : -1181}

def test_irpp_r20000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)

        simulation.set_param()
        test_case = simulation.scenario  
        test_case.indiv[0].update({"rsti":20000})

#pour les cases non individualisables
#       test_case.declar[0].update({"f2tr":20000})   

        
        # Adding children on the same tax sheet (foyer)
#        simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
#        simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
        df = simulation.get_results_dataframe(index_by_code=True)

#        print test_case
#        print df.to_string()
#        print test_case.indiv[0]
#        print test_case.declar[0]
#        print irpp[yr]
#        print abs(df.loc["irpp"][0] - irpp[yr]) < 1e-3
#        print  df.loc["irpp"][0]
#        print  irpp[yr]      
        assert abs(df.loc["irpp"][0] - irppr[yr]) < 1 
#       montant de l'irpp


''' test pour un retraité célibataire ayant une pensio (1AS) de 50 000 € '''


irppr1 = {2010: -8336, 2011 : -8336}

def test_irppr_50000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)

        simulation.set_param()
        test_case = simulation.scenario  
        test_case.indiv[0].update({"rsti":50000})

#pour les cases non individualisables
#       test_case.declar[0].update({"f2tr":20000})   

        
        # Adding children on the same tax sheet (foyer)
#        simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
#        simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
        df = simulation.get_results_dataframe(index_by_code=True)


#        print test_case
#        print df.to_string()
#        print test_case.indiv[0]
#        print test_case.declar[0]
#        print irpp[yr]
#        print abs(df.loc["irpp"][0] - irppr1[yr]) < 1
#        print  df.loc["irpp"][0]
#        print  irpp[yr]      
        assert abs(df.loc["irpp"][0] - irppr1[yr]) < 1 
#       montant de l'irpp

''' test pour un retraité célibataire ayant une pension (1AS) de 150 000 € '''


irppr2 = {2010: -46642, 2011 : -46642}

def test_irpp_r150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)

        simulation.set_param()
        test_case = simulation.scenario  
        test_case.indiv[0].update({"rsti":150000})

#pour les cases non individualisables
#       test_case.declar[0].update({"f2tr":20000})   

        
        # Adding children on the same tax sheet (foyer)
#        simulation.scenario.addIndiv(3, datetime(2000,1,1).date(), 'pac', 'enf')
#        simulation.scenario.addIndiv(4, datetime(2000,1,1).date(), 'pac', 'enf')    
        df = simulation.get_results_dataframe(index_by_code=True)
#        print test_case
#        print df.to_string()
 #       print test_case.indiv[0]
#        print test_case.declar[0]
#        print irpp[yr]
#       print abs(df.loc["irpp"][0] - irppr2[yr]) < 1
        print  df.loc["irpp"][0]
#        print  irpp[yr]      
        assert abs(df.loc["irpp"][0] - irppr2[yr]) < 1 
#       montant de l'irpp










if __name__ == '__main__':
   
    test_irpp_20000()
  

    nose.core.runmodule(argv=[__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)



