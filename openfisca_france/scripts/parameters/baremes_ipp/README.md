# Barèmes IPP

## Présentation

IPP = [Institut des politiques publiques](http://www.ipp.eu/en/)

L'IPP produit des fichiers au format XLSX appelés « Barèmes IPP » :
- en anglais : http://www.ipp.eu/en/tools/ipp-tax-and-benefit-tables/
- en français : http://www.ipp.eu/fr/outils/baremes-ipp/

Ces barèmes IPP sont très complets et il est intéressant pour OpenFisca de profiter de leur contenu.

## Conversion XLSX vers XML

OpenFisca définit ses paramètres dans un format XML décrit [ici](https://doc.openfisca.fr/coding-the-legislation/legislation_parameters.html).

L'IPP fournit ses paramètres sous forme de tableurs au format XLSX.

Le script [`convert_ipp_xlsx_to_openfisca_xml.py`](./convert_ipp_xlsx_to_openfisca_xml.py) prend en charge la conversion de XLSX vers XML.

>**Attention, ce script ne semble fonctionner que sous Linux, et pas sous macOS. Voir la [discussion](https://github.com/openfisca/openfisca-france/pull/746#issuecomment-305123915) sur le sujet.**

Ce script nécessite des dépendances supplémentaires. Pour les installer :

```sh
pip install --editable .[baremes_ipp]
```

Il faut également installer `gnumeric` :
- sous Debian : `sudo apt install gnumeric`
- sous macOS : `brew install gnumeric`

Se placer dans le répertoire racine d'OpenFisca-France, là où se trouve le fichier `setup.py` :

```sh
./openfisca_france/scripts/parameters/baremes_ipp/convert_ipp_xlsx_to_openfisca_xml.py --ref-ipp 2c6936d6
```

> L'argument `--ref-ipp` permet de spécifier une version spécifique des [fichiers `XLSX` publiés par l'IPP](https://framagit.org/french-tax-and-benefit-tables/ipp-tax-and-benefit-tables-xlsx/repository/archive.zip) à utiliser.
> La dernière version de ces fichiers compatible avec le script d'import est `2c6936d6`. Pour utiliser les fichiers les plus récents, retirer le paramètre `--ref-ipp`.

Le script génère un nouveau répertoire dans `/tmp` à chaque exécution, dont une partie du nom est aléatoire. Ce répertoire n'est pas effacé par le script. Par exemple :

```
INFO:convert_ipp_xlsx_to_openfisca_xml:XML files written to '/tmp/baremes-ipp-v3SAEz/xml'
```

> Ce processus de conversion de données a été internalisé dans OpenFisca-France à partir de celui de l'IPP disponible [ici](https://framagit.org/french-tax-and-benefit-tables/ipp-tax-and-benefit-tables-converters#in-the-ipp-world).

### Intégration avec OpenFisca

Le script [`merge_ipp_xml_files_with_openfisca_parameters.py`](./merge_ipp_xml_files_with_openfisca_parameters.py) fusionne les fichiers XML produits depuis les fichiers XLSX de l'IPP avec les fichiers XML existants d'OpenFisca-France.

Plus précisément, il réécrit les fichiers de paramètres d'OpenFisca-France en conservant leur structure, tout en remplaçant les valeurs par celles provenant de l'IPP. Le contributeur voit apparaître un *diff* dans *git*, et peut choisir manuellement d'ajouter ou non les lignes modifiées dans un *commit*.

### Gestion des erreurs

En interne le script passe par différentes étapes de conversion : `XLSX -> XLS -> YAML raw -> YAML clean -> XML`.

Les différentes étapes de conversion peuvent générer des erreurs à caractère informatif, non bloquantes. Celles-ci concernent les étapes `XLS -> YAML raw` et `YAML raw -> YAML clean`.

Les erreurs sont stockées au format YAML dans les fichiers `ERRORS.yaml` et `WARNINGS.yaml` contenus dans les sous-répertoires `yaml_raw` et `yaml_clean` du répertoire temporaire global.

Par exemple, certains onglets des fichiers XLSX sont ignorés car ils ne contiennent pas de données mais uniquement du texte explicatif comme un lexique des abbréviations utilisées. Dans ce cas, ceci est indiqué dans le fichier `WARNINGS.yaml`.

### Transformation de l'arbre

Il existe une étape de transformation de l'arbre des paramètres, définie dans le fichier [`transform_ipp_tree.py`](./transform_ipp_tree.py). La fonction, du même nom que le fichier, reçoit en entrée la racine de l'arbre des paramètres construit depuis les fichiers YAML clean de l'IPP, et modifie cet arbre pour correspondre aux noms d'OpenFisca.

Lorsque les fichiers XLSX de l'IPP sont modifiés, il se peut que leur structure change. Dans ce cas, le script plante, très probablement sur une `KeyError` car la fonction `transform_ipp_tree` essaie d'accéder à une clé qui n'existe plus. Ces clés sont équivalentes aux noms des paramètres XML.

Par exemple, la clé `reduction_pour_versement_compte_epargne_codev` correspond au paramètre IPP `Réduction pour versement compte épargne CODEV`. Si le paramètre IPP change de nom, ou si la structure change et qu'il se retrouve à un autre niveau de l'arbre, il faut adapter la fonction `transform_ipp_tree` manuellement. Il n'existe pas de façon automatisée pour retrouver le nom d'un paramètre dans le fichier YAML correspondant à l'une de ces clés.
