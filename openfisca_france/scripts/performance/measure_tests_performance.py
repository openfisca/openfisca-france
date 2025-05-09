'''
This files tests the performance of the test runner of openfisca-run-test on a subset of YAML tests.
It is placed in openfisca-france because it is the largest set we currently have.

Usage example:

    python openfisca_france/scripts/performance/measure_tests_performance.py
'''

import os
import time
import logging
import importlib

from openfisca_core.tools.test_runner import run_tests
from openfisca_france import CountryTaxBenefitSystem

# Create logger
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

# Baselines for comparision - unit : seconds
BASELINE_TBS_LOAD_TIME = 9.10831403732
BASELINE_YAML_TESTS_TIME = 271.448431969


# Time tax benefit system loading
start_time_tbs = time.time()
tbs = CountryTaxBenefitSystem()
time_spent_tbs = time.time() - start_time_tbs


folder = os.path.join('tests', 'mes-aides.gouv.fr')
yaml_tests_dir = importlib.resources.path('OpenFisca-France', folder)


# Time openfisca-run-test runner
start_time_tests = time.time()
run_tests(tbs, yaml_tests_dir)
time_spent_tests = time.time() - start_time_tests


def compare_performance(baseline, test_result):
    delta = (test_result - baseline) * 100 / baseline

    if test_result > baseline * 1.2:
        logger.warning('The perfomance seems to have worsen by {} %.'.format(delta))
    elif test_result < baseline * 0.8:
        logger.info('The performance seems to have been improved by {} %.'.format(delta))
    else:
        logging.info('The performance seems steady ({} %).'.format(delta))


logger.info('Generate Tax Benefit System: --- {}s seconds ---'.format(time_spent_tbs))
compare_performance(BASELINE_TBS_LOAD_TIME, time_spent_tbs)

logger.info('Pass Mes-aides tests: --- {}s seconds ---'.format(time_spent_tests))
compare_performance(BASELINE_YAML_TESTS_TIME, time_spent_tests)
