#!/usr/bin/env python

'''Fetch and print the minimal versions of Openfisca.

This script fetches and prints the minimal versions of Openfisca-Core and
Openfisca-France dependencies in order to ensure their compatibility during CI
testing.

'''

import re


def fetch_versions_from_setup():
    '''Fetch the versions from the setup.py file.'''
    with open('./setup.py') as file:
        for line in file:
            check_and_print_released(line)
            check_and_print_pre(line)


def check_and_print_released(line):
    '''Check for released versions.'''
    if version := re.search(r'(Core|France)\s*>=\s*([\d.]*)', line):
        print(f'OpenFisca-{version[1]}=={version[2]}')  # noqa: T201 <- This is to avoid flake8 print detection.


def check_and_print_pre(line):
    '''Check for pre-release versions.'''
    if pre := re.search(r'(Core|France)\s@\s(.*)\',$', line):
        print(f'{pre[2]}')  # noqa: T201 <- The same as supra.


if __name__ == '__main__':
    fetch_versions_from_setup()
