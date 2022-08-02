from openfisca_france.model.base import Individu, Variable, ETERNITY, MONTH
from openfisca_france.model.prestations.education import TypesClasse


class sortie_academie(Variable):
    value_type = bool
    label = "Mention d'un vœu de changement d'académie entre le lycée et les études supérieures"
    entity = Individu
    definition_period = ETERNITY


class aide_mobilite_parcoursup(Variable):
    value_type = float
    label = "Montant de l'aide à la mobilité ParcourSup"
    entity = Individu
    definition_period = MONTH
    reference = 'https://www.etudiant.gouv.fr/fr/le-repas-au-crous-passe-1-euro-pour-tous-les-etudiants-2314'

    def formula(individu, period, parameters):
        sortie_academie = individu('sortie_academie', period)
        en_terminale = individu('annee_etude', period) == TypesClasse.terminale
        boursier = individu.famille('bourse_lycee', period) > 0

        montant = parameters(period).prestations_sociales.aides_jeunes.mobilite.parcoursup.montant

        return montant * sortie_academie * en_terminale * boursier


class sortie_region_academique(Variable):
    value_type = bool
    label = 'Changement de région académique entre la 3ème année de licence (L3) et la 1ère année de master (M1)'
    entity = Individu
    definition_period = ETERNITY


class aide_mobilite_master(Variable):
    '''
    Critères non pris en compte :
    - Première inscription en master l'année qui suit l'obtention de la licence
    '''
    value_type = float
    label = "Montant de l'aide à la mobilité Master"
    entity = Individu
    definition_period = MONTH
    reference = [
        "Décret n° 2017-969 du 10 mai 2017 relatif à l'aide à la mobilité accordée aux étudiants inscrits en première année du diplôme national de master",
        'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000034675851/'
        ]

    def formula(individu, period, parameters):
        sortie_academie = individu('sortie_region_academique', period)
        annee_etude = individu('annee_etude', period)
        en_transition = (annee_etude == TypesClasse.licence_3) + (annee_etude == TypesClasse.master_1)
        boursier = individu('boursier', period)

        montant = parameters(period).prestations_sociales.aides_jeunes.mobilite.master.montant

        return montant * sortie_academie * en_transition * boursier
