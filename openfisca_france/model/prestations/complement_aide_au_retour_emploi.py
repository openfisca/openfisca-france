from openfisca_france.model.base import Variable, Individu, MONTH

from numpy import (
    maximum as max_,
    minimum as min_,
    round as round_,
    nan_to_num
    )


# https://www.service-public.fr/particuliers/vosdroits/F14860


class salaire_journalier_reference(Variable):
    entity = Individu
    value_type = float
    definition_period = MONTH


class complement_aide_retour_emploi_jours_base(Variable):
    entity = Individu
    value_type = float
    definition_period = MONTH

    def formula(individu, period):
        are_j = individu('aide_retour_emploi_journaliere', period)
        are_m = are_j * 30

        salaire = individu('salaire_de_base', period)
        return nan_to_num((are_m - 0.7 * salaire) / are_j)


class complement_aide_retour_emploi_jours(Variable):
    entity = Individu
    value_type = float
    definition_period = MONTH

    def formula(individu, period):
        are_j = individu('aide_retour_emploi_journaliere', period)
        nb_jours = individu('complement_aide_retour_emploi_jours_base', period)

        salaire = individu('salaire_de_base', period)
        plafond_e = individu('salaire_journalier_reference', period) * 30.42

        return nan_to_num(round_((min_(plafond_e, are_j * nb_jours + salaire) - salaire) / are_j))


class complement_aide_retour_emploi(Variable):
    entity = Individu
    value_type = float
    definition_period = MONTH

    def formula(individu, period):
        salaire = individu('salaire_de_base', period)
        are_j = individu('aide_retour_emploi_journaliere', period)
        nb_jours = individu('complement_aide_retour_emploi_jours', period)

        return are_j * nb_jours * (salaire > 0)


class aide_retour_emploi_journaliere(Variable):
    entity = Individu
    value_type = float
    definition_period = MONTH

    def formula(individu, period):
        sjr = individu('salaire_journalier_reference', period)
        base_pct = (12 + 0.404 * sjr) / sjr
        return nan_to_num(min_(0.75, max_(0.57, base_pct)) * sjr)
