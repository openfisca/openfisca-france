#! /usr/bin/env bash

set -m
shopt -s globstar
dir=($(ls -d tests/**/*.{yaml,yml}))
final_list=()
len_dir=${#dir[@]}

for i in $(seq 1 $len_dir); do
  index_file=$(($i % ${CI_NODE_TOTAL}))
  if [[ $index_file -eq ${CI_NODE_INDEX} ]]
  then
    final_list+=" ${dir[$i]}"
  fi
done

openfisca test $final_list
