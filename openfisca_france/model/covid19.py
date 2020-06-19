from openfisca_france.model.base import Variable, Individu, Famille, MONTH, not_


class covid_aide_exceptionnelle_tpe_eligible(Variable):
    entity = Individu
    value_type = bool
    label = "Éligibilité à l'aide exceptionnelle pour les TPE pendant la crise sanitaire dûe au COVID-19"
    reference = [
        "Décret n°2020-371 du 30 mars 2020"
        "https://www.legifrance.gouv.fr/eli/decret/2020/3/30/ECOI2007755D/jo/texte",
        ]
    definition_period = MONTH

    def formula(individu, period):
        return individu('travailleur_non_salarie', period)


class covid_aide_exceptionnelle_tpe_montant(Variable):
    entity = Individu
    value_type = float
    label = "Montant de l'aide exceptionnelle pour les TPE pendant la crise sanitaire dûe au COVID-19"
    definition_period = MONTH
    end = '2020-05-31'

    def formula_2020_03(individu, period, parameters):
        elig = individu('covid_aide_exceptionnelle_tpe_eligible', period)
        return elig * parameters(period).covid19.aide_exceptionnelle_tpe.montant


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
