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


class aide_jeunes_diplomes_anciens_boursiers_montant_mensuel_reference(Variable):
    value_type = float
    entity = Individu
    reference = [
        "Article 3 du décret n° 2020-1789 du 30 décembre 2020 instituant une aide financière à titre exceptionnel à destination des jeunes diplômés en recherche d'emploi anciennement boursiers de l'enseignement supérieur",
        "https://www.legifrance.gouv.fr/eli/decret/2020/12/30/2020-1789/jo/article_3"
        ]
    label = "Montant mensuel de référence de l'aide perçue au cours de la dernière année d'étude"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period, parameters):
        bourse_2020 = individu("bourse_criteres_sociaux", 2020, options = [ADD])
        bourse_2021 = individu("bourse_criteres_sociaux", 2021, options = [ADD])
        parameters_bourse = parameters(period).bourses_superieur.criteres_sociaux

        return where(
            bourse_2021 > 0,
            bourse_2021 / parameters_bourse.nombre_mensualites,
            bourse_2020 / parameters_bourse.nombre_mensualites
            )
