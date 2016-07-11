# -*- coding: utf-8 -*-

import datetime
import json

from openfisca_core import conv, legislations, legislationsxml

from openfisca_france import FranceTaxBenefitSystem


# Exceptionally for this test do not import TaxBenefitSystem from tests.base.
tax_benefit_system = FranceTaxBenefitSystem()


def check_legislation_xml_file(year):
    legislation_tree = conv.check(legislationsxml.make_xml_legislation_info_list_to_xml_element(False))(
        tax_benefit_system.legislation_xml_info_list, state = conv.default_state)
    legislation_xml_json = conv.check(legislationsxml.xml_legislation_to_json)(
        legislation_tree,
        state = conv.default_state,
        )

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
