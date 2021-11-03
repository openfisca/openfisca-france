import numpy as np
from openfisca_core.periods import DAY

from openfisca_france.model.base import Famille, Individu, Variable, MONTH, ADD, set_input_dispatch_by_period, \
    set_input_divide_by_period, Enum

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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

    def formula(famille, period):
        age_enfant_eligible = famille('agepi_eligible', period)
        nb_enfants_eligibles = famille.sum(age_enfant_eligible, role=Famille.ENFANT)
        return nb_enfants_eligibles


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
    pas_de_categorie = "Aucune catégorie"
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


class reside_en_region_mayotte(Variable):
    value_type = bool
    entity = Individu
    label = "L'individu réside en région Mayotte"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class TypesActiviteConditionAGEPI(Enum):
    __order__ = 'aucune_activite cdi cdd ctt formation'  # Needed to preserve the enum order in Python 2
    aucune_activite = "AUCUNE ACTIVITE"
    cdi = "CDI"
    cdd = "CDD"
    ctt = "CTT"
    formation = "FORMATION"


class types_activite_condition_agepi(Variable):
    value_type = Enum
    possible_values = TypesActiviteConditionAGEPI
    default_value = TypesActiviteConditionAGEPI.aucune_activite
    entity = Individu
    label = "Les types d'activité éligibles à l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI "
    definition_period = MONTH


class TypesIntensiteActivite(Enum):
    __order__ = 'intensite_non_valide hebdomadaire mensuelle'  # Needed to preserve the enum order in Python 2
    intensite_non_valide = "INTENSITE_NON_VALIDE"
    hebdomadaire = "HEBDOMADAIRE"
    mensuelle = "MENSUELLE"


class types_intensite_activite(Variable):
    value_type = Enum
    possible_values = TypesIntensiteActivite
    default_value = TypesIntensiteActivite.mensuelle
    entity = Individu
    label = "Les types d'intensité pour le calcul de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI "
    definition_period = MONTH


class agepi_eligible(Variable):
    value_type = bool
    entity = Famille
    label = "Eligibilité à l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20"
    ]
    documentation = '''
        Mes conditions
    '''

    def formula(famille, period, parameters):
        # Renvoie true si :
        #   1- L'individu élève seul son enfant dont l'âge est inférieur à 10 ans (condition de garde d'enfant)
        #   2- L'individu n'a pas touché l'AGEPI dans les 12 derniers mois (condition de durée entre faits générateurs)
        #   FIXME 3- L'individu est inscrit en catégorie 1, 2, 3, 4 "stagiaire de la formation professionnelle" ou
        #      5 "contrat aidé" (condition d'inscription)
        #   4- L'individu effectue sa demande au plus tard dans le mois qui suit sa reprise d'emploi ou de formation
        #      (condition de date dépôt)
        #   5- L'individu est non indemnisé ou son ARE est inférieure ou égale à l'ARE minimale
        #      (condition de ressources)
        #   6- L'individu est en reprise d'emploi du type CDI ou CDD, CTT d'au moins 3 mois consécutifs
        #      ou en processus d'entrée en formation d'une durée supérieure ou égale à 40 heures (condition de durée)

        #  Diminution de la précision car la comparaison : 14.77 <= 14.77 me renvoyait un False
        epsilon = 0.001
        print(f"epsilon = {epsilon}")

        ################################################################################################################
        #  1- L'individu élève seul son enfant dont l'age est inférieur à 10 ans
        ################################################################################################################


        parents_isoles = famille('nb_parents', period) == 1
        est_parent = famille.members.has_role(Famille.PARENT)

        age_enfant = famille.members('age', period)
        print(f"age_enfant: {age_enfant}")
        age_enfant_eligible = (age_enfant < parameters(period).prestations.agepi.age_enfant_maximum) * (age_enfant > 0)
        print(f"age_enfant_eligible: {age_enfant_eligible}")

        for parent in parents_isoles:
            if parent != 1 :
                raise Exception(f"{bcolors.FAIL}Le parent doit elever son enfant seul pour etre eligible a l'AGEPI !{bcolors.ENDC}")

        ################################################################################################################
        #  2- L'individu n'a pas touché l'AGEPI dans les 12 derniers mois FIXME: Ne regarde pas le jour/mois
        ################################################################################################################


        annee_glissante = period.start.period('year').offset(-1)
        agepi_non_percues = famille('agepi', annee_glissante, options=[ADD]) == 0

        #  print(f"annee_glissante: {annee_glissante}")
        print(f"agepi_non_percues: {agepi_non_percues}")

        for agepi_non_percue in agepi_non_percues:
            if agepi_non_percue == 0:
                raise Exception(f"{bcolors.FAIL}Une AGEPI a deja ete percue au cours de la derniere annee!{bcolors.ENDC}")


        ################################################################################################################
        #  3- L'individu est inscrit en catégorie 1, 2, 3, 4 ou 5
        ################################################################################################################

        pe_categorie_demandeur_emploi = famille.members('pole_emploi_categorie_demandeur_emploi', period)

        categories_eligibles = ((pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_1) +
                                (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_2) +
                                (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_3) +
                                (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_4) +
                                (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_5) +
                                (np.logical_not(pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_6)) *
                                (np.logical_not(pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_7)) *
                                (np.logical_not(pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_8)) *
                                (np.logical_not(pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.pas_de_categorie)))

        for categorie_eligible in categories_eligibles:
            if not categorie_eligible:
                raise Exception(f"{bcolors.FAIL}Au moins une categorie renseignee n'est pas eligible a l'AGEPI !{bcolors.ENDC}")

        ################################################################################################################
        #  3.2 - L'individu réside ou non en zone Mayotte
        ################################################################################################################


        resident_en_mayotte = famille.members('reside_en_region_mayotte', period) == True
        ne_resident_pas_en_mayotte = np.logical_not(resident_en_mayotte)

        ################################################################################################################
        # FIXME 4- L'individu effectue sa demande au plus tard dans le mois qui suit sa reprise d'emploi ou de formation
        ################################################################################################################


        # date_demande_agepi = str(period.start.day)
        # print(f"date_demande_agepi: {date_demande_agepi}")
        #
        # test_date_plus_1_mois = str((period.offset(1, 'month')).date)
        # print(f"test_date_plus_1_mois: {test_date_plus_1_mois}")
        #
        # date_debut_contrat_de_travail_plus_un_mois = famille.members('contrat_de_travail_duree', period.offset(1, 'month'))
        #
        # print(f"contrat_de_travail_debut: {famille.members('contrat_de_travail_duree', period)}")
        # print(f"date_debut_contrat_de_travail_plus_un_mois: {date_debut_contrat_de_travail_plus_un_mois}")
        #
        # date_demande_agepi_eligible = (date_demande_agepi < date_debut_contrat_de_travail_plus_un_mois)


        ################################################################################################################
        #  5.1- L'individu est non indemnisé ou que son ARE est inférieure ou égale à l'ARE minimale
        ################################################################################################################

        #  Hors Mayotte

        allocation_individu = famille.members('allocation_retour_emploi', period)
        print(f"allocation_individu: {allocation_individu}")

        allocation_minimale_hors_mayotte = parameters(period).allocation_retour_emploi.montant_minimum_hors_mayotte * ne_resident_pas_en_mayotte

        #  Mayotte

        allocation_minimale_mayotte = parameters(period).allocation_retour_emploi.montant_minimum_mayotte * resident_en_mayotte

        allocation_minimale_en_fonction_de_la_region = allocation_minimale_hors_mayotte + allocation_minimale_mayotte
        print(f"allocation_minimale_en_fonction_de_la_region : {allocation_minimale_en_fonction_de_la_region} ")

        #  Montant ARE minimum en fonction de la région (Mayotte / hors Mayotte)

        are_individu_egale_are_min = np.fabs(allocation_individu - allocation_minimale_en_fonction_de_la_region) < epsilon
        print(f"are_individu_egale_are_min = {are_individu_egale_are_min}")

        are_individu_inferieure_are_min = allocation_individu < allocation_minimale_en_fonction_de_la_region

        montants_are_eligibles = are_individu_inferieure_are_min + are_individu_egale_are_min
        print(f"montant_are_eligible: {montants_are_eligibles}")

        for montant_are_eligible in montants_are_eligibles:
            if not montant_are_eligible:
                raise Exception(f"{bcolors.FAIL}Le montant de l'ARE ne permet pas d'etre eligible a l'AGEPI !{bcolors.ENDC}")

        ################################################################################################################
        #  6- L'individu est en reprise d'emploi du type CDI, CDD, CTT d'au moins 3 mois consécutifs
        #   - Ou en procédure d'entrée en formation supérieure ou égale à 40 heures
        ################################################################################################################


        reprises_types_activites = famille.members('types_activite_condition_agepi', period)

        reprises_types_activites_aucune_activite = np.logical_not(reprises_types_activites == TypesActiviteConditionAGEPI.aucune_activite)
        reprises_types_activites_formation = reprises_types_activites == TypesActiviteConditionAGEPI.formation
        reprises_types_activites_cdi = reprises_types_activites == TypesActiviteConditionAGEPI.cdi
        reprises_types_activites_cdd = reprises_types_activites == TypesActiviteConditionAGEPI.cdd
        reprises_types_activites_ctt = reprises_types_activites == TypesActiviteConditionAGEPI.ctt

        #   La formation doit être supérieure ou égale à 40 heures
        duree_formation = famille.members('heures_remunerees_volume', period)
        periode_formation_eligible = duree_formation >= parameters(period).prestations.agepi.duree_de_formation_minimum

        #   Le durée de contrat de l'emploi doit être d'au moins 3 mois
        periode_de_contrat_3_mois_minimum = famille.members('contrat_de_travail_duree', period) >= 3

        reprises_types_activites_formation_eligible = reprises_types_activites_formation * periode_formation_eligible
        reprises_types_activites_cdd_eligible = reprises_types_activites_cdd * periode_de_contrat_3_mois_minimum
        reprises_types_activites_ctt_eligible = reprises_types_activites_ctt * periode_de_contrat_3_mois_minimum

        type_et_duree_activite_eligible = reprises_types_activites_aucune_activite * \
                                          (reprises_types_activites_formation_eligible + \
                                          reprises_types_activites_cdi + \
                                          reprises_types_activites_cdd_eligible + \
                                          reprises_types_activites_ctt_eligible)

        ################################################################################################################

        date_demande_agepi_eligible = True

        return parents_isoles * \
               est_parent * \
               age_enfant_eligible * \
               agepi_non_percues * \
               categories_eligibles * \
               date_demande_agepi_eligible * \
               montants_are_eligibles * \
               type_et_duree_activite_eligible != 0


class agepi(Variable):
    value_type = float
    entity = Famille
    label = "Montant de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20",
        "2. Aide à la garde d’enfants pour les parents isolés (AGEPI)",
        "http://www.bo-pole-emploi.org/bulletinsofficiels/instruction-dg-n2014-48-du-6-jui.html?type=dossiers/2014/bope-n2014-62-du-18-juin-2014"
    ]

    def formula(famille, period, parameters):
        types_de_contrat = famille.members('types_activite_condition_agepi', period)
        contrat_cdi = types_de_contrat == TypesActiviteConditionAGEPI.cdi
        print(f"contrat_cdi: {contrat_cdi}")
        contrat_autre_que_cdi = np.logical_not(types_de_contrat == TypesActiviteConditionAGEPI.cdi)
        print(f"contrat_autre_que_cdi: {contrat_autre_que_cdi}")
        intensite_activite = famille.members('types_intensite_activite', period)
        nb_heures_semaine = famille.sum(famille.members('agepi_temps_travail_semaine', period), role=Famille.PARENT)

        nb_heures_mensuelles = famille.members('heures_remunerees_volume', period)

        nb_enfants_eligibles = famille('pe_nbenf', period)
        eligibilite_agepi = famille('agepi_eligible', period)

        intensite_hebdomadaire = intensite_activite == TypesIntensiteActivite.hebdomadaire
        intensite_mensuelle = intensite_activite == TypesIntensiteActivite.mensuelle

        resident_en_mayotte = famille.members('reside_en_region_mayotte', period) == True
        ne_resident_pas_en_mayotte = np.logical_not(resident_en_mayotte)

        #  Montants en fonction de la région avec ou sans prise en compte de l'intensite
        montants_hors_mayotte = parameters(period).prestations_sociales.prestations_familiales.education_presence_parentale.agepi.montants.hors_mayotte
        montants_mayotte = parameters(period).prestations_sociales.prestations_familiales.education_presence_parentale.agepi.montants.mayotte

        montant_majore_hors_intensite_hors_mayotte = montants_hors_mayotte.majore.calc(nb_enfants_eligibles) * ne_resident_pas_en_mayotte
        montant_majore_hors_intensite_mayotte = montants_mayotte.majore.calc(nb_enfants_eligibles) * resident_en_mayotte

        ################################################################################################################

        #  Montants en fonction du nombre d'enfants pour une reprise emploi ou formation < 15h/sem - HORS MAYOTTE
        montants_minore_intensite_hebdo_hors_mayotte = montants_hors_mayotte.minore.calc(nb_enfants_eligibles) * ne_resident_pas_en_mayotte * intensite_hebdomadaire
        montants_majore_intensite_hebdo_hors_mayotte = montants_hors_mayotte.majore.calc(nb_enfants_eligibles) * ne_resident_pas_en_mayotte * intensite_hebdomadaire

        #  Montants en fonction du nombre d'enfants pour une reprise emploi ou formation < 64h/mensuelle - HORS MAYOTTE
        montants_minore_intensite_mensuelle_hors_mayotte = montants_hors_mayotte.minore.calc(nb_enfants_eligibles) * ne_resident_pas_en_mayotte * intensite_mensuelle
        montants_majore_intensite_mensuelle_hors_mayotte = montants_hors_mayotte.majore.calc(nb_enfants_eligibles) * ne_resident_pas_en_mayotte * intensite_mensuelle

        ################################################################################################################

        #  Montants en fonction du nombre d'enfants pour une reprise emploi ou formation < 15h/sem - MAYOTTE
        montants_minore_intensite_hebdo_mayotte = montants_mayotte.minore.calc(nb_enfants_eligibles) * resident_en_mayotte * intensite_hebdomadaire
        montants_majore_intensite_hebdo_mayotte = montants_mayotte.majore.calc(nb_enfants_eligibles) * resident_en_mayotte * intensite_hebdomadaire

        #  Montants en fonction du nombre d'enfants pour une reprise emploi ou formation < 64h/mensuelle - MAYOTTE
        montants_minore_intensite_mensuelle_mayotte = montants_mayotte.minore.calc(nb_enfants_eligibles) * resident_en_mayotte * intensite_mensuelle
        montants_majore_intensite_mensuelle_mayotte = montants_mayotte.majore.calc(nb_enfants_eligibles) * resident_en_mayotte * intensite_mensuelle

        ################################################################################################################

        #  Montants minorés / majorés - Hors Mayotte - intensité hebdomadaire
        montants_minores_hors_mayotte = montants_minore_intensite_hebdo_hors_mayotte + montants_minore_intensite_mensuelle_hors_mayotte
        montants_majores_hors_mayotte = montants_majore_intensite_hebdo_hors_mayotte + montants_majore_intensite_mensuelle_hors_mayotte

        #  Montants minorés / majorés - Mayotte - intensité mensuelle
        montants_minores_mayotte = montants_minore_intensite_hebdo_mayotte + montants_minore_intensite_mensuelle_mayotte
        montants_majores_mayotte = montants_majore_intensite_hebdo_mayotte + montants_majore_intensite_mensuelle_mayotte

        #  Association des tableaux de montants - Hors Mayotte / Mayotte - intensité hebdomadaire / mensuelle

        montants_minores_en_fonction_de_la_region = montants_minores_hors_mayotte + montants_minores_mayotte
        montants_majores_en_fonction_de_la_region = montants_majores_hors_mayotte + montants_majores_mayotte

        ################################################################################################################

        # Calcul du montant en fonction du nombre d'heures de la reprise d'emploi ou de formation

        condition_montants_minores_hebdomadaire = (nb_heures_semaine < 15) * intensite_hebdomadaire
        condition_montants_minores_mensuelle = (nb_heures_mensuelles < 64) * intensite_mensuelle

        condition_montants_majores_hebdomadaire = (nb_heures_semaine >= 15) * intensite_hebdomadaire
        condition_montants_majores_mensuelle = (nb_heures_mensuelles >= 64) * intensite_mensuelle

        condition_montants_minores = condition_montants_minores_hebdomadaire + condition_montants_minores_mensuelle
        condition_montants_majores = condition_montants_majores_hebdomadaire + condition_montants_majores_mensuelle

        ################################################################################################################

        montant_avec_intensite = ((condition_montants_minores * montants_minores_en_fonction_de_la_region) + \
                                  (condition_montants_majores * montants_majores_en_fonction_de_la_region)) * \
                                 contrat_autre_que_cdi

        print(f"montant_avec_intensite: {montant_avec_intensite}")

        # Si activite CDI, on ne prend pas en compte l'intensite

        montant_sans_intensite = (montant_majore_hors_intensite_hors_mayotte + montant_majore_hors_intensite_mayotte) * contrat_cdi
        print(f"montant_sans_intensite: {montant_sans_intensite}")

        montants = montant_avec_intensite + montant_sans_intensite

        return eligibilite_agepi * montants
