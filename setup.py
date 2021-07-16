#! /usr/bin/env python

from setuptools import setup, find_packages


setup(
    name = "OpenFisca-France",
    version = "56.0.2",
    author = "OpenFisca Team",
    author_email = "contact@openfisca.fr",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Information Analysis",
        ],
    description = "French tax and benefit system for OpenFisca",
    keywords = "benefit france microsimulation social tax",
    license = "http://www.fsf.org/licensing/licenses/agpl-3.0.html",
    url = "https://github.com/openfisca/openfisca-france",

    data_files = [
        (
            "share/openfisca/openfisca-france",
            ["CHANGELOG.md", "LICENSE.AGPL.txt", "README.md"],
            ),
        ],
    extras_require = {
        "inversion_revenus": [
            "scipy >= 0.17",
            ],
        "de_net_a_brut": [
            "scipy >= 0.17",
            ],
        "taxipp": [
            "pandas >= 0.13",
            ],
        "dev": [
            "autopep8 ==1.5.7",
            "flake8 >=3.8.0,<3.10.0",
            "flake8-print",
            "pytest >= 5.0.0, < 7.0.0",
            "scipy >= 0.17",  # Only used to test de_net_a_brut reform
            "requests >= 2.8",
            "yamllint >=1.11.1,<1.27"
            ],
        "casd-dev": [
            # Same as dev with packages not available at CASD removed
            "autopep8 >=1.3.2",
            "pytest >= 5.0.0, < 7.0.0",
            "requests >= 2.8",
            "scipy >= 0.17",  # Only used to test de_net_a_brut reform
            ]
        },
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        "OpenFisca-Core >=35.2.0,<36.0",
        ],
    packages = find_packages(exclude = [
        "openfisca_france.tests*",
        "openfisca_france.assets.taxe_habitation.source*",
        ]),
    )
