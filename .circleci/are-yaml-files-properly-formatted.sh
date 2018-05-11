#! /usr/bin/env bash

python openfisca_france/scripts/yaml_round_trip.py $@

if ! git diff-index --name-only --exit-code HEAD -- $@
then
    echo "This or those files are not appropriately formatted."
    echo "Run openfisca_france/scripts/yaml_round_trip.py to format files and git diff to see the differences."
    exit 3
fi
