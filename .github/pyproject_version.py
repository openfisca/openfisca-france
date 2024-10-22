# Read package version in pyproject.toml and replace it in .conda/recipe.yaml

import argparse
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(message)s')
PACKAGE_VERSION = 'X.X.X'
CORE_VERSION = '>=43,<44'
NUMPY_VERSION = '>=1.24.3,<2'


def get_versions():
    '''
    Read package version and deps in pyproject.toml
    '''
    openfisca_core_api = None
    openfisca_france = None
    with open('./pyproject.toml', 'r') as file:
        content = file.read()
    # Extract the version of openfisca_france
    version_match = re.search(r'^version\s*=\s*"([\d.]*)"', content, re.MULTILINE)
    if version_match:
        openfisca_france = version_match.group(1)
    else:
        raise Exception('Package version not found in pyproject.toml')
    # Extract dependencies
    version = re.search(r'openfisca-core\[web-api\]\s*(>=\s*[\d\.]*,\s*<\d*)"', content, re.MULTILINE)
    if version:
        openfisca_core_api = version.group(1)
    version = re.search(r'numpy\s*(>=\s*[\d\.]*,\s*<\d*)"', content, re.MULTILINE)
    if version:
        numpy = version.group(1)
    if not openfisca_core_api or not numpy:
        raise Exception('Dependencies not found in pyproject.toml')
    return {
        'openfisca_france': openfisca_france,
        'openfisca_core_api': openfisca_core_api.replace(' ', ''),
        'numpy': numpy.replace(' ', ''),
        }


def replace_in_file(filepath: str, info: dict):
    '''
    ::filepath:: Path to meta.yaml, with filename
    ::info:: Dict with information to populate
    '''
    with open(filepath, 'rt') as fin:
        meta = fin.read()
    # Replace with info from pyproject.toml
    if PACKAGE_VERSION not in meta:
        raise Exception(f'{PACKAGE_VERSION=} not found in {filepath}')
    meta = meta.replace(PACKAGE_VERSION, info['openfisca_france'])
    if CORE_VERSION not in meta:
        raise Exception(f'{CORE_VERSION=} not found in {filepath}')
    meta = meta.replace(CORE_VERSION, info['openfisca_core_api'])
    if NUMPY_VERSION not in meta:
        raise Exception(f'{NUMPY_VERSION=} not found in {filepath}')
    meta = meta.replace(NUMPY_VERSION, info['numpy'])
    with open(filepath, 'wt') as fout:
        fout.write(meta)
    logging.info(f'File {filepath} has been updated with informations from pyproject.toml.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--replace', type=bool, default=False, required=False, help='replace in file')
    parser.add_argument('-f', '--filename', type=str, default='.conda/recipe.yaml', help='Path to recipe.yaml, with filename')
    parser.add_argument('-o', '--only_package_version', type=bool, default=False, help='Only display current package version')
    args = parser.parse_args()
    info = get_versions()
    file = args.filename
    if args.only_package_version:
        print(f'{info["openfisca_france"]}')  # noqa: T201
        exit()
    logging.info('Versions :')
    print(info)  # noqa: T201
    if args.replace:
        logging.info(f'Replace in {file}')
        replace_in_file(file, info)
    else:
        logging.info('Dry mode, no replace made')
