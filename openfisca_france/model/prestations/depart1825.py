from openfisca_france.model.base import Variable, Individu, MONTH, TypesActivite, max_


class depart1825_plafond_ressources(Variable):
    value_type = float
    entity = Individu
    definition_period = MONTH
    label = "Plafond de ressources pour le calcul de l'éligibilité au dispositif départ 18-25"

    def formula(individu, period, parameters):
        nbptr = individu.foyer_fiscal('nbptr', period.n_2)
        plafond_ressources = parameters(period).prestations.depart1825.plafond_ressources
        return plafond_ressources.base + 2 * max_(0, nbptr - 1) * plafond_ressources.par_demi_part_supplementaire


class depart1825_eligibilite_financiere(Variable):
    value_type = bool
    label = "Éligibilité au dispositif via les ressources du foyer"
    entity = Individu
    definition_period = MONTH
    reference = [
        "https://programme-depart-1825.com/eligibilite/"
        ]

    def formula(individu, period):
        ressources = individu.foyer_fiscal('rfr', period.n_2)
        plafond_ressources = individu('depart1825_plafond_ressources', period)
        return ressources <= plafond_ressources


class depart1825_eligibilite_statut(Variable):
    """
    Situations non prises en compte
    - en contrat aidé,
    - inscrit dans une école de la deuxième chance,
    - volontaire en service civique,
    - jeunes suivis par l'Aide Sociale à l'Enfance.​
    """
    value_type = bool
    label = "Éligibilité au dispositif via la situation du jeune"
    entity = Individu
    definition_period = MONTH
    reference = [
        "https://programme-depart-1825.com/eligibilite/"
        ]

    def formula(individu, period):
        etudiant_boursier = (individu('activite', period) == TypesActivite.etudiant) * individu('boursier', period)
        alternant = individu('alternant', period)
        garantie_jeunes = individu('garantie_jeunes', period) > 0

        return etudiant_boursier + alternant + garantie_jeunes


class depart1825_eligibilite(Variable):
    value_type = bool
    label = "Éligibilité au dispositif départ 18-25"
    entity = Individu
    definition_period = MONTH
    reference = [
        "https://programme-depart-1825.com/eligibilite/",
        "https://www.ancv.com/actualites/le-magazine/depart-1825-un-nouveau-programme-pour-les-jeunes-de-18-25-ans"
        ]

    def formula(individu, period, parameters):
        criteres_age = parameters(period).prestations.depart1825.age
        age = individu('age', period)

        eligibilite_statut = individu('depart1825_eligibilite_statut', period)
        eligibilite_financiere = individu('depart1825_eligibilite_financiere', period)
        eligible = eligibilite_statut + eligibilite_financiere

        return (criteres_age.minimum <= age) * (age <= criteres_age.maximum) * eligible


class depart1825(Variable):
    value_type = float
    label = "Montant maximum du dispositif départ 18-25"
    entity = Individu
    definition_period = MONTH
    reference = [
        "https://programme-depart-1825.com/eligibilite/",
        "https://www.ancv.com/actualites/le-magazine/depart-1825-un-nouveau-programme-pour-les-jeunes-de-18-25-ans"
        ]

    def formula(individu, period, parameters):
        montant = parameters(period).prestations.depart1825.montant_maximum
        eligibilite = individu('depart1825_eligibilite', period)

        return montant * eligibilite
