"""
Ce script sert à enregistrer les variables pat & sal avant modification
"""
import os
import functools
import re
import json
from pprint import pprint
from openfisca_core.parameters import ParameterNode


def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    Amended from https://code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk/
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1

    for path, dirs, files in os.walk(rootdir):
        if re.search(".ipynb_checkpoints", path):
            pass
        else:
            folders = path[start:].split(os.sep)
            subdir = dict.fromkeys(files)
            parent = functools.reduce(dict.get, folders[:-1], dir)
            parent[folders[-1]] = subdir
    return dir


# PAT 
startpath = "openfisca_france/parameters/cotsoc/pat"
pat_structure = get_directory_structure(startpath)
print(type(pat_structure))
# Dir    
json_file = json.dumps(pat_structure)
with open("pat_structure.json", "w") as outfile:
    outfile.write(json_file)
# Tree    
# pprint(pat_structure)

# SAL 
startpath = "openfisca_france/parameters/cotsoc/sal"
sal_structure = get_directory_structure(startpath)
# Dir
json_file = json.dumps(sal_structure)
with open("sal_structure.json", "w") as outfile:
    outfile.write(json_file)
# Tree    
# pprint(sal_structure)


# Load pat & sal as <class 'openfisca_core.parameters.parameter_node.ParameterNode'>
print(type(pat_structure))
pat = ParameterNode(name="pat", directory_path ="openfisca-france/pat_structure.json", data = pat_structure, file_path = "openfisca-france/")
print(type(pat))
    