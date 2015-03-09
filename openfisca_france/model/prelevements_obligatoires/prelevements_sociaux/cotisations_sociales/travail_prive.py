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
taux_versement_transport_by_localisation_entreprise = None


# TODO:
# contribution patronale de prévoyance complémentaire
# check hsup everywhere !
# versement transport dépdendant de la localité (décommenter et compléter)


# Cotisations proprement dites


@reference_formula
class accident_du_travail(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations patronales accident du travail et maladie professionelle"

    def function(self, simulation, period):
        assiette_cotisations_sociales = simulation.calculate(
            'assiette_cotisations_sociales', period)
        taux_accident_travail = simulation.calculate('taux_accident_travail', period)
        type_sal = simulation.calculate('type_sal', period)
        assujetti = type_sal <= 1  # TODO: ajouter contractuel du public salarié de moins d'un an ou à temps partiel
        return period, - assiette_cotisations_sociales * taux_accident_travail * assujetti


@reference_formula
class agff_tranche_a_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation retraite AGFF tranche A (employé)"

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
class agff_tranche_a_employeur(SimpleFormulaColumn):
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
class agirc_gmp_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation AGIRC pour la garantie minimale de points (GMP, employé)"
    # TODO: gestion annuel/mensuel

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        law = simulation.legislation_at(period.start).cotsoc.agirc_gmp
        taux = simulation.legislation_at(period.start).cotsoc.cotisations_salarie['prive_cadre']['agirc'].rates[1]
        salaire_charniere = law.salaire_charniere  # annuel
        cotisation_forfaitaire = law.cotisation_salarie

        sous_plafond_securite_sociale = (assiette_cotisations_sociales <= plafond_securite_sociale)
        cotisation = - (
            sous_plafond_securite_sociale * cotisation_forfaitaire +
            not_(sous_plafond_securite_sociale) * (salaire_charniere / 12 - assiette_cotisations_sociales) * taux
            ) * (assiette_cotisations_sociales > 0)
        return period, cotisation


@reference_formula
class agirc_gmp_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation AGIRC pour la garantie minimale de points (GMP, employeur)"
    # TODO: gestion annuel/mensuel

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)
        law = simulation.legislation_at(period.start).cotsoc.agirc_gmp
        taux = simulation.legislation_at(period.start).cotsoc.cotisations_employeur['prive_cadre']['arrco'].rates[1]
        salaire_charniere = law.salaire_charniere  # annuel
        cotisation_forfaitaire = law.cotisation_employeur

        sous_plafond_securite_sociale = (assiette_cotisations_sociales <= plafond_securite_sociale)
        cotisation = - (
            sous_plafond_securite_sociale * cotisation_forfaitaire +
            not_(sous_plafond_securite_sociale) * (salaire_charniere / 12 - assiette_cotisations_sociales) * taux
            ) * (assiette_cotisations_sociales > 0)
        return period, cotisation


@reference_formula
class agirc_tranche_b_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation AGIRC tranche B (employé)"

    def function(self, simulation, period):
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "salarie",
            bareme_name = "agirc",
            variable_name = self.__class__.__name__
            )
        gmp_employe = simulation.calculate('agirc_gmp_employe', period)
        type_sal = simulation.calculate('type_sal', period)
        return period, cotisation + gmp_employe * (cotisation == 0) * (type_sal == 1)


@reference_formula
class agirc_tranche_b_employeur(SimpleFormulaColumn):
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
        gmp_employeur = simulation.calculate('agirc_gmp_employeur', period)
        type_sal = simulation.calculate('type_sal', period)
        return period, cotisation + gmp_employeur * (cotisation == 0) * (type_sal == 1)


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
class apec_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations agence pour l'emploi des cadres (APEC, employé)"

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
class arrco_tranche_a_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation ARRCO tranche A (employé)"
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
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        plafond_securite_sociale = simulation.calculate('plafond_securite_sociale', period)

        type_sal = simulation.calculate('type_sal', period)
        cotisation_entreprise = - (
            min_(max_(assiette_cotisations_sociales, 0), plafond_securite_sociale) *
            arrco_tranche_a_taux_salarie
            )
        return period, (
            cotisation_minimale * (arrco_tranche_a_taux_salarie == 0) + cotisation_entreprise
            ) * (type_sal <= 1)


@reference_formula
class arrco_tranche_a_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation ARRCO tranche A (employeur)"

    def function(self, simulation, period):
        cotisation_minimale = apply_bareme(simulation, period, cotisation_type = "employeur", bareme_name = "arrco")
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
class assedic_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation chômage tranche A (employé)"

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
class assedic_employeur(SimpleFormulaColumn):
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
class cotisation_exceptionnelle_temporaire_employe(SimpleFormulaColumn):
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
class maladie_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation maladie (employé)"

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
class maladie_employeur(SimpleFormulaColumn):
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


@reference_formula
class mhsup(SimpleFormulaColumn):
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
    label = u"Catégode taille d'entreprise (pour calcul des cotisations sociales)"
    url = u"http://www.insee.fr/fr/themes/document.asp?ref_id=ip1321"

    def function(self, simulation, period):
        period = period
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)

        taille_entreprise = (
            (effectif_entreprise > 0).astype(int16) +
            (effectif_entreprise > 10).astype(int16) +
            (effectif_entreprise > 20).astype(int16) +
            (effectif_entreprise > 250).astype(int16)
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
class vieillesse_deplafonnee_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse déplafonnée (employé)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'salarie',
            bareme_name = 'vieillessedeplaf',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


@reference_formula
class vieillesse_plafonnee_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation vieillesse plafonnée (employé)"

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
            bareme_name = 'vieillessedeplaf',
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
            bareme_name = 'vieillesseplaf',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation
