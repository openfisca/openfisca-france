# -*- coding: utf-8 -*-

from ...base import *  # noqa analysis:ignore


class retraite_brute(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Retraite brute"

# L'AER est remplacée depuis le 1er juillet 2011 par l'allocation transitoire de solidarité (ATS).
build_column('aer', IntCol(label = u"Allocation équivalent retraite (AER)"))

build_column('retraite_combattant', FloatCol(entity = 'ind', label = u"Retraite du combattant"))
