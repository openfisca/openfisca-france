from numpy import datetime64

from openfisca_france.model.base import *
from openfisca_core.periods import Instant 


class chomeur_longue_duree(Variable):
    cerfa_field = {
        0: "1AI",
        1: "1BI",
        2: "1CI",
        3: "1DI",
        4: "1EI",
        }
    value_type = bool
    entity = Individu
    label = "Demandeur d'emploi inscrit depuis plus d'un an"
    definition_period = YEAR
    # Pour toutes les variables de ce type, les pac3 ne sont plus proposés après 2007


class chomage_brut(Variable):
    value_type = float
    entity = Individu
    label = "Chômage brut"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add


class indemnites_chomage_partiel(Variable):
    value_type = float
    entity = Individu
    label = "Indemnités de chômage partiel"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class salaire_de_reference(Variable):
    value_type = float
    entity = Individu
    label = "Salaire de référence (SR)"
    definition_period = MONTH

    def formula(individu, period):
        sal_ref = 0 * individu('salaire_de_base', period)
        for months in range(0, 48):
            contrat_de_travail_fin_potentiel = period.offset(-months) 
            sal_ref = where(
                individu('contrat_de_travail_fin', period) == datetime64(contrat_de_travail_fin_potentiel.start),
                individu(
                    'salaire_de_base', 
                    contrat_de_travail_fin_potentiel.offset(-12).start.period('month', 12),
                    options = [ADD],
                    ),
                sal_ref,
                )
        return sal_ref

class nombre_jours_calendaires_12_derniers_mois(Variable):
    value_type = float
    entity = Individu
    label = "Jours travaillés sur les 12 derniers mois avant la rupture de contrat"
    definition_period = MONTH

    def formula(individu, period):
        nombre_jours_calendaires_reference = 0 * individu('nombre_jours_calendaires', period)
        for months in range(0, 48):
            contrat_de_travail_fin_potentiel = period.offset(-months) 
            nombre_jours_calendaires_reference = where(
                individu('contrat_de_travail_fin', period) == datetime64(contrat_de_travail_fin_potentiel.start),
                individu(
                    'nombre_jours_calendaires', 
                    contrat_de_travail_fin_potentiel.offset(-12).start.period('month', 12),
                    options = [ADD],
                    ),
                nombre_jours_calendaires_reference,
                )
        return nombre_jours_calendaires_reference



class salaire_de_reference_mensuel(Variable):
    value_type = float
    entity = Individu
    label = "Salaire de référence mensuel (SRM)"
    definition_period = MONTH

    def formula(individu, period):
         nombre_jours_calendaires_12_derniers_mois = individu('nombre_jours_calendaires_12_derniers_mois', period)
         salaire_de_reference = individu('salaire_de_reference', period)
         salaire_ref_mensuel = ((salaire_de_reference) / (nombre_jours_calendaires_12_derniers_mois * 1.4 )) * 30
         
         return salaire_ref_mensuel

class are(Variable):
    value_type = float
    entity = Individu
    label = "Allocation chômage d'aide au retour à l'emploi (ARE)"
    definition_period = MONTH
    
    def formula_2009_01(individu, period, parameters):
        salaire_de_reference_mensuel = individu('salaire_de_reference_mensuel', period)
        are = parameters(period).are
        montant_mensuel = max_(
            are.are_partie_fixe * 30 + are.pourcentage_du_sjr_complement * salaire_de_reference_mensuel, 
            are.pourcentage_du_sjr_seul * salaire_de_reference_mensuel
            )
        montant_plancher = max_(
            are.are_min * 30,
            montant_mensuel
        )
        montant_plafond = min_(
            montant_plancher,
            are.max_en_pourcentage_sjr * salaire_de_reference_mensuel
            )
        
        return montant_plafond

class are_eligibilite_individu(Variable):
    value_type = bool
    label = "Éligibilité individuelle à l'ARE"
    entity = Individu
    definition_period = MONTH
    reference = [
        "Unédic - Règlement général annexé à la convention du 6 mai 2011",
        "https://www.unedic.org/sites/default/files/regulations/RglACh11.pdf",
        ]
       
    #il faut résider en France, être involontairement privé d'emploi, être inscrit comme demandeur d'emploi, être à la recherche active et permanente d'un emploi, être physiquement apte à l'exercice d'un emploi. 


    def formula(individu, period, parameters):
        #critère de l'âge: ARE non versé si l'âge de départ à la retraite atteint, sauf en cas de taux plein non atteint. 
        #Pour simplifier, j'ai stipulé qu'on ne pouvait plus toucher d'ARE dès lors l'âge légal de départ à la retraite atteint.

        age_en_mois = individu('age_en_mois', period)
        age_condition = age_en_mois < parameters(period).are.age_legal_retraite
      
        return age_condition 


    
    
     
     
        
        
        
        
        
        