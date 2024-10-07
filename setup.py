#! /usr/bin/env python

from setuptools import setup, find_namespace_packages
from pathlib import Path

# Read the contents of our README file for PyPi
this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
    name = 'OpenFisca-France',
    version = '168.2.1',
    author = 'OpenFisca Team',
    author_email = 'contact@openfisca.fr',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Information Analysis',
        ],
    description = 'French tax and benefit system for OpenFisca',
    keywords = 'benefit france microsimulation social tax',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    license_files = ('LICENSE.AGPL.txt',),
    url = 'https://github.com/openfisca/openfisca-france',
    long_description=long_description,
    long_description_content_type='text/markdown',

    data_files = [
        (
            'share/openfisca/openfisca-france',
            ['CHANGELOG.md', 'README.md'],
            ),
        ],
    extras_require = {
        'inversion_revenus': [
            'scipy >=1.10.1, <2.0',
            ],
        'de_net_a_brut': [
            'scipy >=1.10.1, <2.0',
            ],
        'taxipp': [
            'pandas >=1.5.3, <2.0',
            ],
        'dev': [
            'autopep8 >=2.0.2, <3.0',
            'flake8 >=6.0.0, <7.0.0',
            'flake8-print >=5.0.0, <6.0.0',
            'flake8-quotes >=3.3.2',
            'pytest >=7.2.2, <8.0',
            'scipy >=1.10.1, <2.0',  # Only used to test de_net_a_brut reform
            'requests >=2.28.2, <3.0',
            'yamllint >=1.30.0, <2.0'
            ],
        'casd-dev': [
            # Same as dev with packages not available at CASD removed
            'autopep8 >=2.0.2, <3.0',
            'pytest >=7.2.2, <8.0',
            'requests >=2.28.2, <3.0',
            'scipy >=1.10.1, <2.0',  # Only used to test de_net_a_brut reform
            ]
        },
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'OpenFisca-Core >=40.0.1, <42',
        ],
    packages = find_namespace_packages(exclude = [
        'openfisca_france.tests*',
        'openfisca_france.assets.taxe_habitation.source*',
        ]),
    )
