from openfisca_france.model.base import Variable, MONTH, Individu


class pass_sport(Variable):
    label = 'Éligibilité au Pass’Sport'
    definition_period = MONTH
    value_type = float
    reference = ['https://www.legifrance.gouv.fr/loda/id/LEGIARTI000046139655/2022-08-05#LEGIARTI000046139655',
                 'https://www.etudiant.gouv.fr/fr/le-pass-sport-et-les-etudiants-2800']
    entity = Individu

    def formula_2022_06_30(individu, period):
        boursier = individu('boursier', period)

        age = individu('age', period)
        eligibilite_age = age <= 28

        montant = 50

        return montant * boursier * eligibilite_age
