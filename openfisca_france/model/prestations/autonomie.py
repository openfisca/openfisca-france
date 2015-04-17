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

from numpy import zeros, logical_not as not_, logical_or as or_

from ..base import *  # noqa analysis:ignore


@reference_formula
class apa(SimpleFormulaColumn):
    column = FloatCol
    label = u"Allocation personalisée d'autonomie"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        gir = simulation.calculate('gir', period)
        base_ressources_apa = simulation.calculate('base_ressources_apa', period)
        tarif_dependance_etablissement = simulation.calculate('tarif_dependance_etablissement', pe)
        montant_mensuel_maximum_by_gir = dict(
            gir1 = 1312.67,
            gir2 = 1125.14,
            gir3 = 843.86,
            gir4 = 562.57,
            )
        seuil_non_versement = 28.83
        apa_seuil_1 = 2437.81
        apa_seuil_2 = 3750.48

        participation_beneficiaire = (
            (base_ressources_apa <= apa_seuil_1) * tarif_dependance_etablissement_gir_5_6 +
            max_((base_ressources_apa - apa_seuil_1) / ( apa_seuil_2 - apa_seuil_1), 0)
            )

        return period, montant / 12


@reference_formula
class base_ressources_apa(SimpleFormulaColumn):
    column = FloatCol
    label = u"Base ressources de l'allocation personalisée d'autonomie"
    entity_class = Familles

    def function(self, simulation, period):
        return zeros(self.holder.entity.count)

reference_input_variable(
    column = EnumCol(
        enum = Enum(
            [
                u"Non pertinent",
                u"Gir 1",
                u"Gir 2",
                u"Gir 3",
                u"Gir 4",
                u"Gir 5",
                u"Gir 6",
                ],
            ),
        default = 0,
        ),
    entity_class = Individus,
    label = u"Groupe iso-ressources de l'individu",
    name = "gir",
    )
