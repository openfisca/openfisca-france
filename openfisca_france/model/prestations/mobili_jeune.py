from openfisca_france.model.base import Variable


class mobili_jeune_eligibilite(Variable):
    value_type = bool
    label = "Éligibilité à l'aide au logement mobili-jeune"
    entity = Individu
    definition_period = MONTH
    reference = "https://www.actionlogement.fr/l-aide-mobili-jeune"

    def formula(individu, period, parameters):
        condition_age = individu("age", period) >= 30
        condition_contrat = individu("alternant", period) * (
            individu("apprenti", period) 
            + individu("professionnalisation", period)
            )
        return condition_age * condition_contrat
