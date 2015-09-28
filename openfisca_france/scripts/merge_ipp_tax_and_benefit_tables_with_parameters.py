#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Merge YAML files of IPP tax and benefit tables with OpenFisca parameters to generate new parameters."""


import argparse
import collections
import datetime
import logging
import os
import sys
import xml.etree.ElementTree as etree

from biryani import strings
import yaml


date_names = (
    # u"Age de départ (AAD=Age d'annulation de la décôte)",
    u"Date",
    u"Date d'effet",
    u"Date de perception du salaire",
    u"Date ISF",
    )
log = logging.getLogger(__name__)
note_names = (
    u"Notes",
    u"Notes bis",
    )
parameters_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'param'))
reference_names = (
    u"Parution au JO",
    u"Références BOI",
    u"Références législatives",
    u"Références législatives - définition des ressources et plafonds",
    u"Références législatives - revalorisation des plafonds",
    u"Références législatives des règles de calcul et du paramètre Po",
    u"Références législatives de tous les autres paramètres",
    )


# YAML configuration


def dict_constructor(loader, node):
    return collections.OrderedDict(loader.construct_pairs(node))


yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dict_constructor)


# Functions


def iter_ipp_values(node):
    if isinstance(node, dict):
        for name, child in node.iteritems():
            for path, value in iter_ipp_values(child):
                yield [name] + path, value
    else:
        yield [], node


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ipp-translations',
        default = os.path.join(parameters_dir, 'ipp-tax-and-benefit-tables-to-parameters.yaml'),
        help = 'path of YAML file containing the association between IPP fields and OpenFisca parameters')
    parser.add_argument('-o', '--origin', default = os.path.join(parameters_dir, 'param.xml'),
        help = 'path of XML file containing the original OpenFisca parameters')
    parser.add_argument('-p', '--param-translations',
        default = os.path.join(parameters_dir, 'param-to-parameters.yaml'),
        help = 'path of YAML file containing the association between param elements and OpenFisca parameters')
    parser.add_argument('-s', '--source-dir', default = 'yaml-clean',
        help = 'path of source directory containing clean IPP YAML files')
    parser.add_argument('-t', '--target', default = os.path.join(parameters_dir, 'parameters.xml'),
        help = 'path of generated YAML file containing the association between IPP fields with OpenFisca parameters')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    file_system_encoding = sys.getfilesystemencoding()

    original_element_tree = etree.parse(args.origin)
    original_root_element = original_element_tree.getroot()

    # Apply translations to original parameters.
    with open(args.param_translations) as param_translations_file:
        param_translations = yaml.load(param_translations_file)
    for old_path, new_path in param_translations.iteritems():
        parent_element = None
        element = original_root_element
        for name in old_path.split('.'):
            for child in element:
                if child.get('code') == name:
                    parent_element = element
                    element = child
                    break
            else:
                assert False, 'Path "{}" not found in "{}"'.format(old_path, args.origin)
        parent_element.remove(element)
        if new_path is not None:
            parent_element = original_root_element
            split_new_path = new_path.split('.')
            for name in split_new_path[:-1]:
                for child in parent_element:
                    if child.get('code') == name:
                        parent_element = child
                        break
                else:
                    parent_element = etree.SubElement(parent_element, 'NODE', attrib = dict(
                        code = name,
                        ))
            name = split_new_path[-1]
            assert all(
                child.get('code') != name
                for child in parent_element
                ), 'Path "{}" already exists in "{}"'.format(new_path, args.origin)
            element.set('code', name)
            parent_element.append(element)

    with open(args.ipp_translations) as ipp_translations_file:
        ipp_translations = yaml.load(ipp_translations_file)

    tree = collections.OrderedDict()
    for source_dir_encoded, directories_name_encoded, filenames_encoded in os.walk(args.source_dir):
        directories_name_encoded.sort()
        for filename_encoded in sorted(filenames_encoded):
            if not filename_encoded.endswith('.yaml'):
                continue
            filename = filename_encoded.decode(file_system_encoding)
            sheet_name = os.path.splitext(filename)[0]
            source_file_path_encoded = os.path.join(source_dir_encoded, filename_encoded)
            relative_file_path_encoded = source_file_path_encoded[len(args.source_dir):].lstrip(os.sep)
            relative_file_path = relative_file_path_encoded.decode(file_system_encoding)
            if sheet_name.isupper():
                continue
            assert sheet_name.islower(), sheet_name
            log.info(u'Loading file {}'.format(relative_file_path))
            with open(source_file_path_encoded) as source_file:
                data = yaml.load(source_file)
            rows = data.get(u"Valeurs")
            if rows is None:
                log.info(u'  Skipping file {} without "Valeurs"'.format(relative_file_path))
                continue
            row_by_start = {}
            for row in rows:
                start = row.get(u"Date d'effet")
                if start is None:
                    for date_name in date_names:
                        start = row.get(date_name)
                        if start is not None:
                            break
                    else:
                        # No date found. Skip row.
                        continue
                elif not isinstance(start, datetime.date):
                    start = start[u"Année Revenus"]
                row_by_start[start] = row
            sorted_row_by_start = sorted(row_by_start.iteritems())

            unsorted_relative_ipp_paths = set()
            relative_ipp_paths_by_start = {}
            for start, row in sorted_row_by_start:
                relative_ipp_paths_by_start[start] = start_relative_ipp_paths = []
                for name, child in row.iteritems():
                    if name in date_names:
                        continue
                    if name in note_names:
                        continue
                    if name in reference_names:
                        continue
                    start_relative_ipp_paths.extend(
                        (name,) + tuple(path)
                        for path, value in iter_ipp_values(child)
                        )
                unsorted_relative_ipp_paths.update(start_relative_ipp_paths)

            def compare_relative_ipp_paths(x, y):
                if x == y:
                    return 0
                for relative_ipp_paths in relative_ipp_paths_by_start.itervalues():
                    try:
                        return cmp(relative_ipp_paths.index(x), relative_ipp_paths.index(y))
                    except ValueError:
                        # Either x or y paths are missing in relative_ipp_paths => Their order can't be compared.
                        continue
                return -1

            sorted_relative_ipp_paths = sorted(unsorted_relative_ipp_paths, cmp = compare_relative_ipp_paths)

            for start, row in sorted_row_by_start:
                for relative_ipp_path in sorted_relative_ipp_paths:
                    value = row
                    for fragment in relative_ipp_path:
                        value = value.get(fragment)
                        if value is None:
                            break

                    if value in (u'-', u'na', u'nc'):
                        # Value is unknown. Previous value must  be propagated.
                        continue
                    ipp_path = relative_file_path.split(os.sep)[:-1] + [sheet_name] + list(relative_ipp_path)

                    remaining_path = ipp_path[:]
                    skip_ipp_path = False
                    sub_tree = tree
                    translations = ipp_translations
                    translated_path = []
                    while remaining_path:
                        fragment = remaining_path.pop(0)
                        type = None
                        if translations is not None:
                            translations = translations.get(fragment, fragment)
                            if translations is None:
                                skip_ipp_path = True
                                break
                            elif isinstance(translations, dict):
                                translation = translations.get('RENAME')
                                if translation is not None:
                                    fragment = translation
                                type = translations.get('TYPE')
                                assert type in (None, u'BAREME')
                            else:
                                fragment = translations
                                translations = None
                        sub_path = [fragment] if isinstance(fragment, basestring) else fragment[:]
                        while sub_path:
                            fragment = sub_path.pop(0)
                            translated_path.append(fragment)
                            if fragment == u'ASSIETTE':
                                assert sub_tree.get('TYPE') == u'BAREME', str((translated_path, sub_path, sub_tree))
                                assert not sub_path
                                slice_name = remaining_path.pop(0)
                                assert not remaining_path
                                sub_tree = sub_tree.setdefault(u'ASSIETTE', collections.OrderedDict()).setdefault(
                                    slice_name, [])
                            elif fragment == u'BAREME':
                                existing_type = sub_tree.get('TYPE')
                                if existing_type is None:
                                    sub_tree['TYPE'] = fragment
                                else:
                                    assert existing_type == fragment
                            elif fragment == u'MONTANT':
                                assert sub_tree.get('TYPE') == u'BAREME', str((translated_path, sub_path, sub_tree))
                                assert not sub_path
                                slice_name = remaining_path.pop(0)
                                assert not remaining_path
                                sub_tree = sub_tree.setdefault(u'MONTANT', collections.OrderedDict()).setdefault(
                                    slice_name, [])
                            elif fragment == u'SEUIL':
                                assert sub_tree.get('TYPE') == u'BAREME', str((translated_path, sub_path, sub_tree))
                                assert not sub_path
                                slice_name = remaining_path.pop(0)
                                assert not remaining_path
                                sub_tree = sub_tree.setdefault(u'SEUIL', collections.OrderedDict()).setdefault(
                                    slice_name, [])
                            elif fragment == u'TAUX':
                                assert sub_tree.get('TYPE') == u'BAREME', str((translated_path, sub_path, sub_tree))
                                assert not sub_path
                                slice_name = remaining_path.pop(0)
                                assert not remaining_path
                                sub_tree = sub_tree.setdefault(u'TAUX', collections.OrderedDict()).setdefault(
                                    slice_name, [])
                            elif sub_path or remaining_path:
                                sub_tree = sub_tree.setdefault(fragment, collections.OrderedDict())
                                if type is not None:
                                    existing_type = sub_tree.get('TYPE')
                                    if existing_type is None:
                                        sub_tree['TYPE'] = type
                                    else:
                                        assert existing_type == type
                            else:
                                sub_tree = sub_tree.setdefault(fragment, [])
                    if skip_ipp_path:
                        continue
                    if sub_tree:
                        last_leaf = sub_tree[-1]
                        if last_leaf['value'] == value:
                            continue
                        last_leaf['stop'] = start - datetime.timedelta(days = 1)
                    sub_tree.append(dict(
                        start = start,
                        value = value,
                        ))

    root_element = transform_node_to_element(u'root', tree)
    root_element.set('deb', original_root_element.get('deb'))
    root_element.set('fin', original_root_element.get('fin'))
    merge_elements(root_element, original_root_element)
    sort_elements(root_element)
    reindent(root_element)

    element_tree = etree.ElementTree(root_element)
    element_tree.write(args.target, encoding = 'utf-8')

    return 0


def merge_elements(element, original_element, path = None):
    if path is None:
        path = []
    else:
        path = path[:]
    path.append(element.get('code'))
    assert element.tag == original_element.tag, 'At {}, IPP element "{}"" differs from original element "{}"'.format(
        '.'.join(path), element.tag, original_element.tag)
    if element.tag == 'NODE':
        for original_child in original_element:
            for child in element:
                if child.get('code') == original_child.get('code'):
                    merge_elements(child, original_child)
                    break
            else:
                # A child with the same code as the original child doesn't exist yet.
                element.append(original_child)


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


def prepare_xml_values(name, leafs):
    leafs = list(reversed([
        leaf
        for leaf in leafs
        if leaf['value'] is not None
        ]))
    format = None
    type = None
    for leaf in leafs:
        value = leaf['value']
        if isinstance(value, basestring):
            split_value = value.split()
            if len(split_value) == 2 and split_value[1] in (
                    u'%',
                    u'AF',  # anciens francs
                    u'CFA',  # francs CFA
                    # u'COTISATIONS',
                    u'EUR',
                    u'FRF',
                    ):
                value = float(split_value[0])
                unit = split_value[1]
                if unit == u'%':
                    if format is None:
                        format = u'percent'
                    elif format != u'percent':
                        log.warning(u'Non constant percent format {} in {}: {}'.format(format, name, leafs))
                        return None, format, type
                    value = value / 100
                else:
                    if format is None:
                        format = u'float'
                    elif format != u'float':
                        log.warning(u'Non constant float format {} in {}: {}'.format(format, name, leafs))
                        return None, format, type
                    if type is None:
                        type = u'monetary'
                    elif type != u'monetary':
                        log.warning(u'Non constant monetary type {} in {}: {}'.format(type, name, leafs))
                        return None, format, type
                    else:
                        assert type == u'monetary', type
                # elif unit == u'AF':
                #     # Convert "anciens francs" to €.
                #     value = round(value / (100 * 6.55957), 2)
                # elif unit == u'FRF':
                #     # Convert "nouveaux francs" to €.
                #     if month < year_1960:
                #         value /= 100
                #     value = round(value / 6.55957, 2)
        if isinstance(value, float) and value == int(value):
            value = int(value)
        leaf['value'] = value
    return leafs, format, type


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


def transform_node_to_element(name, node):
    if isinstance(node, dict):
        if node.get('TYPE') == u'BAREME':
            scale_element = etree.Element('BAREME', attrib = dict(
                code = strings.slugify(name, separator = u'_'),
                ))
            for slice_name in node.get('SEUIL', {}).keys():
                slice_element = etree.Element('TRANCHE', attrib = dict(
                    code = strings.slugify(slice_name, separator = u'_'),
                    ))

                threshold_element = etree.Element('SEUIL')
                values, format, type = prepare_xml_values(name, node.get('SEUIL', {}).get(slice_name, []))
                for value in values:
                    value_element = transform_value_to_element(value)
                    if value_element is not None:
                        threshold_element.append(value_element)
                if len(threshold_element) > 0:
                    slice_element.append(threshold_element)

                amount_element = etree.Element('MONTANT')
                values, format, type = prepare_xml_values(name, node.get('MONTANT', {}).get(slice_name, []))
                for value in values:
                    value_element = transform_value_to_element(value)
                    if value_element is not None:
                        amount_element.append(value_element)
                if len(amount_element) > 0:
                    slice_element.append(amount_element)

                rate_element = etree.Element('TAUX')
                values, format, type = prepare_xml_values(name, node.get('TAUX', {}).get(slice_name, []))
                for value in values:
                    value_element = transform_value_to_element(value)
                    if value_element is not None:
                        rate_element.append(value_element)
                if len(rate_element) > 0:
                    slice_element.append(rate_element)

                base_element = etree.Element('ASSIETTE')
                values, format, type = prepare_xml_values(name, node.get('ASSIETTE', {}).get(slice_name, []))
                for value in values:
                    value_element = transform_value_to_element(value)
                    if value_element is not None:
                        base_element.append(value_element)
                if len(base_element) > 0:
                    slice_element.append(base_element)

                if len(slice_element) > 0:
                    scale_element.append(slice_element)
            return scale_element if len(scale_element) > 0 else None
        else:
            node_element = etree.Element('NODE', attrib = dict(
                code = strings.slugify(name, separator = u'_'),
                ))
            for key, value in node.iteritems():
                child_element = transform_node_to_element(key, value)
                if child_element is not None:
                    node_element.append(child_element)
            return node_element if len(node_element) > 0 else None
    else:
        assert isinstance(node, list), node
        values, format, type = prepare_xml_values(name, node)
        if not values:
            return None
        code_element = etree.Element('CODE', attrib = dict(
            code = strings.slugify(name, separator = u'_'),
            ))
        if format is not None:
            code_element.set('format', format)
        if type is not None:
            code_element.set('type', type)
        for value in values:
            value_element = transform_value_to_element(value)
            if value_element is not None:
                code_element.append(value_element)
        return code_element if len(code_element) > 0 else None


def transform_value_to_element(leaf):
    value = leaf.get('value')
    if value is None:
        return None
    value_element = etree.Element('VALUE', attrib = dict(
        valeur = unicode(value),
        ))
    start = leaf.get('start')
    if start is not None:
        value_element.set('deb', start.isoformat())
    stop = leaf.get('stop')
    if stop is not None:
        value_element.set('fin', stop.isoformat())
    return value_element


if __name__ == "__main__":
    sys.exit(main())
