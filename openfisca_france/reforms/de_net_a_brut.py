# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import columns, reforms
from scipy.optimize import fsolve

from .. import entities


def calculate_net_from(salaire_de_base, simulation, period, requested_variable_names):

    # We're not wanting to calculate salaire_de_base again, but instead manually set it as an input variable
    # To avoid possible conflicts, remove its function
    simulation.holder_by_name['salaire_de_base'].formula.function = None
    simulation.get_or_new_holder('salaire_de_base').array = salaire_de_base

    # Work in isolation
    temp_simulation = simulation.clone()

    # Calculated variable holders might contain undesired cache
    # (their entity.simulation points to the original simulation above)
    for name in requested_variable_names:
        del temp_simulation.holder_by_name[name]

    # Force recomputing of salaire_net
    del temp_simulation.holder_by_name['salaire_net_a_payer']

    net = temp_simulation.calculate('salaire_net_a_payer', period)[0]

    return net


def build_reform(tax_benefit_system):

    Reform = reforms.make_reform(
        key = 'de_net_a_brut',
        name = u'Inversion du calcul brut -> net',
        reference = tax_benefit_system,
        )

    class salaire_de_base(Reform.Variable):
        column = columns.FloatCol
        entity_class = entities.Individus
        label = u"Salaire brut ou traitement indiciaire brut"
        reference = tax_benefit_system.column_by_name["salaire_de_base"]
        url = u"http://www.trader-finance.fr/lexique-finance/definition-lettre-S/Salaire-brut.html"

        def function(self, simulation, period):
            # Calcule le salaire brut à partir du salaire net par inversion numérique.

            net = simulation.get_array('salaire_net_a_payer', period)

            assert net is not None

            simulation = self.holder.entity.simulation

            # List of variables already calculated. We will need it to remove their holders,
            # that might contain undesired cache
            requested_variable_names = simulation.requested_periods_by_variable_name.keys()
            if requested_variable_names:
                requested_variable_names.remove(u'salaire_de_base')
            # Clean 'requested_periods_by_variable_name', that is used by -core to check for computation cycles.
            # This variable, salaire_de_base, might have been called from variable X,
            # that will be calculated again in our iterations to compute the salaire_net requested
            # as an input variable, hence producing a cycle error
            simulation.requested_periods_by_variable_name = dict()

            def solve_func(net):
                def innerfunc(essai):
                    return calculate_net_from(essai, simulation, period, requested_variable_names) - net
                return innerfunc

            brut_calcule = \
                fsolve(
                    solve_func(net),
                    net*1.5,  # on entend souvent parler cette méthode...
                    xtol = 1/10  # précision
                    )

            return period, brut_calcule

    return Reform()
