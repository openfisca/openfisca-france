# -*- coding: utf-8 -*-

from ...base import *  # noqa analysis:ignore


build_column('rsti', IntCol(label = u"Pensions, retraites, rentes connues imposables",
                val_type = "monetary",
                cerfa_field = {QUIFOY['vous']: u"1AS",
                               QUIFOY['conj']: u"1BS",
                               QUIFOY['pac1']: u"1CS",
                               QUIFOY['pac2']: u"1DS",
                               QUIFOY['pac3']: u"1ES",
                               }))  # (f1as, f1bs, f1cs, f1ds, f1es)

class rstbrut(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Retraite brute"

# L'AER est remplacée depuis le 1er juillet 2011 par l'allocation transitoire de solidarité (ATS).
build_column('aer', IntCol(label = u"Allocation équivalent retraite (AER)"))

build_column('retraite_combattant', FloatCol(entity = 'ind', label = u"Retraite du combattant"))
