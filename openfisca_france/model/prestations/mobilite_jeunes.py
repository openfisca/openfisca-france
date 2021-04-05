from openfisca_france.model.base import Individu, Variable, MONTH
from openfisca_france.model.prestations.education import TypesClasse


class aide_mobilite_parcoursup_sortie_academie(Variable):
    value_type = bool
    label = "Indicatrice d'une sortie de l'académie d'études au lycée dans les voeux ParcourSup"
    entity = Individu
    definition_period = MONTH


class aide_mobilite_parcoursup_boursier_lycee(Variable):
    value_type = bool
    label = "Bénéficiaire d'une bourse du lycée"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        return individu.famille("bourse_lycee", period) > 0


class aide_mobilite_parcoursup(Variable):
    value_type = float
    label = "Montant de l'aide à la mobilité ParcourSup"
    entity = Individu
    definition_period = MONTH
    reference = "https://www.etudiant.gouv.fr/fr/le-repas-au-crous-passe-1-euro-pour-tous-les-etudiants-2314"

    def formula(individu, period, parameters):
        sortie_academie = individu("aide_mobilite_parcoursup_sortie_academie", period)
        en_terminal = individu("classe_scolarite", period) == TypesClasse.terminale
        boursier = individu("aide_mobilite_parcoursup_boursier_lycee", period)

        montant = parameters(period).prestations.aide_mobilite_parcoursup.montant

        return montant * sortie_academie * en_terminal * boursier


class aide_mobilite_master_sortie_region_academique(Variable):
    value_type = bool
    label = "Indicatrice d'un changement de région académique entre la 3ème année de licence et la 1ère 1ère année de master"
    entity = Individu
    definition_period = MONTH


class aide_mobilite_master(Variable):
    """
    Critères non pris en comptes:
    - Première inscription en master l'année qui suit l'obtention de la licence
    """
    value_type = float
    label = "Montant de l'aide à la mobilité Master"
    entity = Individu
    definition_period = MONTH
    reference = [
        "Décret n° 2017-969 du 10 mai 2017 relatif à l'aide à la mobilité accordée aux étudiants inscrits en première année du diplôme national de master",
        "https://www.legifrance.gouv.fr/loda/id/JORFTEXT000034675851/"
        ]

    def formula(individu, period, parameters):
        sortie_academie = individu("aide_mobilite_master_sortie_region_academique", period)
        classe = individu("classe_scolarite", period)
        en_transition = (classe == TypesClasse.licence_3) + (classe == TypesClasse.master_1)
        boursier = individu("boursier", period)

        montant = parameters(period).prestations.aide_mobilite_master.montant

        return montant * sortie_academie * en_transition * boursier
