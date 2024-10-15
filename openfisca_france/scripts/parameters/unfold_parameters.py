#! /usr/bin/env python
'''
Unfold parameters located in path
'''


import argparse
import glob
import logging
import os
import re
import sys

import yaml


DATE_REGEXP = re.compile(
    r'^(0001-01-01|[12]\d{3}-(0[1-9]|1[012])-(0[1-9]|[12]\d|3[01]))$'
    )
SHARED_KEYS = ['description', 'documentation', 'file_path', 'metadata', 'name', 'unit']


app_name = os.path.splitext(os.path.basename(__file__))[0]
logger = logging.getLogger(app_name)


# See https://ttl255.com/yaml-anchors-and-aliases-and-how-to-disable-them/
class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def add_dated_metadata_to_parameter(
        parameter,
        dates,
        note_by_date,
        reference_by_date,
        official_journal_date_by_date,
        encountered_dates,
        ):
    metadata = parameter.get('metadata', {})
    for date in dates:
        for key, value_by_date in (
                ('notes', note_by_date),
                ('official_journal_date', official_journal_date_by_date),
                ('reference', reference_by_date),
                ):
            value_at_date = value_by_date.get(date)
            if value_at_date is not None:
                metadata_value = metadata.get(key)
                if metadata_value is None:
                    metadata_value = metadata[key] = {}
                if metadata_value.get(date) is None:
                    metadata_value[date] = value_at_date
    if metadata and parameter.get('metadata') is None:
        parameter['metadata'] = metadata
    encountered_dates.update(dates)


def unfold_file(yaml_source_file_path, remove_source = False):
    assert yaml_source_file_path.endswith('.yaml'), '{} must be a YAML file path.'.format(yaml_source_file_path)
    with open(yaml_source_file_path, 'r', encoding='utf-8') as yaml_source_file:
        source_parameter = yaml.safe_load(yaml_source_file)
    target_dir, yaml_source_filename = os.path.split(yaml_source_file_path)
    id = os.path.splitext(yaml_source_filename)[0]
    parameter_is_unfolded = unfold_parameter([id], source_parameter, target_dir, {}, {}, {}, set())
    if remove_source and parameter_is_unfolded:
        os.remove(yaml_source_file_path)


def unfold_path(yaml_source_path, remove_source = False):
    if os.path.isfile(yaml_source_path):
        logger.debug('Unfolding file {}'.format(yaml_source_path))
        unfold_file(yaml_source_file_path = yaml_source_path, remove_source = remove_source)
    else:
        assert os.path.isdir(yaml_source_path), '{} is not a directory'.format(yaml_source_path)
        if len(os.listdir(yaml_source_path)) == 0:
            return
        logger.debug('Unfolding directory {}'.format(yaml_source_path))

        yaml_source_files_paths = glob.glob(os.path.join(yaml_source_path, '**/*.yaml'), recursive = True)
        for yaml_source_file_path in yaml_source_files_paths:
            if yaml_source_file_path.endswith('index.yaml'):
                continue
            unfold_path(yaml_source_file_path, remove_source = remove_source)


def unfold_parameter(
        ids,
        source_parameter,
        target_dir,
        # Metadata that must dispatched to children
        # when they have a value with a matching date.
        note_by_date,
        reference_by_date,
        official_journal_date_by_date,
        # Filled with dates appearing in children.
        encountered_dates,
        ):
    assert 'reference' not in source_parameter, \
        f"Property 'reference' of parameter {'.'.join(ids)} must be moved into metadata"
    if 'brackets' in source_parameter:
        # Parameter is a scale.
        brackets = source_parameter['brackets']
        dates = set()
        for key in ('amount', 'average_rate', 'base', 'rate', 'threshold'):
            value_by_date = brackets.get(key)
            if value_by_date is not None:
                dates.update(value_by_date.keys())
        add_dated_metadata_to_parameter(
            source_parameter,
            dates,
            note_by_date,
            reference_by_date,
            official_journal_date_by_date,
            encountered_dates,
            )
        write_parameter(ids, source_parameter, target_dir)
        return False  # File has not been unfolded.
    else:
        values = source_parameter.get('values')
        if values is None:
            children_keys = [
                key
                for key in source_parameter
                if key not in SHARED_KEYS
                ]
            assert children_keys
            if all(re.match(DATE_REGEXP, child_key) for child_key in children_keys):
                # Parameter is a value.
                add_dated_metadata_to_parameter(
                    source_parameter,
                    children_keys,
                    note_by_date,
                    reference_by_date,
                    official_journal_date_by_date,
                    encountered_dates,
                    )
                write_parameter(ids, source_parameter, target_dir)
                return False  # File has not been unfolded.
            else:
                # Parameter is a node to unfold.

                metadata = source_parameter.get('metadata', {})
                children_note_by_date = {**note_by_date, **metadata.get('notes', {})}
                children_reference_by_date = {
                    **reference_by_date,
                    **metadata.get('reference', {}),
                    }
                children_official_journal_date_by_date = {
                    **official_journal_date_by_date,
                    **metadata.get('official_journal_date', {}),
                    }
                for child_id in children_keys:
                    unfold_parameter(
                        ids + [child_id],
                        source_parameter[child_id],
                        target_dir,
                        children_note_by_date,
                        children_reference_by_date,
                        children_official_journal_date_by_date,
                        encountered_dates,
                        )

                # Remove metadata dispatched to children from index metadata.
                for key in ('notes', 'reference', 'official_journal_date'):
                    value_by_date = metadata.get(key)
                    if value_by_date is not None:
                        for date in encountered_dates:
                            value_by_date.pop(date, None)
                        if not value_by_date:
                            del metadata[key]
                if not metadata:
                    source_parameter.pop('metadata', None)

                index = {
                    key: value
                    for key, value in source_parameter.items()
                    if key in SHARED_KEYS
                    }
                if index:
                    write_parameter(ids + ['index'], index, target_dir)
                return True  # File has been unfolded.
        else:
            # Parameter is a value.
            add_dated_metadata_to_parameter(
                source_parameter,
                source_parameter['values'].keys(),
                note_by_date,
                reference_by_date,
                official_journal_date_by_date,
                encountered_dates,
                )
            write_parameter(ids, source_parameter, target_dir)
            return False  # File has not been unfolded.


def write_parameter(ids, parameter, target_dir):
    dir = os.path.join(target_dir, *ids[:-1])
    os.makedirs(dir, exist_ok=True)
    with open(os.path.join(dir, f'{ids[-1]}.yaml'), 'w', encoding='utf-8') as parameter_file:
        yaml.dump(parameter, parameter_file, allow_unicode=True, Dumper=NoAliasDumper)


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('-p', '--path', help = 'Parameters path a file or a directory)')
    parser.add_argument('-r', '--remove-source', action = 'store_true', default = False, help = 'remove source files')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = 'increase output verbosity')
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING)
    yaml_source_path = args.path
    remove_source = args.remove_source
    unfold_path(yaml_source_path, remove_source = remove_source)


if __name__ == '__main__':
    sys.exit(main())
