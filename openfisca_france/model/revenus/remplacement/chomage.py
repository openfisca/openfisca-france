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
        salaire_de_base = individu('salaire_de_base', period)
        salaire_de_base_M_1 = individu('salaire_de_base', period.offset(-1, 'month'))
        salaire_de_base_M_2 = individu('salaire_de_base', period.offset(-2, 'month'))
        salaire_de_base_M_3 = individu('salaire_de_base', period.offset(-3, 'month'))
        salaire_de_base_M_4 = individu('salaire_de_base', period.offset(-4, 'month'))
        salaire_de_base_M_5 = individu('salaire_de_base', period.offset(-5, 'month'))
        salaire_de_base_M_6 = individu('salaire_de_base', period.offset(-6, 'month'))
        salaire_de_base_M_7 = individu('salaire_de_base', period.offset(-7, 'month'))
        salaire_de_base_M_8 = individu('salaire_de_base', period.offset(-8, 'month'))
        salaire_de_base_M_9 = individu('salaire_de_base', period.offset(-9, 'month'))
        salaire_de_base_M_10 = individu('salaire_de_base', period.offset(-10, 'month'))
        salaire_de_base_M_11 = individu('salaire_de_base', period.offset(-11, 'month'))
        salaire_de_base_M_12 = individu('salaire_de_base', period.offset(-12, 'month'))
        salaire_de_base_M_13 = individu('salaire_de_base', period.offset(-13, 'month'))
        salaire_de_base_M_14 = individu('salaire_de_base', period.offset(-14, 'month'))
        salaire_de_base_M_15 = individu('salaire_de_base', period.offset(-15, 'month'))
        salaire_de_base_M_16 = individu('salaire_de_base', period.offset(-16, 'month'))
        salaire_de_base_M_17 = individu('salaire_de_base', period.offset(-17, 'month'))
        salaire_de_base_M_18 = individu('salaire_de_base', period.offset(-18, 'month'))
        salaire_de_base_M_19 = individu('salaire_de_base', period.offset(-19, 'month'))
        salaire_de_base_M_20 = individu('salaire_de_base', period.offset(-20, 'month'))
        salaire_de_base_M_21 = individu('salaire_de_base', period.offset(-21, 'month'))
        salaire_de_base_M_22 = individu('salaire_de_base', period.offset(-22, 'month'))
        salaire_de_base_M_23 = individu('salaire_de_base', period.offset(-23, 'month'))
        salaire_de_base_M_24 = individu('salaire_de_base', period.offset(-24, 'month'))
        salaire_de_base_M_25 = individu('salaire_de_base', period.offset(-25, 'month'))
        salaire_de_base_M_26 = individu('salaire_de_base', period.offset(-26, 'month'))
        salaire_de_base_M_27 = individu('salaire_de_base', period.offset(-27, 'month'))
        salaire_de_base_M_28 = individu('salaire_de_base', period.offset(-28, 'month'))
        salaire_de_base_M_29 = individu('salaire_de_base', period.offset(-29, 'month'))
        salaire_de_base_M_30 = individu('salaire_de_base', period.offset(-30, 'month'))
        salaire_de_base_M_31 = individu('salaire_de_base', period.offset(-31, 'month'))
        salaire_de_base_M_32 = individu('salaire_de_base', period.offset(-32, 'month'))
        salaire_de_base_M_33 = individu('salaire_de_base', period.offset(-33, 'month'))
        salaire_de_base_M_34 = individu('salaire_de_base', period.offset(-34, 'month'))
        salaire_de_base_M_35 = individu('salaire_de_base', period.offset(-35, 'month'))
        salaire_de_base_M_36 = individu('salaire_de_base', period.offset(-36, 'month'))
        salaire_de_base_M_37 = individu('salaire_de_base', period.offset(-37, 'month'))
        salaire_de_base_M_38 = individu('salaire_de_base', period.offset(-38, 'month'))
        salaire_de_base_M_39 = individu('salaire_de_base', period.offset(-39, 'month'))
        salaire_de_base_M_40 = individu('salaire_de_base', period.offset(-40, 'month'))
        salaire_de_base_M_41 = individu('salaire_de_base', period.offset(-41, 'month'))
        salaire_de_base_M_42 = individu('salaire_de_base', period.offset(-42, 'month'))
        salaire_de_base_M_43 = individu('salaire_de_base', period.offset(-43, 'month'))
        salaire_de_base_M_44 = individu('salaire_de_base', period.offset(-44, 'month'))
        salaire_de_base_M_45 = individu('salaire_de_base', period.offset(-45, 'month'))
        salaire_de_base_M_46 = individu('salaire_de_base', period.offset(-46, 'month'))
        salaire_de_base_M_47 = individu('salaire_de_base', period.offset(-47, 'month'))
        salaire_de_base_M_48 = individu('salaire_de_base', period.offset(-48, 'month'))
        salaire_de_base_M_49 = individu('salaire_de_base', period.offset(-49, 'month'))


        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)
        contrat_de_travail_fin_M_12 = contrat_de_travail_fin - timedelta(months = 12)

       

        return salaire_de_reference







     
    
        




 
    
    



