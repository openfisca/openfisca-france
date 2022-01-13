## Prérequis

Installation de [Conda](https://www.anaconda.com/products/individual)

## Mise à jour du paquet sur Conda

Pour créer un nouveau paquet il faut faire les actions suivantes à la racine du projet:

- Editer `.conda/meta.yaml` pour mettre à jour:
    - Le numéro de version
    - Le hash 256
    - L'url du paquet sur PyPi si nécessaire
    - Ces informations sont données par le script `.github/get_pypi_info.py`

### Upload manuel du package

- `conda build --croot d:\tmp   .conda` L'option `--croot ` est nécessaire sous Windows à cause des chemins trop long.
- `conda install -c anaconda anaconda-client` Pour installer l'outil en ligne de commande.
- `anaconda login`
- `anaconda upload d:\tmp\noarch\openfisca-france-102.0.0-py_0.tar.bz2`

### Upload automatique du package

L'upload automatique est fait par la CI, mais il faut que le fichier meta.yaml soit conforme.

## Procédure initiale

- Création d'un compte
- Création d'un token sur https://anaconda.org/openfisca.org/settings/access avec le droit "Allow write access to the API site". Attention il expire le 2023/01/13
- Mis en place du token dans GitHub action sous le nom de variable ANACONDA_TOKEN
- Mise en place
