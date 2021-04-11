from openfisca_france.model.base import *


class aide_mobilite_internationale_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilite à l'aide à la mobilité internationale (AMI)"
    definition_period = MONTH

    def formula(individu, period):
        debut_etudes_etranger = individu('debut_etudes_etranger', period)
        fin_etudes_etranger = individu('fin_etudes_etranger', period)

        statuts_etablissement_scolaire = individu('statuts_etablissement_scolaire', period)

        bourse_criteres_sociaux_eligibilite = individu('bourse_criteres_sociaux_eligibilite', period)

        return bourse_criteres_sociaux_eligibilite


class aide_mobilite_internationale(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide à la mobilité internationale (AMI)"
    definition_period = MONTH

    def formula(individu, period, parameters):
        return individu('bourse_criteres_sociaux_eligibilite', period) * parameters(period).prestations.aide_mobilite_internationale.montant
