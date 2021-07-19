from openfisca_france.model.base import *  # noqa analysis:ignore


class garantie_jeunes_neet(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Variable NEET - Ni étudiant, ni employé, ni stagiaire"
    reference = ['https://fr.wikipedia.org/wiki/NEET']

    def formula(individu, period):
        not_in_employment = individu('salaire_net', period) == 0

        activite = individu('activite', period)
        not_in_education = (activite != TypesActivite.etudiant) * (activite != TypesActivite.actif)

        no_indemnites_stage = individu('indemnites_stage', period) == 0
        no_revenus_stage_formation_pro = individu('revenus_stage_formation_pro', period) == 0
        not_in_training = no_indemnites_stage * no_revenus_stage_formation_pro

        return not_in_employment * not_in_education * not_in_training


class garantie_jeunes_max(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant maximal de l'allocation Garantie Jeune"
    reference = [
        "Article D5131-20 du code du travail",
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=DED54A598193DDE1DF59E0AE16BDE87D.tplgfr21s_3?idArticle=LEGIARTI000033709227&cidTexte=LEGITEXT000006072050",
        ]

    def formula(individu, period, parameters):
        params = parameters(period).prestations.minima_sociaux.rsa
        montant_base = params.montant_de_base_du_rsa
        taux_1_personne = params.forfait_logement.taux_1_personne
        return montant_base * (1 - taux_1_personne)


class garantie_jeunes_montant(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant maximal de l'allocation Garantie Jeune"
    reference = [
        "https://travail-emploi.gouv.fr/emploi/mesures-jeunes/garantiejeunes/",
        "https://www.service-public.fr/particuliers/vosdroits/F32700"
        ]

    def formula(individu, period, parameters):
        garantie_jeunes_max = individu("garantie_jeunes_max", period)

        cotsoc = parameters(period).cotsoc
        smic_mensuel_brut = cotsoc.gen.smic_h_b * cotsoc.gen.nb_heure_travail_mensuel

        degressivite = parameters(period).prestations.garantie_jeunes.degressivite
        plafond = degressivite.plafond_en_pourcentage_du_smic_brut * smic_mensuel_brut
        seuil_degressivite = degressivite.seuil

        types_revenus_activites = [
            'revenus_stage_formation_pro',
            'indemnites_journalieres',
            "rsa_revenu_activite_individu",
            'chomage_net',
            'indemnites_volontariat',
            'asi',
            'pensions_alimentaires_percues',
            'rente_accident_travail',
            'stage_gratification',
            'bourse_enseignement_sup',
            'salaire_net',
            ]

        base_ressource = (
            sum(individu(type_revenu, period) for type_revenu in types_revenus_activites))
        return garantie_jeunes_max * min_(1, max_(0, (base_ressource - plafond) / (seuil_degressivite - plafond)))


class garantie_jeunes_eligibilite_age(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Éligibilité en fonction de l'âge à la Garantie Jeune"

    def formula(individu, period, parameters):
        params_age = parameters(period).prestations.garantie_jeunes.critere_age.age
        age = individu('age', period)

        return (params_age.minimum <= age) * (age <= params_age.maximum)


class garantie_jeunes(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Montant de la Garantie Jeune"
    reference = ["https://travail-emploi.gouv.fr/emploi/mesures-jeunes/garantiejeunes/", "https://www.service-public.fr/particuliers/vosdroits/F32700"]

    def formula(individu, period, parameters):
        montant = individu('garantie_jeunes_montant', period)
        neet = individu('garantie_jeunes_neet', period)
        age_ok = individu('garantie_jeunes_eligibilite_age', period)
        return montant * neet * age_ok
