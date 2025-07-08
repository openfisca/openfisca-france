#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# flake8: noqa: T201
'''
Script to extract Enum values for variables listed in a CSV file,
group them by entity, and export them to separate text files.
'''

import csv
import os
import re
import json
from collections import defaultdict
from pathlib import Path

# Define constants
MODEL_DIR = './openfisca_france/model'
CSV_FILE = './openfisca_france/scripts/output/input_variable.csv'
OUTPUT_DIR = './openfisca_france/scripts/output/'


def preload_definitions(model_directory):
    '''
    Parses all Python files in the model directory to build maps of
    variable definitions and Enum class definitions.
    '''
    variable_definitions = {}
    enum_definitions = {}
    model_path = Path(model_directory)

    for file_path in model_path.rglob('*.py'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. Find all Enum classes and their values
            # This pattern captures the class name and its body until the next class/def or end of file
            enum_class_pattern = r"class\s+([a-zA-Z0-9_]+)\(Enum\):((?:.|\n)*?)(?=\nclass|\ndef|\Z)"
            for match in re.finditer(enum_class_pattern, content, re.DOTALL):
                enum_name = match.group(1)
                class_body = match.group(2)

                # First, try to find an '__order__' attribute for explicit ordering
                order_match = re.search(r"__order__\s*=\s*['\"](.*?)['\"]", class_body)
                if order_match:
                    enum_values = order_match.group(1)
                    enum_definitions[enum_name] = enum_values
                else:
                    # If no '__order__', parse members directly from assignments
                    members = []
                    # Regex to find valid python identifiers at the start of a line, followed by =
                    member_pattern = re.compile(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=')
                    for line in class_body.split('\n'):
                        member_match = member_pattern.match(line)
                        if member_match:
                            member_name = member_match.group(1)
                            # Exclude special 'dunder' methods
                            if not (member_name.startswith('__') and member_name.endswith('__')):
                                members.append(member_name)

                    if members:
                        enum_definitions[enum_name] = ' '.join(members)

            # 2. Find all Variable classes and link them to their Enum
            var_pattern = r"class\s+([a-zA-Z0-9_]+)\(Variable\):((?:.|\n)*?)(?=\nclass|\ndef|\Z)"
            for match in re.finditer(var_pattern, content):
                variable_name = match.group(1)
                class_body = match.group(2)

                # Check if it's an Enum type
                type_match = re.search(r'value_type\s*=\s*Enum', class_body)
                if type_match:
                    # Find the associated possible_values class
                    possible_values_match = re.search(r"possible_values\s*=\s*([a-zA-Z0-9_]+)", class_body)
                    if possible_values_match:
                        enum_class_name = possible_values_match.group(1)
                        variable_definitions[variable_name] = enum_class_name

        except Exception as e:
            print(f"Warning: Could not process file {file_path}. Error: {e}")

    return variable_definitions, enum_definitions


def main():
    '''Main function to execute the script.'''
    variable_to_enum_class, enum_class_to_values = preload_definitions(MODEL_DIR)
    print(f"Found {len(variable_to_enum_class)} variables with Enum types and {len(enum_class_to_values)} Enum classes.")
    all_enum = []
    for var, enum in variable_to_enum_class.items():
        all_enum.append({
            var: enum_class_to_values.get(enum, 'N/A').split(' '),
            })


    print(all_enum)
    # Save to file
    with open(OUTPUT_DIR + 'all_enums.json', 'w', encoding='utf-8') as f:
        json.dump(all_enum, f, ensure_ascii=False, indent=4)

    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file not found at {CSV_FILE}")
        return

    print(f"Reading variables from {CSV_FILE}...")
    entity_enums = defaultdict(dict)

    try:
        with open(CSV_FILE, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                variable_name = row.get('variable')
                entity = row.get('entite')

                if not variable_name or not entity:
                    continue

                # Check if this variable is an Enum type
                if variable_name in variable_to_enum_class:
                    enum_class = variable_to_enum_class[variable_name]
                    # Get the values for that Enum class
                    if enum_class in enum_class_to_values:
                        values = enum_class_to_values[enum_class]
                        entity_enums[entity][variable_name] = values
    except Exception as e:
        print(f"Error reading or processing CSV file: {e}")
        return


if __name__ == '__main__':
    main()
