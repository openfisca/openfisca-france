#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Create a YAML file associating the fields in IPP tax and benefit tables to their matching parameters in OpenFisca."""


import argparse
import collections
import copy
import datetime
import logging
import os
import sys

import yaml


from openfisca_france import init_country


date_names = (
    u"Age de départ (AAD=Age d'annulation de la décôte)",
    u"Date",
    u"Date d'effet",
    u"Date de perception du salaire",
    u"Date ISF",
    )
log = logging.getLogger(__name__)


# YAML configuration


class folded_unicode(unicode):
    pass


class literal_unicode(unicode):
    pass


def dict_constructor(loader, node):
    return collections.OrderedDict(loader.construct_pairs(node))


yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dict_constructor)

yaml.add_representer(collections.OrderedDict, lambda dumper, data: dumper.represent_dict(
    (copy.deepcopy(key), value)
    for key, value in data.iteritems()
    ))
yaml.add_representer(dict, lambda dumper, data: dumper.represent_dict(
    (copy.deepcopy(key), value)
    for key, value in data.iteritems()
    ))
yaml.add_representer(folded_unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str',
    data, style='>'))
yaml.add_representer(literal_unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str',
    data, style='|'))
yaml.add_representer(tuple, lambda dumper, data: dumper.represent_list(data))
yaml.add_representer(unicode, lambda dumper, data: dumper.represent_scalar(u'tag:yaml.org,2002:str', data))


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
    parser.add_argument('-s', '--source-dir', default = 'yaml-clean',
        help = 'path of source directory containing clean IPP YAML files')
    parser.add_argument('-t', '--target', default = 'ipp-tax-and-benefit-tables-to-openfisca-parameters.yaml',
        help = 'path of generated YAML file containing the association between IPP fields to OpenFisca parameters')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    file_system_encoding = sys.getfilesystemencoding()

    ipp_infos_by_value = {}
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

                for name, child in row.iteritems():
                    if name in date_names:
                        continue
                    for path, value in iter_ipp_values(child):
                        if isinstance(value, basestring):
                            split_value = value.split()
                            if len(split_value) == 2 and split_value[1] in (
                                    u'%',
                                    u'AF',  # anciens francs
                                    u'CFA',  # francs CFA
                                    u'COTISATIONS',
                                    u'EUR',
                                    u'FRF',
                                    ):
                                value = float(split_value[0])
                        if isinstance(value, float) and value == int(value):
                            value = int(value)
                        full_path = tuple(relative_file_path.split(os.sep)[:-1]) + (sheet_name, name) + tuple(path)
                        ipp_infos_by_value.setdefault(value, []).append(dict(
                            path = full_path,
                            start = start,
                            ))

#    print yaml.dump(ipp_infos_by_value, allow_unicode = True, default_flow_style = False, indent = 2, width = 120)

    TaxBenefitSystem = init_country()
    tax_benefit_system = TaxBenefitSystem()

    # print yaml.dump(tax_benefit_system.legislation_json, allow_unicode = True, default_flow_style = False, indent = 2,
    #     width = 120)

#    openfisca_infos_by_value = {}
#    for path, start, value in iter_openfisca_values(tax_benefit_system.legislation_json):
#        openfisca_infos_by_value.setdefault(value, []).append(dict(
#            path = tuple(path),
#            start = start,
#            ))
#    print yaml.dump(openfisca_infos_by_value, allow_unicode = True, default_flow_style = False, indent = 2, width = 120)

#    ipp_count = {}
#    for path, start, value in iter_openfisca_values(tax_benefit_system.legislation_json):
#        ipp_infos = ipp_infos_by_value.get(value)
#        if ipp_infos is None:
#            # OpenFisca parameter doesn't exit in IPP.
#            continue
#        for ipp_info in ipp_infos:
#            if ipp_info['start'] == start:
#                ipp_child = ipp_count
#                ipp_path = ipp_info['path']
#                for name in path:
#                    ipp_child = ipp_child.setdefault(name, {})
#                    ipp_child_count = ipp_child.setdefault('count_by_path', {})
#                    for ipp_index in range(len(ipp_path)):
#                        ipp_sub_path = ipp_path[:ipp_index + 1]
#                        ipp_child_count[ipp_sub_path] = ipp_child_count.get(ipp_sub_path, 0) + 1
#    print yaml.dump(ipp_count, allow_unicode = True, default_flow_style = False, indent = 2, width = 120)

    starts_by_ipp_path_by_openfisca_path = {}
    starts_by_openfisca_path_by_ipp_path = {}
    for path, start, value in iter_openfisca_values(tax_benefit_system.legislation_json):
        ipp_infos = ipp_infos_by_value.get(value)
        if ipp_infos is None:
            # OpenFisca parameter doesn't exit in IPP.
            continue
        same_start_ipp_paths = [
            ipp_info['path']
            for ipp_info in ipp_infos
            if ipp_info['start'] == start
            ]
        if len(same_start_ipp_paths) == 1:
            ipp_path = same_start_ipp_paths[0]
            starts_by_ipp_path_by_openfisca_path.setdefault(tuple(path), {}).setdefault(ipp_path, set()).add(start)
            starts_by_openfisca_path_by_ipp_path.setdefault(ipp_path, {}).setdefault(tuple(path), set()).add(start)

#    for openfisca_path, starts_by_ipp_path in sorted(starts_by_ipp_path_by_openfisca_path.iteritems()):
##        if len(starts_by_ipp_path) == 1:
##            print u'.'.join(openfisca_path), '->', u' / '.join(starts_by_ipp_path.keys()[0])
#        if len(starts_by_ipp_path) > 1:
#            print u'.'.join(openfisca_path), '->', starts_by_ipp_path

#    for ipp_path, starts_by_openfisca_path in sorted(starts_by_openfisca_path_by_ipp_path.iteritems()):
#        if len(starts_by_openfisca_path) == 1:
#            print u' / '.join(ipp_path), '->', u'.'.join(
#                unicode(fragment)
#                for fragment in starts_by_openfisca_path.keys()[0]
#                )
##        if len(starts_by_openfisca_path) > 1:
##            print u' / '.join(ipp_path), '->', u'.'.join(
##                unicode(fragment)
##                for fragment in starts_by_openfisca_path.keys()[0]
##                )

    openfisca_path_by_ipp_tree = collections.OrderedDict()
    for ipp_path, starts_by_openfisca_path in sorted(starts_by_openfisca_path_by_ipp_path.iteritems()):
        openfisca_path_by_ipp_sub_tree = openfisca_path_by_ipp_tree
        for ipp_name in ipp_path[:-1]:
            openfisca_path_by_ipp_sub_tree = openfisca_path_by_ipp_sub_tree.setdefault(ipp_name,
                collections.OrderedDict())
        ipp_name = ipp_path[-1]
        openfisca_path_by_ipp_sub_tree[ipp_name] = [
            u'.'.join(
                unicode(fragment)
                for fragment in openfisca_name
                )
            for openfisca_name in sorted(starts_by_openfisca_path)
            ]
    with open(args.target, 'w') as target_file:
        yaml.dump(openfisca_path_by_ipp_tree, target_file, allow_unicode = True, default_flow_style = False, indent = 2,
            width = 120)

    return 0


if __name__ == "__main__":
    sys.exit(main())
