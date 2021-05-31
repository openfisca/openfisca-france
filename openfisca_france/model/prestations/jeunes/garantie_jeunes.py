from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.model.prestations.education import TypesScolarite


class garantie_jeunes_neet(Variable):
    value_type = bool
    entity = Individu
    definition_period = MONTH
    label = "Variable NEET - Ni étudiant, ni employé, ni stagiaire"
    reference = ['https://fr.wikipedia.org/wiki/NEET']

    def formula(individu, period):
        not_in_employment = individu('salaire_net', period) == 0

        scolarite = individu('scolarite', period)
        activite = individu('activite', period)
        not_in_education = (scolarite == TypesScolarite.inconnue) * (activite != TypesActivite.etudiant)

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
        "https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=DED54A598193DDE1DF59E0AE16BDE87D.tplgfr21s_3?idArticle=LEGIARTI000033709227&cidTexte=LEGITEXT000006072050"    
        "https://travail-emploi.gouv.fr/emploi/mesures-jeunes/garantiejeunes/",
        "https://www.service-public.fr/particuliers/vosdroits/F32700"
    ]

    def formula(individu, period, parameters):
        """
       SMIC : désigne le montant du SMIC en net
       rev_activites_i : désigne les revenus d'activité de l'individu
       garantie_jeunes_max : désigne le montant de l'allocation maximum
       point_bascule : désigne le point de bascule où le calcul commence à être dégressif
       """
        SMIC = 1243.67
        garantie_jeunes_max = 497.50
        point_bascule = 300
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
            'bourse_enseignement_sup'
        ]
        rev_activites_i = (
            sum(individu(type_revenu, period) for type_revenu in types_revenus_activites))

        # Si les ressources dépassent le plafond du SMIC,
        # l'individu ne peut pas bénéficier de l'aide.
        if rev_activites_i >= SMIC:
            return 0

        # Si les revenus d'activités sont inférieures au montant maximum prévu par la garantie jeune,
        # l'individu bénéficie pleinement de l'aide.
        if rev_activites_i < point_bascule:
            return garantie_jeunes_max


        # Si les revenus 'activités sont supérieures à 300€ et inférieures au SMIC, le calcul
        # de la garantie jeune s'effectue de manière dégressive selon la formule suivante :
        # garantie_jeune = (RevAct - SMIC) x [GJm / (PB - Smic)]
        if rev_activites_i > 300 and rev_activites_i < SMIC:
            return (rev_activites_i - SMIC) * (garantie_jeunes_max / (point_bascule - SMIC))

        return garantie_jeunes_max

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
        montant = individu('garantie_jeunes_max', period)
        neet = individu('garantie_jeunes_neet', period)
        age_ok = individu('garantie_jeunes_eligibilite_age', period)
        return montant  * neet * age_ok
