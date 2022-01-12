## Prérequis

Installation de [Conda](https://www.anaconda.com/products/individual)

## Installation

`conda install -c openfisca.org openfisca-france`

## Mise à jour du paquet sur Conda

Pour créer un nouveau paquet il faut faire les actions suivantes à la racine du projet:

- Editer `.conda/meta.yaml` pour mettre à jour:
    - Le numéro de version
    - Le hash 256
    - L'url du paquet sur PyPi si nécessaire
- `conda build --croot d:\tmp   .conda` L'option `--croot ` est nécessaire sous Windows à cause des chemins trop long.
- `conda install -c anaconda anaconda-client` Pour installer l'outil en ligne de commande.
- `anaconda login`
- `anaconda upload d:\tmp\noarch\openfisca-france-102.0.0-py_0.tar.bz2`
