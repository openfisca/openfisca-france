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

import logging


from numpy import int16, maximum as max_, minimum as min_, logical_not as not_


from ....base import *  # noqa analysis:ignore
from .base import apply_bareme, apply_bareme_for_relevant_type_sal


log = logging.getLogger(__name__)


# TODO:
# contribution patronale de prévoyance complémentaire
# check hsup everywhere !
# versement transport dépdendant de la localité (décommenter et compléter)


@reference_formula
class assiette_cotisations_sociales(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Assiette des cotisations sociales des salaries"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period(u'month')
        assiette_cotisations_sociales_prive = simulation.calculate('assiette_cotisations_sociales_prive', period)
        assiette_cotisations_sociales_public = simulation.calculate('assiette_cotisations_sociales_public', period)
        stage_gratification_reintegration = simulation.calculate('stage_gratification_reintegration', period)
        return period, (
            assiette_cotisations_sociales_prive +
            assiette_cotisations_sociales_public +
            stage_gratification_reintegration
            )


@reference_formula
class assiette_cotisations_sociales_prive(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Assiette des cotisations sociales des salaries du prive"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period(u'month')
        apprenti = simulation.calculate('apprenti', period)
        avantage_en_nature = simulation.calculate('avantage_en_nature', period)
        hsup = simulation.calculate('hsup', period)
        indemnites_compensatrices_conges_payes = simulation.calculate('indemnites_compensatrices_conges_payes', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        primes_salaires = simulation.calculate('primes_salaires', period)
        reintegration_titre_restaurant_employeur = simulation.calculate(
            "reintegration_titre_restaurant_employeur", period
            )
        remuneration_apprenti = simulation.calculate('remuneration_apprenti', period)
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        type_sal = simulation.calculate('type_sal', period)
        smic_proratise = simulation.calculate('smic_proratise', period)

        assiette = (
            salaire_de_base +
            primes_salaires +
            avantage_en_nature +
            hsup +
            indemnites_compensatrices_conges_payes +
            remuneration_apprenti +
            (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique) +
            reintegration_titre_restaurant_employeur
            )
        return period, max_(assiette, smic_proratise * not_(apprenti)) * (assiette > 0)


@reference_formula
class reintegration_titre_restaurant_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Prise en charge de l'employeur des dépenses de cantine et des titres restaurants non exonérés de charges sociales"  # noqa

    def function(self, simulation, period):
        period = period  # TODO
        valeur_unitaire = simulation.calculate("titre_restaurant_valeur_unitaire", period)
        volume = simulation.calculate("titre_restaurant_volume", period)
        taux_employeur = simulation.calculate('titre_restaurant_taux_employeur', period)
        cantines_titres_restaurants = simulation.legislation_at(
            period.start).cotsoc.assiette.cantines_titres_restaurants

        taux_minimum_exoneration = cantines_titres_restaurants.taux_minimum_exoneration
        taux_maximum_exoneration = cantines_titres_restaurants.taux_maximum_exoneration
        seuil_prix_titre = cantines_titres_restaurants.seuil_prix_titre
        condition_exoneration_taux = (
            (taux_minimum_exoneration <= taux_employeur) *
            (taux_maximum_exoneration >= taux_employeur)
            )
        montant_reintegration = volume * (
            condition_exoneration_taux * max_(valeur_unitaire * taux_employeur - seuil_prix_titre, 0) +
            not_(condition_exoneration_taux) * valeur_unitaire * taux_employeur
            )
        return period, montant_reintegration


# Cotisations proprement dites


@reference_formula
class accident_du_travail(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations employeur accident du travail et maladie professionelle"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        assiette_cotisations_sociales = simulation.calculate(
            'assiette_cotisations_sociales', period)
        taux_accident_travail = simulation.calculate('taux_accident_travail', period)
        type_sal = simulation.calculate('type_sal', period)
        assujetti = type_sal <= 1  # TODO: ajouter contractuel du public salarié de moins d'un an ou à temps partiel
        return period, - assiette_cotisations_sociales * taux_accident_travail * assujetti


@reference_formula
class agff_salarie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation retraite AGFF tranche A (salarié)"
    # AGFF: Association pour la gestion du fonds de financement (sous-entendu des départs entre 60 et 65 ans)

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "salarie",
            bareme_name = "agff",
            variable_name = self.__class__.__name__
            )
        return period, cotisation


@reference_formula
class agff_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation retraite AGFF tranche A (employeur)"
    # TODO: améliorer pour gérer mensuel/annuel

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        assiette_cotisations_sociales = simulation.calculate(
            'assiette_cotisations_sociales', period)
        type_sal = simulation.calculate('type_sal', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)

        law = simulation.legislation_at(period.start)

        cotisation_non_cadre = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = law.cotsoc.cotisations_employeur,
            bareme_name = "agffnc",
            base = assiette_cotisations_sociales,
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )

        cotisation_cadre = apply_bareme_for_relevant_type_sal(
            bareme_by_type_sal_name = law.cotsoc.cotisations_employeur,
            bareme_name = "agffc",
            base = assiette_cotisations_sociales,
            plafond_securite_sociale = plafond_securite_sociale,
            type_sal = type_sal,
            )
        return period, cotisation_cadre + cotisation_non_cadre


@reference_formula
class agirc_gmp_assiette(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Assiette de la cotisation AGIRC pour la garantie minimale de points (GMP,  salarié)"
    # TODO: gestion annuel/mensuel

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        salaire_charniere = simulation.legislation_at(period.start).cotsoc.agirc_gmp.salaire_charniere  # annuel
        assiette = max_(
            (salaire_charniere / 12 - assiette_cotisations_sociales) * (assiette_cotisations_sociales > 0),
            0,
            )
        return period, assiette


@reference_formula
class agirc_gmp_salarie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation AGIRC pour la garantie minimale de points (GMP,  salarié)"
    # TODO: gestion annuel/mensuel

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        agirc_gmp_assiette = simulation.calculate('agirc_gmp_assiette', period)
        agirc_salarie = simulation.calculate('agirc_salarie', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        type_sal = simulation.calculate('type_sal', period)

        law = simulation.legislation_at(period.start).cotsoc.agirc_gmp
        cotisation_forfaitaire = law.cotisation_salarie
        taux = simulation.legislation_at(period.start).cotsoc.cotisations_salarie['prive_cadre']['agirc'].rates[1]

        sous_plafond_securite_sociale = (
            (assiette_cotisations_sociales <= plafond_securite_sociale) & (assiette_cotisations_sociales > 0)
            )
        cotisation = - (
            sous_plafond_securite_sociale * cotisation_forfaitaire +
            not_(sous_plafond_securite_sociale) * agirc_gmp_assiette * taux
            )
        return period, min_((cotisation - agirc_salarie) * (type_sal == 1), 0)  # cotisation are negative


@reference_formula
class agirc_gmp_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation AGIRC pour la garantie minimale de points (GMP, employeur)"
    # TODO: gestion annuel/mensuel

    def function(self, simulation, period):

        period = period.start.period(u'month').offset('first-of')
        agirc_employeur = simulation.calculate('agirc_employeur', period)
        agirc_gmp_assiette = simulation.calculate('agirc_gmp_assiette', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        type_sal = simulation.calculate('type_sal', period)

        law = simulation.legislation_at(period.start).cotsoc.agirc_gmp
        cotisation_forfaitaire = law.cotisation_employeur
        taux = simulation.legislation_at(period.start).cotsoc.cotisations_employeur['prive_cadre']['agirc'].rates[1]

        sous_plafond_securite_sociale = (
            (assiette_cotisations_sociales <= plafond_securite_sociale) & (assiette_cotisations_sociales > 0)
            )
        cotisation = - (
            sous_plafond_securite_sociale * cotisation_forfaitaire +
            not_(sous_plafond_securite_sociale) * agirc_gmp_assiette * taux
            )
        return period, min_((cotisation - agirc_employeur) * (type_sal == 1), 0)  # cotisation are negative


@reference_formula
class agirc_salarie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation AGIRC tranche B (salarié)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "salarie",
            bareme_name = "agirc",
            variable_name = self.__class__.__name__
            )
        type_sal = simulation.calculate('type_sal', period)
        return period, cotisation * (type_sal == 1)


@reference_formula
class agirc_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation AGIRC tranche B (employeur)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation, period,
            cotisation_type = "employeur",
            bareme_name = "agirc",
            variable_name = self.__class__.__name__
            )
        type_sal = simulation.calculate('type_sal', period)
        return period, cotisation * (type_sal == 1)


@reference_formula
class ags(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution à l'association pour la gestion du régime de garantie des créances des salariés (AGS, employeur)"  # noqa analysis:ignore

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation, period,
            cotisation_type = "employeur",
            bareme_name = "chomfg",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


@reference_formula
class apec_salarie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations agence pour l'emploi des cadres (APEC,  salarié)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation, period,
            cotisation_type = "salarie",
            bareme_name = "apec",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation  # TODO: check public notamment contractuel


@reference_formula
class apec_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations Agenece pour l'emploi des cadres (APEC, employeur)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "employeur",
            bareme_name = "apec",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation  # TODO: check public notamment contractuel


@reference_formula
class arrco_salarie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation ARRCO tranche 1 (salarié)"
    # TODO: check gestion mensuel/annuel

    def function(self, simulation, period):
        cotisation_minimale = apply_bareme(
            simulation,
            period,
            cotisation_type = "salarie",
            bareme_name = "arrco",
            variable_name = self.__class__.__name__,
            )
        arrco_tranche_a_taux_salarie = simulation.calculate('arrco_tranche_a_taux_salarie', period)
        assiette_cotisations_sociales = simulation.calculate_add('assiette_cotisations_sociales', period)
        plafond_securite_sociale = simulation.calculate_add('plafond_securite_sociale', period)

        type_sal = simulation.calculate('type_sal', period)
        cotisation_entreprise = - (
            min_(max_(assiette_cotisations_sociales, 0), plafond_securite_sociale) *
            arrco_tranche_a_taux_salarie
            )
        return period, (
            cotisation_minimale * (arrco_tranche_a_taux_salarie == 0) + cotisation_entreprise
            ) * (type_sal <= 1)


@reference_formula
class arrco_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation ARRCO tranche 1 (employeur)"
    # TODO: check gestion mensuel/annuel

    def function(self, simulation, period):
        cotisation_minimale = apply_bareme(
            simulation,
            period,
            cotisation_type = "employeur",
            bareme_name = "arrco",
            variable_name = self.__class__.__name__,
            )
        arrco_tranche_a_taux_employeur = simulation.calculate('arrco_tranche_a_taux_employeur', period)
        assiette_cotisations_sociales = simulation.calculate_add('assiette_cotisations_sociales', period)
        plafond_securite_sociale = simulation.calculate_add('plafond_securite_sociale', period)
        type_sal = simulation.calculate('type_sal', period)

        cotisation_entreprise = - (
            min_(max_(assiette_cotisations_sociales, 0), plafond_securite_sociale) *
            arrco_tranche_a_taux_employeur
            )
        return period, (
            cotisation_minimale * (arrco_tranche_a_taux_employeur == 0) + cotisation_entreprise
            ) * (type_sal <= 1)


@reference_formula
class chomage_salarie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation chômage tranche A (salarié)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "salarie",
            bareme_name = "assedic",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


@reference_formula
class chomage_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation chômage tranche A (employeur)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "employeur",
            bareme_name = "assedic",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


@reference_formula
class contribution_solidarite_autonomie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution solidarité autonomie (employeur)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "employeur",
            bareme_name = "csa",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


@reference_formula
class cotisation_exceptionnelle_temporaire_salarie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation_exceptionnelle_temporaire (employe)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'cet',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


@reference_formula
class cotisation_exceptionnelle_temporaire_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation exceptionnelle temporaire (employeur)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'cet',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


@reference_formula
class famille(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation famille (employeur)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'famille',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


@reference_formula
class mmid_salarie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation maladie (salarié)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'maladie',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


@reference_formula
class mmid_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation maladie (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'maladie',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


# TODO: this formula is used only to check fiche_de_paie from memento
@reference_formula
class mmida_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation maladie (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'maladie',
            variable_name = self.__class__.__name__,
            )
        contribution_solidarite_autonomie = simulation.calculate('contribution_solidarite_autonomie', period)
        return period, cotisation + contribution_solidarite_autonomie


@reference_formula
class mhsup(SimpleFormulaColumn):
    calculate_output = calculate_output_add
    column = FloatCol
    entity_class = Individus
    label = u"Heures supplémentaires comptées négativement"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        hsup = simulation.calculate('hsup', period)

        return period, -hsup


@reference_formula
class plafond_securite_sociale(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Plafond de la securite sociale"
    # TODO gérer les plafonds mensuel, trimestriel, annuel

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        heures_non_remunerees_volume = simulation.calculate('heures_non_remunerees_volume')
        nombre_jours_calendaires = simulation.calculate('nombre_jours_calendaires', period)
        _P = simulation.legislation_at(period.start)

        plafond_temps_plein = _P.cotsoc.gen.plafond_securite_sociale
        jours_travailles = nombre_jours_calendaires - heures_non_remunerees_volume / 7
        plafond_securite_sociale = min_(jours_travailles, 30) / 30 * plafond_temps_plein
        return period, plafond_securite_sociale


@reference_formula
class prevoyance_obligatoire_cadre(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation de prévoyance pour les cadres et assimilés"
    # TODO: gérer le mode de recouvrement et l'aspect mensuel/annuel

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        type_sal = simulation.calculate('type_sal', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        prevoyance_obligatoire_cadre_taux_employeur = simulation.calculate(
            'prevoyance_obligatoire_cadre_taux_employeur', period)

        cotisation = - (
            (type_sal == CAT['prive_cadre']) *
            min_(assiette_cotisations_sociales, plafond_securite_sociale) *
            prevoyance_obligatoire_cadre_taux_employeur
            )
        return period, cotisation


@reference_formula
class taille_entreprise(SimpleFormulaColumn):
    column = EnumCol(
        enum = Enum(
            [
                u"Non pertinent",
                u"Moins de 10 salariés",
                u"De 10 à 19 salariés",
                u"De 20 à 249 salariés",
                u"Plus de 250 salariés",
                ],
            ),
        default = 0,
        )
    entity_class = Individus
    label = u"Catégorie de taille d'entreprise"
    url = u"http://www.insee.fr/fr/themes/document.asp?ref_id=ip1321"

    def function(self, simulation, period):
        period = period
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)

        taille_entreprise = (
            (effectif_entreprise > 0).astype(int16) +
            (effectif_entreprise > 9).astype(int16) +
            (effectif_entreprise > 19).astype(int16) +
            (effectif_entreprise > 249).astype(int16)
            )
        return period, taille_entreprise


@reference_formula
class taux_accident_travail(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Approximation du taux accident à partir de l'exposition au risque donnée"
    start_date = date(2012, 1, 1)

    def function(self, simulation, period):
        period_extract = period.start.period(u'month').offset('first-of')
        exposition_accident = simulation.calculate('exposition_accident', period_extract)
        accident = simulation.legislation_at(period_extract.start).cotsoc.accident

        return period, (exposition_accident == 0) * accident.faible + (exposition_accident == 1) * accident.moyen \
            + (exposition_accident == 2) * accident.eleve + (exposition_accident == 3) * accident.treseleve


@reference_formula
class vieillesse_deplafonnee_salarie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse déplafonnée (salarié)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'vieillesse_deplafonnee',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


@reference_formula
class vieillesse_plafonnee_salarie(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse plafonnée (salarié)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation, period,
            cotisation_type = 'salarie',
            bareme_name = 'vieillesse',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


@reference_formula
class vieillesse_deplafonnee_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse déplafonnée"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period, cotisation_type = 'employeur',
            bareme_name = 'vieillesse_deplafonnee',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


@reference_formula
class vieillesse_plafonnee_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse plafonnée (employeur)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period, cotisation_type = 'employeur',
            bareme_name = 'vieillesse_plafonnee',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation
