#! /usr/bin/env bash

RED='\033[0;31m'
BLUE='\033[0;34m'
COLOR_RESET='\033[0m'


# openfisca-france array of expected _directories_ paths for parameters (without trailing slash)
EXPECTED_PATHS=(
    "openfisca_france"
    "openfisca_france/parameters"    
    "openfisca_france/parameters/chomage"
    "openfisca_france/parameters/chomage/allocation_retour_emploi"
    "openfisca_france/parameters/chomage/allocations_assurance_chomage"
    "openfisca_france/parameters/chomage/allocations_chomage_solidarite"
    "openfisca_france/parameters/chomage/preretraites"
    "openfisca_france/parameters/geopolitique"  # premier niveau bloqué seulement ; n'existe pas dans les barèmes IPP
    "openfisca_france/parameters/impot_revenu"
    "openfisca_france/parameters/impot_revenu/anciens_baremes_igr"
    "openfisca_france/parameters/impot_revenu/bareme_ir_depuis_1945"
    "openfisca_france/parameters/impot_revenu/calcul_impot_revenu"
    "openfisca_france/parameters/impot_revenu/calcul_reductions_impots"
    "openfisca_france/parameters/impot_revenu/calcul_revenus_imposables"
    "openfisca_france/parameters/impot_revenu/contributions_exceptionnelles"
    "openfisca_france/parameters/impot_revenu/credits_impots"
    "openfisca_france/parameters/marche_travail"
    "openfisca_france/parameters/marche_travail/epargne"  # bloqué mais n'existe pas dans les barèmes IPP
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
    "openfisca_france/parameters/prelevements_sociaux/pss"  # bloqué mais est un dispositif législatif, pas une catégorie métier
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
    "openfisca_france/parameters/prestations_sociales/prestations_familiales/bmaf"  # bloqué mais est un dispositif législatif, pas une catégorie métier
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
    "openfisca_france/parameters/taxation_indirecte/alcools_autres_boissons"
    "openfisca_france/parameters/taxation_indirecte/produits_energetiques"
    "openfisca_france/parameters/taxation_indirecte/taxe_habitation"
    "openfisca_france/parameters/taxation_indirecte/taxes_assurances"
    "openfisca_france/parameters/taxation_indirecte/taxes_energie_dans_logement"
    "openfisca_france/parameters/taxation_indirecte/taxes_tabacs"
    "openfisca_france/parameters/taxation_indirecte/tva"
    "openfisca_france/parameters/taxation_societes"  # premier niveau bloqué seulement ; à harmoniser avec les barèmes IPP
    )


# get last published git tag
# --first-parent ensures we don't follow tags not published in master through an unlikely intermediary merge commit 
last_tagged_commit=`git describe --tags --abbrev=0 --first-parent`

# compare indexed parameters diff tree with EXPECTED_PATHS
BRANCH_PATHS_ROOT="openfisca_france/parameters/"

# MEMO list indexed files: git ls-files openfisca_france/parameters/
error_status=0

check_change(){
    local item_path="$1"
    
    # item_path is a change in the GIT indexed items; it's a file because GIT doesn't index empty directories
    # we compare its parent directory with EXPECTED_PATHS list
    local item_parent=`dirname $item_path`
    local item_parent_depth=`echo $item_parent | grep -o / | wc -l`

    # does EXPECTED_PATHS contain the parent directory?
    local matching_expected_paths=`echo ${EXPECTED_PATHS[@]} | tr ' ' '\n' | grep ${item_parent}`
    local matching_expected_paths_array=($matching_expected_paths)
  
    if [[ ${matching_expected_paths_array[@]} ]]; then  
        local list_length=`echo "$matching_expected_paths"  | wc -l`
        local j=0

        # look into each EXPECTED_PATHS containing item_parent
        # its path is as long or longer than item_parent path length 
        while [ $j -lt $list_length ]; do
            local expected_item_depth=`echo ${matching_expected_paths_array[$j]} | grep -o / | wc -l`

            if [ $expected_item_depth -eq $item_parent_depth ]; then
                break
            else
                # EXPECTED_PATHS contains a directory longer than current item directory's path
                # list current item directory as a change in the tree hierarchy
                echo $item_parent
            fi
            ((j++))
        done
    else
        # the parent directory is new! it looks like the top tree hierarchy was changed
        # list it as a change in the tree hierarchy as its path doesn't match any directory path of EXPECTED_PATHS
        echo $item_parent           
    fi 
}

added=`git diff-index --name-only --diff-filter=A --exit-code ${last_tagged_commit}  -- ${BRANCH_PATHS_ROOT}`
added_checked=()
if [[ ${added[@]} ]]; then
    for item_path in $added; do
        result=`check_change $item_path`
        added_checked+=($result)
    done
fi
if [[ ${added_checked[@]} ]]; then
    echo "${BLUE}INFO Ces répertoires de paramètres ont été ajoutés :${COLOR_RESET}"
    printf '%s\n' ${added_checked[@]}
    error_status=1
fi

lost=`git diff-index --name-only --diff-filter=D --exit-code ${last_tagged_commit}  -- ${BRANCH_PATHS_ROOT}`
lost_checked=()
if [[ ${lost[@]} ]]; then
    for item_path in $lost; do
        result=`check_change $item_path`
        lost_checked+=($result)
    done
fi
if [[ ${lost_checked[@]} ]]; then
    echo "${BLUE}INFO Ces répertoires de paramètres ont été supprimés :${COLOR_RESET}"
    printf '%s\n' ${lost_checked[@]}
    error_status=2
fi


if [[ ${error_status} -gt 0 ]]; then
    echo "${RED}ERREUR L'arborescence des paramètres a été modifiée.${COLOR_RESET}"
    echo "Elle est commune à openfisca-france et aux Barèmes IPP sur les premiers niveaux de répertoires." 
    echo "Corriger les écarts constatés ci-dessus ou proposer la modification de cette arborescence commune"
    echo "dans une nouvelle issue : https://github.com/openfisca/openfisca-france/issues/new"
    echo "Pour en savoir plus : https://github.com/openfisca/openfisca-france/issues/1811"
fi
exit ${error_status}
