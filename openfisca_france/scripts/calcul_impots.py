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


"""Use finances.gouv.fr web simulator as an API to compute income taxes."""


import argparse
import collections
import logging
import os
import sys
import urllib
import urllib2

from lxml import etree


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    request = urllib2.Request('http://www3.finances.gouv.fr/cgi-bin/calc-2014.cgi', headers = {
        'User-Agent': 'OpenFisca-Script',
        })
    response = urllib2.urlopen(request, urllib.urlencode([
        ('0DA', '1965'),
        ('1AJ', '15000'),
        ('pre_situation_famille', 'C'),
        ('pre_situation_residence', 'M'),
#        ('simplifie', '1'),
        ]))

    page_doc = etree.parse(response, etree.HTMLParser())
    fields = collections.OrderedDict()
    for element in page_doc.xpath('//input[@type="hidden"][@name]'):
        tag = element.tag.lower()
        parent = element.getparent()
        parent_tag = parent.tag.lower()
        if parent_tag == 'table':
            tr = parent[parent.index(element) - 1]
            assert tr.tag.lower() == 'tr', tr
        else:
            assert parent_tag == 'tr'
            tr = parent
        while True:
            name = etree.tostring(tr[1], encoding = unicode, method = 'text').strip().rstrip(u'*').rstrip()
            if name:
                break
            table = tr.getparent()
            tr = table[table.index(tr) - 1]
        code = element.get('name')
        fields[code] = dict(
            code = code,
            name = name,
            value = float(element.get('value').strip()),
            )
    import json
    print json.dumps(fields, encoding = 'utf-8', ensure_ascii = False, indent = 2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
