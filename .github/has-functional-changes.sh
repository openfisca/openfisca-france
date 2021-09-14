#! /usr/bin/env bash

IGNORE_DIFF_ON="README.md CONTRIBUTING.md Makefile .gitignore .github/*"

last_tagged_commit=`git describe --tags --abbrev=0 --first-parent`  # --first-parent ensures we don't follow tags not published in master through an unlikely intermediary merge commit

if git diff-index --name-only --exit-code $last_tagged_commit -- . `echo " $IGNORE_DIFF_ON" | sed 's/ / :(exclude)/g'`  # Check if any file that has not be listed in IGNORE_DIFF_ON has changed since the last tag was published.
then
  echo "No functional changes detected."
  exit 1
else echo "The functional files above were changed."
fi
