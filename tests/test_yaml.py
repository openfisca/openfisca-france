#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from nose.tools import nottest

from openfisca_core.tools.test_runner import generate_tests

from cache import tax_benefit_system

nottest(generate_tests)

def test():
    tests_directory = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    test_generator = generate_tests(tax_benefit_system, tests_directory)

    for test in test_generator:
        yield test
