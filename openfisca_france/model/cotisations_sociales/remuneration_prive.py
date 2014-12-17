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


from functools import partial
import logging
from numpy import (
    busday_count as original_busday_count, datetime64, logical_not as not_, logical_or as or_, maximum as max_,
    minimum as min_, timedelta64
    )

from ...assets.holidays import holidays

from ..base import *  # noqa


log = logging.getLogger(__name__)


@reference_formula
class assiette_cotisations_sociales_prive(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Assiette des cotisations sociales des salaries du prive et des contractuel de la fonction publique"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period(u'month')
        avantages_en_nature = simulation.calculate('avantages_en_nature', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        nombre_heures_remunerees = simulation.calculate('nombre_heures_remunerees', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        primes_salaires = simulation.calculate('primes_salaires', period)
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        type_sal = simulation.calculate('type_sal', period)
        smic_horaire_brut = simulation.legislation_at(period.start).gen.smic_h_b

        assiette = (
            salaire_de_base +
            primes_salaires +
            avantages_en_nature +
            (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique)
            )

        return period, max_(assiette, smic_horaire_brut * nombre_heures_remunerees)


@reference_formula
class avantages_en_nature(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Avantages en nature"

    def function(self, simulation, period):
        period = period
        avantages_en_nature_valeur_reelle = simulation.calculate('avantages_en_nature_valeur_reelle', period)
        avantages_en_nature_valeur_forfaitaire = simulation.calculate('avantages_en_nature_valeur_forfaitaire', period)

        return period, avantages_en_nature_valeur_reelle + avantages_en_nature_valeur_forfaitaire


@reference_formula
class avantages_en_nature_valeur_forfaitaire(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Evaluation fofaitaire des avantages en nature "

    # TODO:
    def function(self, simulation, period):
        period = period
        avantages_en_nature_valeur_reelle = simulation.calculate('avantages_en_nature_valeur_reelle', period)

        return period, avantages_en_nature_valeur_reelle * 0


@reference_formula
class cantine_titres_restaurants(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Dépense de cantine et de titres restaurants"

    def function(self, simulation, period):
        period = period
        cantine_titres_restaurants_taux_entreprise = simulation.calculate('cantine_titres_restaurants_taux_entreprise', period)

        cantine_titres_restaurants_prix_titre = 0
        cantine_titres_restaurants_nombre_titres = 0
        #
        # condition_exoneration_taux = (
        #   (taux_minimum_exoneration <= cantine_titres_restaurants_taux_entreprise) *
        #   (taux_maximum_exoneration >= cantine_titres_restaurants_taux_entreprise)
        #   )
        # cantine_titres_restaurants = cantine_titres_restaurants_nombre_titres * (
        #   condition_taux * max_(cantine_titres_restaurants_prix_titre - seuil_prix_titre, 0) +
        #   not_(condition_taux) * cantine_titres_restaurants_prix_titre
        #   )
        return period, cantine_titres_restaurants_prix_titre * cantine_titres_restaurants_nombre_titres


@reference_formula
class cantine_titres_restaurants_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Prise en charge de l'employeur des dépenses de cantine et des titres restaurants"

    def function(self, simulation, period):
        period = period  # TODO
        cantine_titres_restaurants_taux_entreprise = simulation.calculate('cantine_titres_restaurants_taux_entreprise', period)

        return period, cantine_titres_restaurants_taux_entreprise * cantine_titres_restaurants


@reference_formula
class nombre_heures_remunerees(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Nombre d'heures rémunérées mensuellement"
    # contrat_de_travail :
    #   0     u"temps_plein",
    #   1     u"temps_partiel",
    #   2     u"forfait_heures",
    #   3     u"forfait_jours",
    #   4     u"duree_contractuelle",  # heures/mois

    # Source: Guide IPP cotisations sociales déterminations des assiettes (érroné)

    # Décompte des jours en début et fin de contrat
    # http://www.gestiondelapaie.com/flux-paie/?1029-la-bonne-premiere-paye

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period(u'month')
        contrat_de_travail = simulation.calculate('contrat_de_travail', period)
        contrat_de_travail_arrivee = simulation.calculate('contrat_de_travail_arrivee', period)
        contrat_de_travail_depart = simulation.calculate('contrat_de_travail_depart', period)
        volume_heures_non_remunerees = simulation.calculate('volume_heures_non_remunerees', period)
        volume_heures_remunerees = simulation.calculate('volume_heures_remunerees', period)

        busday_count = partial(original_busday_count, holidays = holidays)

        debut_mois = datetime64(period.start.offset('first-of', 'month'))
        fin_mois = datetime64(period.start.offset('last-of', 'month')) + timedelta64(1, 'D')

        mois_incomplet = or_(contrat_de_travail_arrivee > debut_mois, contrat_de_travail_depart < fin_mois)

        jours_travailles = busday_count(
            max_(contrat_de_travail_arrivee, debut_mois),
            min_(contrat_de_travail_depart, fin_mois)
            )
        jours_travaillables = busday_count(
            max_(contrat_de_travail_arrivee, debut_mois),
            min_(contrat_de_travail_depart, fin_mois)
            )

        duree_legale = 35 * 52 / 12  # mensuelle_temps_plein
        nombre_heures_remunerees = (
            (contrat_de_travail == 0) * (
                duree_legale * not_(mois_incomplet) +  # 151.67
                duree_legale * jours_travailles / jours_travaillables * mois_incomplet
                ) +
            (contrat_de_travail == 1) * volume_heures_remunerees +
            (contrat_de_travail == 2) * (volume_heures_remunerees / 45.7) * (52 / 12) +  # forfait heures/annee
            (contrat_de_travail == 3) * duree_legale * (volume_heures_remunerees / 218)  # forfait jours/annee
            )
        return period, nombre_heures_remunerees - volume_heures_non_remunerees


@reference_formula
class nombre_jours_calendaires(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Nombre de jours calendaires travaillés"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period(u'month')
        contrat_de_travail = simulation.calculate('contrat_de_travail', period)
        contrat_de_travail_arrivee = simulation.calculate('contrat_de_travail_arrivee', period)
        contrat_de_travail_depart = simulation.calculate('contrat_de_travail_depart', period)

        busday_count = partial(original_busday_count, weekmask = "1" * 7)
        debut_mois = datetime64(period.start.offset('first-of', 'month'))
        fin_mois = datetime64(period.start.offset('last-of', 'month')) + timedelta64(1, 'D')
        jours_travailles = busday_count(
            max_(contrat_de_travail_arrivee, debut_mois),
            min_(contrat_de_travail_depart, fin_mois)
            )
        return period, jours_travailles


#@reference_formula
#class sal_h_b(SimpleFormulaColumn):
#    column = FloatCol
#    entity_class = Individus
#    label = u"Salaire horaire brut"
#
#    def function(self, salbrut, nombre_heures_remunerees):
#        return salbrut / nombre_heures_remunerees
#
#    def get_output_period(self, period):
#        return period.start.offset('first-of', 'month').period(u'month')
