# -*- coding: utf-8 -*-

import json
import os
import xml.etree.ElementTree

from openfisca_core import conv, decompositions, decompositionsxml

from .cache import tax_benefit_system

decompositions_directory = os.path.dirname(tax_benefit_system.decomposition_file_path)


def check_decomposition_xml_file(file_path):
    decomposition_tree = xml.etree.ElementTree.parse(os.path.join(file_path))
    decomposition_xml_json = conv.check(decompositionsxml.xml_decomposition_to_json)(decomposition_tree.getroot(),
        state = conv.default_state)

    decomposition_xml_json, errors = decompositionsxml.make_validate_node_xml_json(tax_benefit_system)(
        decomposition_xml_json, state = conv.default_state)
    if errors is not None:
        errors = conv.embed_error(decomposition_xml_json, 'errors', errors)
        if errors is None:
            raise ValueError(unicode(json.dumps(decomposition_xml_json, ensure_ascii = False,
                indent = 2)).encode('utf-8'))
        raise ValueError(u'{0} for: {1}'.format(
            unicode(json.dumps(errors, ensure_ascii = False, indent = 2, sort_keys = True)),
            unicode(json.dumps(decomposition_xml_json, ensure_ascii = False, indent = 2)),
            ).encode('utf-8'))

    decomposition_json = decompositionsxml.transform_node_xml_json_to_json(decomposition_xml_json)

    decomposition_json, errors = decompositions.make_validate_node_json(tax_benefit_system)(
        decomposition_json, state = conv.default_state)
    if errors is not None:
        errors = conv.embed_error(decomposition_json, 'errors', errors)
        if errors is None:
            raise ValueError(unicode(json.dumps(decomposition_json, ensure_ascii = False, indent = 2)).encode('utf-8'))
        raise ValueError(u'{0} for: {1}'.format(
            unicode(json.dumps(errors, ensure_ascii = False, indent = 2, sort_keys = True)),
            unicode(json.dumps(decomposition_json, ensure_ascii = False, indent = 2)),
            ).encode('utf-8'))


def test_decomposition_xml_files():
    files_path = [
        tax_benefit_system.decomposition_file_path,
        os.path.join(
            decompositions_directory,
            'fiche_de_paie_decomposition.xml',
            )
        ]
    for file_path in files_path:
        yield check_decomposition_xml_file, file_path


def test_decomposition_calculate():
    xml_file_path = tax_benefit_system.decomposition_file_path
    decomposition_json = decompositions.get_decomposition_json(tax_benefit_system, xml_file_path)
    year = 2013
    simulation = tax_benefit_system.new_scenario().init_single_entity(
        period = year,
        parent1 = {},
        ).new_simulation()
    decomposition = decompositions.calculate([simulation], decomposition_json)
    assert isinstance(decomposition, dict)
