from numpy import fabs, timedelta64

from openfisca_france.model.base import Famille, Individu, Variable, Enum, MONTH, ADD,\
    set_input_dispatch_by_period, set_input_divide_by_period, date, min_, not_
from openfisca_france.model.revenus.activite.salarie import TypesContrat, TypesLieuEmploiFormation,\
    TypesCategoriesDemandeurEmploi


class agepi_nbenf(Variable):
    value_type = int
    entity = Famille
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    label = "Nombre d'enfants pour le calcul de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    reference = [
        'Article 2 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi',
        'http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20'
        ]

    def formula_2014_01_20(famille, period, parameters):
        age_membres_famille = famille.members('age', period)
        parametres_agepi = parameters(period).prestations_sociales.prestations_familiales.education_presence_parentale.agepi
        age_eligibles = (age_membres_famille < parametres_agepi.age_enfant_maximum) * (age_membres_famille > 0)
        nb_enfants_eligibles = famille.sum(age_eligibles, role=Famille.ENFANT)

        return nb_enfants_eligibles


class agepi_temps_travail_en_heure(Variable):
    value_type = float
    entity = Individu
    label = "Temps de travail en heures pour le calcul de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    set_input = set_input_divide_by_period


class TypesIntensiteActivite(Enum):
    __order__ = 'inconnue hebdomadaire mensuelle'  # Needed to preserve the enum order in Python 2
    inconnue = "Intensité d'emploi ou de formation inconnue"
    hebdomadaire = "Intensité d'emploi ou de formation hebdomadaire"
    mensuelle = "Intensité d'emploi ou de formation mensuelle"


class type_intensite_activite(Variable):
    value_type = Enum
    possible_values = TypesIntensiteActivite
    default_value = TypesIntensiteActivite.inconnue
    entity = Individu
    label = "Le type d'intensité d'activité au regard de Pôle Emploi"
    definition_period = MONTH
    documentation = '''
    L'intensité d'activité est évaluée en fonction de son type (hebdomadaire, ...)
    et du nombre d'heures requises.
    '''


class agepi_date_demande(Variable):
    value_type = date
    default_value = date(1, 1, 1)
    entity = Individu
    label = "Date de demande d'évaluation à l'éligibilité à l'AGEPI (date du fait générateur)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = 'http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20'


class agepi_eligible(Variable):
    value_type = bool
    entity = Individu
    label = "Eligibilité à l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi',
        'http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20'
        ]

    def formula_2014_01_20(individu, period, parameters):
        # L'individu élève seul son enfant (parent isolé)
        parents_isoles = individu.famille('nb_parents', period) == 1

        # L'âge du ou des enfants dont il a la garde est inférieur à 10 ans (condition de garde d'enfant)
        condition_nb_enfants = individu.famille('agepi_nbenf', period) > 0

        # L'individu n'a pas touché l'AGEPI dans les 12 derniers mois (condition de durée entre faits générateurs)
        annee_glissante = period.start.period('year').offset(-1).offset(-1, 'month')
        agepi_non_percues = not_(individu('agepi', annee_glissante, options=[ADD]))

        # L'individu est inscrit en catégorie 1, 2, 3, 4 "stagiaire de la formation professionnelle" ou 5 "contrat aidé"
        pe_categorie_demandeur_emploi = individu('pole_emploi_categorie_demandeur_emploi', period)

        stagiaire_formation_professionnelle = individu('stagiaire', period)
        contrat_aide = individu('contrat_aide', period)

        categorie_4 = pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_4
        categorie_4_stagiaire_formation_professionnelle = categorie_4 * stagiaire_formation_professionnelle

        categorie_5 = pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_5
        categorie_5_contrat_aide = categorie_5 * contrat_aide

        categories_eligibles = ((pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_1)
                                + (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_2)
                                + (pe_categorie_demandeur_emploi == TypesCategoriesDemandeurEmploi.categorie_3)
                                + (categorie_4_stagiaire_formation_professionnelle + categorie_5_contrat_aide))

        # L'emploi ou la formation se situe en France
        lieux_activite_eligibles = not_(individu('lieu_emploi_ou_formation', period) == TypesLieuEmploiFormation.non_renseigne)

        # L'individu effectue sa demande au plus tard dans le mois qui suit sa reprise d'emploi ou de formation
        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)  # numpy.datetime64
        contrat_de_travail_debut_en_mois = contrat_de_travail_debut.astype('M8[M]')

        date_demande_limite = min_(
            (contrat_de_travail_debut_en_mois + 1) + (contrat_de_travail_debut - contrat_de_travail_debut_en_mois),
            (contrat_de_travail_debut_en_mois + 2) - timedelta64(1, 'D')
            )

        agepi_date_de_demande = individu('agepi_date_demande', period)
        dates_demandes_agepi_eligibles = agepi_date_de_demande <= date_demande_limite

        # L'individu est non indemnisé ou son ARE est inférieure ou égale à l'ARE minimale
        mayotte = individu.menage('residence_mayotte', period)
        hors_mayotte = not_(mayotte)

        allocation_individu = individu('allocation_retour_emploi_journaliere', period)

        parametres_are = parameters(period).chomage.allocation_retour_emploi
        allocation_minimale_hors_mayotte = parametres_are.montant_minimum_hors_mayotte * hors_mayotte
        allocation_minimale_mayotte = parametres_are.montant_minimum_mayotte * mayotte

        allocation_minimale_en_fonction_de_la_region = allocation_minimale_hors_mayotte + allocation_minimale_mayotte

        # Montant ARE minimum en fonction de la région (Mayotte / hors Mayotte)
        # (et diminution de la précision car une comparaison : 14.77 <= 14.77 renvoyait un False)
        epsilon = 0.0001
        are_individu_egale_are_min = fabs(allocation_individu - allocation_minimale_en_fonction_de_la_region) < epsilon
        are_individu_inferieure_are_min = allocation_individu < allocation_minimale_en_fonction_de_la_region

        montants_are_eligibles = are_individu_inferieure_are_min + are_individu_egale_are_min

        # L'individu est en reprise d'emploi du type CDI, CDD ou CTT d'au moins 3 mois consécutifs ou en processus d'entrée en formation d'une durée supérieure ou égale à 40 heures
        reprises_types_activites = individu('contrat_de_travail_type', period)

        reprises_types_activites_formation = reprises_types_activites == TypesContrat.formation
        reprises_types_activites_cdi = reprises_types_activites == TypesContrat.cdi
        reprises_types_activites_cdd = reprises_types_activites == TypesContrat.cdd
        reprises_types_activites_ctt = reprises_types_activites == TypesContrat.ctt

        # La formation doit être supérieure ou égale à 40 heures
        duree_formation = individu('duree_formation', period)
        parametres_agepi = parameters(period).prestations_sociales.prestations_familiales.education_presence_parentale.agepi
        periode_formation_eligible = duree_formation >= parametres_agepi.duree_de_formation_minimum

        # Le durée de contrat de l'emploi doit être d'au moins 3 mois
        periode_de_contrat_3_mois_minimum = individu('contrat_de_travail_duree', period) >= parametres_agepi.duree_cdd_ctt_minimum

        reprises_types_activites_formation_eligible = reprises_types_activites_formation * periode_formation_eligible
        reprises_types_activites_cdd_eligible = reprises_types_activites_cdd * periode_de_contrat_3_mois_minimum
        reprises_types_activites_ctt_eligible = reprises_types_activites_ctt * periode_de_contrat_3_mois_minimum

        types_et_duree_activite_eligibles = (reprises_types_activites_formation_eligible
                                            + reprises_types_activites_cdi
                                            + reprises_types_activites_cdd_eligible
                                            + reprises_types_activites_ctt_eligible)

        eligible_agepi = (parents_isoles
            * condition_nb_enfants
            * agepi_non_percues
            * categories_eligibles
            * lieux_activite_eligibles
            * dates_demandes_agepi_eligibles
            * montants_are_eligibles
            * types_et_duree_activite_eligibles)

        return eligible_agepi


class agepi_hors_mayotte(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI - Cas HORS MAYOTTE"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi',
        'http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20',
        '2. Aide à la garde d’enfants pour les parents isolés (AGEPI)'
        ]

    def formula_2014_01_20(individu, period, parameters):
        est_parent = individu.has_role(Famille.PARENT)
        intensite_activite = individu('type_intensite_activite', period)
        nb_heures = individu('agepi_temps_travail_en_heure', period)
        nb_enfants_eligibles = individu.famille('agepi_nbenf', period)
        eligibilite_agepi = individu('agepi_eligible', period)

        intensite_hebdomadaire = intensite_activite == TypesIntensiteActivite.hebdomadaire
        intensite_mensuelle = intensite_activite == TypesIntensiteActivite.mensuelle

        hors_mayotte = not_(individu.menage('residence_mayotte', period))

        parametres_agepi = parameters(period).prestations_sociales.prestations_familiales.education_presence_parentale.agepi
        parametres_montants = parametres_agepi.montants.hors_mayotte
        montants_min_hors_mayotte = parametres_montants.minimum.calc(nb_enfants_eligibles)
        montants_max_hors_mayotte = parametres_montants.maximum.calc(nb_enfants_eligibles)
        intensite_hebdo_seuil = parametres_agepi.intensite_hebdomadaire_seuil
        intensite_mensuelle_seuil = parametres_agepi.intensite_mensuelle_seuil

        montants_min_intensite = montants_min_hors_mayotte * (intensite_hebdomadaire + intensite_mensuelle)
        montants_max_intensite = montants_max_hors_mayotte * (intensite_hebdomadaire + intensite_mensuelle)

        condition_montants_min = ((nb_heures < intensite_hebdo_seuil) * intensite_hebdomadaire) + ((nb_heures < intensite_mensuelle_seuil) * intensite_mensuelle)
        condition_montants_max = ((nb_heures >= intensite_hebdo_seuil) * intensite_hebdomadaire) + ((nb_heures >= intensite_mensuelle_seuil) * intensite_mensuelle)

        montant_avec_intensite = (condition_montants_min * montants_min_intensite) + (condition_montants_max * montants_max_intensite)

        montants = hors_mayotte * (est_parent * montant_avec_intensite)

        return eligibilite_agepi * montants


class agepi_mayotte(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI - Cas MAYOTTE"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi',
        'http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20',
        '2. Aide à la garde d’enfants pour les parents isolés (AGEPI)',
        'http://www.bo-pole-emploi.org/bulletinsofficiels/instruction-dg-n2014-48-du-6-jui.html?type=dossiers/2014/bope-n2014-62-du-18-juin-2014',
        ]

    def formula_2014_01_20(individu, period, parameters):
        est_parent = individu.has_role(Famille.PARENT)
        intensite_activite = individu('type_intensite_activite', period)
        nb_heures = individu('agepi_temps_travail_en_heure', period)
        nb_enfants_eligibles = individu.famille('agepi_nbenf', period)
        eligibilite_agepi = individu('agepi_eligible', period)

        intensite_hebdomadaire = intensite_activite == TypesIntensiteActivite.hebdomadaire
        intensite_mensuelle = intensite_activite == TypesIntensiteActivite.mensuelle

        mayotte = individu.menage('residence_mayotte', period)

        parametres_agepi = parameters(period).prestations_sociales.prestations_familiales.education_presence_parentale.agepi
        parametres_montants = parametres_agepi.montants.mayotte
        montants_min_mayotte = parametres_montants.minimum.calc(nb_enfants_eligibles)
        montants_max_mayotte = parametres_montants.maximum.calc(nb_enfants_eligibles)
        intensite_hebdo_seuil = parametres_agepi.intensite_hebdomadaire_seuil
        intensite_mensuelle_seuil = parametres_agepi.intensite_mensuelle_seuil

        montants_min_intensite = montants_min_mayotte * (intensite_hebdomadaire + intensite_mensuelle)
        montants_max_intensite = montants_max_mayotte * (intensite_hebdomadaire + intensite_mensuelle)

        condition_montants_min = ((nb_heures < intensite_hebdo_seuil) * intensite_hebdomadaire) + ((nb_heures < intensite_mensuelle_seuil) * intensite_mensuelle)
        condition_montants_max = ((nb_heures >= intensite_hebdo_seuil) * intensite_hebdomadaire) + ((nb_heures >= intensite_mensuelle_seuil) * intensite_mensuelle)

        montant_avec_intensite = (condition_montants_min * montants_min_intensite) + (condition_montants_max * montants_max_intensite)

        montants = mayotte * (est_parent * montant_avec_intensite)

        return eligibilite_agepi * montants


class agepi(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide à la garde des enfants de parents isolés de Pôle Emploi - AGEPI"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'Article 4 de la délibération n°2013-46 du 18 décembre 2013 du Pôle Emploi',
        'http://www.bo-pole-emploi.org/bulletinsofficiels/deliberation-n2013-46-du-18-dece.html?type=dossiers/2013/bope-n2013-128-du-24-decembre-20',
        '2. Aide à la garde d’enfants pour les parents isolés (AGEPI)',
        'http://www.bo-pole-emploi.org/bulletinsofficiels/instruction-dg-n2014-48-du-6-jui.html?type=dossiers/2014/bope-n2014-62-du-18-juin-2014',
        ]

    def formula_2014_01_20(individu, period):

        agepi_mayotte = individu('agepi_mayotte', period)
        agepi_hors_mayotte = individu('agepi_hors_mayotte', period)

        return agepi_hors_mayotte + agepi_mayotte
