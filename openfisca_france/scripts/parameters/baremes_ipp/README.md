# Barèmes IPP

## Présentation

IPP = [Institut des politiques publiques](http://www.ipp.eu/en/)

L'IPP produit des fichiers au format XLSX appelés « Barèmes IPP » :
- en anglais : http://www.ipp.eu/en/tools/ipp-tax-and-benefit-tables/
- en français : http://www.ipp.eu/fr/outils/baremes-ipp/

Ces barèmes IPP sont très complets et il est intéressant pour OpenFisca de profiter de leur contenu.

## Conversion XLSX vers XML

OpenFisca définit ses paramètres dans un format XML décrit [ici](https://doc.openfisca.fr/legislation-parameters/index.html).

L'IPP fournit ses paramètres sous forme de tableurs au format XLSX.

Le script [`convert_ipp_xlsx_to_openfisca_xml.py`](./convert_ipp_xlsx_to_openfisca_xml.py) prend en charge la conversion de XLSX vers XML.

Ce script nécessite le paquet [`xlrd`](https://pypi.python.org/pypi/xlrd). Pour l'installer :

```sh
pip install xlrd
# Ou bien utilisez l'extra-require comme ceci : pip install --editable ".[baremes_ipp]"
```

Se placer dans le répertoire racine d'OpenFisca-France, là où se trouve le fichier `setup.py` :

```sh
./openfisca_france/scripts/parameters/baremes_ipp/convert_ipp_xlsx_to_openfisca_xml.py
```

Le script génère un nouveau répertoire temporaire à chaque exécution dont une partie du nom est aléatoire. Il l'affiche en début de script, et ne l'efface pas à la fin. Le script termine en affichant cette ligne, indiquant le nom du répertoire temporaire. Par exemple (la partie `v3SAEz` peut changer) :

```
INFO:convert_ipp_xlsx_to_openfisca_xml:XML files written to '/tmp/baremes-ipp-v3SAEz/xml'
```

> Ce processus de conversion de données a été internalisé dans OpenFisca-France à partir de celui de l'IPP disponible [ici](https://framagit.org/french-tax-and-benefit-tables/ipp-tax-and-benefit-tables-converters#in-the-ipp-world).

### Intégration avec OpenFisca

Il n'existe pas de script automatique de fusion des fichiers XML produits avec les fichiers XML existants – ceux du répertoire `parameters` d'OpenFisca-France. En écrivant les fichiers XML dans `openfisca_france/parameters`, le contributeur voit apparaître un *diff* dans *git*, et peut choisit manuellement d'ajouter ou non les lignes modifiées dans un *commit*.

Pour cela, utiliser l'option `--xml-dir` du script :

```sh
./openfisca_france/scripts/parameters/baremes_ipp/convert_ipp_xlsx_to_openfisca_xml.py --xml-dir openfisca_france/parameters
```

### Gestion des erreurs

En interne le script passe par différentes étapes de conversion : `XLSX -> XLS -> YAML raw -> YAML clean -> XML`.

Les différentes étapes de conversion peuvent générer des erreurs à caractère informatif, non bloquantes. Celles-ci concernent les étapes `XLS -> YAML raw` et `YAML raw -> YAML clean`.

Les erreurs sont stockées au format YAML dans les fichiers `ERRORS.yaml` et `WARNINGS.yaml` contenus dans les sous-répertoires `yaml_raw` et `yaml_clean` du répertoire temporaire global.

Par exemple, certains onglets des fichiers XLSX sont ignorés car ils ne contiennent pas de données mais uniquement du texte explicatif comme un lexique des abbréviations utilisées. Dans ce cas, ceci est indiqué dans le fichier `WARNINGS.yaml`.

### Étape manuelle de transformation

Il existe une étape manuelle de transformation définie dans le fichier [`transform_ipp_tree.py`](./transform_ipp_tree.py) au niveau de la fonction portant le même nom. Cette fonction reçoit en entrée la racine de l'arbre des paramètres construit depuis les fichiers YAML clean de l'IPP, et modifie cet arbre pour correspondre aux noms d'OpenFisca.

Lorsque les fichiers XLSX de l'IPP sont modifiés, il se peut que leur structure change. Dans ce cas la fonction `transform_ipp_tree` doit être adaptée en conséquence.