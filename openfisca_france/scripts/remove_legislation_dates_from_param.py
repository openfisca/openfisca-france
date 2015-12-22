#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Merge YAML files of IPP tax and benefit tables with OpenFisca parameters to generate new parameters."""


import argparse
import datetime
import logging
import os
import sys
import xml.etree.ElementTree as etree


app_name = os.path.splitext(os.path.basename(__file__))[0]
log = logging.getLogger(app_name)
package_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
param_dir = os.path.join(package_dir, 'param')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--param', default = os.path.join(param_dir, 'param.xml'),
        help = 'path of XML file containing the OpenFisca parameters')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    element_tree = etree.parse(args.param)
    root_element = element_tree.getroot()
    del root_element.attrib['deb']
    legislation_stop_date = root_element.attrib.pop('fin')
    sort_elements(root_element)
    for parent_element in root_element.iter():
        value_elements = parent_element.findall('./VALUE')
        for value_element in value_elements:
            if value_element.get('deb') is None or value_element.get('fin') is None:
                # Add "fuzzy" attributes to original value elements without "fin" attribute.
                value_element.attrib['fuzzy'] = "true"
            elif value_element.get('fin') >= legislation_stop_date and value_element is value_elements[0]:
                # When stop date of (last) value is greater or equal than legislation stop date, append a new element,
                # with same value, without stop date and with "fuzzy" attribute.
                next_value_element = etree.Element(value_element.tag, attrib = {
                    name: value
                    for name, value in value_element.items()
                    if name not in ('deb', 'fin')
                    })
                next_value_element.set('deb', (
                    datetime.date(*(
                        int(fragment)
                        for fragment in value_element.get('fin').split('-')
                        )) +
                    datetime.timedelta(days = 1)
                    ).isoformat())
                next_value_element.set('fuzzy', 'true')
                parent_element.insert(0, next_value_element)
    reindent(root_element)
    element_tree.write(args.param, encoding = 'utf-8')

    return 0


def reindent(elem, depth = 0):
    # cf http://effbot.org/zone/element-lib.htm
    indent = "\n" + depth * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for elem in elem:
            reindent(elem, depth + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
    else:
        if depth and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent


def sort_elements(element):
    if element.tag in ('BAREME', 'NODE', 'TRANCHE'):
        if element.tag == 'NODE':
            children = list(element)
            for child in children:
                element.remove(child)
            children.sort(key = lambda child: child.get('code'))
            element.extend(children)
        for child in element:
            sort_elements(child)
    else:
        children = list(element)
        for child in children:
            element.remove(child)
        children.sort(key = lambda child: child.get('deb') or '', reverse = True)
        element.extend(children)


if __name__ == "__main__":
    sys.exit(main())
