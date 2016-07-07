# -*- coding: utf-8 -*-
import numpy as np
from ...base import *  # noqa analysis:ignore

class asile_demandeur(Variable):
    column = BoolCol(default = False)
    entity_class = Familles
    label = u"Famille demandant l'asile"

class place_hebergement(Variable):
    column = BoolCol(default = True)
    entity_class = Familles
    label = u"Bénéficie d'une place dans un centre d'hébergement"

class ada(DatedVariable):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Montant mensuel  de l'aide pour demandeur d'asile"

    @dated_function(start = date(2015, 11, 1))
    def function_2015(self, simulation, period):
        ada_nb_foyer = {'[1]': 6.8,
        '[2]' : 10.2,
        '[3]' : 13.6,
        '[4]' : 17.0,
        '[5]' : 20.4,
        '[6]' : 23.8,
        '[7]' : 27.2,
        '[8]' : 30.6,
        '[9]' : 34.0,
        '[10]' : 37.4}  # dictionnaire où : key = nombre de demandeurs et value = montant versé par jour au foyer

        period = period.this_month
        nb_parents = simulation.calculate('nb_parents', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        place_hebergement = simulation.calculate('place_hebergement', period)
        asile_demandeur = simulation.calculate('asile_demandeur', period)
        ada_jour = np.where(
            asile_demandeur,
            np.where(
                place_hebergement,
                ada_nb_foyer[str(nb_parents + af_nbenf)],
                ada_nb_foyer[str(nb_parents + af_nbenf)] + 4.20
                ),
             0,
             )
        ada = period.days * ada_jour
        return period, ada
