# -*- coding: utf-8 -*-

import os
import shutil
import sys
import yaml

PARENT_DIRECTORY = os.path.abspath('../..')
PATH_LENGTH_TO_IGNORE = len(PARENT_DIRECTORY)

PARAMETERS_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'parameters')
PATH_MAX_LENGTH = 150

CLEANED_PARAMETERS_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'new_parameters')
INDEX_FILENAME = 'index.yaml'


def list_long_paths(absolute_directory_path):
    long_paths = []

    for directory, sub_directories, files in os.walk(absolute_directory_path):
        for f in files:
            file_path = os.path.join(directory, f)
            if (len(file_path) - PATH_LENGTH_TO_IGNORE) > PATH_MAX_LENGTH:
                path_extract = clean_from_filename(get_sub_parent_path(file_path, PARAMETERS_DIRECTORY))
                if path_extract not in long_paths:
                    long_paths.append(path_extract)

    return long_paths


def get_sub_parent_path(directory_path, parent_path):
    absolute_path = os.path.abspath(directory_path)
    return os.path.relpath(absolute_path, parent_path)


def clean_from_filename(relative_path):
    last_separator_index = relative_path.rfind(os.path.sep)
    if last_separator_index == -1:
        raise ValueError(u'Directory expected but none found in: ' + relative_path)
    return relative_path[:last_separator_index]


def merge(directory, fList, destination_path):
    print os.linesep
    print "Merging in: " + destination_path
    if not fList:
        return []

    with open(destination_path, 'a') as yaml_file:
        for f in fList:
            filepath = os.path.join(directory, f)
            with open(filepath, 'r') as stream:
                filename = os.path.splitext(os.path.basename(f))[0]
                fDict = {filename: None}
                fDict[filename] = yaml.load(stream)
                yaml_file.write(yaml.dump(fDict, default_flow_style=False))


def new_parameters_directory(old_directory, new_directory, paths_to_clean):
    # Clean directory content
    if os.path.exists(new_directory):
        shutil.rmtree(new_directory)
    os.mkdir(new_directory)


    # Loop on directories
    for directory, sub_directories, files in os.walk(old_directory):
        functional_path = get_sub_parent_path(directory, old_directory)
        new_path = os.path.join(new_directory, functional_path)

        if functional_path in paths_to_clean:
            # If current directory is too long, create directory but merge its content in one file
            old_index = os.path.join(directory, INDEX_FILENAME)
            new_index = os.path.join(new_path, INDEX_FILENAME)
            # Keep index.yaml
            shutil.copyfile(old_index, new_index)
            # Merge all in index.yaml
            files.remove(INDEX_FILENAME)
            merge(directory, files, new_index)
        else:
            # If current directory isn't too long, don't change it
            if not os.path.exists(new_path):
                shutil.copytree(directory, new_path)


long_parameters_paths = list_long_paths(PARAMETERS_DIRECTORY)
print str(len(long_parameters_paths)) + " directories have files with more than " + str(PATH_MAX_LENGTH) + \
    " characters in their paths starting from this directory: " + PARENT_DIRECTORY

new_parameters_directory(PARAMETERS_DIRECTORY, CLEANED_PARAMETERS_DIRECTORY, long_parameters_paths)
# m = merge(["../../parameters/impot_revenu/plus_values/imposition_des_plus_values_mobilieres_levees_d_options_attribuees_depuis_27_4_2000_cessions_realisees_moins_de_deux_ans_apres_la_levee/index.yaml",
#              "../../parameters/impot_revenu/plus_values/imposition_des_plus_values_mobilieres_levees_d_options_attribuees_depuis_27_4_2000_cessions_realisees_moins_de_deux_ans_apres_la_levee/seuil_tranche_superieure.yaml"
# ], "./toto.yaml")
