#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from nose.tools import nottest

from openfisca_core.tools.test_runner import generate_tests

from openfisca_france.tests import base

nottest(generate_tests)

options_by_dir = {
    # 'calculateur_impots': {
    #     'default_absolute_error_margin': 0.5,
    #     'reforms' : ['inversion_revenus'],
    #     },
    'fiches_de_paie': {},
    'formulas': {},
    'mes-aides.gouv.fr': {
        'default_relative_error_margin': 0.02
        },
    'ui.openfisca.fr': {},
    'scipy': {
        'reforms':['de_net_a_brut'],
        'requires': 'scipy'
        },
}


def test():
    for directory, options in options_by_dir.iteritems():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), directory))

        if options.get('requires'):
            # Check if the required package was successfully imported in tests/base.py
            if getattr(base, options.get('requires')) is None:
                continue

        if not options.get('default_relative_error_margin') and not options.get('default_absolute_error_margin'):
            options['default_absolute_error_margin'] = 0.005

        reform_keys = options.get('reforms')
        tax_benefit_system = base.get_cached_composed_reform(
            reform_keys = reform_keys,
            tax_benefit_system = base.tax_benefit_system,
            ) if reform_keys is not None else base.tax_benefit_system

        test_generator = generate_tests(tax_benefit_system, path, options)

        for test in test_generator:
            yield test

