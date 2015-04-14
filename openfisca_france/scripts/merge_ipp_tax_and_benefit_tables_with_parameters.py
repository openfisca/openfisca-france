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


def iter_openfisca_values(node):
    type = node['@type']
    if type == 'Node':
        for name, child in node['children'].iteritems():
            for path, start, value in iter_openfisca_values(child):
                yield [name] + path, start, value
    elif type == 'Parameter':
        for dated_value in node['values']:
            value = dated_value['value']
            if isinstance(value, float) and value == int(value):
                value = int(value)
            yield [], dated_value['start'], value
    else:
        assert type == 'Scale', type
        for bracket in node['brackets']:
            for i, amount in enumerate(bracket.get('amount') or []):
                value = amount['value']
                if isinstance(value, float) and value == int(value):
                    value = int(value)
                yield [u'amount', i], amount['start'], value
            for i, base in enumerate(bracket.get('base') or []):
                value = base['value']
                if isinstance(value, float) and value == int(value):
                    value = int(value)
                yield [u'base', i], base['start'], value
            for i, rate in enumerate(bracket.get('rate') or []):
                value = rate['value']
                if isinstance(value, float) and value == int(value):
                    value = int(value)
                yield [u'rate', i], rate['start'], value
            for i, threshold in enumerate(bracket.get('threshold') or []):
                value = threshold['value']
                if isinstance(value, float) and value == int(value):
                    value = int(value)
                yield [u'threshold', i], threshold['start'], value


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-r', '--rules',
    #     default = os.path.join(parameters_dir, 'ipp-tax-and-benefit-tables-to-openfisca-parameters.yaml'),
    #     help = 'path of YAML file containing the association between IPP fields and OpenFisca parameters')
    parser.add_argument('-s', '--source-dir', default = 'yaml-clean',
        help = 'path of source directory containing clean IPP YAML files')
    parser.add_argument('-t', '--target', default = os.path.join(parameters_dir, 'parameters.xml'),
        help = 'path of generated YAML file containing the association between IPP fields with OpenFisca parameters')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    file_system_encoding = sys.getfilesystemencoding()

    # with open(args.rules) as rules_file:
    #     rules = yaml.load(rules_file)

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

            for start, row in sorted(row_by_start.iteritems()):
                for name, child in row.iteritems():
                    if name in date_names:
                        continue
                    if name in note_names:
                        continue
                    if name in reference_names:
                        continue
                    for path, value in iter_ipp_values(child):
                        if value in (u'-', u'na', u'nc'):
                            # Value is unknown. Previous value must  be propagated.
                            continue
                        full_path = tuple(relative_file_path.split(os.sep)[:-1]) + (sheet_name, name) + tuple(path)
                        sub_tree = tree
                        for fragment in full_path[:-1]:
                            sub_tree = sub_tree.setdefault(fragment, collections.OrderedDict())
                        leafs = sub_tree.setdefault(full_path[-1], [])
                        if leafs:
                            last_leaf = leafs[-1]
                            if last_leaf['value'] == value:
                                continue
                            last_leaf['stop'] = start - datetime.timedelta(days = 1)
                        leafs.append(dict(
                            start = start,
                            value = value,
                            ))

    print_xml(sys.stdout, u'root', tree)

    return 0


def print_xml(file, name, node, depth = 0):
    if isinstance(node, dict):
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
        leafs = list(reversed([
            leaf
            for leaf in node
            if leaf['value'] is not None
            ]))
        if not leafs:
            return False
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
                            return False
                        value = value / 100
                    else:
                        if format is None:
                            format = u'float'
                        elif format != u'float':
                            log.warning(u'Non constant float format {} in {}: {}'.format(format, name, leafs))
                            return False
                        if type is None:
                            type = u'monetary'
                        elif type != u'monetary':
                            log.warning(u'Non constant monetary type {} in {}: {}'.format(type, name, leafs))
                            return False
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
        file.write(u'{indent}<CODE code="{name}"{format}{type}>\n'.format(
            format = u' format="{}"'.format(format) if format is not None else u'',
            indent = u'  ' * depth,
            name = strings.slugify(name, separator = u'_'),
            type = u' type="{}"'.format(type) if type is not None else u'',
            ).encode('utf-8'))
        for leaf in leafs:
            value = leaf['value']
            start = leaf.get('start')
            stop = leaf.get('stop')
            file.write(u'{indent}<VALUE{start}{stop} valeur="{value}"/>\n'.format(
                indent = u'  ' * (depth + 1),
                start = u' deb="{}"'.format(start.isoformat()) if start is not None else u'',
                stop = u' fin="{}"'.format(stop.isoformat()) if stop is not None else u'',
                value = quoteattr(unicode(value)),
                ).encode('utf-8'))
        file.write(u'{}</CODE>\n'.format(u'  ' * depth).encode('utf-8'))
        return True


if __name__ == "__main__":
    sys.exit(main())
