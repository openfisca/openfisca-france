#! /usr/bin/env bash

RED='\033[0;31m'
BLUE='\033[0;34m'
COLOR_RESET='\033[0m'


# openfisca-france expected paths for parameters
EXPECTED_PATHS=(
    "openfisca_france"
    "openfisca_france/parameters"    
    "openfisca_france/parameters/chomage"
    "openfisca_france/parameters/chomage/allocation_retour_emploi"
    "openfisca_france/parameters/chomage/allocations_assurance_chomage"
    "openfisca_france/parameters/chomage/allocations_chomage_solidarite"
    "openfisca_france/parameters/chomage/preretraites"
    "openfisca_france/parameters/geopolitique"
    "openfisca_france/parameters/impot_revenu"
    "openfisca_france/parameters/marche_travail"
    "openfisca_france/parameters/marche_travail/epargne"
    "openfisca_france/parameters/marche_travail/remuneration_dans_fonction_publique"
    "openfisca_france/parameters/marche_travail/salaire_minimum"
    "openfisca_france/parameters/prelevements_sociaux"
    "openfisca_france/parameters/prelevements_sociaux/autres_taxes_participations_assises_salaires"
    "openfisca_france/parameters/prelevements_sociaux/contributions_assises_specifiquement_accessoires_salaire"
    "openfisca_france/parameters/prelevements_sociaux/contributions_sociales"
    "openfisca_france/parameters/prelevements_sociaux/cotisations_regime_assurance_chomage"
    "openfisca_france/parameters/prelevements_sociaux/cotisations_secteur_public"
    "openfisca_france/parameters/prelevements_sociaux/cotisations_securite_sociale_regime_general"
    "openfisca_france/parameters/prelevements_sociaux/cotisations_taxes_independants_artisans_commercants"
    "openfisca_france/parameters/prelevements_sociaux/cotisations_taxes_professions_liberales"
    "openfisca_france/parameters/prelevements_sociaux/pss"
    "openfisca_france/parameters/prelevements_sociaux/reductions_cotisations_sociales"
    "openfisca_france/parameters/prelevements_sociaux/regimes_complementaires_retraite_secteur_prive"
    "openfisca_france/parameters/prestations_sociales"
    "openfisca_france/parameters/prestations_sociales/aides_jeunes"
    "openfisca_france/parameters/prestations_sociales/aides_logement"
    "openfisca_france/parameters/prestations_sociales/fonc"
    "openfisca_france/parameters/prestations_sociales/prestations_etat_de_sante"
    "openfisca_france/parameters/prestations_sociales/prestations_etat_de_sante/invalidite"
    "openfisca_france/parameters/prestations_sociales/prestations_etat_de_sante/perte_autonomie_personnes_agees"
    "openfisca_france/parameters/prestations_sociales/prestations_familiales"
    "openfisca_france/parameters/prestations_sociales/prestations_familiales/bmaf"
    "openfisca_france/parameters/prestations_sociales/prestations_familiales/def_biactif"
    "openfisca_france/parameters/prestations_sociales/prestations_familiales/def_pac"
    "openfisca_france/parameters/prestations_sociales/prestations_familiales/education_presence_parentale"
    "openfisca_france/parameters/prestations_sociales/prestations_familiales/logement_cadre_vie"
    "openfisca_france/parameters/prestations_sociales/prestations_familiales/petite_enfance"
    "openfisca_france/parameters/prestations_sociales/prestations_familiales/prestations_generales"
    "openfisca_france/parameters/prestations_sociales/solidarite_insertion"
    "openfisca_france/parameters/prestations_sociales/solidarite_insertion/autre_solidarite"
    "openfisca_france/parameters/prestations_sociales/solidarite_insertion/minima_sociaux"
    "openfisca_france/parameters/prestations_sociales/solidarite_insertion/minimum_vieillesse"
    "openfisca_france/parameters/prestations_sociales/transport"
    "openfisca_france/parameters/taxation_capital"
    "openfisca_france/parameters/taxation_capital/impot_fortune_immobiliere_ifi_partir_2018"
    "openfisca_france/parameters/taxation_capital/impot_grandes_fortunes_1982_1986"
    "openfisca_france/parameters/taxation_capital/impot_solidarite_fortune_isf_1989_2017"
    "openfisca_france/parameters/taxation_capital/prelevement_forfaitaire"
    "openfisca_france/parameters/taxation_capital/prelevements_sociaux"
    "openfisca_france/parameters/taxation_indirecte"
    "openfisca_france/parameters/taxation_societes"
    )
EXPECTED_PATHS_MAX_DEPTH=4  # ! EXPECTED_PATHS and EXPECTED_PATHS_MAX_DEPTH should be consistent


# compare with last published git tag: 
# list indexed parameters paths indexd in current branch according to EXPECTED_PATHS_MAX_DEPTH
BRANCH_PATHS_ROOT="openfisca_france/parameters/"
last_tagged_commit=`git describe --tags --abbrev=0 --first-parent`  # --first-parent ensures we don't follow tags not published in master through an unlikely intermediary merge commit
checked_tree=`git ls-tree ${last_tagged_commit} -d --name-only -r ${BRANCH_PATHS_ROOT} | cut -d / -f-${EXPECTED_PATHS_MAX_DEPTH} | uniq`


# compare current indexed parameters tree with EXPECTED_PATHS
all_paths=`echo ${EXPECTED_PATHS[@]} ${checked_tree[@]} | tr ' ' '\n' | sort | uniq -D | uniq`
error_status=0

added=`echo ${all_paths[@]} ${checked_tree[@]} | tr ' ' '\n' | sort | uniq -u | uniq`
if [[ ${added[@]} ]]; then
    echo "${BLUE}INFO Ces répertoires de paramètres ont été ajoutés :${COLOR_RESET}"
    printf '%s\n' ${added}
    error_status=1
fi

lost=`echo ${all_paths[@]} ${EXPECTED_PATHS[@]} | tr ' ' '\n' | sort | uniq -u | uniq`
if [[ ${added[@]} ]]; then
    echo "${BLUE}INFO Ces répertoires de paramètres ont été supprimés :${COLOR_RESET}"
    printf '%s\n' "${lost[@]}"
    error_status=2
fi


if [[ ${error_status} ]]; then
    echo "${RED}ERREUR L'arborescence des paramètres a été modifiée.${COLOR_RESET}"
    echo "Elle est commune à openfisca-france et aux Barèmes IPP sur ${EXPECTED_PATHS_MAX_DEPTH} niveaux." 
    echo "Corriger les écarts constatés ci-dessus ou proposer la modification de cette arborescence commune"
    echo "dans une nouvelle issue : https://github.com/openfisca/openfisca-france/issues/new"
    echo "Pour en savoir plus : https://github.com/openfisca/openfisca-france/issues/1811"
fi
exit ${error_status}
