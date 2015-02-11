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
import logging
from numpy import (
    busday_count as original_busday_count, datetime64, logical_not as not_, logical_or as or_, maximum as max_,
    minimum as min_, timedelta64
    )


from ..base import *  # noqa


log = logging.getLogger(__name__)


@reference_formula
class assiette_cotisations_sociales(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Assiette des cotisations sociales des salaries"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period(u'month')
        assiette_cotisations_sociales_prive = simulation.calculate('assiette_cotisations_sociales_prive', period)
        assiette_cotisations_sociales_public = simulation.calculate('assiette_cotisations_sociales_public', period)
        return period, assiette_cotisations_sociales_prive + assiette_cotisations_sociales_public


@reference_formula
class assiette_cotisations_sociales_prive(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Assiette des cotisations sociales des salaries du prive"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period(u'month')
        avantages_en_nature = simulation.calculate('avantages_en_nature', period)
        indemnite_residence = simulation.calculate('indemnite_residence', period)
        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        primes_salaires = simulation.calculate('primes_salaires', period)
        reintegration_titre_restaurant_employeur = simulation.calculate(
            "reintegration_titre_restaurant_employeur", period
            )
        salaire_de_base = simulation.calculate('salaire_de_base', period)
        type_sal = simulation.calculate('type_sal', period)
        smic_proratise = simulation.calculate('smic_proratise', period)

        assiette = (
            salaire_de_base +
            primes_salaires +
            avantages_en_nature +
            (type_sal == CAT['public_non_titulaire']) * (
                indemnite_residence + primes_fonction_publique
                ) +
            reintegration_titre_restaurant_employeur
            )
        return period, max_(assiette, smic_proratise) * (assiette > 0)


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
class depense_cantine_titre_restaurant_employe(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Dépense de cantine et de titre restaurant à charge de l'employe"

    def function(self, simulation, period):
        period = period

        valeur_unitaire = simulation.calculate("titre_restaurant_valeur_unitaire", period)
        volume = simulation.calculate("titre_restaurant_volume", period)
        taux_employeur = simulation.calculate('titre_restaurant_taux_employeur', period)

        return period, - valeur_unitaire * volume * (1 - taux_employeur)


@reference_formula
class depense_cantine_titre_restaurant_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Dépense de cantine et de titre restaurant à cahrge de l'employeur"

    def function(self, simulation, period):
        period = period
        valeur_unitaire = simulation.calculate("titre_restaurant_valeur_unitaire", period)
        volume = simulation.calculate("titre_restaurant_volume", period)  # Compute with jours ouvrables ?
        taux_employeur = simulation.calculate('titre_restaurant_taux_employeur', period)

        return period, valeur_unitaire * volume * taux_employeur


@reference_formula
class reintegration_titre_restaurant_employeur(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Prise en charge de l'employeur des dépenses de cantine et des titres restaurants non exonérés de charges sociales"

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


@reference_formula
class nombre_jours_calendaires(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Nombre de jours calendaires travaillés"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period(u'month')
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


@reference_formula
class remboursement_transport(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Remboursement partiel des frais de transport par l'employeur"

    def function(self, simulation, period):

        remboursement_transport_base = simulation.calculate('remboursement_transport_base', period)
        return period, - .5 * remboursement_transport_base


@reference_formula
class salbrut(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Salaire brut"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period(u'month')
        avantages_en_nature = simulation.calculate('avantages_en_nature', period)
#        indemnite_residence = simulation.calculate('indemnite_residence', period)
#        primes_fonction_publique = simulation.calculate('primes_fonction_publique', period)
        primes_salaires = simulation.calculate('primes_salaires', period)
        reintegration_titre_restaurant_employeur = simulation.calculate(
            "reintegration_titre_restaurant_employeur", period
            )
        salaire_de_base = simulation.calculate('salaire_de_base', period)
#        type_sal = simulation.calculate('type_sal', period)

        return period, (
            salaire_de_base +
            primes_salaires +
            avantages_en_nature +
#            (type_sal == CAT['public_non_titulaire']) * (indemnite_residence + primes_fonction_publique) + # TODO: a rajouter quand l'assiette cotisations sociales sera corrigée
            reintegration_titre_restaurant_employeur
            )
