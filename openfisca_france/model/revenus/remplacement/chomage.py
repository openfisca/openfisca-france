# -*- coding: utf-8 -*-

from openfisca_france.model.base import *  # noqa analysis:ignore


class chomeur_longue_duree(Variable):
    cerfa_field = {QUIFOY['vous']: u"1AI",
        QUIFOY['conj']: u"1BI",
        QUIFOY['pac1']: u"1CI",
        QUIFOY['pac2']: u"1DI",
        QUIFOY['pac3']: u"1EI",
        }
    column = BoolCol
    entity = Individu
    label = u"Demandeur d'emploi inscrit depuis plus d'un an"
    period_behavior = YEAR

  # Pour toutes les variables de ce type, les pac3 ne sont plus proposés après 2007


class chomage_brut(Variable):
    column = FloatCol()
    entity = Individu
    label = u"Chômage brut"
    period_behavior = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add


class indemnites_chomage_partiel(Variable):
    column = FloatCol
    entity = Individu
    label = u"Indemnités de chômage partiel"
    period_behavior = MONTH
    set_input = set_input_divide_by_period
