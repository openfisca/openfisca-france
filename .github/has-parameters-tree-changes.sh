#! /usr/bin/env bash

PURPLE='\033[0;95m'
CYAN='\033[0;36m'
COLOR_RESET='\033[0m'


EXPECTED_PATHS=(
    "lost_path_test"
    "openfisca_france/parameters/impot_revenu"
    "openfisca_france/parameters/marche_travail"
    )
EXPECTED_PATHS_MAX_DEPTH=3  # EXPECTED_PATHS and EXPECTED_PATHS_MAX_DEPTH should be consistent


# list git indexed parameters paths according to checked depth
checked_tree_root="openfisca_france/parameters/"
last_tagged_commit=`git describe --tags --abbrev=0 --first-parent`  # --first-parent ensures we don't follow tags not published in master through an unlikely intermediary merge commit
checked_tree=`git ls-tree ${last_tagged_commit} -d --name-only -r ${checked_tree_root} | cut -d / -f-${EXPECTED_PATHS_MAX_DEPTH} | uniq`

# compare current parameters tree with EXPECTED_PATHS
all_paths=`echo ${EXPECTED_PATHS[@]} ${checked_tree[@]} | tr ' ' '\n' | sort | uniq -D | uniq`

added=`echo ${all_paths[@]} ${checked_tree[@]} | tr ' ' '\n' | sort | uniq -u | uniq` 
if [[ ${added[@]} ]]; then
    echo "${CYAN}The current branch adds the following directories:${COLOR_RESET}"

    added_array=(${added})
    if [[ ${added_array[0]} == "openfisca_france" && ${added_array[1]} == "openfisca_france/parameters" ]]; then
        printf '%s\n' "${added_array[@]:$((2))}"
    fi
fi


lost=`echo ${all_paths[@]} ${EXPECTED_PATHS[@]} | tr ' ' '\n' | sort | uniq -u | uniq`
if [[ ${added[@]} ]]; then
    echo "${PURPLE}The current branch removes the following directories:${COLOR_RESET}"
    printf '%s\n' "${lost[@]}"
fi
