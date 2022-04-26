from openfisca_france.model.base import Variable, Individu, MONTH, TypesActivite, max_, set_input_dispatch_by_period, set_input_divide_by_period


class depart1825_eligibilite(Variable):
    '''
    Situations non prises en compte
    - en contrat aidé,
    - inscrit dans une école de la deuxième chance,
    - volontaire en service civique,
    - jeunes suivis par l'Aide Sociale à l'Enfance.​
    '''
    value_type = bool
    label = 'Éligibilité au dispositif départ 18-25'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = [
        'https://programme-depart-1825.com/eligibilite/',
        'https://www.ancv.com/actualites/le-magazine/depart-1825-un-nouveau-programme-pour-les-jeunes-de-18-25-ans'
        ]

    def formula(individu, period, parameters):
        criteres_age = parameters(period).prestations_sociales.aides_jeunes.depart1825.age
        age = individu('age', period)

        eligibilite_age = (criteres_age.minimum <= age) * (age <= criteres_age.maximum)

        etudiant_boursier = (individu('activite', period) == TypesActivite.etudiant) * individu('boursier', period)
        alternant = individu('alternant', period)
        garantie_jeunes = individu('garantie_jeunes', period) > 0

        eligibilite_statut = etudiant_boursier + alternant + garantie_jeunes

        nbptr = individu.foyer_fiscal('nbptr', period.n_2)
        plafond_ressources = parameters(period).prestations_sociales.aides_jeunes.depart1825.plafond_ressources
        plafond_ressources = plafond_ressources.base + 2 * max_(0, nbptr - 1) * plafond_ressources.par_demi_part_supplementaire

        ressources = individu.foyer_fiscal('rfr', period.n_2)

        eligibilite_financiere = ressources <= plafond_ressources

        return eligibilite_age * (eligibilite_statut + eligibilite_financiere)


class depart1825_montant_maximum(Variable):
    value_type = float
    label = 'Montant maximum du dispositif départ 18-25'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period
    reference = [
        'https://programme-depart-1825.com/eligibilite/',
        'https://www.ancv.com/actualites/le-magazine/depart-1825-un-nouveau-programme-pour-les-jeunes-de-18-25-ans'
        ]

    def formula(individu, period, parameters):

        montant = parameters(period).prestations_sociales.aides_jeunes.depart1825.montant_maximum
        eligibilite = individu('depart1825_eligibilite', period)

        return montant * eligibilite
