# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa analysis:ignore


class retraite_brute(Variable):
    base_function = requested_period_added_value
    column = FloatCol()
    entity = Individu
    label = u"Retraite brute"
    set_input = set_input_divide_by_period


class aer(Variable):
    column = IntCol
    entity = Individu
    label = u"Allocation équivalent retraite (AER)"
    # L'AER est remplacée depuis le 1er juillet 2011 par l'allocation transitoire de solidarité (ATS).


class retraite_combattant(Variable):
    column = FloatCol
    entity = Individu
    label = u"Retraite du combattant"


