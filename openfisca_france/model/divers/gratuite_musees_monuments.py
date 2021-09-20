from openfisca_france.model.base import *


class gratuite_musees_monuments(Variable):
    value_type = bool
    label = "Accès gratuit aux musées et monuments nationaux"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = "https://www.service-public.fr/particuliers/vosdroits/F20348"

    def formula(individu, period, parameters):
        age = individu('age', period)
        condition_age = (age >= parameters(period).divers.gratuite_musees_monuments.age_min) * (age <= parameters(period).divers.gratuite_musees_monuments.age_max)

        condition_nationalite = individu('resident_ue', period)

        return condition_age * condition_nationalite
