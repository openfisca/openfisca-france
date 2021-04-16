from openfisca_france.model.base import *


class seances_sante_psy(Variable):
    value_type = int
    entity = Individu
    label = "Nombre de séances prises en charge par le chèque santé psy"
    definition_period = MONTH
    reference = "https://www.service-public.fr/particuliers/actualites/A14726"

    def formula_2021_03_10(individu, period, parameters):
        '''
        Le nombre maximum de séances est donné sans prendre en compte les passages obligatoires intermédiaires chez un médecin.
        '''
        eligibilite = individu('etudiant', period)

        return eligibilite * parameters(period).prestations.cheque_sante_psy.seances_max
