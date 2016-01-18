# -*- coding: utf-8 -*-

from ...base import *  # noqa analysis:ignore


build_column('chomeur_longue_duree', BoolCol(label = u"Demandeur d'emploi inscrit depuis plus d'un an",
                   cerfa_field = {QUIFOY['vous']: u"1AI",
                                  QUIFOY['conj']: u"1BI",
                                  QUIFOY['pac1']: u"1CI",
                                  QUIFOY['pac2']: u"1DI",
                                  QUIFOY['pac3']: u"1EI",
                               }))  # Pour toutes les variables de ce type, les pac3 ne sont plus proposés après 2007


build_column('choi', IntCol(label = u"Autres revenus imposables (chômage, préretraite)",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"1AP",
                               QUIFOY['conj']: u"1BP",
                               QUIFOY['pac1']: u"1CP",
                               QUIFOY['pac2']: u"1DP",
                               QUIFOY['pac3']: u"1EP",
                               }))  # (f1ap, f1bp, f1cp, f1dp, f1ep)

class chobrut(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Chômage brut"


build_column('indemnites_chomage_partiel', FloatCol(entity = 'ind', label = u"Indemnités de chômage partiel"))
