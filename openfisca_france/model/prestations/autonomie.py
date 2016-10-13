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

from numpy import maximum as max_, minimum as min_, zeros

from openfisca_france.model.base import *  # noqa analysis:ignore


@reference_formula
class apa_domicile(SimpleFormulaColumn):
    column = FloatCol
    label = u"Allocation personalisée d'autonomie"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        gir = simulation.calculate('gir', period)
        base_ressources_apa = simulation.calculate('base_ressources_apa', period)
        dependance_plan_aide_domicile = simulation.calculate('dependance_plan_aide_domicile', period)

        # TODO: fill the parameters file. May be should use the majoration pour tierce personne as parameter
        montant_mensuel_maximum_by_gir = dict(
            gir1 = 1312.67,
            gir2 = 1125.14,
            gir3 = 843.86,
            gir4 = 562.57,
            )
        seuil_non_versement = 28.83
        apa_seuil_1 = 2437.81
        apa_seuil_2 = 3750.48

        dependance_plan_aide_domicile_maximal = zeros(self.holder.entity.count)
        girs = ['gir' + i for i in rang(1, 5)]
        for target_gir in girs:
            dependance_plan_aide_domicile_maximal = dependance_plan_aide_domicile_maximal + (gir == target_gir) * max_(
                dependance_plan_aide_domicile,
                montant_mensuel_maximum_by_gir[target_gir]
                )

        participation_beneficiaire = dependance_plan_aide_domicile_maximal * .9 * (
            (base_ressources_apa <= apa_seuil_1) +
            min_(
                max_(
                    (base_ressources_apa - apa_seuil_1) / (apa_seuil_2 - apa_seuil_1),
                    0,
                    ),
                1,
                )
            )
        apa = dependance_plan_aide_domicile_maximal - participation_beneficiaire
        return period, apa * (apa >= seuil_non_versement)


@reference_formula
class apa_etablissement(SimpleFormulaColumn):
    column = FloatCol
    label = u"Allocation personalisée d'autonomie"
    entity_class = Familles

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        gir = simulation.calculate('gir', period)
        base_ressources_apa = simulation.calculate('base_ressources_apa', period)
        dependance_tarif_etablissement_gir_5_6 = simulation.calculate('dependance_tarif_etablissement_gir_5_6', period)
        dependance_tarif_etablissement_gir_dependant = simulation.calculate(
            'dependance_tarif_etablissement_gir_dependant', period)

        # TODO: fill the parameters file. May be should use the majoration pour tierce personne as parameter
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
            dependance_tarif_etablissement_gir_5_6 +
            dependance_tarif_etablissement_gir_dependant * (
                (base_ressources_apa <= apa_seuil_1) +
                .8 * min_(
                    max_(
                        (base_ressources_apa - apa_seuil_1) / (apa_seuil_2 - apa_seuil_1),
                        0,
                        ),
                    1,
                    )
                )
            )
        apa = zeros(self.holder.entity.count)
        girs = ['gir' + i for i in rang(1, 5)]
        for target_gir in girs:
            apa = apa + (gir == target_gir) * max_(
                dependance_tarif_etablissement_gir_5_6 + dependance_tarif_etablissement_gir_dependant
                - participation_beneficiaire,
                montant_mensuel_maximum_by_gir[target_gir]
                )

        return period, apa * (apa >= seuil_non_versement)


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


reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = u"Plan d'aide à domicile pour une personne dépendate",
    name = "dependance_plan_aide_domicile",
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = u"Tarif dépendance de l'établissement pour les GIR 5 et 6",
    name = "dependance_tarif_etablissement_gir_5_6",
    )

reference_input_variable(
    column = FloatCol,
    entity_class = Individus,
    label = u"Tarif dépendance de l'établissement pour le GIR de la personne dépendante",
    name = "dependance_tarif_etablissement_gir_dependant",
    )
