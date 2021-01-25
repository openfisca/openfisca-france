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

    def formula_2020_03(individu, period):
        chiffre_d_affaire = individu('tns_auto_entrepreneur_chiffre_affaires', period)
        period_1 = period.offset(-1, 'year')
        chiffre_d_affaire_annee_mois_un_an_avant = individu('tns_auto_entrepreneur_chiffre_affaires', period_1)
        chiffre_d_affaire_annee_moyenne_annee_precedente = individu('tns_auto_entrepreneur_chiffre_affaires', period.last_year, options = [ADD]) / 12
        chiffre_d_affaire_annee_n_1 = max_(chiffre_d_affaire_annee_mois_un_an_avant, chiffre_d_affaire_annee_moyenne_annee_precedente)
        return individu('travailleur_non_salarie', period) * (((chiffre_d_affaire - chiffre_d_affaire_annee_n_1) / chiffre_d_affaire_annee_n_1) < -0.5)


class covid_aide_exceptionnelle_tpe_montant(Variable):
    entity = Individu
    value_type = float
    label = "Montant de l'aide exceptionnelle pour les TPE pendant la crise sanitaire dûe au COVID-19"
    definition_period = MONTH
    end = '2020-12-31'

    def formula_2020_03(individu, period, parameters):
        eligibilite_fse = individu('covid_aide_exceptionnelle_tpe_eligible', period)
        plafond_fse = parameters(period).covid19.aide_exceptionnelle_tpe.plafond
        chiffre_d_affaire = individu('tns_auto_entrepreneur_chiffre_affaires', period)
        period_1 = period.offset(-1, 'year')
        chiffre_d_affaire_annee_mois_un_an_avant = individu('tns_auto_entrepreneur_chiffre_affaires', period_1)
        chiffre_d_affaire_annee_moyenne_annee_precedente = individu('tns_auto_entrepreneur_chiffre_affaires', period.last_year, options = [ADD]) / 12
        chiffre_d_affaire_annee_n_1 = max_(chiffre_d_affaire_annee_mois_un_an_avant, chiffre_d_affaire_annee_moyenne_annee_precedente)
        difference_chiffre_d_affaire = chiffre_d_affaire - chiffre_d_affaire_annee_n_1
        return eligibilite_fse * (difference_chiffre_d_affaire < 0) * min_(plafond_fse, -difference_chiffre_d_affaire)


class covid_aide_exceptionnelle_famille_montant(Variable):
    entity = Famille
    value_type = float
    label = "Montant de l'aide exceptionnelle pour les familles pendant la crise sanitaire dûe au COVID-19"
    definition_period = MONTH
    end = '2020-10-31'

    def formula_2020_05(famille, period, parameters):

        montants = parameters(period).covid19.aide_exceptionnelle_famille
        rsa = famille('rsa', period) > 0
        ass = famille.sum(famille.members('ass', period)) > 0
        al = famille('aide_logement', period) > 0
        af_nbenf = famille('af_nbenf', period)
        aer = famille.sum(famille.members('aer', period)) > 0
        prim_forf = famille.sum(famille.members('prime_forfaitaire_mensuelle_reprise_activite', period)) > 0
        age_i = famille.members('age', period)
        etudiant_i = famille.members('etudiant', period)
        moins_de_25_ans_non_etudiant = famille.any((age_i <= 24) * (etudiant_i == 0), role = Famille.PARENT)
        base_jeune = moins_de_25_ans_non_etudiant * al
        base = (rsa + ass + aer + prim_forf)
        montant = (
            base_jeune * (montants.base_jeune + montants.par_enfant * af_nbenf)
            + base * not_(base_jeune) * (montants.base + montants.par_enfant * af_nbenf)
            + not_(base) * not_(base_jeune) * al * af_nbenf * montants.par_enfant
            )

        period_1 = period.offset(-1, 'month')
        rsa_n_1 = famille('rsa', period_1) > 0
        ass_n_1 = famille.sum(famille.members('ass', period_1)) > 0
        al_n_1 = famille('aide_logement', period_1) > 0
        af_nbenf_n_1 = famille('af_nbenf', period_1) > 0
        aer_n_1 = famille.sum(famille.members('aer', period_1)) > 0
        prim_forf_n_1 = famille.sum(famille.members('prime_forfaitaire_mensuelle_reprise_activite', period_1)) > 0
        age_i_n_1 = famille.members('age', period_1)
        etudiant_i_n_1 = famille.members('etudiant', period_1)
        moins_de_25_ans_non_etudiant_n_1 = famille.any((age_i_n_1 <= 24) * (etudiant_i_n_1 == 0), role = Famille.PARENT)
        base_jeune_n_1 = moins_de_25_ans_non_etudiant_n_1 * al_n_1
        base_n_1 = (rsa_n_1 + ass_n_1 + aer_n_1 + prim_forf_n_1)
        montant_n_1 = (
            base_jeune_n_1 * (montants.base_jeune + montants.par_enfant * af_nbenf_n_1)
            + base_n_1 * not_(base_jeune_n_1) * (montants.base + montants.par_enfant * af_nbenf_n_1)
            + not_(base_n_1) * not_(base_jeune_n_1) * al_n_1 * af_nbenf_n_1 * montants.par_enfant
            )

        return max_(montant, montant_n_1)


class covid_activite_partielle_eligible(Variable):
    entity = Individu
    value_type = bool
    label = "Eligibilité au dispositif du chômage partiel"
    definition_period = MONTH

    def formula(individu, period):
        return individu('salaire_de_base', period) != 0


class covid_activite_partielle_montant(Variable):
    entity = Individu
    value_type = float
    label = "Montant de l'indemnité salariale de chômage partiel"
    definition_period = MONTH
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
