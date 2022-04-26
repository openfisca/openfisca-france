from openfisca_france.model.base import *

from openfisca_france.model.prestations.education import TypesScolarite


class aide_formation_gen_eligibilite(Variable):
    value_type = bool
    entity = Individu
    reference = 'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000034429379/'
    label = "Éligibilité à l'aide accordée aux personnes inscrites dans une formation labellisée par la Grande Ecole du numérique"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula_2017_04_14(individu, period):
        '''
        Les conditions de non-cumul spécifiques à la formation ne sont pas modélisées car aucune n'est modélisée à ce jour dans OpenFisca et qu'un grand nombre sont arbitraires ou à l'échelon infra-national :
        - L'aide n'est pas cumulable avec une aide spécifique versée par le ministre chargé de l'enseignement supérieur ou les établissements publics qui en relèvent.
        - Sont exclues du bénéfice de l'aide les personnes inscrites à Pôle Emploi comme demandeurs d'emploi qui perçoivent une aide à l'insertion ou une aide à la formation professionnelle ainsi que […] les personnes en congé individuel de formation.
        - Sont également exclues du bénéfice de l'aide les personnes percevant une aide du ministère chargé de l'emploi ou d'un conseil régional versée au titre de la formation professionnelle ou de l'insertion professionnelle.
        '''
        eligibilite_formation = individu('scolarite', period) == TypesScolarite.grande_ecole_du_numerique
        eligibilite_nationalite = individu('bourse_criteres_sociaux_eligibilite_nationalite', period)

        non_cumul = individu('alternant', period) + (
            individu.famille('rsa', period) * not_(individu.famille('rsa_majore_eligibilite', period))
            )

        return eligibilite_formation * eligibilite_nationalite * not_(non_cumul)


class aide_formation_gen(Variable):
    value_type = float
    entity = Individu
    reference = 'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000034429379/'
    label = "Montant de l'aide accordée aux personnes inscrites dans une formation labellisée par la Grande Ecole du numérique"
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2017_04_14(individu, period, parameters):
        points_de_charge = individu('bourse_criteres_sociaux_points_de_charge', period)
        baremes = parameters(period).prestations_sociales.aides_jeunes.bourses.bourses_enseignement_superieur.criteres_sociaux.plafond_ressources
        plafond_echelon_0bis = baremes.echelon_0bis.calc(points_de_charge)
        plafond_echelon_1 = baremes.echelon_1.calc(points_de_charge)
        plafond_echelon_2 = baremes.echelon_2.calc(points_de_charge)
        plafond_echelon_3 = baremes.echelon_3.calc(points_de_charge)
        plafond_echelon_4 = baremes.echelon_4.calc(points_de_charge)
        plafond_echelon_5 = baremes.echelon_5.calc(points_de_charge)
        plafond_echelon_6 = baremes.echelon_6.calc(points_de_charge)
        plafond_echelon_7 = baremes.echelon_7.calc(points_de_charge)

        base_ressources = individu('bourse_criteres_sociaux_base_ressources', period)
        echelon = select(
            [
                base_ressources <= plafond_echelon_7,
                base_ressources <= plafond_echelon_6,
                base_ressources <= plafond_echelon_5,
                base_ressources <= plafond_echelon_4,
                base_ressources <= plafond_echelon_3,
                base_ressources <= plafond_echelon_2,
                base_ressources <= plafond_echelon_1,
                base_ressources <= plafond_echelon_0bis,
                ],
            [7, 6, 5, 4, 3, 2, 1, 0], default=-1)

        montants = parameters(period).prestations_sociales.aides_jeunes.bourses.bourses_enseignement_superieur.criteres_sociaux.montants

        return montants.calc(echelon) * individu('aide_formation_gen_eligibilite', period)
