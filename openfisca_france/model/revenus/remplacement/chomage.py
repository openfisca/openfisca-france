# -*- coding: utf-8 -*-

from ...base import *  # noqa analysis:ignore


build_column('chomeur_longue_duree', BoolCol(label = u"Demandeur d'emploi inscrit depuis plus d'un an",
                   cerfa_field = {QUIFOY['vous']: u"1AI",
                                  QUIFOY['conj']: u"1BI",
                                  QUIFOY['pac1']: u"1CI",
                                  QUIFOY['pac2']: u"1DI",
                                  QUIFOY['pac3']: u"1EI",
                               }))  # Pour toutes les variables de ce type, les pac3 ne sont plus proposés après 2007


class chomage_brut(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Chômage brut"


build_column('indemnites_chomage_partiel', FloatCol(entity = 'ind', label = u"Indemnités de chômage partiel"))
