Origin of zones_apl_2013.csv
============================

Downloads
---------

* [Liste des communes existantes au 1er janvier 2014](http://www.insee.fr/fr/methodes/nomenclatures/cog/telechargement.asp) (TXT in a ZIP)
* [Éléments de calcul des aides personnelles au logement](http://www.territoires.gouv.fr/spip.php?page=pdfjs&id_document=1309) (PDF)

Steps
-----

* `unzip comsimp2014.zip; rm comsimp2014.zip`
* `pdftotext -f 93 -nopgbrk MEDDAT_Plaq_logement_2013_bd.pdf classement_communes_2013.txt`
* produce `zone_1_2013.txt` and `zone_2_2013.txt` from `classement_communes_2013.txt` by hand (sad, but we're waiting for raw data files)
* run script `./classement_communes_to_zones_apl.py --comsimp comsimp2014.txt --zone-1 zone_1_2013.txt --zone-2 zone_2_2013.txt > zones_apl_2013.json`
  The JSON file contains "Code INSEE (depcom)" and not commune names.

Notes
-----

* consider all communes of département 75 are in zone 1
* ignore the sentence "En métropole, toutes les îles non reliées par voie routière" for zone 2
* treat cantons : 60 Toutes les communes des cantons de Chantilly, Creil, Nogent-sur-Oise, Creil-Sud, Montataire, Nanteuil-leHaudoin, Neuilly-en-Thelle, Pont-Sainte-Maxence, Senlis.
* treat "Reste du département ne figurant pas en zone I."
* ensemble urbain du Vaudreuil
