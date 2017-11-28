# -*- coding: utf-8 -*-

from __future__ import division

import os

from ..model.base import *


dir_path = os.path.join(os.path.dirname(__file__), 'parameters')


def modify_parameters(parameters):
    file_path = os.path.join(dir_path, 'allocations_familiales_imposables.yaml')
    reform_parameters_subtree = load_parameter_file(name='allocations_familiales_imposables', file_path=file_path)
    parameters.add_child('allocations_familiales_imposables', reform_parameters_subtree)
    return parameters


class allocations_familiales_imposables(Reform):
    name = u'Allocations familiales imposables'

    class rbg(Variable):
        label = u"Nouveau revenu brut global intégrant les allocations familiales"
        definition_period = YEAR

        def formula(self, simulation, period):
            allocations_familiales_imposables = simulation.calculate_add('allocations_familiales_imposables', period)
            deficit_ante = simulation.calculate('deficit_ante', period)
            f6gh = simulation.calculate('f6gh', period)
            nacc_pvce_holder = simulation.calculate('nacc_pvce', period)
            nbic_impm_holder = simulation.calculate('nbic_impm', period)
            rev_cat = simulation.calculate('rev_cat', period)
            cga = simulation.parameters_at(period.start).impot_revenu.rpns.cga_taux2

            nacc_pvce = self.sum_by_entity(nacc_pvce_holder)
            return max_(
                0,
                allocations_familiales_imposables + rev_cat + f6gh +
                (self.sum_by_entity(nbic_impm_holder) + nacc_pvce) * (1 + cga) - deficit_ante
                )

    class rfr(Variable):
        label = u"Nouveau revenu fiscal de référence intégrant les allocations familiales"
        definition_period = YEAR

        def formula(self, simulation, period):
            allocations_familiales_imposables = simulation.calculate('allocations_familiales_imposables')
            abatnet_retraite_dirigeant_pme = simulation.calculate('abatnet_retraite_dirigeant_pme')
            f3vi_holder = simulation.calculate('f3vi')
            f3vz = simulation.calculate('f3vz')
            rfr_cd = simulation.calculate('rfr_cd')
            rfr_rvcm = simulation.calculate('rfr_rvcm')
            rni = simulation.calculate('rni')
            rpns_exon_holder = simulation.calculate('rpns_exon')
            rpns_pvce_holder = simulation.calculate('rpns_pvce')
            rev_cap_lib = simulation.calculate_add('rev_cap_lib')
            microentreprise = simulation.calculate('microentreprise')

            f3vi = self.sum_by_entity(f3vi_holder)
            rpns_exon = self.sum_by_entity(rpns_exon_holder)
            rpns_pvce = self.sum_by_entity(rpns_pvce_holder)

            return (
                max_(0, rni - allocations_familiales_imposables) +
                rfr_cd + rfr_rvcm + rev_cap_lib + f3vi + rpns_exon + rpns_pvce + abatnet_retraite_dirigeant_pme + f3vz + microentreprise
                )

            # TO CHECK : f3vb after 2015 (abattements sur moins-values = interdits)

    class allocations_familiales_imposables(Variable):
        value_type = float
        entity = FoyerFiscal
        label = u"Allocations familiales imposables"
        definition_period = YEAR

        def formula(self, simulation, period):
            imposition = simulation.parameters_at(period.start).allocations_familiales_imposables.imposition
            af = simulation.foyer_fiscal.declarant_principal.famille('af', period, options = [ADD])

            return af * imposition

    def apply(self):
        self.update_variable(self.rbg)
        self.update_variable(self.rfr)
        self.add_variable(self.allocations_familiales_imposables)
        self.modify_parameters(modifier_function = modify_parameters)
