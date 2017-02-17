#! /usr/bin/env bash

current_version=`python setup.py --version`

if ! git diff-index --quiet master openfisca_france
then
    if [[ "$TRAVIS_BRANCH" == "master" && "$TRAVIS_PULL_REQUEST" != false ]]
    then
        if git rev-parse $current_version
        then
            set +x
            echo "Version $version already exists. Please update version number in setup.py before merging this branch into master."
            exit 1
        fi

        if git diff-index master --quiet CHANGELOG.md
        then
            set +x
            echo "CHANGELOG.md has not been modified. Please update it before merging this branch into master."
            exit 1
        fi
    fi
fi

make test
