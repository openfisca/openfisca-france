#! /usr/bin/env bash

# This script is the entry point for the Travis tests platform.
# It allows Travis to checkout on OpenFisca-Core the git branch with the same name than the tested branch,
# so that the pull-request merge status remains valid.


set -x

current_version=`python setup.py --version`
if [ $TRAVIS_PULL_REQUEST = true ]
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


if [[ "$TRAVIS_BRANCH" != "master" && -z "$TRAVIS_TAG" ]]
then
  OPENFISCA_CORE_DIR=`python -c "import pkg_resources; print pkg_resources.get_distribution('OpenFisca-Core').location"`
  pushd "$OPENFISCA_CORE_DIR"
  git checkout "$TRAVIS_BRANCH"
  popd
fi


echo "Pretending to be making test..."
