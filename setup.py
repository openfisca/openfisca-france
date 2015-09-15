#! /usr/bin/env python
# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


""" -- a versatile microsimulation free software"""


from setuptools import setup, find_packages


setup(
    name = 'OpenFisca-France',
    version = '0.5.3.dev0',

    author = 'OpenFisca Team',
    author_email = 'contact@openfisca.fr',
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Information Analysis",
        ],
    description = u'France specific model for OpenFisca',
    keywords = 'benefit france microsimulation social tax',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url = 'https://github.com/openfisca/openfisca-france',

    data_files = [
        ('share/locale/fr/LC_MESSAGES', ['openfisca_france/i18n/fr/LC_MESSAGES/openfisca-france.mo']),
        ],
    install_requires = [
        'Babel >= 0.9.4',
        'Biryani >= 0.10.4',
        'numpy >= 1.6',
        'OpenFisca-Core >= 0.5.0',
        'PyYAML >= 3.10',
        # 'scipy >= 0.12',  # Only for inversion_revenus reform
        # 'pandas >= 0.13',  # Only for taxipp_utils.py which is ignored in Makefile
        ],
    message_extractors = {'openfisca_france': [
        ('**.py', 'python', None),
        ]},
    packages = find_packages(),
    test_suite = 'nose.collector',
    )
