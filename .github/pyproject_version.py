# Read package version in pyproject.toml and replace it in .conda/recipe.yaml

import argparse
import logging
import re

logging.basicConfig(level=logging.INFO)


def get_versions():
    openfisca_core_api = None
    openfisca_france = None
    with open('./pyproject.toml', 'r') as file:
        content = file.read()
    # Extract the version of openfisca_france
    version_match = re.search(r'^version\s*=\s*"([\d.]*)"', content, re.MULTILINE)
    if version_match:
        openfisca_france = version_match.group(1)
    # Extract dependencies
    version = re.search(r'openfisca-core\[web-api\]\s*(>=\s*[\d\.]*,\s*<\d*)"', content, re.MULTILINE)
    if version:
        openfisca_core_api = version.group(1)
    return {
        'openfisca_france': openfisca_france,
        'openfisca_core_api': openfisca_core_api.replace(' ', ''),
        }


def replace_in_file(filepath: str, info: dict):
    '''
    ::filepath:: Path to meta.yaml, with filename
    ::info:: Dict with information to populate
    '''
    with open(filepath, 'rt') as fin:
        meta = fin.read()
    # Replace with info from pyproject.toml
    meta = meta.replace('888.888.888', info['openfisca_france'])
    meta = meta.replace('>=43,<44', info['openfisca_core_api'])
    with open(filepath, 'wt') as fout:
        fout.write(meta)
    logging.info(f'File {filepath} has been updated with informations from pyproject.toml.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--replace', type=bool, default=False, required=False, help='replace in file')
    parser.add_argument('-f', '--filename', type=str, default='.conda/recipe.yaml', help='Path to recipe.yaml, with filename')
    parser.add_argument('-o', '--only_package_version', type=str, default='.conda/recipe.yaml', help='Path to recipe.yaml, with filename')
    args = parser.parse_args()
    info = get_versions()
    file = args.filename
    if args.only_package_version:
        logging.info(f'{info["openfisca_france"]}')
        exit()
    logging.info(f'Versions :\n{info}')
    if args.replace:
        logging.info(f'Replace in {file}')
        replace_in_file(file, info)
    else:
        logging.info('Dry mode, no replace made')

