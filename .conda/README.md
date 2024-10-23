# Publication vers Anaconda

Ce readme décrit la partie publication vers conda, pour utiliser le paquet conda résultant, voir [le readme principal](https://github.com/openfisca/openfisca-france/tree/publish-to-conda#installez-un-environnement-virtuel-avec-conda).

Pour envoyer un paquet vers conda il faut obligatoirement un fichier `meta.yaml` qui décrit le package.

Nous avons fait le choix d'utiliser le paquet PyPi comme source du paquet Conda, pour s'assurer que l'on publie bien la même chose sur les deux plateformes.

L'upload automatique est fait de la façon suivante par la CI uniquement si l'étape de livraison sur PyPi s'est bien déroulée :
- Installation de Miniconda.
- Récupération par le script `.github/get_pypi_info.py` des informations du package sur PyPi.
- Ecriture de ces informations par ce même script dans le fichier `.conda/meta.yaml`.
- Exécution de `conda build` pour construire et publier le paquet conformément au fichier `.conda/meta.yaml`. Cette étape nécessite la variable de CI ANACONDA_TOKEN.

Pour valider que tout a fonctionné, une étape `test-on-windows` a été ajoutée en fin de CI. Cette étape récupère le paquet conda sur une machine Windows et exécute les tests.

**A noter** : Le paquet OpenFisca-France est aussi publié sur `conda-forge`, pour cela voir [le feedstock](https://github.com/openfisca/openfisca-france-feedstock/tree/master/recipe) et la [ci automatique](https://github.com/conda-forge/openfisca-france-feedstock).

C'est le channel `conda-forge` qui est normalement le channel stable à conseiller aux utilisateurs, mais il souffre d'un net retard de mise à jour. Le channel `openfisca` reçoit les derniers paquets de façon automatique.

## Tester le build en local

Pour utiliser les mêmes commandes que la CI, il faut installer `pixi` et `rattler-build` si vous ne l'avez pas déjà :

```sh
curl -fsSL https://pixi.sh/install.sh | bash
source $HOME/.bashrc
pixi global install rattler-build
```

Pour tester le build en local, il suffit de lancer la commande suivante :

```sh
rattler-build build --channel openfisca --channel conda-forge --recipe .conda --output-dir /tmp/rattler
```

Pour tester l'installation du paquet envoyé sur [anaconda](https://anaconda.org/openfisca/openfisca-france) :

```sh
docker run --volume $PWD:/openfisca -i -t continuumio/anaconda3 /bin/bash
cd /openfisca
conda install -c openfisca -c conda-forge openfisca-france
openfisca test --country-package openfisca_france tests
```

## Etapes préparatoires pour arriver à cette automatisation

- Création d'un compte sur https://anaconda.org.
- Création d'un token sur https://anaconda.org/openfisca/settings/access avec le droit _Allow write access to the API site_. Attention il expire le 2023/01/13.

- Mis en place du token dans GitHub Action sous le nom de variable ANACONDA_TOKEN.

### Publication manuelle du package

Les étapes suivantes peuvent être réalisées sous Windows pour tester la publication :

_Cela fonctionne aussi sous macOS et Linux, à condition d'adapter les chemins._

- Editer `.conda/meta.yaml` pour vérifier son contenu.
- Installer [MiniConda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html) si vous n'avez pas déjà [AnaConda](https://www.anaconda.com/products/individual).
- Puis dans le terminal saisissez les instructions suivantes :
    - `conda install -c anaconda conda-build anaconda-client` Pour installer les outils indispensable.
    - `conda build --croot c:\temp .conda` L'option `--croot ` est nécessaire sous Windows à cause des chemins trop long.
    - `conda install -c anaconda anaconda-client` Pour installer l'outil en ligne de commande.
    - `anaconda login` Pour vous connecter avec le compte _openfisca_, voir le Keepass OpenFisca.
    - `anaconda upload c:\temp\noarch\openfisca-france-<VERSION>-py_0.tar.bz2` pour publier le package.
- Vérifier que tout c'est bien passé sur https://anaconda.org/search?q=openfisca.
