from openfisca_france.model.base import Individu, Variable, MONTH, TypesClasse


class aide_mobilite_parcoursup_sortie_academie(Variable):
    value_type = bool
    label = "Indicatrice d'une sortie de l'académie d'études au lycée dans les voeux ParcourSup"
    entity = Individu
    definition_period = MONTH


class aide_mobilite_parcoursup(Variable):
    value_type = float
    label = "Montant de l'aide à la mobilité ParcourSup"
    entity = Individu
    definition_period = MONTH
    reference = "https://www.etudiant.gouv.fr/fr/le-repas-au-crous-passe-1-euro-pour-tous-les-etudiants-2314"

    def formula(individu, period, parameters):
        sortie_academie = individu("aide_mobilite_parcoursup_sortie_academie", period)
        en_terminal = individu("classe_scolarite", period) == TypesClasse.terminale
        boursier = individu.famille("bourse_lycee", period) > 0

        montant = parameters(period).prestations.aide_mobilite_parcoursup.montant

        return montant * sortie_academie * en_terminal * boursier
