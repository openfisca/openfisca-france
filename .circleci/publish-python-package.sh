#! /usr/bin/env bash

python setup.py bdist_wheel  # build this package in the dist directory
twine upload dist/* --username $PYPI_USERNAME --password $PYPI_PASSWORD  # publish
