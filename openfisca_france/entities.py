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


import collections

from openfisca_core import entities


class Familles(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    key_plural = 'familles'
    key_singular = 'famille'
    label = u'Famille'
    max_cardinality_by_role_key = {'parents': 2}
    name_key = 'nom_famille'
    roles_key = ['parents', 'enfants']
    label_by_role_key = {
        'enfants': u'Enfants',
        'parents': u'Parents',
        }
    symbol = 'fam'


class FoyersFiscaux(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    key_plural = 'foyers_fiscaux'
    key_singular = 'foyer_fiscal'
    label = u'Déclaration d\'impôt'
    max_cardinality_by_role_key = {'declarants': 2}
    name_key = 'nom_foyer_fiscal'
    roles_key = ['declarants', 'personnes_a_charge']
    label_by_role_key = {
        'declarants': u'Déclarants',
        'personnes_a_charge': u'Personnes à charge',
        }
    symbol = 'foy'


class Individus(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    is_persons_entity = True
    key_plural = 'individus'
    key_singular = 'individu'
    label = u'Personne'
    name_key = 'nom_individu'
    symbol = 'ind'


class Menages(entities.AbstractEntity):
    column_by_name = collections.OrderedDict()
    key_plural = 'menages'
    key_singular = 'menage'
    label = u'Logement principal'
    max_cardinality_by_role_key = {'conjoint': 1, 'personne_de_reference': 1}
    name_key = 'nom_menage'
    roles_key = ['personne_de_reference', 'conjoint', 'enfants', 'autres']
    label_by_role_key = {
        'autres': u'Autres',
        'conjoint': u'Conjoint',
        'enfants': u'Enfants',
        'personne_de_reference': u'Personne de référence',
        }
    symbol = 'men'


entity_class_by_symbol = dict(
    fam = Familles,
    foy = FoyersFiscaux,
    ind = Individus,
    men = Menages,
    )


def build_entity_class_by_key_plural(entity_class_by_symbol):
    return {
        entity_class.key_plural: entity_class
        for symbol, entity_class in entity_class_by_symbol.iteritems()
        }
