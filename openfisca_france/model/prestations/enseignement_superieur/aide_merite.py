from openfisca_france.model.base import *

class aide_merite_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilité à l'aide au mérite"
    definition_period = MONTH
    reference = [
        "https://www.etudiant.gouv.fr/fr/aide-au-merite-1291",
        "https://www.legifrance.gouv.fr/codes/id/LEGISCTA000030722211/"
        ]
    documentation = '''
    Complémentaire à la bourse sur critères sociaux, pour les étudiants les plus méritants.
    '''
