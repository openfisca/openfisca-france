# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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

import datetime
import logging
from numpy import logical_not as not_, logical_or as or_, maximum as max_, minimum as min_


from openfisca_core.accessors import law
from openfisca_core.columns import FloatCol
from openfisca_core.formulas import dated_function, DatedFormulaColumn, SimpleFormulaColumn

from ..base import CAT, QUIFAM, QUIFOY, QUIMEN
from ..base import Individus, reference_formula


CHEF = QUIFAM['chef']
PREF = QUIMEN['pref']
VOUS = QUIFOY['vous']


log = logging.getLogger(__name__)


@reference_formula
class smic_proratise(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"SMIC annuel proratisé"

    def function(self, nombre_heures_remunerees,
                 smic_horaire_brut = law.cotsoc.gen.smic_h_b):

        smic_proratise = smic_horaire_brut * nombre_heures_remunerees
        return smic_proratise

    def get_output_period(self, period):
        return period


@reference_formula
class ratio_smic_salaire(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Ratio smic/salaire pour le calcul de l'allègement Fillon"

    @dated_function(start = datetime.date(2012, 1, 1))
    def function_2012(self, smic_proratise, salbrut, contrat_de_travail,
                      smic_horaire_brut = law.cotsoc.gen.smic_h_b):
        # salbrut_annuel 2012 nombre_heures_remunerees incluent hsup à partir de 2012
        smic_annuel = smic_proratise  # durée légale du travail = 1820
        ratio_smic_salaire = smic_annuel / (salbrut + 1e-10)
        return ratio_smic_salaire

    @dated_function(start = datetime.date(2011, 1, 1), stop = datetime.date(2011, 12, 31))
    def function_2011(self, smic_proratise, salbrut, contrat_de_travail,
                      smic_horaire_brut = law.cotsoc.gen.smic_h_b):
        # TODO
        # salbrut_annuel 2011 même chose mais avec salbrut sans hsup
        smic_annuel = smic_proratise  # durée légale du travail = 1820
        ratio_smic_salaire = smic_annuel / (salbrut + 1e-10)
        return ratio_smic_salaire

    @dated_function(start = datetime.date(2005, 7, 1), stop = datetime.date(2010, 12, 31))
    def function_2007_2010(self, smic_proratise, salbrut, contrat_de_travail,
                           smic_horaire_brut = law.cotsoc.gen.smic_h_b):
        # TODO: revoir la législation
        smic_annuel = smic_proratise  # durée légale du travail = 1820
        ratio_smic_salaire = smic_annuel / (salbrut + 1e-10)
        return ratio_smic_salaire

    def get_output_period(self, period):
        return period.start.offset('first-of', 'year').period('year')


@reference_formula
class ratio_smic_salaire_anticipe(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Ratio smic/salaire pour le calcul de l'allègement Fillon"

    @dated_function(start = datetime.date(2012, 1, 1))
    def function_2012(self, smic_proratise, salbrut, contrat_de_travail,
                      smic_horaire_brut = law.cotsoc.gen.smic_h_b):
        # salbrut_annuel 2012 nombre_heures_remunerees incluent hsup à partir de 2012
        smic_annuel = smic_proratise  # durée légale du travail = 1820
        ratio_smic_salaire = smic_annuel / (salbrut + 1e-10)
        return ratio_smic_salaire

    @dated_function(start = datetime.date(2011, 1, 1), stop = datetime.date(2011, 12, 31))
    def function_2011(self, smic_proratise, salbrut, contrat_de_travail,
                      smic_horaire_brut = law.cotsoc.gen.smic_h_b):
        # TODO
        # salbrut_annuel 2011 même chose mais avec salbrut sans hsup
        smic_annuel = smic_proratise  # durée légale du travail = 1820
        ratio_smic_salaire = smic_annuel / (salbrut + 1e-10)
        return ratio_smic_salaire

    @dated_function(start = datetime.date(2005, 7, 1), stop = datetime.date(2010, 12, 31))
    def function_2007_2010(self, smic_proratise, salbrut, contrat_de_travail,
                           smic_horaire_brut = law.cotsoc.gen.smic_h_b):
        # TODO: revoir la législation
        smic_annuel = smic_proratise  # durée légale du travail = 1820
        ratio_smic_salaire = smic_annuel / (salbrut + 1e-10)
        return ratio_smic_salaire

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class allegement_fillon_annuel(DatedFormulaColumn):   # annuel
    column = FloatCol
    entity_class = Individus
    label = u"Allègement de charges patronales sur les bas et moyens salaires (dit allègement Fillon)"

    @dated_function(datetime.date(2005, 7, 1))
    def function(self, ratio_smic_salaire, salbrut, taille_entreprise, type_sal,
                 cotsoc = law.cotsoc):

        majoration = (taille_entreprise <= 2)  # majoration éventuelle pour les petites entreprises
        taux_fillon = taux_exo_fillon(ratio_smic_salaire, majoration, cotsoc)
        allegement_fillon = (
            taux_fillon *
            salbrut *
            ((type_sal == CAT['prive_non_cadre']) | (type_sal == CAT['prive_cadre']))
            )
        return allegement_fillon

    def get_output_period(self, period):
        return period.start.offset('first-of', 'year').period('year')


@reference_formula
class allegement_fillon_anticipe(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allègement de charges patronales sur les bas et moyens salaires (dit allègement Fillon)"

    @dated_function(datetime.date(2005, 7, 1))
    def function(self, ratio_smic_salaire_anticipe, salbrut, taille_entreprise, type_sal,
                 cotsoc = law.cotsoc):

        majoration = (taille_entreprise <= 2)  # majoration éventuelle pour les petites entreprises
        taux_fillon = taux_exo_fillon(ratio_smic_salaire_anticipe, majoration, cotsoc)
        allegement_fillon = (
            taux_fillon *
            salbrut *
            ((type_sal == CAT['prive_non_cadre']) | (type_sal == CAT['prive_cadre']))
            )
        return allegement_fillon

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class allegement_fillon_cumul_progressif(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allègement Fillon, cumul progressif"

    @dated_function(datetime.date(2005, 7, 1))
    def function(self, smic_proratise, salbrut, taille_entreprise, type_sal,
                 cotsoc = law.cotsoc):

        ratio_smic_salaire_cumul_progressif = smic_proratise / (salbrut + 1e-10)

        majoration = (taille_entreprise <= 2)  # majoration éventuelle pour les petites entreprises
        taux_fillon = taux_exo_fillon(ratio_smic_salaire_cumul_progressif, majoration, cotsoc)
        allegement_fillon = (
            taux_fillon *
            salbrut *
            ((type_sal == CAT['prive_non_cadre']) | (type_sal == CAT['prive_cadre']))
            )
        return allegement_fillon

    def get_variable_period(self, output_period, variable_name):
        if variable_name in ['smic_proratise', 'salbrut']:
            size = output_period.start.month
            return output_period.start.offset('first-of', 'year').period('month', size)
        else:
            return output_period.start.offset('first-of', 'month').period('month')

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class allegement_fillon_cumul_progressif_retarde(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allègement Fillon, cumul progressif retardé"

    @dated_function(datetime.date(2005, 7, 1))
    def function(self, period, smic_proratise, salbrut, taille_entreprise, type_sal,
                 cotsoc = law.cotsoc):

        ratio_smic_salaire_cumul_progressif = smic_proratise / (salbrut + 1e-10)

        majoration = (taille_entreprise <= 2)  # majoration éventuelle pour les petites entreprises
        taux_fillon = taux_exo_fillon(ratio_smic_salaire_cumul_progressif, majoration, cotsoc)
        allegement_fillon = (
            taux_fillon *
            salbrut *
            ((type_sal == CAT['prive_non_cadre']) | (type_sal == CAT['prive_cadre']))
            )
        return allegement_fillon * (period.start.month >= 2)

    def get_variable_period(self, output_period, variable_name):
        if variable_name in ['smic_proratise', 'salbrut']:
            size = max(output_period.start.month, 2)
            return output_period.start.offset('first-of', 'year').period('month', size - 1)
        else:
            return output_period.start.offset('first-of', 'month').period('month')

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class allegement_fillon(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Allègement de charges patronales sur les bas et moyens salaires (dit allègement Fillon)"

    @dated_function(datetime.date(2005, 7, 1))
    def function(self, period, allegement_fillon_anticipe, allegement_fillon_annuel, allegement_fillon_cumul_progressif,
                 allegement_fillon_cumul_progressif_retarde, allegement_fillon_mode_recouvrement,
                 cotsoc = law.cotsoc):

        if period.start.month < 12:
            return (
                # 0 * (allegement_fillon_mode_recouvrement == 0) +
                allegement_fillon_anticipe * (allegement_fillon_mode_recouvrement == 1) +
                (
                    (allegement_fillon_cumul_progressif - allegement_fillon_cumul_progressif_retarde) *
                    (allegement_fillon_mode_recouvrement == 2)
                    )
                )
        else:
            return (
                allegement_fillon_annuel * (allegement_fillon_mode_recouvrement == 0) +
                (allegement_fillon_annuel - allegement_fillon_anticipe) * (allegement_fillon_mode_recouvrement == 1) +
                (
                    (allegement_fillon_cumul_progressif - allegement_fillon_cumul_progressif_retarde) *
                    (allegement_fillon_mode_recouvrement == 2)
                    )
                )

    def get_variable_period(self, output_period, variable_name):
        if variable_name in ['allegement_fillon_annuel']:
            return output_period.start.offset('first-of', 'year').period('year')
        elif variable_name in ['allegement_fillon_anticipe'] and output_period.start.month == 12:
            return output_period.start.offset('first-of', 'year').period('month', 11)
        else:
            return output_period

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


@reference_formula
class alleg_cice(DatedFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Crédit d'imôt pour la compétitivité et l'emploi"

    @dated_function(datetime.date(2013, 1, 1))
    def function_2013_(self, ratio_smic_salaire, salbrut, taille_entreprise, type_sal,
                       cotsoc = law.cotsoc):

        taux_cice = taux_exo_cice(ratio_smic_salaire, cotsoc)
        alleg_cice = (
            taux_cice
            * salbrut
            * or_((type_sal == CAT['prive_non_cadre']), (type_sal == CAT['prive_cadre']))
            )
        return alleg_cice

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period('month')


# Helper functions

def taux_exo_fillon(ratio_smic_salaire, majoration, P):
    '''
    Exonération Fillon
    http://www.securite-sociale.fr/comprendre/dossiers/exocotisations/exoenvigueur/fillon.htm
    '''
    # La divison par zéro engendre un warning
    # Le montant maximum de l’allègement dépend de l’effectif de l’entreprise.
    # Le montant est calculé chaque année civile, pour chaque salarié ;
    # il est égal au produit de la totalité de la rémunération annuelle telle
    # que visée à l’article L. 242-1 du code de la Sécurité sociale par un
    # coefficient.
    # Ce montant est majoré de 10 % pour les entreprises de travail temporaire
    # au titre des salariés temporaires pour lesquels elle est tenue à
    # l’obligation d’indemnisation compensatrice de congés payés.

    Pf = P.exo_bas_sal.fillon
    seuil = Pf.seuil
    tx_max = (Pf.tx_max * not_(majoration) + Pf.tx_max2 * majoration)
    if seuil <= 1:
        return 0
    # règle d'arrondi: 4 décimales au dix-millième le plus proche
    taux_fillon = round(tx_max * min_(1, max_(seuil * ratio_smic_salaire - 1, 0) / (seuil - 1)), 4)
    return taux_fillon


def taux_exo_cice(ratio_smic_salaire, P):
    Pc = P.exo_bas_sal.cice
    taux_cice = (1 / ratio_smic_salaire <= Pc.max) * Pc.taux
    return taux_cice
