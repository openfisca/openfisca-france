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


from functools import partial
from numpy import (
    busday_count as original_busday_count, datetime64, logical_not as not_, logical_or as or_, maximum as max_,
    minimum as min_, round as round_, timedelta64
    )

import logging

from ....base import *  # noqa analysis:ignore
from .....assets.holidays import holidays

log = logging.getLogger(__name__)


@reference_formula
class assiette_allegement(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Assiette des allègements de cotisations sociales employeur"

    def function(self, simulation, period):
        assiette_cotisations_sociales = simulation.calculate_add('assiette_cotisations_sociales', period)
        type_sal = simulation.calculate('type_sal', period)
        period = period
        # TODO vérifier changement d'assiette
        return period, assiette_cotisations_sociales * (
            (type_sal == CAT['prive_non_cadre']) | (type_sal == CAT['prive_cadre'])
            )


@reference_formula
class allegement_fillon(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allègement de charges employeur sur les bas et moyens salaires (dit allègement Fillon)"

    @dated_function(date(2005, 7, 1))
    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        stagiaire = simulation.calculate('stagiaire', period)
        apprenti = simulation.calculate('apprenti', period)
        allegement_fillon_mode_recouvrement = simulation.calculate('allegement_fillon_mode_recouvrement', period)
        allegement = (
            # en fin d'année
            allegement_fillon_mode_recouvrement == 0) * (
                compute_allegement_fillon_annuel(simulation, period)
                ) + (
            # anticipé
            allegement_fillon_mode_recouvrement == 1) * (
                compute_allegement_fillon_anticipe(simulation, period)
                ) + (
            # cumul progressif
            allegement_fillon_mode_recouvrement == 2) * (
                compute_allegement_fillon_progressif(simulation, period)
            )
        return period, allegement * not_(stagiaire) * not_(apprenti)


@reference_formula
class coefficient_proratisation(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Coefficient de proratisation pour le calcul du SMIC et du plafond de la Sécurité socialele"

    def function(self, simulation, period):
        # u"temps_plein",
        # u"temps_partiel",
        # u"forfait_heures_semaines",
        # u"forfait_heures_mois",
        # u"forfait_heures_annee",
        # u"forfait_jours_annee",
        contrat_de_travail = simulation.calculate('contrat_de_travail', period)
        contrat_de_travail_debut = simulation.calculate('contrat_de_travail_debut', period)
        contrat_de_travail_fin = simulation.calculate('contrat_de_travail_fin', period)
        forfait_heures_remunerees_volume = simulation.calculate('forfait_heures_remunerees_volume', period)
        forfait_jours_remuneres_volume = simulation.calculate('forfait_jours_remuneres_volume', period)
        heures_duree_collective_entreprise = simulation.calculate('heures_duree_collective_entreprise', period)
        heures_remunerees_volume = simulation.calculate('heures_remunerees_volume', period)
        heures_non_remunerees_volume = simulation.calculate('heures_non_remunerees_volume', period)

        # Décompte des jours en début et fin de contrat
        # http://www.gestiondelapaie.com/flux-paie/?1029-la-bonne-premiere-paye

        busday_count = partial(original_busday_count, holidays = holidays)
        debut_mois = datetime64(period.start.offset('first-of', 'month'))
        fin_mois = datetime64(period.start.offset('last-of', 'month')) + timedelta64(1, 'D')

        mois_incomplet = or_(contrat_de_travail_debut > debut_mois, contrat_de_travail_fin < fin_mois)
        jours_travailles = busday_count(
            max_(contrat_de_travail_debut, debut_mois),
            min_(contrat_de_travail_fin, fin_mois)
            )

        duree_legale = 35 * 52 / 12  # mensuelle_temps_plein
        heures_temps_plein = (
            (heures_duree_collective_entreprise == 0) * duree_legale + heures_duree_collective_entreprise
            )
        # heures remunerees avant conges sans soldes/ijss
        heures_remunerees_volume = (
            (contrat_de_travail == 0) * (
                heures_temps_plein * not_(mois_incomplet) +  # 151.67
                jours_travailles * 7 * mois_incomplet  # TODO: 7 = heures / jours
                ) +
            (contrat_de_travail == 1) * heures_remunerees_volume
            )
        heures_realisees = heures_remunerees_volume - heures_non_remunerees_volume

        coefficient = (
            # Salariés à temps plein
            (contrat_de_travail == 0) * heures_realisees / heures_temps_plein +
            # Salariés à temps partiel : plafond proratisé en fonction du ratio durée travaillée / durée du temps plein
            #   Salariés sans convention de forfait à temps partiel
            (contrat_de_travail == 1) * heures_realisees / heures_temps_plein +
            #   Salariés avec convention de forfait
            #      Forfait en heures
            (contrat_de_travail >= 2) * (contrat_de_travail <= 3) * (
                forfait_heures_remunerees_volume / 45.7 * 52 / 12
                ) +
            #      Forfait en jours
            (contrat_de_travail == 4) * forfait_jours_remuneres_volume / 218
            )
        return period, coefficient


@reference_formula
class credit_impot_competitivite_emploi(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Crédit d'imôt pour la compétitivité et l'emploi"

    @dated_function(date(2013, 1, 1))
    def function_2013_(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        assiette_allegement = simulation.calculate('assiette_allegement', period)
        jeune_entreprise_innovante = simulation.calculate('jeune_entreprise_innovante', period)
        smic_proratise = simulation.calculate('smic_proratise', period)
        stagiaire = simulation.calculate('stagiaire', period)
        cotsoc = simulation.legislation_at(period.start).cotsoc
        taux_cice = taux_exo_cice(assiette_allegement, smic_proratise, cotsoc)
        credit_impot_competitivite_emploi = (
            taux_cice
            * assiette_allegement
            )
        non_cumul = (jeune_entreprise_innovante == 0 + stagiaire) > 0

        return period, credit_impot_competitivite_emploi * non_cumul


@reference_formula
class smic_proratise(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"SMIC proratisé"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        coefficient_proratisation = simulation.calculate('coefficient_proratisation', period)
        smic_horaire_brut = simulation.legislation_at(period.start).cotsoc.gen.smic_h_b
        smic_proratise = coefficient_proratisation * smic_horaire_brut * 35 * 52 / 12

        return period, smic_proratise


# Helper functions


def compute_allegement_fillon_annuel(simulation, period):
    if period.start.month < 12:
        return 0
    if period.start.month == 12:
        return compute_allegement_fillon(simulation, period.start.offset('first-of', 'year').period('year'))


def compute_allegement_fillon_anticipe(simulation, period):
    if period.start.month < 12:
        return compute_allegement_fillon(simulation, period.start.offset('first-of', 'month').period('month'))
    if period.start.month == 12:
        cumul = simulation.calculate_add(
            'allegement_fillon',
            period.start.offset('first-of', 'year').period('month', 11))
        return compute_allegement_fillon(
            simulation, period.start.offset('first-of', 'year').period('year')
            ) - cumul


def compute_allegement_fillon_progressif(simulation, period):
    if period.start.month == 1:
        return compute_allegement_fillon(simulation, period.start.offset('first-of', 'month').period('month'))

    if period.start.month > 1:
        up_to_this_month = period.start.offset('first-of', 'year').period('month', period.start.month)
        up_to_previous_month = period.start.offset('first-of', 'year').period('month', period.start.month - 1)
        cumul = simulation.calculate_add('allegement_fillon', up_to_previous_month)
        up_to_this_month = period.start.offset('first-of', 'year').period('month', period.start.month)
        return compute_allegement_fillon(simulation, up_to_this_month) - cumul


def compute_allegement_fillon(simulation, period):
    '''
    Exonération Fillon
    http://www.securite-sociale.fr/comprendre/dossiers/exocotisations/exoenvigueur/fillon.htm
    '''
    assiette_allegement = simulation.calculate_add('assiette_allegement', period)
    smic_proratise = simulation.calculate_add('smic_proratise', period)
    taille_entreprise = simulation.calculate('taille_entreprise', period)
    majoration = (taille_entreprise <= 2)  # majoration éventuelle pour les petites entreprises
    # Calcul du taux
    # Le montant maximum de l’allègement dépend de l’effectif de l’entreprise.
    # Le montant est calculé chaque année civile, pour chaque salarié ;
    # il est égal au produit de la totalité de la rémunération annuelle telle
    # que visée à l’article L. 242-1 du code de la Sécurité sociale par un
    # coefficient.
    # Ce montant est majoré de 10 % pour les entreprises de travail temporaire
    # au titre des salariés temporaires pour lesquels elle est tenue à
    # l’obligation d’indemnisation compensatrice de congés payés.
    Pf = simulation.legislation_at(period.start).cotsoc.exo_bas_sal.fillon
    seuil = Pf.seuil
    tx_max = (Pf.tx_max * not_(majoration) + Pf.tx_max2 * majoration)
    if seuil <= 1:
        return 0
    ratio_smic_salaire = smic_proratise / (assiette_allegement + 1e-16)
    # règle d'arrondi: 4 décimales au dix-millième le plus proche
    taux_fillon = round_(tx_max * min_(1, max_(seuil * ratio_smic_salaire - 1, 0) / (seuil - 1)), 4)

    # Montant de l'allegment
    allegement_fillon = taux_fillon * assiette_allegement
    return allegement_fillon


def taux_exo_cice(assiette_allegement, smic_proratise, P):
    Pc = P.exo_bas_sal.cice
    taux_cice = ((assiette_allegement / (smic_proratise + 1e-16)) <= Pc.max) * Pc.taux
    return taux_cice
