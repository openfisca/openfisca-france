from numpy import datetime64
from functools import partial
from numpy import busday_count as original_busday_count, datetime64, timedelta64
from openfisca_france.model.base import *
from openfisca_core.periods import Instant


class chomeur_longue_duree(Variable):
    cerfa_field = {
        0: "1AI",
        1: "1BI",
        2: "1CI",
        3: "1DI",
        4: "1EI",
        }
    value_type = bool
    entity = Individu
    label = "Demandeur d'emploi inscrit depuis plus d'un an"
    definition_period = YEAR
    # Pour toutes les variables de ce type, les pac3 ne sont plus proposés après 2007


class chomage_brut(Variable):
    value_type = float
    entity = Individu
    label = "Chômage brut"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula(individu, period):
        return individu('are', period)


class indemnites_chomage_partiel(Variable):
    value_type = float
    entity = Individu
    label = "Indemnités de chômage partiel"
    definition_period = MONTH
    set_input = set_input_divide_by_period

class chomeur_au_sens_du_BIT(Variable):
    value_type = bool
    entity = Individu
    label = "Demandeur d'emploi inscrit depuis plus d'un an"
    definition_period = MONTH
    reference = [
        "INSEE - Chômeur au sens du BIT",
        "https://www.insee.fr/fr/metadonnees/definition/c1129",
        ]

    def formula(individu,period):
        # être sans emploi durant une semaine donnée
        salaire_de_base = individu('salaire_de_base', period)
        condition_salaire = (salaire_de_base == 0)
        # être disponible pour travailler dans les deux semaines à venir
        # avoir effectué, au cours des quatre dernières semaines, une démarche active de recherche d’emploi ou a trouvé un emploi qui commence dans les trois mois.
        # Critère de l'âge: être âgé de 15 ans ou plus
        age = individu('age', period)
        condition_age = age >= 15

        return condition_age * condition_salaire


class jours_travailles_chomage(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours travaillés pris en compte dans le calcul du salaire de référence journalier (5 au maximum par semaine civile)"
    definition_period = MONTH
    default_value = 21.75

    def formula(individu, period) :
      contrat_de_travail_debut = individu('contrat_de_travail_debut', period)
      contrat_de_travail_fin = individu('contrat_de_travail_fin', period)
      busday_count = partial(original_busday_count, weekmask = "1111100")
      debut_mois = datetime64(period.start.offset('first-of', 'month'))
      fin_mois = datetime64(period.start.offset('last-of', 'month'))
      jours_travailles = max_(
        busday_count(
            max_(contrat_de_travail_debut, debut_mois),
            min_(contrat_de_travail_fin, fin_mois) + timedelta64(1, 'D')
            ),
        0,
        )
      return jours_travailles


class salaire_de_reference(Variable):
    value_type = float
    entity = Individu
    label = "Salaire de référence (SR)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        salaire_de_reference = individu.empty_array()
        for months in range(0, 48):
            contrat_de_travail_fin_potentiel = period.offset(-months)
            salaire_de_reference = where(
                individu('contrat_de_travail_fin', period) == datetime64(contrat_de_travail_fin_potentiel.start),
                individu(
                    'salaire_de_base',
                    contrat_de_travail_fin_potentiel.offset(-12).start.period('month', 12),
                    options = [ADD],
                    ),
                salaire_de_reference,
                )
        return salaire_de_reference


class nombre_jours_travailles_12_derniers_mois(Variable):
    value_type = float
    entity = Individu
    label = "Jours travaillés sur les 12 derniers mois avant la rupture de contrat"
    definition_period = MONTH

    def formula(individu, period):
        nombre_jours_travailles_chomage = individu.empty_array()
        for months in range(0, 48):
            contrat_de_travail_fin_potentiel = period.offset(-months)
            nombre_jours_travailles_chomage = where(
                individu('contrat_de_travail_fin', period) == datetime64(contrat_de_travail_fin_potentiel.start),
                individu(
                    'jours_travailles_chomage',
                    contrat_de_travail_fin_potentiel.offset(-12).start.period('month', 12),
                    options = [ADD],
                    ),
                nombre_jours_travailles_chomage,
                )
        return nombre_jours_travailles_chomage



class salaire_de_reference_mensuel(Variable):
    value_type = float
    entity = Individu
    label = "Salaire de référence mensuel (SRM)"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        nombre_jours_travailles_12_derniers_mois = individu('nombre_jours_travailles_12_derniers_mois', period)
        salaire_de_reference = individu('salaire_de_reference', period)
        salaire_de_reference_mensuel = where(
            nombre_jours_travailles_12_derniers_mois > 0,
            (
                30
                * salaire_de_reference
                / (nombre_jours_travailles_12_derniers_mois * 1.4)
                ),
            0
            )
        return salaire_de_reference_mensuel


class are(Variable):
    value_type = float
    entity = Individu
    label = "Allocation chômage d'aide au retour à l'emploi (ARE)"
    definition_period = MONTH

    def formula(individu, period, parameters):
        are_eligibilite_individu = individu('are_eligibilite_individu', period)
        salaire_de_reference_mensuel = individu('salaire_de_reference_mensuel', period)
        duree_versement_are = individu('duree_versement_are', period.offset(-1))
        duree_maximale_versement_are = individu('duree_maximale_versement_are', period)

        are = parameters(period).are
        montant_mensuel = max_(
            are.are_partie_fixe * 30 + are.pourcentage_du_sjr_complement * salaire_de_reference_mensuel,
            are.pourcentage_du_sjr_seul * salaire_de_reference_mensuel
            )
        montant_plancher = max_(
            are.are_min * 30,
            montant_mensuel
            )
        montant_plafond = min_(
            montant_plancher,
            are.max_en_pourcentage_sjr * salaire_de_reference_mensuel
            )

        busday_count = partial(original_busday_count, weekmask = "1111100")

        return (
            montant_plafond
            * are_eligibilite_individu
            * min_(
                1,
                max_(
                    0,
                    (duree_maximale_versement_are - (duree_versement_are))
                    ) / 30
                )
            )


class are_eligibilite_individu(Variable):
    value_type = bool
    label = "Éligibilité individuelle à l'ARE"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = [
        "Unédic - Règlement général annexé à la convention du 6 mai 2011",
        "https://www.unedic.org/sites/default/files/regulations/RglACh11.pdf",
        ]

    def formula_2017_11(individu, period, parameters):
        # il faut résider en France, être involontairement privé d'emploi, être inscrit comme demandeur d'emploi,
        # être à la recherche active et permanente d'un emploi,
        # être physiquement apte à l'exercice d'un emploi.
        # Critère de l'âge: ARE non versé si l'âge de départ à la retraite atteint, sauf en cas de taux plein non atteint.
        # Pour simplifier, on stipule qu'on ne peut plus toucher d'ARE dès lors l'âge légal de départ à la retraite atteint.
        are = parameters(period).are
        age = individu('age', period)
        condition_age = age < are.age_legal_retraite

        # Critère d'affiliation : avoir travaillé un certain nombre de jours
        # dans les derniers mois avant la date de fin de contrat.
        # Le nombre de mois diffère selon qu'on ait plus ou moins de 53 ans.
        periode_affiliation = individu('nombre_jours_travailles_dans_les_x_derniers_mois', period)
        condition_affiliation = select(
            [
                age < 53,
                age >= 53
                ],
            [
                periode_affiliation >= are.periode_minimale_affiliation_moins_53_ans,
                periode_affiliation >= are.periode_minimale_affiliation_53_ans_et_plus
                ],
            )
        return condition_age * condition_affiliation


class nombre_jours_travailles_dans_les_x_derniers_mois(Variable):
    value_type = float
    entity = Individu
    label = "Nombre de jours travaillés sur les x derniers mois avant la rupture de contrat pour les moins de 53 ans"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula_2017_11(individu, period, parameters):
        are = parameters(period).are
        age = individu('age', period)
        # Moins de 53 ans
        periode_reference_moins_53 = are.periode_de_reference_affiliation_moins_53_ans
        nombre_jours_travailles_reference_moins_53 = individu.empty_array()
        for months in range(0, 48):
            contrat_de_travail_fin_potentiel = period.offset(-months)
            nombre_jours_travailles_reference_moins_53 = where(
                individu('contrat_de_travail_fin', period) == datetime64(contrat_de_travail_fin_potentiel.start),
                individu(
                    'jours_travailles_chomage',
                    contrat_de_travail_fin_potentiel.offset(-periode_reference_moins_53).start.period('month', periode_reference_moins_53),
                    options = [ADD],
                    ),
                nombre_jours_travailles_reference_moins_53,
                )
        # Plus de 53 ans
        nombre_jours_travailles_reference_plus_53 = individu.empty_array()
        periode_reference_plus_53 = are.periode_de_reference_affiliation_53_ans_et_plus
        for months in range(0, 72):
            contrat_de_travail_fin_potentiel = period.offset(-months)
            nombre_jours_travailles_reference_plus_53 = where(
                individu('contrat_de_travail_fin', period) == datetime64(contrat_de_travail_fin_potentiel.start),
                individu(
                    'jours_travailles_chomage',
                    contrat_de_travail_fin_potentiel.offset(-periode_reference_plus_53).start.period('month', periode_reference_plus_53),
                    options = [ADD],
                    ),
                nombre_jours_travailles_reference_plus_53,
                )

        nombre_jours_travailles_reference = select(
            [age < 53, age >= 53],
            [nombre_jours_travailles_reference_moins_53, nombre_jours_travailles_reference_plus_53],
            )
        return nombre_jours_travailles_reference


class duree_versement_are(Variable):
    value_type = int
    entity = Individu
    label = "Nombre  de jours indemnisés par l'ARE"
    definition_period = MONTH

    def formula(individu, period):
        are = individu('are', period)
        duree_versement_are = individu('duree_versement_are', period.offset(-1))
        busday_count = partial(original_busday_count, weekmask = "1" * 7)
        duree_versement_are = (
            duree_versement_are
            + (
                (are > 0)
                * busday_count(
                   datetime64(period.start),
                    datetime64(period.offset(1).start)
                    )
                )
            )
        return duree_versement_are

class duree_maximale_versement_are(Variable):
    value_type = int
    entity = Individu
    label = "Nombre maximal de jours indemnisés par l'ARE"
    definition_period = MONTH

    def formula(individu, period):
        age = individu('age', period)
        nombre_jours_travailles_dans_la_periode_reference_affiliation = individu('nombre_jours_travailles_dans_les_x_derniers_mois', period)
        nombre_jours_indemnises = nombre_jours_travailles_dans_la_periode_reference_affiliation * 1.4

        return select(
            [age < 53, 53 <= age <= 54, age >= 55],
            [min_(nombre_jours_indemnises, 730), min_(nombre_jours_indemnises, 913), min_(nombre_jours_indemnises, 1095)],
            )


class eligibilite_cumul_are_salaire(Variable):
    value_type = bool
    entity = Individu
    label = "Eligibilité de l'individu au cumul des allocations de chômage et de la rémunération provenant d'une activité professionnelle"
    definition_period = MONTH

    def formula(individu, period):
        cumul_are_salaire = individu('cumul_are_salaire', period)
        salaire_de_reference_mensuel = individu('salaire_de_reference_mensuel', period)

        condition_cumul = cumul_are_salaire <= salaire_de_reference_mensuel

        return condition_cumul

class cumul_are_salaire(Variable):
    value_type = float
    entity = Individu
    label = "Revenus totaux d'un individu cumulant ARE et revenus issus d'une activité professionnelle"
    definition_period = MONTH

    def formula(individu, period):
        are_activite_reduite = individu('are_activite_reduite', period)
        salaire_de_base = individu('salaire_de_base', period)

        return are + salaire_de_base

class are_activite_reduite(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'allocation chomage lorqu'un individu exerce une activité réduite (à faibles revenus professionels"
    definition_period = MONTH

    def formula(individu, period):
        salaire_de_base = individu('salaire_de_base', period)
        are = individu('are', period)
        eligibilite_cumul_are_salaire = individu('eligibilite_cumul_are_salaire', period)
        are_eligibilite_individu = individu('are_eligibilite_individu', period)
        nombre_jours_indemnisables_are = (are - 0.7 * salaire_de_base) / (are / 30)

        return nombre_jours_indemnisables_are * are * eligibilite_cumul_are_salaire * are_eligibilite_individu

class are_nette(Variable):
    value_type = float
    entity = Individu
    label = "Allocation de retour à l'emploi nette déduite des retenues sociales"
    definition_period = MONTH

    def formula(individu, period, parameters):
        chomage_net = individu('chomage_net', period)
        retraite_complementaire_chomage = individu('retraite_complementaire_chomage', period)

        return chomage_net - retraite_complementaire_chomage


class retraite_complementaire_chomage(Variable):
    value_type = float
    entity = Individu
    label = "Retenue sociale de la retraite complémentaire sur l'allocation chômage"
    definition_period = MONTH

    def formula(individu, period, parameters):
        salaire_de_reference_mensuel = individu('salaire_de_reference_mensuel', period)
        seuil_exoneration_retraite_complementaire = parameters(period).are.are_min
        are = individu('are', period)


        montant_retenue_retraite_complementaire = select(
            [are > (seuil_exoneration_retraite_complementaire * 30), are <= (seuil_exoneration_retraite_complementaire * 30)],
            [(0.03 * salaire_de_reference_mensuel) , 0],
            )

        return montant_retenue_retraite_complementaire

class participation_tax_rate(Variable):
    value_type = float
    entity = Individu
    label = "Participation Tax Rate (PTR)"
    definition_period = MONTH

    def formula(individu, period):
        revenu_disponible_emploi = menage('revenu_disponible', period, options = [DIVIDE])
        revenu_disponible_chomage = menage('revenu_disponible', period, options = [DIVIDE])
        salaire_de_base = individu('salaire_de_base', period)

        revenus_disponible_statut = select(
            [chomeur_au_sens_du_BIT, are <= not_(chomeur_au_sens_du_BIT)],
            [revenu_disponible_chomage , revenu_disponible_emploi],
            )

        return (1 - ((revenu_disponible_emploi - revenu_disponible_chomage) / salaire_de_base))
