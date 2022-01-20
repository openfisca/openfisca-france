# Publication vers Anaconda

Ce readme décrit la partie publication vers conda, pour utiliser le paquet conda résultant, voir [le readme principal](https://github.com/openfisca/openfisca-france/tree/publish-to-conda#installez-un-environnement-virtuel-avec-conda).

Pour envoyer un paquet vers conda il faut obligatoirement un fichier `meta.yaml` qui décrit le package.

Nous avons fait le choix d'utiliser la paquet PyPi comme source du paquet Conda, pour s'assurer que l'on publie bien la même chose sur les deux plateformes.

L'upload automatique est fait de la façon suivante par la CI uniquement si l'étape de livraison sur PyPi c'est bien déroulée :
- Miniconda est installé.
- Le script `.github/get_pypi_info.py` récupére les informations du package sur PyPi et les place dans le fichier `.conda/meta.yaml`.
- `conda build` est exécuter pour construire et publier le paquet conformément au fichier `.conda/meta.yaml`. Cette étape nécessite la variable de CI ANACONDA_TOKEN.

Pour valider que tout a fonctionné, une étape `test-on-windows` a été ajouté en fin de CI. Cette étape récupère le paquet conda sur une machine Windows et exécute les tests.

## Etapes préparatoires pour arriver à cette automatisation

- Création d'un compte sur https://anaconda.org
- Création d'un token sur https://anaconda.org/openfisca.org/settings/access avec le droit "Allow write access to the API site". Attention il expire le 2023/01/13
- Mis en place du token dans GitHub Action sous le nom de variable ANACONDA_TOKEN

### Publication manuelle du package

Les étapes suivantes peuvent être réalisées sous Windows pour tester la publication :

_Cela fonctionne aussi sous macOS et Linux, à condition d'adapter les chemins._

- Editer `.conda/meta.yaml` pour vérifier son contenu.
- Installer [MiniConda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) si vous n'avez pas déjà [AnaConda](https://www.anaconda.com/products/individual).
- Puis dans le terminal saisissez les instructions suivantes : 
    - `conda install -c anaconda conda-build anaconda-client`
    - `conda build --croot c:\temp .conda` L'option `--croot ` est nécessaire sous Windows à cause des chemins trop long.
    - `conda install -c anaconda anaconda-client` Pour installer l'outil en ligne de commande.
    - `anaconda login`
    - `anaconda upload c:\temp\noarch\openfisca-france-<VERSION>-py_0.tar.bz2`
