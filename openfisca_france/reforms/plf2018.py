# -*- coding: utf-8 -*-

from __future__ import division

from datetime import date
import os

from ..model.base import *


dir_path = os.path.join(os.path.dirname(__file__), 'parameters')



class plf2018(Reform):
    name = u"Projet de Loi de Finances 2018 appliquée aux revenus 2018"

    class degrevement_taxe_habitation(Variable):
        value_type = bool
        default_value = True
        entity = Menage
        label = u"Exonération de la taxe d'habitation"
        reference = "http://vosdroits.service-public.fr/particuliers/F42.xhtml"
        definition_period = YEAR
    
        def formula(menage, period, parameters):
            """Exonation de la taxe d'habitation
    
            'men'
    
            Eligibilité:
            - âgé de plus de 60 ans, non soumis à l'impôt de solidarité sur la fortune (ISF) en n-1
            - veuf quel que soit votre âge et non soumis à l'impôt de solidarité sur la fortune (ISF) n-1
            - titulaire de l'allocation de solidarité aux personnes âgées (Aspa)  ou de l'allocation supplémentaire d'invalidité (Asi),
            bénéficiaire de l'allocation aux adultes handicapés (AAH),
            atteint d'une infirmité ou d'une invalidité vous empêchant de subvenir à vos besoins par votre travail.
            """
            janvier = period.first_month
    
            P = parameters(period).th
    
            statut_marital = menage.personne_de_reference('statut_marital', janvier)
    
            nbptr_i = menage.members.foyer_fiscal('nbptr', period)
            nbptr = menage.sum(nbptr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)  # TODO: Beurk
    
            rfr_i = menage.members.foyer_fiscal('rfr', period)
            rfr = menage.sum(rfr_i, role = FoyerFiscal.DECLARANT_PRINCIPAL)
    
            seuil_degrevement = P.degrevement.degrevement_th.plaf_degrevement_th_1 + P.degrevement.degrevement_th.plaf_degrevement_sup_th_1 * min_((max_(0, (nbptr - 1) / 2)),2) + P.degrevement.degrevement_th.plaf_degrevement_sup2_th_1 * min_((max_(0, (nbptr - 1) / 2)),2)
            
            elig = (rfr < seuil_degrevement) 
            return (elig)
          
          

    def apply(self):
        for variable in [self.degrevement_taxe_habitation]:
            self.update_variable(variable)
        self.modify_parameters(modifier_function = modify_parameters)
        
        
def modify_parameters(parameters):
    reform_year = 2018
    reform_period = period(reform_year)
    print(reform_period)
    
    
    # file_path = os.path.join(dir_path, 'plf2018.yaml')
    # plf2018_parameters_subtree = load_parameter_file(name='plf2018', file_path=file_path)
    # parameters.add_child('plf2018', plf2018_parameters_subtree)


    # #revalorisation du montant forfaitaire du RSA : le reste de la réforme du RSA/prime d'activité nécessite de coder une fonction supplémentaire
    # parameters.prestations.minima_sociaux.rsa.montant_de_base_du_rsa.update(period=reform_period, value=(545.48+20)) 
    # # Article 7 du PLFSS : Bascule CSG cotisations : 
    # # - hausse de la CSG sur les revenus d'activité
    # parameters.prelevements_sociaux.contributions.csg.activite.deductible.taux.update(period=reform_period, value=0.068)
    # # - hausse de la CSG sur les retraites
    # parameters.prelevements_sociaux.contributions.csg.retraite.deductible.taux_plein.update(period=reform_period, value=0.068)
    # # - suppression de la cotisation salariale d'assurance chomage en deux temps : 
    # # - suppression de la cotisation salariale maladie
    # parameters.cotsoc.children['cotisations_salarie'].children['prive_non_cadre'].children['maladie'][0].rate.update(start = reform_period, value=0.0)
    # parameters.cotsoc.children['cotisations_salarie'].children['prive_cadre'].children['maladie'][0].rate.update(start = reform_period, value=0.0)
    # # - une première baisse de 1,5 pt le 1er janvier 2018
    # parameters.cotsoc.children['cotisations_salarie'].children['prive_non_cadre'].children['assedic'][0].rate.update(start = "2018-01", value=0.009)
    # parameters.cotsoc.children['cotisations_salarie'].children['prive_cadre'].children['assedic'][0].rate.update(start = "2018-01", value=0.009)
    # # - la suppression du reliquat le 1er octobre 2018
    # parameters.cotsoc.children['cotisations_salarie'].children['prive_non_cadre'].children['assedic'][0].rate.update(start = "2018-10", value=0.0)
    # parameters.cotsoc.children['cotisations_salarie'].children['prive_cadre'].children['assedic'][0].rate.update(start = "2018-10", value=0.0)
    # # parameters.prelevements_sociaux.cotisations_sociales.chomage.salarie[0].rate.update(period=reform_period, value=0.0) #fonctionne pas
    # parameters.cotsoc.sal.commun.maladie[0].rate.update(period=reform_period, value=0.0) #fonctionne pas
    # # A voir si on le met : la réforme du minimum vieillesse
    # # parameters.prestations.minima_sociaux.aspa.montant_annuel_seul.update(period=reform_period, value=(9638.42+100*12))
    # # parameters.prestations.minima_sociaux.aspa.montant_annuel_couple.update(period=reform_period, value=(14963.65+100*12))

    return parameters

