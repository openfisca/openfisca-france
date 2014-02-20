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


import datetime
import json
import xml.etree.ElementTree

import openfisca_france
openfisca_france.init_country()

from openfisca_core import conv, legislations, legislationsxml, model


def test_legislation_xml_file():
    legislation_tree = xml.etree.ElementTree.parse(model.PARAM_FILE)
    legislation_xml_json = conv.check(legislationsxml.xml_legislation_to_json)(legislation_tree.getroot(),
        state = conv.default_state)

    legislation_xml_json, errors = legislationsxml.validate_node_xml_json(legislation_xml_json,
        state = conv.default_state)
    if errors is not None:
        errors = conv.embed_error(legislation_xml_json, 'errors', errors)
        if errors is None:
            raise ValueError(unicode(json.dumps(legislation_xml_json, ensure_ascii = False,
                indent = 2)).encode('utf-8'))
        raise ValueError(u'{0} for: {1}'.format(
            unicode(json.dumps(errors, ensure_ascii = False, indent = 2, sort_keys = True)),
            unicode(json.dumps(legislation_xml_json, ensure_ascii = False, indent = 2)),
            ).encode('utf-8'))

    _, legislation_json = legislationsxml.transform_node_xml_json_to_json(legislation_xml_json)

    legislation_json, errors = legislations.validate_node_json(legislation_json, state = conv.default_state)
    if errors is not None:
        errors = conv.embed_error(legislation_json, 'errors', errors)
        if errors is None:
            raise ValueError(unicode(json.dumps(legislation_json, ensure_ascii = False, indent = 2)).encode('utf-8'))
        raise ValueError(u'{0} for: {1}'.format(
            unicode(json.dumps(errors, ensure_ascii = False, indent = 2, sort_keys = True)),
            unicode(json.dumps(legislation_json, ensure_ascii = False, indent = 2)),
            ).encode('utf-8'))

    dated_legislation_json = legislations.generate_dated_legislation_json(legislation_json, datetime.date(2006, 1, 1))
    dated_legislation_json, errors = legislations.validate_dated_legislation_json(dated_legislation_json,
        state = conv.default_state)
    if errors is not None:
        errors = conv.embed_error(dated_legislation_json, 'errors', errors)
        if errors is None:
            raise ValueError(unicode(json.dumps(dated_legislation_json, ensure_ascii = False, indent = 2)).encode(
                'utf-8'))
        raise ValueError(u'{0} for: {1}'.format(
            unicode(json.dumps(errors, ensure_ascii = False, indent = 2, sort_keys = True)),
            unicode(json.dumps(dated_legislation_json, ensure_ascii = False, indent = 2)),
            ).encode('utf-8'))

    compact_legislation = legislations.compact_dated_node_json(dated_legislation_json)


if __name__ == '__main__':
    import nose
    nose.core.runmodule(argv = [__file__, '-v', 'legislation_tests:test_legislation_xml_file'])
