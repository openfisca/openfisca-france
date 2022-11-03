from openfisca_core.reforms import Reform

try:
    from scipy.optimize import fsolve
except ImportError:
    fsolve = None

from .. import entities
from ..model.base import *


def calculate_net_from(salaire_de_base, individu, period):

    # We're not wanting to calculate salaire_de_base again, but instead manually set it as an input variable
    individu.get_holder('salaire_de_base').put_in_cache(salaire_de_base, period)

    # Work in isolation
    temp_simulation = individu.simulation.clone()
    temp_individu = temp_simulation.individu

    # Force recomputing of salaire_net
    temp_individu.get_holder('salaire_net_a_payer').delete_arrays()

    net = temp_individu('salaire_net_a_payer', period)[0]

    return net


class salaire_de_base(Variable):
    value_type = float
    entity = entities.Individu
    label = 'Salaire brut'
    definition_period = MONTH

    def formula(individu, period, parameters):
        # Calcule le salaire brut à partir du salaire net par inversion numérique.

        net = individu.get_holder('salaire_net_a_payer').get_array(period)

        if net is None:
            return individu.empty_array()

        def solve_func(net):
            def innerfunc(essai):
                return calculate_net_from(essai, individu, period) - net
            return innerfunc
        brut_calcule = fsolve(
            solve_func(net),
            net * 1.5,  # on entend souvent parler cette méthode...
            xtol = 1 / 10  # précision
            )

        return brut_calcule


class de_net_a_brut(Reform):
    name = 'Inversion du calcul brut -> net'

    def apply(self):
        self.update_variable(salaire_de_base)
