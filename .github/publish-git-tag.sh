#! /usr/bin/env bash

current_version=$(grep '^version =' pyproject.toml | cut -d '"' -f 2)  # parsing with tomllib is complicated, see https://github.com/python-poetry/poetry/issues/273
git tag $current_version
git push --tags  # update the repository version
