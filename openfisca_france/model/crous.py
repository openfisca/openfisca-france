from openfisca_france.model.base import Individu, Variable, MONTH

class crous_logement_eligibilite(Variable):
    entity = Individu
    value_type = int
    label = "Indicatrice indiquant une forte probabilité à être éligible aux logements proposés par le CROUS"
    definition_period = MONTH

    def formula(individu, period):
        return individu('bourse_criteres_sociaux', period) >= 0
