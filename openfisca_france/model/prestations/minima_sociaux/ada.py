# -*- coding: utf-8 -*-
import numpy as np
from openfisca_france.model.base import *  # noqa analysis:ignore


class ada(Variable):
    column = FloatCol
    entity = Famille
    label = u"Montant mensuel  de l'aide pour demandeur d'asile"
    definition_period = MONTH

    def formula_2015_11(famille, period, legislation):
        nb_parents = famille('nb_parents', period)
        af_nbenf = famille('af_nbenf', period)
        place_hebergement = famille('place_hebergement', period)
        asile_demandeur = famille('asile_demandeur', period)
        ada = legislation(period).prestations.minima_sociaux.ada

        nb_pers = af_nbenf + nb_parents
        ada_par_jour = (ada.montant_journalier_pour_une_personne +
            (nb_pers - 1) * ada.majoration_pers_supp +
            ada.supplement_non_hebergement * (not place_hebergement)
            )

        montant_ada = period.days * ada_par_jour * asile_demandeur
        return montant_ada


class asile_demandeur(Variable):
    column = BoolCol
    entity = Famille
    label = u"Famille demandant l'asile"
    definition_period = MONTH


class place_hebergement(Variable):
    column = BoolCol(default = True)
    entity = Famille
    label = u"Bénéficie d'une place dans un centre d'hébergement"
    definition_period = MONTH
