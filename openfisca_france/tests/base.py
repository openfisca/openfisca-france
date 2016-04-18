# -*- coding: utf-8 -*-

from openfisca_core import reforms
from openfisca_core.tools import assert_near

from .. import init_country
from ..reforms import (
    aides_ville_paris,
    allocations_familiales_imposables,
    cesthra_invalidee,
    plf2016,
    plf2016_ayrault_muet,
    plf2015,
    plfr2014,
    trannoy_wasmer,
    )


__all__ = [
    'assert_near',
    'get_cached_composed_reform',
    'get_cached_reform',
    'tax_benefit_system',
    'TaxBenefitSystem',
    ]


# Initialize a tax_benefit_system

TaxBenefitSystem = init_country()
tax_benefit_system = TaxBenefitSystem()


# Reforms cache, used by long scripts like test_yaml.py

build_reform_function_by_key = {
    'aides_ville_paris': aides_ville_paris.build_reform,
    'allocations_familiales_imposables': allocations_familiales_imposables.build_reform,
    'cesthra_invalidee': cesthra_invalidee.build_reform,
    'plf2016': plf2016.build_reform,
    'ayrault_muet': plf2016_ayrault_muet.build_reform,
    'plf2016_counterfactual': plf2016.build_counterfactual_reform,
    'plf2016_counterfactual_2014': plf2016.build_counterfactual_2014_reform,
    'plf2015': plf2015.build_reform,
    'plfr2014': plfr2014.build_reform,
    'trannoy_wasmer': trannoy_wasmer.build_reform,
    }

# Only use the following reform if scipy can be imported
try:
    import scipy
except ImportError:
    scipy = None

if scipy is not None:
    from ..reforms import de_net_a_brut
    build_reform_function_by_key['de_net_a_brut'] = de_net_a_brut.build_reform

reform_by_full_key = {}


def get_cached_composed_reform(reform_keys, tax_benefit_system):
    full_key = '.'.join(
        [tax_benefit_system.full_key] + reform_keys
        if isinstance(tax_benefit_system, reforms.AbstractReform)
        else reform_keys
        )
    composed_reform = reform_by_full_key.get(full_key)
    if composed_reform is None:
        build_reform_functions = []
        for reform_key in reform_keys:
            assert reform_key in build_reform_function_by_key, \
                'Error loading cached reform "{}" in build_reform_functions'.format(reform_key)
            build_reform_function = build_reform_function_by_key[reform_key]
            build_reform_functions.append(build_reform_function)
        composed_reform = reforms.compose_reforms(
            build_functions_and_keys = zip(build_reform_functions, reform_keys),
            tax_benefit_system = tax_benefit_system,
            )
        assert full_key == composed_reform.full_key
        reform_by_full_key[full_key] = composed_reform
    return composed_reform


def get_cached_reform(reform_key, tax_benefit_system):
    return get_cached_composed_reform([reform_key], tax_benefit_system)
