from numpy import datetime64
from openfisca_france.model.base import (
    Variable, Individu,
    MONTH, ADD, set_input_divide_by_period,
    not_, where,
    TypesNiveauDiplome, TypesActivite, TypesStatutOccupationLogement
    )


class aide_jeunes_diplomes_anciens_boursiers_base_ressources(Variable):
    value_type = float
    entity = Individu
    reference = [
        "Article 3 du décret n° 2020-1789 du 30 décembre 2020 instituant une aide financière à titre exceptionnel à destination des jeunes diplômés en recherche d'emploi anciennement boursiers de l'enseignement supérieur",
        "https://www.legifrance.gouv.fr/eli/decret/2020/12/30/2020-1789/jo/article_3"
        ]
    label = "Ressources mensuelles de référence de l'aide perçue au cours de la dernière année d'étude"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        bourse_2020 = individu("bourse_criteres_sociaux", 2020, options = [ADD])
        bourse_2021 = individu("bourse_criteres_sociaux", 2021, options = [ADD])
        nombre_mensualites = parameters(period).bourses_enseignement_superieur.criteres_sociaux.nombre_mensualites

        return where(
            bourse_2021 > 0,
            bourse_2021 / nombre_mensualites,
            bourse_2020 / nombre_mensualites
            )


class aide_jeunes_diplomes_anciens_boursiers_eligibilite(Variable):
    value_type = bool
    entity = Individu
    label = "Éligibilité à l'aide jeunes diplômés et anciens boursiers"
    definition_period = MONTH
    end = "2021-06-30"
    reference = "https://www.pole-emploi.fr/candidat/mes-droits-aux-aides-et-allocati/allocations-et-aides--les-repons/aides-financieres-aux-jeunes-dip.html"
    documentation = '''
    Conditions non modélisées :
    Être disponible pour occuper un emploi, le jour de la demande.
    Ne pas être inscrit dans une nouvelle formation (de niveau 5 minimum) dans l'année universitaire qui suit l'obtention du diplôme.
    '''

    def formula_2021_02_05(individu, period, parameters):
        age_limite = parameters(period).covid19.aide_jeunes_diplomes_anciens_boursiers.age_limite
        condition_age = individu("age", period) < age_limite

        annee = period.this_year
        niveau_diplome = individu("plus_haut_diplome_niveau", annee)
        date_diplome = individu("plus_haut_diplome_date_obtention", annee)

        condition_diplome = (
            (niveau_diplome == TypesNiveauDiplome.niveau_5)
            + (niveau_diplome == TypesNiveauDiplome.niveau_6)
            + (niveau_diplome == TypesNiveauDiplome.niveau_7)
            + (niveau_diplome == TypesNiveauDiplome.niveau_8)
            ) * (datetime64('2020') <= date_diplome) * (date_diplome < datetime64('2022'))

        # bourse au cours de la dernière année de préparation du diplôme
        condition_bourse = individu("aide_jeunes_diplomes_anciens_boursiers_base_ressources", period) > 0

        # être inscrit sur la liste des demandeurs d’emploi
        demandeur_emploi = individu("activite", period) == TypesActivite.chomeur
        # ne pas être en formation (de niveau 5 minimum) au moment de la demande.
        pas_en_formation = individu("niveau_diplome_formation", annee) == TypesNiveauDiplome.non_renseigne
        condition_activite = demandeur_emploi * pas_en_formation

        condition_non_cumul = not_(
            individu("chomage_brut", period)
            + individu("ass", period)
            + individu("allocation_travailleur_independant", period)
            + individu.famille("rsa", period)
            + individu("garantie_jeunes", period)
            )

        return condition_age * condition_diplome * condition_bourse * condition_activite * condition_non_cumul


class aide_jeunes_diplomes_anciens_boursiers_montant(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide jeunes diplômés et anciens boursiers"
    definition_period = MONTH
    end = "2021-06-30"
    reference = "https://www.pole-emploi.fr/candidat/mes-droits-aux-aides-et-allocati/allocations-et-aides--les-repons/aides-financieres-aux-jeunes-dip.html"

    def formula_2021_02_05(individu, period, parameters):
        aide_jeunes_diplomes_anciens_boursiers_eligibilite = individu("aide_jeunes_diplomes_anciens_boursiers_eligibilite", period)

        bourse_precedente = individu("aide_jeunes_diplomes_anciens_boursiers_base_ressources", period)
        parameters_aide = parameters(period).covid19.aide_jeunes_diplomes_anciens_boursiers

        part_bourse = bourse_precedente * parameters_aide.taux_bourse

        statut_occupation_logement = individu.menage("statut_occupation_logement", period)
        condition_logement = not_(
            (statut_occupation_logement == TypesStatutOccupationLogement.loge_gratuitement)
            + (statut_occupation_logement == TypesStatutOccupationLogement.non_renseigne)
            )
        part_logement = condition_logement * parameters_aide.majoration_logement

        return aide_jeunes_diplomes_anciens_boursiers_eligibilite * (part_bourse + part_logement)
