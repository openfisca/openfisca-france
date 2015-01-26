# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

import copy

from numpy import maximum as max_
import logging

from openfisca_core import columns, formulas, reforms
from openfisca_france.model.impot_revenu import ir
from openfisca_france import entities


log = logging.getLogger(__name__)

from openfisca_france.model.base import QUIFOY
VOUS = QUIFOY['vous']


class rbg(formulas.SimpleFormulaColumn):
    label = u"Nouveau revenu brut global intégrant les allocations familiales"
    reference = ir.rbg

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        allocations_familiales_imposables = simulation.calculate('allocations_familiales_imposables', period)
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


class rfr(formulas.SimpleFormulaColumn):
    label = u"Nouveau revenu fiscal de référence intégrant les allocations familiales"
    reference = ir.rfr

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')

        allocations_familiales_imposables = simulation.calculate('allocations_familiales_imposables')
        f3va_holder = simulation.calculate('f3va')
        f3vi_holder = simulation.calculate('f3vi')
        f3vz = simulation.calculate('f3vz')
        rfr_cd = simulation.calculate('rfr_cd')
        rfr_rvcm = simulation.calculate('rfr_rvcm')
        rni = simulation.calculate('rni')
        rpns_exon_holder = simulation.calculate('rpns_exon')
        rpns_pvce_holder = simulation.calculate('rpns_pvce')
        rev_cap_lib = simulation.calculate('rev_cap_lib')
        microentreprise = simulation.calculate('microentreprise')

        f3va = self.sum_by_entity(f3va_holder)
        f3vi = self.sum_by_entity(f3vi_holder)
        rpns_exon = self.sum_by_entity(rpns_exon_holder)
        rpns_pvce = self.sum_by_entity(rpns_pvce_holder)

        return period, (
            max_(0, rni - allocations_familiales_imposables) +
            rfr_cd + rfr_rvcm + rev_cap_lib + f3vi + rpns_exon + rpns_pvce + f3va + f3vz + microentreprise
            )


class allocations_familiales_imposables(formulas.SimpleFormulaColumn):
    column = columns.FloatCol
    entity_class = entities.FoyersFiscaux
    label = u"Allocations familiales imposables"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'year').period('year')
        af_holder = simulation.calculate('af')
        imposition = simulation.legislation_at(period.start).allocations_familiales_imposables.imposition

        af = self.cast_from_entity_to_role(af_holder, entity= "famille", role = VOUS)
        af = self.sum_by_entity(af)
        return period, af * imposition


# Reform legislation

reform_legislation_subtree = {
    "allocations_familiales_imposables": {
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
        },
    }


# Build function

def build_reform(tax_benefit_system):
    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)
    reform_legislation_json['children'].update(reform_legislation_subtree)

    return reforms.make_reform(
        legislation_json = reform_legislation_json,
        name = u'Allocations familiales imposables',
        new_formulas = (rbg, rfr, allocations_familiales_imposables),
        reference = tax_benefit_system,
        )
