# -*- coding: utf-8 -*-


from __future__ import division

from numpy import maximum as max_, minimum as min_, zeros

from openfisca_france.model.base import *  # noqa analysis:ignore


class apa_domicile(Variable):
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


class apa_etablissement(Variable):
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


class base_ressources_apa(Variable):
    column = FloatCol
    label = u"Base ressources de l'allocation personalisée d'autonomie"
    entity_class = Familles

    def function(self, simulation, period):
        return zeros(self.holder.entity.count)


class gir(Variable):
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
        )
    entity_class = Individus
    label = u"Groupe iso-ressources de l'individu"


class dependance_plan_aide_domicile(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Plan d'aide à domicile pour une personne dépendate"


class dependance_tarif_etablissement_gir_5_6(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Tarif dépendance de l'établissement pour les GIR 5 et 6"


class dependance_tarif_etablissement_gir_dependant(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Tarif dépendance de l'établissement pour le GIR de la personne dépendante"