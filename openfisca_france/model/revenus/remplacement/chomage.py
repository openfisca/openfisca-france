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
    label = "Chômage brut (revenus de remplacement pour les demandeurs d'emploi)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula(individu, period):
        return individu("allocation_retour_emploi", period)


class indemnites_chomage_partiel(Variable):
    value_type = float
    entity = Individu
    label = "Indemnités de chômage partiel"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class allocation_retour_emploi(Variable):
    value_type = float
    entity = Individu
    label = "Allocation chômage d'aide au retour à l'emploi (ARE)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000006178163/"


class allocation_travailleur_independant(Variable):
    value_type = float
    entity = Individu
    label = "Allocation des travailleurs indépendants (ATI)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000037388330/"
    documentation = '''
    Indemnisation de Pôle emploi en vigueur à partir du 1er novembre 2019 à destination
    des travailleurs non salariés indépendants contraints de mettre fin à leur activité.
    '''
