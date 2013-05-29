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



"""
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


''' test sur un revenu des actions (2DA) de 20 000 € '''


irppa = {2010: 0, 2011 : 0}

def test_irpp_a20000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  
#       case non individualisables
#        test_case.indiv[0].update({"sali":0})
        test_case.declar[0].update({"f2da":20000})   
        df = simulation.get_results_dataframe(index_by_code=True)

#        print test_case
#        print df.to_string()
#        print test_case.indiv[0]

#        print test_case.declar[0]
#        print irpp[yr]
#        print abs(df.loc["irpp"][0] - irpp[yr]) < 1e-3
        print  df.loc["irpp"][0]
#        print  irpp[yr]      
        assert abs(df.loc["irpp"][0] - irppa[yr]) < 1 
#       montant de l'irpp


''' test sur un revenu des actions (2DA) de 50 000 € ''' 




irppa1 = {2010: 0, 2011 : 0}

def test_irpp_a150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  

#       case non individualisables
        test_case.declar[0].update({"f2da":50000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
    
        assert abs(df.loc["irpp"][0] - irppa1[yr]) < 1 
#       montant de l'irpp


''' test sur un revenu des actions (2DA) de 150 000 € ''' 


irppa2 = {2010: 0, 2011 : 0}

def test_irpp_a2150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  

#       case non individualisables
        test_case.declar[0].update({"f2da":150000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
    
        assert abs(df.loc["irpp"][0] - irppa2[yr]) < 1 
#       montant de l'irpp






''' test sur le revenu des actions et parts (2DC) de 20 000 € '''


irppdc = {2010: 0, 2011 : 0}

def test_irpp_dc20000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  
#       case non individualisables
#        test_case.indiv[0].update({"sali":0})
        test_case.declar[0].update({"f2dc":20000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
  
        assert abs(df.loc["irpp"][0] - irppdc[yr]) < 1 
#       montant de l'irpp


''' test sur le revenu des actions et parts (2DC) de 50 000 € ''' 


irppdc1 = {2010: -2976, 2011 : -2976}

def test_irpp_dc150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  

#       case non individualisables
        test_case.declar[0].update({"f2dc":50000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
    
        assert abs(df.loc["irpp"][0] - irppdc1[yr]) < 1 
#       montant de l'irpp


''' test sur le revenu des actions et parts (2DC) de 150 000 € ''' 


irppdc2 = {2010: -22917, 2011 : -22917}

def test_irpp_dc2150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  

#       case non individualisables
        test_case.declar[0].update({"f2dc":150000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
    
        assert abs(df.loc["irpp"][0] - irppdc2[yr]) < 1 
#       montant de l'irpp



''' test sur le revenu de valeurs mobilières (2TS) de 20 000 € '''

irppts = {2010: -1461, 2011 : -1461}

def test_irpp_ts20000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  
#       case non individualisables
        test_case.declar[0].update({"f2ts":20000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
  
        assert abs(df.loc["irpp"][0] - irppts[yr]) < 1 
#       montant de l'irpp


''' test sur le revenu de valeurs mobilières (2TS) de 50 000 € ''' 


irppts1 = {2010: -9434, 2011 : -9434}

def test_irpp_ts150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  
#       case non individualisables
        test_case.declar[0].update({"f2ts":50000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
    
        assert abs(df.loc["irpp"][0] - irppts1[yr]) < 1 
#       montant de l'irpp


''' test sur le revenu de valeurs mobilières (2TS) de 150 000 € ''' 


irppts2 = {2010: -48142, 2011 : -48142}

def test_irpp_ts2150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  

#       case non individualisables
        test_case.declar[0].update({"f2ts":150000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
    
        assert abs(df.loc["irpp"][0] - irppts2[yr]) < 1 
#       montant de l'irpp


''' test sur les intérêts (2TR) de 20 000 € '''

irpptr = {2010: -1461, 2011 : -1461}

def test_irpp_tr20000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  
#       case non individualisables
        test_case.declar[0].update({"f2tr":20000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
  
        assert abs(df.loc["irpp"][0] - irpptr[yr]) < 1 
#       montant de l'irpp


''' test sur les intérêts (2TR) de 50 000 € ''' 


irpptr1 = {2010: -9434, 2011 : -9434}

def test_irpp_tr150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  
#       case non individualisables
        test_case.declar[0].update({"f2tr":50000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
    
        assert abs(df.loc["irpp"][0] - irpptr1[yr]) < 1 
#       montant de l'irpp


''' test sur les intérêts (2TR) de 150 000 € ''' 


irpptr2 = {2010: -48142, 2011 : -48142}

def test_irpp_tr2150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  

#       case non individualisables
        test_case.declar[0].update({"f2tr":150000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
    
        assert abs(df.loc["irpp"][0] - irpptr2[yr]) < 1 
#       montant de l'irpp


''' test sur les revenus fonciers (4BA) de 20 000 € '''

irppba = {2010: -1461, 2011 : -1461}

def test_irpp_ba20000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  
#       case non individualisables
        test_case.declar[0].update({"f4ba":20000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
  
        assert abs(df.loc["irpp"][0] - irppba[yr]) < 1 
#       montant de l'irpp


''' test sur les revenus fonciers (4BA) de 50 000 € ''' 


irppba1 = {2010: -9434, 2011 : -9434}

def test_irpp_ba150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  
#       case non individualisables
        test_case.declar[0].update({"f4ba":50000})   
        df = simulation.get_results_dataframe(index_by_code=True)
    
        assert abs(df.loc["irpp"][0] - irppba1[yr]) < 1 
#       montant de l'irpp


''' test sur les revenus fonciers (4BA) de 150 000 € ''' 


irppba2 = {2010: -48142, 2011 : -48142}

def test_irpp_ba2150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  

#       case non individualisables
        test_case.declar[0].update({"f4ba":150000})   
        df = simulation.get_results_dataframe(index_by_code=True)
  
        assert abs(df.loc["irpp"][0] - irppba2[yr]) < 1 
#       montant de l'irpp


''' test sur les plus-values mobilières (3VG) de 20 000 € '''

irppvg = {2010: -3600, 2011 : -3800}

def test_irpp_vg20000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  
#       case non individualisables
        test_case.declar[0].update({"f3vg":20000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
  
        assert abs(df.loc["irpp"][0] - irppvg[yr]) < 1 
#       montant de l'irpp


''' test sur les plus-values mobilières (3VG) de 50 000 € ''' 


irppvg1 = {2010: -9000, 2011 : -9500}

def test_irpp_vg150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  
#       case non individualisables
        test_case.declar[0].update({"f3vg":50000})   
        df = simulation.get_results_dataframe(index_by_code=True)
    
        assert abs(df.loc["irpp"][0] - irppvg1[yr]) < 1 
#       montant de l'irpp


''' test sur les plus-values mobilières (3VG) de 150 000 € ''' 


irppvg2 = {2010: -27000, 2011 : -28500}

def test_irpp_vg2150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  

#       case non individualisables
        test_case.declar[0].update({"f3vg":150000})   
        df = simulation.get_results_dataframe(index_by_code=True)
  
        assert abs(df.loc["irpp"][0] - irppvg2[yr]) < 1 
#       montant de l'irpp
"""

''' test sur une assurance vie (2DH) de 20 000 € '''


irppdh = {2010: 345, 2011 : 345}

def test_irpp_dh20000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  
#       case non individualisables
#        test_case.indiv[0].update({"sali":0})
        test_case.declar[0].update({"f2dh":20000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
  
        assert abs(df.loc["irpp"][0] - irppdh[yr]) < 1 
#       montant de l'irpp


''' test sur une assurance vie (2DH) de 50 000 € ''' 


irppdh1 = {2010: 345, 2011 : 345}

def test_irpp_dh150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  

#       case non individualisables
        test_case.declar[0].update({"f2dh":50000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
    
        assert abs(df.loc["irpp"][0] - irppdh1[yr]) < 1 
#       montant de l'irpp


''' test sur une assurance vie (2DH) de 150 000 € ''' 


irppdh2 = {2010: 345, 2011 : 345}

def test_irpp_dh2150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  

#       case non individualisables
        test_case.declar[0].update({"f2dh":150000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
    
        assert abs(df.loc["irpp"][0] - irppdh2[yr]) < 1 
#       montant de l'irpp


''' test sur les plus-values immobilières (3VZ) de 20 000 € '''

irppvz = {2010: 0, 2011 : 0}

def test_irpp_vz20000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  
#       case non individualisables
        test_case.declar[0].update({"f3vz":20000})   
        df = simulation.get_results_dataframe(index_by_code=True)

        print  df.loc["irpp"][0]
  
        assert abs(df.loc["irpp"][0] - irppvz[yr]) < 1 
#       montant de l'irpp


''' test sur les plus-values immobilières (3VZ) de 50 000 € ''' 


irppvz1 = {2010: 0, 2011 : 0}

def test_irpp_vz150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  
#       case non individualisables
        test_case.declar[0].update({"f3vz":50000})   
        df = simulation.get_results_dataframe(index_by_code=True)
    
        assert abs(df.loc["irpp"][0] - irppvz1[yr]) < 1 
#       montant de l'irpp


''' test sur les plus-values immobilières (3V) de 150 000 € ''' 


irppvz2 = {2010: 0, 2011 : 0}

def test_irpp_vz2150000():
    country = 'france'
    for yr in range(2010,2012):
        simulation = ScenarioSimulation()
        simulation.set_config(year = yr, country = country, nmen = 1)
        simulation.set_param()
        
        test_case = simulation.scenario  

#       case non individualisables
        test_case.declar[0].update({"f3vz":150000})   
        df = simulation.get_results_dataframe(index_by_code=True)
  
        assert abs(df.loc["irpp"][0] - irppvz2[yr]) < 1 
#       montant de l'irpp



if __name__ == '__main__':
   
#    test_irpp_20000()
#    test_irpp_a20000()
#    test_irpp_dc20000()
#    test_irpp_ts20000()
#    test_irpp_tr20000()
#    test_irpp_ba20000()
#    test_irpp_vg20000()
    test_irpp_dh20000()
    test_irpp_vz20000()
    
    nose.core.runmodule(argv=[__file__, '-v', '-i test_*.py'])
#     nose.core.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'], exit=False)



