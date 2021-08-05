from openfisca_france.model.base import Famille, Individu, Variable, MONTH, set_input_dispatch_by_period, set_input_divide_by_period


class pe_nbenf(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Nombre d'enfants pour le calcul de l'aide à la garde des enfants de parents isolés de Pôle Emploi"
    reference = [
        "Article 2 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi"
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20"
        ]

    def formula(famille, period, parameters):
        agepi = parameters(period).prestations.agepi
        return famille.sum(famille.members('age', period) < agepi.age_enfant_maximum, role = Famille.ENFANT)


class agepi_temps_travail_semaine(Variable):
    value_type = float
    entity = Individu
    label = "Temps de travail par semaine pour le calcul de l'aide à la garde des enfants de parents isolés de Pôle Emploi"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        heures_remunerees_volume = individu('heures_remunerees_volume', period)
        return heures_remunerees_volume / 52 * 12  # Passage en heures par semaine


class agepi(Variable):
    value_type = float
    entity = Famille
    label = "Montant de l'aide à la garde des enfants de parents isolés de Pôle Emploi"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi"
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20"
        ]

    def formula(famille, period, parameters):
        isole = famille('nb_parents', period) == 1
        nb_heures = famille.sum(famille.members('agepi_temps_travail_semaine', period), role = Famille.PARENT)
        nbenf = famille('pe_nbenf', period)

        montants = parameters(period).prestations.agepi.montants
        montant_moins_de_15h = montants.moins_de_15h_par_semaine.calc(nbenf)
        montant_plus_de_15h = montants.plus_de_15h_par_semaine.calc(nbenf)

        montant = (nb_heures <= 15) * montant_moins_de_15h + (nb_heures > 15) * montant_plus_de_15h

        return isole * (nb_heures > 0) * montant
