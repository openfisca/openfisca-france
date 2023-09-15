from openfisca_france.model.base import Individu, Variable, MONTH, set_input_dispatch_by_period, not_
from openfisca_france.model.prestations.education import TypesScolarite


class crous_repas_un_euro_eligibilite(Variable):
    value_type = bool
    label = 'Éligibilité au repas Crous à un euro'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = 'https://www.service-public.fr/particuliers/actualites/A16017'

    def formula_2021_01(individu, period):
        return individu('scolarite', period) == TypesScolarite.enseignement_superieur

    def formula_2021_07(individu, period):
        enseignement_superieur = individu('scolarite', period) == TypesScolarite.enseignement_superieur
        detention_carte_des_metiers = individu('detention_carte_des_metiers', period)
        boursier = individu('boursier', period)
        return boursier * (enseignement_superieur + detention_carte_des_metiers)


class crous_repas_tarif_non_boursiers_eligibilite(Variable):
    value_type = bool
    label = 'Éligibilité au repas Crous au tarif pour les non-boursiers'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = 'https://www.service-public.fr/particuliers/actualites/A16017'

    def formula_2021_07(individu, period):
        enseignement_superieur = individu('scolarite', period) == TypesScolarite.enseignement_superieur
        boursier = individu('boursier', period)
        return not_(boursier) * enseignement_superieur


class crous_repas_montant(Variable):
    value_type = float
    label = 'Montant du repas au restaurant universitaire'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = 'https://www.service-public.fr/particuliers/actualites/A16017'

    def formula(individu, period, parameters):
        etudiant_non_boursier = individu('crous_repas_tarif_non_boursiers_eligibilite', period)
        tarif_repas_non_boursier = parameters(period).prestations_sociales.education.alimentation.montant_repas_non_boursier

        eligibilite_repas_un_euro = individu('crous_repas_un_euro_eligibilite', period)

        montant_repas = eligibilite_repas_un_euro * 1 + (etudiant_non_boursier * tarif_repas_non_boursier)

        return montant_repas
