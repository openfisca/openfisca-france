# Changelog

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
	* `aide_logement_participation_personelle`

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
