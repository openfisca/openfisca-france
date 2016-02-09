# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import columns, reforms
from scipy.optimize import fsolve

from .. import entities


def calculate_net_from(salaire_de_base, simulation, period):
    temp_simulation = simulation.clone()

    temp_simulation.get_or_new_holder('salaire_de_base').array = salaire_de_base

    del temp_simulation.holder_by_name['salaire_net'] # required
    temp_simulation.holder_by_name['salaire_de_base'].formula.function = None # will avoid getting a cycles exception
    net = temp_simulation.calculate('salaire_net', period, max_nb_cycles=10)[0]
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

            net = simulation.get_array('salaire_net', period)

            simulation = self.holder.entity.simulation

            def solve_func(net):
                def innerfunc(essai):
                    return calculate_net_from(essai, simulation, period) - net
                return innerfunc

            brut_calcule = \
                fsolve(
                    solve_func(net),
                    net*1.5,  # on entend souvent parler cette méthode...
                    xtol = 1/10  # précision
                    )

            return period, brut_calcule

    return Reform()
