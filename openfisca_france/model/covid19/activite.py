from openfisca_france.model.base import *


class covid_aide_exceptionnelle_tpe_eligible(Variable):
    entity = Individu
    value_type = bool
    label = "Éligibilité à l'aide exceptionnelle pour les TPE pendant la crise sanitaire dûe au COVID-19"
    reference = [
        "Décret n°2020-371 du 30 mars 2020"
        "https://www.legifrance.gouv.fr/eli/decret/2020/3/30/ECOI2007755D/jo/texte",
        "Ordonnance n° 2020-705 du 10 juin 2020"
        "https://www.legifrance.gouv.fr/eli/ordonnance/2020/6/10/ECOI2012371R/jo/texte"
        ]
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula_2020_03(individu, period):
        chiffre_d_affaire = individu('rpns_auto_entrepreneur_chiffre_affaires', period)
        period_1 = period.offset(-1, 'year')
        chiffre_d_affaire_annee_mois_un_an_avant = individu('rpns_auto_entrepreneur_chiffre_affaires', period_1)
        chiffre_d_affaire_annee_moyenne_annee_precedente = individu('rpns_auto_entrepreneur_chiffre_affaires', period.last_year, options = [ADD]) / 12
        chiffre_d_affaire_annee_n_1 = max_(chiffre_d_affaire_annee_mois_un_an_avant, chiffre_d_affaire_annee_moyenne_annee_precedente)
        return individu('travailleur_non_salarie', period) * (((chiffre_d_affaire - chiffre_d_affaire_annee_n_1) / chiffre_d_affaire_annee_n_1) < -0.5)


class covid_aide_exceptionnelle_tpe_montant(Variable):
    entity = Individu
    value_type = float
    label = "Montant de l'aide exceptionnelle pour les TPE pendant la crise sanitaire dûe au COVID-19"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    end = '2020-12-31'

    def formula_2020_03(individu, period, parameters):
        eligibilite_fse = individu('covid_aide_exceptionnelle_tpe_eligible', period)
        plafond_fse = parameters(period).covid19.aide_exceptionnelle_tpe.plafond
        chiffre_d_affaire = individu('rpns_auto_entrepreneur_chiffre_affaires', period)
        period_1 = period.offset(-1, 'year')
        chiffre_d_affaire_annee_mois_un_an_avant = individu('rpns_auto_entrepreneur_chiffre_affaires', period_1)
        chiffre_d_affaire_annee_moyenne_annee_precedente = individu('rpns_auto_entrepreneur_chiffre_affaires', period.last_year, options = [ADD]) / 12
        chiffre_d_affaire_annee_n_1 = max_(chiffre_d_affaire_annee_mois_un_an_avant, chiffre_d_affaire_annee_moyenne_annee_precedente)
        difference_chiffre_d_affaire = chiffre_d_affaire - chiffre_d_affaire_annee_n_1
        return eligibilite_fse * (difference_chiffre_d_affaire < 0) * min_(plafond_fse, -difference_chiffre_d_affaire)


class covid_activite_partielle_eligible(Variable):
    entity = Individu
    value_type = bool
    label = "Eligibilité au dispositif du chômage partiel"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(individu, period):
        return individu('salaire_de_base', period) != 0


class covid_activite_partielle_montant(Variable):
    entity = Individu
    value_type = float
    label = "Montant de l'indemnité salariale de chômage partiel"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        "Ordonnance n° 2020-346 du 27 mars 2020 portant mesures d'urgence en matière d'activité partielle",
        "https://www.legifrance.gouv.fr/eli/ordonnance/2020/3/27/MTRX2008381R/jo/texte",
        ]

    def formula_2020_03(individu, period, parameters):
        '''
        Il s'agit de l'indemnité et pas de l'allocation (somme que doit verser l'entreprise au salarié et pas la somme que l'Etat verse à l'entreprise.
        '''
        eligibilite_activite_partielle = individu('covid_activite_partielle_eligible', period)
        heures = individu('heures_remunerees_volume', period)
        salaire_horaire = individu('salaire_de_base', period) / heures
        indemnite_ap = parameters(period).covid19.indemnite_ap
        indemnite_horaire = max(
            indemnite_ap.taux * salaire_horaire,
            indemnite_ap.plancher
            )
        return eligibilite_activite_partielle * indemnite_horaire * heures
