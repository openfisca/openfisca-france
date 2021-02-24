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






class are(Variable):
    value_type = float
    entity = Individu
    label = "Allocation chômage d'aide au retour à l'emploi (ARE)"
    definition_period = DAY
    
    def formula_2009_01(individu, period, parameters):
        salaire_de_base = individu('salaire_de_base', period)
        salaire_de_base_reference = individu('salaire_de_base', period.last_year, options=[ADD])
        salaire_de_base_reference_journalier = individu('salaire_de_base_reference_journalier', period)

        montant_journalier = max_(base_params.fixe_6_ + salaire_de_base_reference_journalier * base_params.prct_6_, salaire_de_base_reference_journalier * base_params.prct)
        plafond_mensuel = base_params.base_max * salaire_de_base_reference_journalier
        plancher_mensuel = base_params.min_3









        return montant_journalier

class salaire_de_base_reference_journalier(Variable):
    value_type = float
    entity = Individu
    label = "Salaire journalier de référence (SJR)"
    definition_period = DAY

    def formula(individu, period, parameters):
        nombre_jours_travailles_calendaires = individu('nombre_jours_calendaires', period.last_year, options=[ADD])
        result = (salaire_de_base_reference / nombre_jours_travailles_calendaires) * 1,4 
         
        return result

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

     
    
        




 
    
    



