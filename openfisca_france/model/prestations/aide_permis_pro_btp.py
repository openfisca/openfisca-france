from openfisca_france.model.base import Variable, Individu, MONTH
from numpy import select


class aide_permis_pro_btp(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide au permis B PRO BTP"
    reference = "https://www.probtp.com/part/apprenti/aide-permis.html"
    definition_period = MONTH

    def formula(individu, period, parameters):
        params = parameters(period).prestations.aide_permis_pro_btp

        rfr = individu.foyer_fiscal('rfr', period.this_year)
        montant = select(
            [
                rfr <= params.ressources_annuelles_maximal.premier_echelon,
                rfr <= params.ressources_annuelles_maximal.deuxieme_echelon,
                rfr <= params.ressources_annuelles_maximal.troisieme_echelon,
                ],
            [
                params.montant.premier_echelon,
                params.montant.deuxieme_echelon,
                params.montant.troisieme_echelon,
                ],
            default=0
            )

        age = individu('age', period)
        eligibilite_age = (params.age.minimum <= age) * (age <= params.age.maximum)

        alternant = individu("alternant", period)

        return eligibilite_age * alternant * montant
