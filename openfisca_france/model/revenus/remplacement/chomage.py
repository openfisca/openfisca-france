from openfisca_france.model.base import *


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

    def formula(individu, period, parameters):
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)
        instant = contrat_de_travail_fin
        salaire_de_base = individu('salaire_de_base', instant.last_12_months, options=[ADD])

        return salaire_de_base

class salaire_journalier_de_reference_verse_par_mois(Variable):
    value_type = float
    entity = Individu
    label = "Salaire journalier de référence (SJR)"
    definition_period = MONTH

    def formula(individu,period,parameters):
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)
        instant = contrat_de_travail_fin
        salaire_de_base = individu('salaire_de_base', instant.last_12_months, options=[ADD])
        nombre_jours_travailles_calendaires = individu('nombre_jours_calendaires', instant.last_12_months, options=[ADD])
        salaire_journalier_de_reference = (salaire_de_reference / nombre_jours_travailles_calendaires) * 1,4 
        salaire_journalier_de_reference_verse_par_mois = salaire_journalier_de_reference * 30
        
        return salaire_journalier_de_reference_verse_par_mois



class are(Variable):
    value_type = float
    entity = Individu
    label = "Allocation chômage d'aide au retour à l'emploi (ARE)"
    definition_period = MONTH
    
    def formula_2009_01(individu, period, parameters):
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)
        instant = contrat_de_travail_fin
        salaire_de_reference = individu('salaire_de_reference', instant.last_12_months, options=[ADD])
        

        montant_journalier = max_(parameters.ARE.partie_fixe + (parameters.ARE.%_du_SJR_complement * salaire_journalier_de_reference), parameters.ARE.%_du_SJR_seul * salaire_journalier_de_reference)
        montant_mensuel = montant_journalier * 30
        plafond_mensuel = parameters.ARE.max_en_%_SJR * salaire_journalier_de_reference_verse_par_mois
        plancher_mensuel = parameters.ARE.min * salaire_journalier_de_reference_verse_par_mois
        plafond_mensuel > montant_mensuel
        plancher_mensuel < montant_mensuel
        
        return montant_mensuel



class are_eligibilite_individu_2011(Variable):
    value_type = bool
    label = "Éligibilité individuelle à l'ARE"
    entity = Individu
    definition_period = MONTH
    reference = [
        "Unédic - Règlement général annexé à la convention du 6 mai 2011",
        "https://www.unedic.org/sites/default/files/regulations/RglACh11.pdf",
        ]

#il faut résider en France, être involontairement privé d'emploi, être inscrit comme demandeur d'emploi, être à la recherche active et permanente d'un emploi, être physiquement apte à l'exercice d'un emploi. 


    def formula_2011(individu, period, parameters):
        #critère de l'âge : ARE non versé si l'âge de départ à la retraite atteint, sauf en cas de taux plein non atteint
        age_max = parameters(period).prestations.minima_sociaux.aah.age_legal_retraite
        sous_age_limite = individu('age_en_mois', period) <= age_max

        #conditions d'attribution de l'ARE en fonction de la période d'affiliation 

     
    
        




 
    
    



