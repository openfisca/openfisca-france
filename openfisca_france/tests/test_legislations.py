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


import datetime
import json
import xml.etree.ElementTree

from openfisca_core import conv, legislations, legislationsxml

from openfisca_france import init_country


TaxBenefitSystem = init_country()


def check_legislation_xml_file(year):
    legislation_tree = xml.etree.ElementTree.parse(TaxBenefitSystem.legislation_xml_file_path)
    legislation_xml_json = conv.check(legislationsxml.xml_legislation_to_json)(legislation_tree.getroot(),
        state = conv.default_state)

    legislation_xml_json, errors = legislationsxml.validate_legislation_xml_json(legislation_xml_json,
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

    legislation_json, errors = legislations.validate_legislation_json(legislation_json, state = conv.default_state)
    if errors is not None:
        errors = conv.embed_error(legislation_json, 'errors', errors)
        if errors is None:
            raise ValueError(unicode(json.dumps(legislation_json, ensure_ascii = False, indent = 2)).encode('utf-8'))
        raise ValueError(u'{0} for: {1}'.format(
            unicode(json.dumps(errors, ensure_ascii = False, indent = 2, sort_keys = True)),
            unicode(json.dumps(legislation_json, ensure_ascii = False, indent = 2)),
            ).encode('utf-8'))

    # Create tax_benefit system only now, to be able to debug XML validation errors in above code.
    tax_benefit_system = TaxBenefitSystem()
    if tax_benefit_system.preprocess_legislation is not None:
        tax_benefit_system.preprocess_legislation(legislation_json)

    legislation_json = legislations.generate_dated_legislation_json(legislation_json, year)
    legislation_json, errors = legislations.validate_dated_legislation_json(legislation_json,
        state = conv.default_state)
    if errors is not None:
        errors = conv.embed_error(legislation_json, 'errors', errors)
        if errors is None:
            raise ValueError(unicode(json.dumps(legislation_json, ensure_ascii = False, indent = 2)).encode(
                'utf-8'))
        raise ValueError(u'{0} for: {1}'.format(
            unicode(json.dumps(errors, ensure_ascii = False, indent = 2, sort_keys = True)),
            unicode(json.dumps(legislation_json, ensure_ascii = False, indent = 2)),
            ).encode('utf-8'))

    compact_legislation = legislations.compact_dated_node_json(legislation_json)
    assert compact_legislation is not None


def test_legislation_xml_file():
    for year in range(2006, datetime.date.today().year + 1):
        yield check_legislation_xml_file, year


if __name__ == '__main__':
    test_legislation_xml_file()
    import nose
    nose.core.runmodule(argv = [__file__, '-v', 'test_legislations:test_legislation_xml_file'])
