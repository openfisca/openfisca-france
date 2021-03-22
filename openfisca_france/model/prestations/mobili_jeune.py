from openfisca_france.model.base import Variable, Individu, MONTH


class mobili_jeune_eligibilite(Variable):
    value_type = bool
    label = "Éligibilité à l'aide au logement mobili-jeune"
    entity = Individu
    definition_period = MONTH
    reference = "https://www.actionlogement.fr/l-aide-mobili-jeune"

    def formula(individu, period, parameters):
        condition_age = individu("age", period) < 30
        condition_contrat = individu("alternant", period) * (
            individu("apprenti", period) 
            + individu("professionnalisation", period)
            )
        # 1% logement = https://www.service-public.fr/professionnels-entreprises/vosdroits/F22583
        smic_mensuel_brut = individu("smic_proratise", period)
        condition_remuneration = (
            individu("remuneration_apprenti", period) 
            * individu("remuneration_professionnalisation", period)
            ) <= smic_mensuel_brut
        return condition_age * condition_contrat * condition_remuneration
