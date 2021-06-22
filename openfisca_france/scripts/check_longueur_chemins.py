#! /usr/bin/python3
"""
Ce script sert à estimer la longueur des chemins d'arborescence des paramètres,
afin de ne pas avoir de chemins > 150 caractères (incompatible Windows).
Il est à utiliser avant de contribuer à l'harmonisation
"""
import os
import functools
import re
import logging

# from pprint import pprint
# import json

logging.basicConfig(level=logging.DEBUG)


def get_directory_structure(rootdir):
    changes = []
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    Amended from https://code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk/
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    max_length = 0
    max_length_path = ''

    for path, _dirs, files in os.walk(rootdir):
        if re.search(".ipynb_checkpoints", path):
            pass
        else:
            folders = path[start:].split(os.sep)
            # Mémorise le plus long chemin, pour info.
            length = len(path)
            if length > max_length:
                max_length = length
                max_length_path = path
            # On regarde les chemins qui dépassent 150 caractères
            # Ce nombre vient d'ici: https://github.com/openfisca/openfisca-france/pull/1414
            # Et on ajoute 28 caractères pour le openfisca_france/parameters/
            if length > 150 + 28:
                txt = f"Path of {len(path)} caracters here: {path}"
                logging.info(txt)
                changes.append(txt)

            subdir = dict.fromkeys(files)
            parent = functools.reduce(dict.get, folders[:-1], dir)
            parent[folders[-1]] = subdir
    logging.debug(f'Max length path: {max_length_path} of size {max_length} < 150 + 28')
    if len(changes) > 0:
        filename = "path_too_long.txt"
        with open(filename, "w") as outfile:
            for s in changes:
                outfile.write(s)
        logging.warning(f"Sorry, you have long path to shorten. They have been saved in {filename}")
    else:
        logging.info("Congratulation, there is no path too long for you !!!")
    return dir


startpath = "./openfisca_france/parameters/"
if os.path.exists(startpath):
    ipp_dir_structure = get_directory_structure(startpath)
else:
    logging.error("Please run the script in root folder 'openfisca-france', with :",
    "\r\npython3 openfisca_france/scripts/check_longueur_chemins.py ")
