#! /usr/bin/env bash

current_version=`python setup.py --version`

make test

# This part is executed only when merging a branch in master.
if [[ "$TRAVIS_BRANCH" == "master" && "$TRAVIS_PULL_REQUEST" != false ]]; then
    # A version bump is requested by default, except:
    # - when changing a Markdown (.md) file
    # - or when only blank lines are added/removed

    # Note: git diff-index does not work with --ignore-blank-lines option.
    bumping_changes=`git --no-pager diff --ignore-blank-lines master openfisca_france | grep "^diff" | grep -v "\.md$"`

    if [[ -n "$bumping_changes" ]]; then
        if git rev-parse $current_version; then
            set +x
            echo "Version $current_version already exists. Please update version number in setup.py before merging this branch into master."
            exit 1
        fi

        if git diff-index master --quiet CHANGELOG.md; then
            set +x
            echo "CHANGELOG.md has not been modified. Please update it before merging this branch into master."
            exit 1
        fi
    fi
fi
