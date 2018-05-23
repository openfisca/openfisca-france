# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import columns
from openfisca_core.reforms import Reform
try:
    from scipy.optimize import fsolve
except ImportError:
    fsolve = None

from .. import entities
from ..model.base import *

def calculate_net_from(salaire_de_base, individu, period, requested_variable_names):

    # We're not wanting to calculate salaire_de_base again, but instead manually set it as an input variable
    individu.get_holder('salaire_de_base').put_in_cache(salaire_de_base, period)

    # Work in isolation
    temp_simulation = individu.simulation.clone()
    temp_individu = temp_simulation.individu

    # Calculated variable holders might contain undesired cache
    # (their entity.simulation points to the original simulation above)
    for name in requested_variable_names:
        temp_individu.get_holder[name].delete_arrays()

    # Force recomputing of salaire_net
    temp_individu.get_holder('salaire_net_a_payer').delete_arrays()

    net = temp_individu('salaire_net_a_payer', period)[0]

    return net

class salaire_de_base(Variable):
    value_type = float
    entity = entities.Individu
    label = u"Salaire brut ou traitement indiciaire brut"
    reference = u"http://www.trader-finance.fr/lexique-finance/definition-lettre-S/Salaire-brut.html"
    definition_period = MONTH

    def formula(individu, period, parameters):
        # Calcule le salaire brut à partir du salaire net par inversion numérique.

        net = individu.get_holder('salaire_net_a_payer').get_array(period)

        if net is None:
            return individu.empty_array()

        simulation = individu.simulation

        # List of variables already calculated. We will need it to remove their holders,
        # that might contain undesired cache
        requested_variable_names = list(simulation.requested_periods_by_variable_name.keys())
        if requested_variable_names:
            requested_variable_names.remove(u'salaire_de_base')
        # Clean 'requested_periods_by_variable_name', that is used by -core to check for computation cycles.
        # This variable, salaire_de_base, might have been called from variable X,
        # that will be calculated again in our iterations to compute the salaire_net requested
        # as an input variable, hence producing a cycle error
        simulation.requested_periods_by_variable_name = dict()

        def solve_func(net):
            def innerfunc(essai):
                return calculate_net_from(essai, individu, period, requested_variable_names) - net
            return innerfunc
        brut_calcule = fsolve(
            solve_func(net),
            net * 1.5,  # on entend souvent parler cette méthode...
            xtol = 1 / 10  # précision
            )

        return brut_calcule

class de_net_a_brut(Reform):
    name = u'Inversion du calcul brut -> net'

    def apply(self):
        self.update_variable(salaire_de_base)
