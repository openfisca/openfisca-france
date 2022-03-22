from openfisca_france.model.base import *  # noqa analysis:ignore


class pass_culture(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant du pass culture"
    set_input = set_input_divide_by_period
    reference = ['https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000043518870', 'https://www.service-public.fr/particuliers/vosdroits/F34959']

    def formula(individu, period, parameters):
        montant = parameters(period).prestations_sociales.aides_jeunes.pass_culture.montants
        age = individu('age', period.offset(1, 'month'))
        age_maximum = parameters(period).prestations_sociales.aides_jeunes.pass_culture.age_maximum
        return montant.calc(age) * (age <= age_maximum)
