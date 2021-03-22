from openfisca_france.model.base import Variable, Individu, MONTH


class pret_formation_permis_eligibilite(Variable):
    value_type = bool
    label = "Éligibilité au prêt de formation au permis de conduire à 1 euro par jour"
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
    Conditions non modélisées :
    Il ne peut être attribué qu’une seule fois à un même bénéficiaire et pour une même catégorie de permis.
    Ces formations doivent viser l’obtention du permis de conduire soit de la catégorie A1,
    soit de la catégorie A2, soit de la catégorie B.
    '''

    def formula_2005_09_30(individu, period, parameters):
        age = individu('age', period)
        criteres_age = parameters(period).prestations.transport.pret_formation_permis.age
        return (criteres_age.minimum <= age) * (age <= criteres_age.maximum)
