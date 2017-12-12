# -*- coding: utf-8 -*-

from __future__ import division


from openfisca_france.model.base import *  # noqa analysis:ignore
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.base import apply_bareme_for_relevant_type_sal


class stage_duree_heures(Variable):
    value_type = int
    entity = Individu
    label = u"Nombre d'heures effectuées en stage"
    definition_period = MONTH


class stage_gratification_taux(Variable):
    value_type = float
    entity = Individu
    label = u"Taux de gratification (en plafond de la Sécurité sociale)"
    definition_period = MONTH


class stage_gratification(Variable):
    value_type = float
    entity = Individu
    label = u"Gratification de stage"
    definition_period = MONTH

    def formula_2014_11(self, simulation, period):
        stage_duree_heures = simulation.calculate('stage_duree_heures', period)
        stage_gratification_taux = simulation.calculate('stage_gratification_taux', period)
        stagiaire = simulation.calculate('stagiaire', period)
        plafond_securite_sociale_horaire = simulation.parameters_at(period.start).cotsoc.gen.plafond_securite_sociale_horaire
        stage_gratification_taux_min = simulation.parameters_at(period.start).cotsoc.stage.taux_gratification_min
        return stagiaire * plafond_securite_sociale_horaire * stage_duree_heures * max_(
            stage_gratification_taux, stage_gratification_taux_min)


class stage_gratification_reintegration(Variable):
    value_type = float
    entity = Individu
    label = u"Part de la gratification de stage réintégrée à l'assiette des cotisations et contributions sociales"
    definition_period = MONTH

    def formula_2014_11(self, simulation, period):
        stage_duree_heures = simulation.calculate('stage_duree_heures', period)
        stage_gratification = simulation.calculate('stage_gratification', period)
        plafond_securite_sociale_horaire = simulation.parameters_at(period.start).cotsoc.gen.plafond_securite_sociale_horaire
        stage_gratification_taux_min = simulation.parameters_at(period.start).cotsoc.stage.taux_gratification_min
        stage_gratification_min = plafond_securite_sociale_horaire * stage_duree_heures * stage_gratification_taux_min
        return max_(stage_gratification - stage_gratification_min, 0)


class stagiaire(Variable):
    value_type = bool
    entity = Individu
    label = u"L'individu est stagiaire"
    definition_period = MONTH

    def formula(self, simulation, period):
        stage_duree_heures = simulation.calculate('stage_duree_heures', period)
        return (stage_duree_heures > 0)


class exoneration_cotisations_employeur_stagiaire(Variable):
    value_type = float
    entity = Individu
    label = u"Exonrérations de cotisations employeur pour un stagaire"
    reference = "http://www.apce.com/pid2798/stages.html?espace=3"
    definition_period = MONTH

    def formula(self, simulation, period):
        agirc_employeur = simulation.calculate('agirc_employeur', period)
        agirc_gmp_employeur = simulation.calculate('agirc_gmp_employeur', period)
        arrco_employeur = simulation.calculate('arrco_employeur', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        stage_gratification_reintegration = simulation.calculate('stage_gratification_reintegration', period)
        stagiaire = simulation.calculate('stagiaire', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)

        bareme_by_type_sal_name = simulation.parameters_at(period.start).cotsoc.cotisations_employeur
        exoneration = sum(
            apply_bareme_for_relevant_type_sal(
                bareme_by_type_sal_name = bareme_by_type_sal_name,
                bareme_name = bareme_name,
                categorie_salarie = categorie_salarie,
                base = stage_gratification_reintegration,
                plafond_securite_sociale = plafond_securite_sociale,
                round_base_decimals = 2,
                )
            for bareme_name in ['agffnc', 'agffc', 'chomfg', 'assedic']
            )
        exoneration += agirc_employeur + agirc_gmp_employeur + arrco_employeur
        return - exoneration * stagiaire


class exoneration_cotisations_salarie_stagiaire(Variable):
    value_type = float
    entity = Individu
    label = u"Exonrérations de cotisations salarié pour un stagiaire"
    reference = "http://www.apce.com/pid2798/stages.html?espace=3"
    definition_period = MONTH

    def formula(self, simulation, period):
        agirc_salarie = simulation.calculate('agirc_salarie', period)
        agirc_gmp_salarie = simulation.calculate('agirc_gmp_salarie', period)
        arrco_salarie = simulation.calculate('arrco_salarie', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        stage_gratification_reintegration = simulation.calculate('stage_gratification_reintegration', period)
        stagiaire = simulation.calculate('stagiaire', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)

        bareme_by_type_sal_name = simulation.parameters_at(period.start).cotsoc.cotisations_salarie
        bareme_names = ['agff', 'assedic']

        exoneration = plafond_securite_sociale * 0.0
        for bareme_name in bareme_names:
            exoneration += apply_bareme_for_relevant_type_sal(
                bareme_by_type_sal_name = bareme_by_type_sal_name,
                bareme_name = bareme_name,
                categorie_salarie = categorie_salarie,
                base = stage_gratification_reintegration,
                plafond_securite_sociale = plafond_securite_sociale,
                round_base_decimals = 2,
                )
        exoneration = exoneration + agirc_salarie + agirc_gmp_salarie + arrco_salarie

        return - exoneration * stagiaire
