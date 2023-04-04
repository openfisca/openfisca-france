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
        parameters_montants = parameters(period).prestations_sociales.aides_jeunes.contrat_engagement_jeune.montants
        majeur = individu('majeur', period)
        previous_year = period.start.period('year').offset(-1)
        tranche = individu.foyer_fiscal('ir_tranche', previous_year)

        montant_forfaitaire = (
            parameters_montants.montant_mineurs * not_(majeur) * (tranche <= 1)
            + parameters_montants.montant_majeurs_non_imposables * majeur * (tranche == 0)
            + parameters_montants.montant_majeurs_1ere_tranche_ir * majeur * (tranche == 1)
            )
        
        return montant_forfaitaire


class contrat_engagement_jeune_eligbilite_statut(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité en fonction du statut au Contrat d'Engagement Jeune"
    set_input = set_input_dispatch_by_period
    reference = ['https://travail-emploi.gouv.fr/emploi-et-insertion/mesures-jeunes/contrat-engagement-jeune/', 'https://www.service-public.fr/particuliers/vosdroits/F32700']

    def formula_2022_03_01(individu, period):
        activite = individu('activite', period)
        not_in_education = activite != TypesActivite.etudiant
        return not_in_education


class contrat_engagement_jeune_eligibilite_age(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité en fonction de l'âge au Contrat d'Engagement Jeune"
    set_input = set_input_dispatch_by_period

    def formula_2022_03_01(individu, period, parameters):
        params_age = parameters(period).prestations_sociales.aides_jeunes.contrat_engagement_jeune.critere_age
        age = individu('age', period)
        handicap = individu('handicap', period)

        return (params_age.minimum <= age) * ((age <= params_age.maximum) + (age <= (params_age.maximum_handicap) * handicap))


class contrat_engagement_jeune(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period
    label = "Montant du Contrat d'Engagement Jeune"
    reference = ['https://travail-emploi.gouv.fr/emploi-et-insertion/mesures-jeunes/contrat-engagement-jeune/', 'https://www.service-public.fr/particuliers/vosdroits/F32700']

    def formula_2022_03_01(individu, period, parameters):
        three_previous_months = period.last_3_months
        parameters_degressivite = parameters(period).prestations_sociales.aides_jeunes.contrat_engagement_jeune.degressivite

        ressources_individuelles_totalement_deductibles = [
            'revenus_stage_formation_pro',
            'chomage_net',
            ]
        
        ressources_individuelles_partiellement_deductibles = [
            'indemnites_chomage_partiel',
            'salaire_net',
            'rpns_imposables',
            'csg_imposable_non_salarie',
            'crds_non_salarie',
            'indemnites_journalieres',
            'remuneration_apprenti',
            ]
        
        parameters_smic = parameters.marche_travail.salaire_minimum.smic
        smic_brut_mensuel = parameters_smic.nb_heures_travail_mensuel * parameters_smic.smic_b_horaire

        # Calcul sur les trois derniers mois (normalement c'est le niveau de ressources moyen le plus faible entre les 3 derniers mois et les 6 derniers mois)
        ressources_mensuelles_individuelles_totalement_deductibles_3_mois = sum(
            individu(ressources_incluses, three_previous_months, options = [ADD]) for ressources_incluses in ressources_individuelles_totalement_deductibles
            ) / 3
        ressources_mensuelles_individuelles_partiellement_deductibles_3_mois = sum(
            individu(ressources_incluses, three_previous_months, options = [ADD]) for ressources_incluses in ressources_individuelles_partiellement_deductibles
            ) / 3
        
        montant_forfaitaire = individu('contrat_engagement_jeune_montant_forfaitaire', period)
        montant_apres_deduction_totale = max_(montant_forfaitaire - ressources_mensuelles_individuelles_totalement_deductibles_3_mois, 0)
        montant = (
            montant_apres_deduction_totale
            - max_(ressources_mensuelles_individuelles_partiellement_deductibles_3_mois - parameters_degressivite.abattement_deductibilite_partielle, 0) * montant_forfaitaire / (parameters_degressivite.part_smic_deductibilite_partielle * smic_brut_mensuel - parameters_degressivite.abattement_deductibilite_partielle)
            )

        sans_indemnites_volontariat = individu('indemnites_volontariat', period) == 0
        sans_rsa = individu.famille('rsa', three_previous_months, options = [ADD]) <= 0
        sans_ppa = individu.famille('ppa', three_previous_months, options = [ADD]) <= 0

        statut = individu('contrat_engagement_jeune_eligbilite_statut', period)
        eligibilite_age = individu('contrat_engagement_jeune_eligibilite_age', period)

        previous_year = period.start.period('year').offset(-1)
        tranche = individu.foyer_fiscal('ir_tranche', previous_year) <= 1
        return montant * sans_rsa * sans_ppa * sans_indemnites_volontariat * tranche * statut * eligibilite_age
