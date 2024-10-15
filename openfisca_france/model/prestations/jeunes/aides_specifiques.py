from openfisca_france.model.base import Variable, Individu, MONTH, set_input_divide_by_period


class allocation_annuelle_etudiant(Variable):
    value_type = float
    entity = Individu
    label = "Allocation annuelle (type d'aide spécifique aux étudiants à difficultés pérennes)"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'https://www.education.gouv.fr/bo/14/Hebdo40/MENS1420893C.htm',
        'https://www.etudiant.gouv.fr/fr/aides-specifiques-1306'
        ]
    documentation = '''
    Cette aide est l'équivalent d'une bourse sur critères sociaux.
    Elle permet ainsi d'être exonéré·e des droits d'inscription universitaires
    et de la contribution vie étudiante et de campus (CVEC).
    '''
