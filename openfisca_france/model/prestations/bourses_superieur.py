from numpy import datetime64
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


class bourse_criteres_sociaux(Variable):
    value_type = float
    entity = Individu
    reference = [
        "Circulaire ESRS2013435C - Annexe 3 - Conditions de ressources et points de charge / 1 - Conditions de ressources",
        "https://www.education.gouv.fr/bo/20/Hebdo25/ESRS2013435C.htm"
        ]
    label = "Échelon de la bourse sur critères sociaux de l'enseignement supérieur perçue (de 0 à 7)"
    definition_period = MONTH


class aide_jeunes_diplomes_anciens_boursiers_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilité à l'aide jeunes diplômés et anciens boursiers"
    definition_period = MONTH
    end = '2021-06-30'
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
        annee_validation_diplome = date_diplome.astype('datetime64[Y]')

        condition_diplome = (
            ( diplome == TypesDiplome.niveau_5 )
            + ( diplome == TypesDiplome.niveau_6 )
            + ( diplome == TypesDiplome.niveau_7 )
            + ( diplome == TypesDiplome.niveau_8 )
            ) * (
               ( annee_validation_diplome == datetime64('2020') )
               + ( annee_validation_diplome == datetime64('2021') ) 
               )

        # bourse au cours de la dernière année de préparation du diplôme 
        condition_periode_bourse = (
            ( individu("bourse_criteres_sociaux", 2020, options = [ADD]) > 0 )
            + (individu("bourse_criteres_sociaux", 2021, options = [ADD]) > 0 )
        )

        # Être inscrit sur la liste des demandeurs d’emploi
        demandeur_emploi = individu("activite", period) == TypesActivite.chomeur
        pas_en_formation = not_(individu("formation", period))
        condition_activite = demandeur_emploi * pas_en_formation

        condition_non_cumul = not_(
            individu("are", period)
            * individu("ass", period)
            * individu("allocation_travailleur_independant", period)
            * individu("rsa", period)
            * individu("garantie_jeunes", period)
            )

        return condition_age * condition_diplome * condition_periode_bourse * condition_activite * condition_non_cumul
