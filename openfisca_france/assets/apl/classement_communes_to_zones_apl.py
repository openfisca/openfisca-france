#! /usr/bin/env python
# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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


"""Produce zones_apl.json file from TXT files and comsimp file from INSEE."""


import argparse
import codecs
import csv
import json
import logging
import os
import sys
import unicodedata


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def clean(string):
    return unicodedata.normalize('NFKD', string.strip().replace(u'\u2019', u"'").upper()).encode('ascii', 'ignore')


def get_communes_by_departement_from_zone_file(file_path):
    communes_by_departement = {}
    with codecs.open(file_path, encoding = 'utf-8') as zone_file:
        for row in zone_file:
            if ' ' in row:
                departement, communes_str = row.split(' ', 1)
                communes = [
                    clean(commune)
                    for commune in communes_str.split(',')
                    ]
            else:
                departement = row.strip()
                communes = None
            if departement not in communes_by_departement:
                communes_by_departement[departement] = None
            if communes:
                if communes_by_departement[departement] is None:
                    communes_by_departement[departement] = []
                communes_by_departement[departement].extend(communes)
    return communes_by_departement


def iter_depcom(communes_by_departement, commune_code_by_departement_then_commune):
    for departement, communes in communes_by_departement.iteritems():
        if communes is not None:
            for commune in communes:
                if departement in commune_code_by_departement_then_commune:
                    if commune in commune_code_by_departement_then_commune[departement]:
                        commune_code = commune_code_by_departement_then_commune[departement][commune]
                        depcom = departement + commune_code
                        yield depcom
                    else:
                        log.error(u'commune {} of département {} not in INSEE file'.format(commune, departement))
                else:
                    log.error(u'département {} not in INSEE file'.format(departement))


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('--comsimp', required = True, help = u"INSEE communes file")
    parser.add_argument('--zone-1', required = True, help = u"TXT file containing zone 1 communes by département")
    parser.add_argument('--zone-2', required = True, help = u"TXT file containing zone 2 communes by département")
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = u"increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING)

    commune_code_by_departement_then_commune = {}
    with open(args.comsimp) as comsimp_file:
        csv_reader = csv.DictReader(comsimp_file, delimiter = '\t')
        for latin1_row in csv_reader:
            row = {key: value.decode('latin1') for key, value in latin1_row.iteritems()}
            # TODO concatenate accents
            commune_code_by_departement_then_commune.setdefault(row['DEP'], {})[row['NCC']] = row['COM']

    zones_apl = {
        1: list(iter_depcom(
            get_communes_by_departement_from_zone_file(args.zone_1),
            commune_code_by_departement_then_commune,
            )),
        2: list(iter_depcom(
            get_communes_by_departement_from_zone_file(args.zone_2),
            commune_code_by_departement_then_commune,
            )),
        }
    print json.dumps(zones_apl, encoding = 'utf-8', ensure_ascii = False, indent = 2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
