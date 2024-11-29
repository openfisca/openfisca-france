from openfisca_core.model_api import Variable
from openfisca_france.entities import Individu
from openfisca_core.periods import MONTH
from numpy.core.defchararray import startswith

drom_codes = [
    b'971',  # Guadeloupe
    b'972',  # Martinique
    b'973',  # Guyane
    b'974',  # La Réunion
    b'976'   # Mayotte
    ]


class localisation_DROM_aide_alimentation_etudiants_eloignes(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Indique si l'individu réside dans un des DROM concernés par les montants spéciaux pour l'aide alimentaire étudiants éloignés"

    def formula(individu, period):
        depcom = individu.menage('depcom', period)
        eligibilite_geographique = sum([startswith(depcom, code_departement) for code_departement in drom_codes])

        return eligibilite_geographique > 0
