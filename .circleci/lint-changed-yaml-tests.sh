#! /usr/bin/env bash

last_tagged_commit=`git describe --tags --abbrev=0 --first-parent`  # --first-parent ensures we don't follow tags not published in master through an unlikely intermediary merge commit

if ! changes=$(git diff-index --name-only --diff-filter=ACMR --exit-code $last_tagged_commit -- "tests/*.yaml")
then
  echo "Hello boss, I'm linting the following changed files:"
  echo $changes
  yamllint $changes
else echo "Could't find changed files, come visit again!"
fi
