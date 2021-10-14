from openfisca_france.model.base import Famille, Individu, Variable, MONTH, ADD, set_input_dispatch_by_period, \
    set_input_divide_by_period, Enum


class pe_nbenf(Variable):
    value_type = float
    entity = Famille
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Nombre d'enfants pour le calcul de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    reference = [
        "Article 2 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi"
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20"
    ]

    def formula(famille, period, parameters):
        agepi = parameters(period).prestations_sociales.prestations_familiales.education_presence_parentale.agepi
        return famille.sum(famille.members('age', period) < agepi.age_enfant_maximum, role=Famille.ENFANT)


class agepi_temps_travail_semaine(Variable):
    value_type = float
    entity = Individu
    label = "Temps de travail par semaine pour le calcul de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula(individu, period):
        heures_remunerees_volume = individu('heures_remunerees_volume', period)
        return heures_remunerees_volume / 52 * 12  # Passage en heures par semaine

class TypesCategorie(Enum):
    __order__ = 'categorie_1 categorie_2 categorie_3 categorie_4 categorie_5 categorie_6 categorie_7 categorie_8 ' \
                'pas_de_categorie'  # Needed to preserve the enum order in Python 2
    categorie_1 = "1"
    categorie_2 = "2"
    categorie_3 = "3"
    categorie_4 = "4"
    categorie_5 = "5"
    categorie_6 = "6"
    categorie_7 = "7"
    categorie_8 = "8"
    pas_de_categorie = "NA"

class pe_categorie_demandeur_emploi(Variable):
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/instruction-n2016-33-du-6-octobr.html?type=dossiers/2016/bope-n2016-80-du-17-novembre-201#",
        "Annexes"
        ]
    value_type = Enum
    possible_values = TypesCategorie
    default_value = TypesCategorie.pas_de_categorie
    entity = Individu
    label = ""  # TODO
    definition_period = MONTH
    set_input = set_input_dispatch_by_period  # FIXME TODO


class agepi_eligible(Variable):
    value_type = bool
    entity = Famille
    label = "Eligibilité à l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    # set_input = set_input_divide_by_period
    reference = [
        "Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi"
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20"
    ]

    def formula(famille, period, parameters):
        # Renvoi true si :
        #   - l'individu n'a pas touché l'AGEPI dans les 12 derniers mois,
        #   - Est inscrit en catégorie 1, 2, 3, 4 ou 5
        #   - Elève seul son enfant dont l'age est inférieur à 10 ans
        #   - Est non indemnisé ou que son ARE est inférieure ou égale à l'ARE minimale
        #   - Est en reprise d'emploi du type CDI, CDD, CTT d'au moins 3 mois consécutifs
        #       - Ou en processur d'entrée en formation supérieure ou égale à 40 heures

        annee_glissante = period.start.period('year').offset(-1).offset(-1, 'month')
        pe_categorie_demandeur_emploi = famille.members('pe_categorie_demandeur_emploi', period)#  Famille avec 0 parents? FIXME
        categorie_eligible = pe_categorie_demandeur_emploi in [
            TypesCategorie.categorie_1,
            TypesCategorie.categorie_2,
            TypesCategorie.categorie_3,
            TypesCategorie.categorie_4,
            TypesCategorie.categorie_5
        ]

        agepi_non_percue = famille('agepi', annee_glissante, options=[ADD]) == 0

        #ARE_max = famille('allocation_retour_emploi', period) <= parameters.montant_minimum
        #print(ARE_max)

        #return agepi_non_percue * pe_categorie_demandeur_emploi * ARE_max != 0
        print(categorie_eligible)
        return agepi_non_percue and categorie_eligible

class agepi(Variable):
    value_type = float
    entity = Famille
    label = "Montant de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi"
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20"
    ]

    def formula(famille, period, parameters):
        isole = famille('nb_parents', period) == 1
        nb_heures = famille.sum(famille.members('agepi_temps_travail_semaine', period), role=Famille.PARENT)
        nbenf = famille('pe_nbenf', period)
        agepi_eligible = famille('agepi_eligible', period)

        montants = parameters(period).prestations_sociales.prestations_familiales.education_presence_parentale.agepi.montants
        montant_moins_de_15h = montants.moins_de_15h_par_semaine.calc(nbenf)
        montant_plus_de_15h = montants.plus_de_15h_par_semaine.calc(nbenf)

        montant = (nb_heures < 15) * montant_moins_de_15h + (nb_heures >= 15) * montant_plus_de_15h

        return agepi_eligible * isole * (nb_heures > 0) * montant


class pe_categorie_demandeur_emploi(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Catégorie du demandeur d'emploi"
    reference = [
        "Annexe 3 : la fiche 3 - Les effets de l’inscription - 1. Catégories administratives"
        "http://www.bo-pole-emploi.org/bulletinsofficiels/instruction-n2016-33-du-6-octobr.html?type=dossiers/2016/bope-n2016-80-du-17-novembre-201#"
    ]

    def formula(individu, period, parameters):
        # Renvoi true si l'individu appartient à une catégorie et par conséquent inscrit comme demandeur d'emploi chez Pôle Emploi
        agepi = individu('agepi', period)
        return agepi != 0
