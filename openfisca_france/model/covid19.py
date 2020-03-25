# -*- coding: utf-8 -*-

from openfisca_france.model.base import Variable, Individu, MONTH


class covid_aide_exceptionnelle_tpe_eligible(Variable):
    entity = Individu
    value_type = bool
    label = "Unités de consommation du ménage pour le calcul du chèque Énergie"
    definition_period = MONTH

    def formula(individu, period):
        return individu('travailleur_non_salarie', period)


class covid_aide_exceptionnelle_tpe_montant(Variable):
    entity = Individu
    value_type = float
    label = "Unités de consommation du ménage pour le calcul du chèque Énergie"
    definition_period = MONTH

    def formula(individu, period, parameters):
        elig = individu('covid_aide_exceptionnelle_tpe_eligible', period)
        return elig * parameters(period).covid19.aide_exceptionnelle_tpe.montant
