# -*- coding: utf-8 -*-

from openfisca_france.model.base import *
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

    def formula_2014_11(individu, period, parameters):
        stage_duree_heures = individu('stage_duree_heures', period)
        stage_gratification_taux = individu('stage_gratification_taux', period)
        stagiaire = individu('stagiaire', period)
        plafond_securite_sociale_horaire = parameters(period).cotsoc.gen.plafond_securite_sociale_horaire
        stage_gratification_taux_min = parameters(period).cotsoc.stage.taux_gratification_min
        return stagiaire * plafond_securite_sociale_horaire * stage_duree_heures * max_(
            stage_gratification_taux, stage_gratification_taux_min)


class stage_gratification_reintegration(Variable):
    value_type = float
    entity = Individu
    label = u"Part de la gratification de stage réintégrée à l'assiette des cotisations et contributions sociales"
    definition_period = MONTH

    def formula_2014_11(individu, period, parameters):
        stage_duree_heures = individu('stage_duree_heures', period)
        stage_gratification = individu('stage_gratification', period)
        plafond_securite_sociale_horaire = parameters(period).cotsoc.gen.plafond_securite_sociale_horaire
        stage_gratification_taux_min = parameters(period).cotsoc.stage.taux_gratification_min
        stage_gratification_min = plafond_securite_sociale_horaire * stage_duree_heures * stage_gratification_taux_min
        return max_(stage_gratification - stage_gratification_min, 0)


class stagiaire(Variable):
    value_type = bool
    entity = Individu
    label = u"L'individu est stagiaire"
    definition_period = MONTH

    def formula(individu, period, parameters):
        stage_duree_heures = individu('stage_duree_heures', period)
        return (stage_duree_heures > 0)


class exoneration_cotisations_employeur_stagiaire(Variable):
    value_type = float
    entity = Individu
    label = u"Exonrérations de cotisations employeur pour un stagaire"
    reference = "http://www.apce.com/pid2798/stages.html?espace=3"
    definition_period = MONTH

    def formula(individu, period, parameters):
        agirc_employeur = individu('agirc_employeur', period)
        agirc_gmp_employeur = individu('agirc_gmp_employeur', period)
        arrco_employeur = individu('arrco_employeur', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        stage_gratification_reintegration = individu('stage_gratification_reintegration', period)
        stagiaire = individu('stagiaire', period)
        categorie_salarie = individu('categorie_salarie', period)

        bareme_by_type_sal_name = parameters(period).cotsoc.cotisations_employeur
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

    def formula(individu, period, parameters):
        agirc_salarie = individu('agirc_salarie', period)
        agirc_gmp_salarie = individu('agirc_gmp_salarie', period)
        arrco_salarie = individu('arrco_salarie', period)
        plafond_securite_sociale = individu('plafond_securite_sociale', period)
        stage_gratification_reintegration = individu('stage_gratification_reintegration', period)
        stagiaire = individu('stagiaire', period)
        categorie_salarie = individu('categorie_salarie', period)

        bareme_by_type_sal_name = parameters(period).cotsoc.cotisations_salarie
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
