# -*- coding: utf-8 -*-

from openfisca_france.model.base import *


class retraite_brute(Variable):
    value_type = float
    entity = Individu
    label = "Retraite brute"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add


class aer(Variable):
    value_type = int
    entity = Individu
    label = "Allocation équivalent retraite (AER)"
    # L'AER est remplacée depuis le 1er juillet 2011 par l'allocation transitoire de solidarité (ATS).
    definition_period = MONTH


class retraite_combattant(Variable):
    value_type = float
    entity = Individu
    label = "Retraite du combattant"
    definition_period = MONTH
    set_input = set_input_divide_by_period
