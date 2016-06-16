# -*- coding: utf-8 -*-

from ...base import *  # noqa analysis:ignore


class retraite_brute(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Retraite brute"

# L'AER est remplacée depuis le 1er juillet 2011 par l'allocation transitoire de solidarité (ATS).
class aer(Variable):
    column = IntCol
    entity_class = Individus
    label = u"Allocation équivalent retraite (AER)"



class retraite_combattant(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Retraite du combattant"


