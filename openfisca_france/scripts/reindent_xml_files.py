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


"""Reindent XML files."""


import argparse
import logging
import os
import sys
import xml.etree.ElementTree as etree

from openfisca_france import decompositions, param


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)


def indent(elem, level = 0):
    # cf http://effbot.org/zone/element-lib.htm
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    for module in (decompositions, param):
        dir = os.path.dirname(module.__file__)
        for filename in os.listdir(dir):
            if not filename.endswith('.xml'):
                continue
            xml_file_path = os.path.join(dir, filename)
            try:
                tree = etree.parse(xml_file_path)
            except (AttributeError, etree.ParseError):
                log.exception(u'Ignoring "{}" because of a syntax error in XML'.format(xml_file_path))
                continue
            root_element = tree.getroot()
            indent(root_element)
            with open(xml_file_path, 'w') as xml_file:
                xml_file.write(etree.tostring(root_element, encoding = 'utf-8'))

    return 0


if __name__ == "__main__":
    sys.exit(main())
