"""
Ce script sert à enregistrer les variables pat & sal avant modification
"""
import os
import functools
import re
import yaml # import json
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


# Create PAT dict 
startpath = "openfisca_france/parameters/cotsoc/pat"
pat_structure = get_directory_structure(startpath)
# print(type(pat_structure))
# Dir Yaml
f = open('pat_structure.yaml', 'w+')
yaml.dump(pat_structure, f, allow_unicode=True)
# Tree    
# pprint(pat_structure)

# Create SAL dict 
startpath = "openfisca_france/parameters/cotsoc/sal"
sal_structure = get_directory_structure(startpath)
# Dir
f = open('sal_structure.yaml', 'w+')
yaml.dump(sal_structure, f, allow_unicode=True)
# yaml.dump(sal_structure, f, allow_unicode=True, default_flow_style=False)
# Tree    
# pprint(sal_structure)


# Load pat & sal as a: <class 'openfisca_core.parameters.parameter_node.ParameterNode'>
print(type(pat_structure))
cwd = os.getcwd()
print(cwd)

pat = ParameterNode(name="pat", directory_path = "/", file_path = "pat_structure.yaml")
print(type(pat))
