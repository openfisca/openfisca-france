from openfisca_france.model.base import Individu, Variable, MONTH, set_input_dispatch_by_period
from openfisca_france.model.prestations.education import TypesScolarite


class crous_repas_un_euro_eligibilite(Variable):
    value_type = bool
    label = 'Éligibilité au repas Crous à un euro'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = 'https://www.etudiant.gouv.fr/fr/crous-resto-c-est-bon-de-s-y-retrouver-1195'

    def formula_2021_01(individu, period):
        return individu('scolarite', period) == TypesScolarite.enseignement_superieur

    def formula_2021_07(individu, period):
        enseignement_superieur = individu('scolarite', period) == TypesScolarite.enseignement_superieur
        detention_carte_des_metiers = individu('detention_carte_des_metiers', period)
        boursier = individu('boursier', period)
        return boursier * (enseignement_superieur + detention_carte_des_metiers)
