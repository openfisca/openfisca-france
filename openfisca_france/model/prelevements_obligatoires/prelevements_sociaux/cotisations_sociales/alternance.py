from openfisca_france.model.base import Variable, Individu, MONTH


class alternant(Variable):
    value_type = bool
    label = "L'individu est en formation en alternance sous contrat d'apprentissage ou de professionalisation"
    entity = Individu
    definition_period = MONTH
    reference = "https://www.service-public.fr/particuliers/vosdroits/F15478"
    documentation = '''
    Périmètre réduit : 
    Le contrat d'apprentissage ou de professionalisation est dans une entreprise
    du secteur privé non agricole.
    '''
