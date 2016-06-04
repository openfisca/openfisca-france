# -*- coding: utf-8 -*-

from __future__ import division


from numpy import maximum as max_


from ....base import *  # noqa analysis:ignore
from .base import apply_bareme_for_relevant_type_sal


class stage_duree_heures(Variable):
    column = IntCol()
    entity_class = Individus
    label = u"Nombre d'heures effectuées en stage"


class stage_gratification_taux(Variable):
    column = FloatCol()
    entity_class = Individus
    label = u"Taux de gratification (en plafond de la Sécurité sociale)"


class stage_gratification(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Gratification de stage"
    start_date = date(2014, 11, 1)  # TODO: remove when updating legislation backwards

    def function(self, simulation, period):
        period = period.this_month
        stage_duree_heures = simulation.calculate('stage_duree_heures', period)
        stage_gratification_taux = simulation.calculate('stage_gratification_taux', period)
        stagiaire = simulation.calculate('stagiaire', period)
        plafond_securite_sociale_horaire = simulation.legislation_at(period.start).cotsoc.gen.plafond_securite_sociale_horaire
        # TODO: move to legislation parameters file
        stage_gratification_taux_min = .1375  # depuis le 1er décembre 2014
        # .15 à partir de 2015-09-01
        return period, stagiaire * plafond_securite_sociale_horaire * stage_duree_heures * max_(
            stage_gratification_taux, stage_gratification_taux_min)


class stage_gratification_reintegration(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Part de la gratification de stage réintégrée à l'assiette des cotisations et contributions sociales"
    start_date = date(2014, 11, 1)  # TODO: remove when updating legislation backwards

    def function(self, simulation, period):
        period = period.this_month
        stage_duree_heures = simulation.calculate('stage_duree_heures', period)
        stage_gratification = simulation.calculate('stage_gratification', period)
        plafond_securite_sociale_horaire = (
            simulation.legislation_at(period.start).cotsoc.gen.plafond_securite_sociale_horaire)
        # TODO: move to legislation parameters file
        stage_gratification_taux_min = .1375  # .15 à partir de 2015-09-01  
        stage_gratification_min = plafond_securite_sociale_horaire * stage_duree_heures * stage_gratification_taux_min
        return period, max_(stage_gratification - stage_gratification_min, 0)


class stagiaire(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"L'individu est stagiaire"

    def function(self, simulation, period):
        period = period.this_month
        stage_duree_heures = simulation.calculate('stage_duree_heures', period)
        return period, (stage_duree_heures > 0)


class exoneration_cotisations_employeur_stagiaire(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Exonrérations de cotisations employeur pour un stagaire"
    url = "http://www.apce.com/pid2798/stages.html?espace=3"

    def function(self, simulation, period):
        period = period.this_month
        agirc_employeur = simulation.calculate('agirc_employeur', period)
        agirc_gmp_employeur = simulation.calculate('agirc_gmp_employeur', period)
        arrco_employeur = simulation.calculate('arrco_employeur', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        stage_gratification_reintegration = simulation.calculate('stage_gratification_reintegration', period)
        stagiaire = simulation.calculate('stagiaire', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)

        bareme_by_type_sal_name = simulation.legislation_at(period.start).cotsoc.cotisations_employeur
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
        return period, - exoneration * stagiaire


class exoneration_cotisations_salarie_stagiaire(Variable):
    column = FloatCol
    entity_class = Individus
    label = u"Exonrérations de cotisations salarié pour un stagiaire"
    url = "http://www.apce.com/pid2798/stages.html?espace=3"

    def function(self, simulation, period):
        period = period.this_month
        agirc_salarie = simulation.calculate('agirc_salarie', period)
        agirc_gmp_salarie = simulation.calculate('agirc_gmp_salarie', period)
        arrco_salarie = simulation.calculate('arrco_salarie', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        stage_gratification_reintegration = simulation.calculate('stage_gratification_reintegration', period)
        stagiaire = simulation.calculate('stagiaire', period)
        categorie_salarie = simulation.calculate('categorie_salarie', period)

        bareme_by_type_sal_name = simulation.legislation_at(period.start).cotsoc.cotisations_salarie
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

        return period, - exoneration * stagiaire
