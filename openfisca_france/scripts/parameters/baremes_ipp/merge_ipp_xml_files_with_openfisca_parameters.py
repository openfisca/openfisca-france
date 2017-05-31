#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""
Merge IPP XML files with OpenFisca XML parameters.

Keep elements and attributes order from OpenFisca side, replace <CODE> and <BAREME> leaves by IPP ones.

Let the user commit or not the diff using git.
"""


import argparse
import os
import sys

from lxml import etree
from openfisca_core import legislationsxml

from openfisca_france.france_taxbenefitsystem import FranceTaxBenefitSystem, COUNTRY_DIR


parameters_dir_path = os.path.join(COUNTRY_DIR, 'parameters')


def xml_element(tag, attrib, children):
    element = etree.Element(tag, attrib)
    element.extend(children)
    return element


def by_deb(child_element):
    return child_element.attrib['deb']


def by_code(child_element):
    return child_element.attrib['code']


def by_tag(child_element):
    return child_element.tag


def without_comments(element):
    """Return children of `element` ignoring XML comments."""
    return filter(lambda child: child.tag is not etree.Comment, element)


def replace_children(element, children):
    for child in element:
        child.getparent().remove(child)
    element.extend(children)


def merge_elements(openfisca_element, element, path = []):
    """
    Merge `element` in `openfisca_element`, modifying `openfisca_element`.

    The source of truth is `openfisca_element`.

    Returns `None`.
    """
    def error_at_path(error):
        path_with_code = path + [openfisca_element.attrib['code']]
        return u'At {}: {}'.format('.'.join(path_with_code), error)

    assert element.attrib['code'] == openfisca_element.attrib['code'], (element, openfisca_element)
    assert element.tag == openfisca_element.tag, \
        error_at_path(u'OpenFisca element {!r} differs from IPP element {!r}'.format(
            openfisca_element.tag, element.tag).encode('utf-8'))

    if openfisca_element.tag == 'NODE':
        for openfisca_child_element in without_comments(openfisca_element):
            for child_element in element:
                if child_element.attrib['code'] == openfisca_child_element.attrib['code']:
                    merge_elements(openfisca_child_element, child_element, path + [openfisca_element.attrib['code']])
                    break

    elif openfisca_element.tag in {'CODE', 'BAREME'}:
        # Replace OpenFisca attributes from IPP attributes, keeping OpenFisca attributes order.
        for name, _ in openfisca_element.attrib.iteritems():
            if element.get(name) is not None:
                openfisca_element.attrib[name] = element.attrib[name]
        # Add attributes only in IPP element.
        for name, value in element.attrib.iteritems():
            if openfisca_element.get(name) is None:
                openfisca_element.attrib[name] = element.attrib[name]
        if openfisca_element.tag == 'CODE':
            replace_children(openfisca_element, element.getchildren())
        else:
            assert openfisca_element.tag == 'BAREME', openfisca_element
            for index, openfisca_tranche_element in enumerate(openfisca_element):
                ipp_tranche_element = openfisca_element[index]
                openfisca_seuil_element = openfisca_tranche_element.find('SEUIL')
                ipp_seuil_element = ipp_tranche_element.find('SEUIL')
                replace_children(openfisca_seuil_element, ipp_seuil_element.getchildren())
                openfisca_taux_element = openfisca_tranche_element.find('TAUX')
                ipp_taux_element = ipp_tranche_element.find('TAUX')
                replace_children(openfisca_taux_element, ipp_taux_element.getchildren())

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


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('ipp_xml_dir', help = "Directory of XML files converted from IPP")
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()

    if not os.path.isdir(args.ipp_xml_dir):
        parser.error(u'Path {!r} does not exist.'.format(args.ipp_xml_dir))

    xmlschema = legislationsxml.load_xml_schema()
    france_tax_benefit_system = FranceTaxBenefitSystem()

    openfisca_file_paths = [
        file_path
        for file_path, _ in france_tax_benefit_system.legislation_xml_info_list
        ]
    openfisca_xml_tree_by_file_name = get_xml_tree_by_file_name(xmlschema, openfisca_file_paths)

    ipp_file_paths = [
        os.path.join(args.ipp_xml_dir, file_name)
        for file_name in os.listdir(args.ipp_xml_dir)
        if file_name.endswith('.xml')
        ]
    ipp_xml_tree_by_file_name = get_xml_tree_by_file_name(xmlschema, ipp_file_paths)

    for openfisca_file_name, openfisca_xml_tree in openfisca_xml_tree_by_file_name.iteritems():
        openfisca_xml_root_element = openfisca_xml_tree.getroot()
        ipp_xml_tree = ipp_xml_tree_by_file_name.get(openfisca_file_name)
        if ipp_xml_tree is not None:
            ipp_xml_root_element = ipp_xml_tree.getroot()
            merge_elements(openfisca_xml_root_element, ipp_xml_root_element)  # Mutates `openfisca_xml_root_element`
        output_tree = etree.ElementTree(openfisca_xml_root_element)
        output_file_path = os.path.join(parameters_dir_path, openfisca_file_name)
        output_tree.write(output_file_path, encoding='utf-8', pretty_print=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
