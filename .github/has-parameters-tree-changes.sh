#! /usr/bin/env bash

PURPLE='\033[0;95m'
CYAN='\033[0;36m'
COLOR_RESET='\033[0m'

last_tagged_commit=`git describe --tags --abbrev=0 --first-parent`  # --first-parent ensures we don't follow tags not published in master through an unlikely intermediary merge commit

pattern=(
    "pattern_test"
    "openfisca_france/parameters/impot_revenu"
    "openfisca_france/parameters/marche_travail"
    )

checked_tree_depth=3
checked_tree_root="openfisca_france/parameters/"
checked_tree=`git ls-tree ${last_tagged_commit} -d --name-only -r ${checked_tree_root} | cut -d / -f-${checked_tree_depth} | uniq`

common=`echo ${pattern[@]} ${checked_tree[@]} | tr ' ' '\n' | sort | uniq -D | uniq`

# ajouts sur la branche par rapport au pattern
added=`echo ${common[@]} ${checked_tree[@]} | tr ' ' '\n' | sort | uniq -u | uniq`
 
if [[ ${added[@]} ]]; then
    echo "${CYAN}The current branch adds the following directories:${COLOR_RESET}"

    added_array=(${added})
    if [[ ${added_array[0]} == "openfisca_france" && ${added_array[1]} == "openfisca_france/parameters" ]]; then
        printf '%s\n' "${added_array[@]:$((2))}"
    fi
fi

# hypothèse : le pattern est de même profondeur maximale que checked_tree_depth
lost=`echo ${common[@]} ${pattern[@]} | tr ' ' '\n' | sort | uniq -u | uniq`
if [[ ${added[@]} ]]; then
    echo "${PURPLE}The current branch removes the following directories:${COLOR_RESET}"
    printf '%s\n' "${lost[@]}"
fi
