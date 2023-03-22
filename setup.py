#! /usr/bin/env python

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of our README file for PyPi
this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
    name = 'OpenFisca-France',
    version = '148.0.0',
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
            'scipy',
            ],
        'de_net_a_brut': [
            'scipy',
            ],
        'taxipp': [
            'pandas',
            ],
        'dev': [
            'autopep8',
            'flake8',
            'flake8-print',
            'flake8-quotes',
            'pytest',
            'scipy',  # Only used to test de_net_a_brut reform
            'requests',
            'yamllint'
            ],
        'casd-dev': [
            # Same as dev with packages not available at CASD removed
            'autopep8',
            'pytest',
            'requests',
            'scipy',  # Only used to test de_net_a_brut reform
            ]
        },
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        # 'OpenFisca-Core >=35.8.0,<36.0',
        'OpenFisca-Core @ git+https://github.com/openfisca/openfisca-core.git@version_leap',
        ],
    packages = find_packages(exclude = [
        'openfisca_france.tests*',
        'openfisca_france.assets.taxe_habitation.source*',
        ]),
    )
