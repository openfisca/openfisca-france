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


from numpy import logical_not as not_, logical_or as or_
from numpy.core.defchararray import startswith


from ..base import *  # noqa analysis:ignore


build_column('coloc', BoolCol(label = u"Vie en colocation"))

build_column('depcom', FixedStrCol(label = u"Code INSEE (depcom) du lieu de résidence", entity = 'men', max_length = 5))


build_column('logement_chambre', BoolCol(label = u"Le logement est considéré comme une chambre"))

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Loyer ou mensualité d'emprunt pour un primo-accédant",
    name = "loyer",
    set_input = set_input_divide_by_period,
)

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u'Charges locatives',
    name = 'charges_locatives',
    set_input = set_input_divide_by_period,
)

build_column(
    'proprietaire_proche_famille',
    BoolCol(
        entity = "fam",
        label = u"Le propriétaire du logement a un lien de parenté avec la personne de référence ou son conjoint",
    ),
)

reference_input_variable(
    name = 'statut_occupation',
    column = EnumCol(
        enum = Enum([
            u"Non renseigné",
            u"Accédant à la propriété",
            u"Propriétaire (non accédant) du logement",
            u"Locataire d'un logement HLM",
            u"Locataire ou sous-locataire d'un logement loué vide non-HLM",
            u"Locataire ou sous-locataire d'un logement loué meublé ou d'une chambre d'hôtel",
            u"Logé gratuitement par des parents, des amis ou l'employeur",
            u"Locataire d'un foyer (résidence universitaire, maison de retraite, foyer de jeune travailleur, résidence sociale...)",
            u"Sans domicile stable"])
    ),
    entity_class = Menages,
    label = u"Statut d'occupation",
    set_input = set_input_dispatch_by_period,
)


@reference_formula
class residence_dom(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        residence_guadeloupe = simulation.calculate('residence_guadeloupe', period)
        residence_martinique = simulation.calculate('residence_martinique', period)
        residence_guyane = simulation.calculate('residence_guyane', period)
        residence_reunion = simulation.calculate('residence_reunion', period)
        residence_mayotte = simulation.calculate('residence_mayotte', period)
        return period, or_(or_(residence_guadeloupe, residence_martinique), or_(or_(residence_reunion, residence_guyane), residence_mayotte))


@reference_formula
class residence_guadeloupe(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '971')


@reference_formula
class residence_martinique(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '972')


@reference_formula
class residence_guyane(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '973')


@reference_formula
class residence_reunion(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '974')


@reference_formula
class residence_mayotte(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles

    def function(self, simulation, period):
        depcom_holder = simulation.compute('depcom', period)

        depcom = self.cast_from_entity_to_roles(depcom_holder)
        depcom = self.filter_role(depcom, role = CHEF)
        return period, startswith(depcom, '976')
