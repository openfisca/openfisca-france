# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import division

from numpy import (zeros, maximum as max_, minimum as min_, logical_not as not_)

from openfisca_core.accessors import law
from openfisca_core.columns import BoolCol, FloatCol
from openfisca_core.formulas import SimpleFormulaColumn

from .base import QUIFAM, QUIFOY, reference_formula
from ..entities import Individus

CHEF = QUIFAM['chef']
PART = QUIFAM['part']
ENFS = [QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'], QUIFAM['enf8'], QUIFAM['enf9'], ]
VOUS = QUIFOY['vous']


@reference_formula
class tns_total_revenus(SimpleFormulaColumn):
    column = FloatCol
    label = u"Total des revenus non salariés"
    entity_class = Individus
    period_unit = 'month'

    def function(self, tns_autres_revenus, tns_type_structure, tns_type_activite, tns_chiffre_affaires_micro_entreprise, bareme = law.tns):
        cs_ae = bareme.auto_entrepreneur
        abatt_fp_me = bareme.micro_entreprise.abattement_forfaitaire_fp

        out = (tns_autres_revenus / 12 +
            # cas des auto-entrepreneurs
            (tns_type_structure == 0) * tns_chiffre_affaires_micro_entreprise / 12 * (1 -
                (tns_type_activite == 0) * cs_ae.achat_revente -
                (tns_type_activite == 1) * cs_ae.bic -
                (tns_type_activite == 2) * cs_ae.bnc) +
            # cas des autres micro-entreprises
            (tns_type_structure == 1) * (1 - bareme.micro_entreprise.cotisations_sociales) * tns_chiffre_affaires_micro_entreprise * (
                (tns_type_activite == 0) * abatt_fp_me.achat_revente +
                (tns_type_activite == 1) * abatt_fp_me.bic +
                (tns_type_activite == 2) * abatt_fp_me.bnc))

        return out

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')
