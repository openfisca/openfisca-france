import pytest
import yaml
import os
import time
import difflib


from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.preprocessing import *
from openfisca_core.parameters import ParameterNode
from openfisca_france.france_taxbenefitsystem import COUNTRY_DIR

"""
Etapes du réel au résultat du preprocessing

Step 1 - Fichiers Yaml de parametres dans parameters.cotsoc.... définis dans directory_path

Step 2 - On charge le france_taxbenefitsystem (d'openfisca-france) qui appelle load_parameters (d'openfisca-core)
Step 2.1 - load_parameters (d'openfisca-core) appelle le preprocessing (d'openfisca-france)
Entree (de load_parameters): param_dir
Sortie (de load_parameters): instanciation de l'attribut taxbenefitsystem.parameters (avec le preprocessing)
type(taxbenefitsystem.parameters) == ParameterNode

"""


@pytest.fixture
def node_json():
    param_dir = os.path.join(COUNTRY_DIR, 'parameters')
    return ParameterNode('', directory_path = param_dir)


def test_full_build_pat(node_json):
    # Original preprocessing
    path_avant = "openfisca_france/scripts/parameters/pat_children_AVANT.txt"
    pat_avant = []
    with open(path_avant) as avant_file :
        for line in avant_file :
            pat_avant.append(line)
    
    # Output of preprocessingV2
    path_apres = 'openfisca_france/scripts/parameters/pat_children_APRES.txt'
    print( build_pat(node_json).children , file=open(path_apres, "w"))
    pat_apres = []
    with open(path_apres) as apres_file :
        for line in apres_file :
            pat_apres.append(line)

    # If the files are different
    if pat_avant != pat_apres :
        with open(path_avant, 'rU') as f1:
            with open(path_apres, 'rU') as f2:
                readable_last_modified_time1 = time.ctime(os.path.getmtime(path_avant)) # not required
                readable_last_modified_time2 = time.ctime(os.path.getmtime(path_apres)) # not required
                # Save the diff in a file
                difftext = ''.join(difflib.unified_diff(
                f1.readlines(), f2.readlines(), fromfile=path_avant, tofile=path_apres, 
                fromfiledate=readable_last_modified_time1, # not required
                tofiledate=readable_last_modified_time2, # not required
                ))
                with open('openfisca_france/scripts/parameters/pat_diff.txt', 'w') as diff_file:
                    diff_file.write(difftext)

    assert pat_avant == pat_apres


def test_full_build_sal(node_json):
    # Original preprocessing
    path_avant = "openfisca_france/scripts/parameters/sal_children_AVANT.txt"
    sal_avant = []
    with open(path_avant) as avant_file :
        for line in avant_file :
            sal_avant.append(line)
    
    # Output of preprocessingV2
    path_apres = 'openfisca_france/scripts/parameters/sal_children_APRES.txt'
    print( build_sal(node_json).children , file=open(path_apres, "w"))
    sal_apres = []
    with open(path_apres) as apres_file :
        for line in apres_file :
            sal_apres.append(line)

    # If the files are different
    if sal_avant != sal_apres :
        with open(path_avant, 'rU') as f1:
            with open(path_apres, 'rU') as f2:
                readable_last_modified_time1 = time.ctime(os.path.getmtime(path_avant)) # not required
                readable_last_modified_time2 = time.ctime(os.path.getmtime(path_apres)) # not required
                # Save the diff in a file
                difftext = ''.join(difflib.unified_diff(
                f1.readlines(), f2.readlines(), fromfile=path_avant, tofile=path_apres, 
                fromfiledate=readable_last_modified_time1, # not required
                tofiledate=readable_last_modified_time2, # not required
                ))
                with open('openfisca_france/scripts/parameters/sal_diff.txt', 'w') as diff_file:
                    diff_file.write(difftext)

    assert sal_avant == sal_apres
    

def test_preprocess_parameters(node_json):
# Original preprocessing
    path_avant = "openfisca_france/scripts/parameters/preprocessed_parameters_AVANT.txt"
    PP_avant = []
    with open(path_avant) as avant_file :
        for line in avant_file :
            PP_avant.append(line)
    
    # Output of preprocessingV2
    path_apres = 'openfisca_france/scripts/parameters/preprocessed_parameters_APRES.txt'
    print( preprocess_parameters(node_json), file=open(path_apres, "w"))
    PP_apres = []
    with open(path_apres) as apres_file :
        for line in apres_file :
            PP_apres.append(line)

    # If the files are different
    if PP_avant != PP_apres :
        with open(path_avant, 'rU') as f1:
            with open(path_apres, 'rU') as f2:
                readable_last_modified_time1 = time.ctime(os.path.getmtime(path_avant)) # not required
                readable_last_modified_time2 = time.ctime(os.path.getmtime(path_apres)) # not required
                # Save the diff in a file
                difftext = ''.join(difflib.unified_diff(
                f1.readlines(), f2.readlines(), fromfile=path_avant, tofile=path_apres, 
                fromfiledate=readable_last_modified_time1, # not required
                tofiledate=readable_last_modified_time2, # not required
                ))
                with open('openfisca_france/scripts/parameters/preprocessed_parameters_diff.txt', 'w') as diff_file:
                    diff_file.write(difftext)

    assert PP_avant == PP_apres