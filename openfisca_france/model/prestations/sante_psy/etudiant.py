from openfisca_france.model.base import *

from openfisca_france.model.prestations.education import TypesScolarite


class seances_sante_psy_etudiant(Variable):
    value_type = int
    entity = Individu
    label = "Nombre de séances prises en charge par l'Aide Santé Psy Étudiant"
    definition_period = MONTH
    reference = 'https://www.service-public.fr/particuliers/actualites/A14726'
    set_input = set_input_divide_by_period

    def formula_2021_03_10(individu, period, parameters):
        '''
        Le nombre maximum de séances est donné sans prendre en compte les passages obligatoires intermédiaires chez un médecin.
        '''
        etudiant = individu('etudiant', period)
        enseignement_superieur = individu('scolarite', period) == TypesScolarite.enseignement_superieur

        return etudiant * enseignement_superieur * parameters(period).prestations_sociales.aides_jeunes.sante_psy.etudiant.seances_max
