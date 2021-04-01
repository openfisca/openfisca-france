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
    set_input = set_input_divide_by_period


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
        age_limite =  parameters(period).bourses_superieur.criteres_sociaux.aide_jeunes_diplomes_anciens_boursiers.age_limite
        condition_age = individu("age", period) < age_limite

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
            + ( individu("bourse_criteres_sociaux", 2021, options = [ADD]) > 0 )
            )

        # Être inscrit sur la liste des demandeurs d’emploi
        demandeur_emploi = individu("activite", period) == TypesActivite.chomeur
        pas_en_formation = not_(individu("formation", period))
        condition_activite = demandeur_emploi * pas_en_formation

        condition_non_cumul = not_(
            individu("are", period)
            + individu("ass", period)
            + individu("allocation_travailleur_independant", period)
            + individu.famille("rsa", period)
            + individu("garantie_jeunes", period)
            )

        return condition_age * condition_diplome * condition_periode_bourse * condition_activite * condition_non_cumul


class aide_jeunes_diplomes_anciens_boursiers_montant(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide jeunes diplômés et anciens boursiers"
    definition_period = MONTH
    end = '2021-06-30'
    reference = "https://www.pole-emploi.fr/candidat/mes-droits-aux-aides-et-allocati/allocations-et-aides--les-repons/aides-financieres-aux-jeunes-dip.html"

    def formula_2021_02_05(individu, period, parameters):
        aide_jeunes_diplomes_anciens_boursiers_eligibilite = individu("aide_jeunes_diplomes_anciens_boursiers_eligibilite", period)
        # 70% du montant net de la bourse perçue la dernière année
        bourse_2020 = individu("bourse_criteres_sociaux", 2020, options = [ADD])
        bourse_2021 = individu("bourse_criteres_sociaux", 2021, options = [ADD])
        
        parameters_bourse =  parameters(period).bourses_superieur.criteres_sociaux
        part_bourse = where(
            bourse_2021 > 0, 
            bourse_2021/parameters_bourse.nombre_mensualites, 
            bourse_2020/parameters_bourse.nombre_mensualites
            ) * parameters_bourse.aide_jeunes_diplomes_anciens_boursiers.taux_bourse

        # S’ajoute une somme supplémentaire de 100 € si vous ne vivez pas chez l’un de vos parents 
        # et devez-vous loger (sur justificatif : facture d'énergie, bail à votre nom).
        statut_occupation_logement = individu.menage("statut_occupation_logement", period)
        condition_logement = not_(
            (statut_occupation_logement == TypesStatutOccupationLogement.loge_gratuitement)
            + (statut_occupation_logement == TypesStatutOccupationLogement.non_renseigne)
            )
        part_logement = condition_logement * parameters_bourse.aide_jeunes_diplomes_anciens_boursiers.majoration_logement

        return aide_jeunes_diplomes_anciens_boursiers_eligibilite * ( part_bourse + part_logement )
