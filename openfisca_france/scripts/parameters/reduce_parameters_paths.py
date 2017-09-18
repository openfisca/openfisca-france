# -*- coding: utf-8 -*-

import os

PARENT_DIRECTORY = os.path.realpath('../..')
PATH_LENGTH_TO_IGNORE = len(PARENT_DIRECTORY)

PARAMETERS_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'parameters')
PATH_MAX_LENGTH = 150

CLEANED_PARAMETERS_DIRECTORY = os.path.join(PARENT_DIRECTORY, 'new_parameters')


def list_long_paths(absolute_directory_path):
    # print absolute_directory_path
    long_paths = []

    for directory, sub_directories, files in os.walk(absolute_directory_path):
        for f in files:
            file_path = os.path.join(directory, f)
            sub_path_length = len(file_path) - PATH_LENGTH_TO_IGNORE
            if(sub_path_length > PATH_MAX_LENGTH):
                # print(str(sub_path_length) + " " + os.path.relpath(file_path, PARENT_DIRECTORY))
                long_paths.append(file_path)

    return long_paths


def reduce_long_paths(long_paths_list):
    for file_path in long_paths_list:
        print os.path.dirname(file_path)


long_parameters_paths = list_long_paths(PARAMETERS_DIRECTORY)
print str(len(long_parameters_paths)) + " files have more than " + str(PATH_MAX_LENGTH) + \
    " characters in their paths starting from this directory: " + PARENT_DIRECTORY

reduce_long_paths(long_parameters_paths)
