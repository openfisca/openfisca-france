from datetime import date

import numpy as np
from openfisca_core.populations import ADD

from openfisca_france.model.base import Individu, Variable, MONTH, Enum, not_, \
    set_input_dispatch_by_period, set_input_divide_by_period, min_
from openfisca_france.model.caracteristiques_socio_demographiques.logement import TypesLieuResidence
from openfisca_france.model.prestations.agepi import TypesCategoriesDemandeurEmploi, TypesContrat


class amob_date_demande(Variable):
    value_type = date
    default_value = date(1870, 1, 1)
    entity = Individu
    label = "Date de demande d'évaluation à l'éligibilité de l'aide à la mobilité (AMOB) - (date du fait générateur)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"


class distance_aller_retour_activite_domicile(Variable):
    entity = Individu
    value_type = float
    reference = "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
    label = "Distance en kilomètres entre le lieu de l’entretien d’embauche, la reprise d’emploi, la formation, la prestation d’accompagnement, " \
            "l’immersion professionnelle (PMSMP), le concours public ou l’examen certifiant et le lieu de résidence du demandeur d'emploi"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class amob_duree_trajet(Variable):
    entity = Individu
    value_type = float
    reference = "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
    label = "Durée en minutes entre le lieu de l’entretien d’embauche, la reprise d’emploi, la formation, la prestation d’accompagnement, " \
            "l’immersion professionnelle (PMSMP), le concours public ou l’examen certifiant et le lieu de résidence du demandeur d'emploi"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class nuitees(Variable):
    entity = Individu
    value_type = int
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
        ]
    label = "Nombre de nuitées pour le calcul de l'aide à la mobilité de Pôle emploi - AMOB"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class repas(Variable):
    entity = Individu
    value_type = int
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
        ]
    label = "Nombre de repas pour le calcul de l'aide à la mobilité de Pôle emploi - AMOB"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class ContexteActivitePoleEmploi(Enum):
    __order__ = 'indetermine formation reprise_emploi recherche_emploi'  # Needed to preserve the enum order in Python 2
    indetermine = "INDETERMINE"
    formation = "FORMATION"
    reprise_emploi = "REPRISE_EMPLOI"
    recherche_emploi = "RECHERCHE_EMPLOI"


class contexte_activite_pole_emploi(Variable):
    value_type = Enum
    possible_values = ContexteActivitePoleEmploi
    default_value = ContexteActivitePoleEmploi.indetermine
    entity = Individu
    label = "Les différents contextes d'activité pour le calcul de l'aide à la mobilité de Pôle Emploi - AMOB "
    definition_period = MONTH


class formation_validee_par_PoleEmploi(Variable):
    value_type = bool
    entity = Individu
    label = "La formation de l'individu est validée par Pôle emploi"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class formation_financee_ou_cofinancee(Variable):
    value_type = bool
    entity = Individu
    label = "La formation de l'individu est financée ou cofinancée (compte personnel de formation (CPF), fonds propres, Pôle Emploi, un tiers)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class TypesActiviteEnRechercheEmploi(Enum):
    __order__ = 'indetermine entretien_embauche concours_public examen_certifiant prestation_accompagnement immersion_professionnelle_PMSMP'  # Needed to preserve the enum order in Python 2
    indetermine = "INDETERMINE"
    entretien_embauche = "ENTRETIEN_EMBAUCHE"
    concours_public = "CONCOURS_PUBLIC"
    examen_certifiant = "EXAMEN_CERTIFIANT"
    prestation_accompagnement = "PRESTATION_ACCOMPAGNEMENT"
    immersion_professionnelle_PMSMP = "IMMERSION_PROFESSIONNELLE_PMSMP"


class types_activite_en_recherche_emploi(Variable):
    value_type = Enum
    possible_values = TypesActiviteEnRechercheEmploi
    default_value = TypesActiviteEnRechercheEmploi.indetermine
    entity = Individu
    label = "Les types d'activité dans un contexte de recherche d'emploi pour l'aide à la mobilité de Pôle Emploi - AMOB"
    definition_period = MONTH


class amob_montants_allocation_eligibles(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Montant des allocations éligibles pour l'aide à la mobilité de Pôle Emploi - AMOB - Hors Mayotte / Mayotte"
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
        ]

    def formula_2021_06_09(individu, period, parameters):

        #  Diminution de la précision car la comparaison : 14.77 <= 14.77 me renvoyait un False
        epsilon = 0.0001
        lieu_de_residence = individu.menage('residence', period)
        mayotte = lieu_de_residence == TypesLieuResidence.mayotte
        hors_mayotte = not_(mayotte)

        allocation_individu = individu('allocation_retour_emploi', period)

        allocation_minimale_hors_mayotte = parameters(period).allocation_retour_emploi.montant_minimum_hors_mayotte * hors_mayotte
        allocation_minimale_mayotte = parameters(period).allocation_retour_emploi.montant_minimum_mayotte * mayotte

        allocation_minimale_en_fonction_de_la_region = allocation_minimale_hors_mayotte + allocation_minimale_mayotte

        are_individu_egale_are_min = np.fabs(allocation_individu - allocation_minimale_en_fonction_de_la_region) < epsilon
        are_individu_inferieure_are_min = allocation_individu < allocation_minimale_en_fonction_de_la_region

        return are_individu_inferieure_are_min + are_individu_egale_are_min


class amob_categories_eligibles(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Catégories éligibles du demandeur d'emploi pour l'aide à la mobilité de Pôle Emploi - AMOB"
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
        ]

    def formula_2021_06_09(individu, period):

        pe_categorie_demandeur_emploi = individu('pole_emploi_categorie_demandeur_emploi', period)

        stagiaire_formation_professionnelle = individu('stagiaire', period)
        contrat_aide = individu('en_contrat_aide', period)

        categorie_4 = pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_4
        categorie_4_stagiaire_formation_professionnelle = categorie_4 * stagiaire_formation_professionnelle

        categorie_5 = pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_5
        categorie_5_contrat_aide = categorie_5 * contrat_aide

        categories_eligibles = ((pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_1)
                                + (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_2)
                                + (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_3)
                                + (categorie_4_stagiaire_formation_professionnelle + categorie_5_contrat_aide)
                                + (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_6)
                                + (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_7)
                                + (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_8))

        return categories_eligibles


class amob_distances_et_durees_aller_retour_eligibles(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Distance ou la durée éligibles entre le lieu d'activité et de résidence pour l'aide à la mobilité de Pôle Emploi - AMOB"
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
        ]

    def formula_2021_06_09(individu, period, parameters):

        temps_de_trajet = individu('amob_duree_trajet', period)
        lieu_de_residence = individu.menage('residence', period)
        distance_aller_retour = individu('distance_aller_retour_activite_domicile', period)

        amob_parametres = parameters(period).prestations.amob
        distance_minimum_en_metropole = amob_parametres.distance_minimum.metropole
        distance_minimum_hors_metropole = amob_parametres.distance_minimum.hors_metropole
        temps_de_trajet_max = amob_parametres.duree_trajet_minimum
        reside_en_metropole = lieu_de_residence == TypesLieuResidence.metropole
        residence_renseignee = not_(lieu_de_residence == TypesLieuResidence.non_renseigne)

        distances_et_durees_aller_retour_eligibles = (((distance_aller_retour > distance_minimum_en_metropole) * reside_en_metropole)
                                                    + ((distance_aller_retour > distance_minimum_hors_metropole) * not_(reside_en_metropole))
                                                    + ((temps_de_trajet > temps_de_trajet_max) * residence_renseignee))

        return distances_et_durees_aller_retour_eligibles


class amob_activites_eligibles(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Les types d'activités éligibles pour l'aide à la mobilité de Pôle Emploi - AMOB"
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
        ]

    def formula_2021_06_09(individu, period, parameters):

        contexte = individu('contexte_activite_pole_emploi', period) #  ENUM formation, reprise_emploi, recherche_emploi...
        activite_en_recherche_emploi = individu('types_activite_en_recherche_emploi', period) #  ENUM entretien embauche, concours ...
        reprises_emploi_types_activites = individu('types_activite_condition', period) #  ENUM cdi, cdd, ctt, formation
        formation_validee = individu('formation_validee_par_PoleEmploi', period)
        formation_financee = individu('formation_financee_ou_cofinancee', period)

        #  Contexte
        en_formation = contexte == ContexteActivitePoleEmploi.formation
        en_reprise_emploi = contexte == ContexteActivitePoleEmploi.reprise_emploi
        en_recherche_emploi = contexte == ContexteActivitePoleEmploi.recherche_emploi

        # Activites en recherche d'emploi
        en_entretien_embauche = (activite_en_recherche_emploi == TypesActiviteEnRechercheEmploi.entretien_embauche) * en_recherche_emploi

        activites_en_recherche_emploi_eligibles = not_((activite_en_recherche_emploi == TypesActiviteEnRechercheEmploi.entretien_embauche)
                                                     + (activite_en_recherche_emploi == TypesActiviteEnRechercheEmploi.indetermine)) \
                                                     * en_recherche_emploi

        reprises_types_activites_formation = reprises_emploi_types_activites == TypesContrat.formation
        reprises_types_activites_cdi = reprises_emploi_types_activites == TypesContrat.cdi
        reprises_types_activites_cdd = reprises_emploi_types_activites == TypesContrat.cdd
        reprises_types_activites_ctt = reprises_emploi_types_activites == TypesContrat.ctt

        #  Le durée de contrat de l'emploi doit être d'au moins 3 mois
        duree_de_contrat_3_mois_minimum = individu('contrat_de_travail_duree', period) >= 3

        reprises_cdd_ctt_eligibles = (reprises_types_activites_cdd + reprises_types_activites_ctt) * duree_de_contrat_3_mois_minimum

        types_et_duree_activite_eligibles = (((reprises_types_activites_cdi + reprises_cdd_ctt_eligibles) * (en_reprise_emploi + en_entretien_embauche))
                                            + (reprises_types_activites_formation * en_formation * formation_validee * formation_financee))

        activites_eligibles = (types_et_duree_activite_eligibles
                              + activites_en_recherche_emploi_eligibles)

        return activites_eligibles


class amob_calcul_condition_date_de_depot_formation_reprise(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Calcul de la condition de date de dépot dans un contexte de formation ou de reprise d'emploi pour l'aide à la mobilité de Pôle Emploi - AMOB"
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
        ]
    documentation = '''
        Calcul de la condition de date de dépot dans un contexte de formation ou de reprise d'emploi :
        La demande doit être faite au plus tard dans le mois (de date à date) suivant :
            - la reprise d'emploi 
            - l’entrée en formation ou en stage en entreprise lorsque celui est prévu dans le parcours de formation
    '''

    def formula_2021_06_09(individu, period):

        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)  # numpy.datetime64
        contrat_de_travail_debut_en_mois = contrat_de_travail_debut.astype('M8[M]')

        date_limite_eligibilite_contrat = min_((contrat_de_travail_debut_en_mois + 1) + (contrat_de_travail_debut - contrat_de_travail_debut_en_mois),
                                               (contrat_de_travail_debut_en_mois + 2) - np.timedelta64(1, 'D'))

        amob_date_de_demande = individu("amob_date_demande", period)

        return amob_date_de_demande <= date_limite_eligibilite_contrat


class amob_calcul_condition_date_de_depot_recherche(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Calcul de la condition de date de dépot dans un contexte de recherche d'emploi pour l'aide à la mobilité de Pôle Emploi - AMOB"
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
        ]
    documentation = '''
        Calcul de la condition de date de dépot dans un contexte de recherche d'emploi :
        La demande doit être faite de préférence avant :
            - l’entretien d’embauche, 
            - la prestation d’accompagnement,
            - la participation à un concours public,
            - ou à un examen certifiant
        et au plus tard dans un délai de 7 jours de date à date, après ceux-ci
    '''

    def formula_2021_06_09(individu, period, parameters):

        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)  # numpy.datetime64
        date_limite_eligibilite_contrat = contrat_de_travail_debut + parameters(period).prestations.amob.delai_max
        amob_date_de_demande = individu("amob_date_demande", period)

        return amob_date_de_demande <= date_limite_eligibilite_contrat


class amob_contextes_eligibles(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Contextes éligibles à l'aide à la mobilité de Pôle Emploi - AMOB"
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
        ]

    def formula_2021_06_09(individu, period):

        contexte = individu('contexte_activite_pole_emploi', period)
        dates_demandes_amob_eligibles_formation_reprise = individu('amob_calcul_condition_date_de_depot_formation_reprise', period)
        dates_demandes_amob_eligibles_recherche = individu('amob_calcul_condition_date_de_depot_recherche', period)
        en_recherche_emploi = contexte == ContexteActivitePoleEmploi.recherche_emploi
        en_reprise_emploi = contexte == ContexteActivitePoleEmploi.reprise_emploi
        en_formation = contexte == ContexteActivitePoleEmploi.formation

        return (en_recherche_emploi * dates_demandes_amob_eligibles_recherche) + ((en_reprise_emploi + en_formation) * dates_demandes_amob_eligibles_formation_reprise )


class amob_eligible(Variable):
    value_type = bool
    entity = Individu
    label = "Eligibilité à l'aide à la mobilité de Pôle Emploi - AMOB"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
        ]
    documentation = '''
        1- L'individu doit être dans un contexte de recherche d'emploi, reprise d'emploi ou d'entrée en formation
            1.1 - Pour une formation ou une reprise d'emploi, la demande doit être faite au plus tard dans le mois suivant
            1.2 - Pour une recherche d'emploi, la demande doit être faite avant l'entretien d'embauche ou au plus tard dans un délai de 7 jours
        2- L'individu est inscrit en catégorie 1, 2, 3, 4 "stagiaire de la formation professionnelle" ou 5 "contrat aidé", 6, 7 ou 8
        3- L'individu est non indemnisé ou son allocation est inférieure ou égale à l'ARE minimale
        4- L'emploi ou la formation se situe en France
        5- L'individu ne doit pas avoir dépassé son plafond de 5000€ d'aide annuel
        6-  
            6.1 - Son "activité" doit être à plus de 60 km aller-retour de son lieu de résidence
            6.2 - Ou 20 km lorsque l'individu réside en dehors de la métropole
            6.3 - Ou 2 heures de trajet aller-retour
        7- La formation doit être validée par Pôle Emploi

    '''

    def formula_2021_06_09(individu, period, parameters):

        #  1
        contextes_eligibles = individu('amob_contextes_eligibles', period)

        #  2
        activites_eligibles = individu('amob_activites_eligibles', period)

        #  3
        categories_eligibles = individu('amob_categories_eligibles', period)

        #  4
        montants_allocation_eligibles = individu('amob_montants_allocation_eligibles', period)

        #  5
        lieux_activite_eligibles = individu('emploi_ou_formation_en_france', period)

        #  6
        montant_eligible = individu('amob_plafond_disponible', period) >= 0

        #  7
        distances_et_durees_aller_retour_eligibles = individu('amob_distances_et_durees_aller_retour_eligibles', period)


        eligibilite_amob = (contextes_eligibles
                       * activites_eligibles
                       * categories_eligibles
                       * montants_allocation_eligibles
                       * lieux_activite_eligibles
                       * montant_eligible
                       * distances_et_durees_aller_retour_eligibles)

        return eligibilite_amob


class amob_calcul(Variable):
    value_type = float
    entity = Individu
    label = "Calcul du montant de l'aide à la mobilité - AMOB"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
        ]

    def formula_2021_06_09(individu, period, parameters):

        eligibilite_amob = individu('amob_eligible', period)
        distance_aller_retour = individu('distance_aller_retour_activite_domicile', period)
        nb_nuitees = individu('nuitees', period)
        nb_repas = individu('repas', period)

        montant = parameters(period).prestations.amob.montants

        montants_frais_deplacement = montant.deplacement * distance_aller_retour
        montants_frais_hebergement =  montant.hebergement * nb_nuitees
        montants_frais_repas = montant.repas * nb_repas

        montants = montants_frais_deplacement + montants_frais_hebergement + montants_frais_repas

        return eligibilite_amob * montants


class amob_plafond_disponible(Variable):
    value_type = float
    entity = Individu
    label = "Montant disponible plafonné à 5000€ pour l'aide à la mobilité - AMOB"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n-2021-42-du-8-juin-2021-bope-n2021-43.html?type=dossiers/2021/bope-n-2021-043-du-11-juin-2021"
        ]

    def formula_2021_06_09(individu, period, parameters):

        annee_glissante = period.start.period('year').offset(-1).offset(-1, 'month')
        montant_max = parameters(period).prestations.amob.montants.maximum
        montant_deja_percu = individu('amob_calcul', annee_glissante, options=[ADD])

        montant_plafonne = montant_max - montant_deja_percu

        return montant_plafonne