# -*- coding: utf-8 -*-

from numpy import (select)
from openfisca_france.model.base import *  # noqa analysis:ignore

class eligibilite_anah(Variable):
    column = StrCol
    entity = FoyerFiscal
    label = u"Barème d'éligibilité aux aides ANAH"
    definition_period = YEAR

    def function(foyer, period):
        rfr = foyer('rfr',period)
        return select([rfr >= 0],["a_verifier"])
