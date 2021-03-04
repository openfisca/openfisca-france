from openfisca_france.model.base import *
from openfisca_core.periods import Instant 
from datetime import timedelta

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

        for month in range(0, 37):
            sal_ref = where(
                individu('contrat_de_travail_fin', period) == period.offset(-month),
                individu('salaire_de_base', period.first_month.start.period('month', 12).offset(-(12 - month + 1)),options = [ADD]),
                sal_ref
                )
                
        return sal_ref







     
    
        




 
    
    



