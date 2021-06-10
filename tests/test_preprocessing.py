import pytest
import yaml
import os

# from openfisca_core import periods, populations, tools
# from openfisca_core.errors import VariableNameConflictError, VariableNotFoundError
# from openfisca_core.simulations import SimulationBuilder
# from openfisca_core.variables import Variable
# from openfisca_core.rates import average_rate, marginal_rate
# from openfisca_france.scenarios import init_single_entity
#from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales.preprocessingV2 import *
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

    # # Load as txt
    # file = open("openfisca_france/scripts/parameters/pat_children_virtual_ESSAI.txt", 'r')
# 
    # # Convert to dict
    # dictionary = {}
    # with open("openfisca_france/scripts/parameters/pat_children_virtual_ESSAI.txt", 'r') as file:
    #     for line in file:
    #         key, value = line.strip().split(",")
    #         dictionary[key] = value
    # print(dictionary)
    # pat_avant = my_dictionnary

    # Load as json
    #import json
    #with open("openfisca_france/scripts/parameters/pat_children_virtual_ESSAI.json", "w") as json_file:
    #    pat_avant = json.load(json_file)
#
    pat_avant = open ("openfisca_france/scripts/parameters/pat_children_virtual_AVANT.txt", 'r')
    print(type(pat_avant))
    
    # Output of preprocessingV2
    print( build_pat(node_json).children , file=open("openfisca_france/scripts/parameters/pat_children_virtual_with_V2.txt", "a"))
    pat_apres = open ("openfisca_france/scripts/parameters/pat_children_virtual_with_V2.txt", 'r')
    print('👹', type(pat_apres))

    #assert 1 == 10
    #assert type(pat_avant) == type(pat_apres)
    assert pat_avant == pat_apres

# def test_full_build_sal():
# def test_preprocess_parameters()

# def test_arbres_avant_preprocessing:
# with open('openfisca_france/scripts/parameters/pat_children_reel_avant_processing.yaml', 'r') as file:
#         pat_avant = yaml.safe_load(file)
#     print(type(pat_avant))