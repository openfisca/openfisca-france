#! /usr/bin/env python

import os
import re
import sys

import yaml

DATE_REGEXP = re.compile(r'^(0001-01-01|[12]\d{3}-(0[1-9]|1[012])-(0[1-9]|[12]\d|3[01]))$')
SHARED_KEYS = ['description', 'documentation', 'file_path', 'metadata', 'name', 'reference', 'unit']


def unfold_parameter(ids, source_parameter, target_dir):
    if 'brackets' in source_parameter:
        # Parameter is a scale.
        write_parameter(ids, source_parameter, target_dir)
    else:
        values = source_parameter.get('values')
        if values is None:
            children_keys = [
                key
                for key in source_parameter
                if key not in SHARED_KEYS
                ]
            assert len(children_keys) > 0
            if all(re.match(DATE_REGEXP, child_key) for child_key in children_keys):
                # Parameter is a value.
                write_parameter(ids, source_parameter, target_dir)
            else:
                # Parameter is a node to unfold.
                index = {
                    key: value
                    for key, value in source_parameter.items()
                    if key in SHARED_KEYS
                    }
                if len(index) > 0:
                    write_parameter(ids + ['index'], index, target_dir)
                for child_id in children_keys:
                    unfold_parameter(ids + [child_id], source_parameter[child_id], target_dir)
        else:
            # Parameter is a value.
            write_parameter(ids, source_parameter, target_dir)


def write_parameter(ids, parameter, target_dir):
    dir = os.path.join(target_dir, *ids[:-1])
    os.makedirs(dir, exist_ok=True)
    with open(os.path.join(dir, f'{ids[-1]}.yaml'), 'w') as parameter_file:
        yaml.dump(parameter, parameter_file, allow_unicode=True)


yaml_source_file_path = sys.argv[1]
assert yaml_source_file_path.endswith('.yaml'), 'Argument must be a YAML file path.'
with open(yaml_source_file_path, 'r', encoding='utf-8') as yaml_source_file:
    source_parameter = yaml.safe_load(yaml_source_file)
target_dir, yaml_source_filename = os.path.split(yaml_source_file_path)
id = os.path.splitext(yaml_source_filename)[0]
unfold_parameter([id], source_parameter, target_dir)
