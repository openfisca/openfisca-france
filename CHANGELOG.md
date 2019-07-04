# Changelog

# 48.0.0 [#1353](https://github.com/openfisca/openfisca-france/pull/1353)

* Évolution du système socio-fiscal **non rétrocompatible**
* Périodes concernées : toutes.
* Zones impactées :
  - `openfisca_france/model/prestations/minima_sociaux/aah.py`
  - `openfisca_france/parameters/prestations/minima_sociaux/aah`
  - `openfisca_france/parameters/prestations/minima_sociaux/caah`
* Détails :
  - Supprime un doublon entre les paramètres `aah.mva` et `caah.majoration_vie_autonome` (on garde le second).
  - Supprime un doublon entre les paramètres `caah.cpltx` et `caah.taux_du_montant_mensuel_du_complement_aux_adultes_handicape_2` (on renomme en `caah.taux_montant_complement_ressources`).
  - Renomme le paramètre `aah.majoration_du_plafond_pour_un_couple` en `aah.majoration_plafond_couple`.
  - Renomme le paramètre `aah.tx_plaf_supp` en `aah.majoration_plafond_personne_a_charge`.
  - Renomme le paramètre `aah.plafond_de_ressources_en_multiple_du_montant_de_base` en `aah.plafond_ressources`.

## 47.3.0 [#1352](https://github.com/openfisca/openfisca-france/pull/1352)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `openfisca_france/model/prestations/minima_sociaux/aah.py`, `openfisca_france/parameters/prestations/minima_sociaux/aah`, ` openfisca_france/parameters/prestations/minima_sociaux/caah`.
* Détails :
  - Supprime un doublon entre les paramètres `aah.mva` et `caah.majoration_vie_autonome` (on garde le second).
  - Supprime un doublon entre les paramètres `caah.cpltx` et `caah.taux_du_montant_mensuel_du_complement_aux_adultes_handicape_2` (on renomme en `caah.taux_montant_complement_ressources`).
  - Renomme le paramètre `aah.majoration_du_plafond_pour_un_couple` en `aah.majoration_plafond_couple`.
  - Renomme le paramètre `aah.tx_plaf_supp` en `aah.majoration_plafond_personne_a_charge`.
  - Renomme le paramètre `aah.plafond_de_ressources_en_multiple_du_montant_de_base` en `aah.plafond_ressources`.

### 47.2.1 [#1350](https://github.com/openfisca/openfisca-france/pull/1350)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `tests`.
* Détails :
  - Supprime le test `test_api.py` dont le temps d'exécution est prohibitif (10s), la valeur ajoutée très faible (aucune information actionable n'est fournie en cas d'erreur) et qui dégrade l'expérience des contributeurs

## 47.2.0 [#1337](https://github.com/openfisca/openfisca-france/pull/1337)

* Évolution du système socio-fiscal
* Périodes concernées : jusqu'au 31/12/2018
* Zones impactées : `openfisca_france/parameters/impot_revenu`.
* Détails :
  - Mise à jour des charges déductibles du revenu brut global
  - Mise à jour de l'abattement pour revenu net imposable
  - Mise à jour du plafonnement du quotient familial et décote

## 47.1.0 [#1347](https://github.com/openfisca/openfisca-france/pull/1347)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 08/08/2016.
* Zones impactées : N/A.
* Détails :
  - Ajoute la Garantie Jeunes, modélisée par la variable `garantie_jeunes`
    - La garantie jeunes permet d'accompagner les jeunes entre 16 et 25 ans en situation de grande précarité vers l'emploi ou la formation. C'est une modalité spécifique du parcours contractualisé d'accompagnement vers l'emploi et l'autonomie (PACEA).

### 47.0.1 [#1349](https://github.com/openfisca/openfisca-france/pull/1349)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `aah.py`.
* Détails :
  - Corrige des erreurs de formatage bloquantes pour suivre les instructions du README

# 47.0.0 [#1343](https://github.com/openfisca/openfisca-france/pull/1343)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2018.
* Zones impactées :
  - `prelevements_obligatoires/impot_revenu`
  - `revenus/capital/financier`
* Détails :
  - Affine et corrige [#1333](https://github.com/openfisca/openfisca-france/issues/1333) sur le PFU
  - Le PFU a été codé avant la publication du nouveau formulaire de l'IR et des règles précises concernant son application. Désormais, le formulaire est disponible et les règles connues, cette PR vient les corriger
  - Pour plus de détails voir [le descriptif](https://github.com/openfisca/openfisca-france/pull/1343) de la version
  - Corrige également le calcul du RFR pour les années avant 2018 (notamment la prise en compte de l'abattement sur les assurance-vie)

## Guide de migration
  - La variable `assurance_vie_pfu_ir_moins8ans_19970926_primes_apres_20170927`est renommée `f2zz`,
  - La variable `assurance_vie_pfu_ir_plus8ans_19970926_primes_apres_20170927` est remplacée par `f2ww` et `f2zz` (l'ancienne variable correspond à la somme de ces deux nouvelles)

# 46.0.0 [#1320](https://github.com/openfisca/openfisca-france/pull/1320)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées :
  - `prelevements_obligatoires/taxe_habitation`
  - `prelevements_obligatoires/isf`
  - `mesures`
* Détails :
  - Re-code la taxe d'habitation (TH) : on code la TH des communes et EPCI (Etablissement Public de Coopération Intercommunale) due au titre de la résidence principale à partir de la législation 2017, et jusqu'à la législation 2019. Cette PR intègre les barèmes locaux votés par les communes et EPCI (taux de taxation, taux d'abattements) de 2017.
  - Paramètres supprimés :
    - `cotsoc/gen/plaf_th_1`
    - `cotsoc/gen/plaf_th_1_dom`
    - `cotsoc/gen/plaf_th_1_guy`
    - `cotsoc/gen/plaf_th_supp`
    - `cotsoc/gen/plaf_th_supp1_dom`
    - `cotsoc/gen/plaf_th_supp1_guy`

# 45.0.0 [#1340](https://github.com/openfisca/openfisca-france/pull/1340)

* Suppression d'éléments redondants du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées :
  - `impot_revenu`, `revenus`
  - `parameters\prelevements_sociaux\contributions\csg\remplacement`
* Détails :
  - Supprime la variable `cbnc_assc` redondante avec `f5qm`, la variable `f1tz` inutilisée
  - Ajoute l'attribut `cerfa_field` à la variable fiscale `f3va`
  - Met à jour les paramètres relatifs à la CSG sur revenus de remplacement
  - Ajoute une option d'installation `casd-dev` pour les activités de développement de l'IPP au CASD

# 44.0.0 [#1329](https://github.com/openfisca/openfisca-france/pull/1329)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2018.
* Zones impactées : `model/prelevements_obligatoires/impot_revenu/`.
* Détails :
  - Ajoute comme inputs variables les nouvelles cases de la déclaration IR 2018 liée au crédit d'impôt pour la transition énergétique (CITE)
  - Renomme les anciennes inputs variables du même nom, selon la méthode habituelle
  - Mets à jour la formule pour l'impôt 2019 sur revenus 2018
  - Factorise les formules 2016, 2017 et 2018.

## Guide de migration

- Si vous utilisiez les variables `f7bm`, `f7aa`, il faut les renommer en ajoutant le suffixe `_2016`

## 43.1.0 [#1336](https://github.com/openfisca/openfisca-france/pull/1336)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2018.
* Zones impactées : `model/prelevements_obligatoires/`.
* Détails :
  - Affine et corrige [#1333](https://github.com/openfisca/openfisca-france/issues/1333) sur le PFU
  - Le PFU a été codé avant la publication du nouveau formulaire de l'IR et des règles précises concernant son application. Désormais, le formulaire est disponible et les règles connues, cette PR vient les corriger
  - Pour plus de détails voir [le descriptif](https://github.com/openfisca/openfisca-france/pull/1336) de la version

### 43.0.1 [#1342](https://github.com/openfisca/openfisca-france/pull/1342)

* Correction technique
* Périodes concernées : à partir du 01/01/2015.
* Zones impactées : `model/prelevements_obligatoires/impot_revenu/`.
* Détails :
  - Corrige des aspects non fonctionnels (factorisation du code) de la version 43.0.0
  - Ajoute des éléments documentaires (guide de migration) dans le descriptif de la version

# 43.0.0 [#1325](https://github.com/openfisca/openfisca-france/pull/1325)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2015.
* Zones impactées : `model/prelevements_obligatoires/impot_revenu/`.
* Détails :
  - Ajoute comme inputs variables les nouvelles cases de la déclaration IR 2018 liée à la réduction Pinel.
  - Renomme les anciennes inputs variables du même nom, selon la méthode habituelle
  - Mets à jour la formule de calcul de la réduction (introduction des investissements réalisés en 2018 et ajout du report des investissements 2017)
  - Factorise les formules de la réduction Pinel
  - Renomme le paramètre `seuil` en `plafond`
  - Ajoute 2 tests issus des résultats du [calculateur en ligne du site impots.gouv](https://www3.impots.gouv.fr/simulateur/calcul_impot/2019/index.htm)

## Guide de migration

- Si vous utilisiez les variables `f7ra`, `f7rb`, `f7rc`, `f7rd`, il faut les renommer en ajoutant le suffixe `_2015`
- Si vous utilisiez les variables `f7qt`, `f7qu`, `f7qr`, `f7qs` il faut les renommer en ajoutant le suffixe `_2012`

### 42.5.1 [#1334](https://github.com/openfisca/openfisca-france/pull/1334)

* Correction d'un crash.
* Périodes concernées : toutes.
* Zones impactées : `prestations/minima_sociaux/ada`.
* Détails :
  - Utilise numpy `not` à la place du `not` de Python qui ne gère pas les vecteurs

## 42.5.0 [#1326](https://github.com/openfisca/openfisca-france/pull/1326)

* Correction d'un calcul existant
* Périodes concernées : toutes.
* Zones impactées : `prestations/minima_sociaux/ass`.
* Détails :
  - Application de l’abattement sur les revenus de substitution pour l’allocation de solidarité spécifique (ASS).
  - Factorise le calcul de l’abattement des ressources pour les variables ass_base_ressources_individu et ass_base_ressources_conjoint.

## 42.4.0 [#1328](https://github.com/openfisca/openfisca-france/pull/1328)

* Revalorisation périodique.
* Périodes concernées :  à partir du 01/04/2019.
* Zones impactées : `parameters/prestations/minima_sociaux/ass/montant_plein`.
* Détails :
  - Revalorise le montant journalier de l’ASS au 1er avril 2019.

### 42.3.2 [#1327](https://github.com/openfisca/openfisca-france/pull/1327)

* Correction d'un crash.
* Périodes concernées : toutes.
* Zones impactées : `revenus/remplacement/rente_accident_travail`.
* Détails :
  - Corrige une erreur lors du calcul de la rente accident du travail pour les personnes de plus de 100 ans

### 42.3.1 [#1324](https://github.com/openfisca/openfisca-france/pull/1324)

* Évolution du système socio-fiscal
* Périodes concernées : 2018
* Zones impactées : `prelevements_obligatoires/impot_revenu/decote`
* Détails :
  - Met à jour la décote 2018

## 42.3.0 [#1322](https://github.com/openfisca/openfisca-france/pull/1322)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `model/patrimoine/livret_epargne_populaire.py`.
* Détails :
  - Ajoute l'éligibilité au Livret d'épargne populaire

## 42.2.0 [#1319](https://github.com/openfisca/openfisca-france/pull/1319)

* Revalorisation périodique.
* Périodes concernées : à partir du 01/04/2019.
* Zones impactées : `parameters/prestations/minima_sociaux/rsa/montant_de_base_du_rsa`.
* Détails :
  - Revalorise le montant de base du RSA au 1er avril 2019.

### 42.1.2 [#1317](https://github.com/openfisca/openfisca-france/pull/1317)

* Changement mineur.
* Détails :
  - Retire une référence inadaptée.
  - Corrige le label d'une variable.

### 42.1.1 [#1314](https://github.com/openfisca/openfisca-france/pull/1314)

* Évolution du système socio-fiscal
* Périodes concernées : 2018
* Zones impactées : `prelevements_obligatoires/impot_revenu`
* Détails :
  - Met à jour les barèmes de l'impôt sur les revenus 2018

## 42.1.0 [#1313](https://github.com/openfisca/openfisca-france/pull/1313)

* Amélioration technique.
* Détails :
  - Adapte les tests de France à l'utilisation de Pytest
  - Déclare le paquet compatible avec Core 34

### 42.0.3 [#1309](https://github.com/openfisca/openfisca-france/pull/1309)

* Mise à jour de dépendances
* Détails :
  - Met à jour `autopep8`
  - Déclare le paquet compatible avec Core 33

### 42.0.2 [#1307](https://github.com/openfisca/openfisca-france/pull/1307)

* Amélioration technique
* Périodes concernées : toutes.
* Détails :
  - Transforme les références aux rôles de la forme `famille.PARENT` en `Famille.PARENT`.
  - (Ces changements sont rétro-compatibles et n'exigent pas d'ajuster la version de Core requise par France)

### 42.0.1 [#1304](https://github.com/openfisca/openfisca-france/pull/1304)

* Changement mineur.
* Détails :
  - Exige `flake8 >= 3.7` (et pycodestyle transitivement; la double spécification était nécessaire avant la version 3.7 de flake8 mais ce n'est plus le cas)

# 42.0.0 [#1306](https://github.com/openfisca/openfisca-france/pull/1306)

* Évolution du système socio-fiscal **non rétrocompatible**
* Périodes concernées : toutes.
* Zones impactées :
    - `mesures`
    - `prelevements_obligatoires/isf`
    - `prelevements_obligatoires/prelevements_sociaux/contributions_sociales/capital`
* Objectif : cette version vise à fiabiliser le calcul de l'ISF (et à ajouter l'IFI) à partir de la variable `ass_isf` (appelée maintenant `assiette_isf_ifi`). Les variables en amont (utilisées pour le calcul de l'assiette) n'ont pas été modifiées. Les variables de réductions d'impôt (`isf_inv_pme`, `isf_org_int_gen`, `isf_org_int_gen`) n'ont également pas été modifiées.
* Détails :
  - Améliore le calcul du plafonnement de l'ISF
  - Ajoute le calcul de l'IFI
  - Renomme le dossier parameters `isf` en `isf_ifi`
  - Renomme `isf_imm_bati` par `isf_ifi_imm_bati`, `isf_imm_non_bati` par `isf_ifi_imm_non_bati`, `ass_isf` par `assiette_isf_ifi`, `isf_iai` par `isf_ifi_iai`, `isf_avant_reduction` par `isf_ifi_avant_reduction`, `isf_avant_plaf` par `isf_ifi_avant_plaf`, `tot_impot` par `total_impots_plafonnement_isf_ifi`, `revetproduits` par `revenus_et_produits_plafonnement_isf_ifi`, `decote_isf` par `decote_isf_ifi`, `isf_apres_plaf` par `isf_ifi_apres_plaf`, `isf_tot` par `isf_ifi`.
  - Point mineur : simplifie les variables relatives aux PEL-CEL.

### 41.2.1 [#1304](https://github.com/openfisca/openfisca-france/pull/1304)

* Simplification du code.
* Périodes concernées : depuis 2002.
* Zones impactées : `credits_impots`.
* Détails :
  - Factorise la formule générale des crédits d'impôt

## 41.2.0 [#1303](https://github.com/openfisca/openfisca-france/pull/1303)

* Amélioration de modélisation.
* Périodes concernées : toutes.
* Zones impactées :
   - `prestations/prestations_familiales/base_ressources`
   - `prestations/prestations_familiales/cf`
* Détails :
  - Injecte les revenus fiscaux non individualisables dans la base ressources du CF
  - Crée une variable `prestations_familiales_base_ressources_communes` pour mutualiser cette opération pour les différentes bases ressources des prestations familiales
  - Renomme `cf_ressources` par `cf_base_ressources` et `cf_ressources_individu` par `cf_base_ressources_individu`.

## 41.1.0 [#1302](https://github.com/openfisca/openfisca-france/pull/1302)

* Revalorisation périodique.
* Périodes concernées : à partir du 01/04/2019.
* Zones impactées :
  - `parameters/prestations/prestations_familiales/af`.
  - `parameters/cmu`.
  - `parameters/prestations/minima_sociaux/asi`.
* Détails :
  - Revalorise l'allocation familiale (AF) au 1er avril 2019 en métropole .
  - Revalorise l'aide CMU-c et ACS au 01 avril 2019 en métropole .
  - Revalorise l’allocation supplémentaire d’invalidité (ASI) au 1er avril 2019.

# 41.0.0 [#1261](https://github.com/openfisca/openfisca-france/pull/1261)

* Evolution technique **non rétrocompatible**
* Zones impactées : plusieurs (voir liste ci-dessous).
* Détails :
  - Supprime l'attribut base_function des variables `garde_alternee`, `age`, `age_en_mois`, `rsa_isolement_recent`, `contrat_de_travail_debut`, `contrat_de_travail_fin`, `salarie_regime_alsace_moselle`, `entreprise_creation`, `prevoyance_obligatoire_cadre_taux_employe`, `prevoyance_obligatoire_cadre_taux_employeur`, `livret_a`, `epargne_revenus_non_imposables`, `epargne_revenus_imposables`, `valeur_patrimoine_loue`, `valeur_immo_non_loue`, `valeur_terrains_non_loues`, `valeur_locative_terrains_non_loues`
  - Ajoute le comportement `set_input_dispatch_by_period` à ces variables le cas échéant
  - Adapte certains tests qui s'appuyaient sur ces inférences "magiques" pour les variables d'entrée.

## Guide de migration

- Si vous utilisez ces variables en entrée, vous devrez expliciter la période pour laquelle ces variables sont fournies, de sorte qu'elle recouvre toute la période de vos calculs (vous pouvez utiliser la [syntaxe des périodes multi-mois ou multi-années](https://openfisca.org/doc/coding-the-legislation/35_periods.html) pour gagner en concision)

# 40.0.0 [#1268](https://github.com/openfisca/openfisca-france/pull/1268)

* Amélioration technique **non rétrocompatible**
* Détails :
  - Met à jour Core à v.30 (pour plus de détails voir [le descriptif](https://github.com/openfisca/openfisca-france/pull/1268), et suivre le [guide de migration de Core](https://github.com/openfisca/openfisca-core/pull/817)).

### 39.0.2 [#1294](https://github.com/openfisca/openfisca-france/pull/1294)

* Amélioration technique
* Détails :
  - Met à jour yamllint, Pytest, autopep8
  - Supprime les dépendances du groupe "Barèmes IPP", obsolètes

### 39.0.1 [#1292](https://github.com/openfisca/openfisca-france/pull/1292)

* Amélioration technique
* Détails :
  - Met à jour l'outil de suivi du formatage Python

# 39.0.0 [#1293](https://github.com/openfisca/openfisca-france/pull/1293)

* Amélioration technique **non rétrocompatible**
* Détails :
  - Met à jour à la syntaxe Core v.29 (suivre le [guide de migration de Core](https://github.com/openfisca/openfisca-core/blob/232bca40e51c9eb5adaf030c70e0db362e84ec66/CHANGELOG.md#2900-843)).

### 38.1.1 [#1291](https://github.com/openfisca/openfisca-france/pull/1291)

* Changement mineur.
* Périodes concernées : toutes.
* Zones impactées : `prestations\minima_sociaux\ppa`.
* Détails :
  - Ajoute les rentes foncières à titre onéreux dans la base ressources de la PPA
  - Appelle dans les revenus du capital le douzième de l'année N-2, et pas le mois d'il y a deux ans.

## 38.1.0 [#1270](https://github.com/openfisca/openfisca-france/pull/1270)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées :
  - `revenus/remplacement/rente_accident_travail`.
  - `parameters/accident_travail/rente/*`.
* Détails :
  - Permet le calcul de `rente_accident_travail`.
  - Ajoute les variables:
    - `demande_rachat` (en entrée)
    - `pcrtp_nombre_actes_assistance` (en entrée)
    - `indemnite_accident_travail`
    - `pcrtp`
    - `rente_accident_travail_apres_rachat`
    - `rente_accident_travail_base`
    - `rente_accident_travail_exploitant_agricole`
    - `rente_accident_travail_rachat`
    - `rente_accident_travail_salaire_utile`
    - `rente_accident_travail_salarie`

# 38.0.0 [#1284](https://github.com/openfisca/openfisca-france/pull/1284)

* Évolution du système socio-fiscal **non rétrocompatible**
* Périodes concernées : à partir de 2017.
* Zones impactées : `prestations/minima_sociaux/rsa.py`.
* Détails :
  - Supprime `extra_param` du calcul du RSA. Le RSA est calculé au titre d'un mois donné (correspondant à l'argument `period`), en fonction des paramètres en vigueur durant ce mois-ci, et en fonction des ressources de `period.last_3_months`. On supprime la variable `rsa_fictif`, qui devient redondante.
  - Implique la suppression de la distinction des revenus d'activités moyennés et non-moyennés dans la base ressources : suppression des variables `indemnite_fin_contrat_net`, `primes_salaires_net` et `salaire_net_hors_revenus_exceptionnels`.
  - Autres variables impactées : `rsa_base_ressources`, `rsa_base_ressources_minima_sociaux`, `rsa_base_ressources_prestations_familiales`, `rsa_enfant_a_charge`, `rsa_revenu_activite_individu`, `rsa_montant`.

## Guide de migration

- Remplacer la variable `rsa` par `rsa_fictif`
- Remplacer `salaire_net_hors_revenus_exceptionnels` par `salaire_net`
- Utiliser les versions brutes de `indemnite_fin_contrat` et `primes_salaires` qui sont reflétées en net dans `salaire_imposable`

### 37.0.1 [#1289](https://github.com/openfisca/openfisca-france/pull/1289)

* Correction cosmétique de ce fichier (CHANGELOG.md)

# 37.0.0 [#1287](https://github.com/openfisca/openfisca-france/pull/1287)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2012
* Zones impactées : `openfisca_france/model/prelevements_obligatoires/impot_revenu`.
* Détails :
  - Crée une variable `f3sa` correspondant à la case 3SA réintroduite à partir de 2016
  - Renomme la variable `f3sa` (existant précédemment et correspondant à la case en 2012) en `f3sa_2012`

### 36.1.1 [#1286](https://github.com/openfisca/openfisca-france/pull/1286)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2015.
* Zones impactées : `prelevements_obligatoires/prelevements_sociaux/contributions_sociales/activite`.
* Détails :
  - Supprime la taxe exceptionnelle sur les hauts revenus à partir de 2015 (variable `tehr`), car taxation en vigueur seulement sur les revenus de 2013 et 2014.

## 36.1.0 [#1274](https://github.com/openfisca/openfisca-france/pull/1274)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées :
  - `model/prestations/minima_sociaux/aah`.
  - `parameters/prestations/minima_sociaux/aah/mva`.
  - `parameters/prestations/minima_sociaux/aah/taux_aah_hospitalise_ou_incarcere`.
  - `parameters/prestations/minima_sociaux/aah/taux_capacite_travail`.
  - `parameters/prestations/minima_sociaux/caah/garantie_ressources`.

* Détails :
  - Implémente des compléments à l'AAH :
    - le complément de ressources
    - la majoration pour vie autonome (MVA) a désormais une formule de calcul.
  - Applique un montant minimal de l'AAH en cas d'hospitalisation ou incarcération.
  - Ajoute les variables:
    - taux_capacite_travail
    - aah_date_debut_incarceration
    - aah_date_debut_hospitalisation
    - complement_ressources_aah
    - eligibilite_caah

# 36.0.0 [#1269](https://github.com/openfisca/openfisca-france/pull/1269)

* Évolution du système socio-fiscal **non rétro-compatible**.
* Périodes concernées : toutes.
* Zones impactées :
  - `prestations/aides_logement`.
* Informations de mise à niveau :
  - Cette évolution impacte le calcul des aides au logement pour les personnes au chômage. Si vous transmettez la valeur `chomeur` pour la variable `activite`, vous devez maintenant également transmettre `date_debut_chomage`, une condition de durée de chômage de deux mois ou plus étant désormais évaluée.
* Détails :
  - Ajoute la variable `date_debut_chomage`.
  - Corrige une double application des coefficients 'coloc' et 'chambre' dans aides_logement.
  - Corrige l'application de la règle des 2/3 du montant du loyer pour l'AL et l'APL.

## 35.1.0 [#1275](https://github.com/openfisca/openfisca-france/pull/1275)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/07/2012.
* Zones impactées :
  - `model/prestations/minima_sociaux/ass`.
  - `parameters/prestations/minima_sociaux/ass/montant_plein_mayotte`.
* Détails :
  - Applique le montant journalier de l'allocation de solidarité spécifique à Mayotte à compter du 1er juillet 2012.

# 35.0.0 [#1227](https://github.com/openfisca/openfisca-france/pull/1227)

* Amélioration technique **non rétro-compatible**.
* Détails:
  - Adapte à OpenFisca Core v26
  - Pour plus d'informations, voir le [Changelog de Core](https://github.com/openfisca/openfisca-core/blob/master/CHANGELOG.md#2600-790)

### 34.8.1 [#1272](https://github.com/openfisca/openfisca-france/pull/1272)

* Changement mineur.
* Périodes concernées : toutes.
* Zones impactées : `mesures.py`.
* Détails :
  - Tient compte de la CASA dans le calcul de `revenus_remplacement_pensions_bruts_menage`

## 34.8.0 [#1280](https://github.com/openfisca/openfisca-france/pull/1280)

* Revalorisation périodique
* Périodes concernées : à partir du 01/01/2019.
* Zones impactées : `parameters/prestations/minima_sociaux/aspa`.
* Détails :
  - Revalorise l'allocation de solidarité aux personnes âgées au 1er janvier 2019 et au 1er janvier 2020.

### 34.7.3 [#1276](https://github.com/openfisca/openfisca-france/pull/1276)

* Amélioration technique
* Périodes concernées : n/a
* Zones impactées : n/a
* Détails :
  - Supprime **__future__** imports, car trivials après l'arrêt du support Python2

### 34.7.2 [#1279](https://github.com/openfisca/openfisca-france/pull/1279)

* Changement mineur.
* Périodes concernées : à partir du 01/01/2018.
* Zones impactées :
  - `prelevements_obligatoires/impot_revenu/prelevements_forfaitaires/ir_prelevement_forfaitaire_unique`.
* Détails: Corrige l'application d'un abattement sur les produits d'assurance-vie.

### 34.7.1 [#1271](https://github.com/openfisca/openfisca-france/pull/1271)

* Correction d'un calcul existant
* Périodes concernées : à partir du 01/01/2012.
* Zones impactées : `prelevements_obligatoires/impot_revenu/(credits,reductions)_impot`.
* Détails :
  - Introduit les variables `reduction_cotisations_syndicales` et `credit_cotisations_syndicales`
  - Factorise le calcul de ces variables (portant le statut) via `cotsyn` (portant seulement le montant)

## 34.7.0 [#1273](https://github.com/openfisca/openfisca-france/pull/1273)
* Correction d'un crash.
* Périodes concernées : toutes.
* Zones impactées:
    - `prestations/minima_sociaux/rsa.py`
    - `mesures.py`
* Détails :
  - Actualise la formule de la variable `crds_mini`
  - Introduit `crds_mini` et `crds_pfam` dans la chaîne de calcul du revenu disponible

## 34.6.0 [#1258](https://github.com/openfisca/openfisca-france/pull/1258)

* Revalorisation périodique.
* Périodes concernées : à partir de janvier 2019.
* Zones impactées :
  - `prestations/cheque_energie.py`
  - `parameters/cheque_energie.yaml`
* Détails :
  - Met à jour le chèque énergie avec les nouveaux barèmes : les montants changent et il y a une nouvelle tranche de revenus.
  - Exige une version de Core supérieure à 25.3, permettant de reformuler le barème du Chèque Energie comme un SingleAmountTaxScale.

### 34.5.1 [#1267](https://github.com/openfisca/openfisca-france/pull/1267)

* Changement mineur.
* Détails :
  - Ajoute des références pour la prise en compte de l'ASF dans le RSA et la PPA
  - Ajoute des références pour la prise en compte du CF et des AL dans la PPA
  - (AL = Aides au Logement, CF = Complément Familial, ASF = Allocation de Soutien Familial)
  - (RSA = Revenu de Solidarité Active, PPA = Prime Pour l'Activité)

## 34.5.0 [#1248](https://github.com/openfisca/openfisca-france/pull/1248)

* Revalorisation périodique
* Périodes concernées : à partir du 01/01/2019.
* Zones impactées : `prestations/prestations_familiales/af/modulation`.
* Détails :
  - Revalorise les plafonds de ressources et la majoration du plafond par enfant dans le calcul de l'Allocation Familiale.
  - Introduit des paramètres plus proches des textes de loi, les anciens étant basés sur des circulaires.
  - Factorise du code répété vers des "helpers".

### 34.4.1 [#1265](https://github.com/openfisca/openfisca-france/pull/1265)

* Changement mineur.
* Détails :
  - Ajoute des références législatives à une variable de la prime d'activité

## 34.4.0 [#1264](https://github.com/openfisca/openfisca-france/pull/1264)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/11/2018.
* Zones impactées : `prestations/minima_sociaux/aah`
* Détails :
  - Diminue le plafond de ressources à 89% (au lieu de 100%) pour les bénéficiaires de l'allocation adulte handicapé en couple.

### 34.3.1 [#1263](https://github.com/openfisca/openfisca-france/pull/1263)

* Changement mineur
* Zones impactées :
   - `reductions_impot`.
* Détails :
  - Corrige une typo en plusieurs endroits.

## 34.3.0 [#1259](https://github.com/openfisca/openfisca-france/pull/1259)

* Revalorisation périodique
* Périodes concernées : à partir du 01/01/2019.
* Zones impactées :
   - `parameters/prestations/aides_logement`.
   - `parameters/prestations/reduction_loyer_solidarite`.
* Détails :
  - Revalorise les aides au logement au 1er janvier 2019 en métropole.

### 34.2.2 [#1262](https://github.com/openfisca/openfisca-france/pull/1262)

* Correction d'un crash.
* Zones impactées : `prestations/minima_sociaux/ppa.py`.
* Détails :
  - Répare la variable de la prime d'activité versée

### 34.2.1 [#1257](https://github.com/openfisca/openfisca-france/pull/1257)

* Revalorisation périodique
* Périodes concernées : à partir du 01/01/2019.
* Zones impactées :
  - `parameters/prestations/prestations_familiales/paje`.
  - `parameters/prestations/prestations_familiales/cf/majoration_plafond_biact_isole`.
* Détails :
  - Revalorise les plafonds de ressources et les montants de la PAJE en date du 01/01/2019.

## 34.2.0 [#1255](https://github.com/openfisca/openfisca-france/pull/1255)

* Revalorisation périodique
* Périodes concernées : à partir du 01/01/2019.
* Zones impactées : `prestations/prestations_familiales/cf`.
* Détails :
  - Prend en compte la revalorisation des plafonds de ressources et de la majoration du complément familial (CF) au 1er janvier 2019.

### 34.1.1 [#1253](https://github.com/openfisca/openfisca-france/pull/1253)

* Correction d'un crash.
* Périodes concernées : toutes.
* Zones impactées : `prestations/minima_sociaux/rsa`.
* Détails :
  - Gestion de la variable `rsa_eligibilite` pour la période du RMI qui a été endomagée lors de l'introduction du paramètre `rsa_jeune`.
  - Problème de type constaté lors de la mutiplication d'un scalaire égal à 1 avec des vecteurs numpy booléens révélé lors d'un usage au CASD (potentiellement dépendant du système d'exploiattion etc)


## 34.1.0 [#1243](https://github.com/openfisca/openfisca-france/pull/1243)

* Amélioration d'un calcul existant
* Périodes concernées : toutes pour la prime d'activité, ie. à partir de janvier 2016.
* Zones impactées : `prestations/minima_sociaux/ppa`.
* Détails :
  - Prise en compte des revenus du capital dans le calcul de la prime d'activité

# 34.0.0 [#1216](https://github.com/openfisca/openfisca-france/pull/1216)

* Changement majeur.
* Périodes concernées : toutes.
* Zones impactées:
  - `mesures.py`
  - `prelevements_obligatoires\impot_revenu\ir`
  - `prelevements_obligatoires\isf`
  - `prestations\aides_logement`
  - `prestations\prestations_familiales\base_ressource`
  - `prestations\minima_sociaux\ass`
  - `prestations\minima_sociaux\ppa`
  - `prestations\minima_sociaux\rsa`
  - `revenus\capital\foncier`
* Rend les variables de revenus fonciers plus explicites, et redéfinit les variables d'entrée de ces revenus afin d'en avoir une définition plus claire et moins de redondance.
* Détails :
  - Supprime la variable `fon`. A la place, on utilise `revenu_categoriel_foncier`.
  - Réécrit la formule de `revenu_categoriel_foncier`.
  - Enlève la formule qui était mise dans `f4ba`.
  - Définit `revenus_locatifs` via les cases de la déclaration fiscale.
  - Supprime `REV_TYP` et `REVENUES_CATEGORIES`

### 33.0.5 [#1252](https://github.com/openfisca/openfisca-france/pull/1252)

* Amélioration d'un calcul existant
* Périodes concernées : à partir du 01/01/2017.
* Zones impactées : `prestations/minima_sociaux/ass`.
* Détails :
  - Corrige la règle de non indemnisation devenue incorrecte suite à la prise en compte du cumul ASS et salaire

## 33.0.4 [#1249](https://github.com/openfisca/openfisca-france/pull/1249)

* Changement mineur.
* Périodes concernées : aucunes.
* Zones impactées : aucunes.
* Détails :
  - Correction de style induites par l'exécution de `make test`
  - Efface des scripts obsolètes concernant les barèmes IPP

### 33.0.3 [#1233](https://github.com/openfisca/openfisca-france/pull/1233)

* Changement mineur.
* Périodes concernées : toutes.
* Zones impactées : `prestations_sociales/aides_logement.py`.
* Détails :
  - Affine une condition concernant le loyer plafond dans le calcul de L .

### 33.0.2 [#1244](https://github.com/openfisca/openfisca-france/pull/1244)

* Changement mineur.
* Zones impactées : `prestations/minima_sociaux/ass`.
* Détails :
  - Ajoute des références pour l'allocation de solidarité spécifique

### 33.0.1 [#1246](https://github.com/openfisca/openfisca-france/pull/1246)

* Changement mineur
* Périodes concernées : toutes
* Zones impactées :
  - prelevements_obligatoires/prelevements_sociaux/contributions_sociales/versement_transport
* Détails :
  - Une valeur donnée pour le taux est transmise à toutes les sous-périodes (utilisation de set_input_dispatch_by_period)

# 33.0.0 [#1251](https://github.com/openfisca/openfisca-france/pull/1251)

* Changement majeur.
* Périodes concernées : toutes.
* Zones impactées :
  - `prelevements_obligatoires/impot_revenu/ir.py`
  - `prestations/minima_sociaux/aah.py`
* Détails :
  - Corrige le changement de version de la PR [#1250](https://github.com/openfisca/openfisca-france/pull/1250) qui est un changement majeur car suppression de variables.

### 32.4.2 [#1250](https://github.com/openfisca/openfisca-france/pull/1250)

* Changement mineur.
* Périodes concernées : toutes.
* Zones impactées :
  - `prelevements_obligatoires/impot_revenu/ir.py`
  - `prestations/minima_sociaux/aah.py`
* Détails :
  - Supprime les variables `revenu_activite`, `revenu_activite_salariee` et `revenu_activite_non_salariee` qui incorporaient juste `salaire_imposable` et `rpns_individu` et n'étaient utilisées que pour l'AAH.

## 32.4.1 [#1245](https://github.com/openfisca/openfisca-france/pull/1245)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/03/2017
* Zones impactées : `prelevements_sociaux/cotisations_sociales/fds/indice_majore_de_reference`.
* Détails :
  - Met à jour l'indice majoré de référence entrant en compte dans la cotisation FDS.

## 32.4.0 [#1247](https://github.com/openfisca/openfisca-france/pull/1247)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/10/2018.
* Zones impactées :
    - `parameters/prestations/minima_sociaux/ppa`
    - `parameters/cotsoc/gen`
* Détails :
  - Met à jour les paramètres suivants de la PPA suite à la revalorisation exceptionnelle de janvier 2019 :
    - `smic_h_b`
    - `taux_bonification_max`
    - `seuil_max_bonification`

### 32.3.1 [#1235](https://github.com/openfisca/openfisca-france/pull/1235)

* Corrections de tests ou de bugs.
* Périodes concernées : toutes.
* Zones impactées : `tests`.
* Détails :
  - Corrige un test RSA et un PPA en échec non signalés suite à openfisca/openfisca-core#781

## 32.3.0 [#1232](https://github.com/openfisca/openfisca-france/pull/1232)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes pour la PPA c'est à dire à partir du 01/10/2015.
* Zones impactées : `prestations/minima_sociaux/ppa`.
* Détails :
  - Fiabilise le calcul de la PPA en remplaçant par de nouvelles variables dont `ppa_mois_demande` le mécanisme précédent.

### 32.2.1 [#1230](https://github.com/openfisca/openfisca-france/pull/1230)

* Correction mineure.
* Périodes concernées : à partir du 01/08/2018
* Zones impactées :
  - `prestations/minima_sociaux/ppa`
* Détails :
  - Corrige la date d'effet de paramètres de la prime d'activité

## 32.2.0 [#1224](https://github.com/openfisca/openfisca-france/pull/1224)

* Amélioration technique.
* Détails:
  - Adapte à OpenFisca Core v25
  - Change la syntaxe des tests
  - Pour plus d'informations, voir le [Changelog de Core](https://github.com/openfisca/openfisca-core/blob/master/CHANGELOG.md#250-781)

### 32.1.0 [#1225](https://github.com/openfisca/openfisca-france/pull/1225)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2014 jusqu'au 01/01/2017.
* Zones impactées : `parameters/prestations/aides_logement`.
* Détails :
  - Ajout d'anciennes valeurs manquantes pour les paramètres de l'aide au logement

### 32.0.1 [#1217](https://github.com/openfisca/openfisca-france/pull/1217)

* Correction mineure.
* Périodes concernées : à partir du 01/01/2018
* Zones impactées :
  - `mesures.py`
  - `prestations/reduction_loyer_solidarite.py`
* Détails :
  - Ajoute la RLS au montant des prestations sociales
  - Ajoute une date d'effet à `reduction_loyer_solidarite` et la limite aux familles éligibles
  - Affine la condition d'éligibilité en écartant les logements-foyers
  - Met à jour les tests en ce sens

# 32.0.0 [#1223](https://github.com/openfisca/openfisca-france/pull/1223)

* Évolution de la législation **non rétrocompatible**
* Périodes concernées : toutes.
* Zones impactées : `prestations/aides_logement`.
* Détails :
  - Privilégie la notion de logement conventionné pour la détermination du secteur APL
  - Les clients qui s'appuient sur `locataire_hlm` doivent utiliser `logement_conventionne`

### 31.2.1 [#1222](https://github.com/openfisca/openfisca-france/pull/1222)

* Changement mineur.
* Zones impactées : `assets`, `cotisations_sociales`.
* Détails :
  - Supprime le fichier `holidays.py` qui contenait une liste de jours fériés français
  - Supprime le script de génération de ce fichier
  - Supprime l'usage, jamais testé, de ces jours fériés dans `coefficient_proratisation`

## 31.2.0 [#1219](https://github.com/openfisca/openfisca-france/pull/1219)

* Changement mineurs.
* Périodes concernées : toutes.
* Zones impactées :
  - prelevements_obligatoires/prelevements_sociaux/contributions_sociales/remplacement
  - prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/travail_totaux
  - revenus/activite/salarie
* Détails :
  - Corrige les employés de la fonction publique disposant d'un indice majorée
  - Corrige les employés de la fonction publique disposant d'une prime

## 31.1.0 [#1221](https://github.com/openfisca/openfisca-france/pull/1221)

* Amélioration technique.
* Périodes concernées : Avant 01/01/2018.
* Zones impactées : prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/travail_fonction_publique.
* Détails : Correction et clarification de la cotisation exceptionnelle de solidarité

# 31.0.0 [#1207](https://github.com/openfisca/openfisca-france/pull/1207)

* Évolution du système socio-fiscal **non rétrocompatible**
* Périodes concernées : toutes.
* Zones impactées:
  - `mesures.py`
  - `prelevements_obligatoires/prelevements_sociaux/contributions_sociales/csg_crds.py`
* Détails :
  - Ajoute des mesures de revenu super brut au niveau du ménage
  - Corrige le calcul de `minima_sociaux` (pour prendre en compte la CRDS sur ces revenus, comme c'est le cas pour `aides_logement` et `prestations_familiales`.
  - Corrige le calcul de la variable `csg` pour inclure la CSG sur les revenus non salariés
  - Modifie le calcul de la variable `revenus_nets_du_travail`
  - Renomme la variable `plus_values_revenus_nets_du_capital` en `plus_values_base_large`
 - Supprime les variables:
   - `niveau_de_vie_net`
   - `revenu_net`
   - `revenu_net_individu`

# 30.0.0 [#1199](https://github.com/openfisca/openfisca-france/pull/1199)

* Évolution de la législation **non rétrocompatible**
* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées :
  - `prestations/aides_logement`.

* Détails :
  - Ajoute le barème spécifique à certains publics "logements foyers".
  - Ajoute et renomme plusieurs variables liées aux aides au logement.
  - Ajoute des tests correspondants.
  - Supprime les variables:
    - `aide_logement_loyer_seuil_degressivite`
    - `aide_logement_loyer_seuil_suppression`
    - `aides_logement_primo_accedant`
    - `aides_logement_primo_accedant_loyer_minimal`
    - `aides_logement_primo_accedant_nb_part`
    - `als_etudiant`
    - `als_non_etudiant`

### 29.4.1 [#1215](https://github.com/openfisca/openfisca-france/pull/1215)

* Changement mineur.
* Périodes concernées : à partir de 2016.
* Zones impactées : `ir.py`.

* Détails :
  - Clarifie le statut de reduction_ss_condition_revenus
    - Cette réduction instaurée en 2016 vise à adoucir un effet de seuil d'assujettissement à l'impôt pour les foyers fiscaux les plus modestes, elle est plus à considérer comme une "décote bis" qu'une réduction fiscale.
  - Simplifie la formule ip_net qui n'a pas besoin d'être dupliquée, la formule de la réduction étant datée

### 29.4.0 [#1196](https://github.com/openfisca/openfisca-france/pull/1196)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `prestations/minima_sociaux/ass.py`.
* Détails :
  - Intègre pensions d'invalidité et revenus locatifs dans la base de ressources de l'ASS.
  - Ajoute un cas de test issu de Mes Aides.

### 29.3.14 [#1209](https://github.com/openfisca/openfisca-france/pull/1209)

* Changement mineur
* Périodes concernées : toutes.
* Zones impactées:
  - `revenus/capital/financier.py`
  - `prelevements_obligatoires/impot_revenu/ir.py`
* Détails :
  - Enlève la variable `avoirs_credits_fiscaux` des variables de mesure de revenus du capital
  - Renomme `avoirs_credits_fiscaux` en `credits_impot_sur_valeurs_etrangeres`
  - Déplace l'utilisation de cette variable directement dans `assiette_csg_revenus_capital`

### 29.3.13 [#1200](https://github.com/openfisca/openfisca-france/pull/1200)

* Changement mineur.
* Zones impactées : `model/mesures.py`.
* Détails :
  - Corrige le double compte de la CRDS logement dans `aides_logement`
  - Ajoute un test vérifiant l'égalité de `aides_logement` (annuelle) et `aide_logement` (mensuelle)

### 29.3.12 [#1212](https://github.com/openfisca/openfisca-france/pull/1212)

* Correction d'un crash.
* Zones impactées : `model/prestations/cheque_energie`.
* Détails :
  - Remplace l'utilisation de `a < b < x` par `(a < b) * (b < c)` car la première notion ne fonctionne pas avec des vecteurs `numpy`.

### 29.3.11 [#1182](https://github.com/openfisca/openfisca-france/pull/1182)

* Changement mineur.
* Périodes concernées : à partir du 01/10/2017
* Zones impactées : `parameters/cotsoc/pat/commun/assedic`.
* Détails :
  - Intègre la CET de 2017

### 29.3.10 [#1208](https://github.com/openfisca/openfisca-france/pull/1208)

* Changement mineur.
* Périodes concernées : toutes.
* Détails :
  - Actualise un plafond de ressources de l'ARS

### 29.3.9 [#1206](https://github.com/openfisca/openfisca-france/pull/1206)

* Changement mineur
* Périodes concernées : toutes.
* Zones impactées :
  - `prestations/prestations_familiales/base_ressource.py`
* Détails :
  - Corrige la biactivité dans les bases ressources des prestations sociales

### 29.3.8 [#1198](https://github.com/openfisca/openfisca-france/pull/1198)

* Amélioration technique | Ajout de tests
* Périodes concernées : toutes.
* Zones impactées :
  - `prelevements_obligatoires/impot_revenu/ir.py`
  - `prelevements_obligatoires/impot_revenu/reductions_impot.py`
  - `prelevements_obligatoires/impot_revenu/variables_reductions_credits.py`.
  - `tests/calculateur_impots`.
* Détails :
  - Ajout de tests concernant l'impôt sur le revenu.
  - Gestion des arrondis dans le calcul de l'impôt.

### 29.3.7 [#1195](https://github.com/openfisca/openfisca-france/pull/1195)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `prelevements_obligatoires/impot_revenu/reductions_impot.py`.
* Détails :
  - Unifie en une seule les formules datées de la variable `reductions`.

### 29.3.6 [#1107](https://github.com/openfisca/openfisca-france/pull/1107)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : certains barèmes dont les seuils sont en unité monétaire dans les paramètres de la législation.
* Détails :
  - Utilisation des champs `rate_unit` et `threshold_unit` dans les méta-données (champ `metadata`) des paramètres qui sont des barèmes.
  - Correction du script d'investigation des unités

### 29.2.6 [#1154](https://github.com/openfisca/openfisca-france/pull/1154)

* Changement mineur.
* Périodes concernées : toutes
* Zones impactées : `prestations/minima_sociaux/[rsa,ppa].py`.
* Détails :
  - Déprécie explicitement l'usage de extra_params dans France

### 29.2.5 [#1183](https://github.com/openfisca/openfisca-france/pull/1183)

* Changement mineur.
* Périodes concernées : toutes.
* Zones impactées : `asi_aspa`.
* Détails :
  - Corrige un commentaire avec une référence législative

### 29.2.4 [#1193](https://github.com/openfisca/openfisca-france/pull/1193)

* Amélioration de calculs existants.
* Périodes concernées : toutes.
* Zones impactées : `impot_revenu`.
* Détails :
  - Nouveaux cas de tests faisant apparaitre des divergences entre OpenFisca et le calculateur DGFIP.
  - Correctifs pour résoudre ces divergences.

### 29.2.3 [#1180](https://github.com/openfisca/openfisca-france/pull/1180)

* Amélioration technique
* Détails :
  - Permet d'utiliser `pytest` pour faire tourner les tests.
  - La librairie actuelle, `nose`, n'est plus en développement actif.

### 29.2.2 [#1166](https://github.com/openfisca/openfisca-france/pull/1166)

* Amélioration technique.
* Zones impactées : `prelevements_obligatoires/impot_revenu/ir.py`.
* Détails :
  - Fiabilise le calcul de l'âge en années et en mois

### 29.2.1 [#1178](https://github.com/openfisca/openfisca-france/pull/1178)

* Changement mineur
* Détails :
  - Lors de l'ajout d'un fichier statique requis pour le fonctionnement de la librairie, nous devons le rendre découvrable par `wheel`
  - Pour éviter des soucis involontaires de packaging, on _build_ désormais la librairie, et on exécute les tests contre la version qui sera mise à disposition des usagers

## 29.2.0 [#1189](https://github.com/openfisca/openfisca-france/pull/1189)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/11/2018.
* Zones impactées : `parameters/prestations/minima_sociaux/aah/montant`.
* Détails :
  - Prends en compte les revalorisations à venir de l'AAH

### 29.1.3 [#1162](https://github.com/openfisca/openfisca-france/pull/1162)

* Changement mineur.
* Zones impactées : `openfisca_france/parameters/**/*.yaml`.
* Détails :
  - Unifie les références législatives associées aux paramètres
    - Supprime les `reference: openfisca`
    - Modifie `reference: ipp` pour inclure l'URL des barèmes IPP

## 29.1.2 [#1194](https://github.com/openfisca/openfisca-france/pull/1194)

* Changement mineur.
* Périodes concernées : à partir du 01/04/2018.
* Zones impactées : `tests/formulas/asf*`.
* Détails :
  - Ajoute des tests pour la revalorisation de l'allocation de soutien familial (ASF) au 1er avril 2018.

## 29.1.1 [#1192](https://github.com/openfisca/openfisca-france/pull/1192)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/10/2018.
* Zones impactées : `parameters/prestations/minima_sociaux/ppa`.
* Détails :
  - Intègre la revalorisation exceptionnelle de la prime d'activité (+20 euros en octobre 2018)
  - Intègre la hausse du taux de dégressivité de la prime d'activité (octobre 2018)

### 29.0.1 [#1181](https://github.com/openfisca/openfisca-france/pull/1181)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `prestations_sociales/ass`.
* Détails :
  - Ajoute une condition d'âge sur l'ASS.
  - Ajoute un test.

# 29.0.0 [#1190](https://github.com/openfisca/openfisca-france/pull/1190)[#1191](https://github.com/openfisca/openfisca-france/pull/1191)

* Évolution de la législation **non rétrocompatible**
* Périodes concernées : à partir du 01/01/2013.
* Zones impactées :
  - `prestations/minima_sociaux`
  - `prestations/aides_logement`
  - `prestations/prestations_familiales/base_ressources`
  - `revenus/capital/plus_value`
  - `reforms/allocations_familiales_imposables`
  - `prelevements_obligatoires`
  - `mesures`

* Détails :
  - Supprime les variables:
    - `div`
    - `div_ms`
    - `f3vu`
  - Renomme les variables:
    - `rev_cat_rfon` en `revenu_categoriel_foncier`
    - `rev_cat_pv` en `revenu_categoriel_plus_values`
    - `rev_cat_tspr` en `revenu_categoriel_tspr`
    - `rev_cat_rvcm` en `revenu_categoriel_capital`
    - `rev_cat_rpns` en `revenu_categoriel_non_salarial`
    - `rev_cat` en `revenu_categoriel`
    - `abattement_net_duree_detention_retraite_dirigeant_pme` en `abattements_plus_values`
- Corrige la définition des plus-values prises en compte dans les minima sociaux.
  - Modifie le calcul des plus-values entrant dans le calcul du RFR à partir de 2018 (cf. variable `rfr_plus_values_hors_rni`)


### 28.0.1 [#1184](https://github.com/openfisca/openfisca-france/pull/1184)

* Changement mineur.
* Périodes concernées : à partir du 01/04/2018.
* Zones impactées : `tests/formulas/af_2018_04`.
* Détails :
  - Ajoute des tests pour la revalorisation des allocations familiales (AF) au 1er avril 2018.

# 28.0.0 [#1172](https://github.com/openfisca/openfisca-france/pull/1172)

* Changement majeur.
* Zones impactées :
  - `prestations/minima_sociaux/ass`
  - `prestations/minima_sociaux/rsa`
  - `tests/formulas/ass.yaml`
* Détails :
  - Passe à une définition de l'ASS au niveau "Individu" au lieu de "Famille"
  - Ajoute les revenus du capital au calcul de la base revenu de l'individu demandeur de l'ASS et de son conjoint éventuel
  - Ajoute un test d'un ménage avec individus tous deux éligibles à l'ASS.

### 27.1.1 [#1171](https://github.com/openfisca/openfisca-france/pull/1171)

* Changement mineur.
* Détails :
  - Ajoute des tests pour la revalorisation du complément familial (CF) au 1er avril 2018.

## 27.1.0 [#1152](https://github.com/openfisca/openfisca-france/pull/1152)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/07/2018
* Zones impactées : `openfisca_france/assets/versement_transport`.
* Détails :
  - Mise à jour des taux de versement transport conformément à [la circulaire du 31 mai 2018](https://www.urssaf.fr/portail/files/live/sites/urssaf/files/Lettres_circulaires/2018/ref_LCIRC-2018-0000018.pdf)

### 27.0.5 [#1173](https://github.com/openfisca/openfisca-france/pull/1173)

* Amélioration technique
* Détails :
  - Corrige et uniformise le style des fichiers

### 27.0.4 [#1176](https://github.com/openfisca/openfisca-france/pull/1176)

* Amélioration d'un calcul existant
* Périodes concernées : toutes
* Zones impactées : `prestations/minima_sociaux/rsa`.
* Détails :
  - Corrige un double compte de revenus du capital

### 27.0.3 [#1174](https://github.com/openfisca/openfisca-france/pull/1174) [#1170](https://github.com/openfisca/openfisca-france/pull/1170)

* Amélioration technique.
* Détails :
  - Dans la route `/spec` de la Web API:
    - Introduit un exemple de simulation à utiliser pour `/calculate` et `/trace`
    - Définit les exemples de variables et paramètres à utliser

### 27.0.1 [#1168](https://github.com/openfisca/openfisca-france/pull/1168)

* Changement mineur.
* Détails :
  - Ajout de tests pour l'ASI afin de vérifier que la formule prend bien en compte la dégressivité au delà d'un seuil.

# 27.0.0 [#1150](https://github.com/openfisca/openfisca-france/pull/1150)

* Évolution du système socio-fiscal **non rétro-compatible**
* Périodes concernées : toutes.
* Zones impactées :
- `prestations/minima_sociaux/cmu`.
- `prestations/minima_sociaux/rsa`.
- `revenus/autres`
* Détails :
  - Supprime la variable `allocation_aide_retour_emploi`, inutilisée

## 26.2.0 [#1149](https://github.com/openfisca/openfisca-france/pull/1149)

* Évolution du système socio-fiscal
* Périodes concernées : à partir du 01/01/2003.
* Zones impactées : `prestations/minima_sociaux/aefa`.
* Détails :
  - Fiabilise, unifie et simplifie le calcul de l'aide exceptionnelle de fin d'année.
  - Corrige le montant de base de l'AEFA de 125,45€ à 152,45€
  - Prolonge l'AEFA au-delà de 2015 car elle a été reconduite
  - N'applique la majoration familiale que pour les bénéficiaires du RSA

### 26.1.4 [#1151](https://github.com/openfisca/openfisca-france/pull/1151)

* Changement mineur.
* Périodes concernées : 2013
* Zones impactées : `tests/formulas/irpp.yaml`.
* Détails :
  - Ajoute des tests couvrant le calcul de la décote de l'IR en 2013

### 26.1.3 [#1155](https://github.com/openfisca/openfisca-france/pull/1155)

* Amélioration technique.
* Détails :
  - Correction de scripts qui ne marchaient plus.
  - Documentation de scripts.
  - Suppression de scripts.

### 26.1.2 [#1159](https://github.com/openfisca/openfisca-france/pull/1159) [#1158](https://github.com/openfisca/openfisca-france/pull/1158)

* Évolution du système socio-fiscal
* Périodes concernées : toutes
* Zones impactées:
  - `prestations/minima_sociaux/aah`
* Détails :
  - Ajoute la variable plafond de ressources pour l'AAH

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/travail_prive.py`.
* Détails :
  - Extrait par factorisation une nouvelle variable `quotite_de_travail`.
  - Assied le calcul de `agirc_gmp_[employeur,salarie]` et `plafond_securite_sociale` sur la quotité.


> Les versions `26.0.1`, `26.1.0` et `26.1.1` ont été dépubliées, car basée sur une version de Core depuis dépubliée. Merci d'utiliser la version `26.1.2` (ou plus récente).


# 26.0.0 [#1157](https://github.com/openfisca/openfisca-france/pull/1157)

* Évolution du système socio-fiscal **non rétro-compatibles**
* Périodes concernées : toutes
* Zones impactées:
- `model/prestations/minima_sociaux/aah`
* Détails :
  - Fiabilise l'évaluation de l'AAH
    - Prise en compte particulière des revenus d'activité en milieu ordinaire
    - Prise en compte de la Réduction Substantielle et Durable d'Accès à l'Emploi
  - Renomme aah_base_ressources_eval_trimestrielle en aah_base_ressources_activite_eval_trimestrielle
  - Supprime la variable aah_non_calculable

# 25.0.0 [#1156](https://github.com/openfisca/openfisca-france/pull/1156)

* Évolution du système socio-fiscal **non rétro-compatibles**
* Périodes concernées : toutes
* Zones impactées:
- `model/mesures`
- `model/prelevements_obligatoires/taxe_habitation`
- `model/prestations/minima_sociaux/aah`
- `model/prestations/minima_sociaux/asi_aspa`
- `model/prestations/minima_sociaux/cmu`
- `model/prestations/minima_sociaux/ppa`
- `model/prestations/minima_sociaux/rsa`
- `tests/**/*`
* Détails :
  - Déplace la variable ASI de la famille vers l'individu

### 24.14.9 [#1153](https://github.com/openfisca/openfisca-france/pull/1153)

* Amélioration technique
* Détails :
  - Corrige et uniformise le style des fichiers

### 24.14.8 [#1148](https://github.com/openfisca/openfisca-france/pull/1148)

* Changement mineur
* Périodes concernées : à partir du 01/01/1943
* Zones impactées:
- `openfisca_france/model/prelevements_obligatoires/prelevements_sociaux/taxes_salaires_main_oeuvre.py`
- `openfisca_france/parameters/cotsoc/pat/commun/construction_node/seuil.yaml`
* Détails :
  - Extrait vers un paramètre le nombre de salariés au-delà duquel le prélèvement s'applique.

### 24.14.7 [#1147](https://github.com/openfisca/openfisca-france/pull/1147)

* Amélioration technique
* Détails :
  - Corrige et uniformise le style des fichiers
  - Règle W504 : saut de ligne avant opérateur binaire

### 24.14.6 [#1146](https://github.com/openfisca/openfisca-france/pull/1146)

* Amélioration technique
* Détails :
  - Corrige et uniformise le style des fichiers
  - Règle W504 : saut de ligne avant opérateur binaire

### 24.14.5 [#1145](https://github.com/openfisca/openfisca-france/pull/1145)

* Amélioration technique
* Détails :
  - Corrige et uniformise le style des fichiers
  - Règle W504 : saut de ligne avant opérateur binaire

### 24.14.4 [#1144](https://github.com/openfisca/openfisca-france/pull/1144)

* Amélioration technique
* Détails :
  - Corrige et uniformise le style des fichiers

### 24.14.3 [#1142](https://github.com/openfisca/openfisca-france/pull/1142)

* Amélioration technique
* Détails :
  - Corrige et uniformise le style des fichiers

### 24.14.2 [#1143](https://github.com/openfisca/openfisca-france/pull/1143)

* Amélioration technique
* Détails :
  - Corrige et uniformise le style des fichiers

### 24.14.1 [#1139](https://github.com/openfisca/openfisca-france/pull/1139)

* Amélioration technique
* Détails :
  - Corrige et uniformise le style des fichiers

## 24.14.0

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2018.
* Zones impactées : prestations/reduction_loyer_solidarite.
* Détails :
  - Corrige la prise en compte des ressources dans le calcul de la RLS
  - Un nouveau cas de test était en erreur suite à l'utilisation de ressources recombinée en annuel comparées à un plafond mensuel.

## 24.13.0 [#1138](https://github.com/openfisca/openfisca-france/pull/1138)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées :
  - `model\prestations\aides_logement`
* Détails :
  - Suppression des aides au logement dans le cadre de l'accession à la propriété, sauf exception.
  - Ajout des variables:
   - `TypeEtatLogement`
   - `etat_logement`
   - `aide_logement_date_pret_conventionne`
   - `aides_logement_primo_accedant_eligibilite`

### 24.12.3 [#1137](https://github.com/openfisca/openfisca-france/pull/1137)

* Changement mineur.
* Périodes concernées : n/a
* Zones impactées : n/a
* Détails :
  - Supprime le fichier `openfisca-run-test` à la racine

### 24.12.2 [#1135](https://github.com/openfisca/openfisca-france/pull/1135)

* Changement mineur.
* Zones impactées : `.circleci`.
* Détails :
  - Lint des test YAML en incrémental (`yamllint`).
  - Lint des fichiers Python en incrémental (`flake8`).

### 24.12.1 [#1043](https://github.com/openfisca/openfisca-france/pull/1043)

* Changement mineur.
* Zones impactées : `openfisca_france/parameters/prestations/prestations_familiales/af/bmaf.yaml`
* Détails :
  - Correction du calcul de l'ASF, en cas de pension alimentaire.
  - Prise en compte de la revalorisation 2018.

## 24.12.0 [#1047](https://github.com/openfisca/openfisca-france/pull/1047)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées :
  - `model\prestations\minima_sociaux\ppa`
* Détails :
  - Correction de la formule de calcul du forfait logement en fonction du nombre de personnes au foyer.
  - Correction des tests de revalorisation de la prime d'activité.

### 24.11.2 [#1132](https://github.com/openfisca/openfisca-france/pull/1132)

* Changement mineur.
* Zones impactées : `__init__.py`.
* Détails :
  - Efface __init.py__ de la racine.

### 24.11.1 [#1110](https://github.com/openfisca/openfisca-france/pull/1110)

* Correction d'un bug.
* Périodes concernées : à partir du 01/01/2004.
* Zones impactées :
  - `prestations/prestations_familiales/paje`
* Détails :
  - Corrige le calcul de la PAJE lorsqu'on l'évalue pour un vecteur de familles.
  - Simplifie et uniformise la formule de calcul pour toutes les périodes.

##  24.11.0 [#1049](https://github.com/openfisca/openfisca-france/pull/1098)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2018.
* Zones impactées :
  - `prestations/minima_sociaux/rsa`
  - `parameters/prestations/prestations_familiales/af/bmaf`
  - `parameters/prestations/minima_sociaux/rsa/age_min_rsa_jeune`
  - `parameters/prestations/minima_sociaux/rsa/age_max_rsa_jeune`
  - `parameters/prestations/minima_sociaux/rsa/rsa_jeune`
* Détails :
  - Fiabilisation du calcul du revenu de solidarité active (RSA) au 1er avril 2018.
    A partir du 1er janvier 2017, Le rsa_forfait_logement et le rsa_base_ressources sont prises en compte sur le mois_courant (et pas sur le mois_demande), car les prestations sont prises en compte sur les 3 derniers mois précédant l'examen ou le réexamen périodique du droit au RSA.

## 24.10.0 [#994](https://github.com/openfisca/openfisca-france/pull/994)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/04/2018.
* Zones impactées :
  - `parameters/prestations/prestations_familiales/af`
  - `parameters/prestations/prestations_familiales/paje`
* Détails :
  - Revalorise les plafonds de ressources et les montants de la PAJE en date du 01/04/2018.

## 24.9.0 [#1111](https://github.com/openfisca/openfisca-france/pull/1111)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées :
  - `prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/travail_non_salarie`
  - `mesures`
* Détails :
  - Ajout sommaire des contributions et cotisations sociales des non salariés artisan, commeçcant ou profession libérale
  - Ajout des variables
    - `assiette_csg_crds_non_salarie`
    - `categorie_non_salarie`
    - `crds_non_salarie`
    - `csg_non_salarie`
    - `famille_independant`
    - `formation_artisan_commercant`
    - `formation_profession_liberale`
    - `maladie_maternite_artisan_commercant`
    - `maladie_maternite_profession_liberale`
    - `retraite_complementaire_artisan_commercant`
    - `vieillesse_artisan_commercant`
    - `vieillesse_profession_liberale`

## 24.8.0 [#1082](https://github.com/openfisca/openfisca-france/pull/1082)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/10/2017.
* Zones impactées : `parameters/prestations/aides_logement`.
* Détails :
  - Mise à jour des paramètres utilisés dans le calcul de l'aide au logement.
  - Correction mineure pour éviter un montant d'aide au logement négatif.

### 24.7.2 [#1104](https://github.com/openfisca/openfisca-france/pull/#1104)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `revenus/activite/salarie.py`.
* Détails :
  - Fixe l'attribut set_input = set_input_divide_by_period pour les variables `supplement_familial_traitement` et `indemnite_residence`
  - Efface les options `ADD` superflues lors du calcul de `salaire_super_brut_hors_allegements`

### 24.7.1 [#1105](https://github.com/openfisca/openfisca-france/pull/1105)

* Changement mineur.
* Périodes concernées : toutes.
* Zones impactées : `model/prestations/minima_sociaux/asi_aspa`.
* Détails :
  - Suppression de `revenus_fonciers_minima_sociaux`

## 24.7.0 [#1070](https://github.com/openfisca/openfisca-france/pull/1070)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées :
  - `revenus/remplacement/rente_accident_travail`
  - `prestations/minima_sociaux/cmu`
* Détails :
  - Intégration de la ressource rente d'accident du travail dans le calcul des aides en santé CMU-c et ACS.

##  24.6.0 [#1101](https://github.com/openfisca/openfisca-france/pull/1101)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `prelevements_obligatoires/prelevements_sociaux/contributions_sociales/remplacement`.
* Détails :
  - Ajoute une formule pour calculer les taux de CSG sur les revenus de remplacement
  - Ré-ajoute `invrev` qui avait été malencontreusement retirée dans le passé
  - Coorige à la marge dans le passé la durée de validité de certains paramètres

###  24.5.4 [#1103](https://github.com/openfisca/openfisca-france/pull/1103)

* Changement mineur.
* Périodes concernées : à partir du 01/04/2018.
* Zones impactées : `tests/formulas/aspa`.
* Détails :
  - Ajoute des tests pour la revalorisation de l'ASPA (voir [#1066](https://github.com/openfisca/openfisca-france/pull/1066))

###  24.5.3 [#1097](https://github.com/openfisca/openfisca-france/pull/1097)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2014.
* Zones impactées :
  - `prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/travail_fonction_publique`.
  - `prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/travail_prive`.

* Détails :
  - Fin de la cotisation exceptionnelle au fonds de solidarité en 2018.
  - Mise à jour taux de cotisation CNRACL depuis 2014.
  - Mise à jour taux de cotisation FEH depuis 2017.
  - Mise à jour assiette AGFF depuis 2016.
  - Correction taux assurance maladie collectivités locales depuis 2018
  - Correction taux de cotisation au fonds de pension de l'Etat depuis 2014
  - Mise à jour barèmes taxes sur les salaires depuis 2017
  - Mise à jour allègement Fillon pour 2018
  - Mise à jour des paramètres du seuil d'assujettissement au FDS depuis 2016

###  24.5.2 [#1094](https://github.com/openfisca/openfisca-france/pull/1094)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2018.
* Zones impactées : `prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/travail_prive`.
* Détails :
  - Mise à jour des paramètres de la garantie minimale de points de l'AGIRC (GMP)

###  24.5.1 [#1093](https://github.com/openfisca/openfisca-france/pull/1093)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2018.
* Zones impactées : `prelevements_obligatoires/prelevements_sociaux/contributions_sociales/remplacement`.
* Détails :
  - Mise à jour du taux de CSG déductible sur les retraites

## 24.5.0 [#1075](https://github.com/openfisca/openfisca-france/pull/1075)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes
* Zones impactées:
   - `model/mesures`
   - `model/prelevements_obligatoires/impot_revenu/credits_impot`
   - `model/prelevements_obligatoires/impot_revenu/ir`
   - `model/prelevements_obligatoires/prelevement_forfaitaire_liberatoire` : déplacé dans
     `model/prelevements_obligatoires/impot_revenu/prelevements_forfaitaires/prelevement_forfaitaire_liberatoire`
   - `model/prelevements_obligatoires/impot_revenu/prelevements_forfaitaires/__init__` (création)
   - `model/prelevements_obligatoires/impot_revenu/prelevements_forfaitaires/variables_communes` (création)
   - `model/prelevements_obligatoires/impot_revenu/prelevements_forfaitaires/ir_prelevement_forfaitaire_unique` (création)
   - `model/prelevements_obligatoires/isf`
   - `model/prelevements_obligatoires/prelevements_obligatoires/prelevements_sociaux/contributions_sociales/capital`
   - `model/prestations/aides_logement`
   - `model/prestations/prestations_familiales/base_ressource`
   - `model/revenus/capital/financier`
   - `model/revenus/capital/plus_value`
   - `reforms/allocations_familiales_imposables`
   - `reforms/landais_piketty_saez`
* Détails :
  - Code le prélèvement forfaitaire unique (PFU) instauré dans la loi de finances 2018.
    Cette "flat tax" à 30 % se décompose en :
      - Une hausse des prélèvements sociaux (17,2%)
      - Un prélèvement forfaitaire au titre de l'impôt sur le revenu (12,8%). Pour coder cette partie, création d'une nouvelle variable d'impôt `prelevement_forfaitaire_unique_ir`, calculée dans `model/prelevements_obligatoires/impot_revenu/prelevements_forfaitaires/ir_prelevement_forfaitaire_unique`.
      Pour cela :
          - Redéfinition ou création des variables d'assurance-vie et des variables d'épargne logement (PEL, CEL) pour s'adapter aux nouvelles assiettes
          - Définition de nouvelles assiettes `revenus_capitaux_prelevement_forfaitaire_unique_ir` et `plus_values_prelevement_forfaitaire_unique_ir`, en remplacement des anciennes variables d'assiettes injectées dans les différents dispositifs et bases ressources (`revenus_capitaux_prelevement_bareme`, `revenus_capitaux_prelevement_liberatoire`, `rev_cat_rvcm`, `rev_cat_pv`, `rfr_rvcm`, etc.).
          - Ensemble des variables neutralisées à partir de 2018 : `rev_cat_pv` `rev_cat_rvcm` `rfr_rvcm` `tax_rvcm_forfaitaire` `taxation_plus_values_hors_bareme`,
          `revenus_capitaux_prelevement_bareme`, `revenus_capitaux_prelevement_liberatoire`, `prelevement_forfaitaire_liberatoire`,
          , `f2ch`, `f2ts`, `prlire`,
          `acompte_ir_elus_locaux`, `prelevement_forfaitaire_non_liberatoire`, `acomptes_ir`, variables commençant par `assurance_vie_pl_non_anonyme`, `assurance_vie_pl_anonyme`.
  - Note : pour les revenus 2018, on ne dispose pas du formulaire de déclaration des revenus.
    Hypothèse : la structure des cases du formulaire 2042 et 2042C est identique entre 2018 et 2019 (i.e. entre les revenus 2017 et 2018). Les assiettes du PFU sont donc définies avec les cases des formulaires de l'IR 2018 sur revenus 2017. Et on neutralise les variables d'acomptes d'impôt.
  - Changements mineurs concernant les années antérieures à 2018 :
      - Actualise certaines variables fiscales pour 2017 : cases 2TT, 2TU et 2TV, variable `rev_cat_pv`.
      - Renomme `rfr_plus_values` en `rfr_plus_values_hors_rni`.
      - Renomme `rfr_rvcm` par `rfr_rvcm_abattements_a_reintegrer`

## 24.4.0 [#1081](https://github.com/openfisca/openfisca-france/pull/1081)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/travail_prive`.
* Détails :
  - Corrige le calcul de la cotisation  agirc gmp

##  24.3.0 [#1092](https://github.com/openfisca/openfisca-france/pull/1092)

* Évolution du système socio-fiscal
* Périodes concernées : à partir du 01/10/2018
* Zones impactées : prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/travail_prive
* Détails :
  - Annule la cotisation chomage à partir du 01/10/2018

### 24.2.1 [#1090](https://github.com/openfisca/openfisca-france/pull/1090)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2018.
* Zones impactées : prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/travail_prive.
* Détails :
  - Corrige la cotisation patronale maladie (mmida) à partir de 2018.
  - Annule la cotisation salariale maladie (mmid) à partir de 2018.

## 24.2.0

* Il n'y a pas de version 24.2.0

### 24.1.1 [#1085](https://github.com/openfisca/openfisca-france/pull/1085)

* Changement mineur.
* Détails :
  - Normalisation manuelle des fichiers de test en YAML

## 24.1.0 [#1079](https://github.com/openfisca/openfisca-france/pull/1079)

* Changement mineur.
* Périodes concernées : toutes.
* Zones impactées : model/base/TAUX_DE_PRIME, revenus/activite/salarie.
* Détails :
  - Corrige le type des salariés éligibles à l'indemnité de résidence
  - Modifie le taux moyen de primes dans la fonction publique pour qu'il soit égal à 19,5 % au lieu de 25 %

# 24.0.0 [#1062](https://github.com/openfisca/openfisca-france/pull/1062)

* Amélioration technique **non rétro-compatibles**.
* Détails :
  - Aucun impact pour les **clients** de l'API.
  - Rend optionnelle l'installation de la Web API
    - `pip install OpenFisca-France` n'installera _plus_ l'API.
    - `pip install openfisca-france && pip install openfisca-core[web-api]` permet d'inclure l'API.
  - Sert l'API Web sur le port 5000 par défault (à la place de 6000, considéré non-sûr)
  - Renomme le groupe des dépendances optionnelles de développement:
    - `pip install --editable .[dev]` permet de les installer (à la place de of `pip install --editable .[test]`).

### 23.1.1 [#1077](https://github.com/openfisca/openfisca-france/pull/1077)

* Correction d'un crash
* Périodes concernées : toutes
* Zones impactées:
  - `prestations/minima_sociaux/rsa`
  - `prestations/minima_sociaux/asi_aspa`
  - `model/revenus/capital/financier`
* Détails :
  - Supprime les doubles comptes de certains revenus du capital dans les bases ressources du RSA et de l'ASI-ASPA
  - Exemple : les revenus de `f2ee` étaient injectés deux fois via `rsa_base_ressources_patrimoine_individu` et via les variables `revenus_capitaux_prelevement_bareme` et `revenus_capitaux_prelevement_liberatoire`

## 23.1.0 [#1058](https://github.com/openfisca/openfisca-france/pull/1058)

* Évolution du système socio-fiscal.
* Zones impactées :
  - `model\prestations\aides_logement`
  - `parameters\prestations\reduction_loyer_solidarite`
* Détails :
  - Integration de la réduction du loyer de solidarité dans la formule de calcul de l'APL.

# 23.0.0 [#1069](https://github.com/openfisca/openfisca-france/pull/1069)

* Changement majeur
* Détails :
  - Supprime deux paramètres obsolètes :
    - `prestations.minima_sociaux.rmi.RMI_fixe`
    - `prestations.minima_sociaux.rsa.RMI_fixe`

## 22.9.0 [#1066](https://github.com/openfisca/openfisca-france/pull/1066)

* Évolution du système socio-fiscal | Changements mineurs
* Périodes concernées : à partir du 01/04/2018 essentiellement
* Zones impactées : `openfisca_france/parameters/prestations/minima_sociaux`.
* Détails :
   - Mise à jour des paramètres de l'ADA, de l'ASI et de l'ASPA
   - Suppression de `openfisca_france/parameters/prestations/minima_sociaux/aspa/personnes_seules.yaml`
     (car inutilisé et redondant avec `openfisca_france/parameters/prestations/minima_sociaux/aspa/plafond_ressources_seul.yaml`)

## 22.8.0 [#1065](https://github.com/openfisca/openfisca-france/pull/1065)

* Evolution du système socio-fiscal
* Périodes concernées : toutes
* Zones impactées :
  - `openfisca_france/model/prelevements_obligatoires/impot_revenu/ir`
  - `openfisca_france/model/prelevements_obligatoires/impot_revenu/plus_values_immobilieres`
  - `openfisca_france/model/prelevements_obligatoires/prelevement_forfaitaire_liberatoire` (nouveau fichier)
  - `openfisca_france/model/prelevements_obligatoires/prelevements_sociaux/contributions_sociales/capital`
  - `openfisca_france/model/revenus/capital/financier`
  - `openfisca_france/model/revenus/capital/plus_value`
  - `openfisca_france/model/prelevements_obligatoires/impot_revenu/credits_impot`
  - `openfisca_france/model/mesures`
* Détails :
  - Recodage du prélèvement forfaitaire libératoire (PFL), pour les revenus du 01/01/2013 au 31/12/2017 : suppression de la variable `imp_lib` et remplaceent par la variable `prelevement_forfaitaire_liberatoire` (créée dans un nouveau fichier).
  - Recodage des prélèvements sociaux sur les revenus du capital, pour les revenus du 01/01/2013 au 31/12/2017 : changement du calcul, de la structure, et des noms de variables associées à ces prélèvements.
  - Définition de la notion d'acomptes sur IR (`acomptes_ir`) et distinction d'une notion adminitrative (`irpp`, identique à auparavant) et d'une notion économique de l'IR (`irpp_eco`)
  - Corrections mineures :
     - Correction de la CSG déductible du RBG pour le calcul de l'IR : la variable `csg_deduc` prenait en compte seulement la case 6DE, et non pas les revenus de la case 2BH.
     - Renommage de `csg_deduc` par `csg_patrimoine_deductible_ir`.
     - Renommage de `plus_values` par `taxation_plus_values_hors_bareme`
     - Regroupe les variables `abattement_net_retraite_dirigeant_pme` et `abattement_net_duree_detention` en `abattement_net_duree_detention_retraite_dirigeant_pme`
     - Nettoyage du fichier `openfisca_france/model/mesures` :
        - Inclusion des acomptes de l'IR dans la variable `impots_directs`
        - Déplacement de `prelevement_forfaitaire_liberatoire` de `revenus_nets_du_capital` à `impots_directs`
        - Suppression et renommage de variables
        - Inclusion de l'impôt sur les plus-values immobilières (`ir_pv_immo`) dans `impots_directs`
        - Suppression de `rac` de la variable `revenus_nets_du_capital` (car déjà compté dans `rpns`)

### 22.7.1 [#1022](https://github.com/openfisca/openfisca-france/pull/1022)

* Changement mineur
* Détails :
  - Renseigne les unités manquantes dans les paramètres législatifs

## 22.7.0 [#992](https://github.com/openfisca/openfisca-france/pull/992)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/04/2018.
* Zones impactées :
  - `prestations/minima_sociaux/cmu`
  - `parameters/cmu`
  - `prestations/minima_sociaux/rsa`
  - `prestations/minima_sociaux/aah`
* Détails :
  - Revalorise les plafonds de ressources pour bénéficier des aides CMU-c et ACS en date du 01/04/2018.
  - Fiabilise le calcul de la CMUc-ACS en complétant les ressources prises en compte
  - Complete le calcul du CAAH avec la MVA

### 22.6.1 [#998](https://github.com/openfisca/openfisca-france/pull/1053)

* Amélioration technique.
* Détails :
  - Compatibilité python2 et python3

## 22.6.0 [#1064](https://github.com/openfisca/openfisca-france/pull/1064)

* Évolution du système socio-fiscal | Changements mineurs
* Périodes concernées : toutes.
* Zones impactées : openfisca_france/model/prelevements_obligatoires/impot_revenu/charges_deductibles.
* Détails :
  - Corrige une erreur dans le calcul du revenu fiscal de référence à propos des charges déductibles

## 22.5.0 [#1040](https://github.com/openfisca/openfisca-france/pull/1040)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2013.
* Zones impactées :
  - `model/prelevements_obligatoires/impot_revenu/ir`
* Détails :
  - Ajoute une variable "depcom_foyer" donnant le lieu de résidence fiscale du foyer.
  - Utilise cette variable pour calculer l'abattement d'impôt spécial DOM
  - Ajoute des tests correspondants

## 22.4.0 [#1059](https://github.com/openfisca/openfisca-france/pull/1059)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2017
* Zones impactées : openfisca_france/parameters/impot_revenu/bareme.yaml
* Détails :
  - Mets à jour le barème de l'impôt pour les revenus 2017

## 22.3.0 [#998](https://github.com/openfisca/openfisca-france/pull/998)

* Évolution du système socio-fiscal.
* Zones impactées :
  - `prestations/reduction_loyer_solidarite`
* Détails :
  - Ajoute le calcul de la réduction du loyer de solidarité.

### 22.2.2 [#1039](https://github.com/openfisca/openfisca-france/pull/1039)

* Amélioration technique.
* Détails :
  - Ajout d'un linter pour les fichiers YAML
  - Validation en CI du format des fichiers YAML

### 22.2.1 [#1038](https://github.com/openfisca/openfisca-france/pull/1038)

* Correction d'un crash
* Zones impactées :
  - `prelevements_obligatoires/impot_revenu/reductions_impot`
  - `prestations/anah/eligibilite_anah`
* Détails :
  - Corrige la formule de `locmeu` (Réduction d'impôt en faveur de l'acquisition de logements destinés à la location meublée non professionnelle), qui crashait pour 2017.
  - Corrige la formule de `eligibilite_anah`, qui crashait pour les départements de Corse.
  - Corrige la configuration des tests pour qu'ils soient tous executés:
    - Corrige les appels `circleci tests glob` pour que `**` soit récursif.

## 22.2.0 [#1034](https://github.com/openfisca/openfisca-france/pull/1034)

* Évolution du système socio-fiscal.
* Zones impactées :
  - `prelevements_obligatoires/impot_revenu/ir`
  - `revenus/capital/financier`
  - `revenus/capital/plus_value`
* Détails :
  - Mise à jour de la taxation des revenus du capital dans l'IRPP
  - Ajout de nouvelles cases de l'impôt (2013-2017) relatives aux plus-values ou aux revenus financiers
  - Réorganise le fichier plus_value.py afin de le rendre plus lisible
  - Corrige le calcul du RFR (afin de prendre en compte les revenus financiers et les plus-values qui sont éxonérés ou imposés forfaitairement)
  - Corrige et mets à jour le calcul des revenus des capitaux et valeurs mobilières (RVCM) et plus-value taxés au barème, et de ceux taxés forfaitairement
  - Déplace des variables de revenus qui étaient dans le fichier de calcul de l'IR

## 22.1.0 [#1037](https://github.com/openfisca/openfisca-france/pull/1037)

* Amélioration technique
* Détails :
  - Création d'une réforme qui adapte la législation pour les simulateurs

### 22.0.1 [#1036](https://github.com/openfisca/openfisca-france/pull/1036)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2017.
* Zones impactées :
  - `prestations/logement_social`
* Détails :
  - Fait commencer la variable `logement_social_eligible` au 01/01/2017

# 22.0.0 [#1026](https://github.com/openfisca/openfisca-france/pull/1026)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées :
  - `prestations/minima_sociaux/aah`
  - `revenus/activite/salarie`
  - `fonc.supp_fam`
  - `prelevements_obligatoires/impot_revenu/ir`
* Détails :
  - [Prise en compte du taux d'incapacité dans l'éligibilité au CAAH #1021](https://github.com/openfisca/openfisca-france/pull/1021)
    - Renomme le paramètre `prestations.minima_sociaux.aah.taux_d_incapcite` en `prestations.minima_sociaux.aah.taux_incapacite`
    - Prend en compte le taux d'incapacité dans le calcul de l'éligibilité au CAAH.
  - [Amélioration de la lisibilité du supplément familial de traitement](https://github.com/openfisca/openfisca-france/pull/1025)
    - Renomme la variable `supp_familial_traitement` en `supplement_familial_traitement`
    - Renomme le noeud de l'arbre des paramètres `fonc.supp_fam` en `fonc.supplement_familial`
  - [Amélioration de la lisibilité de variables de la fiscalité](https://github.com/openfisca/openfisca-france/pull/1027)
    - Renomme les variables
      - `rev_cap_lib` en `revenus_capitaux_prelevement_liberatoire`
      - `rev_cap_bar` en `revenus_capitaux_prelevement_bareme`
      - `retraite_titre_onereux` en `rente_viagere_titre_onereux`

### 21.12.3 [#1032](https://github.com/openfisca/openfisca-france/pull/1032)

* Correction d'un bug dans le script qui détermine le besoin d'un bump de version
* Zones impactées : .circleci/is-version-number-acceptable.sh b/.circleci/is-version-number-acceptable.sh.
* Détails :
  - Le script faisait référence a un autre script qui a été renommé
  - Changement du path du script pour qu'il soit bien exécuté

### 21.12.2 [#1031](https://github.com/openfisca/openfisca-france/pull/1031)

* Correction d'un bug
* Périodes concernées : toutes.
* Zones impactées :
  - `prelevements_obligatoires/impot_revenu/reductions_impot`
* Détails :
  - Corrige une erreur dans le nom de variable utilisée

### 21.12.1 [#1030](https://github.com/openfisca/openfisca-france/pull/1030)

* Correction d'un bug
* Périodes concernées : à partir du 01/01/2017.
* Zones impactées :
  - `prestations/logement_social`
* Détails :
  - Corrige le calcul du logement social pour la Corse dont le code INSEE n'est pas un nombre

## 21.12.0 [#1018](https://github.com/openfisca/openfisca-france/pull/1018)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2017.
* Zones impactées :
  - `model\prelevements_obligatoires\impot_revenu`
  - `parameters\impot_revenu`
  - `parameters\prelevements_sociaux\contributions`
* Détails :
  - Mis à jour du calcul de l'impôt sur les revenus 2017

## 21.11.0 [#1008](https://github.com/openfisca/openfisca-france/pull/1008)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2017.
* Zones impactées :
  - `prestations/logement_social`
* Détails :
  - Ajoute le calcul de l'éligibilité au logement social dans le cadre du prêt locatif aidé d’intégration (PLAI)

### 21.10.11 [#1020](https://github.com/openfisca/openfisca-france/pull/1020)

* Changement mineur.
* Détails :
  - Ajoute l'unité manquante à certains barèmes libellés en euros ou francs.

### 21.10.10 [#1017](https://github.com/openfisca/openfisca-france/pull/1017)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2015.
* Zones impactées : `prelevements_obligatoires/impot_revenu`
* Détails :
  - Ajoute les paramètres de l'impôt sur les revenus 2017
  - Mets à jour les paramètres non actualisés de l'impôt sur les revenus 2015-2016

### 21.10.9 [#1012](https://github.com/openfisca/openfisca-france/pull/1012)

* Changement mineur.
* Détails :
  - Ajoute un test de performance sur les tests de CircleCI
  - Ce test peut être lancé avec la commande :
    `python openfisca_france/scripts/performance_tests/test_circleci_builds.py 1717 1716`

### 21.10.8 [#1010](https://github.com/openfisca/openfisca-france/pull/1010)

* Changement mineur.
* Détails :
  - Ajoute un test de performance sur les tests YAML
  - Ce test peut être lancé avec la commande `make performance`

### 21.10.7 [#986](https://github.com/openfisca/openfisca-france/pull/986)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/09/2017.
* Zones impactées :
  - `prestations/minima_sociaux/ass`
* Détails :
  - Ajoute la possibilité de cumuler l'ASS avec un revenu d'activité.
  - Ajoute une variable calculée ass_eligibilite_cumul_individu qui permet de déterminer le droit à ce cumul.

### 21.10.6 [#993](https://github.com/openfisca/openfisca-france/pull/993)
* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/04/2018.
* Zones impactées :
  - `parameters/minima_sociaux/aah`
  - `parameters/minima_sociaux/caah`
* Détails :
  - Met à jour le montant maximum de l'AAH en date du 01/04/2018

### 21.10.5 [#997](https://github.com/openfisca/openfisca-france/pull/997)

* Correction d'une erreur
* Détails :
  - Rappatrie `test_mes_aides_54d4e0704ec19fce442273a0.yaml` de la racine au répertoire de tests

### 21.10.4 [#983](https://github.com/openfisca/openfisca-france/pull/983)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2018.
* Zones impactées :
  - `prestations/aides_logement/ressources`
* Détails :
  - Met à jour les planchers de ressources intervenant dans le calcul de l'Aide au logement

### 21.10.3 [#985](https://github.com/openfisca/openfisca-france/pull/985)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/04/2018.
* Zones impactées :
  - `prestations/minima_sociaux/rsa`
* Détails :
  - Met à jour le montant de base du RSA en date du 1er avril 2018

### 21.10.2 [#984](https://github.com/openfisca/openfisca-france/pull/984)

* Évolution du système socio-fiscal.
* Zones impactées : `prestations/minima_sociaux/ppa`
* Périodes concernées : à partir du 01/04/2018.
* Détails :
  - Met à jour le montant forfaitaire de base du calcul de la PPA

### 21.10.1 [#977](https://github.com/openfisca/openfisca-france/pull/977)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/04/2018.
* Zones impactées :
  - `prestations/minima_sociaux/ass`
* Détails :
  - Met à jour le montant journalier à taux plein de l'ASS en date du 01/04/2018

## 21.10.0 [#980](https://github.com/openfisca/openfisca-france/pull/980)

* Amélioration technique
* Détails :
  - Adapte à Python 3

### 21.9.2 [#982](https://github.com/openfisca/openfisca-france/pull/982)

* Changement mineur
* Détails :
  - Supprime les énums utilisées en syntaxe pré-V4, qui n'est plus supportée.

### 21.9.1 [#975](https://github.com/openfisca/openfisca-france/pull/975)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/10/2016.
* Zones impactées :
  - `prestations/aides_logement`
* Détails :
  - Ajoute l'exclusion des cas particuliers dans le calcul des ressources prises en compte pour l'aide logement (AAH, AEEH, logement foyer)

## 21.9.0 [#969](https://github.com/openfisca/openfisca-france/pull/969)

* Amélioration technique
* Détails :
  - Adapte à Core v23

### 21.8.6 [#972](https://github.com/openfisca/openfisca-france/pull/972)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2015.
* Zones impactées :
  - `prestations/prestations_familiales/paje/base/apres_2014/taux_partiel`
  - `prestations/prestations_familiales/paje/base/apres_2014/taux_plein`
  - `prestations/prestations_familiales/paje`
* Détails :
  - Revalorisation des plafonds de ressources pour la PAJE en date du 01/01/2018
  - Prise en compte du plus jeune enfant dans le calcul de l'éligibilité à la PAJE
  - Mise à jour de la formule de calcul de la PAJE naissance en date du 01/01/2015

### 21.8.5 [#971](https://github.com/openfisca/openfisca-france/pull/971)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2018.
* Zones impactées : `prestations/prestations_familiales/cf`
* Détails :
  - Revalorisation du plafond de ressources de base (0 enfants) et de la majoration biactif/personne isolée dans le calcul du Complément Familial

### 21.8.4 [#970](https://github.com/openfisca/openfisca-france/pull/970)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2018.
* Zones impactées : `prestations/prestations_familiales/af/modulation`
* Détails :
  - Revalorisation des plafonds de ressources et de la majoration du plafond par enfant dans le calcul de l'Allocation Familiale

### 21.8.3 [#962](https://github.com/openfisca/openfisca-france/pull/962)

* Changement mineur.
* Détails :
  - Amélioration du template de Pull Request.
  - Ajout d'une liste de casses à cocher avec de bonnes conseils pour rédiger une belle pull request.

### 21.8.2 [#968](https://github.com/openfisca/openfisca-france/pull/968)

* Changement mineur.
* Détails :
  - Corrige lien vers la documentation dans `README.md`
  - Corrige lien vers Swagger dans `notebooks/getting-started.ipynb`

### 21.8.1 [#960](https://github.com/openfisca/openfisca-france/pull/960)

* Évolution du système socio-fiscal.
* Zones impactées : `prestations/cheque_energie`
* Périodes concernées : À partir de 2017
* Détails :
  - Corrige le calcul des unités de consommation pour le chèque énergie
  - Corrige la période de validité des variables relatives au chèque énergie

## 21.8.0 [#919](https://github.com/openfisca/openfisca-france/pull/919)

* Evolution du système socio-fiscal
* Périodes concernées : toutes
* Zones impactées :
  - `prelevements_obligatoires/impot_revenu/credits_impot`
  - `prelevements_obligatoires/impot_revenu/reductions_impot`
  - `revenus/autres`
* Détails :
  - Les avantages fiscaux pour mécénat d'entreprises (depuis 2003) et pour acquisition de biens culturels (depuis 2002) sont définies comme des réductions d'impôt et non plus des crédits d'impôt
  - Mise à jour de 'creimp' pour 2014-2016, et correction d'une petite erreur pour 2012

## 21.7.0 [#918](https://github.com/openfisca/openfisca-france/pull/918)

* Correction du système socio-fiscal.
* Périodes concernées : toutes
* Zones impactées :
  - `caracteristiques_socio_demographiques/demographie`
  - `revenus/autres`
  - `prelevements_obligatoires/impot_revenu/ir`
  - `parameters/impot_revenu/plafond_qf`
  - `parameters/impot_revenu/quotient_familial/veuf`
* Détails :
  - Ajout de la nouvelle réduction d'impôt de 20% "sous condition de revenus" (2016-) qui s'impute juste après la décote dans le calcul de l'impôt (https://www.impots.gouv.fr/portail/files/formulaires/2042/2017/2042_1891.pdf, p.3)
  - Corrige et nettoie le calcul du plafonnement du quotient familial à partir de 2013
  - Correction du calcul du nombre de parts fiscales (demi-part pour personnes seules ayant élevé des enfants caseL, nombre de parts des veufs avec enfants revalorisé depuis 2008 ..)
  - Création de paramètres spécifiques à la réduction d'impôt spécial DOM-TOM qui intervient juste après le plafonnement du quotient familial (pour l'instant non calculée mais à termes oui ?)
  - Mise à jour des paramètres

## 21.6.0 [#917](https://github.com/openfisca/openfisca-france/pull/917)

* Correction du système socio-fiscal.
* Périodes concernées : toutes
* Zones impactées :
  - `prelevements_obligatoires/impot_revenu/ir`
  - `revenus/activite/non_salarie`
  - `impot_revenu/rpns/micro/specialbnc/max`
  - `impot_revenu/rpns/micro/specialbnc/min`
* Détails :
  - Correction de la formule des 'rpns'
  - Distinction des moins-values des revenus non salariaux "professionnels" (variable 'rpns_mvct_pro') de celles des revenus non salariaux "non professionnels" ('rpns_mvct_nonpro'), car seuls les premiers peuvent s'imputer sur le revenu global
  - Création d'une variable intermédiaire 'rpns_frag' : revenus non salariaux relevant du forfait agricole. Celui-ci disparait en 2016 et est remplacé par le régime "micro bénéfice agricole" (A FAIRE)
  - Correction du calcul de l'abattement appliqué aux revenus non commerciaux relevant du régime micro-bnc (34%) + Ajout de nouveaux paramètres associés à cet abattement
  - Modification des labels et end_date de variables de revenus non salariaux dans non_salarie.py

## 21.5.0 [#916](https://github.com/openfisca/openfisca-france/pull/916)

* Évolution du système socio-fiscal.
* Zones impactées :
  - `openfisca_france/model/prelevements_obligatoires/impot_revenu/credits_impots`
  - `openfisca_france/parameters/impot_revenu/credits_impot/aidper/max_wl`
* Périodes concernées : à partir du 01/01/2012
* Détails :
  - Mise à jour de la formule (2014-2016) du crédit d'impôt 'aidper'
  - Correction de la formule du crédit d'impôt en 2012 et 2013
  - Ajout d'un nouveau paramètre associé

## 21.4.0 [#915](https://github.com/openfisca/openfisca-france/pull/915)

* Évolution du système socio-fiscal.
* Zones impactées :
  - `prelevements_obligatoires/impot_revenu/credits_impot`
  - `prelevements_obligatoires/impot_revenu/reductions_impot`
  - `prelevements_obligatoires/impot_revenu/variables_reductions_credits`
* Périodes concernées : 2014 - 2016
* Détails :
  - Mise à jour des formules (2014-2016) de la réduction 'cappme' (réduction pour souscription au capital de PME non cotées)
  - Ajout des inputs variables associées

## 21.3.0 [#914](https://github.com/openfisca/openfisca-france/pull/914)

* Évolution du système socio-fiscal.
* Zones impactées :
  - `prelevements_obligatoires/impot_revenu/credits_impot`
  - `prelevements_obligatoires/impot_revenu/reductions_impot`
  - `prelevements_obligatoires/impot_revenu/variables_reductions_credits`
* Périodes concernées : 2005 - 2016
* Détails :
  - Mise à jour des formules (2014-2016) du crédit d'impôt 'saldom2' et de la réduction d'impôt 'saldom'
  - Correction de la formule du crédit d'IR (sur la majoration pour nombre d'ascendants sd eplus de 65 bénéficiaires de l'APA et pour lesquels des dépenses d'emploi à domicile ont été engagées - case 7DL)
  - Ajout de la case 7DD dans les inputs variables

### 21.2.1 [#956](https://github.com/openfisca/openfisca-france/pull/956)

* Amélioration technique
* Détails :
  - Adapte France à Numpy v1.14

## 21.2.0 [#913](https://github.com/openfisca/openfisca-france/pull/913)

* Évolution du système socio-fiscal.
* Zones impactées :
  - `prelevements_obligatoires/impot_revenu/credits_impot`
  - `prelevements_obligatoires/impot_revenu/reductions_impot`
* Périodes concernées : 2005 - 2016
* Détails :
  - Mise à jour des formules (2014-2016) du crédit d'impôt 'quaenv' (et de la condition de bouquet : variables 'quaenv_bouquet')
  - Ajout des "inputs variables" (cases de la déclaration fiscales) associées
  - Création de paramètres YAML associés (notamment pour éviter de rentrer "en dur" les plafonds de RFR)
  - Correction de la formule (à partir de 2012) : le plafonnement s'applique aux dépenses et non à la réduction.

## 21.1.0 [#949](https://github.com/openfisca/openfisca-france/pull/949)

* Évolution du système socio-fiscal.
* Zones impactées : `prestations/cheque_energie`
* Périodes concernées : À partir de 2018
* Détails :
  - Suppression de l'éligibilité des foyers de Saint Martin au chèque énergie

# 21.0.0 [#902](https://github.com/openfisca/openfisca-france/pull/902)

* Évolution du système socio-fiscal.
* Zones impactées :
  -  `prestations/aides_logement`
  -  `prestations/minima_sociaux/rsa`
* Périodes concernées : à partir de juin 2009.
* Détails :
  - Mise à jour de la prise en compte du patrimoine dans la base ressource du RSA
    + Suppression de `interets_epargne_sur_livrets` et `epargne_non_remuneree`
    + Création de `livret_a` et `epargne_revenus_non_imposables`
    + Renommage de `prestations.minima_sociaux.rsa.patrimoine.abattement_valeur_locative_terrains_non_loue` en `prestations.minima_sociaux.rsa.patrimoine.abattement_valeur_locative_terrains_non_loues`
  - Prise en compte du patrimoine dans la base ressource des aides au logement
    + Création de `valeur_patrimoine_loue`, `valeur_immo_non_loue`, `valeur_terrains_non_loues` et `epargne_revenus_imposables`
    + Renommage de `valeur_terrains_non_loue` en `valeur_terrains_non_loues`

### 20.9.1 [#954](https://github.com/openfisca/openfisca-france/pull/954)

* Évolution du système socio-fiscal.
* Zones impactées : `mesures`
* Détails :
  - Corrige la formule des `unites_consommation`

## 20.9.0 [#912](https://github.com/openfisca/openfisca-france/pull/912)

* Évolution du système socio-fiscal.
* Périodes concernées : 2005 - 2016
* Détails :
  - Mise à jour des formules (2014-2016) des réductions 'doment', 'domlog', 'domsoc'
  - Correction de la formule de 'doment' en 2013 (les cases de la déclaration correspondant à cette réduction sont dans le nouveau formulaire 2042 IOM et commencent toutes par "fh" et non "f7")
  - Ajout des inputs variables associées à ces réductions (nouvelles cases de la déclaration IOM à partir de 2014)


## 20.8.0 [#911](https://github.com/openfisca/openfisca-france/pull/911)

* Évolution du système socio-fiscal.
* Périodes concernées : 2002 - 2016
* Détails :
  - Mise à jour des formules (2014-2016) de la réduction d'impôt 'invfor'
  - Correction d'une erreur dans la formule précédente : les reports de dépenses entrent dans le plafonnement de la réduction

## 20.7.0 [#895](https://github.com/openfisca/openfisca-france/pull/895)

* Amélioration technique
* Détails :
  - Adapte France à OpenFisca Core v22

### 20.6.2 [#920](https://github.com/openfisca/openfisca-france/pull/920)

* Amélioration technique
* Détails :
  - Migre la formule de `cmu_c_plafond` vers la syntaxe standard

### 20.6.1 [#927](https://github.com/openfisca/openfisca-france/pull/927)

* Correction d'un crash.
* Zones impactées : `reforms/landais_piketty_saez`
* Détails :
   - La réforme ne fonctionnait plus à la suite d'un changement de syntaxe qui a conduit à une erreur sur le nom d'une variable dans une formule non-testée.

## 20.6.0 [#910](https://github.com/openfisca/openfisca-france/pull/910)

* Évolution du système socio-fiscal.
* Périodes concernées : 2014 - 2016
* Détails :
  - Correction de la formule de la réduction Duflot en 2013 (plafonnement)
  - Mise à jour des formules (2014-2016) des réductions d'impôts : 'resimm' (réduction d'impot Malraux), 'locmeu' (réduction d'impôt Censi-Bouvard), 'scelli' (réduction d'impôt Scellier) et 'duflot (réduction d'impôt Duflot) qui sont toutes des réductions d'impôts portant sur les investissements immobiliers
  - Ajout de la réduction d'impôt Pinel crée en 2014
  - Ajout d'inputs variables associées à ces réductions

### 20.5.1 [#925](https://github.com/openfisca/openfisca-france/pull/925)

* Correction d'un bug
* Zones impactées : `revenus/activite/salarie`
* Détails :
  - Autorise, pour les fonctionnaires, le basculement automatique en mensuel si les revenus sont renseignés en annuel
  - Adopte un comportement similaire aux autres revenus des salariés

## 20.5.0 [#909](https://github.com/openfisca/openfisca-france/pull/909)

* Évolution du système socio-fiscal.
* Périodes concernées : 2004 - 2016
* Détails :
  - Correction des formules de certaines réductions et certains crédits d'impôts
  - Mise à jour des formules pour la période 2014 - 2016
  - Ajout de nouvelles inputs variables associées

### 20.4.1 [#948](https://github.com/openfisca/openfisca-france/pull/948)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `prestations/aides_logement`.
* Détails :
  - Implémentation des décrets limitant l'application de [`abat_spe`](https://legislation.openfisca.fr/abat_spe) dans la base ressources des ALs

## 20.4.0 [#924](https://github.com/openfisca/openfisca-france/pull/924)

* Évolution du système socio-fiscal.
* Périodes concernées : A partir de 2017
* Zones impactées : `prestations/cheque_energie`
* Détails :
  - Ajoute le calcul du montant du chèque énergie

## 20.3.0 [#908](https://github.com/openfisca/openfisca-france/pull/908)

* Évolution du système socio-fiscal.
* Périodes concernées : 2009 - 2016
* Détails :
  - Correction de la formule de l'IR : A partir de 2013, une partie des plus-values est taxé au barème alors qu'avant elles étaient taxées forfaitairement.
  - Correction de la formule du RFR : Les plus-values et revenus du capital (taxées forfaitairement ou au barème ou éxonérées) doivent entrer en compte dans le calcul du RFR
  - Création de la variable 'rfr_pv' qui regroupe l'ensemble des plus-values entrant dans le calcul du RFR, hormis celles taxées au barème (qui entrent dans le RFR également mais via le revenu net imposable 'rni')
  - Correction d'un des taux forfaitaires
  - Ajout de nouvelles inputs variables associées aux nouvelles cases des déclarations fiscales se rapportant aux plus-values

## 20.2.0 [#907](https://github.com/openfisca/openfisca-france/pull/907)

Évolution du système socio-fiscal.
* Périodes concernées : 2009 - 2016
* Zones impactées : `prelevements_obligatoires/impot_revenu/charges_deductibles`
* Détails :
  - Ammélioration du calcul des grosses réparations et de leurs prise en compte dans le calcul des charges déductibles
  - Ajout de nouvelles variables d'inputs pour les cases de l'IR correspondantes

## 20.1.0 [#884](https://github.com/openfisca/openfisca-france/pull/884)

* Évolution du système socio-fiscal.
* Périodes concernées : A partir de 04/2017
* Zones impactées : `prestations_familiales/paje`
* Détails :
  - Remplace la `paje_clca` par la `page_prepare` dans le calcul de la `paje` à partir d'avril 2017.

### 20.0.9 [#906](https://github.com/openfisca/openfisca-france/pull/906)

* Évolution du système socio-fiscal.
* Périodes concernées : principalement, mise à jour avec les barèmes 2016, avec quelques corrections sur 2012-2013 et 2015.
* Détails :
  - Ajout des barèmes IPP de l'impôt sur le revenu 2016
  - Correction de quelques paramètres de l'impôt, pour les années précédentes

### 20.0.8 [#862](https://github.com/openfisca/openfisca-france/pull/862)

* Évolution du système socio-fiscal.
* Zones impactées :
  - `prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/allegements`
  - `revenus/activite/salarie`
* Détails :
  - Corrige #844 (erreurs de calcul constatées sur la réduction générale dite "Fillon")

### 20.0.7 [#867](https://github.com/openfisca/openfisca-france/pull/867)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 1er janvier 2018.
* Détails :
  - Mise à jour des taux MMID salarié.
  - Mise à jour du taux du CICE.
  - Mise à jour du SMIC horaire.
  - Mise à jour du plafond mensuel de la sécurité sociale.
  - Mise à jour du taux de CGS déductible.
  - Mise à jour de la cotisation chômage salarié.
  - Ajout de tests

### 20.0.6 [#892](https://github.com/openfisca/openfisca-france/pull/892)

* Correction d'un crash
* Détails :
  - Corrige l'erreur 500 qui apparaît dans les calculs de la PPA et du RSA depuis février 2018.
  - Vérifie dans les tests que le revenu disponible peut être calculé jusuqu'à 2020 pour éviter qu'un problème similaire se reproduise.

### 20.0.5 [#857](https://github.com/openfisca/openfisca-france/pull/857)

* Changement mineur.
* Détails :
  - Clarification d'un nom de variable intermédiaire intervenant dans le calcul de af_base.

### 20.0.4 [#842](https://github.com/openfisca/openfisca-france/pull/842)

* Amélioration technique
* Détails :
  - Migre la quasi-totalité des formules vers la syntaxe introduite par OpenFisca-Core 4

### 20.0.3 [#879](https://github.com/openfisca/openfisca-france/pull/879)

* Amélioration technique
* Détails :
  - Adapte France à OpenFisca Core v21.2

### 20.0.2 [#878](https://github.com/openfisca/openfisca-france/pull/878)

* Correction d'un crash
* Détails :
  - Fixe la version d'OpenFisca Core utilisée, la version v21.2 de Core n'étant à ce jour pas compatible avec OpenFisca France.

### 20.0.1 [#875](https://github.com/openfisca/openfisca-france/pull/875)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `prestations/aides_logement`
* Détails :
  - Garantie que l'aide au logement pour un foyer primo-accédant est nulle si le prêt est déjà remboursé.

# 20.0.0 [#846](https://github.com/openfisca/openfisca-france/pull/846)

* Amélioration technique
* Détails :
  - Modifie la façon dont les Enumerations sont définies et appelées.
  - Renomme des fichiers de parametres pour pouvoir simplifier des formules dont le resultat dépend de `TypesZoneAPL` (Fancy indexing).
  - Certains Enums étaient utilisées comme booléens. La valeur 0/1 a été remplacée par le membre d'Enum correspondant.

Par exemple pour :

```
class TypesAAHNonCalculable(Enum):
calculable = u"Calculable"
intervention_CDAPH_necessaire = u"intervention_CDAPH_necessaire"
```

- `False`, ancien index 0, devient `TypesAAHNonCalculable.calculable`
- `True`, ancien index 1, devient `TypesAAHNonCalculable.intervention_CDAPH_necessaire`

Les valeurs possibles des Enums ainsi que les nouvelles valeurs par défaut sont disponibles sur legislation.openfisca.fr

#### Pour les mainteneurs de formules:

Les Enums commencent tous par `Types` et sont habituellement placés au-dessus des variables qui les calculent.

Les Enums les plus fréquemments utilisés sont placés dans le fichier `model/base.py`.

Référencer un Enum dans une formule :

Si l'Enum est dans votre fichier ou dans `base.py`, référencez le directement dans la formule:
```py
statut_marital == TypesStatutMarital.celibataire
```

Sinon, importez-le dans votre formule avec l'attribut `possible_values` de la variable qui le calcule :

```py
TypesContratDeTravailDuree = contrat_de_travail_duree.possible_values
contrat_travail == TypesContratDeTravailDuree.cdi
```
#### Effets sur la Web API

Avant:

```
"individus": {
"Bill": {
"categorie_salarie": {
"2017-01": 1
}
}
```

Maintenant:

```
"individus": {
"Bill": {
"categorie_salarie": {
"2017-01": prive_cadre
}
}
}
```

#### YAML testing
Avant:

```
period: "2016-06"
name:
Taxe d'apprentissage
relative_error_margin: 0.01
input_variables:
salaire_de_base: 1467
categorie_salarie: 0
output_variables:
taxe_apprentissage: -9.97
```
Maintenant:

```
period: "2016-06"
name:
Taxe d'apprentissage
relative_error_margin: 0.01
input_variables:
salaire_de_base: 1467
categorie_salarie: prive_non_cadre
output_variables:
taxe_apprentissage: -9.97
```

#### Python API

Lors du calcul d'une variable Enum en Python, l'output est un array de membres Enum.

> Chaque membre d'Enum :
> - a un attribut `name` qui contient sa clé (e.g. `nulle`)
> - a un attribut `value` qui contient sa description (e.g. `u"Nulle, pas d'exposition de l'employé à un facteur de pénibilité"`)

### 19.0.4 [#870](https://github.com/openfisca/openfisca-france/pull/870)

* Amélioration technique.
* Périodes concernées : toutes.
* Zones impactées : `prelevements_obligatoires/taxe_habitation`.
* Détails : Corrige la négation des booléens en utilisant de façon appropriée logical_not.

### 19.0.3 [#790](https://github.com/openfisca/openfisca-france/issues/790)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `prestations/minima_sociaux/cmu`
* Détails :
  - Ajout du CAAH à la liste des ressources prises en compte pour le calcul de la CMU-C / ACS

### 19.0.2

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées :
  - `prestations/minima_sociaux/ppa`
  - `prestations/minima_sociaux/rsa`
* Détails :
  - Prend en compte l'avantage en nature des primo-accédants dans le calcul des aides au logement.

### 19.0.1

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/10/2017.
* Zones impactées :
  - prestations/aides_logement
* Détails :
  - Ajout de l'abattement forfaitaire de 5€ dans le calcul des aides au logement à partir du 01/10/2017.

# 19.0.0 [#858](https://github.com/openfisca/openfisca-france/pull/858)

* Améliorations techniques **non rétro-compatibles**
* Détails :
  - Change la valeur par défaut de `asi_aspa_condition_nationalite` à `True`
  - Change la valeur par défaut de `rsa_condition_nationalite` à `True`
  - Change la valeur par défaut de `nombre_jours_calendaires` à `30`
  - Change la péride de définition de `retraite_imposable`: cette variable est désormais mensuelle.
  - Renomme `uc` en `unites_consommation`

<!-- -->

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `/mesures`.
* Détails :
  - Corrige le calcul de `unites_consommation` (Unités de consommation d'un ménage)
  - Introduit la variable `revenu_primaire`

<!-- -->

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `/prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/`.
* Détails :
  - Introduit la nouvelle valeur `Mensuel strict` à l'énum `cotisation_sociale_mode_recouvrement`
  - Corrige les cotisations sociales pour la fonction publique
  - Ne compte pas de cotisations sociales à quelqu'un qui n'a pas d'activité salariée.

<!-- -->

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées :
  - `/prestations/aides_logement`
  - `/prestations/prestations_familiales`
* Détails :
  - Corrige la base ressources des aides logement et des prestations familiales quand les 2 conjoints ne sont pas dans le même foyer fiscal.

<!-- -->

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées :
  - `/revenus/capital/`
* Détails :
  - Relie la variable `revenus_capital` aux variables qui lui correspondent sur la déclaration d'impot.

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

### 18.9.10 [#829](https://github.com/openfisca/openfisca-france/pull/829)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `/prestations/aides_logement`.
* Détails :
  - Corrige les aides au logement pour les primo-accédants ayant une importante base ressources.

### 18.9.9 [#803](https://github.com/openfisca/openfisca-france/pull/803)

* Changement mineur
* Détails :
  - Simplifie le calcul des aides au logement en utilisant le calcul de législation dynamique (nouvelle feature de OpenFisca)

### 18.9.8 [#825](https://github.com/openfisca/openfisca-france/pull/825)

* Correction d'un crash sous Windows
* Détails :
  - Corrige l'erreur WindowsError: `[Error 206] Nom de fichier ou extension trop long` qui interrompt le clone d'OpenFisca-France sous Windows.
  - Dans `parameters`, assemble dans un nouveau YAML le contenu d'un sous-répertoire lorsque le chemin vers celui-ci ou l'un de ses fichiers est trop long.

### 18.9.7 [#811](https://github.com/openfisca/openfisca-france/pull/811)

* Changement mineur
* Détails :
  - Documente les entités `FoyerFiscal` et `Menage`

### 18.9.6 [#815](https://github.com/openfisca/openfisca-france/pull/815)

* Changement mineur
* Détails :
  - Corrige une typo dans la description de `credit_impot_competitivite_emploi`

### 18.9.5 [#814](https://github.com/openfisca/openfisca-france/pull/814)

* Changement mineur
* Détails :
  - Rajout des références législatives sur la baisse de la cotisation AGS au 1er juillet 2017.

### 18.9.4 [#809](https://github.com/openfisca/openfisca-france/pull/809)

* Changement mineur.
* Détails :
  - Référence la nouvelle adresse de la documentation technique

### 18.9.3 [#817](https://github.com/openfisca/openfisca-france/pull/817)

* Changement mineur.
* Périodes concernées : à partir du 07/05/2017.
* Zones impactées : `parameters/bourses_education/bourse_college`.
* Détails :
  - Mise à jour des montant des bourses des collèges conformément au [décret du 5 mai 2017](https://www.legifrance.gouv.fr/eli/decret/2017/5/5/MENE1711101D/jo/texte).

### 18.9.2 [#812](https://github.com/openfisca/openfisca-france/pull/812)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `/prestations/aides_logement`.
* Détails :
  - Suppresion de la notification de non-calculabilité des aides au logement pour les primo-accédants.

### 18.9.1 [#583](https://github.com/openfisca/openfisca-france/pull/583)

* Changement mineur.
* Périodes concernées : à partir du 01/11/2014.
* Zones impactées : `prelevements_obligatoires/prelevements_sociaux/cotisations_sociales/stage`.
* Détails :
  - Extraction du taux de gratification minimum des stagiaires vers le fichier de paramètres.

## 18.9.0 [#798](https://github.com/openfisca/openfisca-france/pull/798)

* Amélioration technique
* Détails :
  - Migration vers la version 17 d'OpenFisca-Core.
  - Transformation des paramètres depuis XML vers YAML.
  - Ajout d'un sous-répertoire `migrations` dans le répertoire `scripts`.

### 18.8.2 [#806](https://github.com/openfisca/openfisca-france/pull/788)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/07/2017
* Zones impactées : `prelevements_obligatoires/prelevements_sociaux/contributions_sociales/versement_transport`.
* Détails :
  - Mise à jour conformément à [la circulaire du 31 mai](https://www.urssaf.fr/portail/files/live/sites/urssaf/files/Lettres_circulaires/2017/ref_LCIRC-2017-0000019.pdf)
  - données extraites via l'API de l'URSSAF, cf. https://github.com/sgmap/taux-versement-transport

### 18.8.1 [#789](https://github.com/openfisca/openfisca-france/pull/789)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/07/2017
* Zones impactées : `openfisca_france/parameters/cotsoc.xml`, `openfisca_france/parameters/prelevements_sociaux.xml`.
* Détails :
  - Prise en compte de la baisse de la cotisation AGS au 1er juillet.

## 18.8.0 [#801](https://github.com/openfisca/openfisca-france/pull/801)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `/prestations/aides_logement`.
* Détails :
  - Calcul des aides au logement pour les primo-accédants.
  - Marge d'erreur (~5% sur les tests) voir avec un expert métier pour rectifier le calcul.

## 18.7.0 [#797](https://github.com/openfisca/openfisca-france/pull/797)

* Amélioration technique
* Détails :
  - Déclare OpenFisca-France compatible avec OpenFisca-Core 16

### 18.6.6 [#781](https://github.com/openfisca/openfisca-france/pull/781)

* Changement mineur.
* Détails :
  - Mise à jour du `label` de `age` pour expliciter qu'il s'agit de l'âge en début de mois

### 18.6.5 [#785](https://github.com/openfisca/openfisca-france/pull/785)

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

### 18.6.4 [#784](https://github.com/openfisca/openfisca-france/pull/784)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2017
* Zones impactées : `prestations/minima_sociaux/ass`.
* Détails :
  - Implémentation de la non-éligibilité à l'ASS (Allocation de Solidarité Spécifique) en cas d'éligibilité à l'AAH (Allocation aux Adultes Handicapés)
    - [article 87 loi n° 2016-1917 du 29 décembre 2016 de finances pour 2017](https://www.legifrance.gouv.fr/affichTexteArticle.do;jsessionid=49AD9A92D43F6C7A085F8E1D669AEFC2.tpdila18v_2?cidTexte=JORFTEXT000033734169&idArticle=LEGIARTI000033760616&dateTexte=20170622&categorieLien=id#LEGIARTI000033760616)
    - [article L. 5423-7 du code du travail](https://www.legifrance.gouv.fr/affichCodeArticle.do;jsessionid=49AD9A92D43F6C7A085F8E1D669AEFC2.tpdila18v_2?idArticle=LEGIARTI000033813814&cidTexte=LEGITEXT000006072050&dateTexte=20170622)

### 18.6.3 [#787](https://github.com/openfisca/openfisca-france/pull/787)

* Amélioration technique
* Détails :
  - Migre les formules situés dans les fichiers suivant vers la syntaxe introduite par OpenFisca-Core 4 :
    - `prelevements_obligatoires/impot_revenu/credits_impot.py`
    - `prelevements_obligatoires/impot_revenu/ir.py`
    - `prelevements_obligatoires/isf.py`
    - `prelevements_obligatoires/taxe_habitation.py`
    - `reforms/landais_piketty_saez.py`

### 18.6.2 [#794](https://github.com/openfisca/openfisca-france/pull/794)

* Correction d'un crash
+ Détails :
  - Mets à jour la version d'OpenFisca-Web-API requise pour qu'elle soit compatible avec la version d'OpenFisca-Core requise.
  - Les deux versions référencées dans le `setup.py` étaient incompatibles, provoquant une erreur au démarrage de l'API avec `gunicorn` ou `paster`.

### 18.6.1 [#793](https://github.com/openfisca/openfisca-france/pull/793)

* Changement mineur
* Détails :
  - Répare la déclaration de l'URL du dépôt, endomagée dans la version `18.6.0`

## 18.6.0 [#775](https://github.com/openfisca/openfisca-france/pull/775)

* Amélioration technique
* Détails :
  - Adapte `france` à  la version `15.0.0` de `core`.
  - Applique le renommage de l'attribut de `Variable` `url` en `reference`.
  - Pour les variables réformées, ne définis plus l'attribut `reference`.

### 18.5.3 [#786](https://github.com/openfisca/openfisca-france/pull/786)

* Changement mineur
* Détails
  - Répare la réforme `de_net_a_brut`.

### 18.5.2 [#778](https://github.com/openfisca/openfisca-france/pull/778)

* Amélioration technique
* Détails :
  - Ajoute un script de reformatage des fichiers de paramètres XML. Ce reformatage est utile pour rendre plus lisible le diff lors des import des paramètres de l'IPP.
  - Reformate les paramètres XML en utilisant le script décrit plus haut.
  - Ajoute un script de merge des paramètres XML avec les paramètres de l'IPP (Institut des Politiques Publiques). Ce script réécrit les paramètres XML en laissant un diff le plus lisible possible.

### 18.5.1 [#780](https://github.com/openfisca/openfisca-france/pull/780)

* Amélioration technique
* Détails :
  - Migre les formules liées aux prestations sociales vers la syntaxe introduite par OpenFisca-Core 4

## 18.5.0 [#704](https://github.com/openfisca/openfisca-france/pull/685)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/01/2017
* Zones impactées : `openfisca_france/model/prestations/anah`.
* Détails :
  - Estimation de [l'éligibilité aux aides de l'ANAH](http://www.anah.fr/proprietaires/proprietaires-occupants/les-conditions-de-ressources/)

### 18.4.2 [#770](https://github.com/openfisca/openfisca-france/pull/770)

* Amélioration technique
* Détails :
  - Mets à jour OpenFisca-Core
    - Modifie la manière de définir les dates de début des formules, et les dates de fin des variables.
    - Modifie les conventions de nommages des formules des variables.
    - Pour plus d'information, voir le [Changelog d'OpenFisca-Core](https://github.com/openfisca/openfisca-core/blob/master/CHANGELOG.md#1400---522) correspondant.

### 18.4.1 [#776](https://github.com/openfisca/openfisca-france/pull/776)

* Correction d'un crash
* Détails :
  - Openfisca n'est pas compatible avec la nouvelle version de numpy 1.13.
  - Requiert numpy < 1.13

## 18.4.0 [#772](https://github.com/openfisca/openfisca-france/pull/772)

* Amélioration technique
* Détails :
  - Permet d'ajouter une référence aux paramètres XML.
  - Supprime les commentaires des XML (Compatibilité avec core 13.0.0).

### 18.3.1 [#767](https://github.com/openfisca/openfisca-france/pull/767)

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

## 18.3.0 [#746](https://github.com/openfisca/openfisca-france/pull/746)

* Amélioration technique
* Détails :
  - Réunit dans un même répertoire les fichiers relatifs aux barèmes IPP.
  - Ajoute un script qui exécute le processus d'import dans son ensemble.
    - Laisse le contributeur commiter les changements manuellement.
	- Internalisation du dépôt [converters](https://framagit.org/french-tax-and-benefit-tables/ipp-tax-and-benefit-tables-converters) de l'IPP.
  - Désormais le seul lieu de contribution pour les paramètres est `openfisca_france/parameters`.
    - Disparition de `param.xml`.

### 18.2.9 [#763]

* Changement mineur
* Détails :
  - Introduit la réforme `smic_h_b_9_euros`

### 18.2.8 [#762](https://github.com/openfisca/openfisca-france/pull/762)

* Changement mineur
* Détails :
  - Fait passer les tests en parallèle

### 18.2.7 [#728](https://github.com/openfisca/openfisca-france/pull/728)

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

### 18.2.6 [#747](https://github.com/openfisca/openfisca-france/pull/747)

* Évolution du système socio-fiscal.
* Périodes concernées : à partir du 01/04/2017.
* Zones impactées : `prestations/minima_sociaux/asi_aspa`,
* Détails :
  - Mise à jour des plafonds et montants de l'ASI et de l'ASPA
  - Source: http://www.legislation.cnav.fr/Documents/circulaire_cnav_2017_13_04042017.pdf

### 18.2.5 [#760](https://github.com/openfisca/openfisca-france/pull/760)

* Changement mineur
* Détails :
  - Supprime le système de chargement automatique des extensions via le dossier `extensions` . Les extensions sont maintenant installées sous la forme de packages indépendants.

### 18.2.4 [#759](https://github.com/openfisca/openfisca-france/pull/759)

* Changement mineur
* Détails :
  - Suppression de l'internationalisation (traductions des messages d'erreurs). Cette fonctionnalité n'était pas utilisée.

### 18.2.3 [#757](https://github.com/openfisca/openfisca-france/pull/757)

* Changement mineur
* Détails :
  - Retirer le fichier model/datatrees, le script de génération et les références aux date-trees présentes dans france_taxbenefitsystem.py

### 18.2.2 [#742](https://github.com/openfisca/openfisca-france/pull/742)

* Amélioration technique
* Détails :
  - Amélioration des messages d'erreur en cas d'erreur dans la législation

### 18.2.1 [#708](https://github.com/openfisca/openfisca-france/pull/708)

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

## 18.2.0 [#731](https://github.com/openfisca/openfisca-france/pull/731)

* Amélioration technique
* Détails :
  - Adapte `france` à  la version `12.0.0` de `core`.
  - Enlève les attributs `fuzzy` des paramètres, qui devient le comportement par défaut. Enlève les attributs `fin`.

## 18.1.0 [#739](https://github.com/openfisca/openfisca-france/pull/739)

* Changement mineur
* Détails:
  - Rends OpenFisca-France compatible avec la version `11.0` d'OpenFisca-Core

# 18.0.0 [#718](https://github.com/openfisca/openfisca-france/pull/718)

* Évolution du système socio-fiscal
* Périodes concernées : toutes
* Zones impactées: `prestations/aides_logement`
* Détails :
    - Corrige l'erreur de frappe sur le nom de la variable `aide_logement_participation_personelle` qui devient donc `aide_logement_participation_personnelle`

## 17.2.0 [#726](https://github.com/openfisca/openfisca-france/pull/726)

* Évolution du système socio-fiscal
* Périodes concernées : à partir du 01/04/2017.
* Zones impactées: `prelevements_obligatoires/prelevements_sociaux/contributions_sociales/versement_transport`
* Détails :
    - Mise à jour des taux de versement transport

* Changement mineur
* Zones impactées: `/assets/versement_transport`
* Détails :
    - Suppression de fichiers inutilisés (quelques mégas)

## 17.1.0 [#724](https://github.com/openfisca/openfisca-france/pull/724)

* Amélioration technique.
* Détails :
  - Permet d'installer OpenFisca-France avec une API web compatible via `pip install openfisca_france[api]`
  - Redéploie `api.openfisca.fr` à chaque publication de version

### 17.0.1 [#730](https://github.com/openfisca/openfisca-france/pull/730)

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

### 16.1.1 [#632](https://github.com/openfisca/openfisca-france/pull/632)

* Changement mineur
* Détails :
    - Arrête d'importer de numpy des fonctions qui sont déjà fournies par `openfisca_core.model_api`

## 16.1.0 [#707](https://github.com/openfisca/openfisca-france/pull/707))

* Évolution du système socio-fiscal
* Périodes concernées : à partir du 01/07/2016.
    - Les changements prennent effet à partir de la rentrée scolaire 2016
* Zones impactées: `prestations/education`
* Détails :
    - Met à jour le mode de calcul des bourses de collège et lycée, entré en vigueur à la rentrée 2016.
    - Introduit les variables `bourse_college_echelon` et `bourse_lycee_echelon`

# 16.0.0 [#710](https://github.com/openfisca/openfisca-france/pull/710)
* Amélioration technique **non-rétrocompatible**
* Détails :
    - Restreint les périodes acceptées par OpenFisca
    - La liste des périodes autorisées est disponible dans la [documentation](https://openfisca.org/doc/key-concepts/periodsinstants.html)

<!-- -->

* Amélioration technique
* Détails :
  - Adapte `france` à  la version `9.0.0` de `core`.

## 15.1.0 [#699](https://github.com/openfisca/openfisca-france/pull/699)

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

### 15.0.1 [#697](https://github.com/openfisca/openfisca-france/pull/697)

> Version précédemment publiée à tort en tant que 14.1.1

* Amélioration technique
* Utilise le module `core.model_api` plutôt que de réimporter un par un tous les objets Python nécessaires pour écrire une formule
    - Aucun impact pour les ré-utilisateurs

# 15.0.0 [#685](https://github.com/openfisca/openfisca-france/pull/685)

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

# 14.0.0 [#690](https://github.com/openfisca/openfisca-france/pull/690)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : aucune.
* Détails :
  - Retire la variable  `nbptr_n_2`. Elle est inutilisée et obsolète depuis l'introduction des `period`.
  - Cette variable n'intervenant dans aucune formule, elle n'a donc aucun impact.

### 13.2.2 [#695](https://github.com/openfisca/openfisca-france/pull/695)

* Évolution du système socio-fiscal.
* Périodes concernées : toutes.
* Zones impactées : `mesures`.
* Détails :
  - Correction du calcul de `type_menage`.
  - Des erreurs peuvent subsister quand ménage et famille ne coincide pas (cas des ménages complexes).
  - Cette variable est utilisée à des fins statistiques et n'entre dans le calcul d'aucune prestation.

### 13.2.1 [#687](https://github.com/openfisca/openfisca-france/pull/687)

* Évolution du système socio-fiscal.
* Périodes concernées : Jusqu'au 31/12/2015.
* Zones impactées : `prelevements_obligatoires/impot_revenu/ppe`.
* Détails :
  - Corrige la valeur erronnée retournée par `ppe_tp_sa`.
  - Le calcul de l'indicatrice de travail à temps plein `ppe_tp_sa` renvoyait une valeur érronée, provoquant des erreurs dans le calcul de la prime pour l'emploi `ppe`.

## 13.2.0 [#676](https://github.com/openfisca/openfisca-france/pull/676)

* Amélioration technique
* Détails :
  - Cette évolution est a priori transparente pour les utilisateurs.
  - Déplace la transformation du JSON en test case du module `scenarios` de `france` vers `core`
  - Adapte `france` à  la version `5.0.0` de `core`.

### 13.1.5 [#684](https://github.com/openfisca/openfisca-france/pull/684)

* Évolution du système socio-fiscal
* Périodes concernées : à partir du 01/01/2017.
* Zones impactées : `prelevements_obligatoires/prelevements_sociaux/cotisations_sociales`
* Détails :
  - Corrige le taux de la réduction générale sur les bas salaires (Fillon) au 01/01/2017.
  - Corrige le taux de la cotisation maladie MMID employeur au 01/01/2017.

### 13.1.4 [#682](https://github.com/openfisca/openfisca-france/pull/682)

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

### 12.0.6

* Fix `rsa_activite`

### 12.0.5

* Change `af` to DatedVariable to take into account the introduction of degressivite

### 12.0.4

* Change `aige_aine` column from IntCol to AgeCol.

### 12.0.3

* Rename `CAT` to `CATEGORIE_SALARIE` to be more explicit.

### 12.0.2

* Don't consider handicaped demandeur/conjoint as personne à charge in aides logement.

### 12.0.1

* Fix `aide_logement_montant_brut_avant_degressivite` returned `period` to month.

# 12.0.0

* Use core `test_runner` for yaml tests
* Return yearly amount for `acs`, `bourse_college`, `bourse_lycee` instead of artificially divide it by 12 (breaking change).

## 11.1.0

 * Implement "Aides au logement" degression when rent is above a threshold.

### 11.0.2

* Fix typo in `casa` variable label

### 11.0.1

* Add a `sans_objet` level to variable `contrat_de_travail`

# 11.0.0

* Rename `cotsoc_noncontrib` to `cotisations_non_contibutives`

### 10.1.1

* Fix combination rule for aide 1er salarié / aide PME

## 10.1.0

* Add cotisation pénibilité

### 10.0.2

* Fix csg legislation link in `inversion_directe_salaires` reform.

### 10.0.1

* Update the following rates that changed on the first of january 2017:
	- SMIC
	- Plafond de la sécurité sociale
	- Taux AGIRC-GMP
	- Taux AGS
	- Prolongation Aide embauche PME 2017

# 10.0.0

* From 2017, for RSA, remove CA and number of employees conditions.
* Calculate RSA for Travailleurs Non Salariés
* Introduce RSA fictif mechanism
* Deprecate:
	- `rsa_majore`
	- `rsa_non_majore`
* Introduce inputs:
	- `primes_salaires_net`
	- `indemnite_fin_contrat_net`

### 9.0.1

* Add `fuzzy` in some `ppa` parameters, needed to run calculations in 2017

# 9.0.0

* Continue mesures migration
* Complete remplacement migration
* Rename `impo` to `impots_directs`
* Rename `revnet` to `revenu_net`
* Rename `revini` to `revenu_initial`

### 8.0.1

* Introduce echelon_bourse

# 8.0.0

* Rename `paje_clmg` to `paje_cmg`

### 7.0.1

* Improving CASA

# 7.0.0

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

### 6.0.7

* Remove wrong max numbers of enfants in entities

### 6.0.6

* Deprecate `entreprise_assujettie_tva`

### 6.0.5

* Add effectif_entreprise exclusion condition to Contribution Supplémentaire Apprentissage

### 6.0.4

* Fix some regressions in parameters introcduced by 6.0.0
  * Re-apply RSA revalorisation from september
  * Correct bonification rate for PPA

### 6.0.3

* Migrate some formulas to new syntax
  * `aefa.py`
  * `af.py`
  * `anciens_ms.py`
  * `ars.py`
  * `base_ressource.py`
  * `cf.py`
  * `paje.py`
  * `rsa.py`

### 6.0.2

* Fix legislation parameter call for RMI-RSA transition

### 6.0.1

* Fix packaging of 6.0.0

# 6.0.0

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
	* `rente_viagere_titre_onereux_declarant1`
	* `rente_viagere_titre_onereux_net_declarant1`
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

### 4.1.20

* Set `set_input` attribute to `set_input_divide_by_period` for variables `heures_remunerees_volume` et `heures_non_remunerees_volume`.

### 4.1.19

* Introduce MVA

### 4.1.18

* Introduce PCH

### 4.1.17

* Reimplement `rsa_indemnites_journalieres_activite` and `date_arret_de_travail` using `datetime.date.min`.

### 4.1.16

* Correct wrong behaviour in the combination of exemptions with the dispositif Jeune Entreprise Innovante (JEI)


### 4.1.15

* Consider some indemnités journalieres as revenus de remplacement in PPA (and RSA), according to the date of the arret de travail.
* Introduce
	* `rsa_indemnites_journalieres_hors_activite`
	* `rsa_indemnites_journalieres_activite`
	* `date_arret_de_travail`

### 4.1.14

* Add cerfa boxe : 3vt (PEA)

### 4.1.13

* Increase RSA base amount to 535.17 from September 2016

### 4.1.12

* Fix links in README

### 4.1.11

* Remove end dates where not necessary

### 4.1.10

* Refactor asi_aspa.py
* Fix abattement for conjoint salary
* Adjust interaction with AAH
* Small fix on RSA: don't use euclidian division because of rounding issues
* Small fix on PPA: don't take into acccount more AF that it have been declared (see 4.1.8)

### 4.1.9

* Tighten CMU/ACS eligibility conditions when when person is less than 25
* Introduce `cmu_acs_eligibilite`, `habite_chez_parents`

### 4.1.8

* Refactor rsa.py
* Do not take stages gratification into account
* Do not take into acccount more AF that it have been declared

### 4.1.7

* Fix bug in CMU forfait_logement
* Refactor CMU computation

### 4.1.6

* Fix bugs in RSA:
  * One need to be **strictly** more that 25 to benefit it.
  * Apply rsa_forfait_asf accordingly to the asf actually being paid.
* Deprecate rsa_forfait_asf_individu

### 4.1.5

* Follow OpenFisca-Core major release

### 4.1.4

* Update travis procedures

### 4.1.3

* Delete rfr_n_1

### 4.1.2

* Use "python -m compileall" to check for syntax errors, not flake8

### 4.1.1

* Add labels to several variables

## 4.1.0

* Run yaml tests from CLI
	* Exemple: `openfisca-run-test my_test.yaml`

### 4.0.11

* Enhance and move getting-started notebook

### 4.0.10 [diff](https://github.com/openfisca/openfisca-france/compare/4.0.9..4.0.10)

* Fix Landais, Piketty, Saez reform

### 4.0.9 [diff](https://github.com/openfisca/openfisca-france/compare/4.0.8..4.0.9)

* Adapt plfr2014 reform to new Reform API

### 4.0.8 [diff](https://github.com/openfisca/openfisca-france/compare/4.0.7..4.0.8)

* Adapt PPA to avoid antedating paramameters of 3 months.

### 4.0.7 [diff](https://github.com/openfisca/openfisca-france/compare/4.0.6..4.0.7)

* Include ppa in minimas sociaux (mini) and update decompositions accordingly

### 4.0.6 [diff](https://github.com/openfisca/openfisca-france/compare/4.0.5..4.0.6)

* Add back extensions folder and README

### 4.0.5 [diff](https://github.com/openfisca/openfisca-france/compare/4.0.4..4.0.5)

* Fix inversion-directe-salaires reform

### 4.0.4 [diff](https://github.com/openfisca/openfisca-france/compare/4.0.3..4.0.4)

* Fix plf2016 and ayrault_muet reforms

### 4.0.3 [diff](https://github.com/openfisca/openfisca-france/compare/4.0.2..4.0.3)

* Update numpy dependency to 1.11
* Upgrade pip to >= 8.0 in travis
* Do not install numpy from apt in travis
* Install scipy by wheels
* Fix semver version number towards OpenFisca-Core

### 4.0.2 [diff](https://github.com/openfisca/openfisca-france/compare/4.0.1..4.0.2)

* Remove wrong stop date of `aeeh`

### 4.0.1 [diff](https://github.com/openfisca/openfisca-france/compare/4.0.0..4.0.1)

* Correct bug in `switch_on_allegement_mode`

# 4.0.0 [diff](https://github.com/openfisca/openfisca-france/compare/3.4.1..4.0.0)

* Apply core API changes introduced by [openfisca-core 2.0](https://github.com/openfisca/openfisca-core/pull/388)
* Change the way the France tax benefit system is built
* Change the way reforms are built
* Move extensions from `./model/extensions` to `./extensions`
* Warning : relatives imports are now impossible in model files.

### 3.4.1 [diff](https://github.com/openfisca/openfisca-france/compare/3.4.1..3.4.0)

* Only enforce version and changelog update in CI when PR target is master.

## 3.4.0 [diff](https://github.com/openfisca/openfisca-france/compare/3.4.0..3.3.0)

* Introduce the `entreprise_est_association_non_lucrative` boolean input variable
* Null the CICE and taxe d'apprentissage (taxe + contribution supplémentaire) when this input is True
* Force the computing of taxe sur les salaires when this input is True
* Implement franchise, décôte and abattement associations non lucratives in Taxe sur les salaires

## 3.3.0 [diff](https://github.com/openfisca/openfisca-france/compare/3.3.0..3.2.0)

* Add variables for `complémentaire santé`, compulsory in 2016 :
	* `complementaire_sante_taux_employeur`
	* `complementaire_sante_employeur`
	* `complementaire_sante_salarie`
It is included in the bases of the following variables.

* Correct `forfait_social` and link it to the `cotisations`, test it.
* Correct `taxe_salaires` and update its rates
* Test CSG-CRDS

## 3.2.0 [diff](https://github.com/openfisca/openfisca-france/compare/3.2.0..3.1.0)

* Consolidate the case of `temps partiel` for the input of a number of hours per month, based on the legal duration of 151.67 per month
* Specifically, correct the proratisation of `plafond de la sécurité sociale` and `coefficient de proratisation`.
* See issue #496 for details

## 3.1.0 [diff](https://github.com/openfisca/openfisca-france/compare/3.1.0..3.0.0)

* Update the rates of the versement transport contribution
* Introduce an history of rates
* Move its code to a new file (~ 5 functions)

# 3.0.0 [diff](https://github.com/openfisca/openfisca-france/compare/3.0.0..2.0.0)

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

# 2.0.0 [diff](https://github.com/openfisca/openfisca-france/compare/1.3.1..2.0.0)

* Deprecate Paris reform
* Introduce enfant_place

### 1.3.1 [diff](https://github.com/openfisca/openfisca-france/compare/1.3.1rc0...1.3.1)

* Adjust ppa computation

### 1.3.1rc0 [diff](https://github.com/openfisca/openfisca-france/compare/1.3.0..1.3.1rc0)

* Fix versioning enforcement

## 1.3.0 [diff](https://github.com/openfisca/openfisca-france/compare/1.2.0...1.3.0)

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

## 1.2.0 [diff](https://github.com/openfisca/openfisca-france/compare/1.1.0...1.2.0)

* Force version number incrementation through CI
* Force changelog editing through CI
* Publish tag after merging
* Publish on pypi after tagging

## 1.1.0 [diff](https://github.com/openfisca/openfisca-france/compare/1.0...1.1.0)

* Replace `build_column` function calls by `Variable` classes (see [#384](https://github.com/openfisca/openfisca-core/pull/384))

# 1.0.0 [diff](https://github.com/openfisca/openfisca-france/compare/0.5.5...1.0)

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
	* `rto_declarant1` -> `rente_viagere_titre_onereux_declarant1`
	* `rto_net_declarant1` -> `rente_viagere_titre_onereux_net_declarant1`
	* `rto_net` -> `rente_viagere_titre_onereux_net`
	* `salcho_imp` -> `revenu_assimile_salaire_apres_abattements`
	* `smic55` -> `autonomie_financiere`
	* `statut_occupation_famille` -> `statut_occupation_logement_famille`
	* `statut_occupation_individu` -> `statut_occupation_logement_i`
	* `statut_occupation_logement_i` -> `statut_occupation_logement_individu`
	* `statut_occupation` -> `statut_occupation_logement`
	* `tns_employe` -> `tns_avec_employe`
	* `tspr` -> `traitements_salaires_pensions_rentes`
	* `type_sal` -> `categorie_salarie`

### 0.5.5 [diff](https://github.com/openfisca/openfisca-france/compare/0.5.4.3...0.5.5)

* Prime d'activité fiabilization
* Implementation of Indemnite de fin de contrat
* Prolongation of aidper, credit_impots, reductions
* Remove detailes logs in CI
* Update prestations parameters (2016/04/01 revalorisation)
* Add net -> brut reform

#### 0.5.4.2, 0.5.4.3 [diff](https://github.com/openfisca/openfisca-france/compare/0.5.4.1...0.5.4.3)

* Update OpenFisca-Core requirement version

#### 0.5.4.1 [diff](https://github.com/openfisca/openfisca-france/compare/0.5.4...0.5.4.1)

* Add missing assets for versement_transport

### 0.5.4 [diff](https://github.com/openfisca/openfisca-france/compare/0.5.3...0.5.4)

* Many updates

### 0.5.3 [diff](https://github.com/openfisca/openfisca-france/compare/0.5.2...0.5.3)

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

### 0.5.2 [diff](https://github.com/openfisca/openfisca-france/compare/0.5.1...0.5.2)

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

### 0.5.1 [diff](https://github.com/openfisca/openfisca-france/compare/0.5.0...0.5.1)

* Remove scipy by default

## 0.5.0

* First release uploaded to PyPI
