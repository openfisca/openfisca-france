from openfisca_france.model.base import Variable, MONTH, Individu
from numpy import datetime64


class pass_colo(Variable):
    label = 'Éligibilité au Pass colo'
    definition_period = MONTH
    value_type = float
    reference = ['https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000049339145',
                 'https://www.jeunes.gouv.fr/passcolo']
    entity = Individu
    documentation = '''
    Modélisation (2024) :
        -  Avoir un enfant né(e) en 2013, il/elle souhaite partir en colonie de vacances et le quotient familial est égal ou inférieur à 1500€.
    '''

    def formula_2024_01(individu, period, parameters):
        parametres = parameters(period).prestations_sociales.education.pass_colo
        annee_naissance_enfant = datetime64(str(parametres.annee_naissance_enfant))
        annee_naissance_eligible = any(annee_naissance_enfant == year.astype('datetime64[Y]') for year in individu.famille.members('date_naissance', period))

        rfr = individu.foyer_fiscal('rfr', period.n_2)
        nbptr = individu.foyer_fiscal('nbptr', period.n_2)
        quotient_familial = rfr / nbptr

        modalites = parametres.montants
        montant = modalites.calc(quotient_familial)

        return montant * annee_naissance_eligible
