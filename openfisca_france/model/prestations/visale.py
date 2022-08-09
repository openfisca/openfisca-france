from openfisca_france.model.base import *
from numpy import datetime64


class visale_eligibilite(Variable):
    value_type = bool
    entity = Menage
    label = "Indique l'éligibilité à une caution Visale"
    definition_period = MONTH
    reference = 'https://www.visale.fr/vos-questions/faq-locataires/locataire-de-30-ans-ou-moins-suis-je-eligible/'

    # L'extension à toutes les personnes de moins de 30 ans sauf les étudiants boursiers encore rattachés au foyer fiscal de leurs parents a été faite en septembre 2016 : https://www.lemonde.fr/immobilier/article/2016/08/04/location-la-caution-visale-etendue-aux-moins-de-30-ans-au-plus-tard-le-30-septembre_4978567_1306281.html
    # L'extension à toutes les personnes de moins de 30 ans y compris les étudiants boursiers encore rattachés au foyer fiscal de leurs parents a été faite le 19 juin 2018.
    def formula_2018_06_19(menage, period, parameters):
        '''
        Le cas où un ménage est constitué d'une personne éligible et l'autre non éligible n'est pas spécifié dans la documentation Visale, on va donc tester l'égibilité uniquement sur la personne de référence.
        La documentation Visale indique : « Si vous êtes 2 à rechercher un logement et un garant, votre demande Visale doit être réalisée conjointement. Pour les logements en colocation, au-delà de 2 colocataires, un bail et un visa individuels doivent être faits par colocataire. »
        Cette modélisation est impossible à réaliser telle quelle dans OpenFisca, car cela correspondrait à une variable de Ménage pour 1 à 2 personnes, et une variable d'Individu à partir de 3 personnes en colocation, mais pour lesquelles le montant du loyer serait différent (ou en tous cas, serait la quote-part du loyer total du logement loué).
        Par conséquent, le calcul de cette variable fait l'hypothèse d'une déclaration des Ménages avec un Ménage par personne inscrite sur le bail pour 3 personnes ou plus, et avec un seul Ménage pour une colocation (ou un bail solidaire) de 2 personnes.
        '''
        age = menage.personne_de_reference('age', period)
        majeur = menage.personne_de_reference('majeur', period)

        eligibilite_age = majeur * (age <= parameters(period).prestations_sociales.aides_logement.action_logement.visale.eligibilite.age_max)

        etudiant = menage.personne_de_reference('etudiant', period)
        ressortissant_eee = menage.personne_de_reference('ressortissant_eee', period)
        nationalite = menage.personne_de_reference('nationalite', period)
        ressortissant_pays_eligible = sum([nationalite == str.encode(etat) for etat in parameters(period).prestations_sociales.aides_logement.action_logement.visale.eligibilite.residence_hors_eee])  # TOOPTIMIZE: string encoding into bytes array should be done at load time

        eligibilite_nationalite = ressortissant_eee + ressortissant_pays_eligible + etudiant  # Sont éligibles les « étudiant‧e‧s hors Union Européenne justifiant d’un visa long séjour valant titre de séjour mention étudiant ou passeport talent en cours de validité, ou d’un titre de séjour mention étudiant en cours de validité ». Vu qu'il s'agit d'une aide au logement, on suppose que le visa long séjour (4 mois à 1 an) est acquis, et on ignore donc les cas où un étudiant hors UE vient pour une durée de moins de 4 mois sans visa (ex : étudiante néo-zélandaise en visa touristique de 90 jours, l'éligibilité à Visale sera indiquée à tort comme positive).

        loyer = menage('loyer', period)
        charges_locatives = menage('charges_locatives', period)
        montant_max = menage('visale_montant_max', period)

        eligibilite_loyer = (loyer + charges_locatives) <= montant_max
        eligibilite_date_entree_logement = menage('date_entree_logement', period) > datetime64(period.start)

        return eligibilite_age * eligibilite_nationalite * eligibilite_loyer * eligibilite_date_entree_logement


class visale_montant_max(Variable):
    value_type = float
    entity = Menage
    label = 'Montant maximum du loyer éligible à une caution Visale'
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.visale.fr/vos-questions/faq-locataires/locataire-de-30-ans-ou-moins-suis-je-eligible/#13'

    def formula_2016_01_01(menage, period, parameters):
        '''
        Attention, un montant non nul pour cette variable ne signifie pas nécessairement que l'entité est éligible à Visale : d'autres conditions peuvent ne pas être remplies. Pour déterminer l'éligibilité à la caution Visale au loyer actuellement renseigné pour le ménage, il faut utiliser la variable `visale_eligibilite`.
        La documentation Visale indique : « Si vous êtes 2 à rechercher un logement et un garant, votre demande Visale doit être réalisée conjointement. Pour les logements en colocation, au-delà de 2 colocataires, un bail et un visa individuels doivent être faits par colocataire. »
        Cette modélisation est impossible à réaliser telle quelle dans OpenFisca, car cela correspondrait à une variable de Ménage pour 1 à 2 personnes, et une variable d'Individu à partir de 3 personnes en colocation, mais pour lesquelles le montant du loyer serait différent (ou en tous cas, serait la quote-part du loyer total du logement loué).
        Par conséquent, le calcul de cette variable fait l'hypothèse d'une déclaration des Ménages avec un Ménage par personne inscrite sur le bail pour 3 personnes ou plus, et avec un seul Ménage pour une colocation (ou un bail solidaire) de 2 personnes.
        '''
        residence_ile_de_france = menage('residence_ile_de_france', period)

        etudiant = menage.personne_de_reference('etudiant', period)  # le cas où un ménage est constitué d'une personne étudiante et d'une personne non étudiante n'est pas spécifié dans la documentation Visale
        minimum_etudiant = where(
            residence_ile_de_france,
            parameters(period).prestations_sociales.aides_logement.action_logement.visale.plafond_loyer.etudiant.ile_de_france,
            parameters(period).prestations_sociales.aides_logement.action_logement.visale.plafond_loyer.etudiant.hors_ile_de_france,
            )

        plafond_loyer = where(
            residence_ile_de_france,
            parameters(period).prestations_sociales.aides_logement.action_logement.visale.plafond_loyer.cas_general.ile_de_france,
            parameters(period).prestations_sociales.aides_logement.action_logement.visale.plafond_loyer.cas_general.hors_ile_de_france,
            )

        moitie_des_ressources = menage('visale_base_ressources', period) / 2

        return max_(etudiant * minimum_etudiant, min_(moitie_des_ressources, plafond_loyer))


class visale_base_ressources(Variable):
    value_type = float
    entity = Menage
    label = "Revenus pris en compte pour l'éligibilité à la caution Visale"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.visale.fr/wp-content/uploads/2020/04/Visale-Ressources-Locataire_2020.pdf#page_7'

    def formula_2016_01_01(menage, period, parameters):
        '''
        La documentation Visale indique : « Si vous êtes 2 à rechercher un logement et un garant, votre demande Visale doit être réalisée conjointement. Pour les logements en colocation, au-delà de 2 colocataires, un bail et un visa individuels doivent être faits par colocataire. »
        Cette modélisation est impossible à réaliser telle quelle dans OpenFisca, car cela correspondrait à une variable de Ménage pour 1 à 2 personnes, et une variable d'Individu à partir de 3 personnes en colocation, mais pour lesquelles le montant du loyer serait différent (ou en tous cas, serait la quote-part du loyer total du logement loué).
        Par conséquent, le calcul de cette variable fait l'hypothèse d'une déclaration des Ménages avec un Ménage par personne inscrite sur le bail pour 3 personnes ou plus, et avec un seul Ménage pour une colocation (ou un bail solidaire) de 2 personnes.
        '''
        revenus_individus = menage.sum(menage.members('visale_base_ressources_individuelle', period))

        ressources_foyer_fiscal = [
            'rente_viagere_titre_onereux',
            ]

        ressources_famille = [
            'aeeh',
            'af',
            'asf',
            'aspa',
            'cf',
            'ppa',
            'rsa',
            ]

        ressources_famille_abattues = [  # ressources de la famille à prendre en compte à 67% sur la base du loyer du logement pour lequel Visale est demandé
            'alf',
            'als',
            'apl',
            ]

        revenus_foyers_fiscaux = sum(
            menage.sum(menage.members.foyer_fiscal(ressource, period.last_month), role = FoyerFiscal.DECLARANT_PRINCIPAL)
            for ressource in ressources_foyer_fiscal
            )

        revenus_familles = sum(
            menage.sum(menage.members.famille(ressource, period.last_month), role = Famille.DEMANDEUR)
            for ressource in ressources_famille
            )

        revenus_familles_abattus = sum(
            menage.sum(menage.members.famille(ressource, period), role = Famille.DEMANDEUR)
            for ressource in ressources_famille_abattues
            ) * parameters(period).prestations_sociales.aides_logement.action_logement.visale.quote_part_aides_logement

        return revenus_individus + revenus_foyers_fiscaux + revenus_familles + revenus_familles_abattus


class visale_base_ressources_individuelle(Variable):
    value_type = float
    entity = Individu
    label = "Revenus des individus pris en compte pour l'éligibilité à la caution Visale"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = 'https://www.visale.fr/wp-content/uploads/2020/04/Visale-Ressources-Locataire_2020.pdf#page_7'

    def formula_2016_01_01(individu, period, parameters):
        ressources_individu_mensuelles = [
            'salaire_net',
            'primes_salaires_non_exonerees',  # Sont prises en compte toutes les « primes récurrentes perçues dans le cadre d’une activité intégrée dans le calcul du salaire ou traitement ». Note : ce revenu est brut, il devrait être net.
            'prime_forfaitaire_mensuelle_reprise_activite',
            'revenus_stage_formation_pro',
            'remuneration_apprenti',
            'garantie_jeunes',
            'bourse_enseignement_sup',
            'bourse_recherche',
            'rpns_auto_entrepreneur_benefice',
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

        revenus_individu = sum(individu(ressource, period.last_month) for ressource in ressources_individu_mensuelles)  # les justificatifs des ressources sont demandés « sur le mois précédant la demande de visa »

        ressources_individu_annuelles = [
            'rpns_imposables',
            'csg_imposable_non_salarie',
            'crds_non_salarie',
            ]

        revenus_non_salarie = sum(individu(ressource, period.last_year.first_month, options = [DIVIDE]) for ressource in ressources_individu_annuelles)

        return revenus_individu + revenus_non_salarie
