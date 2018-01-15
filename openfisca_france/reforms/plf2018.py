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

    ########################################
    # Article 3 du PLF : dégrèvement de TH :
    ########################################
    parameters.th.degrevement.taux.update(start="2018-01", value=0.3)
    parameters.th.degrevement.taux.update(start="2019-01", value=0.65)
    parameters.th.degrevement.taux.update(start="2020-01", value=1.0)
    #############################################################
    # Article 63 du PLF : revalorisation de la prime d'activité
    ############################################################
    #revalorisation du montant forfaitaire du RSA : le reste de la réforme du RSA/prime d'activité nécessite de coder une fonction supplémentaire
    parameters.prestations.minima_sociaux.ppa.montant_de_base.update(start="2018-10", value=546.25)
    parameters.prestations.minima_sociaux.ppa.pente.update(start="2018-10", value=0.61)
    # # création du surbonus de prime d'activité
    parameters.prestations.minima_sociaux.ppa.sur_bonification.montant_sur_bonification_max.update(period="2019", value=(20))
    parameters.prestations.minima_sociaux.ppa.sur_bonification.montant_sur_bonification_max.update(period="2020", value=(40))
    parameters.prestations.minima_sociaux.ppa.sur_bonification.montant_sur_bonification_max.update(period="2021", value=(60))
    parameters.prestations.minima_sociaux.ppa.sur_bonification.montant_sur_bonification_max.update(period="2022", value=(60))
    #     
    
    #################################################
    # Article 7 du PLFSS : Bascule CSG cotisations :
    #################################################
    # - hausse de la CSG sur les revenus d'activité
    parameters.prelevements_sociaux.contributions.csg.activite.deductible.taux.update(start="2018-01", value=0.068)
    # - hausse de la CSG sur les retraites
    parameters.prelevements_sociaux.contributions.csg.retraite.deductible.taux_plein.update(start="2018-01", value=0.059)
    # - suppression de la cotisation salariale maladie
    parameters.cotsoc.children['cotisations_salarie'].children['prive_non_cadre'].children['maladie'][0].rate.update(start = reform_period, value=0.0)
    # parameters.cotsoc.children['cotisations_salarie'].children['prive_cadre'].children['maladie'][0].rate.update(start = reform_period, value=0.0)
    # - suppression de la cotisation salariale d'assurance chomage en deux temps :
    # # - une première baisse de 1,5 pt le 1er janvier 2018
    parameters.cotsoc.children['cotisations_salarie'].children['prive_non_cadre'].children['assedic'][0].rate.update(start = "2018", value=0.0095)
    # parameters.cotsoc.children['cotisations_salarie'].children['prive_cadre'].children['assedic'][0].rate.update(start =  "2018", value=0.009)
    # - la suppression du reliquat le 1er octobre 2018
    parameters.cotsoc.children['cotisations_salarie'].children['prive_non_cadre'].children['assedic'][0].rate.update(start = "2018-10", value=0.000)
    # parameters.cotsoc.children['cotisations_salarie'].children['prive_cadre'].children['assedic'][0].rate.update(start = "2018-10", value=0.000)
    # - neutralisation de la hausse de CSG pour les fonctionnaires : énorme workaround, car en réalité c'est beaucup plus complexe.
    parameters.cotsoc.children['cotisations_salarie'].children['public_titulaire_etat'].children['pension'][0].rate.update(start = "2018-01", value=0.1001-0.0171) #vérifier la date d'entrée en vigueur.
    parameters.cotsoc.children['cotisations_salarie'].children['public_titulaire_etat'].children['pension'][0].rate.update(start = "2019-01", value=0.1028-0.0171) #vérifier la date d'entrée en vigueur.
    parameters.cotsoc.children['cotisations_salarie'].children['public_titulaire_etat'].children['pension'][0].rate.update(start = "2020-01", value=0.1055-0.0171) #vérifier la date d'entrée en vigueur.
    # - baisse des cotisations famille sur les indépendants
    # parameters.prelevements_sociaux.famille_ind.si_revenu_d_activite_140_pss.update(start = "2018-01",value = 0.0)

    #######################################################################
    # Article 28 du PLFSS : revalorisation du minimum vieillesse sur 3 ans:
    #######################################################################
    parameters.prestations.minima_sociaux.aspa.montant_annuel_seul.update(start = "2018-04-01", value=(9638.42+30*12))
    parameters.prestations.minima_sociaux.aspa.plafond_ressources_seul.update(start = "2018-04-01", value=(9638.42+30*12))
    parameters.prestations.minima_sociaux.aspa.montant_annuel_seul.update(start = "2019-01-01", value=(9638.42+65*12))
    parameters.prestations.minima_sociaux.aspa.plafond_ressources_seul.update(start = "2019-01-01", value=(9638.42+65*12))
    parameters.prestations.minima_sociaux.aspa.montant_annuel_seul.update(start = "2020-01-01", value=(9638.42+100*12))
    parameters.prestations.minima_sociaux.aspa.plafond_ressources_seul.update(start = "2020-01-01", value=(9638.42+100*12))
    
    parameters.prestations.minima_sociaux.aspa.montant_annuel_couple.update(start = "2018-04-01", value=(14963.65+46.6*12))
    parameters.prestations.minima_sociaux.aspa.plafond_ressources_couple.update(start = "2018-04-01", value=(14963.65+46.6*12))
    parameters.prestations.minima_sociaux.aspa.montant_annuel_couple.update(start = "2019-01-01", value=(14963.65+101*12))
    parameters.prestations.minima_sociaux.aspa.plafond_ressources_couple.update(start = "2019-01-01", value=(14963.65+101*12))
    parameters.prestations.minima_sociaux.aspa.montant_annuel_couple.update(start = "2020-01-01", value=(14963.65+155.2*12))
    parameters.prestations.minima_sociaux.aspa.plafond_ressources_couple.update(start = "2020-01-01", value=(14963.65+155.2*12))
    
    parameters.prestations.minima_sociaux.aah.montant.update(start = "2018-12-01", value=(860))
    parameters.prestations.minima_sociaux.aah.montant.update(start = "2019-12-01", value=(900))
    
    
    #######################################################################
    # Baisse forfaitaire des APL
    #######################################################################
    parameters.prestations.aides_logement.autres.abattement_forfaitaire.update(start = "2017-10-01", value=(5))

    return parameters

