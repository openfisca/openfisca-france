# -*- coding: utf-8 -*-
import numpy as np
from openfisca_france.model.base import *  # noqa analysis:ignore


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
        period = period.this_month
        nb_parents = simulation.calculate('nb_parents', period)
        af_nbenf = simulation.calculate('af_nbenf', period)
        place_hebergement = simulation.calculate('place_hebergement', period)
        asile_demandeur = simulation.calculate('asile_demandeur', period)
        ada = simulation.legislation_at(period.start).prestations.minima.ada

        nb_pers = af_nbenf + nb_parents

        ada_par_jour = (ada.montant_journalier_pour_une_personne +
            (nb_pers - 1) * ada.majoration_pers_supp +
            ada.supplement_non_hebergement * (not ada.place_hebergement)
            )

        montant_ada = period.days * ada_par_jour
        return period, montant_ada
