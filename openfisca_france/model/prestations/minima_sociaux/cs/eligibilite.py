from numpy import logical_not as not_
from openfisca_france.model.base import Variable, Famille, MONTH, ADD, set_input_dispatch_by_period


class css_cmu_acs_eligibilite(Variable):
    value_type = bool
    entity = Famille
    label = "Pré-éligibilité à l'ACS, la CMU-C et à la CSS, avant prise en compte des ressources"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(famille, period, parameters):
        previous_year = period.start.period('year').offset(-1)
        this_year = period.this_year
        age_min = parameters(period).prestations_sociales.solidarite_insertion.minima_sociaux.cs.cmu.age_limite_pac
        nb_enfants = famille('cmu_nb_pac', period)

        # Une personne de 25 ans ne doit pas être à charge fiscale, ni hébergée par ses parents, ni recevoir de pensions alimentaires pour pouvoir bénéficier de la CMU individuellement.
        a_charge_des_parents = famille.members('enfant_a_charge', this_year)
        habite_chez_parents = famille.members('habite_chez_parents', period)
        recoit_pension = famille.members('pensions_alimentaires_percues', previous_year, options = [ADD]) > 0
        condition_independance = not_(a_charge_des_parents + habite_chez_parents + recoit_pension)

        age = famille.members('age', period)
        condition_age = (age >= age_min)

        eligibilite_famille = (
            (nb_enfants > 0)
            + famille.any(condition_age)
            + famille.all(condition_independance)
            )

        return eligibilite_famille
