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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from .base import *  # noqa


@reference_formula
class tns_total_revenus(DatedFormulaColumn):
    column = FloatCol
    label = u"Total des revenus non salariés"
    entity_class = Individus
#    start = "2008-01-01"

    @dated_function(date(2008, 1, 1))
    def function_2008__(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        tns_autres_revenus = simulation.calculate('tns_autres_revenus', period)
        tns_type_structure = simulation.calculate('tns_type_structure', period)
        tns_type_activite = simulation.calculate('tns_type_activite', period)
        tns_chiffre_affaires_micro_entreprise = simulation.calculate('tns_chiffre_affaires_micro_entreprise', period)
        bareme = simulation.legislation_at(period.start).tns

        cs_ae = bareme.auto_entrepreneur
        abatt_fp_me = bareme.micro_entreprise.abattement_forfaitaire_fp

        total_revenus = (
            tns_autres_revenus / 12 +
            # cas des auto-entrepreneurs
            (tns_type_structure == 0) * tns_chiffre_affaires_micro_entreprise / 12 * (
                1 -
                (tns_type_activite == 0) * cs_ae.achat_revente -
                (tns_type_activite == 1) * cs_ae.bic -
                (tns_type_activite == 2) * cs_ae.bnc) +
            # cas des autres micro-entreprises
            (tns_type_structure == 1) * tns_chiffre_affaires_micro_entreprise / 12 * (
                1 -
                (tns_type_activite == 0) * abatt_fp_me.achat_revente -
                (tns_type_activite == 1) * abatt_fp_me.bic -
                (tns_type_activite == 2) * abatt_fp_me.bnc
                ) * (1 - bareme.micro_entreprise.cotisations_sociales)
            )

        return period, total_revenus

