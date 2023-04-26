#! /usr/bin/env bash

RED='\033[0;31m'
BLUE='\033[0;34m'
COLOR_RESET='\033[0m'


# openfisca-france array of expected _directories_ paths for parameters (no duplicates)
EXPECTED_PATHS=(
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

get_path_depth(){
    # trim last slash in path string and count remaining slashes
    # usage: get_path_depth "openfisca_france/parameters/taxation_indirecte/taxes_tabacs/"
    local path_string="$1"
    echo ${path_string%/} | grep -o / | wc -l
}


get_max_paths_depth(){
    # get longer path depth in an array of string paths
    # usage: get_max_paths_depth "${array_of_string_paths[@]}"
    # where array_of_string_paths is expanded to get the right and full sequence of items
    local paths_strings_array=("$@")
    local max_path_depth=-1
    for p in "${paths_strings_array[@]}"; do
        # echo $p
        depth=`get_path_depth $p`
        if [ $depth -gt $max_path_depth ]; then
            max_path_depth=$depth
        fi
    done
    echo $max_path_depth
}


# compare local parameters tree with EXPECTED_PATHS
error_status=0
PARAMETERS_PATHS_ROOT="openfisca_france/parameters"
expected_paths_max_depth=`get_max_paths_depth "${EXPECTED_PATHS[@]}"`
local_parameters=`find $PARAMETERS_PATHS_ROOT -type d -maxdepth $expected_paths_max_depth | sort` 


check_change(){
    local dirpath="$1"
    local parent=`dirname $dirpath`
    local matching_expected_paths=( `echo ${EXPECTED_PATHS[@]} | tr ' ' '\n' | grep ${parent}` )

    if [[ ${matching_expected_paths[@]} ]]; then
        local matching_count="${#matching_expected_paths[@]}"
        
        local i=0
        local expected_path=""
        while [ $i -lt $matching_count ]; do
            expected_path="${matching_expected_paths[$i]}"
            if [ $expected_path != $parent ]; then
                echo $dirpath
                break
            fi
            ((i++))
        done         
    fi 
}

added=`echo ${EXPECTED_PATHS[@]} ${EXPECTED_PATHS[@]} ${local_parameters[@]} | tr ' ' '\n' | sort | uniq -u`
added_checked=()
if [[ ${added[@]} ]]; then
    for path in $added; do
        added_checked+=(`check_change $path`)
    done
fi
if [[ ${added_checked[@]} ]]; then
    echo "${BLUE}INFO Ces répertoires de paramètres ont été ajoutés :${COLOR_RESET}"
    printf '%s\n' ${added_checked[@]}
    error_status=1
fi

lost=`echo ${local_parameters[@]} ${local_parameters[@]} ${EXPECTED_PATHS[@]} | tr ' ' '\n' | sort | uniq -u`
if [[ ${lost[@]} ]]; then
    echo "${BLUE}INFO Ces répertoires de paramètres ont été supprimés :${COLOR_RESET}"
    printf '%s\n' ${lost[@]}
    error_status=2
fi


if [[ ${error_status} -gt 0 ]]; then
    echo "${RED}ERREUR L'arborescence des paramètres a été modifiée.${COLOR_RESET}"
    echo "Elle est commune à openfisca-france et aux Barèmes IPP sur les premiers niveaux de répertoires." 
    echo "Corriger les écarts constatés ci-dessus ou proposer la modification de cette arborescence commune"
    echo "dans une nouvelle issue : https://github.com/openfisca/openfisca-france/issues/new"
    echo "Pour en savoir plus : https://github.com/openfisca/openfisca-france/issues/1811"
else
    echo "Merci. La validité de l'arborescence des paramètres est maintenue."
fi
exit ${error_status}
