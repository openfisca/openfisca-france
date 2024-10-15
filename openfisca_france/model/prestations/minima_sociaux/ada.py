from openfisca_france.model.base import *


class ada(Variable):
    value_type = float
    entity = Famille
    label = "Montant mensuel  de l'aide pour demandeur d'asile"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2015_11(famille, period, parameters):
        nb_parents = famille('nb_parents', period)
        af_nbenf = famille('af_nbenf', period)
        place_hebergement = famille('place_hebergement', period)
        asile_demandeur = famille('asile_demandeur', period)
        ada = parameters(period).prestations_sociales.solidarite_insertion.autre_solidarite.ada

        nb_pers = af_nbenf + nb_parents
        ada_par_jour = (
            ada.montant_journalier_pour_une_personne
            + (nb_pers - 1) * ada.majoration_pers_supp
            + ada.supplement_non_hebergement
            * not_(place_hebergement)
            )

        montant_ada = period.days * ada_par_jour * asile_demandeur
        return montant_ada


class asile_demandeur(Variable):
    value_type = bool
    entity = Famille
    label = "Famille demandant l'asile"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class place_hebergement(Variable):
    value_type = bool
    default_value = True
    entity = Famille
    label = "Bénéficie d'une place dans un centre d'hébergement"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
