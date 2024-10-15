#! /usr/bin/env bash

git tag `python setup.py --version`
git push --tags  # update the repository version
