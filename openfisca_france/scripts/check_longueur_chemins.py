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
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    Amended from https://code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk/
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1

    with open("chemins_trop_longs.json", "w") as outfile:
        for path, dirs, files in os.walk(rootdir):
            if re.search(".ipynb_checkpoints", path):
                pass
            else:
                folders = path[start:].split(os.sep)
                # On regarde les chemins qui dépassent 150 caractères
                # Ce nombre vient d'ici: https://github.com/openfisca/openfisca-france/pull/1414
                # Et on ajoute 28 caractères pour le openfisca_france/parameters/
                if len(path) > 150 + 28:
                    outfile.write("{} here: {}".format(len(path), path) + "\n \n")
                subdir = dict.fromkeys(files)
                parent = functools.reduce(dict.get, folders[:-1], dir)
                parent[folders[-1]] = subdir
    return dir


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
startpath = "{}/openfisca_france/parameters/".join(COUNTRY_DIR)
ipp_dir_structure = get_directory_structure(startpath)

# json_file = json.dumps(ipp_dir_structure)
# with open("ipp_dir_structure.json", "w") as outfile:
#    outfile.write(json_file)
