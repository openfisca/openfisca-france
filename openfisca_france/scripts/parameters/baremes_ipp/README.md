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

Le script crée un répertoire temporaire, affiche les différentes étapes de la conversion, et termine par une ligne telle que :

```
INFO:convert_ipp_xlsx_to_openfisca_xml:XML files written to '/tmp/baremes-ipp-v3SAEz/xml'
```

En interne le script passe par différentes étapes de conversion : `XLSX -> XLS -> YAML raw -> YAML clean -> XML`.

> Ce processus de conversion de données a été internalisé dans OpenFisca-France à partir de celui de l'IPP disponible [ici](https://framagit.org/french-tax-and-benefit-tables/ipp-tax-and-benefit-tables-converters#in-the-ipp-world).