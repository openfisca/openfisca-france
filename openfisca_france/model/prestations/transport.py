from openfisca_france.model.base import Variable, Individu, MONTH, not_

class pret_formation_permis(Variable):
    value_type = bool
    label = "Bénéficiaire du prêt à la formation au permis de conduire à 1 euro par jour"
    entity = Individu
    definition_period = MONTH
    reference = [
        "https://www.legifrance.gouv.fr/loda/id/LEGITEXT000006052491/",
        "https://www.securite-routiere.gouv.fr/passer-son-permis-de-conduire/financement-du-permis-de-conduire/permis-1-eu-par-jour"
        ]
    documentation = '''
    Le prêt « permis à un euro par jour » est exclusivement destiné au financement
    d’une formation initiale ou, dans le cas d’un échec à l’épreuve pratique 
    de l’examen du permis de conduire, d’une formation complémentaire. 
    '''


class pret_formation_permis_eligibilite(Variable):
    value_type = bool
    label = "Éligibilité au prêt de formation au permis de conduire à 1 euro par jour"
    entity = Individu
    definition_period = MONTH
    reference = [
        "https://www.legifrance.gouv.fr/loda/id/LEGITEXT000006052491/",
        "https://www.securite-routiere.gouv.fr/passer-son-permis-de-conduire/financement-du-permis-de-conduire/permis-1-eu-par-jour"
        ]

    def formula(individu, period):
        pret_formation_permis = individu('pret_formation_permis', period)
        age = individu('age', period)
        condition_age = (15 <= age) * (age <= 25)
        return not_(pret_formation_permis) * condition_age
