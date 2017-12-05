# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa analysis:ignore


class chomeur_longue_duree(Variable):
    cerfa_field = {QUIFOY['vous']: u"1AI",
        QUIFOY['conj']: u"1BI",
        QUIFOY['pac1']: u"1CI",
        QUIFOY['pac2']: u"1DI",
        QUIFOY['pac3']: u"1EI",
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
