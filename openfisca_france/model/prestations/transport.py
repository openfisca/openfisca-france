from openfisca_france.model.base import Variable, Individu, MONTH, set_input_dispatch_by_period, set_input_divide_by_period
from openfisca_france.model.caracteristiques_socio_demographiques.logement import TypesLieuResidence


class pret_formation_permis_eligibilite(Variable):
    value_type = bool
    label = 'Éligibilité au prêt de formation au permis de conduire à 1 euro par jour'
    entity = Individu
    definition_period = MONTH
    reference = [
        'https://www.legifrance.gouv.fr/loda/id/LEGITEXT000006052491/',
        'https://www.securite-routiere.gouv.fr/passer-son-permis-de-conduire/financement-du-permis-de-conduire/permis-1-eu-par-jour'
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
        criteres_age = parameters(period).prestations_sociales.transport.permis_de_conduire.pret_formation_permis.age
        return (criteres_age.minimum <= age) * (age <= criteres_age.maximum)


class aide_financement_permis_apprenti(Variable):
    value_type = float
    label = "Montant de l'aide au financement du permis de conduire pour les apprentis"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "Décret n° 2019-1 du 3 janvier 2019 relatif à l'aide au financement du permis de conduire pour les apprentis",
        'https://www.legifrance.gouv.fr/eli/decret/2019/1/3/MTRD1835610D/jo/article_1'
        ]

    def formula(individu, period, parameters):
        montant = parameters(period).prestations_sociales.transport.permis_de_conduire.aide_financement_permis_apprenti.montant
        eligibilite = individu('aide_financement_permis_apprenti_eligibilite', period)

        return montant * eligibilite


class aide_financement_permis_apprenti_eligibilite(Variable):
    value_type = bool
    label = "Éligibilité à l'aide au financement du permis de conduire pour les apprentis"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = [
        "Décret n° 2019-1 du 3 janvier 2019 relatif à l'aide au financement du permis de conduire pour les apprentis",
        'https://www.legifrance.gouv.fr/eli/decret/2019/1/3/MTRD1835610D/jo/article_1'
        ]

    def formula(individu, period, parameters):
        age_minimal = parameters(period).prestations_sociales.transport.permis_de_conduire.aide_financement_permis_apprenti.age_min
        age = individu('age', period)
        apprenti = individu('apprenti', period)

        return (age_minimal <= age) * apprenti


class carte_sncf_eleve_apprenti_eligibilite(Variable):
    value_type = bool
    label = 'Éligibilité à la carte SNCF pour les élèves et les apprentis'
    entity = Individu
    definition_period = MONTH
    reference = [
        'https://www.sncf.com/fr/offres-voyageurs/cartes-tarifs-grandes-lignes/eleves-apprentis'
        ]

    def formula(individu, period, parameters):
        age_apprenti = parameters(period).prestations_sociales.transport.carte_sncf_eleve_apprenti.age_apprenti
        age_etudiant = parameters(period).prestations_sociales.transport.carte_sncf_eleve_apprenti.age_etudiant
        age = individu('age', period)

        eligibilite_apprenti = (age_apprenti > age) * individu('apprenti', period)
        eligibilite_etudiant = (age_etudiant > age) * individu('etudiant', period)

        residence_metropole = individu.menage('residence', period) == TypesLieuResidence.metropole

        return (eligibilite_apprenti + eligibilite_etudiant) * residence_metropole
