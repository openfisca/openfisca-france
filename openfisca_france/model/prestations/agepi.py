from openfisca_france.model.base import Famille, Individu, Variable, MONTH


class pe_nbenf(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    label = "Nombre d'enfants pour le calcul de l'aide à la garde des enfants de parents isolés de Pôle Emploi"
    reference = [
        "Article 2 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi"
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20"
        ]

    def formula(famille, period):
        return famille.sum(famille.members('age', period) < 10, role = Famille.ENFANT)


class temps_travail_semaine(Variable):
    value_type = float
    entity = Individu
    label = "Temps de travail par semaine pour le calcul de l'aide à la garde des enfants de parents isolés de Pôle Emploi"
    definition_period = MONTH


class agepi(Variable):
    value_type = float
    entity = Famille
    label = "Montant de l'aide à la garde des enfants de parents isolés de Pôle Emploi"
    definition_period = MONTH
    reference = [
        "Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi"
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20"
        ]

    def formula(famille, period):
        isole = famille('nb_parents', period) == 1
        nb_heures = famille.sum(famille.members('temps_travail_semaine', period), role = Famille.PARENT)
        nbenf = famille('pe_nbenf', period)

        montant_moins_de_15h = 170 * (nbenf == 1) + 195 * (nbenf == 2) + 220 * (nbenf > 2)
        montant_plus_de_15h = 400 * (nbenf == 1) + 460 * (nbenf == 2) + 520 * (nbenf > 2)
        montant = (nb_heures <= 15) * montant_moins_de_15h + (nb_heures > 15) * montant_plus_de_15h

        return isole * (nb_heures > 0) * montant
