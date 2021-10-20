from openfisca_core.periods import Period, Instant, instant

from openfisca_france.model.base import Famille, Individu, Variable, MONTH, ADD, set_input_dispatch_by_period, \
    set_input_divide_by_period, Enum


class pe_nbenf(Variable):
    value_type = int
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


class TypesCategoriesDemandeurEmploi(Enum):
    __order__ = 'pas_de_categorie categorie_1 categorie_2 categorie_3 categorie_4 categorie_5 categorie_6 categorie_7 categorie_8 ' \
                # Needed to preserve the enum order in Python 2
    pas_de_categorie = "NA"
    categorie_1 = "Catégorie 1 - Personnes sans emploi, immédiatement disponibles en recherche de CDI plein temps."
    categorie_2 = "Catégorie 2 - Personnes sans emploi, immédiatement disponibles en recherche de CDI à temps partiel."
    categorie_3 = "Catégorie 3 - Personnes sans emploi, immédiatement disponibles en recherche de CDD."
    categorie_4 = "Catégorie 4 - Personnes sans emploi, non immédiatement disponibles et à la recherche d’un emploi."
    categorie_5 = "Catégorie 5 - Personnes non immédiatement disponibles, parce que titulaires d'un ou de plusieurs emplois, et à la recherche d'un autre emploi."
    categorie_6 = "Catégorie 6 - Personnes non immédiatement disponibles, en recherche d'un autre emploi en CDI à plein temps."
    categorie_7 = "Catégorie 7 - Personnes non immédiatement disponibles, en recherche d'un autre emploi en CDI à temps partiel."
    categorie_8 = "Catégorie 8 - Personnes non immédiatement disponibles, en recherche d'un autre emploi en CDD."


class pole_emploi_categorie_demandeur_emploi(Variable):
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/instruction-n2016-33-du-6-octobr.html?type=dossiers/2016/bope-n2016-80-du-17-novembre-201#",
        "Annexe 3 : la fiche 3 - Les effets de l’inscription"
    ]
    value_type = Enum
    possible_values = TypesCategoriesDemandeurEmploi
    default_value = TypesCategoriesDemandeurEmploi.pas_de_categorie
    entity = Individu
    label = "Le classement des demandeurs d’emploi dans les différentes catégories d’inscription à Pôle Emploi"
    definition_period = MONTH


class agepi_eligible(Variable):
    value_type = bool
    entity = Famille
    label = "Eligibilité à l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    # set_input = set_input_divide_by_period
    reference = [
        "Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20"
    ]


    def formula(famille, period, parameters):
        # Renvoi true si :
        #   1- L'individu élève seul son enfant dont l'age est inférieur à 10 ans
        #   2- L'individu n'a pas touché l'AGEPI dans les 12 derniers mois
        #   3- L'individu est inscrit en catégorie 1, 2, 3, 4 ou 5
        #   4- L'individu effectue sa demande au plus tard dans le mois qui suit sa reprise d'emploi ou de formation
        #   5- L'individu est non indemnisé ou que son ARE est inférieure ou égale à l'ARE minimale
        #   6- L'individu est en reprise d'emploi du type CDI, CDD, CTT d'au moins 3 mois consécutifs
        #       - Ou en processur d'entrée en formation supérieure ou égale à 40 heures

        #  1- L'individu élève seul son enfant dont l'age est inférieur à 10 ans

        parent_isole = famille('nb_parents', period) == 1
        #  TODO enfants_eligibles

        #  2- L'individu n'a pas touché l'AGEPI dans les 12 derniers mois

        annee_glissante = period.start.period('year').offset(-1).offset(-1, 'month')
        agepi_non_percue = famille('agepi', annee_glissante, options=[ADD]) == 0

        #  3- L'individu est inscrit en catégorie 1, 2, 3, 4 ou 5

        pe_categorie_demandeur_emploi = famille.members('pole_emploi_categorie_demandeur_emploi', period)

        # print("pe_categorie_demandeur_emploi = " + str(pe_categorie_demandeur_emploi))
        categories_eligibles = ((pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_1) +
                                (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_2) +
                                (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_3) +
                                (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_4) +
                                (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_5))

        #  4- L'individu effectue sa demande au plus tard dans le mois qui suit sa reprise d'emploi ou de formation

        # date_demande_agepi = str(period.date)
        # print(f"date_demande_agepi: {date_demande_agepi}")
        #
        # test_date_plus_1_mois = str((period.offset(1, 'month')).date)
        # print(f"test_date_plus_1_mois: {test_date_plus_1_mois}")
        #
        # date_debut_contrat_de_travail_plus_un_mois = famille.members('contrat_de_travail_debut', period.offset(1, 'month'))
        #
        # print(f"contrat_de_travail_debut: {famille.members('contrat_de_travail_debut', period)}")
        # print(f"date_debut_contrat_de_travail_plus_un_mois: {date_debut_contrat_de_travail_plus_un_mois}")

        #date_demande_agepi_eligible = (date_demande_agepi <= date_debut_contrat_de_travail_plus_un_mois)

        #  5- L'individu est non indemnisé ou que son ARE est inférieure ou égale à l'ARE minimale

        allocation_individu = famille.members('allocation_retour_emploi', period)
        print(f"alloc_user: {allocation_individu}")

        allocation_minimale = parameters(period).allocation_retour_emploi.montant_minimum
        print(f"alloc_mini: {allocation_minimale}")

        montant_ARE_eligible = allocation_individu <= allocation_minimale
        print(f"montant_ARE_eligible: {montant_ARE_eligible}")

        #   TODO 6- L'individu est en reprise d'emploi du type CDI, CDD, CTT d'au moins 3 mois consécutifs
        #       - Ou en processur d'entrée en formation supérieure ou égale à 40 heures
        #

        date_demande_agepi_eligible = True

        return parent_isole * agepi_non_percue * categories_eligibles * date_demande_agepi_eligible * montant_ARE_eligible != 0


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
        nb_heures = famille.sum(famille.members('agepi_temps_travail_semaine', period), role=Famille.PARENT)
        nbenf = famille('pe_nbenf', period)
        agepi_eligible = famille('agepi_eligible', period)

        montants = parameters(period).prestations_sociales.prestations_familiales.education_presence_parentale.agepi.montants
        montant_moins_de_15h = montants.moins_de_15h_par_semaine.calc(nbenf)
        montant_plus_de_15h = montants.plus_de_15h_par_semaine.calc(nbenf)

        montant = (nb_heures < 15) * montant_moins_de_15h + (nb_heures >= 15) * montant_plus_de_15h

        return agepi_eligible * (nb_heures > 0) * montant
