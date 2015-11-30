# -*- coding: utf-8 -*-

import datetime
import json
import xml.etree.ElementTree

from openfisca_core import conv, legislations, legislationsxml

from openfisca_france.tests.base import TaxBenefitSystem, tax_benefit_system


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
    if tax_benefit_system.preprocess_legislation is not None:
        legislation_json = tax_benefit_system.preprocess_legislation(legislation_json)

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
