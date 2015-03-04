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


from numpy import int16, maximum as max_, minimum as min_, logical_not as not_, ones, round as round_
from openfisca_core.enumerations import Enum
from openfisca_core.columns import EnumCol, FloatCol
from openfisca_core.formulas import DatedFormulaColumn, SimpleFormulaColumn


from ..base import *  # noqa analysis:ignore
from .base import apply_bareme_for_relevant_type_sal


log = logging.getLogger(__name__)
taux_versement_transport_by_localisation_entreprise = None


# TODO:
# contribution patronale de prévoyance complémentaire
# check hsup everywhere !
# versement transport dépdendant de la localité (décommenter et compléter)

# Helpers

def apply_bareme(simulation, period, cotisation_type = None, bareme_name = None, variable_name = None):
    # period = period.start.offset('first-of', 'month').period('month')
    cotisation_mode_recouvrement = simulation.calculate('cotisation_sociale_mode_recouvrement', period)
    cotisation = (
        # en fin d'année
        cotisation_mode_recouvrement == 1) * (
            compute_cotisation_annuelle(
                simulation,
                period,
                cotisation_type = cotisation_type,
                bareme_name = bareme_name,
                )
            ) + (
        # anticipé
        cotisation_mode_recouvrement == 0) * (
            compute_cotisation_anticipee(
                simulation,
                period,
                cotisation_type = cotisation_type,
                bareme_name = bareme_name,
                variable_name = variable_name,
                )
            )
    return cotisation


def compute_cotisation(simulation, period, cotisation_type = None, bareme_name = None):

    assert cotisation_type is not None
    law = simulation.legislation_at(period.start)
    if cotisation_type == "employeur":
        bareme_by_type_sal_name = law.cotsoc.cotisations_employeur
    elif cotisation_type == "salarie":
        bareme_by_type_sal_name = law.cotsoc.cotisations_salarie
    assert bareme_name is not None

    assiette_cotisations_sociales = simulation.calculate_add('assiette_cotisations_sociales', period)
    plafond_securite_sociale = simulation.calculate_add('plafond_securite_sociale', period)
    type_sal = simulation.calculate('type_sal', period)

    cotisation = apply_bareme_for_relevant_type_sal(
        bareme_by_type_sal_name = bareme_by_type_sal_name,
        bareme_name = bareme_name,
        base = assiette_cotisations_sociales,
        plafond_securite_sociale = plafond_securite_sociale,
        type_sal = type_sal,
        )
    return cotisation


def compute_cotisation_annuelle(simulation, period, cotisation_type = None, bareme_name = None):
    if period.start.month < 12:
        return 0
    if period.start.month == 12:
        return compute_cotisation(
            simulation,
            period = period.start.offset('first-of', 'year').period('year'),
            cotisation_type = cotisation_type,
            bareme_name = bareme_name,
            )


def compute_cotisation_anticipee(simulation, period, cotisation_type = None, bareme_name = None, variable_name = None):
    if period.start.month < 12:
        return compute_cotisation(
            simulation,
            period = period.start.offset('first-of', 'month').period('month'),
            cotisation_type = cotisation_type,
            bareme_name = bareme_name,
            )
    if period.start.month == 12:
        cumul = simulation.calculate_add(variable_name, period.start.offset('first-of', 'month').offset(
            -11, 'month').period('month', 11))

        return compute_cotisation(
            simulation,
            period = period.start.offset('first-of', 'year').period('year'),
            cotisation_type = cotisation_type,
            bareme_name = bareme_name,
            ) - cumul


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
    label = u"Contribution à l'association pour la gestion du régime de garantie des créances des salariés (AGS, employeur)" # noqa analysis:ignore

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
class conge_individuel_formation_cdd(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution au financement des congé individuel de formation (CIF) des salariées en CDD"

    # TODO: date de début
    def function(self, simulation, period):
        contrat_de_travail_duree = simulation.calculate('contrat_de_travail_duree', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        law = simulation.legislation_at(period.start).cotsoc.conge_individuel_formation

        cotisation = - law.cdd * (contrat_de_travail_duree == 1) * assiette_cotisations_sociales
        return period, cotisation


@reference_formula
class contribution_developpement_apprentissage(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution additionnelle au développement de l'apprentissage"

    def function(self, simulation, period):
        redevable_taxe_apprentissage = simulation.calculate('redevable_taxe_apprentissage', period)
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = "employeur",
            bareme_name = "apprentissage_add",
            variable_name = self.__class__.__name__,
            )
        return period, cotisation * redevable_taxe_apprentissage


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
class contribution_supplementaire_apprentissage(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Contribution supplémentaire à l'apprentissage"

    @dated_function(date(2010, 1, 1))
    def function(self, simulation, period):
        redevable_taxe_apprentissage = simulation.calculate('redevable_taxe_apprentissage', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        ratio_alternants = simulation.calculate('ratio_alternants', period)
        effectif_entreprise = simulation.calculate('effectif_entreprise', period)
        taux = simulation.legislation_at(period.start).cotsoc.contribution_supplementaire_apprentissage

        if period.start.year > 2012:
            taux_contribution = redevable_taxe_apprentissage * (
                (effectif_entreprise < 2000) * (ratio_alternants < .01) * taux.moins_2000_moins_1pc_alternants +
                (effectif_entreprise >= 2000) * (ratio_alternants < .01) * taux.plus_2000_moins_1pc_alternants +
                (.01 <= ratio_alternants) * (ratio_alternants < .02) * taux.entre_1_2_pc_alternants +
                (.02 <= ratio_alternants) * (ratio_alternants < .03) * taux.entre_2_3_pc_alternants +
                (.03 <= ratio_alternants) * (ratio_alternants < .04) * taux.entre_3_4_pc_alternants +
                (.04 <= ratio_alternants) * (ratio_alternants < .05) * taux.entre_4_5_pc_alternants
                )
        else:
            taux_contribution = (effectif_entreprise >= 250) * taux.plus_de_250 * redevable_taxe_apprentissage
            # TODO: gestion de la place dans le XML pb avec l'arbre des paramètres / preprocessing
        return period, - taux_contribution * assiette_cotisations_sociales


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
class fnal_tranche_a(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Cotisation fonds national action logement (FNAL tout employeur)"

    def function(self, simulation, period):
        taille_entreprise = simulation.calculate('taille_entreprise', period)
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'fnal1',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation * (taille_entreprise <= 2)


@reference_formula
class fnal_tranche_a_plus_20(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Fonds national action logement (FNAL, employeur avec plus de 20 salariés)"

    def function(self, simulation, period):
        taille_entreprise = simulation.calculate('taille_entreprise', period)
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'fnal2',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation * (taille_entreprise > 2)


@reference_formula
class forfait_social(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Forfait social"
    start_date = date(2009, 1, 1)

    # les contributions destinées au financement des prestations de prévoyance complémentaire versées
    # au bénéfice de leurs salariés, anciens salariés et de leurs ayants droit (entreprises à partir de 10 salariés),
    # la réserve spéciale de participation dans les sociétés coopératives ouvrières de production (Scop).

    def function(self, simulation, period):
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre', period)
        prise_en_charge_employeur_prevoyance_complementaire = simulation.calculate(
            'prise_en_charge_employeur_prevoyance_complementaire', period)

        taux_plein = simulation.legislation_at(period.start).forfait_social.taux_plein
        taux_reduit = simulation.legislation_at(period.start).forfait_social.taux_reduit

        # TODO: complete this
        assiette_taux_plein = 0  # TODO: complete this
        assiette_taux_reduit = prevoyance_obligatoire_cadre - prise_en_charge_employeur_prevoyance_complementaire

        return period, (
            assiette_taux_plein * taux_plein +
            assiette_taux_reduit * taux_reduit
            )


@reference_formula
class formation_professionnelle(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Formation professionnelle"

    def function(self, simulation, period):
        taille_entreprise = simulation.calculate('taille_entreprise', period)
        cotisation_0_9 = (taille_entreprise == 1) * apply_bareme(
            simulation,
            period, cotisation_type = 'employeur',
            bareme_name = 'formprof_09',
            variable_name = self.__class__.__name__,
            )
        cotisation_10_19 = (taille_entreprise == 2) * apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_1019',
            variable_name = self.__class__.__name__,
            )
        cotisation_20 = (taille_entreprise > 2) * apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'formprof_20',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation_0_9 + cotisation_10_19 + cotisation_20


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
class participation_effort_construction(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Participation à l'effort de construction"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'construction',
            variable_name = self.__class__.__name__,
            )
        return period, cotisation


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
class taxe_apprentissage(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Taxe d'apprentissage (employeur, entreprise redevable de la taxe d'apprentissage uniquement)"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        redevable_taxe_apprentissage = simulation.calculate('redevable_taxe_apprentissage', period)
        cotisation = apply_bareme(
            simulation,
            period,
            cotisation_type = 'employeur',
            bareme_name = 'apprentissage',
            variable_name = self.__class__.__name__,
            )
        return period, redevable_taxe_apprentissage * cotisation


@reference_formula
class taxe_salaires(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Taxe sur les salaires"
# Voir
# http://www.impots.gouv.fr/portal/deploiement/p1/fichedescriptiveformulaire_8920/fichedescriptiveformulaire_8920.pdf

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        assujettie_taxe_salaires = simulation.calculate('assujettie_taxe_salaires', period)
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        prevoyance_obligatoire_cadre = simulation.calculate('prevoyance_obligatoire_cadre', period)
        law = simulation.legislation_at(period.start)

        bareme = law.cotsoc.taxes_sal.taux_maj
        base = assiette_cotisations_sociales - prevoyance_obligatoire_cadre
        # TODO: exonérations apprentis
        # TODO: modify if DOM

        return period, - (
            bareme.calc(
                base,
                factor = 1 / 12,
                round_base_decimals = 2
                ) +
            round_(law.cotsoc.taxes_sal.taux.metro * base, 2)
            ) * assujettie_taxe_salaires


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
class taux_versement_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u""

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        localisation_entreprise = simulation.calculate('localisation_entreprise', period)
        _P = simulation.legislation_at(period.start)

        aot_salarie = 0 # Autorité organisatrice des transports du salarié (nul si absent)
        smt_salarie = 0 # Syndicat mixte des transports du salarié (nul si absent)

        entreprise_seuil_employe_aot = 0 # "L'entreprise emploie-t-elle 9 salariés ou plus dans le périmètre
                                   # de l'Autorité organisatrice de transport (AOT) suivante :"
    #  Taux du versement de transport dans l'AOT du salari<E9> -> *SALARIE.TX_VT (Valeur par d<E9>faut: '0.00000')
    #
    #% Cas ou le salari<E9> travaille dans une commune avec AOT
    #
    #        2.6.2 [Versement de transport additionnel]
    #
    #              # Question : "L'entreprise emploie-t-elle 9 salari<E9>s ou plus dans le p<E9>rim<E8>tre du Syndicat mixte de tranports (SMT) suivant ?"
    #
    #              # Affichage : Afficher le nom du SMT (SALARIE.NOM_SMT) ainsi que toutes les communes couvertes par le SMT (SALARIE.SMT.LISTE_COMMUNES)
    #
    #              # Mode de saisie : <E0> cocher au choix : "oui" / "non" (case coch<E9>e par d<E9>faut : "oui")
    #
    #              # Enregistrements:
    #                R<E9>ponse -> *SALARIE.IS_SMT_9P (bool : '1' si "oui" / '0' si "non")
    #                Taux du versement de transport additionel dans le SMT du salari<E9> -> *SALARIE.TX_VTA (Valeur par d<E9>faut: '0.0000')
    #
    #        }

    #    global taux_versement_transport_by_localisation_entreprise
    #    if taux_versement_transport_by_localisation_entreprise is None:
    #        with pkg_resources.resource_stream(
    #            openfisca_france.__name__,
    #            'assets/versement_transport/versement_transport.csv',
    #            ) as csv_file:
    #            csv_reader = csv.DictReader(csv_file)
    #            taux_versement_transport_by_localisation_entreprise = {
    #                # Keep only first char of Zonage column because of 1bis value considered equivalent to 1.
    #                row['CODGEO']: int(row['Taux'][0])
    #                for row in csv_reader
    #                }
    #        # Add subcommunes (arrondissements and communes associées), use the same value as their parent commune.
    #        with pkg_resources.resource_stream(
    #            openfisca_france.__name__,
    #            'assets/versement_transport/versement_transport_by_subcommune_depcom.json',
    #            ) as json_file:
    #            commune_depcom_by_subcommune_depcom = json.load(json_file)
    #            for subcommune_depcom, commune_depcom in commune_depcom_by_subcommune_depcom.iteritems():
    #                taux_versement_transport_by_localisation_entreprise[subcommune_depcom] = taux_versement_transport_by_localisation_entreprise[commune_depcom]
    #
    #    default_value = _P.cotsoc.cotisations_employeur['prive_non_cadre']["transport"].rates[0]
    #    return fromiter(
    #        (
    #            taux_versement_transport_by_localisation_entreprise.get(localisation_entreprise_cell, default_value)
    #            for localisation_entreprise_cell in localisation_entreprise
    #            ),
    #        dtype = float,
    #        )
        rate = _P.cotsoc.cotisations_employeur['prive_non_cadre']["transport"].rates[0]
        return period, rate * ones(len(localisation_entreprise))


@reference_formula
class versement_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Versement transport"

    def function(self, simulation, period):
        period = period.start.period(u'month').offset('first-of')
        assiette_cotisations_sociales = simulation.calculate('assiette_cotisations_sociales', period)
        taux_versement_transport = simulation.calculate('taux_versement_transport', period)
        cotisation = - taux_versement_transport * assiette_cotisations_sociales
        return period, cotisation


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
