#! /usr/bin/env python
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


"""Merge YAML files of IPP tax and benefit tables with OpenFisca parameters to generate new parameters."""


import argparse
import collections
import cStringIO
import datetime
import logging
import os
import sys
from xml.sax.saxutils import quoteattr

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
    parser.add_argument('-s', '--source-dir', default = 'yaml-clean',
        help = 'path of source directory containing clean IPP YAML files')
    parser.add_argument('-t', '--target', default = os.path.join(parameters_dir, 'parameters.xml'),
        help = 'path of generated YAML file containing the association between IPP fields with OpenFisca parameters')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    file_system_encoding = sys.getfilesystemencoding()

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
                # print x
                # print y
                # print unsorted_relative_ipp_paths
                # print relative_ipp_paths_by_start
                # assert False, "This should not occur."

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
                            if fragment == u'BAREME':
                                existing_type = sub_tree.get('TYPE')
                                if existing_type is None:
                                    sub_tree['TYPE'] = fragment
                                else:
                                    assert existing_type == fragment
                            elif fragment == u'SEUIL':
                                assert sub_tree.get('TYPE') == u'BAREME', str((translated_path, sub_path, sub_tree))
                                assert not sub_path
                                slice_name = remaining_path.pop(0)
                                assert not remaining_path
                                sub_tree = sub_tree.setdefault(u'SEUILS', collections.OrderedDict()).setdefault(
                                    slice_name, [])
                            elif fragment == u'TAUX':
                                assert sub_tree.get('TYPE') == u'BAREME', str((translated_path, sub_path, sub_tree))
                                assert not sub_path
                                slice_name = remaining_path.pop(0)
                                assert not remaining_path
                                sub_tree = sub_tree.setdefault(u'TAUX', collections.OrderedDict()).setdefault(
                                    slice_name, [])
                            # elif fragment == u'TRANCHE':
                            #     assert sub_tree.get('TYPE') == u'BAREME'
                            #     sub_tree = sub_tree.setdefault(u'TRANCHES', [])
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

    with open(args.target, 'w') as target_file:
        print_xml(target_file, u'root', tree)

    return 0


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


def print_xml(file, name, node, depth = 0):
    if isinstance(node, dict):
        if node.get('TYPE') == u'BAREME':
            slices_file = cStringIO.StringIO()
            has_slices = False
            slices_name = node.get('SEUILS', {}).keys()
            for slice_name in slices_name:
                has_amounts = False
                amounts_file = cStringIO.StringIO()
                amounts, format, type = prepare_xml_values(name, node.get('MONTANT', {}).get(slice_name, []))
                for amount in amounts:
                    has_amounts = print_xml_value(amounts_file, amount, depth = depth + 3) or has_amounts

                has_bases = False
                bases_file = cStringIO.StringIO()
                bases, format, type = prepare_xml_values(name, node.get('ASSIETTE', {}).get(slice_name, []))
                for base in bases:
                    has_bases = print_xml_value(bases_file, base, depth = depth + 3) or has_bases

                has_rates = False
                rates_file = cStringIO.StringIO()
                rates, format, type = prepare_xml_values(name, node.get('TAUX', {}).get(slice_name, []))
                for rate in rates:
                    has_rates = print_xml_value(rates_file, rate, depth = depth + 3) or has_rates

                has_thresholds = False
                thresholds_file = cStringIO.StringIO()
                thresholds, format, type = prepare_xml_values(name, node.get('SEUILS', {}).get(slice_name, []))
                for threshold in thresholds:
                    has_thresholds = print_xml_value(thresholds_file, threshold, depth = depth + 3) or has_thresholds

                if has_bases or has_amounts or has_rates or has_thresholds:
                    slices_file.write(u'{indent}<TRANCHE code="{name}">\n'.format(
                        indent = u'  ' * (depth + 1),
                        name = strings.slugify(slice_name, separator = u'_'),
                        ).encode('utf-8'))
                    if has_thresholds:
                        slices_file.write(u'{indent}<SEUIL>\n'.format(
                            indent = u'  ' * (depth + 2),
                            ).encode('utf-8'))
                        slices_file.write(thresholds_file.getvalue())
                        slices_file.write(u'{indent}</SEUIL>\n'.format(
                            indent = u'  ' * (depth + 2),
                            ).encode('utf-8'))
                    if has_amounts:
                        slices_file.write(u'{indent}<MONTANT>\n'.format(
                            indent = u'  ' * (depth + 2),
                            ).encode('utf-8'))
                        slices_file.write(amounts_file.getvalue())
                        slices_file.write(u'{indent}</MONTANT>\n'.format(
                            indent = u'  ' * (depth + 2),
                            ).encode('utf-8'))
                    if has_rates:
                        slices_file.write(u'{indent}<TAUX>\n'.format(
                            indent = u'  ' * (depth + 2),
                            ).encode('utf-8'))
                        slices_file.write(rates_file.getvalue())
                        slices_file.write(u'{indent}</TAUX>\n'.format(
                            indent = u'  ' * (depth + 2),
                            ).encode('utf-8'))
                    if has_bases:
                        slices_file.write(u'{indent}<ASSIETTE>\n'.format(
                            indent = u'  ' * (depth + 2),
                            ).encode('utf-8'))
                        slices_file.write(bases_file.getvalue())
                        slices_file.write(u'{indent}</ASSIETTE>\n'.format(
                            indent = u'  ' * (depth + 2),
                            ).encode('utf-8'))
                    slices_file.write(u'{indent}</TRANCHE>\n'.format(
                        indent = u'  ' * (depth + 1),
                        ).encode('utf-8'))
                    has_slices = True
            if not has_slices:
                return False
            file.write(u'{indent}<BAREME code="{name}">\n'.format(
                indent = u'  ' * depth,
                name = strings.slugify(name, separator = u'_'),
                ).encode('utf-8'))
            file.write(slices_file.getvalue())
            file.write(u'{indent}</BAREME>\n'.format(
                indent = u'  ' * depth,
                ).encode('utf-8'))
            return True
        else:
            items_file = cStringIO.StringIO()
            has_children = False
            for key, value in node.iteritems():
                has_children = print_xml(items_file, key, value, depth = depth + 1) or has_children
            if not has_children:
                return False
            file.write(u'{indent}<NODE code="{name}">\n'.format(
                indent = u'  ' * depth,
                name = strings.slugify(name, separator = u'_'),
                ).encode('utf-8'))
            file.write(items_file.getvalue())
            file.write(u'{indent}</NODE>\n'.format(
                indent = u'  ' * depth,
                ).encode('utf-8'))
            return True
    else:
        assert isinstance(node, list), node
        # Print list of leafs as a single CODE element.
        leafs, format, type = prepare_xml_values(name, node)
        if not leafs:
            return False
        file.write(u'{indent}<CODE code="{name}"{format}{type}>\n'.format(
            format = u' format="{}"'.format(format) if format is not None else u'',
            indent = u'  ' * depth,
            name = strings.slugify(name, separator = u'_'),
            type = u' type="{}"'.format(type) if type is not None else u'',
            ).encode('utf-8'))
        for leaf in leafs:
            print_xml_value(file, leaf, depth = depth + 1)
        file.write(u'{}</CODE>\n'.format(u'  ' * depth).encode('utf-8'))
        return True


def print_xml_value(file, leaf, depth = 0):
    start = leaf.get('start')
    stop = leaf.get('stop')
    file.write(u'{indent}<VALUE{start}{stop} valeur={value}/>\n'.format(
        indent = u'  ' * depth,
        start = u' deb="{}"'.format(start.isoformat()) if start is not None else u'',
        stop = u' fin="{}"'.format(stop.isoformat()) if stop is not None else u'',
        value = quoteattr(unicode(leaf['value'])),
        ).encode('utf-8'))
    return True


# def translate_path(remaining_path, translations, translated_path = None):
#     if not remaining_path:
#         return translated_path
#     if isinstance(remaining_path, tuple):
#         remaining_path = list(remaining_path)
#     if translated_path is None:
#         translated_path = ()
#     name = remaining_path.pop(0)
#     if translations is not None:
#         translations = translations.get(name)
#         if translations is not None:
#             if isinstance(translations, dict):
#                 translation = translations.get('RENAME')
#                 if translation is not None:
#                     name = translation
#             else:
#                 name = translations
#                 translations = None
#     if isinstance(name, basestring):
#         name = (name,)
#     if isinstance(name, list):
#         name = tuple(name)
#     return translate_path(remaining_path, translations, translated_path + name)


if __name__ == "__main__":
    sys.exit(main())
