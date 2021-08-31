#! /usr/bin/env bash

last_tagged_commit=`git describe --tags --abbrev=0 --first-parent`  # --first-parent ensures we don't follow tags not published in master through an unlikely intermediary merge commit

if ! changes=$(git diff-index --name-only --diff-filter=ACMR --exit-code $last_tagged_commit -- "*.py")
then
  echo "Linting the following Python files:"
  echo $changes
  flake8 $changes
else echo "No changed Python files to lint"
fi
