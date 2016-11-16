# -*- coding: utf-8 -*-


from __future__ import division

from numpy import maximum as max_, minimum as min_, zeros, select

from openfisca_france.model.base import *  # noqa analysis:ignore


# TODO: fill the parameters file. May be should use the majoration pour tierce personne as parameter
apa_age_min = 60
apa_seuil_dom_1 = .67
apa_seuil_dom_2 = 2.67
apa_seuil_etab_1 = 2.21
apa_seuil_etab_2 = 3.40
majoration_tierce_personne = 1103.08
montant_mensuel_maximum_by_gir = {
    1: 1312.67,
    2: 1125.14,
    3: 843.86,
    4: 562.57,
    }
seuil_non_versement = 28.83
taux_max_participation = .9
taux_reste_a_vivre = 0.10
seuil_fraction_plan_aide_1 = 0.317 * majoration_tierce_personne
seuil_fraction_plan_aide_2 = 0.498 * majoration_tierce_personne


class apa_domicile_participation(DatedVariable):
    column = FloatCol
    label = u"Participation du bénéficiaire de l'APA à domicile"
    entity_class = Individus

    @dated_function(start = date(2002, 1, 1), stop = date(2016, 2, 29))
    def function_2002_20160229(self, simulation, period):
        # Les départements doivent appliquer la nouvelle formule
        # entre le 1er mars 2016 et le 28 février 2017
        base_ressources_apa = simulation.calculate('base_ressources_apa', period)
        dependance_plan_aide_domicile = simulation.calculate('dependance_plan_aide_domicile', period)
        dependance_plan_aide_domicile_accepte = zeros(self.holder.entity.count)
        seuil_inferieur = simulation.legislation_at(period.start).apa_domicile.seuil_de_revenu_en_part_du_mtp.seuil_inferieur
        seuil_superieur = simulation.legislation_at(period.start).apa_domicile.seuil_de_revenu_en_part_du_mtp.seuil_superieur
        majoration_tierce_personne = simulation.legislation_at(period.start).dependance.apa_domicile.mtp

        condition_ressources_domicile = [
            base_ressources_apa <= seuil_inferieur * majoration_tierce_personne,
            seuil_inferieur * majoration_tierce_personne < base_ressources_apa <= seuil_superieur * majoration_tierce_personne,
            base_ressources_apa > seuil_superieur * majoration_tierce_personne,
            ]
        taux_participation = [
            taux_min_participation,
            ( base_ressources_apa - seuil_inferieur * majoration_tierce_personne ) / ( (seuil_superieur - seuil_inferieur) * majoration_tierce_personne) * taux_max_participation,
            taux_max_participation,
            ]
        
        apa_domicile_participation = select(condition_ressources_domicile, taux_participation) * dependance_plan_aide_domicile


        return period, apa_domicile_participation


    @dated_function(start = date(2016, 3, 1))
    def function_20160301(self, simulation, period):
        # Les départements doivent appliquer la nouvelle formule
        # entre le 1er mars 2016 et le 28 février 2017
        base_ressources_apa = simulation.calculate('base_ressources_apa', period)
        dependance_plan_aide_domicile = simulation.calculate('dependance_plan_aide_domicile', period)
        dependance_plan_aide_domicile_accepte = zeros(self.holder.entity.count)
        majoration_tierce_personne = simulation.legislation_at(period.start).dependance.apa_domicile.mtp

        # TODO: use a marignal tax scale
        condlist = [
            dependance_plan_aide_domicile_accepte <= (0.317 * majoration_tierce_personne),
            (0.317 * majoration_tierce_personne) <= dependance_plan_aide_domicile_accepte <= (0.498 * majoration_tierce_personne),
            dependance_plan_aide_domicile_accepte >= (0.498 * majoration_tierce_personne),
            ]
        choicelist_1 = [
            dependance_plan_aide_domicile_accepte,
            0.317 * majoration_tierce_personne,
            0.317 * majoration_tierce_personne,
            ]
        choicelist_2 = [
            0,
            dependance_plan_aide_domicile_accepte - 0.317 * majoration_tierce_personne,
            0.498 * majoration_tierce_personne,
            ]
        choicelist_3 = [
            0,
            0,
            dependance_plan_aide_domicile_accepte - 0.815 * majoration_tierce_personne
            ]
        A_1 = select(condlist, choicelist_1)
        A_2 = select(condlist, choicelist_2)
        A_3 = select(condlist, choicelist_3)

        apa_domicile_participation = (
            0.9 *
            (base_ressources_apa - 0.725 * majoration_tierce_personne) / (1.945 * majoration_tierce_personne) *
            (
                A_1 +
                A_2 * (
                    (1 - 0.4) * base_ressources_apa / (1.945 * majoration_tierce_personne) +
                    (0.4 * 2.67 * majoration_tierce_personne - 0.725 * majoration_tierce_personne) / (1.945 * majoration_tierce_personne)
                    ) +
                A_3 * (
                    (1 - 0.2) * base_ressources_apa / (1.945 * majoration_tierce_personne) +
                    (0.2 * 2.67 * majoration_tierce_personne - 0.725 * majoration_tierce_personne) / (1.945 * majoration_tierce_personne)
                    )
                )
            )

        return period, apa_domicile_participation


class apa_domicile(Variable):
    column = FloatCol
    label = u"Allocation personalisée d'autonomie"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age = simulation.calculate('age', period)
        dependance_plan_aide_domicile = simulation.calculate('dependance_plan_aide_domicile', period)
        gir = simulation.calculate('gir', period)
        plafond_gir1 = simulation.legislation_at(period.start).apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_1
        plafond_gir2 = simulation.legislation_at(period.start).apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_2
        plafond_gir3 = simulation.legislation_at(period.start).apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_3
        plafond_gir4 = simulation.legislation_at(period.start).apa_domicile.plafond_de_l_apa_a_domicile_en_part_du_mtp.gir_4
        apa_domicile_participation = simulation.calculate('apa_domicile_participation', period)

        condition_plafond_par_gir = [
            gir = 1,
            gir = 2,
            gir = 3,
            gir = 4,
            ]
        valeur_plafond_par_gir = [
            plafond_gir1 * majoration_tierce_personne,
            plafond_gir2 * majoration_tierce_personne,
            plafond_gir3 * majoration_tierce_personne,
            plafond_gir4 * majoration_tierce_personne,
            ]
        plafond_par_gir = select(condition_plafond_par_gir, valeur_plafond_par_gir)

        dependance_plan_aide_domicile_accepte = min_(plafond_par_gir, dependance_plan_aide_domicile)

        apa = dependance_plan_aide_domicile_accepte - apa_domicile_participation
        return period, apa * (apa >= seuil_non_versement) * (age >= apa_age_min)


class apa_etablissement(Variable):
    column = FloatCol
    label = u"Allocation personalisée d'autonomie en institution"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        age = simulation.calculate('age', period)
        gir = simulation.calculate('gir', period)
        base_ressources_apa = simulation.calculate('base_ressources_apa', period)
        dependance_tarif_etablissement_gir_5_6 = simulation.calculate('dependance_tarif_etablissement_gir_5_6', period)
        dependance_tarif_etablissement_gir_dependant = simulation.calculate(
            'dependance_tarif_etablissement_gir_dependant', period)
        conditions_ressources = [
            base_ressources_apa <= 2.21 * majoration_tierce_personne,
            2.21 * majoration_tierce_personne < base_ressources_apa <= 3.40 * majoration_tierce_personne,
            base_ressources_apa > 3.40 * majoration_tierce_personne
            ]
        participations = [
            dependance_tarif_etablissement_gir_5_6,
            (
                dependance_tarif_etablissement_gir_5_6 +
                (dependance_tarif_etablissement_gir_dependant - dependance_tarif_etablissement_gir_5_6) * (
                    (base_ressources_apa - 2.21 * majoration_tierce_personne) / 
                    (1.19 * majoration_tierce_personne) * 0.80
                    )
                ),
            dependance_tarif_etablissement_gir_5_6 + (
                dependance_tarif_etablissement_gir_dependant - dependance_tarif_etablissement_gir_5_6) * 0.80
            ]
        participation_beneficiaire = select(conditions_ressources, participations)
        participation_beneficiaire = min_(
            participation_beneficiaire, 
            max_(base_ressources_apa * (1 - taux_reste_a_vivre), 0)
            )
        apa = dependance_tarif_etablissement_gir_dependant - participation_beneficiaire

        eligibilite_etablissement = (
            (dependance_tarif_etablissement_gir_5_6 > 0) *
            (dependance_tarif_etablissement_gir_dependant > 0)
            )

        return period, apa * (apa >= seuil_non_versement) * eligibilite_etablissement * (age >= apa_age_min)


class base_ressources_apa(Variable):
    column = FloatCol
    label = u"Base ressources de l'allocation personalisée d'autonomie"
    entity_class = Familles

    def function(self, simulation, period):
        return period, zeros(self.holder.entity.count)


class gir(Variable):
    column = EnumCol(
        enum = Enum(
            [
                u"Non défini",
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

class apa_urgence_domicile(Variable):
    column = FloatCol
    label = u"Allocation personalisée d'autonomie en institution"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        apa_urgence_domicile = 
            0.5 * 

class apa_urgence_institution(Variable):
    column = FloatCol
    label = u"Allocation personalisée d'autonomie en institution"
    entity_class = Individus

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')