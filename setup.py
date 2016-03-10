#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" -- a versatile microsimulation free software"""


from setuptools import setup, find_packages


setup(
    name = 'OpenFisca-France',
    version = '0.5.4.1',

    author = 'OpenFisca Team',
    author_email = 'contact@openfisca.fr',
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Information Analysis",
        ],
    description = u'French tax and benefit system for OpenFisca',
    keywords = 'benefit france microsimulation social tax',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url = 'https://github.com/openfisca/openfisca-france',

    data_files = [
        ('share/locale/fr/LC_MESSAGES', ['openfisca_france/i18n/fr/LC_MESSAGES/openfisca-france.mo']),
        ('share/openfisca/openfisca-france', ['CHANGELOG.md', 'LICENSE', 'README.md']),
        ],
    extras_require = {
        'inversion_revenus': [
            'scipy >= 0.12',
            ],
        'taxipp': [
            'pandas >= 0.13',
            ],
        'test': [
            'nose',
            ],
        },
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'Babel >= 0.9.4',
        'Biryani[datetimeconv] >= 0.10.4',
        'numpy >= 1.6',
        'OpenFisca-Core >= 0.5.4',
        'PyYAML >= 3.10',
        'requests >= 2.8',
        ],
    message_extractors = {'openfisca_france': [
        ('**.py', 'python', None),
        ]},
    packages = find_packages(exclude=['openfisca_france.tests*']),
    test_suite = 'nose.collector',
    )
