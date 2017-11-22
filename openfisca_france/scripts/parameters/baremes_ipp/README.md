# Barèmes IPP

## Présentation

IPP = [Institut des politiques publiques](http://www.ipp.eu/en/)

L'IPP produit des fichiers au format XLSX appelés « Barèmes IPP » :
- en anglais : http://www.ipp.eu/en/tools/ipp-tax-and-benefit-tables/
- en français : http://www.ipp.eu/fr/outils/baremes-ipp/

Ces barèmes IPP sont très complets et il est intéressant pour OpenFisca de profiter de leur contenu.

Les scripts décrits ici permettent d'importer les barèmes IPP (fournis sous forme de tableurs au format XLSX) dans [les fichiers de paramètres](http://openfisca.org/doc/coding-the-legislation/legislation_parameters.html) d'OpenFisca France, au [format XML](https://github.com/openfisca/openfisca-france/tree/master/openfisca_france/parameters).

## Imports des barèmes IPP dans OpenFisca

### En local

>**Attention, ce script ne semble fonctionner que sous Linux, et pas sous macOS. Voir la [discussion](https://github.com/openfisca/openfisca-france/pull/746#issuecomment-305123915) sur le sujet.**  
> **Si vous avez accès au serveur OpenFisca-France, vous pouvez [executer le script sur ce-dernier](#sur-le-serveur-openfisca)**

#### Installation

L'import nécessite des dépendances supplémentaires. Pour les installer :

```sh
pip install --editable ".[baremes_ipp]"
```

Il faut également installer `gnumeric` :
- sous Debian : `sudo apt install gnumeric`

> L'import a été testé sour `gnumeric` `1.12.18`

#### Utilisation

Se placer dans le répertoire racine d'OpenFisca-France, là où se trouve le fichier `setup.py` et exécuter:

```sh
./openfisca_france/scripts/parameters/baremes_ipp/convert_ipp_xlsx_to_openfisca_xml.py --ref-ipp 2c6936d6 --merge
```

> L'argument `--ref-ipp` est une référence git qui permet de spécifier une version spécifique des [fichiers `XLSX` publiés par l'IPP](https://git.framasoft.org/french-tax-and-benefit-tables/ipp-tax-and-benefit-tables-xlsx) à utiliser.
> La dernière version de ces fichiers compatible avec le script d'import est `2c6936d6`. Pour utiliser les fichiers les plus récents, retirer le paramètre `--ref-ipp`.

Une fois le script exécuté, le contributeur voit apparaître un *diff* dans *git*, et peut choisir manuellement d'ajouter ou non les lignes modifiées dans un *commit*.

### Sur le serveur OpenFisca

> **Vous devez avoir les droits d'accès en `ssh` au serveur `openfisca.fr` pour pouvoir exécuter l'import en suivant cette procédure**

Se connecter au serveur OpenFisca :

```sh
ssh baremes-ipp@openfisca.fr -A
```

Puis exécuter les commandes suivantes :

```sh
cd openfisca-france
BRANCH_NAME=update-baremes-ipp-`date +'%Y-%m-%d-%H-%M'`
git checkout -b $BRANCH_NAME
./openfisca_france/scripts/parameters/baremes_ipp/convert_ipp_xlsx_to_openfisca_xml.py --ref-ipp 2c6936d6 --merge
git commit --all -m "Update baremes IPP"
git push origin $BRANCH_NAME
git checkout master
```

> L'argument `--ref-ipp` permet de spécifier une version spécifique des [fichiers `XLSX` publiés par l'IPP](https://framagit.org/french-tax-and-benefit-tables/ipp-tax-and-benefit-tables-xlsx/repository/archive.zip) à utiliser.
> La dernière version de ces fichiers compatible avec le script d'import est `2c6936d6`. Pour utiliser les fichiers les plus récents, retirer le paramètre `--ref-ipp`.

Une fois le script exécuté, une branche `update-baremes-ipp-YYYY-MM-DD-HH-MM` est publiée sur ce dépôt.

>Exemple :  `update-baremes-ipp-2017-06-14-15-30` si le script est exécuté le 14 juin 2017 à 15h30

 Le contributeur peut alors éditer le code sur cette branche, et ouvrir une pull request.

## Étapes de la transformation

### Conversion XLSX vers XML

Le script [`convert_ipp_xlsx_to_openfisca_xml.py`](./convert_ipp_xlsx_to_openfisca_xml.py) prend en charge la conversion de XLSX vers XML.

Ce script génère un nouveau répertoire dans `/tmp` à chaque exécution, dont une partie du nom est aléatoire.

Le nom du répertoire où sont créés les fichiers `XML` issus de la conversion est visible dans les logs du script. Par exemple :

```
INFO:convert_ipp_xlsx_to_openfisca_xml:XML files written to '/tmp/baremes-ipp-v3SAEz/xml'
```

> Ce processus de conversion de données a été internalisé dans OpenFisca-France à partir de celui de l'IPP disponible [ici](https://framagit.org/french-tax-and-benefit-tables/ipp-tax-and-benefit-tables-converters#in-the-ipp-world).

### Fusion avec les paramètres OpenFisca

Le script [`merge_ipp_xml_files_with_openfisca_parameters.py`](./merge_ipp_xml_files_with_openfisca_parameters.py) fusionne les fichiers XML produits depuis les fichiers XLSX de l'IPP avec les fichiers XML existants d'OpenFisca-France :

>Exemple : si le dossier temporaire qui contient les `XML` produits par le script de conversion précédent est `/tmp/baremes-ipp-v3SAEz/xml`, exécuter :
>
>```sh
>./openfisca_france/scripts/parameters/baremes_ipp/merge_ipp_xml_files_with_openfisca_parameters.py /tmp/baremes-ipp-v3SAEz/xml 
>```

Plus précisément, il réécrit les fichiers de paramètres d'OpenFisca-France en conservant leur structure, tout en remplaçant les valeurs par celles provenant de l'IPP. 

### Gestion des erreurs

En interne le script passe par différentes étapes de conversion : `XLSX -> XLS -> YAML raw -> YAML clean -> XML`.

Les différentes étapes de conversion peuvent générer des erreurs à caractère informatif, non bloquantes. Celles-ci concernent les étapes `XLS -> YAML raw` et `YAML raw -> YAML clean`.

Les erreurs sont stockées au format YAML dans les fichiers `ERRORS.yaml` et `WARNINGS.yaml` contenus dans les sous-répertoires `yaml_raw` et `yaml_clean` du répertoire temporaire global.

Par exemple, certains onglets des fichiers XLSX sont ignorés car ils ne contiennent pas de données mais uniquement du texte explicatif comme un lexique des abbréviations utilisées. Dans ce cas, ceci est indiqué dans le fichier `WARNINGS.yaml`.

### Transformation de l'arbre

Il existe une étape de transformation de l'arbre des paramètres, définie dans le fichier [`transform_ipp_tree.py`](./transform_ipp_tree.py). La fonction, du même nom que le fichier, reçoit en entrée la racine de l'arbre des paramètres construit depuis les fichiers YAML clean de l'IPP, et modifie cet arbre pour correspondre aux noms d'OpenFisca.

Lorsque les fichiers XLSX de l'IPP sont modifiés, il se peut que leur structure change. Dans ce cas, le script plante, très probablement sur une `KeyError` car la fonction `transform_ipp_tree` essaie d'accéder à une clé qui n'existe plus. Ces clés sont équivalentes aux noms des paramètres XML.

Par exemple, la clé `reduction_pour_versement_compte_epargne_codev` correspond au paramètre IPP `Réduction pour versement compte épargne CODEV`. Si le paramètre IPP change de nom, ou si la structure change et qu'il se retrouve à un autre niveau de l'arbre, il faut adapter la fonction `transform_ipp_tree` manuellement. Il n'existe pas de façon automatisée pour retrouver le nom d'un paramètre dans le fichier YAML correspondant à l'une de ces clés.
