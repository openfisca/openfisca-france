#! /usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name = "OpenFisca-France",
    version = "39.0.2",
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
        ("share/openfisca/openfisca-france", ["CHANGELOG.md", "LICENSE.AGPL.txt", "README.md"]),
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
            "autopep8 ==1.4.3",
            "flake8 >=3.5.0,<3.8.0",
            "flake8-print",
            "pycodestyle >=2.3.0,<2.6.0",  # To avoid incompatibility with flake
            "pytest <5.0",
            "scipy >= 0.17",  # Only used to test de_net_a_brut reform
            "requests >= 2.8",
            "yamllint >=1.11.1,<1.16"
            ],
        },
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        "OpenFisca-Core >=29.0, <30.0",
        ],
    message_extractors = {"openfisca_france": [
        ("**.py", "python", None),
        ]},
    packages = find_packages(exclude=["openfisca_france.tests*"]),
    )
