# -*- coding: utf-8 -*-

from __future__ import division

from datetime import date
import os

from ..model.base import *


dir_path = os.path.join(os.path.dirname(__file__), 'parameters')



class plf2018(Reform):
    name = u"Projet de Loi de Finances 2018 appliquée aux revenus 2018"


    def apply(self):
        self.modify_parameters(modifier_function = modify_parameters)
        
        
def modify_parameters(parameters):
    reform_year = 2018
    reform_period = period(reform_year)
    print(reform_period)
  
    #revalorisation du montant forfaitaire du RSA : le reste de la réforme du RSA/prime d'activité nécessite de coder une fonction supplémentaire
    parameters.prestations.minima_sociaux.rsa.montant_de_base_du_rsa.update(period=reform_period, value=(545.48+20))
    # Article 3 du PLF : dégrèvement de TH :
    parameters.th.degrevement.taux.update(period=reform_period, value=0.3)
    
    
    
    
    # Article 7 du PLFSS : Bascule CSG cotisations :
    # - hausse de la CSG sur les revenus d'activité
    parameters.prelevements_sociaux.contributions.csg.activite.deductible.taux.update(period=reform_period, value=0.068)
    # - hausse de la CSG sur les retraites
    parameters.prelevements_sociaux.contributions.csg.retraite.deductible.taux_plein.update(period=reform_period, value=0.068)
    # - suppression de la cotisation salariale d'assurance chomage en deux temps :
    # - suppression de la cotisation salariale maladie
    parameters.cotsoc.children['cotisations_salarie'].children['prive_non_cadre'].children['maladie'][0].rate.update(start = reform_period, value=0.0)
    parameters.cotsoc.children['cotisations_salarie'].children['prive_cadre'].children['maladie'][0].rate.update(start = reform_period, value=0.0)
    # - une première baisse de 1,5 pt le 1er janvier 2018
    parameters.cotsoc.children['cotisations_salarie'].children['prive_non_cadre'].children['assedic'][0].rate.update(start = "2018-01", value=0.009)
    parameters.cotsoc.children['cotisations_salarie'].children['prive_cadre'].children['assedic'][0].rate.update(start = "2018-01", value=0.009)
    # - la suppression du reliquat le 1er octobre 2018
    parameters.cotsoc.children['cotisations_salarie'].children['prive_non_cadre'].children['assedic'][0].rate.update(start = "2018-10", value=0.0)
    parameters.cotsoc.children['cotisations_salarie'].children['prive_cadre'].children['assedic'][0].rate.update(start = "2018-10", value=0.0)
    # parameters.prelevements_sociaux.cotisations_sociales.chomage.salarie[0].rate.update(period=reform_period, value=0.0) #fonctionne pas
    parameters.cotsoc.sal.commun.maladie[0].rate.update(period=reform_period, value=0.0) #fonctionne pas
    # A voir si on le met : la réforme du minimum vieillesse
    # parameters.prestations.minima_sociaux.aspa.montant_annuel_seul.update(period=reform_period, value=(9638.42+100*12))
    # parameters.prestations.minima_sociaux.aspa.montant_annuel_couple.update(period=reform_period, value=(14963.65+100*12))

    return parameters

