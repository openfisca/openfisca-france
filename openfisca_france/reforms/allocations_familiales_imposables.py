# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import columns
from openfisca_core.reforms import Reform
from ..model.base import *


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "type": "node",
        "description": "Intégration au revenu imposable des allocations familiales",
        "children": {
            "imposition": {
                "type": "parameter",
                "description": "Indicatrice d'imposition",
                "format": "boolean",
                "values": [
                    {'start': u'2015-01-01', },
                    {'start': u'2000-01-01', 'value': True}
                    ],
                },
            },
        }
    reference_legislation_json_copy['children']['allocations_familiales_imposables'] = reform_legislation_subtree
    return reference_legislation_json_copy


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
            cga = simulation.legislation_at(period.start).impot_revenu.rpns.cga_taux2

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
            f3va_holder = simulation.calculate('f3va')
            f3vi_holder = simulation.calculate('f3vi')
            f3vz = simulation.calculate('f3vz')
            rfr_cd = simulation.calculate('rfr_cd')
            rfr_rvcm = simulation.calculate('rfr_rvcm')
            rni = simulation.calculate('rni')
            rpns_exon_holder = simulation.calculate('rpns_exon')
            rpns_pvce_holder = simulation.calculate('rpns_pvce')
            rev_cap_lib = simulation.calculate_add('rev_cap_lib')
            microentreprise = simulation.calculate('microentreprise')

            f3va = self.sum_by_entity(f3va_holder)
            f3vi = self.sum_by_entity(f3vi_holder)
            rpns_exon = self.sum_by_entity(rpns_exon_holder)
            rpns_pvce = self.sum_by_entity(rpns_pvce_holder)

            return (
                max_(0, rni - allocations_familiales_imposables) +
                rfr_cd + rfr_rvcm + rev_cap_lib + f3vi + rpns_exon + rpns_pvce + f3va + f3vz + microentreprise
                )

    class allocations_familiales_imposables(Variable):
        column = columns.FloatCol
        entity = FoyerFiscal
        label = u"Allocations familiales imposables"
        definition_period = YEAR

        def formula(self, simulation, period):
            imposition = simulation.legislation_at(period.start).allocations_familiales_imposables.imposition
            af = simulation.foyer_fiscal.declarant_principal.famille('af', period, options = [ADD])

            return af * imposition

    def apply(self):
        self.update_variable(self.rbg)
        self.update_variable(self.rfr)
        self.add_variable(self.allocations_familiales_imposables)
        self.modify_legislation_json(modifier_function = modify_legislation_json)
