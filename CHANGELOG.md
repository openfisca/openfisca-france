# Changelog

### 18.11.1

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2016.
* Zones impactées : `/prestations/ppa`.
* Détails :
  - Améliore l'implémentation de la prime d'activité en utilisant le bon montant forfaitaire

## 18.11.0

* Amélioration technique
* Détails :
  - Rends OpenFisca-France comptabible avec OpenFisca-Core 20
    - Change la manière de déclarer les variables
    - Voir [changelog de Core](https://github.com/openfisca/openfisca-core/pull/590)

### 18.10.2

* Amélioration technique
* Détails :
  - Déclare OpenFisca-France compatible avec OpenFisca-Core 19

### 18.10.1

* Amélioration technique
* Détails :
  - Déclare OpenFisca-France compatible avec OpenFisca-Core 18

## 18.10.0

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `/prestations/apa`.
* Détails :
  - Implémente l'Allocation Personnalisée d'Autonomie.

### 18.9.10 - [#829](https://github.com/openfisca/openfisca-france/pull/829)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `/prestations/aides_logement`.
* Détails :
  - Corrige les aides au logement pour les primo-accédants ayant une importante base ressources.

### 18.9.9 - [#803](https://github.com/openfisca/openfisca-france/pull/803)

* Changement mineur
* Détails :
  - Simplifie le calcul des aides au logement en utilisant le calcul de législation dynamique (nouvelle feature de OpenFisca)

### 18.9.8 - [#825](https://github.com/openfisca/openfisca-france/pull/825)

* Correction d'un crash sous Windows
* Détails :
  - Corrige l'erreur WindowsError: `[Error 206] Nom de fichier ou extension trop long` qui interrompt le clone d'OpenFisca-France sous Windows.
  - Dans `parameters`, assemble dans un nouveau YAML le contenu d'un sous-répertoire lorsque le chemin vers celui-ci ou l'un de ses fichiers est trop long.

### 18.9.7 - [#811](https://github.com/openfisca/openfisca-france/pull/811)

* Changement mineur
* Détails :
  - Documente les entités `FoyerFiscal` et `Menage`

### 18.9.6 - [#815](https://github.com/openfisca/openfisca-france/pull/815)

* Changement mineur
* Détails :
  - Corrige une typo dans la description de `credit_impot_competitivite_emploi`

### 18.9.5 - [#814](https://github.com/openfisca/openfisca-france/pull/814)

* Changement mineur
* Détails :
  - Rajout des références législatives sur la baisse de la cotisation AGS au 1er juillet 2017.

### 18.9.4 - [#809](https://github.com/openfisca/openfisca-france/pull/809)

* Changement mineur.
* Détails :
  - Référence la nouvelle adresse de la documentation technique

### 18.9.3 - [#817](https://github.com/openfisca/openfisca-france/pull/817)

* Changement mineur.
* Périodes concernées : à partir du 07/05/2017.
* Zones impactées : `parameters/bourses_education/bourse_college`.
* Détails :
  - Mise à jour des montant des bourses des collèges conformément au [décret du 5 mai 2017](https://www.legifrance.gouv.fr/eli/decret/2017/5/5/MENE1711101D/jo/texte).

### 18.9.2 - [#812](https://github.com/openfisca/openfisca-france/pull/812)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `/prestations/aides_logement`.
* Détails :
  - Suppresion de la notification de non-calculabilité des aides au logement pour les primo-accédants.

### 18.9.1 - [#583](https://github.com/openfisca/openfisca-france/pull/583)

* Changement mineur.
* Périodes concernées : à partir du 01/11/2014.
* Zones impactées : `prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/stage`.
* Détails :
  - Extraction du taux de gratification minimum des stagiaires vers le fichier de paramètres.

## 18.9.0 - [#798](https://github.com/openfisca/openfisca-france/pull/798)

* Amélioration technique
* Détails :
  - Migration vers la version 17 d'OpenFisca-Core.
  - Transformation des paramètres depuis XML vers YAML.
  - Ajout d'un sous-répertoire `migrations` dans le répertoire `scripts`.

### 18.8.2 - [#806](https://github.com/openfisca/openfisca-france/pull/788)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/07/2017
* Zones impactées : `prelevements_obligatoires/prelevements_sociaux/contributions_sociales/versement_transport`.
* Détails :
  - Mise à jour conformément à [la circulaire du 31 mai](https://www.urssaf.fr/portail/files/live/sites/urssaf/files/Lettres_circulaires/2017/ref_LCIRC-2017-0000019.pdf)
  - données extraites via l'API de l'URSSAF, cf. https://github.com/sgmap/taux-versement-transport

## 18.8.1 - [#789](https://github.com/openfisca/openfisca-france/pull/789)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/07/2017
* Zones impactées : `openfisca_france/parameters/cotsoc.xml`, `openfisca_france/parameters/prelevements_sociaux.xml`.
* Détails :
  - Prise en compte de la baisse de la cotisation AGS au 1er juillet.

## 18.8.0 - [#801](https://github.com/openfisca/openfisca-france/pull/801)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `/prestations/aides_logement`.
* Détails :
  - Calcul des aides au logement pour les primo-accédants.
  - Marge d'erreur (~5% sur les tests) voir avec un expert métier pour rectifier le calcul.

## 18.7.0 - [#797](https://github.com/openfisca/openfisca-france/pull/797)

* Amélioration technique
* Détails :
  - Déclare OpenFisca-France compatible avec OpenFisca-Core 16

### 18.6.6 - [#781](https://github.com/openfisca/openfisca-france/pull/781)

* Changement mineur.
* Détails :
  - Mise à jour du `label` de `age` pour expliciter qu'il s'agit de l'âge en début de mois

### 18.6.5 - [#785](https://github.com/openfisca/openfisca-france/pull/785)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/04/2017.
* Zones impactées :
  - `prestations/minima_sociaux/cmu`
  - `prestations/minima_sociaux/aah`
* Détails :
  - Mise à jour du plafond de ressources pour la CMU
    - [Cf. Code de la sécurité sociale - Article D861-1](https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000006739670)
  - Mise à jour du montant de l'AAH et de son complément de ressources
    - [Montant de l'AAH au 1er avril 2017](https://www.legifrance.gouv.fr/eli/decret/2017/5/3/AFSA1710706D/jo/texte)
    - Le montant de la garantie de revenus est calculé à partir du montant précédent, plus un montant fixe défini dans [cet article](https://www.legifrance.gouv.fr/affichCodeArticle.do?cidTexte=LEGITEXT000006073189&idArticle=LEGIARTI000019505277)
    - [Circulaire indiquant le coefficient de revalorisation](http://circulaire.legifrance.gouv.fr/pdf/2017/03/cir_41966.pdf)

### 18.6.4 - [#784](https://github.com/openfisca/openfisca-france/pull/784)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2017
* Zones impactées : `prestations/minima_sociaux/ass`.
* Détails :
  - Implémentation de la non-éligibilité à l'ASS (Allocation de Solidarité Spécifique) en cas d'éligibilité à l'AAH (Allocation aux Adultes Handicapés)
    - [article 87 loi n° 2016-1917 du 29 décembre 2016 de finances pour 2017](https://www.legifrance.gouv.fr/affichTexteArticle.do;jsessionid=49AD9A92D43F6C7A085F8E1D669AEFC2.tpdila18v_2?cidTexte=JORFTEXT000033734169&idArticle=LEGIARTI000033760616&dateTexte=20170622&categorieLien=id#LEGIARTI000033760616)
    - [article L. 5423-7 du code du travail](https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=49AD9A92D43F6C7A085F8E1D669AEFC2.tpdila18v_2?idArticle=LEGIARTI000033813814&cidTexte=LEGITEXT000006072050&dateTexte=20170622)

### 18.6.3 - [#787](https://github.com/openfisca/openfisca-france/pull/787)

* Amélioration technique
* Détails :
  - Migre les formules situés dans les fichiers suivant vers la syntaxe introduite par OpenFisca-Core 4 :
    - `prelevements_obligatoires/impot_revenu/credits_impot.py`
    - `prelevements_obligatoires/impot_revenu/ir.py`
    - `prelevements_obligatoires/isf.py`
    - `prelevements_obligatoires/taxe_habitation.py`
    - `reforms/landais_piketty_saez.py`

### 18.6.2 - [#794](https://github.com/openfisca/openfisca-france/pull/794)

* Correction d'un crash
+ Détails :
  - Mets à jour la version d'OpenFisca-Web-API requise pour qu'elle soit compatible avec la version d'OpenFisca-Core requise.
  - Les deux versions référencées dans le `setup.py` étaient incompatibles, provoquant une erreur au démarrage de l'API avec `gunicorn` ou `paster`.

### 18.6.1 - [#793](https://github.com/openfisca/openfisca-france/pull/793)

* Changement mineur
* Détails :
  - Répare la déclaration de l'URL du dépôt, endomagée dans la version `18.6.0`

## 18.6.0 - [#775](https://github.com/openfisca/openfisca-france/pull/775)

* Amélioration technique
* Détails :
  - Adapte `france` à  la version `15.0.0` de `core`.
  - Applique le renommage de l'attribut de `Variable` `url` en `reference`.
  - Pour les variables réformées, ne définis plus l'attribut `reference`.

### 18.5.3 - [#786](https://github.com/openfisca/openfisca-france/pull/786)

* Changement mineur
* Détails
  - Répare la réforme `de_net_a_brut`.

### 18.5.2 - [#778](https://github.com/openfisca/openfisca-france/pull/778)

* Amélioration technique
* Détails :
  - Ajoute un script de reformatage des fichiers de paramètres XML. Ce reformatage est utile pour rendre plus lisible le diff lors des import des paramètres de l'IPP.
  - Reformate les paramètres XML en utilisant le script décrit plus haut.
  - Ajoute un script de merge des paramètres XML avec les paramètres de l'IPP (Institut des Politiques Publiques). Ce script réécrit les paramètres XML en laissant un diff le plus lisible possible.

### 18.5.1 - [#780](https://github.com/openfisca/openfisca-france/pull/780)

* Amélioration technique
* Détails :
  - Migre les formules liées aux prestations sociales vers la syntaxe introduite par OpenFisca-Core 4

## 18.5.0 - [#704](https://github.com/openfisca/openfisca-france/pull/685)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2017
* Zones impactées : `openfisca_france/model/prestations/anah`.
* Détails :
  - Estimation de [l'éligibilité aux aides de l'ANAH](http://www.anah.fr/proprietaires/proprietaires-occupants/les-conditions-de-ressources/)

### 18.4.2 - [#770](https://github.com/openfisca/openfisca-france/pull/770)

* Amélioration technique
* Détails :
  - Mets à jour OpenFisca-Core
    - Modifie la manière de définir les dates de début des formules, et les dates de fin des variables.
    - Modifie les conventions de nommages des formules des variables.
    - Pour plus d'information, voir le [Changelog d'OpenFisca-Core](https://github.com/openfisca/openfisca-core/blob/master/CHANGELOG.md#1400---522) correspondant.

### 18.4.1 - [#776](https://github.com/openfisca/openfisca-france/pull/776)

* Correction d'un crash
* Détails :
  - Openfisca n'est pas compatible avec la nouvelle version de numpy 1.13.
  - Requiert numpy < 1.13

### 18.4.0 - [#772](https://github.com/openfisca/openfisca-france/pull/772)

* Amélioration technique
* Détails :
  - Permet d'ajouter une référence aux paramètres XML.
  - Supprime les commentaires des XML (Compatibilité avec core 13.0.0).

### 18.3.1 - [#767](https://github.com/openfisca/openfisca-france/pull/767)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/04/2017.
* Zones impactées :
  - `prestations.minima_sociaux.rsa`
  - `prestations.prestations_familiales.af`
* Détails :
  - Mise à jour du montant du montant de base pour le RSA aux 1er avril, 1er septembre 2017.
    - [Source](https://www.legifrance.gouv.fr/eli/decret/2017/5/4/2017-739/jo/article_1)
  - Mise à jour de la BMAF au 1er avril 2017
    - [Source](http://circulaire.legifrance.gouv.fr/pdf/2017/03/cir_41970.pdf)
  - Correction mineure du taux de la BMAF au 1er avril 2015
    - [Source](http://circulaire.legifrance.gouv.fr/pdf/2016/03/cir_40664.pdf) cf. valeur initiale (valeur erronée 406.21274, valeur corrigée 406.21)

### 18.3.0 - [#746](https://github.com/openfisca/openfisca-france/pull/746)

* Amélioration technique
* Détails :
  - Réunit dans un même répertoire les fichiers relatifs aux barèmes IPP.
  - Ajoute un script qui exécute le processus d'import dans son ensemble.
    - Laisse le contributeur commiter les changements manuellement.
	- Internalisation du dépôt [converters](https://framagit.org/french-tax-and-benefit-tables/ipp-tax-and-benefit-tables-converters) de l'IPP.
  - Désormais le seul lieu de contribution pour les paramètres est `openfisca_france/parameters`.
    - Disparition de `param.xml`.

### 18.2.9 - [#763]

* Changement mineur
* Détails :
  - Introduit la réforme `smic_h_b_9_euros`

### 18.2.8 - [#762](https://github.com/openfisca/openfisca-france/pull/762)

* Changement mineur
* Détails :
  - Fait passer les tests en parallèle

### 18.2.7 - [#728](https://github.com/openfisca/openfisca-france/pull/728)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/04/2016.
* Zones impactées :
  - `prestations.prestations_familiales.asf`
  - `prestations.prestations_familiales.cf`
  - `prestations.minima_sociaux.ass`
* Détails :
  - Mise à jour du montant de l'ASF aux 1er avril 2016, 1er avril 2017, et 1er avril 2018.
    - [Source pour 2016](https://www.legifrance.gouv.fr/affichTexteArticle.do?cidTexte=JORFTEXT000032345545&idArticle=LEGIARTI000032347447&dateTexte=20160403)
    - [Autre source pour 2016](http://circulaire.legifrance.gouv.fr/pdf/2016/03/cir_40664.pdf)
    - [Source pour 2017 et 2018](https://www.legifrance.gouv.fr/eli/decret/2017/4/12/2017-532/jo/texte)
  - Mise à jour du montant du CF majoré en métropole aux 1er avril 2017 et 1er avril 2018.
    - [Source](https://www.legifrance.gouv.fr/eli/decret/2017/4/12/2017-532/jo/texte)
  - Mise à jour du montant du du CF majoré dans les DOM au 1er avril 2017
    - [Source](https://www.legifrance.gouv.fr/eli/decret/2017/4/12/2017-534/jo/texte)
  - Mise à jour du montant de l'ASS aux 1er avril 2016 et premier avril 2017
    - [Source pour 2016](https://www.legifrance.gouv.fr/eli/decret/2016/5/3/2016-540/jo/texte)
    - [Source pour 2017](https://www.legifrance.gouv.fr/eli/decret/2017/5/10/2017-1022/jo/texte)
  - Mise à jour du montant de l'ATA aux 1er avril 2016 et premier avril 2017
    - [Source pour 2016](https://www.legifrance.gouv.fr/eli/decret/2016/5/3/2016-540/jo/texte)
    - [Source pour 2017](https://www.legifrance.gouv.fr/eli/decret/2017/5/10/2017-1022/jo/texte)

### 18.2.6 - [#747](https://github.com/openfisca/openfisca-france/pull/747)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/04/2017.
* Zones impactées : `prestations/minima_sociaux/asi_aspa`,
* Détails :
  - Mise à jour des plafonds et montants de l'ASI et de l'ASPA
  - Source: http://www.legislation.cnav.fr/Documents/circulaire_cnav_2017_13_04042017.pdf

### 18.2.5 - [#760](https://github.com/openfisca/openfisca-france/pull/760)

* Changement mineur
* Détails :
  - Supprime le système de chargement automatique des extensions via le dossier `extensions` . Les extensions sont maintenant installées sous la forme de packages indépendants.

### 18.2.4 - [#759](https://github.com/openfisca/openfisca-france/pull/759)

* Changement mineur
* Détails :
  - Suppression de l'internationalisation (traductions des messages d'erreurs). Cette fonctionnalité n'était pas utilisée.

### 18.2.3 - [#757](https://github.com/openfisca/openfisca-france/pull/757)

* Changement mineur
* Détails :
  - Retirer le fichier model/datatrees, le script de génération et les références aux date-trees présentes dans france_taxbenefitsystem.py

### 18.2.2 - [#742](https://github.com/openfisca/openfisca-france/pull/742)

* Amélioration technique
* Détails :
  - Amélioration des messages d'erreur en cas d'erreur dans la législation

### 18.2.1 - [#708](https://github.com/openfisca/openfisca-france/pull/708)

* Évolution du système socio-fiscal
* Périodes concernées : toutes
* Zones impactées : `prestations/aides_logement`
* Détails :
  - Corrige certains calculs pour les aides logement :
    - La neutralisation des ressources en cas de perception du RSA était sur-évaluée.
    - Les abattements des ressources en cas de chômage ou de départ en retraite étaient imprécis.
      - Non prise en compte des frais réels
      - Non prise en compte du plafond et du plancher pour l'abattement sur les frais profesionnels
  - Ajoute les références législatives

<!-- -->

* Amélioration technique
* Détails :
  - Migre toutes les formules de `prestations/aides_logement` vers la syntaxe `v4`

## 18.2.0 - [#731](https://github.com/openfisca/openfisca-france/pull/731)
* Amélioration technique
* Détails :
  - Adapte `france` à  la version `12.0.0` de `core`.
  - Enlève les attributs `fuzzy` des paramètres, qui devient le comportement par défaut. Enlève les attributs `fin`.

## 18.1.0 - [#739](https://github.com/openfisca/openfisca-france/pull/739)

* Changement mineur
* Détails:
  - Rends OpenFisca-France compatible avec la version `11.0` d'OpenFisca-Core

# 18.0.0 - [#718](https://github.com/openfisca/openfisca-france/pull/718)

* Évolution du système socio-fiscal
* Périodes concernées : toutes
* Zones impactées: `prestations/aides_logement`
* Détails :
    - Corrige l'erreur de frappe sur le nom de la variable `aide_logement_participation_personelle` qui devient donc `aide_logement_participation_personnelle`

## 17.2.0 - [#726](https://github.com/openfisca/openfisca-france/pull/726)

* Évolution du système socio-fiscal
* Périodes concernées : à partir du 01/04/2017.
* Zones impactées: `prelevements_obligatoires/prelevements_sociaux/contributions_sociales/versement_transport`
* Détails :
    - Mise à jour des taux de versement transport

* Changement mineur
* Zones impactées: `/assets/versement_transport`
* Détails :
    - Suppression de fichiers inutilisés (quelques mégas)

## 17.1.0 - [#724](https://github.com/openfisca/openfisca-france/pull/724)

* Amélioration technique.
* Détails :
  - Permet d'installer OpenFisca-France avec une API web compatible via `pip install openfisca_france[api]`
  - Redéploie `api.openfisca.fr` à chaque publication de version

### 17.0.1 - [#730](https://github.com/openfisca/openfisca-france/pull/730)

* Amélioration technique
* Détails :
  - Supprime les tests non exécutés par la CI
    - Ceux ignorés via le prefixe `IGNORE_` ou la propriété `ignore`
    - Ceux qui n'étaient pas mentionnés dans `test_yaml.py`
  - Exécute dans la CI tous les tests YAML présents dans le répertoire `tests`
  - Déplace les tests hors du package principal
  - Déplace les configurations par dossier des tests YAML vers les fichiers de tests.
  - Simplifie en conséquence `test_yaml.py`

# 17.0.0

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2003.
* Zones impactées : `prestations/prestations_familiales/aeeh`.
* Détails :
  - Retourne pour `aeeh` un montant mensuel et non annuel

### 16.1.1 - [#632](https://github.com/openfisca/openfisca-france/pull/632)

* Changement mineur
* Détails :
    - Arrête d'importer de numpy des fonctions qui sont déjà fournies par `openfisca_core.model_api`

## 16.1.0 - [#707](https://github.com/openfisca/openfisca-france/pull/707))

* Évolution du système socio-fiscal
* Périodes concernées : à partir du 01/07/2016.
    - Les changements prennent effet à partir de la rentrée scolaire 2016
* Zones impactées: `prestations/education`
* Détails :
    - Met à jour le mode de calcul des bourses de collège et lycée, entré en vigueur à la rentrée 2016.
    - Introduit les variables `bourse_college_echelon` et `bourse_lycee_echelon`

# 16.0.0 - [#710](https://github.com/openfisca/openfisca-france/pull/710)
* Amélioration technique **non-rétrocompatible**
* Détails :
    - Restreint les périodes acceptées par OpenFisca
    - La liste des périodes autorisées est disponible dans la [documentation](http://openfisca.org/doc/periodsinstants.html)

<!-- -->

* Amélioration technique
* Détails :
  - Adapte `france` à  la version `9.0.0` de `core`.

## 15.1.0 - [#699](https://github.com/openfisca/openfisca-france/pull/699)

> Version précédemment publiée à tort en tant que 14.2.0

* Amélioration technique
* Détails :
  - Adapte `france` à  la version `7.0.0` de `core`.
  - Spécifie toujours une période dans les appels de variables, dans les formules et dans les tests.

<!-- -->

* Évolution du système socio-fiscal
* Périodes concernées : toutes
* Zones impactées : `revenus/activite/salarie`
* Détails :
  - Corrige le calcul de `salaire_net_a_payer`
  - Dans certains cas, on utilisait la valeur de `depense_cantine_titre_restaurant_employe` pour une autre période que celle demandée.

### 15.0.1 - [#697](https://github.com/openfisca/openfisca-france/pull/697)

> Version précédemment publiée à tort en tant que 14.1.1

* Amélioration technique
* Utilise le module `core.model_api` plutôt que de réimporter un par un tous les objets Python nécessaires pour écrire une formule
    - Aucun impact pour les ré-utilisateurs

# 15.0.0 - [#685](https://github.com/openfisca/openfisca-france/pull/685)

> Version précédemment publiée à tort en tant que 14.1.0

* Amélioration technique **non-rétrocompatible**
* Détails :
  - Interdit par défaut de calculer ou de définir une variable pour une période qui ne correspond pas à sa période de définition.
    - Par exemple, interdit de définir une variable annuelle, comme l'impôt sur le revenu, sur un mois.
  - Renforce le contrôle de cohérence des entrées d'une simulation.
  - Interdit de déclarer, pour une entrée de la simulation, à la fois un montant annuel et les douze montants mensuels correspondants s'ils ne sont pas parfaitement cohérents.

<!-- -->

* Amélioration technique
* Détails :
  - Adapte `france` à  la version `6.0.0` de `core`.
  - Évolution du format de retour des formules : `return result` à la place de `return period, result`.
  - Ajout d'un attribut `definition_period` pour toutes les variables.

# 14.0.0 - [#690](https://github.com/openfisca/openfisca-france/pull/690)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : aucune.
* Détails :
  - Retire la variable  `nbptr_n_2`. Elle est inutilisée et obsolète depuis l'introduction des `period`.
  - Cette variable n'intervenant dans aucune formule, elle n'a donc aucun impact.

### 13.2.2 - [#695](https://github.com/openfisca/openfisca-france/pull/695)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `mesures`.
* Détails :
  - Correction du calcul de `type_menage`.
  - Des erreurs peuvent subsister quand ménage et famille ne coincide pas (cas des ménages complexes).
  - Cette variable est utilisée à des fins statistiques et n'entre dans le calcul d'aucune prestation.

### 13.2.1 — [#687](https://github.com/openfisca/openfisca-france/pull/687)

* Évolution du système socio-fiscal.
* Périodes concernées : Jusqu'au 31/12/2015.
* Zones impactées : `prelevements_obligatoires/impot_revenu/ppe`.
* Détails :
  - Corrige la valeur erronnée retournée par `ppe_tp_sa`.
  - Le calcul de l'indicatrice de travail à temps plein `ppe_tp_sa` renvoyait une valeur érronée, provoquant des erreurs dans le calcul de la prime pour l'emploi `ppe`.

## 13.2.0 - [#676](https://github.com/openfisca/openfisca-france/pull/676)

* Amélioration technique
* Détails :
  - Cette évolution est a priori transparente pour les utilisateurs.
  - Déplace la transformation du JSON en test case du module `scenarios` de `france` vers `core`
  - Adapte `france` à  la version `5.0.0` de `core`.

### 13.1.5 - [#684](https://github.com/openfisca/openfisca-france/pull/684)

* Évolution du système socio-fiscal
* Périodes concernées : à partir du 01/01/2017.
* Zones impactées : `prelevements_obligatoires/prelevements_sociaux/cotisations_sociales`
* Détails :
  - Corrige le taux de la réduction générale sur les bas salaires (Fillon) au 01/01/2017.
  - Corrige le taux de la cotisation maladie MMID employeur au 01/01/2017.

### 13.1.4 - [#682](https://github.com/openfisca/openfisca-france/pull/682)

* Évolution du système socio-fiscal
* Périodes concernées : à partir du 01/01/2017.
* Zones impactées : `prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/travail_prive`
* Détails :
  - Met à jour la valeur de l'AGS au 01/01/2017.
  - La mise à jour de l'AGS de la version 10.0.1 n'a pas fonctionné, pour cause de duplication de paramètres.

### 13.1.3

* Fix `rsa_has_ressources_substitution` `Column` attribute

### 13.1.2

* Refactor TaxBenefitSystem decomposition attributes

### 13.1.1

* Update taux CICE 2017 : from 6% to 7%

## 13.1.0

* Use `individu` `revenus_locatifs` if any to compute `f4ba` (revenus fonciers imposables)

This may change any variable related to impot sur le revenu if `revenus_locatifs` is not zero and f4ba is not initialized.

### 13.0.2

* Add `pensions_invalidite` to pensions imposables

### 13.0.1

* Fix `ppe`

# 13.0.0

* Deprecate `nbsala`
* Deprecate `tva_ent`

These changes are low impact since the two deprecated variables were not used.

## 12.0.6

* Fix `rsa_activite`

## 12.0.5

* Change `af` to DatedVariable to take into account the introduction of degressivite

## 12.0.4

* Change `aige_aine` column from IntCol to AgeCol.

## 12.0.3

* Rename `CAT` to `CATEGORIE_SALARIE` to be more explicit.

## 12.0.2

* Don't consider handicaped demandeur/conjoint as personne à charge in aides logement.

## 12.0.1

* Fix `aide_logement_montant_brut_avant_degressivite` returned `period` to month.

## 12.0.0

* Use core `test_runner` for yaml tests
* Return yearly amount for `acs`, `bourse_college`, `bourse_lycee` instead of artificially divide it by 12 (breaking change).

## 11.1.0

 * Implement "Aides au logement" degression when rent is above a threshold.

## 11.0.2

* Fix typo in `casa` variable label

## 11.0.1

* Add a `sans_objet` level to variable `contrat_de_travail`

## 11.0.0

* Rename `cotsoc_noncontrib` to `cotisations_non_contibutives`

## 10.1.1

* Fix combination rule for aide 1er salarié / aide PME

## 10.1.0

* Add cotisation pénibilité

## 10.0.2

* Fix csg legislation link in `inversion_directe_salaires` reform.

## 10.0.1

* Update the following rates that changed on the first of january 2017:
	- SMIC
	- Plafond de la sécurité sociale
	- Taux AGIRC-GMP
	- Taux AGS
	- Prolongation Aide embauche PME 2017

## 10.0.0

* From 2017, for RSA, remove CA and number of employees conditions.
* Calculate RSA for Travailleurs Non Salariés
* Introduce RSA fictif mechanism
* Deprecate:
	- `rsa_majore`
	- `rsa_non_majore`
* Introduce inputs:
	- `primes_salaires_net`
	- `indemnite_fin_contrat_net`

## 9.0.1

* Add `fuzzy` in some `ppa` parameters, needed to run calculations in 2017

## 9.0.0

* Continue mesures migration
* Complete remplacement migration
* Rename `impo` to `impots_directs`
* Rename `revnet` to `revenu_net`
* Rename `revini` to `revenu_initial`

## 8.0.1

* Introduce echelon_bourse

## 8.0.0

* Rename `paje_clmg` to `paje_cmg`

## 7.0.1

* Improving CASA

## 7.0.0

* Introduce minimum_vieillesse
* Rename `mini` to `minima_sociaux`
* Rename `nivvie` to `niveau_de_vie`
* Rename `nivvie_net` to `niveau_de_vie_net`
* Rename `nivvie_ini` to `niveau_de_vie_initial`
* Rename `pfam` to `prestations_familiales`
* Rename `psoc` to `prestations_sociales`
* Rename `pen` to `pensions`
* Rename `rev_cap` to `reveunus_du_capital`
* Rename `rev_trav` to `revenus_du_travail`
* Rename `revdisp` to `revenu_disponible`
* Rename `typ_men` to `type_menage`
* Cleaning:
   * remove superfluous `default = 0` in `FloatCol` and `IntCol`
   * remove superfluous comments
   * migrate some formulas

## 6.1.0

* Add the local regime Alsace-Moselle through the boolean variable `salarie_regime_alsace_moselle`.
* Impacts the cotisations :
	* Maladie (MMID)
	* Taxe apprentissage
	* Contribution supplémentaire à l'apprentissage.

## 6.0.7

* Remove wrong max numbers of enfants in entities

## 6.0.6

* Deprecate `entreprise_assujettie_tva`

## 6.0.5

* Add effectif_entreprise exclusion condition to Contribution Supplémentaire Apprentissage

## 6.0.4

* Fix some regressions in parameters introcduced by 6.0.0
    * Re-apply RSA revalorisation from september
    * Correct bonification rate for PPA

## 6.0.3

* Migrate some formulas to new syntax
    * `aefa.py`
    * `af.py`
    * `anciens_ms.py`
    * `ars.py`
    * `base_ressource.py`
    * `cf.py`
    * `paje.py`
    * `rsa.py`

## 6.0.2

* Fix legislation parameter call for RMI-RSA transition

## 6.0.1

* Fix packaging of 6.0.0

## 6.0.0

* Use legislation parameters from IPP

* Rename variables:
	* `cd_penali` -> `pensions_alimentaires_deduites`
	* `cd_percap` -> `pertes_capital_societes_nouvellespertes_capital_societes_nouvelles`
	* `cd_cinema` -> `souscriptions_cinema_audiovisuel`
	* `cd_ecodev` -> `epargne_codeveloppement`
	* `cd_grorep` -> `grosses_reparations`

* Add variables for allocation pour demandeur d'asile (ADA):
	* `asile_demandeur`
	* `place_hebergement`
	* `ada`

## 5.0.0b0

* Adapt France to Openfisca-Core#v4
	* Declare entities in the new way

* Deprecate all conversion variables:
	* `cotsoc_bar_declarant1`
	* `cotsoc_lib_declarant1`
	* `crds_cap_bar_declarant1`
	* `crds_cap_lib_declarant1`
	* `csg_cap_bar_declarant1`
	* `csg_cap_lib_declarant1`
	* `loyer_famille`
	* `loyer_individu`
	* `maj_cga_individu`
	* `pensions_alimentaires_versees_declarant1`
	* `prelsoc_cap_bar_declarant1`
	* `prelsoc_cap_lib_declarant1`
	* `retraite_titre_onereux_declarant1`
	* `retraite_titre_onereux_net_declarant1`
	* `rev_microsocial_declarant1`
	* `statut_occupation_famille`
	* `statut_occupation_logement_individu`
	* `zone_apl_famille`
	* `zone_apl_individu`

* Deprecate entity structure variables:
	* `idmen`
	* `idfoy`
	* `idfam`
	* `quimen`
	* `quifoy`
	* `quifam`

* Change some variables entity:
	* `FoyersFiscaux` -> `Individus`
		* `maj_cga`
	* `Individus` -> `FoyersFiscaux
		* `rev_coll`
	* `Individus` -> `Menages`
		* `coloc`
		* `logement_chambre`
	* `Familles` -> `Individus`
		* `aah_non_calculable`
	* `Familles` -> `Menages`
		* `residence_dom`
		* `residence_guadeloupe`
		* `residence_martinique`
		* `residence_guyane`
		* `residence_reunion`
		* `residence_mayotte`

* Introduce:
    * `cotsoc_bar`
    * `cotsoc_lib`

## 4.1.20

 * Set `set_input` attribute to `set_input_divide_by_period` for variables `heures_remunerees_volume` et `heures_non_remunerees_volume`.

## 4.1.19

* Introduce MVA

## 4.1.18

* Introduce PCH

## 4.1.17

* Reimplement `rsa_indemnites_journalieres_activite` and `date_arret_de_travail` using `datetime.date.min`.

## 4.1.16

* Correct wrong behaviour in the combination of exemptions with the dispositif Jeune Entreprise Innovante (JEI)


## 4.1.15

* Consider some indemnités journalieres as revenus de remplacement in PPA (and RSA), according to the date of the arret de travail.
* Introduce
	* `rsa_indemnites_journalieres_hors_activite`
	* `rsa_indemnites_journalieres_activite`
	* `date_arret_de_travail`

## 4.1.14

* Add cerfa boxe : 3vt (PEA)

## 4.1.13

* Increase RSA base amount to 535.17 from September 2016

## 4.1.12

* Fix links in README

## 4.1.11

* Remove end dates where not necessary

## 4.1.10

* Refactor asi_aspa.py
* Fix abattement for conjoint salary
* Adjust interaction with AAH
* Small fix on RSA: don't use euclidian division because of rounding issues
* Small fix on PPA: don't take into acccount more AF that it have been declared (see 4.1.8)

## 4.1.9

* Tighten CMU/ACS eligibility conditions when when person is less than 25
* Introduce `cmu_acs_eligibilite`, `habite_chez_parents`

## 4.1.8

* Refactor rsa.py
* Do not take stages gratification into account
* Do not take into acccount more AF that it have been declared

## 4.1.7

* Fix bug in CMU forfait_logement
* Refactor CMU computation

## 4.1.6

* Fix bugs in RSA:
  * One need to be **strictly** more that 25 to benefit it.
  * Apply rsa_forfait_asf accordingly to the asf actually being paid.
* Deprecate rsa_forfait_asf_individu

## 4.1.5

* Follow OpenFisca-Core major release

## 4.1.4

* Update travis procedures

## 4.1.3

* Delete rfr_n_1

## 4.1.2

* Use "python -m compileall" to check for syntax errors, not flake8

## 4.1.1

* Add labels to several variables

## 4.1.0

* Run yaml tests from CLI
	* Exemple: `openfisca-run-test my_test.yaml`

## 4.0.11

* Enhance and move getting-started notebook

## 4.0.10 - [diff](https://github.com/openfisca/openfisca-france/compare/4.0.9..4.0.10)

* Fix Landais, Piketty, Saez reform

## 4.0.9 - [diff](https://github.com/openfisca/openfisca-france/compare/4.0.8..4.0.9)

* Adapt plfr2014 reform to new Reform API

## 4.0.8 - [diff](https://github.com/openfisca/openfisca-france/compare/4.0.7..4.0.8)

* Adapt PPA to avoid antedating paramameters of 3 months.

## 4.0.7 - [diff](https://github.com/openfisca/openfisca-france/compare/4.0.6..4.0.7)

* Include ppa in minimas sociaux (mini) and update decompositions accordingly

## 4.0.6 - [diff](https://github.com/openfisca/openfisca-france/compare/4.0.5..4.0.6)

* Add back extensions folder and README

## 4.0.5 - [diff](https://github.com/openfisca/openfisca-france/compare/4.0.4..4.0.5)

* Fix inversion-directe-salaires reform

## 4.0.4 - [diff](https://github.com/openfisca/openfisca-france/compare/4.0.3..4.0.4)

* Fix plf2016 and ayrault_muet reforms

## 4.0.3 - [diff](https://github.com/openfisca/openfisca-france/compare/4.0.2..4.0.3)

* Update numpy dependency to 1.11
* Upgrade pip to >= 8.0 in travis
* Do not install numpy from apt in travis
* Install scipy by wheels
* Fix semver version number towards OpenFisca-Core

## 4.0.2 - [diff](https://github.com/openfisca/openfisca-france/compare/4.0.1..4.0.2)

* Remove wrong stop date of `aeeh`

## 4.0.1 - [diff](https://github.com/openfisca/openfisca-france/compare/4.0.0..4.0.1)

* Correct bug in `switch_on_allegement_mode`

## 4.0.0 - [diff](https://github.com/openfisca/openfisca-france/compare/3.4.1..4.0.0)

* Apply core API changes introduced by [openfisca-core 2.0](https://github.com/openfisca/openfisca-core/pull/388)
* Change the way the France tax benefit system is built
* Change the way reforms are built
* Move extensions from `./model/extensions` to `./extensions`
* Warning : relatives imports are now impossible in model files.

## 3.4.1 - [diff](https://github.com/openfisca/openfisca-france/compare/3.4.1..3.4.0)

* Only enforce version and changelog update in CI when PR target is master.

## 3.4.0 - [diff](https://github.com/openfisca/openfisca-france/compare/3.4.0..3.3.0)

* Introduce the `entreprise_est_association_non_lucrative` boolean input variable
* Null the CICE and taxe d'apprentissage (taxe + contribution supplémentaire) when this input is True
* Force the computing of taxe sur les salaires when this input is True
* Implement franchise, décôte and abattement associations non lucratives in Taxe sur les salaires

## 3.3.0 - [diff](https://github.com/openfisca/openfisca-france/compare/3.3.0..3.2.0)

* Add variables for `complémentaire santé`, compulsory in 2016 :
	* `complementaire_sante_taux_employeur`
	* `complementaire_sante_employeur`
	* `complementaire_sante_salarie`
It is included in the bases of the following variables.

* Correct `forfait_social` and link it to the `cotisations`, test it.
* Correct `taxe_salaires` and update its rates
* Test CSG-CRDS

## 3.2.0 - [diff](https://github.com/openfisca/openfisca-france/compare/3.2.0..3.1.0)

* Consolidate the case of `temps partiel` for the input of a number of hours per month, based on the legal duration of 151.67 per month
* Specifically, correct the proratisation of `plafond de la sécurité sociale` and `coefficient de proratisation`.
* See issue #496 for details

## 3.1.0 - [diff](https://github.com/openfisca/openfisca-france/compare/3.1.0..3.0.0)

* Update the rates of the versement transport contribution
* Introduce an history of rates
* Move its code to a new file (~ 5 functions)

## 3.0.0 - [diff](https://github.com/openfisca/openfisca-france/compare/3.0.0..2.0.0)

* Make `enfant_a_charge` usable in monthly mode so that we can re-use it in mes-aides, and broaden its definition so that in includes children in `garde_alternee`.
* Refactor and test nbF, nbG, nbH, nbI.
* Deprecate:
	* `nombre_enfants_a_charge_menage`
	* `enfant_a_charge_invalide`
	* `enfant_a_charge_garde_alternee`
	* `enfant_a_charge_garde_alternee_invalide`
* Rename:
    * `statmarit` -> `statut_marital`
    * `marpac` -> `maries_ou_pacses`
    * `celdiv` -> `celibataire_ou_divorce`
    * `jveuf` -> `jeune_veuf`

## 2.0.0 - [diff](https://github.com/openfisca/openfisca-france/compare/1.3.1..2.0.0)

* Deprecate Paris reform
* Introduce enfant_place

## 1.3.1 – [diff](https://github.com/openfisca/openfisca-france/compare/1.3.1rc0...1.3.1)

* Adjust ppa computation

## 1.3.1rc0 – [diff](https://github.com/openfisca/openfisca-france/compare/1.3.0..1.3.1rc0)

* Fix versioning enforcement

## 1.3.0 – [diff](https://github.com/openfisca/openfisca-france/compare/1.2.0...1.3.0)

* Introduce mechanism to blacklist variables so that they are not cached
* Refactor AL computation, and implement special DOM rules
* Introduce:
	* `aide_logement_loyer_retenu`
	* `al_couple`
	* `aide_logement_charges`
	* `aide_logement_R0`
	* `aide_logement_taux_famille`
	* `aide_logement_taux_loyer`
	* `aide_logement_participation_personnelle`

## 1.2.0 – [diff](https://github.com/openfisca/openfisca-france/compare/1.1.0...1.2.0)

* Force version number incrementation through CI
* Force changelog editing through CI
* Publish tag after merging
* Publish on pypi after tagging

## 1.1.0 – [diff](https://github.com/openfisca/openfisca-france/compare/1.0...1.1.0)

* Replace `build_column` function calls by `Variable` classes (see [#384](https://github.com/openfisca/openfisca-core/pull/384))

## 1.0 – [diff](https://github.com/openfisca/openfisca-france/compare/0.5.5...1.0)

* Add tests yaml for cotisations sociales
* Introduction of `invalidite`
* Depreciation of `af_enfant_a_charge`, `asf_enfant`, `isol`, `pfam_ressources_i`, `rmi_nbp`, `sal_pen_net`.
* Massive renaming:
	* `abat_sal_pen` -> `abattement_salaires_pensions`
	* `af_forf_complement_degressif` -> `af_allocation_forfaitaire_complement_degressif`
	* `af_forf_nbenf` -> `af_allocation_forfaitaire_nb_enfants`
	* `af_forf_taux_modulation` -> `af_allocation_forfaitaire_taux_modulation`
	* `af_forf` -> `af_allocation_forfaitaire`
	* `af_majo` -> `af_majoration`
	* `al_pac` -> `al_nb_personnes_a_charge`
	* `als_nonet` -> `als_non_etudiant`
	* `alset` -> `als_etudiant`
	* `ape_temp` -> `ape_avant_cumul`
	* `apje_temp` -> `apje_avant_cumul`
	* `asi_aspa_base_ressources_i` -> `asi_aspa_base_ressources_individu`
	* `asi_elig` -> `asi_eligibilite`
	* `aspa_elig` -> `aspa_eligibilite`
	* `ass_base_ressources_i` -> `ass_base_ressources_individu`
	* `ass_eligibilite_i` -> `ass_eligibilite_individu`
	* `biact` -> `biactivite`
	* `birth` -> `date_naissance`
	* `br_mv_i` -> `asi_aspa_base_ressources_i`
	* `br_mv` -> `asi_aspa_base_ressources`
	* `br_pf_i` -> `prestations_familiales_base_ressources_i`
	* `br_pf` -> `prestations_familiales_base_ressources`
	* `categ_inv` -> `aeeh_niveau_handicap`
	* `cf_ressources_i` -> `cf_ressources_individu`
	* `cmu_base_ressources_i` -> `cmu_base_ressources_individu`
	* `concub` -> `en_couple`
	* `invalide` -> `handicap`
	* `maj_cga_i` -> `maj_cga_individu`
	* `nb_enfant_rsa` -> `rsa_nb_enfants`
	* `nb_par` -> `nb_parents`
	* `pen_net` -> `revenu_assimile_pension_apres_abattements`
	* `pfam_enfant_a_charge` -> `prestations_familiales_enfant_a_charge`
	* `ppa_ressources_hors_activite_i` -> `ppa_ressources_hors_activite_individu`
	* `ppa_revenu_activite_i` -> `ppa_revenu_activite_individu`
	* `ppe_elig_i` -> `ppe_elig_individu`
	* `prestations_familiales_base_ressources_i` -> `prestations_familiales_base_ressources_individu`
	* `rev_act_nonsal` -> `revenu_activite_non_salariee`
	* `rev_act_sal` -> `revenu_activite_salariee`
	* `rev_pen` -> `revenu_assimile_pension`
	* `rev_sal` -> `revenu_assimile_salaire`
	* `rpns_i` -> `rpns_individu`
	* `rsa_act_i` -> `rsa_activite_individu`
	* `rsa_act` -> `rsa_activite`
	* `rsa_base_ressources_i` -> `rsa_base_ressources_individu`
	* `rsa_base_ressources_patrimoine_i` -> `rsa_base_ressources_patrimoine_individu`
	* `rsa_forfait_asf_i` -> `rsa_forfait_asf_individu`
	* `rsa_non_calculable_tns_i` -> `rsa_non_calculable_tns_individu`
	* `rsa_revenu_activite_i` -> `rsa_revenu_activite_individu`
	* `rto_declarant1` -> `retraite_titre_onereux_declarant1`
	* `rto_net_declarant1` -> `retraite_titre_onereux_net_declarant1`
	* `rto_net` -> `retraite_titre_onereux_net`
	* `salcho_imp` -> `revenu_assimile_salaire_apres_abattements`
	* `smic55` -> `autonomie_financiere`
	* `statut_occupation_famille` -> `statut_occupation_logement_famille`
	* `statut_occupation_individu` -> `statut_occupation_logement_i`
	* `statut_occupation_logement_i` -> `statut_occupation_logement_individu`
	* `statut_occupation` -> `statut_occupation_logement`
	* `tns_employe` -> `tns_avec_employe`
	* `tspr` -> `traitements_salaires_pensions_rentes`
	* `type_sal` -> `categorie_salarie`

## 0.5.5 – [diff](https://github.com/openfisca/openfisca-france/compare/0.5.4.3...0.5.5)

* Prime d'activité fiabilization
* Implementation of Indemnite de fin de contrat
* Prolongation of aidper, credit_impots, reductions
* Remove detailes logs in CI
* Update prestations parameters (2016/04/01 revalorisation)
* Add net -> brut reform

## 0.5.4.2, 0.5.4.3 – [diff](https://github.com/openfisca/openfisca-france/compare/0.5.4.1...0.5.4.3)

* Update OpenFisca-Core requirement version

## 0.5.4.1 – [diff](https://github.com/openfisca/openfisca-france/compare/0.5.4...0.5.4.1)

* Add missing assets for versement_transport

## 0.5.4 – [diff](https://github.com/openfisca/openfisca-france/compare/0.5.3...0.5.4)

* Many updates

## 0.5.3 – [diff](https://github.com/openfisca/openfisca-france/compare/0.5.2...0.5.3)

* Fix vieillesse deplafonnee baremes
* Fix some dates in arrco and formation prof. baremes
* Remove obsolete or unuseful comment which induces indentation problem when using parameters fusion scripts
* Improve decote legislation parameters
* Removing unused obsolete reform parameters still in param.xml
* Add tests
* Round ceilings values
* Resources need to be non superior to ceilings, not inferior
* update bourse_college params
* flake8
* Do not pre-initialize reforms cache
* Remove licence from code files
* Introduce asi_aspa_condition_nationalite Introduce rsa_condition_nationalite
* Introduce ressortissant_eee Introduce duree_possession_titre_sejour
* change it in the tests too...
* Change name and description of the prestation
* add a test for decote where the individual is below the first tax threshold
* implement true_decote that is the decote amount provided by dgfip (at list on their simulator) which is the fiscal gain accountable to the decote mechanism
* add a test for irpp couples
* Actualize legislation for min/max abattements pour frais pro add a test for IR 2015 ; change label of reform plf 2015.
* Change reforms.plf2015 decote to a DatedVariable
* Conform to instructions given by @benjello for PR
* add empty line
* add an empty line for two empty lines between two classes
* add decote ir2014 on income 2014 from reform plf hardcoded.
* Small changes, trash plf2015 reform
* Put reforms/plf2015.py into legislation. WIP still need a proper test on decote
* Return ape_temp for a month, not for a weird period
* Repair imports in test_basics.py
* Remove irrelevant calculate_divide and calculate_add_divide in rsa.py, cf.py, asi_aspa.py
* Merge formulas and formulas_mes_aides folder
* Typo in cerfa field
* Add test for psoc formula
* Clean test_plf2015
* NOT WORKING Reform plf2015 on revenus 2013
* Rename paje_nais to paje_naissance
* Fix params references
* Redefine period in functions
* Fix indentation in params
* Fix param for retro-compatibility
* Kid age need to be *strictly* < 3
* Réécriture et update de la paje
* Rename cf_temp to cf_montant Rename paje_base_temp to paje_base_montant
* Refactor aide_logement_montant_brut
* Add clean-mo target
* Add make clean target
* Add MANIFEST.in
* Do not package tests
* Remove unnecessary __init__.py in scripts
* Add data_files in setup.py
* Use extras_require in setup.py
* Remove nose section from setup.cfg
* Add CONTRIBUTING.md file

## 0.5.2 – [diff](https://github.com/openfisca/openfisca-france/compare/0.5.1...0.5.2)

* Merge pull request #304 from sgmap/taille_entreprise
* Remove unmaintainable tests
* Merge pull request #307 from sgmap/al-abattement-30-retraite
* Merge pull request #301 from sgmap/several-updates
* Move doc to openfisca-gitbook
* Massive test update
* Rename asf_elig_i to asf_elig_enfant Rename asf_i to asf_enfant
* Rename fra to frais_reels Rename cho_ld to chomeur_longue_duree
* Give RSA to young people with kids
* Enhance error when loading a cached reform which was undeclared
* Merge remote-tracking branch 'sgmap/executable-test' into next
* Merge remote-tracking branch 'origin/master' into next
* Merge pull request #303 from sgmap/plafonds-fillon
* Display YAML file path on test error
* Use relative error margin in fillon test
* Add tests for fillon from embauche.sgmap.fr
* Update end date for fillon seuil
* Update plafonds for fillon
* Merge remote-tracking branch 'sgmap/plafonds-fillon' into next
* Add tests for fillon from embauche.sgmap.fr
* Make test_yaml.py executable
* Merge pull request #302 from sgmap/no-bom
* Remove leading U+FEFF from param.xml
* Update travis according to http://docs.travis-ci.com/user/migrating-from-legacy/
* Do not install scipy in travis
* Do not use relative import in script (__main__)
* Add biryani extra require

## 0.5.1 – [diff](https://github.com/openfisca/openfisca-france/compare/0.5.0...0.5.1)

* Remove scipy by default

## 0.5.0

* First release uploaded to PyPI
