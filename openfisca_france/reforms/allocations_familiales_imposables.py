# -*- coding: utf-8 -*-

from __future__ import division

from numpy import maximum as max_
from openfisca_core import columns, reforms

from .. import entities
from ..model.base import QUIFOY
from ..model.prelevements_obligatoires.impot_revenu import ir


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'allocations_familiales_imposables',
        name = u'Allocations familiales imposables',
        reference = tax_benefit_system,
        )

    class rbg(Reform.Variable):
        label = u"Nouveau revenu brut global intégrant les allocations familiales"
        reference = ir.rbg

        def function(self, simulation, period):
            period = period.this_year
            allocations_familiales_imposables = simulation.calculate_add('allocations_familiales_imposables', period)
            deficit_ante = simulation.calculate('deficit_ante', period)
            f6gh = simulation.calculate('f6gh', period)
            nacc_pvce_holder = simulation.calculate('nacc_pvce', period)
            nbic_impm_holder = simulation.calculate('nbic_impm', period)
            rev_cat = simulation.calculate('rev_cat', period)
            cga = simulation.legislation_at(period.start).ir.rpns.cga_taux2

            nacc_pvce = self.sum_by_entity(nacc_pvce_holder)
            return period, max_(
                0,
                allocations_familiales_imposables + rev_cat + f6gh +
                (self.sum_by_entity(nbic_impm_holder) + nacc_pvce) * (1 + cga) - deficit_ante
                )

    class rfr(Reform.Variable):
        label = u"Nouveau revenu fiscal de référence intégrant les allocations familiales"
        reference = ir.rfr

        def function(self, simulation, period):
            period = period.this_year

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

            return period, (
                max_(0, rni - allocations_familiales_imposables) +
                rfr_cd + rfr_rvcm + rev_cap_lib + f3vi + rpns_exon + rpns_pvce + f3va + f3vz + microentreprise
                )

    class allocations_familiales_imposables(Reform.Variable):
        column = columns.FloatCol
        entity_class = entities.FoyersFiscaux
        label = u"Allocations familiales imposables"

        def function(self, simulation, period):
            period = period.this_year
            af_holder = simulation.calculate_add('af')
            imposition = simulation.legislation_at(period.start).allocations_familiales_imposables.imposition

            af = self.cast_from_entity_to_role(af_holder, entity= "famille", role = QUIFOY['vous'])
            af = self.sum_by_entity(af)
            return period, af * imposition

    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "Intégration au revenu imposable des allocations familiales",
        "children": {
            "imposition": {
                "@type": "Parameter",
                "description": "Indicatrice d'imposition",
                "format": "boolean",
                "values": [{'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': True}],
                },
            },
        }
    reference_legislation_json_copy['children']['allocations_familiales_imposables'] = reform_legislation_subtree
    return reference_legislation_json_copy
