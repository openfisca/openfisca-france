from openfisca_france.model.base import *


class retraite_de_base_n_1(Variable):
    value_type = float
    entity = Individu
    label = "Retraite brute de l'année passée"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add
    unit = 'currency'


class retraite_de_base(Variable):
    value_type = float
    entity = Individu
    label = 'Retraite de base'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add
    unit = 'currency'


class retraite_complementaire(Variable):
    value_type = float
    entity = Individu
    label = 'Retraite complémentaire'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add
    unit = 'currency'


class retraite_brute(Variable):
    unit = 'currency'
    value_type = float
    entity = Individu
    label = 'Retraites au sens strict imposables (rentes à titre onéreux exclues)'
    set_input = set_input_divide_by_period
    reference = 'http://vosdroits.service-public.fr/particuliers/F415.xhtml'
    definition_period = MONTH

    def formula(individu, period):
        retraite_de_base = individu('retraite_de_base', period)
        retraite_complementaire = individu('retraite_complementaire', period)

        return retraite_de_base + retraite_complementaire


class aer(Variable):
    value_type = int
    entity = Individu
    label = 'Allocation équivalent retraite (AER)'
    # L'AER est remplacée depuis le 1er juillet 2011 par l'allocation transitoire de solidarité (ATS).
    definition_period = MONTH
    set_input = set_input_divide_by_period
    unit = 'currency'


class retraite_combattant(Variable):
    value_type = float
    entity = Individu
    label = 'Retraite du combattant'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    unit = 'currency'
