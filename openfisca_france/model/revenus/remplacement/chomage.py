# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa analysis:ignore


class chomeur_longue_duree(Variable):
    cerfa_field = {0: u"1AI",
        1: u"1BI",
        2: u"1CI",
        3: u"1DI",
        4: u"1EI",
        }
    value_type = bool
    entity = Individu
    label = u"Demandeur d'emploi inscrit depuis plus d'un an"
    definition_period = YEAR
    # Pour toutes les variables de ce type, les pac3 ne sont plus proposés après 2007


class chomage_brut(Variable):
    value_type = float
    entity = Individu
    label = u"Chômage brut"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add


class indemnites_chomage_partiel(Variable):
    value_type = float
    entity = Individu
    label = u"Indemnités de chômage partiel"
    definition_period = MONTH
    set_input = set_input_divide_by_period
