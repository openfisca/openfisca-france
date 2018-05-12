# -*- coding: utf-8 -*-


"""Transform clean YAML files from IPP to XML files compatible with OpenFisca."""


import collections
import datetime
import itertools
import logging
import os
import sys

from biryani import strings
from lxml import etree
import yaml

from transform_ipp_tree import transform_ipp_tree


app_name = os.path.splitext(os.path.basename(__file__))[0]
date_names = (
    # u"Age de départ (AAD=Age d'annulation de la décôte)",
    u"Date",
    u"Date d'effet",
    u"Date de perception du salaire",
    u"Date ISF",
    )
file_system_encoding = sys.getfilesystemencoding()
log = logging.getLogger(app_name)
note_names = (
    u"Notes",
    u"Notes bis",
    )
reference_names = (
    u"Parution au JO",
    u"Références BOI",
    u"Références législatives",
    u"Références législatives - définition des ressources et plafonds",
    u"Références législatives - revalorisation des plafonds",
    u"Références législatives des règles de calcul et du paramètre Po",
    u"Références législatives de tous les autres paramètres",
    )


def dict_constructor(loader, node):
    return collections.OrderedDict(loader.construct_pairs(node))


yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dict_constructor)


def build_tree_from_yaml_clean(yaml_dir):
    tree = collections.OrderedDict()
    for yaml_dir_encoded, _, filenames_encoded in os.walk(yaml_dir):
        for filename_encoded in sorted(filenames_encoded):
            if not filename_encoded.endswith('.yaml'):
                continue
            filename = filename_encoded.decode(file_system_encoding)
            sheet_name = os.path.splitext(filename)[0]
            yaml_file_path_encoded = os.path.join(yaml_dir_encoded, filename_encoded)
            relative_file_path_encoded = yaml_file_path_encoded[len(yaml_dir):].lstrip(os.sep)
            relative_file_path = relative_file_path_encoded.decode(file_system_encoding)
            if sheet_name.isupper():
                continue
            assert sheet_name.islower(), sheet_name
            log.info(u'Loading file {}'.format(relative_file_path))
            with open(yaml_file_path_encoded) as yaml_file:
                data = yaml.load(yaml_file)
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
            sorted_row_by_start = sorted(row_by_start.items())

            relative_ipp_paths_by_start = {}
            unsorted_relative_ipp_paths = set()
            for start, row in sorted_row_by_start:
                relative_ipp_paths_by_start[start] = start_relative_ipp_paths = []
                for name, child in row.items():
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
            # tax_rate_tree_by_bracket_type = {}

            for start, row in sorted_row_by_start:
                for relative_ipp_path in sorted_relative_ipp_paths:
                    value = row
                    for fragment in relative_ipp_path:
                        value = value.get(fragment)
                        if value is None:
                            break

                    if value in (u'-', u'na', u'nc'):
                        # Value is unknown. Previous value must be propagated.
                        continue
                    ipp_path = [
                        fragment if fragment in ('RENAME', 'TRANCHE', 'TYPE') else strings.slugify(fragment,
                            separator = u'_')
                        for fragment in itertools.chain(
                            relative_file_path.split(os.sep)[:-1],
                            [sheet_name],
                            relative_ipp_path,
                            )
                        ]

                    sub_tree = tree
                    for fragment in ipp_path[:-1]:
                        sub_tree = sub_tree.setdefault(fragment, collections.OrderedDict())
                    fragment = ipp_path[-1]
                    sub_tree = sub_tree.setdefault(fragment, [])
                    if sub_tree:
                        previous_leaf = sub_tree[-1]
                        if previous_leaf['value'] == value:
                            # Merge leaves with the same value.
                            # One day, when we'll support "Références législatives", this behavior may change.
                            continue
                    sub_tree.append(dict(
                        start = start,
                        value = value,
                        ))
    return tree


def iter_ipp_values(node):
    if isinstance(node, dict):
        for name, child in node.items():
            for path, value in iter_ipp_values(child):
                yield [name] + path, value
    else:
        yield [], node


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


def ipp_node_to_element(name, node):
    """
    A `node` is a dict or a list produced by `build_tree_from_yaml_clean` or `transform_ipp_tree`.
    """
    if isinstance(node, dict):
        if node.get('TYPE') == u'BAREME':
            bareme_element = etree.Element('BAREME', attrib = dict(
                code = strings.slugify(name, separator = u'_'),
                origin = u'ipp',
                ))
            for slice_name in node.get('SEUIL', {}).keys():
                tranche_element = etree.Element('TRANCHE', attrib = dict(
                    code = strings.slugify(slice_name, separator = u'_'),
                    ))

                seuil_element = etree.Element('SEUIL')
                values, format, type = prepare_xml_values(name, node.get('SEUIL', {}).get(slice_name, []))
                transform_values_to_element_children(values, seuil_element)
                if len(seuil_element) > 0:
                    tranche_element.append(seuil_element)

                taux_element = etree.Element('TAUX')
                values, format, type = prepare_xml_values(name, node.get('TAUX', {}).get(slice_name, []))
                transform_values_to_element_children(values, taux_element)
                if len(taux_element) > 0:
                    tranche_element.append(taux_element)

                if len(tranche_element) > 0:
                    bareme_element.append(tranche_element)
            return bareme_element if len(bareme_element) > 0 else None
        else:
            node_element = etree.Element('NODE', attrib = dict(
                code = strings.slugify(name, separator = u'_'),
                origin = u'ipp',
                ))
            for key, value in node.items():
                child_element = ipp_node_to_element(key, value)
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
            origin = u'ipp',
            ))
        if format is not None:
            code_element.set('format', format)
        if type is not None:
            code_element.set('type', type)
        transform_values_to_element_children(values, code_element)
        return code_element if len(code_element) > 0 else None


def transform_values_to_element_children(values, element):
    element.extend(map(
        lambda value: etree.Element('VALUE', attrib = dict(
            deb = value['start'].isoformat(),
            valeur = unicode(value['value']),
            )),
        values,
        ))


def write_xml_file(xml_dir, file_name, element):
    element_tree = etree.ElementTree(element)
    element_tree.write(
        os.path.join(xml_dir, file_name),
        encoding = 'utf-8',
        pretty_print = True,
        )


def transform(yaml_clean_dir, xml_dir):
    ipp_tree = build_tree_from_yaml_clean(yaml_clean_dir)
    transform_ipp_tree(ipp_tree)  # User-written transformations which modify `ipp_tree`.
    ipp_root_element = ipp_node_to_element(u'root', ipp_tree)

    for child_element in ipp_root_element:
        write_xml_file(xml_dir, '{}.xml'.format(child_element.attrib['code']), child_element)
        ipp_root_element.remove(child_element)
    write_xml_file(xml_dir, '__root__.xml', ipp_root_element)
