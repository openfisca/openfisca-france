# -*- coding: utf-8 -*-

"""
This files tests the performance of the YAML test runner (openfisca-run-test).
It is placed in openfisca-france because it is the largest set we currently have.
"""

import os
import time
import pkg_resources
from openfisca_core.tools.test_runner import run_tests
from openfisca_france import CountryTaxBenefitSystem

# Time tax benefit system loading
start_time_tbs = time.time()
tbs = CountryTaxBenefitSystem()
time_spent_tbs = time.time() - start_time_tbs


openfisca_france_dir = pkg_resources.get_distribution('OpenFisca-France').location
yaml_tests_dir = os.path.join(openfisca_france_dir, 'tests', 'mes-aides.gouv.fr')


# Time openfisca-run-test runner
start_time_tests = time.time()
run_tests(tbs, yaml_tests_dir)
time_spent_tests = time.time() - start_time_tests

print("Generate Tax Benefit System: --- {}s seconds ---".format(time_spent_tbs))
print("Pass Mes-aides tests: --- {}s seconds ---".format(time_spent_tests))
