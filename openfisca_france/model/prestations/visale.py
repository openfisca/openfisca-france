from openfisca_france.model.base import *


class visale_base_ressources(Variable):
    value_type = float
    entity = Menage  # « Si vous êtes 2 à rechercher un logement et un garant, votre demande Visale doit être réalisée conjointement. Pour les logements en colocation, au-delà de 2 colocataires, un bail et un visa individuels doivent être faits par colocataire. »
    label = "Revenus pris en compte pour l'éligibilité à la caution Visale"
    definition_period = MONTH
    reference = 'https://www.visale.fr/wp-content/uploads/2020/04/Visale-Ressources-Locataire_2020.pdf#page_7'

    def formula(menage, period, parameters):
        visale_bases_ressources_individuelles = menage.members('visale_base_ressources_individuelle', period)

        return menage.sum(visale_bases_ressources_individuelles)


class visale_base_ressources_individuelle(Variable):
    value_type = float
    entity = Individu
    label = "Revenus des individus pris en compte pour l'éligibilité à la caution Visale"
    definition_period = MONTH
    reference = 'https://www.visale.fr/wp-content/uploads/2020/04/Visale-Ressources-Locataire_2020.pdf#page_7'

    def formula(individu, period, parameters):

        # TODO: sont demandés les justificatifs des ressources sur le mois précédant la demande de visa

        ressources_individu_mensuelles = [
            'salaire_net',
            'primes_salaires',  # Sont prises en compte toutes les « primes récurrentes perçues dans le cadre d’une activité intégrée dans le calcul du salaire ou traitement ». Note : ce revenu est brut, il devrait être net.
            'prime_forfaitaire_mensuelle_reprise_activite',
            'revenus_stage_formation_pro',
            'remuneration_apprenti',
            'garantie_jeunes',
            'bourse_enseignement_sup',
            'bourse_recherche',
            'tns_auto_entrepreneur_benefice',
            'chomage_net',
            'indemnites_chomage_partiel',  # à inclure dans chomage_net ?
            'ass',
            'retraite_nette',
            'pensions_alimentaires_percues',
            'pensions_invalidite',
            'pch',
            'asi',
            'apa_domicile',
            'indemnites_journalieres',
            'rente_accident_travail',
            # Ressources non prises en compte à ce jour car non modélisées dans OpenFisca :
            # mobili-jeune
            # prime transitoire de solidarité (PTS)
            # allocation journalière de présence parentale (AJPP)
            ]

        ressources_individu_annuelles = [
            'rpns_individu',
            'cotisations_non_salarie',
            'csg_non_salarie',
            'crds_non_salarie',
            ]

        # Ressources de la famille à prendre en compte à 100% :
        # 'aspa',
        # 'ppa',
        # 'rsa',
        # 'af',
        # 'cf',
        # 'aeeh',
        # 'asf',

        # Ressources de la famille à prendre en compte à 67% sur la base du loyer du logement pour lequel Visale est demandé :
        # 'alf'
        # 'als'
        # 'apl'

        # Ressources du foyer fiscal à prendre en compte :
        # foyer_fiscal = individu.foyer_fiscal
        # rente_viagere_titre_onereux = foyer_fiscal('rente_viagere_titre_onereux', period)

        revenus_mensuels = sum(individu(ressource, period) for ressource in ressources_individu_mensuelles)
        revenus_annuels = sum(individu(ressource, period.this_year) for ressource in ressources_individu_annuelles)  # DIVIDE ?

        return revenus_mensuels + (revenus_annuels / 12)
