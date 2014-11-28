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


import functools

from openfisca_core.columns import AgeCol, BoolCol, build_column, FloatCol
from openfisca_core.enumerations import Enum
from openfisca_core.formulas import (alternative_function, AlternativeFormulaColumn, dated_function, DatedFormulaColumn,
    EntityToPersonColumn, make_reference_formula_decorator, PersonToEntityColumn, select_function, SelectFormulaColumn,
    SimpleFormulaColumn)

from ..entities import entity_class_by_symbol, Familles, FoyersFiscaux, Individus, Menages


__all__ = [
    'AgeCol',
    'alternative_function',
    'AlternativeFormulaColumn',
    'build_column',
    'BoolCol',
    'CAT',
    'dated_function',
    'DatedFormulaColumn',
    'EntityToPersonColumn',
    'Enum',
    'Familles',
    'FloatCol',
    'FoyersFiscaux',
    'Individus',
    'Menages',
    'PersonToEntityColumn',
    'QUIFAM',
    'QUIFOY',
    'QUIMEN',
    'reference_formula',
    'SelectFormulaColumn',
    'select_function',
    'SimpleFormulaColumn',
    'TAUX_DE_PRIME',
    ]

CAT = Enum(['prive_non_cadre',
            'prive_cadre',
            'public_titulaire_etat',
            'public_titulaire_militaire',
            'public_titulaire_territoriale',
            'public_titulaire_hospitaliere',
            'public_non_titulaire'])

QUIFAM = Enum(['chef', 'part', 'enf1', 'enf2', 'enf3', 'enf4', 'enf5', 'enf6', 'enf7', 'enf8', 'enf9'])
QUIFOY = Enum(['vous', 'conj', 'pac1', 'pac2', 'pac3', 'pac4', 'pac5', 'pac6', 'pac7', 'pac8', 'pac9'])
QUIMEN = Enum(['pref', 'cref', 'enf1', 'enf2', 'enf3', 'enf4', 'enf5', 'enf6', 'enf7', 'enf8', 'enf9'])

TAUX_DE_PRIME = 1 / 4  # primes_fonction_publique (hors suppl. familial et indemnité de résidence)/rémunération brute


# Functions and decorators


build_column = functools.partial(
    build_column,
    entity_class_by_symbol = entity_class_by_symbol,
    )

reference_formula = make_reference_formula_decorator(entity_class_by_symbol = entity_class_by_symbol)
