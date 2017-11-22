#! /usr/bin/env bash

VERSION_CHANGE_TRIGGERS="setup.py MANIFEST.in openfisca_france"

current_version=`python setup.py --version`

if git diff-index --quiet origin/master -- $VERSION_CHANGE_TRIGGERS ":(exclude)*.md"
then exit 0  # there are no functional changes at all, the version is correct
fi

if git rev-parse --verify --quiet $current_version
then
    echo "Version $current_version already exists:"
    git --no-pager log -1 $current_version
    echo
    echo "Update the version number in setup.py before merging this branch into master."
    echo "Look at the CONTRIBUTING.md file to learn how the version number should be updated."
    exit 1
fi

if git diff-index --quiet origin/master CHANGELOG.md
then
    echo "CHANGELOG.md has not been modified, while the code has changed."
    echo "Explain what you changed before merging this branch into master."
    echo "Look at the CONTRIBUTING.md file to learn how to write the changelog."
    exit 2
fi
