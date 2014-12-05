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


import logging


from numpy import maximum as max_


from openfisca_core.accessors import law
from openfisca_core.columns import FloatCol
from openfisca_core.formulas import SimpleFormulaColumn


from ..base import CAT, QUIFAM, QUIFOY, QUIMEN
from ..base import Individus, reference_formula


log = logging.getLogger(__name__)


CHEF = QUIFAM['chef']
PREF = QUIMEN['pref']
VOUS = QUIFOY['vous']


@reference_formula
class assiette_cotisations_sociales_prive(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Assiette des cotisations sociales des salaries du prive et des contractuel de la fonction publique"

    def function(self, avantages_en_nature, indemnite_residence, nombre_heures, primes_fonction_publique,
                 primes_salaires, salaire_de_base, type_sal,
                 smic_horaire_brut = law.gen.smic_h_b,
                 taux_minimum_exoneration = law.gen.taux_minimum_exoneration,
                 taux_maximum_exoneration = law.gen.taux_maximum_exoneration):
        # assiette des cotisations sociales
        # Autres élements de rémunérations à prendre en compte:
        #   * cantine_titres_restaurants
        #   * prise en charge par l'employeur de la part salariale
        #    des cotisations sociales à un régime de retraite complémentaire
        #       (celle conernant les régime de prévoyance complémentaire et de retraite supplémentaire n'entrent pas
        #        dans l'assiette des cotisations sociales)
        #   * cotisations partonales à:
        #       - retraite complémentaire obligatoire
        #       - retraite supplémentaire et de prévoyance complémentaire
        #       - retraite à prestations définies (retraite chapeau)
        #   * Épargne salariale, intéressement et participation
        #   * Actionnarait salarié
        #   * Indemnités journalières de sécurité sociale
        #   * Indemnités de rupture du contrat de travail

        cantine_titres_restaurants_taux_entreprise = 0
        cantine_titres_restaurants_prix_titre = 0
        cantine_titres_restaurants_nombre_titres = 0

        condition_exoneration_taux = (
            (taux_minimum_exoneration <= cantine_titres_restaurants_taux_entreprise) *
            (taux_maximum_exoneration >= cantine_titres_restaurants_taux_entreprise)
            )
        cantine_titres_restaurants = cantine_titres_restaurants_nombre_titres * (
            condition_taux * max_(cantine_titres_restaurants_prix_titre - seuil_prix_titre, 0) +
            not_(condition_taux) * cantine_titres_restaurants_prix_titre
            )
        assiette = (
            salaire_de_base +
            primes_salaires +
            avantages_en_nature +
            (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
            )

        return max_(assiette, smic_horaire_brut * nombre_heures)

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period(u'month')


@reference_formula
class avantages_en_nature(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Avantages en nature"

    def function(self, avantages_en_nature_valeur_reelle, avantages_en_nature_valeur_forfaitaire):
        return avantages_en_nature_valeur_reelle + avantages_en_nature_valeur_forfaitaire

    def get_output_period(self, period):
        return period


@reference_formula
class avantages_en_nature_valeur_forfaitaire(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Evaluation fofaitaire des avantages en nature "

    # TODO:
    def function(self, avantages_en_nature_valeur_reelle):
        return avantages_en_nature_valeur_reelle * 0

    def get_output_period(self, period):
        return period


@reference_formula
class nombre_heures(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Nombre d'heures rémunérées mensuellement"
    # type_heures_remunerees :
    #   0     u"temps_plein",
    #   1     u"temps_partiel",
    #   2     u"forfait_heures",
    #   3     u"forfait_jours",
    #   4     u"duree_contractuelle",  # heures/mois

    def function(self, type_heures_remunerees, volume_heures_remunerees):
        # TODO faire remonter dans les paramètres les valeurs codées en dur qui doivent/peuvent l'être
        nombre_heures = (
            (type_heures_remunerees == 0) * 151.67 +
            (type_heures_remunerees == 1) * volume_heures_remunerees +
            (type_heures_remunerees == 2) * 151.67 * (volume_heures_remunerees / 45.7) * (52 / 12) +
            (type_heures_remunerees == 3) * 151.67 * (volume_heures_remunerees / 218) * (52 / 12) +
            (type_heures_remunerees == 4) * 151.67 * volume_heures_remunerees
            )
        return nombre_heures

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period(u'month')


@reference_formula
class sal_h_b(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Salaire horaire brut"

    def function(self, salbrut, nombre_heures):
        return salbrut / nombre_heures

    def get_output_period(self, period):
        return period.start.offset('first-of', 'month').period(u'month')
