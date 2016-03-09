#! /usr/bin/env bash

# This script is the entry point for the Travis tests platform.
# It allows Travis to checkout on OpenFisca-Core the git branch with the same name than the tested branch,
# so that the pull-request merge status remains valid.


set -x


if [ "$TRAVIS_BRANCH" != "master" ]; then
  OPENFISCA_CORE_DIR=`python -c "import pkg_resources; print pkg_resources.get_distribution('OpenFisca-Core').location"`
  pushd "$OPENFISCA_CORE_DIR"
  git checkout "$TRAVIS_BRANCH"
  popd
fi


make test
