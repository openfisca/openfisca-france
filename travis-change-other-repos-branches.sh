#! /usr/bin/env bash

# This script allows Travis to checkout on OpenFisca-Core the git branch with the same name than the tested branch.
# We do that to allow the development of features which involve cross-repositories code modifications.


if [[ "$TRAVIS_BRANCH" != "master" && -z "$TRAVIS_TAG" ]]
then
    OPENFISCA_CORE_DIR=`python -c "import pkg_resources; print pkg_resources.get_distribution('OpenFisca-Core').location"`
    pushd "$OPENFISCA_CORE_DIR"
    git checkout "$TRAVIS_BRANCH" && pip install --editable .
    popd
fi
