#! /usr/bin/python3
"""
Ce script sert à estimer la longueur des chemins d'arborescence des paramètres,
afin de ne pas avoir de chemins > 150 caractères (incompatible Windows).
Il est à utiliser avant de contribuer à l'harmonisation
"""
import os
import functools
import re

# from pprint import pprint
# import json


def get_directory_structure(rootdir):
    changes = []
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    Amended from https://code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk/
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1

    for path, _dirs, files in os.walk(rootdir):
        if re.search(".ipynb_checkpoints", path):
            pass
        else:
            folders = path[start:].split(os.sep)
            # On regarde les chemins qui dépassent 150 caractères
            # Ce nombre vient d'ici: https://github.com/openfisca/openfisca-france/pull/1414
            # Et on ajoute 28 caractères pour le openfisca_france/parameters/
            if len(path) > 150 + 28:
                change = True
                txt = f"Path of {len(path)} caracters here: {path}"
                print(txt)
                changes.append(txt)

            subdir = dict.fromkeys(files)
            parent = functools.reduce(dict.get, folders[:-1], dir)
            parent[folders[-1]] = subdir
    if len(changes) > 0:
        filename = "path_too_long.txt"
        
        with open(filename, "w") as outfile:
            for s in changes:
                outfile.write(s)
        print(f"Sorry, you have long path to shorten. They have been saved in {filename}")
    else:
        print("Congratulation, there is no path too long for you !!!")
    return dir


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
startpath = "{}/openfisca_france/parameters/".join(COUNTRY_DIR)
ipp_dir_structure = get_directory_structure(startpath)

# json_file = json.dumps(ipp_dir_structure)
# with open("ipp_dir_structure.json", "w") as outfile:
#    outfile.write(json_file)
