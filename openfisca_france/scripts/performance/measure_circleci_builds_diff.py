'''
This script takes in two CircleCI build numbers
(should be the `build_python2` and `build_python3` of the same workflow)
and outputs if their mean runtime is in the same ball park
as the master branch's mean runtime for the same builds.

Usage example:

    python openfisca_france/scripts/performance/measure_circleci_builds_diff.py 1717 1716
'''

import sys
import requests
import json
import logging


logging.basicConfig(level=logging.INFO)

if len(sys.argv) < 2:
    raise AttributeError(
        '''
        This script needs two CircleCI build numbers to work,
        e.g. python openfisca_france/scripts/performance/measure_circleci_builds_diff.py 1717 1716
        '''
        )

python2_build_number = sys.argv[1]
python3_build_number = sys.argv[2]


MAX_RATIO_STANDARD_DEVIATION = 10
MIN_NUMBER_OF_MASTER_BUILDS = 5


def get_master_branch_performance():
    '''
    Accesses the CircleCI API and gets the info for all available master branch builds.
    :return: a Dict with the master branch build time statistics
    '''
    def mean(numbers):
        return sum(numbers, 0.0) / len(numbers)

    def standard_deviation(numbers):
        mean_of_numbers = mean(numbers)
        variance = mean([(x - mean_of_numbers)**2 for x in numbers])
        return variance**0.5

    api_url = 'https://circleci.com/api/v1.1/project/github/openfisca/openfisca-france/tree/master'
    response = requests.get(api_url)
    if response.status_code == 200:
        response_python = json.loads(response.content.decode('utf-8'))
    else:
        response_python = None
        logging.warning('No connection to the API - Aborting')
        exit(0)

    builds = []

    for response in response_python:
        job_name = response['workflows']['job_name']
        job_status = response['status']

        if job_status == 'success' and (job_name == 'build_python2' or job_name == 'build_python3'):
            builds.append(response['build_time_millis'])

    if len(builds) < MIN_NUMBER_OF_MASTER_BUILDS:
        logging.warning('Too few circle builds on master branch : {} builds'.format(len(builds)))
        exit(1)
    else:
        logging.info('The master branch has {} builds available for analysis.'.format(len(builds)))

    results = dict()
    results['mean'] = mean(builds)
    results['standard_deviation'] = standard_deviation(builds)
    ratio_sd = round(results['standard_deviation'] / results['mean'] * 100, 2)
    if ratio_sd > MAX_RATIO_STANDARD_DEVIATION:
        logging.warning('The standard deviation is unsound : {}'.format(ratio_sd))
        exit(1)
    return results


def get_current_build_performance(python2_build_number, python3_build_number):
    '''
    get the build time for the tests
    :param python2_build_number: a circle ci build number
    :param python3_build_number: a circle ci build number
    :return: a number of milliseconds the build took
    '''
    builds = [python2_build_number, python3_build_number]
    current_build_performance = 0
    for build in builds:
        api_url = 'https://circleci.com/api/v1.1/project/github/openfisca/openfisca-france/{}'.format(build)
        response = requests.get(api_url)
        if response.status_code == 200:
            response_python = json.loads(response.content.decode('utf-8'))
        else:
            logging.warning('Cannot reach build - Aborting')
            exit(1)
        current_build_performance += response_python['build_time_millis']

    return current_build_performance / 2


master_branch = get_master_branch_performance()
current_build = get_current_build_performance(python2_build_number, python3_build_number)
current_master_ratio = abs(master_branch['mean'] - current_build) / master_branch['mean'] * 100

if current_build > master_branch['mean'] * (1. + (MAX_RATIO_STANDARD_DEVIATION / 100.)):
    sys.exit('This build makes the test performance more than {}% worst : {}%'.format(MAX_RATIO_STANDARD_DEVIATION, current_master_ratio))

elif current_build > master_branch['mean'] + master_branch['standard_deviation']:
    sys.exit('This build may be making the test performance worst : {}%'.format(current_master_ratio))

elif current_build < master_branch['mean'] + master_branch['standard_deviation']:
    logging.info('Performances are good : {}%'.format(current_master_ratio))
    sys.exit(0)
