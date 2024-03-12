from openfisca_france.model.base import *  # noqa analysis:ignore
from numpy import (
    logical_not as not_,
    maximum as max_,
    )


class contrat_engagement_jeune_montant_forfaitaire(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant maximal de l'allocation Contrat d'Engagement Jeune"
    set_input = set_input_dispatch_by_period
    reference = [
        'https://travail-emploi.gouv.fr/emploi-et-insertion/mesures-jeunes/contrat-engagement-jeune/',
        'https://www.service-public.fr/particuliers/vosdroits/F32700'
        ]

    def formula_2022_03_01(individu, period, parameters):
        parameters_montants = parameters(period).prestations_sociales.education.contrat_engagement_jeune.montants
        majeur = individu('majeur', period)

        tranche = individu.foyer_fiscal('ir_tranche', period.n_2)

        montant_forfaitaire = (
            parameters_montants.montant_mineurs * not_(majeur) * (tranche <= 1)
            + parameters_montants.montant_majeurs_non_imposables * majeur * (tranche == 0)
            + parameters_montants.montant_majeurs_1ere_tranche_ir * majeur * (tranche == 1)
            )

        return montant_forfaitaire


class contrat_engagement_jeune_eligibilite(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité au Contrat d'Engagement Jeune"
    set_input = set_input_dispatch_by_period

    def formula_2022_03_01(individu, period, parameters):
        # En fonction de l'âge
        params_age = parameters(period).prestations_sociales.education.contrat_engagement_jeune.critere_age
        age = individu('age', period)
        handicap = individu('handicap', period)
        eligibilite_age = (params_age.minimum <= age) * ((age <= params_age.maximum) + (age <= (params_age.maximum_handicap) * handicap))

        # En fonction du statut
        activite = individu('activite', period)
        eligibilite_statut = activite != TypesActivite.etudiant

        # En fonction de l'imposition du foyer fiscal
        tranche = individu.foyer_fiscal('ir_tranche', period.n_2)
        eligibilite_ir = (tranche <= 1)

        # En fonction d'autres prestations et dispositifs
        three_previous_months = period.last_3_months
        sans_indemnites_volontariat = individu('indemnites_volontariat', period) == 0
        sans_rsa = individu.famille('rsa', three_previous_months, options = [ADD]) <= 0
        sans_ppa = individu.famille('ppa', three_previous_months, options = [ADD]) <= 0
        eligibilite_autres_dispositifs = sans_rsa * sans_ppa * sans_indemnites_volontariat

        return eligibilite_age * eligibilite_statut * eligibilite_ir * eligibilite_autres_dispositifs


class contrat_engagement_jeune(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period
    label = "Montant du Contrat d'Engagement Jeune"
    reference = ['https://travail-emploi.gouv.fr/emploi-et-insertion/mesures-jeunes/contrat-engagement-jeune/', 'https://www.service-public.fr/particuliers/vosdroits/F32700']

    def formula_2022_03_01(individu, period, parameters):
        three_previous_months = period.last_3_months
        parameters_degressivite = parameters(period).prestations_sociales.education.contrat_engagement_jeune.degressivite

        ressources_totalement_deductibles = [
            'revenus_stage_formation_pro',
            'chomage_net',
            ]

        ressources_partiellement_deductibles_month = [
            'indemnites_chomage_partiel',
            'salaire_net',
            'indemnites_journalieres',
            'remuneration_apprenti',
            ]
        ressources_partiellement_deductibles_year = [
            'revenus_non_salarie_nets',
            ]

        parameters_smic = parameters(period).marche_travail.salaire_minimum.smic
        smic_brut_mensuel = parameters_smic.nb_heures_travail_mensuel * parameters_smic.smic_b_horaire

        # Calcul sur les trois derniers mois (normalement c'est le niveau de ressources moyen le plus faible entre les 3 derniers mois et les 6 derniers mois)
        ressources_mensuelles_individuelles_totalement_deductibles_3_mois = sum(
            individu(ressources_incluses, three_previous_months, options = [ADD]) for ressources_incluses in ressources_totalement_deductibles
            ) / 3
        ressources_mensuelles_individuelles_partiellement_deductibles_3_mois = (
            sum(
                individu(ressources_incluses, three_previous_months, options = [ADD]) for ressources_incluses in ressources_partiellement_deductibles_month
                ) / 3
            + sum(
                individu(ressources_incluses, period.this_year) for ressources_incluses in ressources_partiellement_deductibles_year
                ) / 12
            )

        montant_forfaitaire = individu('contrat_engagement_jeune_montant_forfaitaire', period)
        montant_apres_deduction_totale = max_(montant_forfaitaire - ressources_mensuelles_individuelles_totalement_deductibles_3_mois, 0)
        montant_apres_toutes_deductions = (
            montant_apres_deduction_totale
            - max_(ressources_mensuelles_individuelles_partiellement_deductibles_3_mois - parameters_degressivite.abattement_deductibilite_partielle, 0) * montant_forfaitaire / (parameters_degressivite.part_smic_deductibilite_partielle * smic_brut_mensuel - parameters_degressivite.abattement_deductibilite_partielle)
            )
        montant = max_(montant_apres_toutes_deductions, 0)

        contrat_engagement_jeune_eligibilite = individu('contrat_engagement_jeune_eligibilite', period)

        return montant * contrat_engagement_jeune_eligibilite
