from openfisca_france.model.base import *


class echelon_bourse(Variable):
    entity = Individu
    value_type = int
    label = "Echelon de la bourse perçue (de 0 à 7)"
    definition_period = MONTH


class boursier(Variable):
    value_type = bool
    entity = Individu
    label = "Élève ou étudiant boursier"
    definition_period = MONTH


class bourse_criteres_sociaux(Variable):
    value_type = float
    entity = Individu
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 1 - Conditions de ressources",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Échelon de la bourse sur critères sociaux de l'enseignement supérieur perçue (de 0 à 7)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
