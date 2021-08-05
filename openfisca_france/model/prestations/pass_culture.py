from openfisca_france.model.base import *  # noqa analysis:ignore


class pass_culture(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant du pass culture"
    set_input = set_input_divide_by_period
    reference = ['https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000043518870', 'https://www.service-public.fr/particuliers/vosdroits/F34959']

    def formula(individu, period, parameters):
        montant = parameters(period).prestations.pass_culture.montant
        a_18ans = individu('age', period.offset(1, 'month')) == 18
        return a_18ans * montant
