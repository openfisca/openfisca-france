#! /usr/bin/env bash

last_tagged_commit=`git describe --tags --abbrev=0 --first-parent`  # --first-parent ensures we don't follow tags not published in master through an unlikely intermediary merge commit
# last_tagged_commit="dd99f9bf357c2f438d62a1a025b8e56c4f9261d2"

checked_tree_root="openfisca_france/parameters/"
checked_tree_depth=3
checked_tree=`git ls-tree ${last_tagged_commit} -d --name-only -r ${checked_tree_root} | cut -d / -f-${checked_tree_depth} | uniq`

# echo ${checked_tree}

pattern=(
    "pattern_test"
    "openfisca_france/parameters/impot_revenu"
    "openfisca_france/parameters/marche_travail"
    )

# echo ${pattern}

# uniq -u : lignes non répétées (ajouts ?)
# uniq -D : lignes répétées (pas de suppression ?)
# uniq -d : lignes répétées, print unique

common=`echo ${pattern[@]} ${checked_tree[@]} | tr ' ' '\n' | sort | uniq -D | uniq`
# echo ${common}

# ajouts sur la branche par rapport au pattern
added=`echo ${common[@]} ${checked_tree[@]} | tr ' ' '\n' | sort | uniq -u | uniq`
# printf '%s\n' "${added[@]}"

# hypothèse : le pattern est de même profondeur maximale que checked_tree_depth
lost=`echo ${common[@]} ${pattern[@]} | tr ' ' '\n' | sort | uniq -u | uniq`
printf '%s\n' "${lost[@]}"
