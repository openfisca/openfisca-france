# -*- coding: utf-8 -*-

import logging

from numpy import busday_count, datetime64, logical_or as or_, logical_and as and_, timedelta64

from openfisca_france.model.base import *

log = logging.getLogger(__name__)


class assiette_allegement(Variable):
    value_type = float
    entity = Individu
    label = "Assiette des allègements de cotisations sociales employeur"
    definition_period = MONTH

    def formula(individu, period, parameters):
        assiette_cotisations_sociales = individu('assiette_cotisations_sociales', period, options = [ADD])
        categorie_salarie = individu('categorie_salarie', period)
        # TODO vérifier changement d'assiette
        return assiette_cotisations_sociales * (
            (categorie_salarie == TypesCategorieSalarie.prive_non_cadre) | (categorie_salarie == TypesCategorieSalarie.prive_cadre)
            )


class coefficient_proratisation(Variable):
    value_type = float
    entity = Individu
    label = "Coefficient de proratisation du salaire notamment pour le calcul du SMIC"
    definition_period = MONTH

    def formula(individu, period, parameters):
        #  * Tous les calculs sont faits sur le mois *

        # Les types de contrats gérés
        contrat_de_travail = individu('contrat_de_travail', period)
        TypesContratDeTravail = contrat_de_travail.possible_values
        # [ temps_plein
        #   temps_partiel
        #   forfait_heures_semaines
        #   forfait_heures_mois
        #   forfait_heures_annee
        #   forfait_jours_annee ]

        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)

        # Volume des heures rémunérées à un forfait heures
        forfait_heures_remunerees_volume = individu('forfait_heures_remunerees_volume', period)  # noqa F841
        # Volume des heures rémunérées à forfait jours
        forfait_jours_remuneres_volume = individu('forfait_jours_remuneres_volume', period)
        heures_duree_collective_entreprise = individu('heures_duree_collective_entreprise', period)
        # Volume des heures rémunérées contractuellement (heures/mois, temps partiel)
        heures_remunerees_volume = individu('heures_remunerees_volume', period)
        # Volume des heures non rémunérées (convenance personnelle hors contrat/forfait)
        heures_non_remunerees_volume = individu('heures_non_remunerees_volume', period)

        # Décompte des jours en début et fin de contrat
        # http://www.gestiondelapaie.com/flux-paie/?1029-la-bonne-premiere-paye

        debut_mois = datetime64(period.start.offset('first-of', 'month'))
        fin_mois = datetime64(period.start.offset('last-of', 'month')) + timedelta64(1,
                                                                                     'D')  # busday ignores the last day

        jours_ouvres_ce_mois = busday_count(
            debut_mois,
            fin_mois,
            weekmask='1111100'
            )

        # jours travaillables sur l'intersection du contrat de travail et du mois en cours
        jours_ouvres_ce_mois_incomplet = busday_count(
            max_(contrat_de_travail_debut, debut_mois),
            min_(contrat_de_travail_fin, fin_mois),
            weekmask='1111100'
            )

        duree_legale_mensuelle = 35 * 52 / 12  # ~151,67

        heures_temps_plein = switch(heures_duree_collective_entreprise,
                                    {0: duree_legale_mensuelle, 1: heures_duree_collective_entreprise})

        jours_absence = heures_non_remunerees_volume / 7

        coefficient_proratisation_temps_partiel = heures_remunerees_volume / heures_temps_plein
        coefficient_proratisation_forfait_jours = forfait_jours_remuneres_volume / 218

        # temps plein
        coefficient = switch(
            contrat_de_travail,
            {  # temps plein
                TypesContratDeTravail.temps_plein: (
                    (jours_ouvres_ce_mois_incomplet - jours_absence)
                    / jours_ouvres_ce_mois
                    ),

                # temps partiel
                # (en l'absence du détail pour chaque jour de la semaine ou chaque semaine du mois)
                TypesContratDeTravail.temps_partiel: coefficient_proratisation_temps_partiel * (
                    (jours_ouvres_ce_mois_incomplet * coefficient_proratisation_temps_partiel - jours_absence)
                    / (jours_ouvres_ce_mois * coefficient_proratisation_temps_partiel + 1e-16)
                    ),

                TypesContratDeTravail.forfait_jours_annee: coefficient_proratisation_forfait_jours * (
                    (jours_ouvres_ce_mois_incomplet * coefficient_proratisation_forfait_jours - jours_absence)
                    / (jours_ouvres_ce_mois * coefficient_proratisation_forfait_jours + 1e-16)
                    )
                }
            )

        #      Forfait en heures
        # coefficient = (contrat_de_travail >= 2) * (contrat_de_travail <= 3) * (
        #     forfait_heures_remunerees_volume / 45.7 * 52 / 12
        #     ) +
        return (jours_ouvres_ce_mois_incomplet > 0) * coefficient


class credit_impot_competitivite_emploi(Variable):
    value_type = float
    entity = Individu
    label = "Crédit d'impôt pour la compétitivité et l'emploi"
    definition_period = MONTH
    calculate_output = calculate_output_add

    def formula_2013_01_01(individu, period, parameters):
        assiette_allegement = individu('assiette_allegement', period)
        jeune_entreprise_innovante = individu('jeune_entreprise_innovante', period)  # noqa F841
        smic_proratise = individu('smic_proratise', period)
        stagiaire = individu('stagiaire', period)
        parameters = parameters(period)
        taux_cice = taux_exo_cice(assiette_allegement, smic_proratise, parameters)
        credit_impot_competitivite_emploi = taux_cice * assiette_allegement
        non_cumul = not_(stagiaire)
        association = individu('entreprise_est_association_non_lucrative', period)

        return credit_impot_competitivite_emploi * non_cumul * not_(association)


class aide_premier_salarie(Variable):
    value_type = float
    entity = Individu
    label = "Aide à l'embauche d'un premier salarié"
    definition_period = MONTH
    calculate_output = calculate_output_add

    def formula_2015_06_09(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)
        apprenti = individu('apprenti', period)
        contrat_de_travail_duree = individu('contrat_de_travail_duree', period)
        TypesContratDeTravailDuree = contrat_de_travail_duree.possible_values
        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)
        coefficient_proratisation = individu('coefficient_proratisation', period)
        exoneration_cotisations_employeur_jei = individu('exoneration_cotisations_employeur_jei', period)

        # Cette aide est temporaire.
        # TODO : Si toutefois elle est reconduite et modifiée pour 2017, les dates et le montant seront à
        # implémenter comme des params xml.

        eligible_contrat = and_(
            contrat_de_travail_debut >= datetime64("2015-06-09"),
            contrat_de_travail_debut <= datetime64("2016-12-31")
            )

        # Si CDD, durée du contrat doit être > 1 an
        eligible_duree = or_(
            # durée indéterminée
            contrat_de_travail_duree == TypesContratDeTravailDuree.cdi,
            # durée déterminée supérieure à 1 an
            and_(
                contrat_de_travail_duree == TypesContratDeTravailDuree.cdd,
                # > 6 mois
                (contrat_de_travail_fin - contrat_de_travail_debut).astype('timedelta64[M]') >= timedelta64(6, 'M')
                # Initialement, la condition était d'un contrat >= 12 mois,
                # pour les demandes transmises jusqu'au 26 janvier.
                )
            )

        eligible_date = datetime64(period.offset(-24, 'month').start) < contrat_de_travail_debut
        eligible = \
            (effectif_entreprise == 1) * not_(apprenti) * eligible_contrat * eligible_duree * eligible_date

        # somme sur 24 mois, à raison de 500 € maximum par trimestre
        montant_max = 4000

        # non cumul avec le dispositif Jeune Entreprise Innovante (JEI)
        non_cumulee = not_(exoneration_cotisations_employeur_jei)

        # TODO comment implémenter la condition "premier employé" ? L'effectif est insuffisant en cas de rupture
        # d'un premier contrat
        # Condition : l’entreprise n’a pas conclu de contrat de travail avec un salarié,
        # au-delà de la période d’essai, dans les 12 mois précédant la nouvelle
        # embauche.

        # Si le salarié est embauché à temps partiel,
        # l’aide est proratisée en fonction de sa durée de travail.
        # TODO cette multiplication par le coefficient de proratisation suffit-elle pour le cas du temps partiel ?
        # A tester
        return eligible * (montant_max / 24) * coefficient_proratisation * non_cumulee


class aide_embauche_pme(Variable):
    value_type = float
    entity = Individu
    label = "Aide à l'embauche d'un salarié pour les PME"
    reference = "http://travail-emploi.gouv.fr/grands-dossiers/embauchepme"
    definition_period = MONTH
    calculate_output = calculate_output_add

    def formula_2016_01_18(individu, period, parameters):
        effectif_entreprise = individu('effectif_entreprise', period)
        apprenti = individu('apprenti', period)
        contrat_de_travail_duree = individu('contrat_de_travail_duree', period)
        TypesContratDeTravailDuree = contrat_de_travail_duree.possible_values
        contrat_de_travail_debut = individu('contrat_de_travail_debut', period)
        contrat_de_travail_fin = individu('contrat_de_travail_fin', period)
        coefficient_proratisation = individu('coefficient_proratisation', period)
        smic_proratise = individu('smic_proratise', period)
        salaire_de_base = individu('salaire_de_base', period)
        exoneration_cotisations_employeur_jei = individu('exoneration_cotisations_employeur_jei', period)
        aide_premier_salarie = individu('aide_premier_salarie', period)

        # Cette aide est temporaire.
        # Si toutefois elle est reconduite et modifiée, les dates et le montant seront à implémenter comme
        # des params xml.

        # jusqu’à 1,3 fois le Smic
        eligible_salaire = salaire_de_base <= (1.3 * smic_proratise)

        # pour les PME
        eligible_effectif = effectif_entreprise < 250

        non_cumulee = and_(
            # non cumulable avec l'aide pour la première embauche
            # qui est identique, si ce n'est qu'elle couvre tous les salaires
            aide_premier_salarie == 0,
            # non cumul avec le dispositif Jeune Entreprise Innovante (JEI)
            not_(exoneration_cotisations_employeur_jei)
            )

        eligible_contrat = and_(
            contrat_de_travail_debut >= datetime64("2016-01-18"),
            contrat_de_travail_debut <= datetime64("2017-06-30")
            )

        # Si CDD, durée du contrat doit être > 1 an
        eligible_duree = or_(
            # durée indéterminée
            contrat_de_travail_duree == TypesContratDeTravailDuree.cdi,
            # durée déterminée supérieure à 1 an
            and_(
                # CDD
                contrat_de_travail_duree == TypesContratDeTravailDuree.cdd,
                # > 6 mois
                (contrat_de_travail_fin - contrat_de_travail_debut).astype('timedelta64[M]') >= timedelta64(6, 'M')
                )
            )

        # Valable 2 ans seulement
        eligible_date = datetime64(period.offset(-24, 'month').start) < contrat_de_travail_debut

        eligible = (
            eligible_salaire
            * eligible_effectif
            * non_cumulee
            * eligible_contrat
            * eligible_duree
            * eligible_date
            * not_(apprenti)
            )

        # somme sur 24 mois, à raison de 500 € maximum par trimestre
        montant_max = 4000

        # Si le salarié est embauché à temps partiel,
        # l’aide est proratisée en fonction de sa durée de travail.
        # TODO cette multiplication par le coefficient de proratisation suffit-elle pour le cas du temps partiel ?
        # A tester

        return eligible * (montant_max / 24) * coefficient_proratisation


class smic_proratise(Variable):
    value_type = float
    entity = Individu
    label = "SMIC proratisé (mensuel)"
    definition_period = MONTH

    def formula(individu, period, parameters):
        coefficient_proratisation = individu('coefficient_proratisation', period)
        smic_horaire_brut = parameters(period).cotsoc.gen.smic_h_b
        smic_proratise = coefficient_proratisation * smic_horaire_brut * 35 * 52 / 12

        return smic_proratise


class allegement_fillon(Variable):
    value_type = float
    entity = Individu
    label = "Allègement de charges employeur sur les bas et moyens salaires (dit allègement Fillon)"
    reference = "https://www.service-public.fr/professionnels-entreprises/vosdroits/F24542"
    definition_period = MONTH
    calculate_output = calculate_output_add

    # Attention : cet allègement a des règles de cumul spécifiques

    def formula_2005_07_01(individu, period, parameters):
        stagiaire = individu('stagiaire', period)
        apprenti = individu('apprenti', period)
        allegement_mode_recouvrement = individu('allegement_fillon_mode_recouvrement', period)
        exoneration_cotisations_employeur_jei = individu('exoneration_cotisations_employeur_jei', period)

        non_cumulee = not_(exoneration_cotisations_employeur_jei)

        # switch on 3 possible payment options
        allegement = switch_on_allegement_mode(
            individu, period, parameters,
            allegement_mode_recouvrement,
            "allegement_fillon",
            )

        return allegement * not_(stagiaire) * not_(apprenti) * non_cumulee


def compute_allegement_fillon(individu, period, parameters):
    """
        Exonération Fillon
        https://www.service-public.fr/professionnels-entreprises/vosdroits/F24542
    """
    # Be careful ! Period is several months
    first_month = period.first_month

    assiette = individu('assiette_allegement', period, options = [ADD])
    smic_proratise = individu('smic_proratise', period, options = [ADD])
    taille_entreprise = individu('taille_entreprise', first_month)
    TypesTailleEntreprise = taille_entreprise.possible_values
    majoration = (
        (taille_entreprise == TypesTailleEntreprise.non_pertinent)
        + (taille_entreprise == TypesTailleEntreprise.moins_de_10)
        + (taille_entreprise == TypesTailleEntreprise.de_10_a_19)
        )  # majoration éventuelle pour les petites entreprises

    # Calcul du taux
    # Le montant maximum de l’allègement dépend de l’effectif de l’entreprise.
    # Le montant est calculé chaque année civile, pour chaque salarié ;
    # il est égal au produit de la totalité de la rémunération annuelle telle
    # que visée à l’article L. 242-1 du code de la Sécurité sociale par un
    # coefficient.
    # Ce montant est majoré de 10 % pour les entreprises de travail temporaire
    # au titre des salariés temporaires pour lesquels elle est tenue à
    # l’obligation d’indemnisation compensatrice de congés payés.

    fillon = parameters(period).prelevements_sociaux.fillon

    # Du 2003-07-01 au 2005-06-30
    if date(2003, 7, 1) <= period.start.date <= date(2005, 6, 30):
        seuil = fillon.entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003.plafond
        tx_max = fillon.entreprises_ayant_signe_un_accord_de_rtt_avant_le_30_06_2003.reduction_maximale
    # Après le 2005-07-01

    else:
        seuil = fillon.ensemble_des_entreprises.plafond
        tx_max = (
            fillon.ensemble_des_entreprises.reduction_maximale.entreprises_de_20_salaries_et_plus
            * not_(majoration)
            + fillon.ensemble_des_entreprises.reduction_maximale.entreprises_de_moins_de_20_salaries
            * majoration
            )

    if seuil <= 1:
        return 0

    ratio_smic_salaire = smic_proratise / (assiette + 1e-16)

    # règle d'arrondi: 4 décimales au dix-millième le plus proche
    taux_fillon = round_(tx_max * min_(1, max_(seuil * ratio_smic_salaire - 1, 0) / (seuil - 1)), 4)

    # Montant de l'allegment
    return taux_fillon * assiette


class allegement_cotisation_allocations_familiales(Variable):
    value_type = float
    label = "Allègement de la cotisation d'allocations familiales sur les bas et moyens salaires"
    entity = Individu
    reference = "https://www.urssaf.fr/portail/home/employeur/calculer-les-cotisations/les-taux-de-cotisations/la-cotisation-dallocations-famil/la-reduction-du-taux-de-la-cotis.html"
    definition_period = MONTH

    def formula_2015_01_01(individu, period, parameters):
        stagiaire = individu('stagiaire', period)
        apprenti = individu('apprenti', period)
        allegement_mode_recouvrement = \
            individu('allegement_cotisation_allocations_familiales_mode_recouvrement', period)
        exoneration_cotisations_employeur_jei = individu('exoneration_cotisations_employeur_jei', period)

        non_cumulee = not_(exoneration_cotisations_employeur_jei)

        # switch on 3 possible payment options
        allegement = switch_on_allegement_mode(
            individu, period, parameters,
            allegement_mode_recouvrement,
            "allegement_cotisation_allocations_familiales",
            )

        return allegement * not_(stagiaire) * not_(apprenti) * non_cumulee


def compute_allegement_cotisation_allocations_familiales(individu, period, parameters):
    """
        La réduction du taux de la cotisation d’allocations familiales
    """
    assiette = individu('assiette_allegement', period, options = [ADD])
    smic_proratise = individu('smic_proratise', period, options = [ADD])
    # TODO: Ne semble pas dépendre de la taille de l'entreprise mais à vérifier
    # taille_entreprise = individu('taille_entreprise', period)
    law = parameters(period).prelevements_sociaux.allegement_cotisation_allocations_familiales

    # Montant de l'allegment
    return (assiette < law.plafond_en_nombre_de_smic * smic_proratise) * law.reduction * assiette


###############################
#  Helper functions and classes
###############################


def switch_on_allegement_mode(individu, period, parameters, mode_recouvrement, variable_name):
    """
        Switch on 3 possible payment options for allegements

        Name of the computation method specific to the allegement
        should precisely be the variable name prefixed with 'compute_'
    """
    compute_function = globals()['compute_' + variable_name]
    TypesAllegementModeRecouvrement = mode_recouvrement.possible_values
    recouvrement_fin_annee = (mode_recouvrement == TypesAllegementModeRecouvrement.fin_d_annee)
    recouvrement_anticipe = (mode_recouvrement == TypesAllegementModeRecouvrement.anticipe)
    recouvrement_progressif = (mode_recouvrement == TypesAllegementModeRecouvrement.progressif)

    return (
        (recouvrement_fin_annee * compute_allegement_annuel(individu, period, parameters, variable_name, compute_function))
        + (recouvrement_anticipe * compute_allegement_anticipe(individu, period, parameters, variable_name, compute_function))
        + (recouvrement_progressif * compute_allegement_progressif(individu, period, parameters, variable_name, compute_function))
        )


def compute_allegement_annuel(individu, period, parameters, variable_name, compute_function):
    if period.start.month < 12:
        return 0
    if period.start.month == 12:
        return compute_function(individu, period.this_year, parameters)


def compute_allegement_anticipe(individu, period, parameters, variable_name, compute_function):
    if period.start.month < 12:
        return compute_function(individu, period.first_month, parameters)
    if period.start.month == 12:
        cumul = individu(
            variable_name,
            period.start.offset('first-of', 'year').period('month', 11), options = [ADD])
        return compute_function(
            individu, period.this_year, parameters
            ) - cumul


def compute_allegement_progressif(individu, period, parameters, variable_name, compute_function):
    if period.start.month == 1:
        return compute_function(individu, period.first_month, parameters)

    if period.start.month > 1:
        up_to_this_month = period.start.offset('first-of', 'year').period('month', period.start.month)
        up_to_previous_month = period.start.offset('first-of', 'year').period('month', period.start.month - 1)
        cumul = individu(variable_name, up_to_previous_month, options = [ADD])
        return compute_function(individu, up_to_this_month, parameters) - cumul


def taux_exo_cice(assiette_allegement, smic_proratise, parameters):
    cice = parameters.prelevements_sociaux.cice
    taux_cice = ((assiette_allegement / (smic_proratise + 1e-16)) <= cice.plafond_smic) * cice.taux
    return taux_cice
