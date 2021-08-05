from openfisca_france.model.base import Individu, Variable, MONTH, set_input_dispatch_by_period
from openfisca_france.model.prestations.education import TypesScolarite


class crous_repas_un_euro_eligibilite(Variable):
    value_type = bool
    label = "Éligibilité au repas Crous à un euro"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = "https://www.etudiant.gouv.fr/fr/le-repas-au-crous-passe-1-euro-pour-tous-les-etudiants-2314"
    documentation = '''
    Suite à la crise Covid-19, tous les étudiants, boursiers ou non, peuvent bénéficier
    de deux repas par jour au tarif de 1 euro.
    Pour en bénéficier, il suffit d’activer son compte Izly.
    Pour les étudiants déjà titulaires d’un compte Izly,
    la modification de tarif a été effectuée à partir du vendredi 22 janvier
    et jusqu’au début de la semaine du 25 janvier.
    '''

    def formula_2021_01(individu, period, parameters):
        return individu('scolarite', period) == TypesScolarite.enseignement_superieur
