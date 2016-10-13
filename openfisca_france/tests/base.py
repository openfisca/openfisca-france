# -*- coding: utf-8 -*-

from openfisca_core.reforms import Reform, compose_reforms
from openfisca_core.tools import assert_near

from .. import FranceTaxBenefitSystem
from ..reforms import (
    allocations_familiales_imposables,
    cesthra_invalidee,
    inversion_directe_salaires,
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
    ]

tax_benefit_system = FranceTaxBenefitSystem()

# Reforms cache, used by long scripts like test_yaml.py
# The reforms commented haven't been adapted to the new core API yet.
reform_list = {
    'allocations_familiales_imposables': allocations_familiales_imposables.allocations_familiales_imposables,
    'cesthra_invalidee': cesthra_invalidee.cesthra_invalidee,
    'inversion_directe_salaires': inversion_directe_salaires.inversion_directe_salaires,
    'plf2016': plf2016.plf2016,
    'ayrault_muet': plf2016_ayrault_muet.ayrault_muet,
    'plf2016_counterfactual': plf2016.plf2016_counterfactual,
    'plf2016_counterfactual_2014': plf2016.plf2016_counterfactual_2014,
    'plf2015': plf2015.plf2015,
    'plfr2014': plfr2014.plfr2014,
    'trannoy_wasmer': trannoy_wasmer.trannoy_wasmer,
    }

# Only use the following reform if scipy can be imported
try:
    import scipy
except ImportError:
    scipy = None

if scipy is not None:
    from ..reforms import de_net_a_brut
    reform_list['de_net_a_brut'] = de_net_a_brut.de_net_a_brut

reform_by_full_key = {}


def get_cached_composed_reform(reform_keys, tax_benefit_system):
    full_key = '.'.join(
        [tax_benefit_system.full_key] + reform_keys
        if isinstance(tax_benefit_system, Reform)
        else reform_keys
        )
    composed_reform = reform_by_full_key.get(full_key)

    if composed_reform is None:
        reforms = []
        for reform_key in reform_keys:
            assert reform_key in reform_list, \
                'Error loading cached reform "{}" in build_reform_functions'.format(reform_key)
            reform = reform_list[reform_key]
            reforms.append(reform)
        composed_reform = compose_reforms(
            reforms = reforms,
            tax_benefit_system = tax_benefit_system,
            )
        assert full_key == composed_reform.full_key, (full_key, composed_reform.full_key)
        reform_by_full_key[full_key] = composed_reform
    return composed_reform


def get_cached_reform(reform_key, tax_benefit_system):
    return get_cached_composed_reform([reform_key], tax_benefit_system)
