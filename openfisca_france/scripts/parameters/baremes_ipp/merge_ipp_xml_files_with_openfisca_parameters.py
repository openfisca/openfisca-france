#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
Merge IPP XML files with OpenFisca XML parameters.

Keep elements and attributes order from OpenFisca side, replace <CODE> and <BAREME> leaves by IPP ones.

Let the user commit or not the diff using git. The script `../format_parameters.py` can be used to ease the merge.
"""


import argparse
import os
import sys

from lxml import etree
from openfisca_core import legislationsxml

from openfisca_france.france_taxbenefitsystem import FranceTaxBenefitSystem, COUNTRY_DIR


parameters_dir_path = os.path.join(COUNTRY_DIR, 'parameters')


def replace_children(element, children):
    for child in element:
        child.getparent().remove(child)
    element.extend(children)


def merge_attributes(openfisca_element, ipp_element):
    for key, value in ipp_element.attrib.iteritems():
        if key in openfisca_element.attrib:
            if openfisca_element.attrib[key] != ipp_element.attrib[key]:
                openfisca_element.attrib[key] = ipp_element.attrib[key]
        else:
            openfisca_element.attrib[key] = ipp_element.attrib[key]


def merge_elements(openfisca_element, ipp_element, path = []):
    """
    Merge `ipp_element` in `openfisca_element`, modifying `openfisca_element`.

    Returns `None`.
    """
    def error_at_path(error):
        path_with_code = path + [openfisca_element.attrib['code']]
        return u'At {}: {}'.format('.'.join(path_with_code), error)

    assert ipp_element.attrib['code'] == openfisca_element.attrib['code'], (openfisca_element, ipp_element)
    assert ipp_element.tag == openfisca_element.tag, \
        error_at_path(u'OpenFisca element {!r} differs from IPP element {!r}'.format(
            openfisca_element.tag, ipp_element.tag).encode('utf-8'))

    merge_attributes(openfisca_element, ipp_element)

    # Merge children

    if openfisca_element.tag == 'NODE':
        ipp_children_by_code = {
            child.attrib['code']: child
            for child in ipp_element
        }
        for openfisca_child in openfisca_element:
            code = openfisca_child.attrib['code']
            if code in ipp_children_by_code.keys():
                ipp_child = ipp_children_by_code[code]
                del ipp_children_by_code[code]
                merge_elements(openfisca_child, ipp_child, path + [openfisca_element.attrib['code']])
        for code, ipp_child in ipp_children_by_code.iteritems():
            openfisca_element.append(ipp_child)

    elif openfisca_element.tag == 'CODE':
        replace_children(openfisca_element, ipp_element.getchildren())

    elif openfisca_element.tag == 'BAREME':
        assert ipp_element.tag == 'BAREME', (openfisca_element, ipp_element)
        for index, openfisca_tranche in enumerate(openfisca_element):
            ipp_tranche = ipp_element[index]
            merge_attributes(openfisca_tranche, ipp_tranche)

            ipp_tranche_children_by_tag = {
                child.tag: child
                for child in ipp_tranche
            }

            for openfisca_tranche_child in openfisca_tranche:
                tag = openfisca_tranche_child.tag
                if tag in ipp_tranche_children_by_tag.keys():
                    ipp_tranche_child = ipp_tranche_children_by_tag[tag]
                    del ipp_tranche_children_by_tag[tag]
                    replace_children(openfisca_tranche_child, ipp_tranche_child)
            for tag, ipp_tranche_child in ipp_tranche_children_by_tag.iteritems():
                openfisca_tranche.append(ipp_tranche_child)
    else:
        raise NotImplementedError(openfisca_element)


def get_xml_tree_by_file_name(xmlschema, file_paths):
    xml_tree_by_file_name = dict()
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            tree = etree.parse(f)
        if not xmlschema.validate(tree):
            raise ValueError(xmlschema.error_log.filter_from_errors())
        file_name = os.path.basename(file_path)
        xml_tree_by_file_name[file_name] = tree
    return xml_tree_by_file_name


def merge_ipp_xml_files_with_openfisca_parameters(ipp_xml_dir):
    if not os.path.isdir(ipp_xml_dir):
        parser.error(u'Path {!r} does not exist.'.format(ipp_xml_dir))

    xmlschema = legislationsxml.load_xml_schema()
    france_tax_benefit_system = FranceTaxBenefitSystem()

    openfisca_file_paths = [
        file_path
        for file_path, _ in france_tax_benefit_system.legislation_xml_info_list
        ]
    openfisca_xml_tree_by_file_name = get_xml_tree_by_file_name(xmlschema, openfisca_file_paths)

    ipp_file_paths = [
        os.path.join(ipp_xml_dir, file_name)
        for file_name in os.listdir(ipp_xml_dir)
        if file_name.endswith('.xml')
        ]
    if not ipp_file_paths:
        print("Warning : no IPP XML found.")
    ipp_xml_tree_by_file_name = get_xml_tree_by_file_name(xmlschema, ipp_file_paths)

    for openfisca_file_name, openfisca_xml_tree in openfisca_xml_tree_by_file_name.iteritems():
        openfisca_xml_root_element = openfisca_xml_tree.getroot()
        ipp_xml_tree = ipp_xml_tree_by_file_name.get(openfisca_file_name)
        if ipp_xml_tree is not None:
            print('Processing {}...'.format(openfisca_file_name))
            ipp_xml_root_element = ipp_xml_tree.getroot()
            merge_elements(openfisca_xml_root_element, ipp_xml_root_element)  # Mutates `openfisca_xml_root_element`
        output_tree = etree.ElementTree(openfisca_xml_root_element)
        output_file_path = os.path.join(parameters_dir_path, openfisca_file_name)
        output_tree.write(output_file_path, encoding='utf-8', pretty_print=True)

    return 0


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('ipp_xml_dir', help = "Directory of XML files converted from IPP")
    args = parser.parse_args()

    merge_ipp_xml_files_with_openfisca_parameters(args.ipp_xml_dir)

if __name__ == "__main__":
    sys.exit(main())
