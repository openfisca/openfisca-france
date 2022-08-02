from openfisca_france.model.base import *  # noqa analysis:ignore


class garantie_jeunes_neet(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = 'Variable NEET - Ni étudiant, ni employé, ni stagiaire'
    set_input = set_input_divide_by_period
    reference = ['https://fr.wikipedia.org/wiki/NEET']

    def formula_2017_01_01(individu, period):
        not_in_employment = individu('salaire_net', period) == 0

        activite = individu('activite', period)
        not_in_education = (activite != TypesActivite.etudiant) * (activite != TypesActivite.actif)

        no_indemnites_stage = individu('indemnites_stage', period) == 0
        no_revenus_stage_formation_pro = individu('revenus_stage_formation_pro', period) == 0
        not_in_training = no_indemnites_stage * no_revenus_stage_formation_pro

        return not_in_employment * not_in_education * not_in_training


class garantie_jeunes_montant(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant maximal de l'allocation Garantie Jeune"
    set_input = set_input_dispatch_by_period
    reference = [
        'https://travail-emploi.gouv.fr/emploi/mesures-jeunes/garantiejeunes/',
        'https://www.service-public.fr/particuliers/vosdroits/F32700'
        ]

    def formula_2017_01_01(individu, period, parameters):
        params = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.rsa
        montant_base = params.rsa_m.montant_de_base_du_rsa
        taux_1_personne = params.rsa_fl.forfait_logement.taux_1_personne
        garantie_jeunes_max = montant_base * (1 - taux_1_personne)
        salaire_minimum = parameters(period).marche_travail.salaire_minimum
        smic_mensuel_brut = salaire_minimum.smic.smic_b_horaire * salaire_minimum.smic.nb_heures_travail_mensuel

        degressivite = parameters(period).prestations_sociales.aides_jeunes.garantie_jeunes.degressivite
        plafond = degressivite.plafond * smic_mensuel_brut
        seuil_degressivite = degressivite.seuil

        types_revenus_activites = [
            'revenus_stage_formation_pro',
            'indemnites_journalieres',
            'chomage_net',
            'indemnites_volontariat',
            'asi',
            'pensions_alimentaires_percues',
            'rente_accident_travail',
            'stage_gratification',
            'bourse_enseignement_sup',
            'salaire_net',
            'bourse_recherche',
            'rpns_auto_entrepreneur_benefice',
            ]

        base_ressource = (
            sum(individu(type_revenu, period) for type_revenu in types_revenus_activites)
            )
        return garantie_jeunes_max * min_(1, max_(0, (base_ressource - plafond) / (seuil_degressivite - plafond)))


class garantie_jeunes_eligibilite_age(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité en fonction de l'âge à la Garantie Jeune"
    set_input = set_input_dispatch_by_period

    def formula_2017_01_01(individu, period, parameters):
        params_age = parameters(period).prestations_sociales.aides_jeunes.garantie_jeunes.critere_age
        age = individu('age', period)

        return (params_age.minimum <= age) * (age <= params_age.maximum)


class garantie_jeunes_eligibilite_ressources(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = 'Éligibilité en fonction du niveau de ressources à la Garantie Jeune'
    set_input = set_input_dispatch_by_period

    def formula_2017_01_01(individu, period, parameters):
        three_previous_months = period.last_3_months
        params = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.rsa
        montant_base = params.rsa_m.montant_de_base_du_rsa
        taux_1_personne = params.rsa_fl.forfait_logement.taux_1_personne
        plafond_condition_ressources = montant_base * (1 - taux_1_personne)

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
            'chomage_net',  # A éclaircir : cette ressource n'est pas mentionné dans la liste des ressources figurant dans la loi, mais plusieurs sites mentionnent leur prise en compte (dont service-public.fr, site de pole emploi)
            ]

        # Calcul sur les trois derniers mois (normalement c'est le niveau de ressources moyen le plus faible entre les 3 derniers mois et les 6 derniers mois)
        niveau_ressources_individuelles_3_mois = sum(
            individu(ressources_incluses, three_previous_months, options = [ADD]) for ressources_incluses in ressources_individuelles
            )

        rsa = individu.famille('rsa', three_previous_months, options = [ADD])
        ppa = individu.famille('ppa', three_previous_months, options = [ADD])
        rsa_ppa_demandeurs = (
            (rsa + ppa)
            * (individu.has_role(Famille.DEMANDEUR) + individu.has_role(Famille.CONJOINT))
            )

        niveau_ressources = (niveau_ressources_individuelles_3_mois + rsa_ppa_demandeurs) / 3

        return (niveau_ressources <= plafond_condition_ressources)


class garantie_jeunes(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period
    label = 'Montant de la Garantie Jeune'
    reference = ['https://travail-emploi.gouv.fr/emploi/mesures-jeunes/garantiejeunes/', 'https://www.service-public.fr/particuliers/vosdroits/F32700']
    end = '2022-02-28'

    def formula_2017_01_01(individu, period, parameters):
        montant = individu('garantie_jeunes_montant', period)
        neet = individu('garantie_jeunes_neet', period)
        age_ok = individu('garantie_jeunes_eligibilite_age', period)
        garantie_jeunes_eligibilite_ressources = individu('garantie_jeunes_eligibilite_ressources', period)
        return montant * neet * age_ok * garantie_jeunes_eligibilite_ressources
