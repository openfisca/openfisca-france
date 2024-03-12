from openfisca_france.model.base import Variable, Individu, MONTH, set_input_dispatch_by_period


class service_civique(Variable):
    value_type = bool
    label = 'Est en contrat de service civique'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = 'https://www.service-public.fr/particuliers/vosdroits/F13278'
