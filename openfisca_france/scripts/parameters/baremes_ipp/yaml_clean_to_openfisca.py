# -*- coding: utf-8 -*-


"""Transform clean YAML files from IPP to XML files compatible with OpenFisca."""


import collections
import datetime
import itertools
import logging
import os
import sys
import re

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
            try:
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

                    references = []
                    for reference_name in reference_names:
                        if reference_name in row:
                            references.append(row[reference_name])
                            del row[reference_name]
                    row['reference'] = ' - '.join(references)

                    row_by_start[start] = row
                sorted_row_by_start = sorted(row_by_start.iteritems())

                relative_ipp_paths_by_start = {}
                unsorted_relative_ipp_paths = set()
                for start, row in sorted_row_by_start:
                    relative_ipp_paths_by_start[start] = start_relative_ipp_paths = []
                    for name, child in row.iteritems():
                        if name in date_names:
                            continue
                        if name in note_names:
                            continue
                        if name == 'reference':
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
                                continue
                        sub_tree.append(dict(
                            start = start,
                            value = value,
                            reference = row['reference'],
                            ))
            except Exception as e:
                log.error('Parsing failed for file {} : \n{}'.format(filename_encoded, e))
    return tree


def iter_ipp_values(node):
    if isinstance(node, dict):
        for name, child in node.iteritems():
            for path, value in iter_ipp_values(child):
                yield [name] + path, value
    else:
        yield [], node


def transform_values_history_to_openfisca_format(values_list):
    new_values_dict = {}
    for element in values_list:
        value = element['value']
        unit = None
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
            if unit == '%':
                value /= 100.
                unit = '/1'
        if isinstance(value, float) and value == int(value):
            value = int(value)
        new_value = {
            'value': value,
            'reference': element['reference'],
        }
        if unit:
            new_value['unit'] = unit
        new_values_dict[element['start']] = new_value
    return new_values_dict

traduction_bareme = {
    'MONTANT': 'amount',
    'BASE': 'base',
    'SEUIL': 'threshold',
    'TAUX': 'rate',
}

def transform_node_to_openfisca_format(node):
    if isinstance(node, dict):
        if 'TYPE' in node:
            node_type = node['TYPE']
            if node_type == 'BAREME':
                bracket_names = []
                for member_french, member_english in traduction_bareme.items():
                    if member_french in node:
                        if not bracket_names:
                            bracket_names = node[member_french].keys()
                        else:
                            if set(bracket_names) != set(node[member_french].keys()):
                                log.error('Mismatch in brackets : {} vs {}'.format(bracket_names, node[member_french].keys()))
                                return
                try:
                    # tranche_1, tranche_2...
                    bracket_names = sorted(bracket_names, key = lambda x: int(x.split('_')[1]))
                except:
                    try:
                        # tranche1, tranche2...
                        bracket_names = sorted(bracket_names, key = lambda x: int(x[7:]))
                    except:
                        # I give up
                        pass
                
                brackets = []
                for bracket_name in bracket_names:
                    bracket = {}
                    for member_french, member_english in traduction_bareme.items():
                        if member_french in node:
                            bracket[member_english] = transform_values_history_to_openfisca_format(node[member_french][bracket_name])
                    brackets.append(bracket)
                return {'brackets': brackets}
            else:
                raise ValueError(node_type)
        else:
            new_node = {}
            for name, child in node.items():
                new_child = transform_node_to_openfisca_format(child)
                new_node[name] = new_child
            return new_node
    elif isinstance(node, list):
        return {
            'values': transform_values_history_to_openfisca_format(node),
            }

    raise ValueError(node)


def custom_str_representer(dumper, data):
    if re.match(r'^\d{4}-\d{2}-\d{2}$', data):
        tag = u'tag:yaml.org,2002:timestamp'
        return dumper.represent_scalar(tag, data)
    return dumper.represent_str(data)


def custom_unicode_representer(dumper, data):
    if re.match(r'^\d{4}-\d{2}-\d{2}$', data):
        tag = u'tag:yaml.org,2002:timestamp'
        return dumper.represent_scalar(tag, data)
    return dumper.represent_unicode(data)

yaml.add_representer(str, custom_str_representer, Dumper=yaml.SafeDumper)
yaml.add_representer(unicode, custom_unicode_representer, Dumper=yaml.SafeDumper)


def merge_dir(node, directory):
    print(directory)
    
    dir_children = os.listdir(directory)
    
    for name, child in node.items():
        dir_name = name
        file_name = name + '.yaml'
        if dir_name in dir_children:
            dir_path = os.path.join(directory, dir_name)
            merge_dir(child, dir_path)
        elif file_name in dir_children:
            file_path = os.path.join(directory, file_name)
            merge_file(child, file_path)
        else:
            write_node(name, child, directory)

def merge_file(node, file_path):
    return write_file(node, file_path)

def write_node(name, child, directory):
    file_name = name + '.yaml'
    file_path = os.path.join(directory, file_name)
    return write_file(child, file_path)

def write_file(node, file_path):
    with open(file_path, 'w') as f:
        yaml.safe_dump(node, f, default_flow_style=False, allow_unicode=True)
