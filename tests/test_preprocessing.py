import pytest
import os


from openfisca_france.model.prelevements_obligatoires.prelevements_sociaux.cotisations_sociales import preprocessing, preprocessing_old
from openfisca_core.parameters import ParameterNode
from openfisca_france.france_taxbenefitsystem import COUNTRY_DIR
from openfisca_france.scripts.parameters.check_keys import check_keys, check_keys2

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
    pat = preprocessing_old.build_pat(node_json)
    path_avant = "openfisca_france/scripts/parameters/pat_children_AVANT_old.txt"
    # print(preprocessing_old.build_pat(node_json).children, file=open(path_avant, "w"))  # noqa: T001
    # Output of preprocessingV2
    path_apres = 'openfisca_france/scripts/parameters/pat_children_APRES.txt'
    print(preprocessing.build_pat(node_json).children, file=open(path_apres, "w"))  # noqa: T001

    missing, en_trop = check_keys(path_avant, path_apres)

    assert missing == []
    assert en_trop == []


def test_full_build_sal(node_json):
    # Original preprocessing
    sal = preprocessing_old.build_sal(node_json)
    path_avant = "openfisca_france/scripts/parameters/sal_children_AVANT_old.txt"
    # print(preprocessing_old.build_sal(node_json).children, file=open(path_avant, "w"))  # noqa: T001
    # Output of preprocessingV2
    path_apres = 'openfisca_france/scripts/parameters/sal_children_APRES.txt'
    print(preprocessing.build_sal(node_json).children, file=open(path_apres, "w"))  # noqa: T001

    missing, en_trop = check_keys(path_avant, path_apres)
    assert missing == []
    assert en_trop == []


def test_preprocess_parameters(node_json):
    # Original preprocessing
    #preprocessing_old.preprocess_parameters(node_json) #Ne marche plus une fois qu'on a supprimé PAT et SAL
    path_avant = "openfisca_france/scripts/parameters/preprocessed_parameters_AVANT_old.txt"
    #print(preprocessing_old.preprocess_parameters(node_json).cotsoc, file=open(path_avant, "w"))  # noqa: T001

    # Output of preprocessingV2
    path_apres = 'openfisca_france/scripts/parameters/preprocessed_parameters_APRES.txt'
    print(preprocessing.preprocess_parameters(node_json).cotsoc, file=open(path_apres, "w"))  # noqa: T001

    missing, en_trop = check_keys2(path_avant, path_apres)
    assert missing == []
    assert en_trop == []
