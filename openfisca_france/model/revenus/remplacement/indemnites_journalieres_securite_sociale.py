from openfisca_france.model.base import *


class indemnites_journalieres_maternite(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnités journalières de maternité'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_journalieres_paternite(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnités journalières de paternité'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_journalieres_adoption(Variable):
    value_type = float
    entity = Individu
    label = "Indemnités journalières d'adoption"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_journalieres_maladie(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnités journalières de maladie'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_journalieres_accident_travail(Variable):
    value_type = float
    entity = Individu
    label = "Indemnités journalières d'accident du travail"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_journalieres_maladie_professionnelle(Variable):
    value_type = float
    entity = Individu
    label = 'Indemnités journalières de maladie professionnelle'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class indemnites_journalieres(Variable):
    value_type = float
    label = 'Total des indemnités journalières'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        ressources = [
            'indemnites_journalieres_maternite',
            'indemnites_journalieres_paternite',
            'indemnites_journalieres_adoption',
            'indemnites_journalieres_maladie',
            'indemnites_journalieres_accident_travail',
            'indemnites_journalieres_maladie_professionnelle',
            ]
        total = sum(individu(ressource, period) for ressource in ressources)

        return total


class indemnites_journalieres_imposables(Variable):
    value_type = float
    label = 'Total des indemnités journalières imposables'
    entity = Individu
    reference = 'http://vosdroits.service-public.fr/particuliers/F3152.xhtml'
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        indemnites_journalieres = individu('indemnites_journalieres', period)
        indemnites_journalieres_accident_travail = individu('indemnites_journalieres_accident_travail', period)
        indemnites_journalieres_maladie_professionnelle = individu('indemnites_journalieres_accident_travail', period)
        result = indemnites_journalieres - 0.5 * (
            indemnites_journalieres_accident_travail + indemnites_journalieres_maladie_professionnelle
            )

        return result


class indemnites_journalieres_atexa(Variable):
    value_type = float
    entity = Individu
    label = "Indemnités de l'assurance Accident du Travail des Exploitants Agricoles"
    reference = 'https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000649169'
    definition_period = MONTH
    set_input = set_input_divide_by_period


class date_arret_de_travail(Variable):
    value_type = date
    default_value = date.min
    entity = Individu
    label = 'Date depuis laquelle la personne est en arrêt de travail'
    definition_period = ETERNITY
