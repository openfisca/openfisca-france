from openfisca_france.model.base import *  # noqa analysis:ignore


class contrat_engagement_jeune_montant(Variable):
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
        montant = parameters(period).prestations_sociales.aides_jeunes.contrat_engagement_jeune.montants
        montant_degressivite = parameters(period).prestations_sociales.aides_jeunes.contrat_engagement_jeune.degressivite.montant
        age = individu('age', period)
        majeur = individu('majeur', period)
        previous_year = period.start.period('year').offset(-1)
        tranche = individu.foyer_fiscal('ir_tranche', previous_year)

        degressivite = majeur * (tranche > 0) * montant_degressivite
        return montant.calc(age) - degressivite


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


class contrat_engagement_jeune_eligibilite_ressources(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité en fonction du niveau de ressources au Contrat d'Engagement Jeune"
    set_input = set_input_dispatch_by_period

    def formula_2022_03_01(individu, period, parameters):
        three_previous_months = period.last_3_months
        plafond = parameters(period).prestations_sociales.aides_jeunes.contrat_engagement_jeune.plafond
        ressources_individuelles = [
            'revenus_stage_formation_pro',
            'indemnites_chomage_partiel',
            'indemnites_volontariat',
            'asi',
            'pensions_alimentaires_percues',
            'stage_gratification',
            'bourse_enseignement_sup',
            'salaire_net',
            'indemnites_journalieres',
            'prestation_compensatoire',
            'rente_accident_travail',
            'pensions_invalidite',
            'aah',
            'remuneration_apprenti',
            'chomage_net',
            ]

        # Calcul sur les trois derniers mois (normalement c'est le niveau de ressources moyen le plus faible entre les 3 derniers mois et les 6 derniers mois)
        niveau_ressources_individuelles_3_mois = sum(
            individu(ressources_incluses, three_previous_months, options = [ADD]) for ressources_incluses in ressources_individuelles
            )

        sans_rsa = individu.famille('rsa', three_previous_months, options = [ADD]) <= 0
        sans_ppa = individu.famille('ppa', three_previous_months, options = [ADD]) <= 0

        niveau_ressources = (niveau_ressources_individuelles_3_mois) / 3

        previous_year = period.start.period('year').offset(-1)
        tranche = individu.foyer_fiscal('ir_tranche', previous_year) <= 1
        return (niveau_ressources <= plafond) * sans_rsa * sans_ppa * tranche


class contrat_engagement_jeune(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period
    label = "Montant du Contrat d'Engagement Jeune"
    reference = ['https://travail-emploi.gouv.fr/emploi-et-insertion/mesures-jeunes/contrat-engagement-jeune/', 'https://www.service-public.fr/particuliers/vosdroits/F32700']

    def formula_2022_03_01(individu, period, parameters):
        montant = individu('contrat_engagement_jeune_montant', period)
        statut = individu('contrat_engagement_jeune_eligbilite_statut', period)
        eligibilite_age = individu('contrat_engagement_jeune_eligibilite_age', period)
        eligibilite_ressources = individu('contrat_engagement_jeune_eligibilite_ressources', period)
        return montant * statut * eligibilite_age * eligibilite_ressources
