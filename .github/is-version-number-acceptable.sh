#! /usr/bin/env bash

if [[ ${GITHUB_REF#refs/heads/} == master ]]
then
    echo "No need for a version check on master."
    exit 0
fi

if ! $(dirname "$BASH_SOURCE")/has-functional-changes.sh
then
    echo "No need for a version update."
    exit 0
fi

current_version=`python setup.py --version`

if git rev-parse --verify --quiet $current_version
then
    echo "Version $current_version already exists in commit:"
    git --no-pager log -1 $current_version
    echo
    echo "Update the version number in setup.py before merging this branch into master."
    echo "Look at the CONTRIBUTING.md file to learn how the version number should be updated."
    exit 1
fi

if ! $(dirname "$BASH_SOURCE")/has-functional-changes.sh | grep --quiet CHANGELOG.md
then
    echo "CHANGELOG.md has not been modified, while functional changes were made."
    echo "Explain what you changed before merging this branch into master."
    echo "Look at the CONTRIBUTING.md file to learn how to write the changelog."
    exit 2
fi
