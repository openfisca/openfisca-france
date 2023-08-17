from openfisca_france.model.base import Variable, Individu, MONTH
from numpy import select

from openfisca_france.model.caracteristiques_socio_demographiques.demographie import DomaineSpecialitesFormation


class aide_permis_pro_btp(Variable):
    value_type = float
    entity = Individu
    label = "Montant de l'aide au permis B PRO BTP"
    reference = 'https://www.probtp.com/part/apprenti/aide-permis.html'
    definition_period = MONTH

    def formula_2023(individu, period, parameters):
        params = parameters(period).prestations_sociales.education.aide_permis_pro_btp

        smic_annuel = parameters(period).marche_travail.salaire_minimum.smic.smic_b_mensuel * 12
        rfr = individu.foyer_fiscal('rfr', period.this_year)
        eligibilite_ressource = rfr <= smic_annuel

        montant = params.montant.montant_unique

        age = individu('age', period)
        eligibilite_age = (params.age.minimum <= age) * (age < params.age.maximum)

        alternant = individu('alternant', period)

        est_en_formation_btp = individu('domaine_specialites_formation', period) == DomaineSpecialitesFormation.domaine_23

        return eligibilite_age * alternant * eligibilite_ressource * est_en_formation_btp * montant

    def formula(individu, period, parameters):
        params = parameters(period).prestations_sociales.education.aide_permis_pro_btp

        rfr = individu.foyer_fiscal('rfr', period.this_year)
        montant = select(
            [
                rfr <= params.plafonds.premier_echelon,
                rfr <= params.plafonds.deuxieme_echelon,
                rfr <= params.plafonds.troisieme_echelon,
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

        alternant = individu('alternant', period)

        est_en_formation_btp = individu('domaine_specialites_formation', period) == DomaineSpecialitesFormation.domaine_23

        return eligibilite_age * alternant * montant * est_en_formation_btp
