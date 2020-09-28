from openfisca_france.model.base import Variable, Individu, Famille, MONTH, not_

class covid_aide_exceptionnelle_tpe_eligible(Variable):
    entity = Individu
    value_type = bool
    label = "Éligibilité à l'aide exceptionnelle pour les TPE pendant la crise sanitaire dûe au COVID-19"
    reference = [
        "Décret n°2020-371 du 30 mars 2020"
        "https://www.legifrance.gouv.fr/eli/decret/2020/3/30/ECOI2007755D/jo/texte",
        "Ordonnance n° 2020-705 du 10 juin 2020"
        "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000041983045?r=D4toiqv7co"
        ]
    definition_period = MONTH

    def formula(individu, period):
        ca_n = individu('tns_auto_entrepreneur_chiffre_affaires', period)
        period_1 = period.offset(-1, 'year')
        ca_n_1 = individu('tns_auto_entrepreneur_chiffre_affaires', period_1)
        delta_ca_rel = (ca_n - ca_n_1)/ca_n_1
        return individu('travailleur_non_salarie', period)*(delta_ca_rel<-0.5)


class covid_aide_exceptionnelle_tpe_montant(Variable):
    entity = Individu
    value_type = float
    label = "Montant de l'aide exceptionnelle pour les TPE pendant la crise sanitaire dûe au COVID-19"
    definition_period = MONTH
    end = '2020-12-31'

    def formula_2020_03(individu, period, parameters):
        elig = individu('covid_aide_exceptionnelle_tpe_eligible', period)
        plaf = parameters(period).covid19.aide_exceptionnelle_tpe.plafond
        ca_n = individu('tns_auto_entrepreneur_chiffre_affaires', period)
        period_1 = period.offset(-1, 'year')
        ca_n_1 = individu('tns_auto_entrepreneur_chiffre_affaires', period_1)
        delta_ca = ca_n - ca_n_1
        return elig*(delta_ca < 0)*((delta_ca < -plaf)*plaf + (delta_ca> -plaf)*(-delta_ca))


class covid_aide_exceptionnelle_famille_eligible(Variable):
    entity = Famille
    value_type = bool
    label = "Montant de l'aide exceptionnelle pour les familles pendant la crise sanitaire dûe au COVID-19"
    reference = [
        "Décret n°2020-519 du 5 mai 2020"
        "https://www.legifrance.gouv.fr/eli/decret/2020/5/5/SSAA2010355D/jo/texte",
        ]
    definition_period = MONTH

    def formula(famille, period, parameters):
        rsa = famille('rsa', period) > 0
        ass = famille.sum(famille.members('ass', period)) > 0
        al = famille('aide_logement', period) > 0
        af_nbenf = famille('af_nbenf', period) > 0

        return rsa + ass + (al * af_nbenf)


class covid_aide_exceptionnelle_famille_montant(Variable):
    entity = Famille
    value_type = float
    label = "Montant de l'aide exceptionnelle pour les familles pendant la crise sanitaire dûe au COVID-19"
    definition_period = MONTH
    end = '2020-05-31'

    def formula_2020_03(famille, period, parameters):
        montants = parameters(period).covid19.aide_exceptionnelle_famille
        rsa = famille('rsa', period) > 0
        ass = famille.sum(famille.members('ass', period)) > 0
        al = famille('aide_logement', period) > 0
        af_nbenf = famille('af_nbenf', period)

        base = rsa + ass

        return base * (montants.base + montants.par_enfant * af_nbenf) + not_(base) * al * af_nbenf * montants.par_enfant

class covid_activite_partielle_eligible(Variable):
    entity = Individu
    value_type = bool
    label = "Eligibilité au dispositif du chômage partiel"
    definition_period = MONTH

    def formula(individu, period) :
        return individu('salaire_de_base', period)!=0

class covid_activite_partielle_montant(Variable):
    entity = Individu
    value_type = float
    label = "Montant de l'indemnité salariale de chômage partiel"
    definition_period = MONTH
    
    def formula_2020_03(individu, period, parameters) :
        elig= individu('covid_activite_partielle_eligible', period)
        heures = individu('heures_remunerees_volume', period)
        salh = individu('salaire_de_base', period) / heures
        indemn_nonplaf_h = parameters(period).covid19.indemnite_ap.taux * salh
        plaf = parameters(period).cotsoc.gen.smic_h_b * parameters(period).covid19.indemnite_ap.plafond_smic
        plancher = parameters(period).covid19.indemnite_ap.plancher
        indemn_h = max(min(indemn_nonplaf_h, plaf), plancher)
        return elig*indemn_h*heures 

