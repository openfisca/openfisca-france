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


class aide_jeunes_diplomes_anciens_boursiers_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilité à l'aide jeunes diplômés et anciens boursiers"
    definition_period = MONTH
    reference = "https://www.pole-emploi.fr/candidat/mes-droits-aux-aides-et-allocati/allocations-et-aides--les-repons/aides-financieres-aux-jeunes-dip.html"
    documentation = '''
    Conditions non modélisées :
    Être disponible pour occuper un emploi, le jour de la demande.
    Ne pas être en formation (de niveau 5 minimum) au moment de la demande.
    Ne pas être inscrit dans une nouvelle formation (de niveau 5 minimum) dans l'année universitaire qui suit l'obtention du diplôme.   
    '''

    def formula_2021_02_05(individu, period, parameters):
        condition_age = individu("age", period) < 30

        diplome = individu("diplome", period)
        date_diplome = individu("date_diplome", period)
        condition_diplome = (
            diplome == TypesDiplome.niveau_5
            + diplome == TypesDiplome.niveau_6
            + diplome == TypesDiplome.niveau_7
            + diplome == TypesDiplome.niveau_8
            ) * (
                date_diplome.this_year == '2020'
                + date_diplome.this_year == '2021'
                )  # à améliorer

        bourse_criteres_sociaux = individu("bourse_criteres_sociaux", date_diplome.last_year) > 0  # à améliorer

        # Être inscrit sur la liste des demandeurs d’emploi
        demandeur_emploi = individu("activite", period) == TypesActivite.chomeur
        pas_en_formation = not_(individu("formation", period))
        condition_activite = demandeur_emploi * pas_en_formation

        condition_non_cumul = (
            # ajouter ARE ATI
            individu("ass", period)
            * individu("rsa", period)
            * individu("garantie_jeunes", period)
            ) <= 0.

        return condition_age * condition_diplome * bourse_criteres_sociaux * condition_activite * condition_non_cumul
