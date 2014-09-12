`20110914_zonage.csv` comes from an XML file sent to Etalab.
This file will be released on http://data.gouv.fr/ soon.

"Arrondissements" and "communes associées" (subcommunes) are not in `20110914_zonage.csv`.
Using the file
"Liste des communes de la métropole et DOM (toutes les communes ayant existé depuis 1943)" `france2014.txt`
available on http://www.insee.fr/fr/methodes/nomenclatures/cog/telechargement.asp
and the script `extract_arrondissements_and_communes_associees.py`, we associate subcommues depcom codes to communes
depcom code :
```
python extract_subcommunes.py france2014.txt > commune_depcom_by_subcommune_depcom.json
```
