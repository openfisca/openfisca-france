# -*- coding: utf-8 -*-

from datetime import date

from openfisca_core.columns import (AgeCol, BoolCol, DateCol, EnumCol, FixedStrCol, FloatCol, IntCol,
    PeriodSizeIndependentIntCol, StrCol)
from openfisca_core.enumerations import Enum
from openfisca_core.formulas import (calculate_output_add, calculate_output_add_divide, calculate_output_divide,
    dated_function, DatedVariable, EntityToPersonColumn, missing_value, PersonToEntityColumn,
    set_input_dispatch_by_period, set_input_divide_by_period, Variable)
from openfisca_core.base_functions import (
    last_duration_last_value,
    requested_period_added_value,
    requested_period_default_value,
    requested_period_last_or_next_value,
    requested_period_last_value,
    )
from openfisca_core.formula_helpers import apply_thresholds, switch

from ..entities import Familles, FoyersFiscaux, Individus, Menages


__all__ = [
    'AgeCol',
    'apply_thresholds',
    'BoolCol',
    'calculate_output_add',
    'calculate_output_add_divide',
    'calculate_output_divide',
    'CAT',
    'CHEF',
    'CONJ',
    'CREF',
    'date',
    'DateCol',
    'dated_function',
    'DatedVariable',
    'ENFS',
    'EntityToPersonColumn',
    'Enum',
    'EnumCol',
    'Familles',
    'FixedStrCol',
    'FloatCol',
    'FoyersFiscaux',
    'Individus',
    'IntCol',
    'last_duration_last_value',
    'Menages',
    'missing_value',
    'PAC1',
    'PAC2',
    'PAC3',
    'PART',
    'PeriodSizeIndependentIntCol',
    'PersonToEntityColumn',
    'PREF',
    'QUIFAM',
    'QUIFOY',
    'QUIMEN',
    'requested_period_added_value',
    'requested_period_default_value',
    'requested_period_last_or_next_value',
    'requested_period_last_value',
    'set_input_dispatch_by_period',
    'set_input_divide_by_period',
    'switch',
    'Variable',
    'StrCol',
    'TAUX_DE_PRIME',
    'VOUS',
    ]

CAT = Enum([
    'prive_non_cadre',
    'prive_cadre',
    'public_titulaire_etat',
    'public_titulaire_militaire',
    'public_titulaire_territoriale',
    'public_titulaire_hospitaliere',
    'public_non_titulaire',
    ])

TAUX_DE_PRIME = 1 / 4  # primes_fonction_publique (hors suppl. familial et indemnité de résidence)/rémunération brute

QUIFAM = Enum(['chef', 'part', 'enf1', 'enf2', 'enf3', 'enf4', 'enf5', 'enf6', 'enf7', 'enf8', 'enf9'])
QUIFOY = Enum(['vous', 'conj', 'pac1', 'pac2', 'pac3', 'pac4', 'pac5', 'pac6', 'pac7', 'pac8', 'pac9'])
QUIMEN = Enum(['pref', 'cref', 'enf1', 'enf2', 'enf3', 'enf4', 'enf5', 'enf6', 'enf7', 'enf8', 'enf9'])

CHEF = QUIFAM['chef']
CONJ = QUIFOY['conj']
CREF = QUIMEN['cref']
ENFS = [
    QUIFAM['enf1'], QUIFAM['enf2'], QUIFAM['enf3'], QUIFAM['enf4'], QUIFAM['enf5'], QUIFAM['enf6'], QUIFAM['enf7'],
    QUIFAM['enf8'], QUIFAM['enf9'],
    ]
PAC1 = QUIFOY['pac1']
PAC2 = QUIFOY['pac2']
PAC3 = QUIFOY['pac3']
PART = QUIFAM['part']
PREF = QUIMEN['pref']
VOUS = QUIFOY['vous']
