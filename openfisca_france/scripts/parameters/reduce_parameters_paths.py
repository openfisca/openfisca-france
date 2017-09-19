# -*- coding: utf-8 -*-

import os
import shutil


PARENT_DIRECTORY = os.path.abspath('../..')
PATH_LENGTH_TO_IGNORE = len(PARENT_DIRECTORY)

PARAMETERS_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'parameters')
PATH_MAX_LENGTH = 150

CLEANED_PARAMETERS_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'new_parameters')


def list_long_paths(absolute_directory_path):
    long_paths = []

    for directory, sub_directories, files in os.walk(absolute_directory_path):
        for f in files:
            file_path = os.path.join(directory, f)
            sub_path_length = len(file_path) - PATH_LENGTH_TO_IGNORE
            if(sub_path_length > PATH_MAX_LENGTH):
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


def new_parameters_directory(old_directory, new_directory, paths_to_clean):
    # Clean directory content
    if os.path.exists(new_directory):
        shutil.rmtree(new_directory)
    os.mkdir(new_directory)

    # Loop on directories
    for directory, sub_directories, files in os.walk(old_directory):
        for sub_directory in sub_directories:
            functional_path = get_sub_parent_path(os.path.join(directory, sub_directory), old_directory)
            new_path = os.path.join(new_directory, functional_path)

            if functional_path in paths_to_clean:
                # If current directory is too long, create directory but merge its content in one file
                print ""
            else:
                # If current directory isn't too long, don't change it
                print os.path.join(directory, sub_directory) + " > " + new_path
                if not os.path.exists(new_path):
                    shutil.copytree(os.path.join(directory, sub_directory), new_path)

long_parameters_paths = list_long_paths(PARAMETERS_DIRECTORY)
print str(len(long_parameters_paths)) + " directories have files with more than " + str(PATH_MAX_LENGTH) + \
    " characters in their paths starting from this directory: " + PARENT_DIRECTORY

new_parameters_directory(PARAMETERS_DIRECTORY, CLEANED_PARAMETERS_DIRECTORY, long_parameters_paths)
